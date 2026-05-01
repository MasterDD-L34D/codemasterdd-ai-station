# DECISIONS_LOG

Indice decisionale corrente.

Gli ADR in `docs/adr/` restano la fonte storica delle decisioni strategiche.
Questo file e' l'indice operativo aggiornato per la recovery.

## Decisione corrente di recovery

### Decisione R-2026-04-30-001 - Scope reset post-transplant

- Data: 2026-04-30.
- Status: active.
- Decisione: `codemasterdd-ai-station` governa solo se stesso finche i repo
  esterni non vengono riattivati.
- Rationale: i path originali di Game, Synesthesia, Dafne e AA01 non esistono
  in questa copia; governarli da qui produrrebbe piani non verificabili.
- Output:
  - `docs/recovery/2026-04-30-transplant-audit.md`
  - `EXTERNAL_REPOS.md`
  - `SPRINT_02.md`

### Decisione R-2026-04-30-002 - Historical files are retained

- Data: 2026-04-30.
- Status: active.
- Decisione: non cancellare ADR, Journal, session logs, archive framework o
  agent cross-repo nel primo pass.
- Rationale: la priorita e' ridurre la superficie attiva, non perdere storia.
- Consequence: molti file restano nel repo ma non sono automaticamente live.

### Decisione R-2026-04-30-003 - Runtime evidence must exist locally

- Data: 2026-04-30.
- Status: active.
- Decisione: log, DB, promptfoo outputs e backup gitignored non sono fonte di
  verita se non esistono nella copia locale.
- Rationale: diversi vecchi file root assumevano presenti dati non trasportati.

### Decisione R-2026-05-01-004 - Structure over cross-repo orchestration

- Data: 2026-05-01.
- Status: active.
- Decisione: prima di riattivare Game, Synesthesia, Dafne o AA01, il repo deve
  avere una mappa di sistema, un profilo macchina locale, una dashboard recovery
  e uno script unico di verifica.
- Rationale: senza questi guardrail, i vecchi piani cross-repo tornano a
  confondersi con lo stato reale del checkout.
- Output:
  - `config/system-map.yaml`
  - `config/machine-profile.example.yaml`
  - `docs/recovery/client-runtime-matrix.md`
  - `scripts/recovery-status.ps1`
  - `scripts/check-all.ps1`
  - `apps/dogfood-ui/templates/recovery.html`

## ADR index

| # | Topic | Status in file | Recovery interpretation |
|---:|-------|----------------|-------------------------|
| 0001 | Sovereign AI strategy | Accepted | Historical backbone; keep. |
| 0002 | Workstation naming CodeMasterDD | Accepted | Historical; keep. |
| 0003 | Node 24 vs 22 | Accepted | Historical setup decision; verify locally before using. |
| 0004 | Ollama RTX 5060 config | Accepted/updated | Original-machine config; dormant until local Ollama verified. |
| 0005 | YAGNI minimalism approach | Accepted | Active principle. |
| 0006 | Cline + Qwen 7B viability | Accepted | Historical; keep. |
| 0007 | Aider + Qwen quantization findings | Partially superseded | Dormant unless wrappers/models verified. |
| 0008 | Aider whole format silent-corruption | Accepted | Active safety principle. |
| 0009 | Upgrade strategy | Proposed/addended | Historical strategy; not active plan. |
| 0010 | MADR format + skill policy | Accepted | Active documentation principle. |
| 0011 | Cross-agent commit governance | Accepted | Active principle, local hook presence unverified. |
| 0012 | RAM upgrade 64GB impact | Accepted | Original-machine hardware decision; verify current hardware before using. |
| 0013 | Tier 3 cloud free providers | Accepted | Dormant until keys/wrappers verified. |
| 0014 | Fase 6 timeline compression | Accepted | Historical; dogfood closure is not actionable without missing evidence. |
| 0015 | Fase 7 budget decision full-sovereign | Proposed | Dormant ratification; depends on missing/runtime evidence. |
| 0016 | Constraint-count routing dimension | Proposed | Useful heuristic; Accepted trigger is dormant without dogfood evidence. |
| 0017 | UI + observability stack | Proposed / validated live historically | Scaffold present; runtime live state unverified here. |
| 0018 | Agent readiness protocol | Accepted | Active principle; many agents now require reactivation. |
| 0019 | Dafne process persistence | Accepted | Historical/dormant here because Dafne path is missing. |
| 0020 | Silent-fail Python guardrail | Accepted | Active safety principle, local hook presence unverified. |
| 0021 | Structural recovery and external repo quarantine | Accepted | Active recovery architecture for this branch. |

## In review after recovery

- Should `CLAUDE.md` remain the tracked operational file, or should the repo
  migrate to `AGENTS.md` for Codex-first usage?
- Should `apps/dogfood-ui` remain in active scope or be moved to dormant
  scaffold?
- Should runtime artifacts get an export bundle format for future machine moves?
- Should cross-repo agents be moved out of `.claude/agents/` or only labelled?

## Closed or dormant old decisions

Old OD/H/M/U labels from Sprint 01 are historical unless reintroduced in
`SPRINT_02.md`.
