@echo off
REM Jarvis AI Assistant - Uninstall Script
REM Safely removes Jarvis while preserving user data

setlocal enabledelayedexpansion
title Jarvis AI - Uninstall

echo.
echo ========================================
echo   Jarvis AI Assistant - Uninstall
echo ========================================
echo.
echo This will remove Jarvis while preserving:
echo - User settings (settings.yaml)
echo - Configuration (jarvis_config.json)
echo - Backups (backups/ folder)
echo - Error logs (logs/ folder)
echo.

set /p CONFIRM="Are you sure? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Uninstall cancelled.
    exit /b 0
)

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo Removing virtual environment...
if exist ".venv" (
    rmdir /s /q ".venv" 2>nul
    echo ✓ Virtual environment removed
)

echo Cleaning cache files...
if exist "__pycache__" (
    rmdir /s /q "__pycache__" 2>nul
    echo ✓ Cache removed
)

echo.
echo ========================================
echo   Uninstall Complete
echo ========================================
echo.
echo Preserved files:
echo - settings.yaml
echo - jarvis_config.json
echo - backups/ folder
echo - logs/ folder
echo.
echo To reinstall, run: setup_jarvis.bat
echo To remove everything, delete this folder.
echo.
pause

endlocal
