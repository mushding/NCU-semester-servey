import glob
import os
from pathlib import Path
from tqdm import tqdm
from argparse import ArgumentParser

from survey_info import getFrontAns, getBackAns
from analyse_result import analyseFrontCheck, analyseBackCheck
from save_csv import save_csv

if __name__ == '__main__':

    # set args
    parser = ArgumentParser()
    parser.add_argument('--class_name', dest='class_name', required=True, help='Please enter the folder of class name. ex: --class_name 深度學習電腦視覺')
    args = parser.parse_args()
    
    class_dir = Path('class_dir') / args.class_name

    input_image_dir = Path(class_dir) / 'input_image'
    (input_image_dir / 'front').mkdir(parents=True, exist_ok=True) 
    (input_image_dir / 'back').mkdir(parents=True, exist_ok=True) 

    assert any((input_image_dir / 'front').iterdir()) != 0, 'The folder has already created, you can put "FRONT/BACK" image into corresponding folder'
    assert any((input_image_dir / 'back').iterdir()) != 0, 'The folder has already created, you can put "BACK" image into corresponding folder'

    frontAnsList = list()
    frontPaths = sorted((input_image_dir / 'front').glob('*'), key=os.path.getmtime)
    print("Total file in Dict: ", len(frontPaths))
    for path in tqdm(frontPaths, desc='Processing front image...'):
        frontAnsList.append(getFrontAns(str(path), class_dir))
        # print(f'at file: {path} - {frontPaths.index(path)}')

    backAnsList = list()
    backPaths = sorted((input_image_dir / 'back').glob('*'), key=os.path.getmtime)
    print("Total file in Dict: ", len(backPaths))
    for path in tqdm(backPaths, desc='Processing back image...'):
        backAnsList.append(getBackAns(str(path), class_dir))
        # print(f'at file: {path} - {backPaths.index(path)}')

    # init total ans sum dict, (total 21 questions)
    ansIdx = ['1-1', '1-2', '1-2-1', '1-3', '1-4', '1-5', '1-6', '2-1', '2-2', '2-2-1', '2-3', '2-3-1', '2-4', '2-4-1', '2-5', '2-5-1', '2-6', '2-7', '2-8', '2-8-1', '3-1']
    ansSumList = {idx: {index: 0 for index in range(1, 6)} for idx in ansIdx}
    
    assert len(frontAnsList) == len(backAnsList), "The front images & back images aren't the same amount"
    
    for idx, (frontAns, backAns) in tqdm(enumerate(zip(frontAnsList, backAnsList)), desc='Calculating final result...'):
        ansSumList = analyseFrontCheck(ansSumList, frontAns, idx, class_dir)
        ansSumList = analyseBackCheck(ansSumList, backAns, idx, class_dir)

    save_csv(class_dir, ansSumList)
