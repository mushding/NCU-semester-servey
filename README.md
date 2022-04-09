[![hackmd-github-sync-badge](https://hackmd.io/DFESNuxzT4O4zQCjZ_CwDw/badge)](https://hackmd.io/DFESNuxzT4O4zQCjZ_CwDw)
###### tags: `github README.md`

NCU semester sruvey
====

NCU semester sruvey automatic analysis system, input a survey sheet, return the sum of answer check on the question box.

## Requirement
opencv-python

numpy

## Usage

To start the system, enter following commands:

```
python3 sruvey.py --class_name "THE CLASS NAME YOU WANT TO ANALYSIS"
```

```
optional arguments:
  -h, --help            show this help message and exit
  --class_name CLASS_NAME
                        Please enter the folder of class name. ex:
                        --class_name 深度學習電腦視覺
```

Once you run the command, a Assertion error raised:

```
Traceback (most recent call last):
  File "/Users/lucas/Desktop/程式/leetcode/opencv/survey.py", line 24, in <module>
    assert any((input_image_dir / 'front').iterdir()) != 0, 'The folder has already created, you can put "FRONT/BACK" image into corresponding folder'
AssertionError: The folder has already created, you can put "FRONT/BACK" image into corresponding folder
```

* The system would automatically create a folder inside `class_dir` which name as your `--class_name CLASS_NAME`. 
* Then find the front/back folder inside the `--class_name CLASS_NAME`. 
* Last add scan of front images & back images into corresponding folder

After doing that, run the command again

```
python3 sruvey.py --class_name "THE CLASS NAME YOU WANT TO ANALYSIS"
```

And there you have it !

## Result

The system would generate two folders under `--class_name CLASS_NAME` folder. `./answer_image` and `./writen_image`

* `./answer_image` The bounding box of detection image result would save in this folder
* `./writen_image` If there have any writen answer in writen question blank, save in this folder

## TODO

- [ ] fix skip small check issue
- [ ] fix get empty seggestion box issue

