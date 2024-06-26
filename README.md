# Focus Timer

A minimalistic terminal based countdown timer which uses intervals [focus | break] to help work efficiently. The program was developed and tested on Windows.

## How does the program even look?

![Screenshot 2024-06-15 112150](https://github.com/Testspieler09/focus_timer/assets/142326461/f5898b1d-7fc6-471f-94d9-17a1aa0d70c3)

The headline switches between `Focus Time` and `Break Time`. Furthermore the intervals get displayed as `n/N`.

The foreground and background colors are determined by the color set for **black** [background] and **white** [foreground] in the terminal/shell.

## Aim of the Program

The program is supposed to be minimalistic and fast. Therefore it may be rewritten in C in the future. Moreover it is meant for the terminal and does not need a GUI.

## Current features

- basic features (pause, reset, continue timer)
- update the screen if window was resized (should work automatically but just in case one can do it manually)
    - STILL TRY TO NOT RESIZE THE WINDOW WHILE IT'S EXECUTING, AS IT WON'T ALWAYS WORK AND MAY CAUSE PROBLEMS
- support for own alert sounds

### Add your own sound

To add your own sound change line 173. Should work with any audio file, but if not convert it to a different typ. The default file is `sound.mp3`. Only tested on Windows, so if the filepath gets generated wrong open an issue or send a pull request.
```python
file = "sound.mp3"
# other code e.g. generation of filepath
playsound(filepath, False)
```
Otherwise you could also just add your file to the directory and name it `sound.mp3`, but remember to delete or rename the default one. To give credit the sound is published by [Alex Jauk](https://pixabay.com/de/users/alex_jauk-16800354/).

## Planed features

- support for different ASCII (Art) numbers or even letters (for bigger numbers and text)
- change the timedisplay to e.g. an animated plant (ASCII animation based on time passed)

## How to get started

1. Make shure you have installed python and pip (should be installed with python by default).
1. Clone the repo and run the following command in the projects directory.

```pwsh
pip install -r requirements.txt
```

3. Have fun with the program

## You want to contribute?

- Open an issue for bugs or wanted features.
- Fork the repo and send a pull request with the new changes.

### What could you contribute?

Generally speaking anything that makes the program more efficient (less memory usage, less operations on cpu, ...) or fixes bugs.
Otherwise take a look at open issues to answer this question.
