# WinSwitcher
## Introduction
WinSwicher is a utility which runs in background and brings easier application and windows switching to Microsoft Windows. WinSwitcher enables efficient applications and windows switching functionality that is optimized for the keyboard and screen reader users, inspired by macOS and the VoiceOver screen reader way of switching between applications and windows. You will find the benefit of WinSwitcher especially if you are running many applications and their open windows at the same time.

## Features
After starting, WinSwitcher notifies the user it has been started and then runs in background until its applications or windows switching functionality is invoked using the corresponding keyboard shortcuts, which are global, that is, the shortcuts work no matter which application or window is currently in the foreground. The user can invoke the following lists:

* List of running applications and their open windows.
* List of open windows only for the application in the foreground.

### List of running applications and their open windows
By pressing Windows + F12, the user can invoke a list of currently running applications, ordered by the most recently used application first. The list can be operated using the following keys:

* Down or Up arrow: Navigates to the next or previous item in the list.
* Right arrow: When an application is selected, navigates to the list of open windows only for that selected application.
* Left arrow: When a window is selected, navigates back to the list of running applications.
* Enter: When an application is selected, switches to that application's most recently used window. If a window is selected, switches to that window. Then hides WinSwitcher.
* Escape: Hides WinSwitcher.
* Alt + F4: Exits WinSwitcher, so it no longer runs in background. WinSwitcher notifies the user it is exiting.

### List of open windows only for the application in the foreground
By pressing Windows + F11, the user can invoke a list of open windows  only for the application in the foreground, ordered by the most recently used window first. The list can be operated using the following keys:

* Down or Up arrow: Navigates to the next or previous item in the list.
* Enter: When a window is selected, switches to that window. Then hides WinSwitcher.
* Escape: Hides WinSwitcher.
* Alt + F4: Exits WinSwitcher, so it no longer runs in background. WinSwitcher notifies the user it is exiting.

### Navigation by typing in applications or windows lists
To make the navigation in the applications or windows list faster, WinSwitcher supports the navigation by typing feature, that is, typing the first letters of an application name or a window title moves focus to the first matched item.

### Applications or windows list filtering
By pressing Control + F when WinSwitcher is invoked, the focus is moved to the filter text field. Typing a text to that field immediately filters the applications or windows listed below. Pressing Enter when on the filter text field moves focus back to the applications or windows list. The navigation between the list of applications or windows and the filter text field is also possible using the Tab key or Shift + Tab.

The filtering is not case sensitive and also matches the list items disregarding the diacritics, curls, strokes and other modified latin letters. 

### Keyboard shortcuts summary
* Windows + F12: Global shortcut which shows the list of running applications.
* Windows + F11: Global shortcut which shows the list of open windows only for the application in the foreground.
* Control + F: When WinSwitcher is invoked, moves focus to the filter text field.

### Known limitations
* WinSwitcher is unable to list and switch to modern Windows applications, such as Mail or Calculator.
* Sometimes after an attempt to switch to a window, the focus is not properly placed to that window. What may help in this condition is pressing Alt + Tab and then Alt + Shift + Tab.

## Download
### Installer
Below, you can download the installer for WinSwitcher, which also creates a startup shortcut, so you don't have to run WinSwitcher manually every time your system restarts. The installer also creates a Desktop shortcut.

Note that Windows Defender security software may prevent this installer from starting. In that case, visit the "More info"link which should be available on the page displayed to you, and then press the "Run anyway" button.

[Download WinSwitcher installer for Windows (32-bit)][installer-download].

### Portable version
WinSwitcher is also available as a portable executable not requiring installation. Download the ZIP archive from the link below,extract it to a location of your choice and run it by executing the WinSwitcher.exe file. Note that the installer available for download above, as opposed to this portable version, also creates startup shortcut for you, so you don't have to start WinSwitcher manually every time your system restarts.

[Download WinSwitcher portable for Windows (32-bit)][portable-download].

### Source files
WinSwitcher is a free and open-source software developed in Python. You can find all the necessary source files in the "src" folder of this repo, and run the program from that folder by executing the following if all the Python dependancies are met:

```
python WinSwitcher.py
```

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

[installer-download]: http://files.adamsamec.cz/apps/WinSwitcher-win32.msi
[portable-download]: http://files.adamsamec.cz/apps/WinSwitcher-win32.zip
