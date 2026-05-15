@echo off
REM Aider wrapper for HuggingFace Inference Providers -- tier 3 cloud free unified proxy
REM Endpoint: https://router.huggingface.co/v1 -- OpenAI-compatible drop-in
REM Default model: deepseek-ai/DeepSeek-R1:fastest (reasoning specialty, free via HF inference)
REM Alternative models: openai/gpt-oss-120b:fastest, Qwen/Qwen2.5-Coder-32B-Instruct, Black-forest-labs/FLUX.1-dev (image)
REM Edit model line below to switch. Model suffix :fastest|:cheapest|:preferred per HF router policy
REM
REM diff format + no-auto-commits + map-tokens 0 + no-stream -- safety + context reduction
REM --git-commit-verify: respect git hooks ADR-0011 Gap 3
REM Caveat: invia source code a HF + selected upstream provider ToS -- usare solo su repo non-sensitive
REM Privacy guard rail H8 2026-05-09 ADR-0023: abort se repo non whitelisted
REM SECURITY HARDENED: HUGGINGFACE_API_KEY via temp env-file NTFS-protected NON in argv -- mitigation CWE-214
REM Note: REM lines no parens -- L-2026-05-015 PowerShell pollution mitigation Option B
REM Created 2026-05-15 SPRINT_02 integration HF + NotebookLM

setlocal
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8

REM Privacy guard rail check
set "REPO_ROOT="
for /f "delims=" %%i in ('git rev-parse --show-toplevel 2^>nul') do set "REPO_ROOT=%%i"
if "%REPO_ROOT%"=="" (
    echo ERROR: not in a git repo. aider-hf aborted -- privacy guard rail H8.
    endlocal
    exit /b 1
)
set "REPO_ROOT_WIN=%REPO_ROOT:/=\%"
set "WHITELIST=%USERPROFILE%\.config\aider-privacy-whitelist.txt"
if not exist "%WHITELIST%" (
    echo ERROR: privacy whitelist not found at %WHITELIST%
    echo aider-hf aborted -- privacy guard rail H8.
    endlocal
    exit /b 1
)
findstr /B /I /C:"%REPO_ROOT_WIN%" "%WHITELIST%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: repo NOT in cloud-OK whitelist:
    echo   repo: %REPO_ROOT_WIN%
    echo   whitelist: %WHITELIST%
    echo aider-hf aborted -- privacy guard rail H8 ADR-0023.
    echo If repo should be cloud-OK, add path to whitelist and retry.
    endlocal
    exit /b 1
)

REM Read HUGGINGFACE_API_KEY from keys.env
set "HF_KEY="
for /f "tokens=2 delims==" %%i in ('findstr /B "HUGGINGFACE_API_KEY" "%USERPROFILE%\.config\api-keys\keys.env" 2^>nul') do set "HF_KEY=%%i"
if "%HF_KEY%"=="" (
    echo ERROR: HUGGINGFACE_API_KEY not found in %USERPROFILE%\.config\api-keys\keys.env
    echo.
    echo SETUP STEPS:
    echo   1. Signup https://huggingface.co
    echo   2. Generate fine-grained token at https://huggingface.co/settings/tokens
    echo      with permission "Make calls to Inference Providers"
    echo   3. Append to keys.env:
    echo      HUGGINGFACE_API_KEY=hf_...
    echo   4. Retry aider-hf
    endlocal
    exit /b 1
)

REM Write temporary ephemeral env-file -- key IN file NTFS-protected NOT in argv
set "TEMP_ENV=%TEMP%\aider-hf-%RANDOM%-%RANDOM%.env"
> "%TEMP_ENV%" echo OPENAI_API_KEY=%HF_KEY%

REM Invoke Aider with temp env-file -- key NOT in argv -- safe vs tasklist /v
REM Default model: deepseek-ai/DeepSeek-R1:fastest -- adjust below for different model
aider --env-file "%TEMP_ENV%" --openai-api-base https://router.huggingface.co/v1 --model openai/deepseek-ai/DeepSeek-R1:fastest --edit-format diff --no-auto-commits --map-tokens 0 --no-stream --no-show-model-warnings --git-commit-verify --commit-prompt "Commit message MUST be in English, Conventional Commits format type colon short description, subject line less than 72 chars total, lowercase description, no trailing period. Example: fix: handle null input in parser." %*

REM Cleanup temp file -- key removed from disk
del /q "%TEMP_ENV%" 2>nul
endlocal
