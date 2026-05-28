# scripts/ -- categorization

Inventory + status classification per `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` test-di-cancellazione (vedi `docs/research/2026-05-28-codemasterdd-first-principles-audit.md`).

## Core daily (touched per session, cardine workflow)

- `hooks/commit-guard.js` -- PreToolUse Claude Code, enforce ADR-0011 commit trailers + Conventional format.
- `hooks/journal-drift-check.ps1` -- Stop hook, JOURNAL/COMPACT drift mitigation (H12).
- `hooks/session-start-marker.ps1` -- SessionStart hook, marker HEAD pre-session per journal-drift-check.
- `hooks/tddguard-seed-instructions.ps1` -- tdd-guard seed (disabilitato via config.json 2026-05-28).

## Setup (reproducible, run once per PC fleet)

- `setup/deploy-global-skills.ps1` -- L2+L3 cross-fleet deploy LITE skill + L3 directive ~/.claude/CLAUDE.md (sandbox QG + bounded sentinel + -Remove rollback). NEW 2026-05-28.
- `setup/install-privacy-guard.ps1` -- H8 ADR-0023 wrapper privacy guard installer.
- `setup/install-wrappers.ps1` -- installa 6+ aider wrapper canonical to `~/.local/bin/`.
- `setup/aider-wrapper-template.txt` -- template wrapper privacy guard block.
- `setup/test-privacy-guard.cmd` -- smoke test privacy whitelist hit/miss.

## Wrappers (delegation aider tier-routing, daily use)

- `wrappers/aider-cosmetic.cmd` -- Qwen 7B + diff + no-auto-commits.
- `wrappers/aider-refactor.cmd` -- Qwen 14B Q2 + diff + no-auto-commits.
- `wrappers/aider-groq-bypass.cmd` -- Groq llama-3.3-70b via OpenAI-compat (post LiteLLM-Groq adapter bug).
- `wrappers/aider-cerebras.cmd` -- Cerebras 8B + diff + no-auto-commits.
- `wrappers/aider-gemini.cmd` -- Gemini 2.5-flash + diff + no-auto-commits.
- `wrappers/aider-openai.cmd` -- gpt-4o-mini + diff + no-auto-commits.
- `wrappers/aider-hf.cmd` (proposed) -- HuggingFace Inference Providers proxy.
- `wrappers/aider-github-models.cmd` (proposed) -- GitHub Models GPT-4o 150 req/giorno free.

## Backup (idempotent, scheduled or on-demand)

- `backup/mirror-repos.ps1` -- bare-mirror locale 7 repo fleet (scheduled weekly Sun 10:00 via `codemasterdd-mirror-backup` Task Scheduler).
- `backup/copy-mirror-to-external.ps1` -- one-shot helper periodic copy a drive esterno (disk-loss insurance). NEW 2026-05-28.
- `backup-api-keys.ps1` -- daily snapshot `~/.config/api-keys/keys.env` (M7).

## Bench (run-on-demand, periodic re-bench)

- `bench-cloud.ps1` -- bench cloud tier 3 (Groq / Cerebras / Gemini / OpenAI).
- `bench-ollama.ps1` -- bench local Ollama models.
- `bench-mixed-workload/run-bench.ps1` -- mixed-workload n=4 per tier 7B/14B Q2/30B MoE (H9).
- `bench-opencode-cloud-free.ps1` -- bench OpenCode + cloud free providers (M10 conclusive).
- `quality-bench/load-problems.js` -- promptfoo problem loader (U3 ADR-0017 stack).
- `quality-bench/playwright-monitor-regression.py` -- regression monitor.
- `quality-bench/run-bench.ps1` -- promptfoo eval wrapper.

## Cross-repo / Sprint-time

- `cross-repo/coord-event-log.ps1` -- spec V3 cross-repo orchestrator (Component 2).
- `cross-repo/dry-run-pr.ps1` -- dry-run PR validator (Component 2).
- `cross-repo/install-gate-e-reminder.ps1` -- Gate E weekly reminder cron install (Component 3, Sprint-window).

## Smoke / quality

- `smoke-test-hooks.ps1` -- weekly hook chain smoke (M8). Scheduled Sunday 09:00.
- `governance-lint.ps1` -- governance file lint check.
- `task-classify.ps1` -- decision tree CLAUDE.md / ADR-0008/0016/0022 wrapper-routing helper (M9).
- `aider-log.sh` -- aider delegation log entry helper.
- `llmfit-task-eval.py` -- task-eval N-sample anti lucky-sample (anti-pattern #14 mitigation).

## One-time (executed once per PC initial bootstrap, retained for re-use on new fleet PC)

- `bitlocker-hard-disable.ps1` -- BitLocker triple-layer disable (Lenovo 2026-04-19).
- `disconnect-onedrive.ps1` -- OneDrive account unbind + sync block (Lenovo 2026-04-19).
- `godot-install-ryzen.ps1` -- Godot 4.x install (Ryzen one-time per PC).
- `migrate-log-to-sqlite.py` -- aider-delegation markdown -> dogfood.sqlite migration (executed once post Fase 6 closure).

## Audit notes (FIRST_PRINCIPLES audit 2026-05-28)

- Test di cancellazione applicato. NESSUNO script tagliato per cerimony. One-time scripts categorizzati per chiarezza (retained for new-PC bootstrap re-use cross-fleet).
- Quality-bench cluster e' parte dello stack ADR-0017. Stack post-Hybrid-A1 (ADR-0030) e' OD-009 review pending -- vedi OPEN_DECISIONS.
