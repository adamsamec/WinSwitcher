python setup-cx_Freeze.py build

xcopy /s ..\src\locales ..\build\WinSwitcher\locales\
xcopy ..\src\config.default.json ..\build\WinSwitcher

title Build completed
pause
