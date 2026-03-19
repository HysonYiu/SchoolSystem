@echo off
REM SchoolSystem - Windows Launcher
REM This script starts SchoolSystem in the background

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)

REM Create a log file
set LOG_FILE=%~dp0\schoolsystem.log
echo [%date% %time%] Starting SchoolSystem... >> %LOG_FILE%

REM Start the server in background (using VBS helper)
cscript //nologo "%~dp0\start.vbs" >> %LOG_FILE% 2>&1

echo.
echo ========================================
echo SchoolSystem Started!
echo.
echo Access it at:
echo   http://127.0.0.1:8081
echo   http://192.168.68.53:8081
echo.
echo Logs: %LOG_FILE%
echo.
echo To stop: taskkill /F /IM python.exe
echo ========================================
pause
