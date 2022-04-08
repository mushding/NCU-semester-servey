import cv2 as cv
from pathlib import Path

from image_process import findTableLine, getBoxCBList
from find_answer import findBigCheckAns, findSmallCheckAns, findWritenBox

def getFrontAns(path, dirPath):   
    raw_image = cv.imread(path)
    crop_image = raw_image[int(raw_image.shape[0] / 4):,:].copy()
    answer_image = crop_image.copy()
    gray_image = cv.cvtColor(crop_image, cv.COLOR_BGR2GRAY)
    table_line = findTableLine(gray_image)
    boxCBList = getBoxCBList(gray_image, table_line)

    # assert len(boxCBList) == 21, "Front image table column is not 21"
    
    big_check_index = [3, 4, 8, 16, 17, 19]
    bigCheckAns, answer_image = findBigCheckAns(gray_image, boxCBList, big_check_index, answer_image)    
    # print('bigCheckAns: ', bigCheckAns)
    
    small_check_index = [5, 7, 10, 12]
    smallCheckAns, answer_image = findSmallCheckAns(gray_image, boxCBList, small_check_index, answer_image)
    # print('smallCheckAns: ', smallCheckAns)

    writen_index = [(18, 0.05), (20, 0.05)]
    writenAns, answer_image = findWritenBox(gray_image, boxCBList, writen_index, answer_image)
    # print('writenAns: ', writenAns)

    front_save_path = Path(dirPath) / 'answer_image' / 'front'
    front_save_path.mkdir(parents=True, exist_ok=True) 
    cv.imwrite(str(front_save_path / Path(path).name), answer_image)

    return {
        "big_check": bigCheckAns,
        "small_check": smallCheckAns,
        "writen": writenAns
    }
    

def getBackAns(path, dirPath):    
    raw_image = cv.imread(path)
    answer_image = raw_image.copy()

    crop_image = raw_image[:int(raw_image.shape[0] // 2.6), :]
    gray_image = cv.cvtColor(crop_image, cv.COLOR_BGR2GRAY)
    table_line = findTableLine(gray_image)
    boxCBList = getBoxCBList(gray_image, table_line)

    assert len(boxCBList) == 11, "Back image table column is not 11"

    big_check_index = [3, 5, 7, 8, 9]
    bigCheckAns, answer_image = findBigCheckAns(gray_image, boxCBList, big_check_index, answer_image)
    # print('bigCheckAns: ', bigCheckAns)

    writen_index = [(4, 0.05), (6, 0.05), (10, 0.04)]
    writenAns, answer_image = findWritenBox(gray_image, boxCBList, writen_index, answer_image)
    # print('writenAns: ', writenAns)
    
    # seggestion part (recrop the input image)
    crop_image = raw_image[int(raw_image.shape[0] // 2.6):, :]
    gray_image = cv.cvtColor(crop_image, cv.COLOR_BGR2GRAY)
    table_line = findTableLine(gray_image)
    boxCBList = getBoxCBList(gray_image, table_line, isSeggestion=True)

    # assert len(boxCBList) == 1, "Seggestion image table column is not 1"

    seggestion_index = [(0, 0.037)]
    start_coord = (0, int(raw_image.shape[0] // 2.6))
    seggestionAns, answer_image = findWritenBox(gray_image, boxCBList, seggestion_index, answer_image, start_coord)
    # print('writenAns: ', writenAns)

    back_save_path = Path(dirPath) / 'answer_image' / 'back'
    back_save_path.mkdir(parents=True, exist_ok=True) 
    cv.imwrite(str(back_save_path / Path(path).name), answer_image)

    return {
        "big_check": bigCheckAns,
        "writen": writenAns,
        "seggestion": seggestionAns
    }