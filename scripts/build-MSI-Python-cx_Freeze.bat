python setup-msi-cx_Freeze.py bdist_msi

xcopy /s ..\src\locales ..\build\WinSwitcher\locales\
@REM xcopy ..\src\md ..\build\WinSwitcher\md\

title MSI build completed
pause
