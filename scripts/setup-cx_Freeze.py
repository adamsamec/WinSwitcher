import cx_Freeze
import os
import sys


sys.path.append(os.path.realpath(sys.path[0] + "\\..\\src"))

options = {"build_exe": "..\\build\\WinSwitcher"}
executables = [
    cx_Freeze.Executable(
        "..\\src\\WinSwitcher.py", base="Win32GUI", targetName="WinSwitcher.exe"
    )
]

cx_Freeze.setup(
    name="WinSwitcher",
    version="0.2.0",
    description="Utility which brings easier application and windows switching to Microsoft Windows.",
    author="Adam Samec",
    author_email="adam.samec@gmail.com",
    options={"build_exe": options},
    executables=executables,
)
