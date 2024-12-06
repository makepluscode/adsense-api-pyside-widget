@echo off
echo Building executable...

call venv\Scripts\activate.bat

pyinstaller --onefile ^
            --log-level=DEBUG ^
            --add-data "config;config" ^
            --hidden-import=PySide6.QtCore ^
            --hidden-import=PySide6.QtWidgets ^
            --hidden-import=PySide6.QtGui ^
            --hidden-import=google.auth.transport.requests ^
            --hidden-import=google_auth_oauthlib.flow ^
            --hidden-import=google.oauth2.credentials ^
            --hidden-import=google.auth ^
            --hidden-import=google_auth_httplib2 ^
            --hidden-import=dotenv ^
            --collect-submodules=google ^
            --collect-data google.oauth2 ^
            --collect-data google_auth_oauthlib ^
            --collect-data PySide6 ^
            main.py

echo Build completed! Executable is in dist folder
pause