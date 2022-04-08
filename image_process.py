import cv2 as cv
import numpy as np
from imutils import contours

def findTableLine(input_image):
    blur_image = cv.GaussianBlur(input_image, (5, 5), cv.BORDER_DEFAULT)
    threshold, bin_image = cv.threshold(blur_image, 128, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    # cv.imshow('binary image', bin_image)

    vertical_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, np.array(input_image).shape[1] // 100))
    eroded_image = cv.erode(bin_image, vertical_kernel, iterations=3)
    vertical_lines = cv.dilate(eroded_image, vertical_kernel, iterations=3)
    # cv.imshow('vertical line', vertical_lines)

    horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (np.array(input_image).shape[1] // 40, 1))
    eroded_image = cv.erode(bin_image, horizontal_kernel, iterations=3)
    horizontal_lines = cv.dilate(eroded_image, horizontal_kernel, iterations=3)
    # cv.imshow('horizontal line', horizontal_lines)

    table_line = vertical_lines | horizontal_lines
    kernel = np.ones((3,3), np.uint8)
    table_line = cv.dilate(table_line, kernel, iterations=1)
    # cv.imshow('final', table_line)
    # cv.waitKey(0)

    return table_line

def getApproxRectImage(input_image, cnt):
    # img_1 = np.zeros([input_image.shape[1], input_image.shape[0], 1], dtype=np.uint8)
    # img_1.fill(255)

    peri = cv.arcLength(cnt, True)
    approxPoints = cv.approxPolyDP(cnt, 0.005*peri, True)
    # cv.polylines(img_1, [approxPoints], True, (0,0,255), 3)
    # cv.imshow('approx', img_1)
    # cv.waitKey(0)

    (x, y, w, h) = cv.boundingRect(approxPoints)
    approxPoints = approxPoints[:, 0, :].astype('float32')

    # order by top-left, top-right, bottom-left, bottm-right
    # https://pyimagesearch.com/2016/03/21/ordering-coordinates-clockwise-with-python-and-opencv/
    orderPoints = np.zeros((4, 2), dtype="float32")
    s = approxPoints.sum(axis=1)
    orderPoints[0] = approxPoints[np.argmin(s)]
    orderPoints[3] = approxPoints[np.argmax(s)]

    diff = np.diff(approxPoints, axis=1)
    orderPoints[1] = approxPoints[np.argmin(diff)]
    orderPoints[2] = approxPoints[np.argmax(diff)]
    
    transformedPoints = np.float32([[0,0],[w,0],[0,h],[w,h]])
    # for point in transformedPoints:
    #     cv.circle(img_2, (int(point[0]), int(point[1])), 10, (0,0,255), 3)
    #     cv.imshow('circle2', img_2)
    #     cv.waitKey(0)
    trans_matrix = cv.getPerspectiveTransform(orderPoints, transformedPoints)
    approxRectImage = cv.warpPerspective(input_image, trans_matrix, (w,h))
    # cv.imshow('dst', dst)
    # cv.waitKey(0)
    return approxRectImage

def getBoxCBList(input_image, table_line, isSeggestion=False):
    cnts = 0
    if isSeggestion:
        cnts, _ = cv.findContours(table_line, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    else:
        cnts, _ = cv.findContours(table_line, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
    cnts, boundingBoxes = contours.sort_contours(cnts, method="top-to-bottom")
    
    # print('number of found boundingBox: ', len(boundingBoxes))

    # img_1 = np.zeros([input_image.shape[0], input_image.shape[1], 1], dtype=np.uint8)
    # img_1.fill(255)
    # for bbox in boundingBoxes:
    #     (x, y, w, h) = bbox
    #     cv.rectangle(img_1, (x, y), (x+w, y+h), (0, 0, 255), 2)
    #     cv.imshow('count table', img_1)
    #     cv.waitKey(0)

    # sort boundingbox by (y) center point
    zipCB = list(zip(cnts, boundingBoxes))
    if not isSeggestion:
        zipCB = filter(lambda x: x[1][3] < input_image.shape[0] // 5, zipCB)
        zipCB = sorted(zipCB, key=lambda x: x[1][1]+x[1][3]/2)
    
    # boundingBox = list(filter(lambda x: x[3] < input_image.shape[0] // 5, boundingBox))
    # boundingBox = sorted(boundingBox, key=lambda x: x[1]+x[3]/2)
    
    lastCenter, offset = 0, 10
    boxCBList, row = list(), list()
    for i, (cnt, boundingBox) in enumerate(zipCB):
        center = boundingBox[1] + boundingBox[3]/2
        if i == 0:
            row = [(cnt, boundingBox)]
        elif abs(lastCenter - center) > offset:
            row = sorted(row, key=lambda x: x[1][0])
            boxCBList.append(row)
            row = [(cnt, boundingBox)]
        else:
            row.append((cnt, boundingBox))
        lastCenter = center
        # if the last element -> append to boxCBList
        if i == len(zipCB) - 1:
            boxCBList.append(row)

        # img_1 = np.zeros([input_image.shape[0], input_image.shape[1], 1], dtype=np.uint8)
        # img_1.fill(255)
        # (x, y, w, h) = boundingBox
        # cv.rectangle(img_1, (x, y), (x+w, y+h), (0, 0, 255), 2)
        # cv.imshow('count table', img_1)
        # cv.waitKey(0)
    return boxCBList
