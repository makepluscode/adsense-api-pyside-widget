REM install.bat
@echo off
echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing required packages...
pip install google-api-python-client
pip install google-auth-httplib2
pip install google-auth-oauthlib

echo Creating config directory...
mkdir config

echo Installation completed!
echo Please place your service account key file in the config directory.
echo Remember to update the account ID in the script.
pause