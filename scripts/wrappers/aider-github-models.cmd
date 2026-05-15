@echo off
REM Aider wrapper for GitHub Models -- tier 3 cloud free GPT-4o access
REM Endpoint: https://models.inference.ai.azure.com -- OpenAI-compatible drop-in
REM Default model: gpt-4o -- 150 req/giorno free tier per token GitHub fine-grained PAT
REM Alternative models: gpt-4o-mini, Llama-3.3-70B-Instruct, Mistral-Large-2407, Phi-3.5-MoE-instruct
REM Edit model line below to switch. See https://github.com/marketplace/models for full catalog
REM
REM diff format + no-auto-commits + map-tokens 0 + no-stream -- safety + context reduction
REM --git-commit-verify: respect git hooks ADR-0011 Gap 3
REM Caveat: invia source code a GitHub + upstream Azure OpenAI ToS -- usare solo su repo non-sensitive
REM Privacy guard rail H8 2026-05-09 ADR-0023: abort se repo non whitelisted
REM SECURITY HARDENED: GITHUB_MODELS_API_KEY via temp env-file NTFS-protected NON in argv -- mitigation CWE-214
REM Note: REM lines no parens -- L-2026-05-015 PowerShell pollution mitigation Option B
REM Created 2026-05-15 -- tier 3 add-on free LLM ecosystem audit verdict PROPOSED

setlocal
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8

REM Privacy guard rail check
set "REPO_ROOT="
for /f "delims=" %%i in ('git rev-parse --show-toplevel 2^>nul') do set "REPO_ROOT=%%i"
if "%REPO_ROOT%"=="" (
    echo ERROR: not in a git repo. aider-github-models aborted -- privacy guard rail H8.
    endlocal
    exit /b 1
)
set "REPO_ROOT_WIN=%REPO_ROOT:/=\%"
set "WHITELIST=%USERPROFILE%\.config\aider-privacy-whitelist.txt"
if not exist "%WHITELIST%" (
    echo ERROR: privacy whitelist not found at %WHITELIST%
    echo aider-github-models aborted -- privacy guard rail H8.
    endlocal
    exit /b 1
)
findstr /B /I /C:"%REPO_ROOT_WIN%" "%WHITELIST%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: repo NOT in cloud-OK whitelist:
    echo   repo: %REPO_ROOT_WIN%
    echo   whitelist: %WHITELIST%
    echo aider-github-models aborted -- privacy guard rail H8 ADR-0023.
    echo If repo should be cloud-OK, add path to whitelist and retry.
    endlocal
    exit /b 1
)

REM Read GITHUB_MODELS_API_KEY from keys.env
set "GITHUB_MODELS_KEY="
for /f "tokens=2 delims==" %%i in ('findstr /B "GITHUB_MODELS_API_KEY" "%USERPROFILE%\.config\api-keys\keys.env" 2^>nul') do set "GITHUB_MODELS_KEY=%%i"
if "%GITHUB_MODELS_KEY%"=="" (
    echo ERROR: GITHUB_MODELS_API_KEY not found in %USERPROFILE%\.config\api-keys\keys.env
    echo.
    echo SETUP STEPS:
    echo   1. Open https://github.com/settings/tokens?type=beta
    echo   2. Generate new fine-grained PAT:
    echo      - Resource owner: MasterDD-L34D
    echo      - Repository access: Public Repositories (read-only)
    echo      - Permission: Models read-only
    echo   3. Append to keys.env:
    echo      GITHUB_MODELS_API_KEY=github_pat_...
    echo   4. Retry aider-github-models
    endlocal
    exit /b 1
)

REM Write temporary ephemeral env-file -- key IN file NTFS-protected NOT in argv
set "TEMP_ENV=%TEMP%\aider-github-models-%RANDOM%-%RANDOM%.env"
> "%TEMP_ENV%" echo OPENAI_API_KEY=%GITHUB_MODELS_KEY%

REM Invoke Aider with temp env-file -- key NOT in argv -- safe vs tasklist /v
REM Default model: gpt-4o-mini via GitHub Models free tier (corretto 2026-05-15 endpoint + model namespace)
REM Endpoint NEW 2026: https://models.github.ai/inference (era models.inference.ai.azure.com deprecato)
REM Model namespace: openai/openai/gpt-4o-mini (Aider strips first openai/, GitHub Models receives openai/gpt-4o-mini)
aider --env-file "%TEMP_ENV%" --openai-api-base https://models.github.ai/inference --model openai/openai/gpt-4o-mini --edit-format diff --no-auto-commits --map-tokens 0 --no-stream --no-show-model-warnings --git-commit-verify --commit-prompt "Commit message MUST be in English, Conventional Commits format type colon short description, subject line less than 72 chars total, lowercase description, no trailing period. Example: fix: handle null input in parser." %*

REM Cleanup temp file -- key removed from disk
del /q "%TEMP_ENV%" 2>nul
endlocal
