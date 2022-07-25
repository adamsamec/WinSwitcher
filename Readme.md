# WinSwitcher
## Introduction
WinSwicher is a utility which runs in background and brings easier application and windows switching to Microsoft Windows, inspired by macOS way of switching between applications and windows.

## Features
* Show a list of running applications which can be switched to.

## Keyboard shortcuts
* Windows + F12: Shows the list of running applications. Pressing Enter will switch to the currently selected application. Pressing Escape will hide the application list window.
* Windows + F4: Quits WinSwitcher.

## Download
### Executable
Not yet available.

### Source files
WinSwitcher is developed in Python. You can find all the necessary source files in the "src" folder of this repo, and run the program from that folder by executing the following:

    python WinSwitcher.py

## Python dependancies
The Python source files of WinSwitcher require the cefpython3, markdown2, playsound, psutil, pynput, pywinauto and wxPython packages, which can be installed using [PIP][PIP] like this:

    pip install cefpython3
    pip install markdown2
    pip install playsound
    pip install psutil
    pip install pynput
    pip install pywinauto
    pip install wxPython

## License
WinSwitcher is available under the MIT licence

### The MIT License (MIT)

Copyright (c) 2022 Adam Samec

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[PIP]: https://pypi.org/project/pip/
