@echo off
title Hollowgate
cd /d "%~dp0"

python --version >nul 2>&1
if not errorlevel 1 (
    goto :found_python
)

py --version >nul 2>&1
if not errorlevel 1 (
    set PYLAUNCHER=py
    goto :run_game
)

echo.
echo  Python was not found on this computer.
echo  Please install Python 3.8 or newer from:
echo     https://www.python.org/downloads/
echo.
echo  During installation, make sure to check the box that says
echo  "Add python.exe to PATH".
echo.
pause
exit /b

:found_python
set PYLAUNCHER=python

:run_game
%PYLAUNCHER% -c "import colorama" >nul 2>&1
if errorlevel 1 (
    echo First-time setup - installing a small display library...
    %PYLAUNCHER% -m pip install colorama --quiet --disable-pip-version-check >nul 2>&1
)

mode con: cols=112 lines=48 >nul 2>&1

%PYLAUNCHER% main.py

echo.
pause
