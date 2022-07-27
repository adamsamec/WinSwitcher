python setup-cx_Freeze.py build

xcopy /s ..\src\locales ..\build\WinSwitcher\locales\
@REM xcopy ..\src\md ..\build\WinSwitcher\md\

title Build completed
pause
