@echo off
REM Aider wrapper for cloud tier 3 -- Google Gemini 60 req per min free tier
REM Model: gemini-2.5-flash -- multimodal 1M ctx input thinking-capable
REM Nota: gemini-2.0-flash DEPRECATO quota 0 effettiva 2026-04-22 test
REM Se thinking budget consuma output: passare --extra-body per disable thinking LiteLLM feature specifica
REM diff format + no-auto-commits behavior-critical safety ADR-0008
REM --git-commit-verify: respect git hooks ADR-0011 Gap 3
REM Caveat: invia source code a Google data retention ToS -- usare solo su repo non-sensitive
REM cp1252 fix 2026-04-23: force console + Python UTF-8 to avoid Rich UnicodeEncodeError
REM Privacy guard rail H8 2026-05-09 ADR-0023 / harsh review V2: abort se repo non whitelisted
REM Note: REM lines with parens removed -- L-2026-05-015 PowerShell pollution mitigation Option B 2026-05-13
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8

REM Privacy guard rail check
set "REPO_ROOT="
for /f "delims=" %%i in ('git rev-parse --show-toplevel 2^>nul') do set "REPO_ROOT=%%i"
if "%REPO_ROOT%"=="" (
    echo ERROR: not in a git repo. aider-gemini aborted ^(privacy guard rail H8^).
    exit /b 1
)
set "REPO_ROOT_WIN=%REPO_ROOT:/=\%"
set "WHITELIST=%USERPROFILE%\.config\aider-privacy-whitelist.txt"
if not exist "%WHITELIST%" (
    echo ERROR: privacy whitelist not found at %WHITELIST%
    echo aider-gemini aborted ^(privacy guard rail H8^).
    exit /b 1
)
findstr /B /I /C:"%REPO_ROOT_WIN%" "%WHITELIST%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: repo NOT in cloud-OK whitelist:
    echo   repo: %REPO_ROOT_WIN%
    echo   whitelist: %WHITELIST%
    echo aider-gemini aborted ^(privacy guard rail H8 ADR-0023^).
    echo If repo should be cloud-OK, add path to whitelist and retry.
    exit /b 1
)

aider --model gemini/gemini-2.5-flash --edit-format diff --no-auto-commits --git-commit-verify --commit-prompt "Commit message MUST be in English, Conventional Commits format (type: short description), subject line <=72 chars total, lowercase description, no trailing period. Example: 'fix: handle null input in parser'." %*
