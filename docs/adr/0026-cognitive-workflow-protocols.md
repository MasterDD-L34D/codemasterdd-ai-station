# ADR-0026 -- Cognitive workflow protocols (AA01 + autoresearch + Archon)

> *TL;DR: Formalize integration di 3 cognitive workflow protocols (AA01 + autoresearch + Archon) come **operating rules codemasterdd**, non solo memory feedback. Trigger phrases esplicit per ogni protocol + cross-link methodology lesson L-2026-05-002 + L-2026-05-003. Rationale: mio error 2026-05-11 sera (refresh-verify state interno MANCATO -> ADR-0025 CONDITIONAL GO erroneous) è caso studio gap integration governance permanent vs memory drift. Triple anchor (ADR + memory + CLAUDE.md) preserva methodology cross-session anche se memory non loaded.*

- **Status**: **Proposed** (2026-05-12)
- **Data**: 2026-05-12
- **Decisore**: Eduardo Scarpelli (final accept/reject)
- **Deciders**: solo-dev

## Context and Problem Statement

### Stato pre-ADR (gap analysis 2026-05-12)

4 cognitive workflow tools usati durante sessioni Claude Code, integrazione asimmetrica:

| Component | Memory | CLAUDE.md | ADR | Verdict integration |
|-----------|--------|-----------|-----|---------------------|
| **Vault sibling-peer** | ✅ `project_vault_shared.md` | ✅ linee 171-180 | ✅ ADR-0023 reference + research doc 2026-05-11 | ✅ FULL |
| **AA01 Personal Cognitive Studio** | ✅ `project_aa01_studio.md` | ⚠️ marginale (riga 139 Game context) | ❌ Nessuno | ⚠️ PARTIAL |
| **Autoresearch 8-step** | ✅ `feedback_autoresearch_default.md` + `reference_autoresearch_tools.md` | ❌ Zero match | ❌ Nessuno | ⚠️ MEMORY-ONLY |
| **Archon v2 7-step First Principles** | ❌ **None pre-ADR** (creata in this commit) | ❌ Zero match | ⚠️ Solo ADR-0025 D-009/D-015 reference | ❌ NOT-INTEGRATED |

### Caso studio root-cause: mio error 2026-05-11 sera

In sessione 2026-05-11 sera ho startato aa01-003 hyperspace audit web-only autoresearch (6 fonti parallel) **SENZA** refresh-verify state interno. Task aa01-001 fleet-discovery aveva già completato (2026-05-10 sera / 2026-05-11 mattina) 22 decisions empirico (D-001 to D-022) con verdict **NO-GO empirico definitivo** (D-017, 99% confidence) post 30s daemon trial + pktmon capture.

Mio audit web-only ha:
- Duplicato 4-5h lavoro empirico precedente
- Reached verdict ERRATO (CONDITIONAL GO 5 hard gates) vs reality (NO-GO empirico)
- ADR-0025 originale CONDITIONAL GO -> AMEND post discovery NO-GO

**Root cause analysis** (lesson L-2026-05-003):
1. Memory `feedback_governance_refresh_verify` esisteva MA non in CLAUDE.md operating rules → NOT loaded sempre
2. AA01 task aa01-001 (22 decisions) NON cross-referenced da CLAUDE.md → invisibile a session che legge solo CLAUDE.md
3. Archon protocol applied solo in lesson L-2026-05-002 post-fact, non come pattern enforced
4. Autoresearch enforce solo memory `feedback_autoresearch_default` → drift risk

**Recovery costo**:
- AMEND ADR-0025 (commit `b36a7df`)
- AMEND research doc + memory + JOURNAL + PR description
- Lesson L-2026-05-003 created (capture methodology pattern)
- Process honesty preserved transparency

**Prevention pattern**: integration **triple anchor** (ADR + memory + CLAUDE.md) per cognitive workflow methodology. Memory drift mitigated da ADR governance permanent + CLAUDE.md authoritative.

## Decision

### Adottare cognitive workflow protocols come operating rules

3 protocols formalmente integrati come operating rules codemasterdd:

#### Protocol 1 -- Refresh-verify state interno (PRE-action)

**Source**: memory `feedback_governance_refresh_verify` (caso studio PR #11 8/5 + ADR-0025 amend 12/5).

**Rule**: PRIMA di azione significativa (audit / eval / decision / commit governance), verifica state interno:
1. **AA01 workspace** (`bash scripts/status.sh`) -- task attivi + recent archive
2. **AA01 decisions logs** dei task workspace correlati allo scope corrente
3. **Memory recente** (`MEMORY.md` index + memory file rilevanti)
4. **Codemasterdd ADR** existing che già coprono lo scope
5. **Git state** repo monitored se rilevante (`git log -1` + `gh pr list`)
6. **Filesystem check** per file promessi/cited da governance (es. template promessi ADR-0018)

**Trigger**: ogni audit / eval / new ADR / strategic decision.

**Anti-pattern**: ereditare narrative da COMPACT/JOURNAL precedente senza re-verify source-of-truth.

#### Protocol 2 -- Autoresearch multi-source synthesis

**Source**: memory `feedback_autoresearch_default` (8-step checklist).

**Rule**: per audit / eval / research, multi-source parallel investigation con synthesis weighted (NON one-shot README).

**8-step checklist**:
1. README empirical (starting point, NON authoritative)
2. Release tag history + changelog dedicato (verify version drift)
3. Recent announcement (Twitter/blog/X feed)
4. WebSearch broader context
5. Sibling repos / org repos correlati
6. GitHub Discussions / issues recenti (real-world friction)
7. License + LICENSE file empirical (404 check)
8. Synthesis multi-source con weighting (recent > old, multiple corroborate > single signal, **internal > external**, **empirical > documentation**)

**Trigger**: ogni audit / eval / research significativa.

**Anti-pattern**: one-shot README fetch + verdict confidente.

#### Protocol 3 -- Archon v2 7-step First Principles (high-stakes)

**Source**: memory `reference_archon_protocol` (created 2026-05-12).

**Rule**: per decisioni high-stakes (architectural lock-in irreversibile / pivot framework / abandonment workflow), applicare Archon v2 7-step protocol:
1. **RESTATE** problema vero
2. **ENUMERATE** assunzioni espliciti + impliciti
3. **DECOMPOSE** primitivi irriducibili
4. **CHALLENGE** 5-perché + truth-maker
5. **RECONSTRUCT** soluzione da primitivi
6. **RED-TEAM** pre-mortem 12 mesi
7. **CALIBRATE** verdict + confidence + falsifying experiment ~30s-5min

**Trigger**:
- Audit ha prodotto >=3 cicli verdict opposti
- Decision architectural irreversibile
- "Sono sicuro?" introspection trigger
- High-stakes adoption / pivot / abandonment

**Anti-pattern**: skip Archon per decision time-sensitive >15min lock-in (over-engineered se patch fix routine).

**Path Archon**: `C:/Users/edusc/aa01/archon/system/ARCHON_v2_SYSTEM.md` + BOOTSTRAP. Invoke manuale via read protocol + apply mentally (NON automation in codemasterdd).

#### Protocol 4 -- AA01 workspace audit trail (workflow standard)

**Source**: memory `project_aa01_studio`.

**Rule**: per audit / eval / research / pivot / strategic decision significativa, usare AA01 workflow standard:
1. Capture in `inbox/<YYYY-MM-DD-slug>.md` (zero friction)
2. Classify: `bash scripts/classify.sh inbox/<file>`
3. Promote: `bash scripts/promote.sh inbox/<file> <preset>` (research-long / code-sprint / design-iteration / idea-capture / code-long-alpha / code-maintenance)
4. DRAFT lavoro fino a PROPOSED
5. Lesson scritta in `lesson.md` (obbligatoria per SHIP)
6. Archive `--status=SHIP|REJECT|DORMANT|TIMEOUT`
7. Promote lesson `learnings/L-YYYY-MM-NNN-<slug>.md`

**Trigger**: ogni audit/eval/research >=30min effort + cross-session value.

**Anti-pattern**:
- F2 cimitero (archive senza lesson)
- F3 confused re-opening (modifica archive)
- F4 inbox-zero theater (auto-promote senza confirm) -- ECCEZIONE: plan formalmente approvato Eduardo

**Path AA01**: `C:/Users/edusc/aa01/` (separato codemasterdd, NON-git, disciplina personale).

### Combined methodology

Lesson L-2026-05-002 + L-2026-05-003 cattura combined methodology:

```
[Trigger: audit / eval / decision significativa]
        ↓
Protocol 1: Refresh-verify state interno (OBBLIGATORIO)
        ↓
Protocol 4: AA01 workspace audit trail (start)
        ↓
Protocol 2: Autoresearch multi-source (NECESSARY ma INSUFFICIENT)
        ↓
[Decision high-stakes irreversibile?]
        ├── SI → Protocol 3: Archon 7-step First Principles
        |          ↓
        |       CALIBRATE → falsifying experiment ~30s-5min
        |          ↓
        |       [Confidence >70% post-empirical?]
        |          ├── SI → formalize decision (ADR / commit / PR)
        |          └── NO → iterate Archon o defer
        ↓
[Decision low-medium stakes]
        ↓
Empirical trial breve per architectural validation
        ↓
Synthesis weighted (internal > external, empirical > documentation, recent > old)
        ↓
Output: ADR Proposed / research doc / lesson / archive AA01 SHIP
```

### Application precedence

Ordine application (NOT necessariamente strict sequence):
1. **Protocol 1 ALWAYS** (refresh-verify state PRE-action)
2. **Protocol 4 if effort >=30min** (AA01 workspace)
3. **Protocol 2 if external research needed** (autoresearch multi-source)
4. **Protocol 3 if high-stakes irreversibile** (Archon 7-step)

Empirical trial breve è cross-cutting (NOT a separate protocol but enabler per Protocol 2+3 validation).

## Options considered

### Opzione A -- Triple anchor governance (ADR + memory + CLAUDE.md) (scelta)

3 protocols formalizzati come operating rules + memory + ADR + CLAUDE.md addendum.

**Pro**:
- Governance permanent (ADR authoritative)
- Memory drift mitigated
- CLAUDE.md always-loaded reference
- Prevention mio error 2026-05-11 pattern recurrence
- Lesson L-2026-05-002+003 cattura in governance permanent

**Contro**:
- Setup cost ~60min (ADR + memory + CLAUDE.md addendum + commit)
- Risk over-formalization se protocols evolvono

### Opzione B -- Memory-only + CLAUDE.md lean (zero ADR)

Solo memory updates + CLAUDE.md short addendum, no ADR.

**Pro**: lower effort (~25min)
**Contro**:
- Memory drift risk preservato
- CLAUDE.md può drift senza authoritative governance
- Lesson methodology vulnerable a memory not-loaded

**Verdict**: scartata -- preserve drift risk identificato come root cause mio error.

### Opzione C -- Defer post-Max SPRINT_02

Zero effort window pre-Max, defer 20/05+.

**Pro**: zero token spend
**Contro**:
- Same error pattern può ripetere prima del 19/05
- Window strategic (Tier 0 ADR-0023 capability) MANCATA

**Verdict**: scartata -- gap critical, preserve recurrence.

## Consequences

### Positive

- Triple anchor governance permanent (ADR + memory + CLAUDE.md authoritative)
- Methodology lesson L-2026-05-002+003 catturata in governance permanent
- Prevention mio error pattern recurrence
- Cognitive workflow consolidated come operating rules cross-session
- Future Claude Code session che legge CLAUDE.md ha visibilità immediata trigger phrases per ogni protocol

### Negative

- ADR governance bloat marginale (+1 ADR)
- Memory addition (`reference_archon_protocol`)
- CLAUDE.md addition section "Cognitive workflow protocols"

### Mitigations

- Lesson L-2026-05-002+003 documented + cross-linked
- ADR-0026 cita esempi concrete (aa01-001 22 decisions)
- Anti-pattern dichiarati esplicit per ogni protocol

## Path Reference (AA01 personale, NON-clone codemasterdd)

Cherry-pick policy: NON clonare Archon docs / AA01 scripts in codemasterdd. Reference path only.

- AA01: `C:/Users/edusc/aa01/` (workspace + inbox + archive + learnings)
- Archon: `C:/Users/edusc/aa01/archon/system/ARCHON_v2_{SYSTEM,BOOTSTRAP}.md` + folders
- Lesson L-2026-05-002: `C:/Users/edusc/aa01/learnings/L-2026-05-002-hyperspace-audit-cycle.md`
- Lesson L-2026-05-003: `C:/Users/edusc/aa01/learnings/L-2026-05-003-cross-repo-pattern-adoption.md`

## CLAUDE.md addendum (to be added in PR atomic)

Section "Cognitive workflow protocols" link a questo ADR + 4 protocols trigger phrases sintetiche.

## Related

- **Lesson L-2026-05-002** Hyperspace audit cycle (3 anti-pattern + 4 pattern positive)
- **Lesson L-2026-05-003** Cross-repo pattern adoption (cross-check governance interna)
- **ADR-0025** Hyperspace privacy assessment NO-GO empirico (caso studio recovery error)
- **Memory** `feedback_governance_refresh_verify` (Protocol 1 prescription)
- **Memory** `feedback_autoresearch_default` (Protocol 2 8-step checklist)
- **Memory** `reference_archon_protocol` (Protocol 3 7-step, created 2026-05-12)
- **Memory** `project_aa01_studio` (Protocol 4 workflow standard)
- **AA01 task** aa01-001 fleet-discovery-pod-design (22 decisions D-001 to D-022, caso studio Archon applied)

## Notes

### Ratification

Status **Proposed**. Eduardo decide accept/reject/modify.

### Reactivation triggers (per ADR addendum future)

- Protocol evolution (es. nuovo workflow tool consolidate)
- Lesson learnt new caso studio (es. Archon over-engineered in scenario X → anti-pattern explicit)
- AA01 → Codex Cloud / OpenCode integration (se non più Eduardo-only)

### Non-negotiable

- Triple anchor preservato (ADR + memory + CLAUDE.md sempre allineati)
- Cherry-pick policy: NO clone Archon docs in codemasterdd
- AA01 path personale (Eduardo-only), NON portable
- Lesson L-2026-05-002 + L-2026-05-003 cited + accessibili per future session
