import os
import sys

# Add the path to the "src" directory to the PATH environment variable
sys.path.append(os.path.realpath(sys.path[0] + "\\..\\src"))

main_path = "..\\src\\WinSwitcher.py"
base = "Win32GUI"
target = "WinSwitcher.exe"

name = "WinSwitcher"
version = "0.8.2"
description = "WinSwitcher"
author = "Adam Samec"
author_email = "adam.samec@gmail.com"
