@echo off
:: Move the command prompt's focus to the folder where this script is located
cd /d "%~dp0"
:: Run the python script
python src/scheduler_service.py
pause