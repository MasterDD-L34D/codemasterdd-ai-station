@echo off
REM Cross-repo Dashboard launcher (Component 1 v0.2)
REM Launches Flask in production mode (waitress) + opens browser

cd /d "%~dp0"
start "" "http://127.0.0.1:8081/"
python app.py --prod
