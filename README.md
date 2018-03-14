# D3TA (Dear Diary, Don't Tell Anyone)

### An encrypted diary program

Store your diary entries encrypted with this program.<br>

Requirements:
+ Python 3.6 or newer
+ bcrypt
+ pycrypto
+ urwid 2.x
+ pyside2

The program stores the data in a SQLite3 database file. It may have any name and extension you provide, although I'd recommend using the .sqlite3 extension.
The GUI actually saves each new file with it.

Each entry is stored in a table with three values, one date, one hint and one text with types of datetime, tinytext and longtext, respectively.
The date is the date and time when the entry was created and the hint is an optional user input.
The program shows the name of an entry as the combination of the datetime and the hint.

The database itself is not password protected, but each text entry is encrypted with [PyCrypto](https://www.dlitz.net/software/pycrypto/) using the AES algorithm and hashed with SHA-256 for storage.

A salted hash generated from the password using [bcrypt](https://github.com/pyca/bcrypt/) is also stored in the database, in another table.

The program allows you to create new databases, change their passwords, create new entries, save and modify entries, delete entries and empty databases.
These functions are accessible both from the command line and from the GUI.

The GUI uses [PySide2](https://wiki.qt.io/PySide2), and the main window and license windows are created with [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html).

This project is licensed under the [Apache License version 2.0](https://www.apache.org/licenses/LICENSE-2.0).<br>
PySide2 is licensed under the [GNU Lesser General Public License version 3](https://opensource.org/licenses/lgpl-3.0.html).<br>
PyCrypto is licensed under [its own open source license](https://www.dlitz.net/software/pycrypto/submission-requirements/).<br>
bcrypt is licensed under the [Apache License version 2.0](https://www.apache.org/licenses/LICENSE-2.0).<br>

### Command line usage:
```
usage: cli.py [-h] [--change-password | --new-database] database

D3TA (Dear Diary, Don't Tell Anyone)

positional arguments:
  database           [path +] filename to your database

optional arguments:
  -h, --help         show this help message and exit
  --new-database
  --change-password
```

Note: urwid has mouse support, so mouse clickes are registered.

### CLI Screenshots
<img src="screenshots/c1.png" alt="CLI screenshot 1"> <img src="screenshots/c2.png" alt="CLI screenshot 2"><br>
<img src="screenshots/c3.png" alt="CLI screenshot 3">

### GUI Screenshots
<img src="screenshots/g1.png" alt="GUI screenshot 3"><br>
<img src="screenshots/g2.png" alt="GUI screenshot 2"><br>
<img src="screenshots/g3.png" alt="GUI screenshot 3">