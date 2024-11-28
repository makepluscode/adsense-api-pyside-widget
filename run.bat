
REM run.bat
@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running AdSense earnings script...
python main.py
pause