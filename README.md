# Focus Timer

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A minimalistic terminal based countdown timer which uses intervals [focus | break] to help work efficiently. The program was developed and tested on Windows.

## How does the program even look?

![Program](assets/program.png)

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

To add your own sound change line 169. It now only works with `.wav` files, but if your file isn't of that type just convert it online or with e.g. pydub. The default file is `sound.wav`.
```python
file = "sound.wav" # needs to be a .wav file
```
Otherwise you could also just add your file to the directory and name it `sound.wav`, but remember to delete or rename the default one. To give credit the sound is published by [Alex Jauk](https://pixabay.com/de/users/alex_jauk-16800354/).

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

### Wheel problem on MAC

Make shure you follow [these steps](https://stackoverflow.com/questions/73268630/error-could-not-build-wheels-for-pyaudio-which-is-required-to-install-pyprojec) if you have a problem installing pyaudio related to wheels.

> These steps worked on M1 Pro chips
>
> 1. Install portaudio
> `brew install portaudio`
>
> 2. Link portaudio
> `brew link portaudio`
>
> 3. Copy the path where portaudio was installed (use it in the next step)
> `brew --prefix portaudio`
>
> 4. Create .pydistutils.cfg in your home directory
> `sudo nano $HOME/.pydistutils.cfg`
> then paste the following
>
> ```txt
> [build_ext]
> include_dirs=<PATH FROM STEP 3>/include/
> library_dirs=<PATH FROM STEP 3>/lib/
> ```
>
> 5. Install pyaudio
> `pip install pyaudio` or `pip3 install pyaudio`

## You want to contribute?

- Open an issue for bugs or wanted features.
- Fork the repo and send a pull request with the new changes.

### What could you contribute?

Generally speaking anything that makes the program more efficient (less memory usage, less operations on cpu, ...) or fixes bugs.
Otherwise take a look at open issues to answer this question.
