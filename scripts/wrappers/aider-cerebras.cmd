@echo off
REM Aider wrapper for cloud tier 3 -- Cerebras WSE free tier limited a llama3.1-8b
REM Model: llama3.1-8b -- 8B general ~733 tok per s empirico 2026-04-22
REM Nota: gpt-oss-120b e qwen-3-235b nel catalog NON accessibili free paid tier
REM diff format + no-auto-commits behavior-critical safety ADR-0008
REM --git-commit-verify: respect git hooks ADR-0011 Gap 3
REM Caveat: invia source code a Cerebras data retention ToS -- usare solo su repo non-sensitive
REM cp1252 fix 2026-04-23: force console + Python UTF-8 to avoid Rich UnicodeEncodeError
REM Privacy guard rail H8 2026-05-09 ADR-0023 / harsh review V2: abort se repo non whitelisted
REM Note: REM lines with parens removed -- L-2026-05-015 PowerShell pollution mitigation Option B 2026-05-13
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8

REM Privacy guard rail check
set "REPO_ROOT="
for /f "delims=" %%i in ('git rev-parse --show-toplevel 2^>nul') do set "REPO_ROOT=%%i"
if "%REPO_ROOT%"=="" (
    echo ERROR: not in a git repo. aider-cerebras aborted ^(privacy guard rail H8^).
    exit /b 1
)
set "REPO_ROOT_WIN=%REPO_ROOT:/=\%"
set "WHITELIST=%USERPROFILE%\.config\aider-privacy-whitelist.txt"
if not exist "%WHITELIST%" (
    echo ERROR: privacy whitelist not found at %WHITELIST%
    echo aider-cerebras aborted ^(privacy guard rail H8^).
    exit /b 1
)
findstr /B /I /C:"%REPO_ROOT_WIN%" "%WHITELIST%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: repo NOT in cloud-OK whitelist:
    echo   repo: %REPO_ROOT_WIN%
    echo   whitelist: %WHITELIST%
    echo aider-cerebras aborted ^(privacy guard rail H8 ADR-0023^).
    echo If repo should be cloud-OK, add path to whitelist and retry.
    exit /b 1
)

aider --model cerebras/llama3.1-8b --edit-format diff --no-auto-commits --git-commit-verify --commit-prompt "Commit message MUST be in English, Conventional Commits format (type: short description), subject line <=72 chars total, lowercase description, no trailing period. Example: 'fix: handle null input in parser'." %*
