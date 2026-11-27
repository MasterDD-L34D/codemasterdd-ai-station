@echo off
REM Aider wrapper for cosmetic edits -- SUSPENDED 2026-11-27
REM Old model qwen2.5-coder:7b was removed from the Lenovo on 2026-11-27; the Ryzen dropped it earlier, see MODEL_ROUTING.md.
REM No local model is promoted for the cosmetic role, so this wrapper does NOT call aider.
REM Do not swap in another tag here: a new default needs a promotion in
REM C:\dev\codemasterdd-workspace\test-llm\INDICE-VALUTAZIONE-LLM.md first.
REM Meanwhile use a cloud-free wrapper with privacy guard, e.g. aider-cerebras, or Claude Code direct.
REM Note: REM lines with parens removed -- L-2026-05-015 PowerShell pollution mitigation Option B
echo aider-cosmetic SOSPESO: modello qwen2.5-coder:7b rimosso il 27/11/2026, nessun locale promosso per cosmetic. 1>&2
echo Usa un wrapper cloud-free con privacy guard, es. aider-cerebras, oppure Claude Code diretto. Vedi MODEL_ROUTING.md 1>&2
exit /b 1
