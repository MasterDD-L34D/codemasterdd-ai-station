@echo off
REM Aider wrapper for behavior-critical edits refactor bug fix logic change
REM Model: Qwen 14B Q2 + diff format + no-auto-commits ADR-0008 safety protocol
REM --commit-prompt: enforce English + Conventional Commits ADR-0011 Gap 2C
REM --git-commit-verify: respect git hooks ADR-0011 Gap 3 Aider default False
REM cp1252 fix 2026-04-23: force console + Python UTF-8 to avoid Rich UnicodeEncodeError on retry loop dogfood #3 bug
REM Note: REM lines with parens removed -- L-2026-05-015 PowerShell pollution mitigation Option B 2026-05-13
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
aider --model ollama/qwen2.5-coder:14b-instruct-q2_K --edit-format diff --no-auto-commits --git-commit-verify --commit-prompt "Commit message MUST be in English, Conventional Commits format (type: short description), subject line <=72 chars total, lowercase description, no trailing period. Example: 'fix: handle null input in parser'." %*
