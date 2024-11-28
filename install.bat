@echo off
echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing required packages...
pip install google-api-python-client
pip install google-auth-httplib2
pip install google-auth-oauthlib
pip install PySide6
pip install dataclasses
pip install typing
pip install python-dotenv

echo Creating config directory...
mkdir config 2>nul

echo Installation completed!
echo Please place your credentials.json file in the config directory.
echo.
echo Required files:
echo  - config/credentials.json
echo.
pause