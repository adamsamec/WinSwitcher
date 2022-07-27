set scripts=%cd%

@REM Generate English MO file
cd %scripts%\..\src\locales\en\LC_MESSAGES
python %scripts%\msgfmt.py -o base.mo base

@REM Generate Czech MO file
cd %scripts%\..\src\locales\cs\LC_MESSAGES
python %scripts%\msgfmt.py -o base.mo base

title MO language files generation completed
pause