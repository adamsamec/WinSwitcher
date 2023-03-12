# WinSwitcher
## Introduction
WinSwitcher is a utility which runs in background and brings easier application and windows management to Microsoft Windows. WinSwitcher enables efficient applications and windows switching and closing functionality that is optimized for the keyboard and screen reader users, inspired by macOS and the VoiceOver screen reader way of switching between applications and windows. You will find the benefit of WinSwitcher especially if you are running many applications and their open windows at the same time.

## Features
After starting, WinSwitcher notifies the user it has been started and then runs in background until its functionality is invoked using the corresponding keyboard shortcuts, which are global, that is, the shortcuts work no matter which application or window is currently in the foreground. The user can invoke the following lists:

* List of running applications and their open windows.
* List of open windows only for the application in the foreground.

### List of running applications and their open windows
After pressing Windows + F12, or Windows + Shift + A, the user can invoke a list of currently running applications, ordered by the most recently used application first. The list can be operated using the following keys:

* Down or Up arrow: Navigates to the next or previous item in the list.
* Right arrow: When an application is selected, navigates to the list of open windows only for that selected application.
* Left arrow: When a window is selected, navigates back to the list of running applications.
* Enter: When an application is selected, switches to that application's most recently used window. If a window is selected, switches to that window. Then hides WinSwitcher.
* Delete: When an application is selected, force quits that application. If a window is selected, closes that window. Note that quitting an application may cause unsaved work to be lost, whereas window closing may fail and require you to save work before closing.
* Escape: Hides WinSwitcher.
* Alt + F4: Exits WinSwitcher, so it no longer runs in background. WinSwitcher notifies the user it is exiting.

### List of open windows only for the application in the foreground
After pressing Windows + F11, or Windows + Shift + W, the user can invoke a list of open windows  only for the application in the foreground, ordered by the most recently used window first. The list can be operated using the following keys:

* Down or Up arrow: Navigates to the next or previous item in the list.
* Enter: When a window is selected, switches to that window. Then hides WinSwitcher.
* Delete: When a window is selected, closes that window. Note that window closing may fail and require you to save work before closing.
* Escape: Hides WinSwitcher.
* Alt + F4: Exits WinSwitcher, so it no longer runs in background. WinSwitcher notifies the user it is exiting.

### WinSwitcher settings
The WinSwitcher settings can be accessed by the "Settings" button which can be navigated to using Tab or Shift + Tab on the main WinSwitcher window.

### Applications or windows list filtering and first-letter navigation
To make the finding of the desired application or window faster, the list of applications or windows supports filter by typing feature, which means that whenever the list is focused, typing characters immediately filters the list, displaying only the applications or windows whose titles contain the typed characters. The filter can be reset and the original unfiltered list of applications or windows displayed back again by pressing Backspace.

However, if you rather prefer a standard behavior of a list, that is, that typing characters navigates to the list item whose first characters matche the characters typed, you can switch to this behavior in settings by unchecking the "Filter running apps and windows list by typing" checkbox. This option can also be toggled on or off anytime easily by the Control + T keyboard shortcut, when pressed in the main WinSwitcher window.

If you choose to disable the filter list by typing feature described above, then you can still access the filter functionality by pressing Control + F when WinSwitcher is invoked. The focus will be moved to the filter text field located above the applications or windows list. Typing a text to that field immediately filters the applications or windows listed below the field. Pressing Enter when on the filter text field moves focus back to the applications or windows list. The navigation between the list of applications or windows and the filter text field is also possible using the Tab key or Shift + Tab.

The filtering is not case sensitive and also matches the list items disregarding the diacritics, curls, strokes and other modified latin letters.

### Changing the global keyboard shortcuts
The WinSwitcher settings dialog allows you to configure the global keyboard shortcuts for invoking WinSwitcher. More than one shortcut can be enabled at the same time, so that the chance of conflicting with another program is minimized.

For invoking the list of running applications, you can choose from the following shortcuts:

* Windows + F12 (checked by default).
* Windows + Shift + A (checked by default).
* Control + Shift + 1.

For invoking the list of open windows for the application in the foreground, you can choose from the following shortcuts:

* Windows + F11 (checked by default).
* Windows + Shift + W (checked by default).
* Control + Shift + 2.

### Known limitations
* WinSwitcher is unable to list and switch to modern Windows applications, such as Mail, Calendar or Calculator.
* Occasionally, after an attempt to switch to a window, the focus is not properly placed to that window. What may help in this condition is pressing Alt + Tab and then Alt + Shift + Tab.

## Download
### Installer
Below, you can download the installer for WinSwitcher, which also creates a startup shortcut, so you don't have to run WinSwitcher manually every time your system restarts. The installer also creates a Desktop shortcut.

Note that Windows Defender security software may prevent this installer from starting. In that case, visit the "More info"link which should be available on the page displayed to you, and then press the "Run anyway" button.

[Download WinSwitcher installer for Windows][installer-download].

### Portable version
WinSwitcher is also available as a portable executable not requiring installation. Download the ZIP archive from the link below, extract it to a location of your choice and run it by executing the WinSwitcher.exe file. Note that the installer available for download above, as opposed to this portable version, also creates startup shortcut for you, so you don't have to start WinSwitcher manually every time your system restarts.

[Download WinSwitcher portable for Windows][portable-download].

### Source files
WinSwitcher is a free and open-source software developed in Python. You can find all the necessary source files in the "src" folder of this repo, and run the program from that folder by executing the following if all the Python dependancies are met:

```
python WinSwitcher.py
```

## Troubleshooting
If you encounter an error message right after starting WinSwitcher, try deleting the contents of C:\Users\<username>\AppData\Local\Temp\gen_py. If that folder doesn't exist, try looking if C:\Temp\gen_py exists, and if so, delete its content.

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

[installer-download]: https://files.adamsamec.cz/apps/WinSwitcher-win32.msi
[portable-download]: https://files.adamsamec.cz/apps/WinSwitcher-win32.zip
