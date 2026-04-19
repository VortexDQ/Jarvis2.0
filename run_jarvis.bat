@echo off
REM Jarvis AI Assistant - Main Launcher
REM This script launches Jarvis with proper Python environment setup

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if .venv exists, if not create it
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if dependencies are installed
pip show slint >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -q slint vosk sounddevice pyttsx3 requests
    if errorlevel 1 (
        echo Warning: Some packages may not have installed successfully
    )
)

REM Run the Jarvis application
echo Starting Jarvis AI Assistant...
python -m jarvis_app

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Jarvis encountered an error. Press any key to continue...
    pause
)

endlocal
