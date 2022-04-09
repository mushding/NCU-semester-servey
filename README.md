###### tags: `github README.md`

NCU semester sruvey
====

NCU semester sruvey automatic analysis system, input a survey sheet, return the sum of answer check on the question box.

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

## TODO

- [ ] fix skip small check issue
- [ ] fix get empty seggestion box issue

