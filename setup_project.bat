@echo off
cd /d "%~dp0"
:: Only run once, in case the project dependencies are missing
echo Installing necessary Python libraries...
pip install -r requirements.txt
echo Setup complete!
pause