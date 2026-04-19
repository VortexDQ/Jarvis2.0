@echo off
REM Jarvis AI Assistant - Dependency Checker
REM Verifies all required packages are installed

setlocal enabledelayedexpansion
title Jarvis - Dependency Check

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

call .venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo Error: Virtual environment not activated
    echo Please run setup_jarvis.bat first
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
echo.

setlocal enabledelayedexpansion
set missing=

REM Check each dependency
python -c "import slint" 2>nul || set "missing=!missing! slint"
python -c "import vosk" 2>nul || set "missing=!missing! vosk"
python -c "import sounddevice" 2>nul || set "missing=!missing! sounddevice"
python -c "import pyttsx3" 2>nul || set "missing=!missing! pyttsx3"
python -c "import requests" 2>nul || set "missing=!missing! requests"
python -c "import yaml" 2>nul || set "missing=!missing! pyyaml"

if defined missing (
    echo Missing packages:!missing!
    echo.
    echo Installing missing packages...
    pip install slint vosk sounddevice pyttsx3 requests pyyaml
    if errorlevel 1 (
        echo Error: Failed to install packages
        pause
        exit /b 1
    )
)

echo.
echo ✓ All dependencies installed!
echo.
echo You can now run: run_jarvis.vbs
echo.
pause

endlocal
