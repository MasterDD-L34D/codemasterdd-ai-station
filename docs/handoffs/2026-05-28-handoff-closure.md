# Handoff -- next session start (post 2026-05-28 closure)

> **Paste questo in una nuova Claude Code session** (cwd `C:\dev\codemasterdd-ai-station` su Lenovo, oppure `C:\dev\codemasterdd-ai-station` su Ryzen post-pull).
> Authored 2026-05-28 closure notte da Lenovo (CodeMasterDD/edusc/.10).

---

## Quick verify commands (run first, ~30sec)

```powershell
# PC identity
Write-Output ("PC=" + $env:COMPUTERNAME + " USER=" + $env:USERNAME)

# codemasterdd state
git -C C:/dev/codemasterdd-ai-station fetch origin main -q
git -C C:/dev/codemasterdd-ai-station log -1 --format='%h %s'
git -C C:/dev/codemasterdd-ai-station status -sb

# Agent scanner deployed? (should appear in skill-list automatically on Claude Code load)
Test-Path "$env:USERPROFILE\.claude\skills\agent-scanner\SKILL.md"
Select-String -Path "$env:USERPROFILE\.claude\CLAUDE.md" -Pattern "Agent Scanner discipline" | Select-Object -First 1
```

Expected:
- PC=CODEMASTERDD USER=edusc (Lenovo) OR PC=DESKTOP-T77TMKT USER=Vgit (Ryzen).
- codemasterdd HEAD `f9cf038` (or later) `docs(session): journal + compact_context v25 closure 2026-05-28`.
- Skill file present su Lenovo. **Su Ryzen NO se T13 deploy non ancora fatto**.

## Sintesi sessione precedente (2026-05-28)

**Giornata densissima**. 30+ commit codemasterdd, 3 PR Game merge, 1 PR vault external merge, 1 PR evo-swarm merge. Highlights:

1. **SoT Drift Sentinel** A+B LIVE (Game Action push:main + codemasterdd subagent verdict sovereign-gated).
2. **VC governance review** + 4 hardening (CI codemasterdd safety-net + scheduled mirror + Game #2410 ci-gate fix + `.aiderignore` privacy guard).
3. **OPEN_DECISIONS 9/9 CLOSED** (OD-005 FIRST_PRINCIPLES_INFRA_CHECKLIST.md BUILD + OD-007 cross-fleet agent-scanner 3-layer deploy + OD-009 ADR-0017 stack decommission).
4. **First-principles audit codemasterdd** (`docs/research/2026-05-28-codemasterdd-first-principles-audit.md`) -> 5 sub-agent dormant + scripts categorization + dead-weight delete.
5. **ADR-0017 decommission**: `git rm -r infra/ apps/dogfood-ui/` post-Hybrid-A1 (Pro+Meridian routing primario, NOT LiteLLM proxy).
6. **Cross-fleet pull-pass**: codemasterdd / Game / Game-Godot-v2 / Game-Database / vault / evo-swarm tutti sync. vault gc 99.93% orphan removal.
7. **3 nuove lessons**: L-038 (ESM CLI pathToFileURL Windows-vs-CI guard) + L-039 (Game branch-protection footgun fix) + L-040 (PowerShell native-stderr-under-Stop false-fail).

## Stato fleet 2026-05-28 closure

| Repo | Lenovo HEAD | Ryzen HEAD | Note |
|---|---|---|---|
| codemasterdd | `f9cf038` | `3feef6a` | **Ryzen behind 13 commit, T13 deploy pending** |
| Game | `31250b5d` | `14f2063a` (feat branch) | Ryzen su feature `aliena-coherence-diagnostic` |
| Game-Godot-v2 | `efd5bf6` | `efd5bf6` | synced |
| Game-Database | `13079e2` | `13079e2` | synced (CLAUDE.md drift fixed) |
| vault | `af851b67f` | `af851b67f` | synced (post #208 SoT demote + gc) |
| synesthesia | `05f8a92` | `05f8a92` | dormant UniUPO ago 2026 |
| evo-swarm | `10a40ba` (main) | `670e309` | Ryzen behind 1 (weekly digest merge today) |

## Cose da fare (priority ordered)

### 🟢 Quick wins (~5-15min ognuna, alta leverage)

1. **T13 Ryzen cross-fleet deploy** (~5min). Cose pratiche:
   ```powershell
   # da Lenovo, oppure dirett su Ryzen
   ssh Vgit@<ryzen-ip>
   cd C:/dev/codemasterdd-ai-station
   git pull origin main   # ~13 commit pending
   .\scripts\setup\deploy-global-skills.ps1 -Apply
   ```
   Expected: sandbox QG OK -> Phase 1+2+3 OK -> `DONE. Deploy successful.`
   Verify: `Get-FileHash $env:USERPROFILE\.claude\skills\agent-scanner\SKILL.md`.

2. **T12 behavioral smoke agent-scanner** (~10min). Apri **fresh Claude Code session** (cwd qualsiasi, no context inherit) + 3 prompt:
   - FIRE-A: `che agent uso per code review?` -> atteso scanner auto-invoca, raccomanda agent esistente.
   - FIRE-B: `scan agents` -> atteso ON_DEMAND full report.
   - FIRE-C: `fix typo at line 42 in foo.js` -> atteso STRONG-PURE fires (no eccezione).
   Cattura tokens + time -> aggiorna `codemasterdd/.claude/global-skills/agent-scanner/QUALITY.md` Step 3.

3. **U0-test** aider --browser (~10min). 1-2 dev-loop session. Gate UX accettabile? Si -> step 1+ ADR-0017 deferred (gia' superseded comunque); No -> opzionale flag follow-up.

### 🟡 Opportunistic (no time pressure)

4. **External-drive mirror copy** quando colleghi drive: `.\scripts\backup\copy-mirror-to-external.ps1 -Destination E:\codemasterdd-mirror-backup` (cadenza ~1x/mese opportunistica).
5. **M14 AA01 Task D**: vault Cards 3/4 sibling-peer (Eduardo-direct, fuori scope codemasterdd).
6. **TKT-ENCOUNTER-CLI** Game-side: future ticket Game BACKLOG, no codemasterdd action.

### ⚪ Standing items (no action needed unless trigger emerges)

- **M5 Synesthesia** privacy validation: dormant fino esame UniUPO ago 2026.
- **L1-L5 BACKLOG**: opportunistic re-bench / multimodal dogfood / skill audit cadence 3 mesi.

## Reading order (orient new session)

1. `CLAUDE.md` -- convenzioni progetto + Hybrid A1 + tier routing + PC identity refresh-verify.
2. `COMPACT_CONTEXT.md` v25 -- snapshot stato corrente (post questa sessione).
3. `STATUS_MULTI_REPO.md` -- dashboard cross-repo (refresh ~13/5 sera Eduardo Ryzen + addendum mattina epigenome Fase-3; sera-notte codemasterdd self-update non in STATUS, vive in JOURNAL).
4. `OPEN_DECISIONS.md` -- Snapshot 2026-05-28 player-recap in cima, 9/9 CLOSED.
5. `BACKLOG.md` -- Snapshot 2026-05-28 in cima, item residui by priority (U0-test + M5 + M14 + L1-5).
6. `JOURNAL.md` ultime 2 entries (sera-notte 2026-05-28) -- storia oggi.
7. **Memory file** `~/.claude/projects/C--dev-codemasterdd-ai-station/memory/project_session_resumption.md` -- pointer compatto + where-it-lives table.

## Cognitive protocols cheat-sheet (post questa sessione)

**Sempre** (P1 default): refresh-verify state interno PRE-action (`git log -1` + `gh pr list` + branch + memory).

**On-trigger**:
- **P2 autoresearch**: per audit/eval/research significativa (multi-source weighted; case ieri: VC governance review + LiteLLM/Langfuse decommission).
- **P5 harsh-reviewer** subagent: per spec architectural pre-merge OR cluster file security/governance-critical (case ieri: spec agent-scanner deploy + Game PR #2413 ci-gate pre-merge).
- **P6 brainstorming** superpowers skill: per design generative architectural (case ieri: 3-layer agent-scanner deploy options A/B/C).
- **P7 SDMG** Self-Designed-Method Governance: gate quando integri in governance durevole un metodo self-designed (4-stage falsification).

**Anti-pattern attivi sotto monitor**:
- **#19 stale-tracker**: ground-truth verify markers ⏳/🟡/PENDING/APERTA pre-action -- 3 caught oggi.
- **#9 idempotent-write sandbox-test**: ogni script idempotent-write deve avere -Apply sandbox PRE live (deploy script implementa nativo).
- **#11 fragile helper**: counting nested-quoting + cross-shell + unicode-touch + cross-tool-incompat layers >= 2 -> STOP scripting, runbook diretto.
- **#12 non-ASCII enforcement**: ASCII-first body prose per ADR-0021 nuovi file (`ps1|sh|bat|cmd|py|js|json|ya?ml` hook block).

## Per chiudere il giro -- auto-orient via compass

**`.compass.toml` configurato 2026-05-28 sera** (5 pillars: governance / agentic-tooling / cross-fleet-reproducibility / research-and-design / knowledge-preservation). Baseline Direction Index = 81/100 (rotta coerente).

**Workflow session-start ideale**:

1. **Invoca `/compass:boot`** -> auto-mini-brief 3-5 righe (Direction Index + top drift + next-smallest-step CONCRETO).
2. **Se Direction Index >= 75 + suggerimento concreto**: vai direttamente sul next-smallest-step suggerito (work alignment-coerente con pillars).
3. **Se Direction Index < 75 OR drift significativo**: invoca `/compass:drift` per dettaglio top-5 drift signals + threshold warning.
4. **Override manuale** (solo se compass non dà signal utile O hai priorità diversa): scegli tra Eduardo-manual residui (T13 Ryzen / T12 smoke / U0-test / opportunistic items).

**Combo cross-verify** post-compass-boot se serve diagnosi profonda:
- `agent-scanner` skill (LIVE post-deploy): "scan agents" -> inventario per anti-shadow-duplicate prima di selezionare specialist.
- `repo-health-auditor` subagent: cross-repo state audit on-demand quando il check fleet emerge dubbio.

**Se l'unico drift attuale (`knowledge-preservation` pillar)** suggerisce next-smallest-step su `docs/archive/ryzen-memory-archive/**`, NON forzare un commit cerimoniale solo per "alzare il numero". Il drift e' atteso (layer reference, non daily-touched). Tunabile via `/compass:evolve` se emerge pattern stabile.

Buona sessione.
