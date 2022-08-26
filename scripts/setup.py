import os
import sys

# Add the path to the "src" directory to the PATH environment variable
sys.path.append(os.path.realpath(sys.path[0] + "\\..\\src"))

main_path = "..\\src\\WinSwitcher.py"
target = "WinSwitcher.exe"

name = "WinSwitcher"
version = "0.5.0"
description = "Utility which brings easier application and windows switching and closing to Microsoft Windows."
author = "Adam Samec"
author_email = "adam.samec@gmail.com"
