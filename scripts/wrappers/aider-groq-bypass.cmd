@echo off
REM Aider wrapper for Groq via OpenAI-compatible bypass -- LiteLLM Groq adapter bug workaround
REM Bypass GitHub Issues #9296 + #12660 + #4804 + #16040 LiteLLM-Groq streaming hang
REM Routes via LiteLLM OpenAI provider -- api_base=Groq URL -- skip buggy LiteLLM Groq adapter
REM Model: openai/llama-3.3-70b-versatile -- Groq 70B 280 tok per s 300K TPM Tier 1+
REM diff format + no-auto-commits + map-tokens 0 + no-stream -- safety + context reduction
REM --git-commit-verify: respect git hooks ADR-0011 Gap 3
REM Caveat: invia source code a Groq data retention ToS -- usare solo su repo non-sensitive
REM Privacy guard rail H8 2026-05-09 ADR-0023: abort se repo non whitelisted
REM Created 2026-05-13 -- T1 #9 SPRINT_02 entry #36 PASS
REM SECURITY HARDENED 2026-05-13 P0 fix harsh-reviewer: GROQ_API_KEY via temp env-file NTFS-protected NON in argv -- mitigation CWE-214
REM Note: REM lines no parens -- L-2026-05-015 PowerShell pollution mitigation Option B

setlocal
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8

REM Privacy guard rail check
set "REPO_ROOT="
for /f "delims=" %%i in ('git rev-parse --show-toplevel 2^>nul') do set "REPO_ROOT=%%i"
if "%REPO_ROOT%"=="" (
    echo ERROR: not in a git repo. aider-groq-bypass aborted -- privacy guard rail H8.
    endlocal
    exit /b 1
)
set "REPO_ROOT_WIN=%REPO_ROOT:/=\%"
set "WHITELIST=%USERPROFILE%\.config\aider-privacy-whitelist.txt"
if not exist "%WHITELIST%" (
    echo ERROR: privacy whitelist not found at %WHITELIST%
    echo aider-groq-bypass aborted -- privacy guard rail H8.
    endlocal
    exit /b 1
)
findstr /B /I /C:"%REPO_ROOT_WIN%" "%WHITELIST%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: repo NOT in cloud-OK whitelist:
    echo   repo: %REPO_ROOT_WIN%
    echo   whitelist: %WHITELIST%
    echo aider-groq-bypass aborted -- privacy guard rail H8 ADR-0023.
    echo If repo should be cloud-OK, add path to whitelist and retry.
    endlocal
    exit /b 1
)

REM Read GROQ_API_KEY from keys.env
set "GROQ_KEY="
for /f "tokens=2 delims==" %%i in ('findstr /B "GROQ_API_KEY" "%USERPROFILE%\.config\api-keys\keys.env"') do set "GROQ_KEY=%%i"
if "%GROQ_KEY%"=="" (
    echo ERROR: GROQ_API_KEY not found in %USERPROFILE%\.config\api-keys\keys.env
    endlocal
    exit /b 1
)

REM Write temporary ephemeral env-file -- key IN file NTFS-protected NOT in argv
REM Aider --env-file flag overrides .aider.conf.yml env-file: directive
set "TEMP_ENV=%TEMP%\aider-groq-bypass-%RANDOM%-%RANDOM%.env"
> "%TEMP_ENV%" echo OPENAI_API_KEY=%GROQ_KEY%

REM Invoke Aider with temp env-file -- key NOT in argv -- safe vs tasklist /v
REM --no-show-model-warnings -- suppress noise
REM --map-tokens 0 -- reduce context vs Groq 12k TPM legacy bottleneck (now 300K Tier 1+)
REM --no-stream -- bypass LiteLLM Groq streaming bug double safety
aider --env-file "%TEMP_ENV%" --openai-api-base https://api.groq.com/openai/v1 --model openai/llama-3.3-70b-versatile --edit-format diff --no-auto-commits --map-tokens 0 --no-stream --no-show-model-warnings --git-commit-verify --commit-prompt "Commit message MUST be in English, Conventional Commits format type colon short description, subject line less than 72 chars total, lowercase description, no trailing period. Example: fix: handle null input in parser." %*

REM Cleanup temp file -- key removed from disk
del /q "%TEMP_ENV%" 2>nul
endlocal
