import cv2 as cv
import numpy as np

from image_process import getApproxRectImage

def findBigCheckAns(input_image, boxCBList, big_check_index, answer_image):
    big_check_list = list()
    for i in big_check_index:
        boxCBList[i] = filter(lambda x: x[1][2] < input_image.shape[1] // 3, boxCBList[i])
        boxCBList[i] = sorted(boxCBList[i], key=lambda x: x[1][0])
        big_check_list.append(boxCBList[i])

    blur_image = cv.GaussianBlur(input_image, (5, 5), cv.BORDER_DEFAULT)
    adaptive_threshold = cv.adaptiveThreshold(blur_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 5, 2)

    # big check part
    ratio_thresh = 0.01
    ans, full_ans = list(), list()
    for questionCBList in big_check_list:
        ans = []
        for checkIdx, (cnt, boundingBox) in enumerate(questionCBList):
            checkBox_image = getApproxRectImage(adaptive_threshold, cnt)
            # cv.imshow('checkImage', checkBox_image)
            # cv.waitKey(0)
               
            right_slope_kernel = np.array([[0,0,1], [0,1,0], [1,0,0]], dtype='uint8')
            eroded_image = cv.erode(checkBox_image, right_slope_kernel, iterations=3)
            checkBox_right = cv.dilate(eroded_image, right_slope_kernel, iterations=6)
            # cv.imshow('q1 right', question1_1_image_right)

            left_right_slope_kernel = np.array([[0,1,0], [0,1,0], [0,0,1]], dtype='uint8')
            eroded_image = cv.erode(checkBox_image, left_right_slope_kernel, iterations=3)
            checkBox_left = cv.dilate(eroded_image, left_right_slope_kernel, iterations=6)
            # cv.imshow('q1 left', question1_1_image_left)

            checkBox_final = checkBox_right | checkBox_left
            # cv.imshow('q1 final', checkBox_final)
            # cv.waitKey(0)

            number_of_white_pix = np.sum(checkBox_final == 255)
            number_of_black_pix = np.sum(checkBox_final == 0)
            ratio = number_of_white_pix / number_of_black_pix
            # print(ratio)
            
            if ratio > ratio_thresh:
                ans.append(checkIdx) 
                (x, y, w, h) = boundingBox
                cv.rectangle(answer_image, (x, y), (x+w, y+h), (0,0,255), 2)
        
        full_ans.append(ans) if ans else full_ans.append([-1])
    return full_ans, answer_image

def findSmallCheckAns(input_image, boxCBList, small_check_index, answer_image):
    small_check_list = list()
    for i in small_check_index:
        small_check_list.append(boxCBList[i])

    small_question_list, checkBox_image_list = list(), list()
    for questionCBList in small_check_list:
        checkBox_image_list = list()
        for (cnt, boundingBox) in questionCBList:
            checkBox_image = getApproxRectImage(input_image, cnt)

            blur_image = cv.GaussianBlur(checkBox_image, (5, 5), cv.BORDER_DEFAULT)
            adaptive_threshold = cv.adaptiveThreshold(blur_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 5, 2)
            
            lWidth = 2
            lineMinWidth = 10

            kernal1h = np.ones((1,lWidth), np.uint8)
            kernal1v = np.ones((lWidth,1), np.uint8)
            kernal6h = np.ones((1,lineMinWidth), np.uint8)
            kernal6v = np.ones((lineMinWidth,1), np.uint8)

            ### finding horizontal lines
            img_bin_h = cv.morphologyEx(~adaptive_threshold, cv.MORPH_CLOSE, kernal1h) # bridge small gap in horizonntal lines
            img_bin_h = cv.morphologyEx(img_bin_h, cv.MORPH_OPEN, kernal6h) # kep ony horiz lines by eroding everything else in hor direction
            
            ## detect vert lines
            img_bin_v = cv.morphologyEx(~adaptive_threshold, cv.MORPH_CLOSE, kernal1v)  # bridge small gap in vert lines
            img_bin_v = cv.morphologyEx(img_bin_v, cv.MORPH_OPEN, kernal6v)# kep ony vert lines by eroding everything else in vert direction
            
            check_box_image = (img_bin_h | img_bin_v)

            ### getting labels
            _, _, stats, _ = cv.connectedComponentsWithStats(~check_box_image, connectivity=8, ltype=cv.CV_32S)
            # cv.imshow('check_box_image', ~check_box_image)
            # cv.waitKey(0)
            # img_1 = np.zeros([checkBox_image.shape[0], checkBox_image.shape[1], 1], dtype=np.uint8)
            # img_1.fill(255)
            # for x,y,w,h, area in stats[2:]:
            #     cv.rectangle(img_1, (x,y), (x+w, y+h), (0,0,255), 1)
            # cv.imshow('imshowrect', img_1)
            # cv.waitKey(0)
            ### drawing recangles for visualisation
            rect_thresh = 100
            checkBox_list = list(filter(lambda x: x[4] > rect_thresh, stats[2:]))
            checkBox_list = [checkBox[:4] for checkBox in checkBox_list] 

            biggestCheckBoxRect_image = np.zeros([checkBox_image.shape[0], checkBox_image.shape[1], 1], dtype=np.uint8)
            biggestCheckBoxRect_image2 = biggestCheckBoxRect_image.copy()
            biggestCheckBoxRect_image3 = biggestCheckBoxRect_image.copy()

            for x, y, w, h in checkBox_list:
                cv.rectangle(biggestCheckBoxRect_image, (x,y), (x+w, y+h), (255,255,255), 1) 
            contours, _ = cv.findContours(biggestCheckBoxRect_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cv.drawContours(biggestCheckBoxRect_image2, contours, -1, (255,255,255), 3)  
            checkBox_list = [cv.boundingRect(c) for c in contours]
            for x, y, w, h in checkBox_list:
                cv.rectangle(biggestCheckBoxRect_image3, (x,y), (x+w, y+h), (255,255,255), 1) 
            _, _, stats, _ = cv.connectedComponentsWithStats(~biggestCheckBoxRect_image3, connectivity=8, ltype=cv.CV_32S)

            rect_thresh = 400
            checkBox_list = list(filter(lambda x: x[4] > rect_thresh, stats[2:]))
            checkBox_list = [checkBox[:4] for checkBox in checkBox_list] 
            
            # for x, y, w, h in checkBox_list:
            #     cv.rectangle(checkBox_image, (x,y), (x+w, y+h), (0,0,255), 1) 
            #     checkBox_image[y:y+h, x:x+w]
            #     cv.imshow('imshowrect', checkBox_image[y:y+h, x:x+w])
            #     cv.waitKey(0)

            # for x,y,w,h,area in stats[2:]:
            #     if area > rect_thresh:
            #         checkBox_list.append((x,y,w,h))
            checkBox_list = sorted(checkBox_list, key=lambda x: x[0])
            checkBox_image_list = [checkBox_image[y:y+h, x:x+w] for (x, y, w, h) in checkBox_list]
        small_question_list.append([checkBox_image_list, boundingBox, checkBox_list])

    ratio_thresh = 0.01
    edgeOffset = 5
    ans, full_ans = list(), list()
    for question in small_question_list:
        ans = []
        (checkBox_image_list, outBBoxCoor, checkBox_list) = question
        for check_index, (image, inBBoxCoor) in enumerate(zip(checkBox_image_list, checkBox_list)):
            
            blur_image = cv.GaussianBlur(image, (5, 5), cv.BORDER_DEFAULT)
            adaptive_threshold = cv.adaptiveThreshold(blur_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 5, 2)
            adaptive_threshold = adaptive_threshold[:-edgeOffset, :-edgeOffset]
            # cv.imshow('testset', adaptive_threshold)
            # cv.waitKey(0)
            right_slope_kernel = np.array([[0,0,1], [0,1,0], [1,0,0]], dtype='uint8')
            eroded_image = cv.erode(adaptive_threshold, right_slope_kernel, iterations=3)
            checkBox_right = cv.dilate(eroded_image, right_slope_kernel, iterations=6)
            # cv.imshow('q1 right', question1_1_image_right)

            left_right_slope_kernel = np.array([[0,1,0], [0,1,0], [0,0,1]], dtype='uint8')
            eroded_image = cv.erode(adaptive_threshold, left_right_slope_kernel, iterations=3)
            checkBox_left = cv.dilate(eroded_image, left_right_slope_kernel, iterations=6)
            # cv.imshow('q1 left', question1_1_image_left)

            checkBox_final = checkBox_right | checkBox_left
            # cv.imshow('q1 final', checkBox_final)
            # cv.waitKey(0)

            number_of_white_pix = np.sum(checkBox_final == 255)
            number_of_black_pix = np.sum(checkBox_final == 0)
            ratio = number_of_white_pix / number_of_black_pix
            
            if ratio > ratio_thresh:
                ans.append(check_index) 
                (x, y, w, h) = inBBoxCoor
                (ox, oy, ow, oh) = outBBoxCoor
                cv.rectangle(answer_image, (ox+x, oy+y), (ox+x+w, oy+y+h), (0,255,0), 2)

        full_ans.append(ans) if ans else full_ans.append([-1])
    return full_ans, answer_image

def findWritenBox(input_image, boxCBList, writen_index, answer_image, start_coord=(0,0)):
    writen_list = list()
    for index, ratio_thresh in writen_index:
        writen_list.append((boxCBList[index], ratio_thresh))

    ans = list()
    for questionCBList, ratio_thresh in writen_list:
        for (cnt, boundingBox) in questionCBList:
            checkBox_image = getApproxRectImage(input_image, cnt)
            
            blur_image = cv.GaussianBlur(checkBox_image, (5, 5), cv.BORDER_DEFAULT)
            checkBox_final = cv.adaptiveThreshold(blur_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 5, 2)
            # cv.imshow('checkbox', checkBox_final)
            # cv.waitKey(0)
            number_of_white_pix = np.sum(checkBox_final == 255)
            number_of_black_pix = np.sum(checkBox_final == 0)
            ratio = number_of_white_pix / number_of_black_pix
            # print(ratio)

            if ratio > ratio_thresh:
                ans.append(checkBox_image) 
                (x, y, w, h) = boundingBox
                sx, sy = start_coord
                cv.rectangle(answer_image, (sx+x, sy+y), (sx+x+w, sy+y+h), (255,0,0), 2)
            else:
                ans.append(np.array([]))               
    return ans, answer_image

