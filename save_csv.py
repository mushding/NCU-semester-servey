import csv
from pathlib import Path

def save_csv(savePath, ansList):
    with open(str(Path(savePath) / 'final_result.csv'), 'w', newline='') as csvfile:
        fieldnames = ['問題題號', '選項一', '選項二', '選項三', '選項四', '選項五']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for questionKey, answersDict in ansList.items():
            print(answersDict[1])
            writer.writerow([questionKey, answersDict[1], answersDict[2], answersDict[3], answersDict[4], answersDict[5]])
