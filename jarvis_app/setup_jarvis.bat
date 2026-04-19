@echo off
REM Jarvis AI Assistant - Setup and Installation
REM This script sets up Jarvis, installs dependencies, and creates desktop shortcuts

setlocal enabledelayedexpansion
title Jarvis AI Assistant - Installation

echo.
echo ========================================
echo   Jarvis AI Assistant - Setup
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo Python found. Creating virtual environment...

REM Create virtual environment
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate and upgrade pip
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1

echo.
echo Installing required packages:
echo   - slint (Modern UI framework)
echo   - vosk (Voice recognition)
echo   - sounddevice (Audio input)
echo   - pyttsx3 (Text-to-speech)
echo   - requests (HTTP library)
echo   - pyyaml (Configuration)
echo.
echo This may take a few minutes...
echo.

REM Install dependencies
pip install -q ^
    slint ^
    vosk ^
    sounddevice ^
    pyttsx3 ^
    requests ^
    pyyaml

if errorlevel 1 (
    echo Warning: Some packages failed to install
    echo You may need to install them manually
    pause
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo You can now launch Jarvis by:
echo 1. Double-clicking: run_jarvis.vbs
echo 2. Or running: run_jarvis.bat
echo.
echo Creating desktop shortcut...

REM Create desktop shortcut using VBScript
set DESKTOP=%USERPROFILE%\Desktop
set VBSFILE=%TEMP%\create_shortcut.vbs

(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "%DESKTOP%\Jarvis.lnk"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "%SCRIPT_DIR%run_jarvis.vbs"
    echo oLink.WorkingDirectory = "%SCRIPT_DIR%"
    echo oLink.Description = "Jarvis AI Assistant"
    echo oLink.IconLocation = "%SCRIPT_DIR%run_jarvis.vbs"
    echo oLink.Save
) > "%VBSFILE%"

cscript "%VBSFILE%" >nul 2>&1
del "%VBSFILE%"

echo Desktop shortcut created: Jarvis.lnk
echo.
echo Ready to use! Press any key to launch Jarvis...
pause

call run_jarvis.bat

endlocal
