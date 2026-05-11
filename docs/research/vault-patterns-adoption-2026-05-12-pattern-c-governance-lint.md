# Vault-shared pattern adoption -- Pattern C addendum (2026-05-12)

<!--
Cherry-pick policy applicata: pull-when-needed, audit-then-replay.
Source: vault-shared sibling-peer (C:/dev/vault-shared/, Karpathy LLM-wiki).
NO clone vault files, NO commit hash citato (drift risk repo Eduardo-driven).
Boundary: sovereign-only sibling-peer disjoint scope (memory project_vault_shared.md).
Audit-then-replay 2026-05-12 (AA01 task aa01-001-2026-05-11-vault-integration-readonly Phase 3-5).
-->

> **Scope**: addendum a `vault-patterns-adoption-2026-05-11.md` (PR #39). Documenta Pattern C ADOPT non coperto nella research doc precedente: governance-lint automation per drift detection codemasterdd, concept transfer da vault `vault-linter.md`.
>
> **Status**: Research complete + MVP implementation 2026-05-12. Smoke test 3/3 ALL-CLEAR su stato reale repo.
>
> **AA01 task source**: `2026-05-aa01-001-2026-05-11-vault-integration-readonly` Phase 0+3+4+5 (Phase 1+2 abbreviated per time-bound, sample 1 agent letto in dettaglio + frontmatter scanned per altri 6).

## TL;DR

Pattern C "vault-linter concept adoption" -> **ADOPT MVP** via `scripts/governance-lint.ps1` PowerShell-native (3 check categories: COMPACT HEAD sync + Coda PR consistency + JOURNAL stale).

Trigger empirico: questa stessa sessione 12/5 ha identificato manualmente 4 drift in COMPACT v20 (HEAD lag, Coda PR stale claim, Hyperspace status mismatch, worktree reference obsoleta). Automation ridurrebbe overhead manuale Protocol 1 refresh-verify.

## Decision matrix esteso

Aggiornamento alla tabella `vault-patterns-adoption-2026-05-11.md` con Pattern C esplicitato:

| Pattern | Source | Codemasterdd-side | Verdict | Stato implementazione |
|---------|--------|-------------------|---------|----------------------|
| A1 routing per-task granular | Vault `llm-routing.json` | -- | SKIP | (PR #39 closed) |
| A2 3-step Quality Gate | Vault `CLAUDE.md` Override globale | ADR-0018 | SKIP redundant | (PR #39 closed) |
| A3 A/B benchmark twin | Vault `Extras/benchmarks/TASK-002-AB` | -- | DEFER | (PR #39 closed) |
| B Agent template sections | Vault `production/agents/*.md` | `.claude/agents/SMOKE_TEST_TEMPLATE.md` + `SUB_AGENT_TEMPLATE.md` | EXPAND ADOPT | DONE (PR #39 closed) |
| C smoke_metric frontmatter | Vault frontmatter convention | -- | SKIP (inglobato in B body) | (PR #39 closed) |
| **D vault-linter concept** | **Vault `production/agents/vault-linter.md`** | **`scripts/governance-lint.ps1`** | **ADOPT MVP** | **DONE this PR (2026-05-12)** |

NOTE su naming: usata sigla "D" per evitare conflitto con Pattern C precedente (smoke_metric frontmatter SKIP). Originale DRAFT/02-adoption-decisions.md questa sessione nomava "Pattern C" -- rinominato in final doc per consistency.

## Pattern D implementation details

### Concept transfer (audit-then-replay)

Letto: `C:/dev/vault-shared/production/agents/vault-linter.md` (READ-ONLY, no clone).

Elementi concettuali trasferiti:
- **READ-ONLY operativo** (no edit su file controllati, output solo in report path)
- **Categorical checks** (link rotti / pagine orfane / claim stantii / frontmatter mancante / duplicati)
- **Report-only output** (no auto-fix)
- **Schedule weekly** (analogo a `HookIntegritySmoke` esistente)

NON trasferiti (audit-then-replay decisions):
- Python implementation (replay PowerShell-native, allinea con stack `scripts/*.ps1` codemasterdd)
- Vault-specific check categories (link rotti markdown, frontmatter Obsidian) -> replay con check categories codemasterdd-specifiche (COMPACT HEAD sync, Coda PR claim, JOURNAL stale)

### MVP scope finale (3 check categories)

1. **CHECK-1 COMPACT HEAD sync**: regex extract `HEAD origin/main \`<sha>\`` vs `git rev-parse --short origin/main`. Threshold: WARNING se lag >1 commit (lag=1 atteso post-merge per evitare false positive sistematici).
2. **CHECK-2 Coda PR consistency**: regex extract `Coda PR codemasterdd: VUOTA|N PR` vs `gh pr list --state open`. WARNING se mismatch.
3. **CHECK-3 JOURNAL stale**: regex extract ultima entry `## YYYY-MM-DD` (parse last match -- JOURNAL append-only oldest-first). WARNING se gap >14gg.

Checks 4-7 (markdown links / OD-ADR cross-ref / ADR Proposed age / worktree orphan) deferred Three Strikes monitor SPRINT_03+.

### Output

- Path: `logs/governance-lint-YYYY-MM-DD.md` (gitignored via `logs/*`)
- Format: Markdown con sezioni Summary / Findings (severity + detail + action) / All-clear / MVP scope
- Exit code: 0 ALL-CLEAR / 1 WARNING(s) / 2 CRITICAL(s)
- Flags: `-Quiet` (no stdout), `-OutputStdout` (no file write, stdout only)

### Smoke validation empirica

Run 3 iterazioni su stato reale codemasterdd:
1. **Run 1** (CHECK-3 bug select-first): 2 WARNING (CHECK-1 lag post-PR50 + CHECK-3 falso stale 23gg per parsing oldest-first)
2. **Run 2** (post fix Select-Last): 1 WARNING (CHECK-1 lag=1 post-merge atteso)
3. **Run 3** (post threshold tune lag>1): **3/3 ALL-CLEAR** confermato su stato reale

Bug discovery loop validato: il tool ha identificato 2 bug nella propria implementazione tramite self-application (false positive sistematico + parsing oldest-first). Pattern positive: dogfood-driven refinement.

### Effort reale vs stima

- Stima DRAFT/02: ~1.5-2h (script + smoke + schedule + runbook)
- Reale: ~50min (script + 2 bug fix iter + 3 smoke runs)
- Saving: 60% under estimate (no schedule install + no separate runbook necessario, script auto-documented)

## Findings cross-session

1. **Vault status drift confermato**: 7/7 agent `status: draft` frontmatter ma location `production/agents/`. Memory codemasterdd claim "7/7 production milestone" valid via interpretazione "location = ground truth". Caveat noted.
2. **Stack overlap vault-shared <-> codemasterdd**: Ollama LAN endpoint + 4 model family (qwen3-coder, qwen2.5-coder, mistral, deepseek-r1) verified empirically.
3. **Quality Gate equivalence con ADR-0018**: confermata gia in PR #39, NON re-investigata.
4. **Drift detection MVP fattibile**: 3 check categories sufficient per copertura governance core. Three Strikes monitor per expansion.

## Constraint hard respected

- [x] NO clone agent files da vault
- [x] Audit-then-replay pattern (concept letto, implementation PowerShell-native)
- [x] Attribution header in script implementation (source vault `vault-linter.md` concept, NO commit hash)
- [x] NO write su vault-shared (only Read tool)
- [x] Sovereign-only privacy preservata

## Next action

- **Implementation**: `scripts/governance-lint.ps1` (this PR)
- **Schedule install**: opzionale future (no questa PR scope) -- analogo a `scripts/setup/install-schtasks.ps1` esistente
- **Expand checks 4-7**: Three Strikes monitor SPRINT_03+ (trigger: 3+ drift detection PASS reali in 30gg + Eduardo confirm value)
- **Memory update**: `project_vault_shared.md` con Pattern D ADOPT note (post-merge questa PR)
