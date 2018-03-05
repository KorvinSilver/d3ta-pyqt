# D3TA (Dear Diary, Don't Tell Anyone)

### An encrypted diary program

<strong>This program is Work In Progress.</strong>

Store your diary entries encrypted with this program.<br>
Currently it works only in the command line. The GUI written in PySide2 coming sometime in the near future.

Requirements:
+ Python 3.6 or newer
+ bcrypt 3.x (tested on 3.1.4)
+ pycrypto 2.x (tested on 2.6.1)
+ urwid 2.x (tested on 2.0.1)

Additional GUI requirements:
+ pyside2

### Usage:
```
usage: cli.py [-h] [--change-password | --new-diary] diary

D3TA (Dear Diary, Don't Tell Anyone)

positional arguments:
  diary              [path +] filename to your diary

optional arguments:
  -h, --help         show this help message and exit
  --new-diary
  --change-password
```
