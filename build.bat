@echo off
echo Building executable...

call venv\Scripts\activate.bat

pyinstaller --noconsole ^
            --add-data "config/.env;config" ^
            --add-data "config/credentials.json;config" ^
            --add-data "config/token.pickle;config" ^
            --hidden-import=google.auth.transport.requests ^
            --hidden-import=google_auth_oauthlib.flow ^
            --hidden-import=google.oauth2.credentials ^
            --hidden-import=dotenv ^
            --collect-submodules=google ^
            main.py

echo Build completed! Executable is in dist/main folder
pause