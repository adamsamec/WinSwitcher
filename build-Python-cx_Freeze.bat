cd src
python setup-cx_Freeze.py build

@REM xcopy md ..\build\AccessibleWindowSwitcher-cx_Freeze\md\

cd ..
title build completed
pause
