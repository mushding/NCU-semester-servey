from pathlib import Path
import cv2 as cv

def analyseFrontCheck(sumList, ansList, imageIdx, dirPath):
    bigCheckList = ansList["big_check"]
    smallCheckList = ansList["small_check"]
    writeAnsList = ansList["writen"]

    big_check_index = ['1-1', '1-2', '1-4', '2-1', '2-2', '2-3']
    small_check_index = ['1-2-1', '1-3', '1-5', '1-6']
    writen_index = ['2-2-1', '2-3-1']

    for question, checkIdx in zip(bigCheckList, big_check_index):
        # use -1 to check is there has any answer
        for check in question:
            if check != -1:
                sumList[checkIdx][check + 1] += 1

    for question, checkIdx in zip(smallCheckList, small_check_index):
        for check in question:
            if check != -1:
                sumList[checkIdx][check + 1] += 1

    for question, checkIdx in zip(writeAnsList, writen_index):
        if question.size != 0:
            savePath = Path('.') / dirPath / 'writen_image' / checkIdx
            Path(savePath).mkdir(parents=True, exist_ok=True) 
            cv.imwrite(str(Path(savePath) / f'{imageIdx}.jpg'), question)

    return sumList


def analyseBackCheck(sumList, ansList, imageIdx, dirPath):
    bigCheckList = ansList["big_check"]
    writeAnsList = ansList["writen"]
    seggestionList = ansList["seggestion"]

    big_check_index = ['2-4', '2-5', '2-6', '2-7', '2-8']
    writen_index = ['2-4-1', '2-5-1', '2-8-1']
    seggestion_index = ['3-1']

    for question, checkIdx in zip(bigCheckList, big_check_index):
        for check in question:
            if check != -1:
                sumList[checkIdx][check + 1] += 1

    for question, checkIdx in zip(writeAnsList, writen_index):
        # use check size to tell whether is 'np.array([])' or is a image
        if question.size != 0:
            savePath = Path('.') / dirPath / 'writen_image' / checkIdx
            Path(savePath).mkdir(parents=True, exist_ok=True) 
            cv.imwrite(str(Path(savePath) / f'{imageIdx}.jpg'), question)

    for question, checkIdx in zip(seggestionList, seggestion_index):
        if question.size != 0:
            savePath = Path('.') / dirPath / 'writen_image' / checkIdx
            Path(savePath).mkdir(parents=True, exist_ok=True) 
            cv.imwrite(str(Path(savePath) / f'{imageIdx}.jpg'), question)

    return sumList