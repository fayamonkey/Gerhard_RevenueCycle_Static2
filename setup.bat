@echo off
setlocal enabledelayedexpansion

echo ===================================
echo Sales Process Simulation Setup (Pure Python Version)
echo ===================================

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Get the current directory
set "CURRENT_DIR=%CD%"

:: Create desktop shortcut
echo.
echo Creating desktop shortcut...
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\SalesProcessSimulator-Pure.lnk"
set "TARGET_PATH=%CURRENT_DIR%\run_sim.bat"

:: Create the run_sim.bat with correct Python path
echo @echo off > run_sim.bat
echo cd /d "%CURRENT_DIR%" >> run_sim.bat
echo set PYTHONPATH=%CURRENT_DIR% >> run_sim.bat
echo python main.py >> run_sim.bat
echo pause >> run_sim.bat

:: Create the shortcut using PowerShell
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%SHORTCUT_PATH%'); $SC.TargetPath = '%TARGET_PATH%'; $SC.WorkingDirectory = '%CURRENT_DIR%'; $SC.Save()"

echo.
echo ===================================
echo Setup completed successfully!
echo.
echo A desktop shortcut 'SalesProcessSimulator-Pure' has been created.
echo You can now use the sales process simulator by:
echo 1. Double-clicking the desktop shortcut
echo 2. Running run_sim.bat directly
echo.
echo Note: This is the pure Python version that doesn't require
echo any external dependencies or API keys.
echo ===================================
echo.
pause 