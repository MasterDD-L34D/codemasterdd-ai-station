# ADR-0027 — Cross-PC clone architecture clarification (Lenovo + Ryzen)

## Status

**Accepted** — empirical evidence-driven, 2026-05-13 notte (auto-mode session ADR-0026 P3 Archon LITE protocol applied + P1 Refresh-verify saved expensive Archon work).

## Context

Sessione 2026-05-12 sera (cross-PC audit Ryzen+Lenovo, PR #69) ha rivelato cross-PC ecosystem reality: Ryzen ha 13 repo su `Desktop\repos\` + Game/Game-Godot-v2 su Desktop top + `_workspace` orchestration area + Vault origin Ryzen-side. PR #69 review (harsh-reviewer) ha enumerato 3 strategic questions deferred SPRINT_02 Protocol 3 Archon candidates:

- **Q1** codemasterdd policy hub home (Lenovo `C:\dev` vs Ryzen `Desktop\repos\_workspace`)
- **Q2** Game canonical clone (Lenovo passive vs Ryzen "active divergent" — claim PR #69)
- **Q3** 9 Ryzen-only repos status (STATUS_MULTI_REPO monitored vs silent-driver autonomous)

Sessione 2026-05-13 notte (auto-mode post Phase 1 R2/R4/R5 closure), Eduardo authorized "procedi auto modo come raccomandato dal metodo". Method = ADR-0026 Protocols 1-4.

## Decision

**P1 Refresh-verify empirical SHORT-CIRCUITED Archon 7-step needs** — tutte le 3 question RESOLVED senza deep analysis:

### Q1 — codemasterdd policy hub home: **FALSE DICHOTOMY**

Evidenza empirica refresh-verify 2026-05-13 notte:

| Asset | Path | Stato verificato |
|-------|------|------------------|
| codemasterdd repo | Lenovo `C:\dev\codemasterdd-ai-station` | Active policy hub, origin `e8ffa6a` PR #72, 72+ PR cumulative history |
| codemasterdd Ryzen clone | Ryzen `Desktop\repos\codemasterdd-ai-station` | **STALE**: branch `codex/structural-reset` HEAD `4b7c84a`, 6 ahead origin/main, NOT main, NOT active workflow |
| Ryzen `_workspace` | Ryzen `Desktop\repos\_workspace\` | 8 sub-dir (~1.1GB), TUTTI `2026-05-12` writes, contiene 109-file mirror operative-library + scratch areas evo-tactics 346MB + vault-overflow 694MB + synesthesia working files |

**Verdict Q1**: codemasterdd policy hub (versioned, ADR-grade governance) e Ryzen `_workspace` (non-versioned, personal operational scratch area) sono **OPERATIVAMENTE ORTOGONALI**, NON competing per stesso ruolo. NO migration architectural needed.

- codemasterdd Lenovo: **STATUS QUO mantained** come canonical policy hub
- Ryzen `_workspace`: **STATUS QUO mantained** come personal operational area
- Ryzen `Desktop\repos\codemasterdd-ai-station` clone: stale Codex branch, sandbox abandoned → BACKLOG cleanup candidate

### Q2 — Game canonical: **NARRATIVE DRIFT in PR #69**

Evidenza empirica refresh-verify 2026-05-13 notte:

| Clone | HEAD | Sync vs origin/main |
|-------|------|---------------------|
| Lenovo `C:\dev\Game` | `36c9822` "chore(phase-b): Day 5/8 OOA audit + Path C handoff preserve (#2258)" | `0 0` synced |
| GitHub origin/main | `36c9822` PR #2258 (2026-05-11) | (canonical) |
| Ryzen `Desktop\Game` | `5d27fc50` PR #2139 (older) | **`0 107` BEHIND**, detached-HEAD-like (empty current branch output), working tree dirty (apps/backend/* deletions) |

**Verdict Q2**: PR #69 claim "Ryzen Game AHEAD vs Lenovo" era **DRIFT NARRATIVO L-2026-05-002 case-study**. Reality empirical: origin/main canonical de-facto, Lenovo synced primary client, Ryzen clone è **stale exploration sandbox 107 commits behind** (NON active divergent canonical competitor). NO architectural decision needed — origin canonical pattern già in vigore.

Action follow-up: cleanup Ryzen Desktop\Game sandbox (delete o reset --hard origin/main + commit Eduardo-direct se Eduardo decide preservare un'esplorazione).

### Q3 — 9 Ryzen-only repos: **ADD minimal monitoring**

Repos elencati per stato attivita osservata empirical:

| Repo | Branch HEAD | Status inferito |
|------|-------------|------------------|
| claude-supermemory-local | main `a72152b` | Active (recent supermemory local SDK work) |
| compass-marketplace | `fix/marketplace-schema-source-string` `5943ffa` | Active (v0.4.3 fix in flight) |
| Game-Database | main `91f5468` PR #105 | Active (last merge) |
| Gpt | main (no HEAD shown) | Likely dormant (empty repo) |
| Item-generator | main `4c89a12` | Dormant (last work Pathfinder GPT enhancement) |
| LeaD | main `75c6961` "Initial commit" | Dormant |
| Master-DD-Pathfinder-GPT | `codex-fix-pr-542-follow-up-regressions-clean` `5bd2ccb` | Active (Codex branch in flight) |
| pathfinder-1e-homebrew | main `37801e0` "Initial commit" | Dormant |
| torneo-cremesi-site | main `43eda85` PR #18 | Active (last merge) |

**Verdict Q3**: aggiungi 5 active repos a STATUS_MULTI_REPO con minimal monitoring (1-line entry each); 4 dormant lasciati silent-driver autonomous (no friction). Trigger ADR addendum se uno dormant si attiva con scope strategic.

### R3 — Ryzen `core.hooksPath` install: **DORMANT, no trigger**

Empirical: Eduardo NON usa Ryzen `Desktop\repos\codemasterdd-ai-station` per commit workflow (è su Codex branch stale 6 ahead, ultimo movimento branch `codex/structural-reset` non-recent). Commit workflow codemasterdd avviene da Lenovo `C:\dev\codemasterdd-ai-station` (hookPath `C:/Users/edusc/.local/share/git-hooks` attivo). Game commits avvengono da Lenovo `C:\dev\Game` (`.husky/_` repo-local hooks).

**Verdict R3**: hookPath Ryzen install **non urgente**. Trigger emergent: se Eduardo inizia commit codemasterdd da Ryzen (futuro Q1 amendment), allora install hooksPath as side action. Currently NO trigger.

## Consequences

### Positive

- 3 strategic questions resolved senza Archon 7-step formal (~3h saved Opus time)
- L-2026-05-002 lesson REINFORCED: refresh-verify state interno PRIMA di analysis previene Archon over-engineered su narrative drift
- PR #69 narrative drift identified + corrected in CLAUDE.md
- No architectural lock-in decision necessary (status quo preserved)
- STATUS_MULTI_REPO update minimo (5 new active repos), low maintenance

### Negative / Trade-offs

- Ryzen `Desktop\Game` clone resta come stale sandbox (107 behind origin, dirty) — cosmetic clutter, NON impacto operatività
- Ryzen `Desktop\repos\codemasterdd-ai-station` resta clone abandoned Codex branch — cleanup deferred
- Q3 minimal monitoring richiede aggiornamento STATUS_MULTI_REPO se entries cambiano status (dormant -> active)

### Cleanup BACKLOG candidates

- C1 (low priority): Ryzen Desktop\Game sandbox reset --hard origin/main o deletion (Eduardo-direct)
- C2 (low priority): Ryzen Desktop\repos\codemasterdd-ai-station Codex branch cleanup (Eduardo-direct)

## Validation

Empirical evidence:
- `git log --oneline -3` Lenovo Game (riga 73 conferma main `36c9822` synced)
- `git rev-list --left-right --count HEAD...origin/main` Ryzen Game = `0 107` (BEHIND, NON AHEAD)
- `git rev-list --left-right --count HEAD...origin/main` Ryzen codemasterdd Desktop\repos = `6 0` su branch `codex/structural-reset` (NOT main)
- `_workspace` 8 sub-dir analysis: tutti `2026-05-12` last write, 1.1GB cumulative, contenuti scratch + framework mirror

## Ratification trigger

ADR Accepted da subito (early-acceptance ADR-0010 pattern, low-stakes empirical findings). Ratification check NON necessario perche` decisione = "status quo preserved" + cleanup candidates BACKLOG. Se uno dei 4 dormant Ryzen-only repos diventa active strategic, trigger Q3 addendum.

## References

- PR #69 cross-PC drift fix 2026-05-12 (originated Q1/Q2/Q3 deferred)
- L-2026-05-002 Hyperspace audit cycle anti-pattern (one-shot README + narrative drift)
- L-2026-05-014 candidate (autoresearch first, in promotion)
- ADR-0026 cognitive workflow protocols (P1 Refresh-verify + P3 Archon)
- Session 2026-05-13 notte auto-mode execution

## Addendum anti-rot — snapshot HEAD/N-behind rotti (fence 2026-05-17)

⚠️ **I verdetti Q1/Q2/Q3 restano VALIDI** (status-quo, Lenovo=hub
canonico, Ryzen=scratch ortogonale, no migration). **Ma le tabelle
HEAD/N-behind erano snapshot 2026-05-13 e sono ROTTE** (audit veracità
ADR 2026-05-17, regola-0):

- "Ryzen Game `5d27fc50` 107 BEHIND" / "codemasterdd Ryzen `4b7c84a`
  6-ahead codex" = conteggi 2026-05-13. Verifica fresca 2026-05-17:
  Game origin `427db9a6`, cloni Ryzen Game+codemasterdd **riallineati a
  origin/main** (0/0) post-fix; vault Ryzen sempre synced. Q3 repo-HEAD
  (Game-Database `91f5468` → ora `3be942cc`) rotti.

**Trattamento**: verdetti invariati; le tabelle HEAD/N-behind = *snapshot
storico 2026-05-13, NON stato corrente*. Stato cloni reale → eseguire
`Vault-ops-remote/scripts/cross_pc_mgmt_reconcile.py` (git-truth fresh),
mai i numeri qui. Anti-rot principio #135 (decouple narrativa da
git-truth).

## Addendum 2026-05-17 — Capability-parity objective (Eduardo-decided, scoped override)

**Status**: Accepted (Eduardo decision 2026-05-17).

**Contesto**: cross-PC reconciliation 2026-05-17 ha rivelato che il layer
`~/.claude` + sistema metodo-personale (ARCHON v2 + AA01 engine) era
**100% Lenovo-only, zero Ryzen, zero git** → causa-radice profonda di
"Claude si comporta diversamente per PC" a livello **capacità/metodo**
(non solo repo-clone-staleness, già trattata sopra).

**Decisione (obiettivo Eduardo)**: per il **layer user-home capability**
(`~/.claude`: CLAUDE.md, skills, agents, hooks, commands, plugins-set,
ARCHON/AA01 engine) l'obiettivo diventa **parità funzioni-complete identiche
su ENTRAMBI i PC**. Questo **supersede localmente** il framing
"Ryzen = stale exploration sandbox" *limitatamente a questo layer*.

**NON cambia** (resta valido dal corpo ADR-0027): repo-clone canonical =
origin/main; Lenovo = primary client per i repo; Ryzen-repo-clones =
sandbox (staleness gestita via reconcile, non via parità forzata).
La parità è del **capability/engine layer**, non dei **repo working-copies**.

**Distinzione parità**:
- **Engine/metodo/agent/skill/regole/hooks** = identici, git-truth-deployed
  entrambi PC (via `deploy_claude_global.ps1` + canonical-config).
- **Dati-task personali** (AA01 inbox/workspace/archive/decision-log/lesson):
  Eduardo 2026-05-17 ha autorizzato **sync in vault-privato git** (opzione
  "Engine completo + dati sync") → parità totale incluso storico personale.
  Audience-expansion scritture personali consapevolmente autorizzata
  (vault = repo privato MasterDD-L34D).

**Implementazione**: vendor ARCHON+AA01 → `Vault-ops-remote/claude-global/`;
deploy esteso path-canonico entrambi PC; reconcile.py `--parity` flag drift.
Anchor metodologico: ADR-0026 triple→quad-anchor (+layer `~/.claude`).
Cross-link: vault `docs/decisions/OD-046` (lesson-layer durability).
