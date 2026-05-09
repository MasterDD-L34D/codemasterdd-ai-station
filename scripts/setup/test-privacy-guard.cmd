@echo off
REM Test logica privacy guard rail H8 (no aider invocation, solo verifica)
REM Returns: 0 = repo whitelisted (cloud OK), 1 = repo not whitelisted (abort)

setlocal

set "REPO_ROOT="
for /f "delims=" %%i in ('git rev-parse --show-toplevel 2^>nul') do set "REPO_ROOT=%%i"
if "%REPO_ROOT%"=="" (
    echo NOT in git repo
    exit /b 1
)
set "REPO_ROOT_WIN=%REPO_ROOT:/=\%"
set "WHITELIST=%USERPROFILE%\.config\aider-privacy-whitelist.txt"
if not exist "%WHITELIST%" (
    echo whitelist NOT FOUND: %WHITELIST%
    exit /b 1
)
findstr /B /I /C:"%REPO_ROOT_WIN%" "%WHITELIST%" >nul 2>&1
if errorlevel 1 (
    echo BLOCKED: %REPO_ROOT_WIN% NOT in whitelist
    exit /b 1
) else (
    echo ALLOWED: %REPO_ROOT_WIN% in whitelist
    exit /b 0
)
