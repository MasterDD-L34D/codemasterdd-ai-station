# Handoff -- post-restart: SoT Drift Sentinel Component A

> Paste questo in una nuova sessione Claude Code (cwd `C:\dev\codemasterdd-ai-station`).
> Motivo restart: tdd-guard plugin disabilitato (settings `false`) ma hook ancora caricati
> da sessione precedente -> bloccava ogni `.mjs/.sh` impl (no reporter node:test = test
> uncaptured = validator blocca). Restart scarica gli hook.

## 0. PRIMA cosa: verifica tdd-guard OFF
Dopo restart dovrebbe essere off (enabledPlugins `tdd-guard@tdd-guard: false`). Se un Write
su `.mjs` viene ancora bloccato "Premature implementation": scrivi `.claude/tdd-guard/data/config.json`
= `{"guardEnabled": false}` e riprova.

## 1. GOAL
Eseguire **Component A** di SoT Drift Sentinel (Game-side GitHub Action, detection deterministica).
- Plan: `docs/superpowers/plans/2026-05-28-sot-drift-sentinel.md` -- Tasks 1-5 (contenuto file VERBATIM lì).
- Spec: `docs/superpowers/specs/2026-05-28-sot-drift-sentinel-design.md`.

## 2. GIA FATTO (non rifare)
- **Component B LIVE**: subagent `codemasterdd/.claude/agents/sot-drift-verifier.md` + `KNOWLEDGE_MAP.md` §8. Pushed (codemasterdd HEAD ~`7e8b04d`). logic-smoke PASS.
  - **TODO post-restart**: girare il LIVE subagent-dispatch smoke di `sot-drift-verifier` (ora registrato come subagent) -> flippa QG status a full-PASS nel file agent.
- **4 PR merged**: vault #202 (classification-4d Card) · #203 (epigenome SoT DEFERRED->SHIPPED) · #204 (gitignore .aider*) · Game #2403 (games-index link-fix + TKT-ENCOUNTER-CLI).
- Knowledge preservato: `docs/ryzen-memory-archive/` (139 file) + `docs/KNOWLEDGE_MAP.md` (mappa cross-repo SoT-vs-ref A0-A5 + reuse-queue §7 + drift-automation §8).

## 3. Component A -- file da creare (Game repo, PUBLIC)
- `.github/sot-drift/watch-map.yml` (config path-glob -> SoT-ref)
- `tools/sot-drift/detect.mjs` + `tools/sot-drift/detect.test.mjs` (matcher dep-free, TDD `node:test`)
- `.github/workflows/sot-drift-sentinel.yml` (trigger push:main -> diff -> detect -> idempotent gh issue)
- `tools/sot-drift/flag-issue.sh` (apre/aggiorna issue label `sot-drift-candidate`)
Contenuto esatto di ognuno = nel plan (Tasks 1-4). Smoke = Task 5.

## 4. COME eseguire A (logistica repo) -- IMPORTANTE
- Game local STALE (`196a63a4`, ~76+ behind origin) + `.husky/pre-commit` skip-worktree blocca commit su main.
  **USA WORKTREE fresco da origin/main**:
  `git -C C:/dev/Game worktree add -b claude/sot-drift-sentinel C:/dev/Game-drift origin/main`
  Build lì -> commit sul branch (husky permette non-main) -> push -> `gh pr create` (merge governance Game) -> `git worktree remove C:/dev/Game-drift --force`.
- Label one-time: `gh label create sot-drift-candidate --repo MasterDD-L34D/Game --color FBCA04 --description "Game runtime ahead of vault SoT"`.
- **Commit trailers OBBLIGATORI** (ADR-0011): `Coding-Agent: claude-...` + `Trace-Id: <uuid v4 ok>`, NO `Co-Authored-By`. Subject <=72 char, **descrizione minuscola dopo `type:`** (hook blocca "SoT" maiuscolo -> riformula "...for SoT...").
- TDD: il plan è red-green strutturato. Con tdd-guard OFF non interferisce. `node --test tools/sot-drift/detect.test.mjs`.

## 5. Stati repo
- codemasterdd: synced, PRIVATE, commit diretto OK.
- vault: synced `553b56c63`, sovereign, **branch+PR only** (merge Eduardo), no direct-main.
- Game: local stale -> worktree da origin/main (current ~`362f89df`+, public, PR governance-merge).

## 6. Gotchas
- **caveman mode full** attivo (terse; code/commit normali).
- Privacy: codemasterdd cloud-whitelisted aider -> `docs/ryzen-memory-archive/` valutare path-exclude wrapper cloud (follow-up KNOWLEDGE_MAP §6).
- SoT corre veloce (Game ship multipli/sessione) -> il sentinel È la mitigazione anti-#19 in costruzione.
- Sync cloni: vault FF-pull pulito; Game = husky-dance (comandi in KNOWLEDGE_MAP §6) o worktree.
