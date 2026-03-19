@echo off
REM Stop SchoolSystem

taskkill /F /IM python.exe
if errorlevel 0 (
    echo SchoolSystem stopped successfully
) else (
    echo No SchoolSystem process found
)
pause
