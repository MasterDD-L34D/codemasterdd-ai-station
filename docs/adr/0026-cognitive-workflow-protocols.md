# ADR-0026 -- Cognitive workflow protocols (AA01 + autoresearch + Archon)

> *TL;DR: Formalize integration di 3 cognitive workflow protocols (AA01 + autoresearch + Archon) come **operating rules codemasterdd**, non solo memory feedback. Trigger phrases esplicit per ogni protocol + cross-link methodology lesson L-2026-05-002 + L-2026-05-003. Rationale: mio error 2026-05-11 sera (refresh-verify state interno MANCATO -> ADR-0025 CONDITIONAL GO erroneous) è caso studio gap integration governance permanent vs memory drift. Triple anchor (ADR + memory + CLAUDE.md) preserva methodology cross-session anche se memory non loaded.*

- **Status**: **Accepted** (2026-05-12 sera auto-ratified) -- soft-default ratification anticipata via Eduardo authorization "fai tutti i residual possibili in auto" + empirical support raccolto Bundle 2 reflexive audit
- **Data**: 2026-05-12 (originale + ratification stesso giorno)
- **Decisore**: Eduardo Scarpelli (final accept/reject)
- **Deciders**: solo-dev

## Ratification note (2026-05-12 sera auto)

Auto-ratified Proposed -> Accepted via Eduardo authorization "fai tutti i residual possibili in auto" 12/5 sera. Empirical support cumulative Bundle 2 reflexive audit (`docs/research/adr-0026-effectiveness-reflexive-audit-2026-05-12.md`):

- **Cite density empirical** JOURNAL post-formalize: Protocol 4 AA01 (73) >> Protocol 3 Archon (27) >> Protocol 2 Autoresearch (21) >> Protocol 1 Refresh-verify (14)
- **3 caso studi combined methodology HIGH outcome**:
  - Hyperspace ABANDONED (1+2+3+4 applicati, ADR-0025 amend + L-002)
  - M12 claude-mem INSTALL (1+2+3+4, L-009 PIVOT pattern)
  - Bundle 1 hygiene (1+4 partial, PR #63)
- **Reflexive validation questa stessa sessione**: Bundle 1 PRE-edit Protocol 1 applicato (4 evidence empirical raccolti) + Bundle 2 Protocol 4 AA01 capture + Bundle 3 Protocol 4 AA01 capture
- **L-2026-05-010 lesson promoted** Reflexive methodology audit pattern (7-step apply method to method + 7-step cross-pattern adoption deferred decision)
- **L-2026-05-011 lesson promoted** Applicative optimization audit pattern (7-step empirical smoke)

3 gap identified mitigation candidate (NON urgent, deferred):
- Gap 1 Protocol 1 visibility risk (low cite density)
- Gap 2 Combined methodology canonical example missing
- Gap 3 Protocol 2 vs Protocol 3 boundary fuzzy

Trigger addendum E3 future: post 2 settimane uso empirical + Three Strikes pattern emergent. Reversibility: Eduardo puo' revert via amend ADR (Status -> Proposed) se gap critico emerge.

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

**Source**: memory `feedback_autoresearch_default` (8-step checklist) + amendment 2026-05-15 sera (Step 0 API ground truth check from L-2026-05-025).

**Rule**: per audit / eval / research, multi-source parallel investigation con synthesis weighted (NON one-shot README). Per audit di scope / privacy / installation / deployment ("where/which/how-many"), Step 0 obbligatorio: verify API authoritative presence prima di heuristic proxy.

**9-step checklist (post 2026-05-15 amendment)**:

0. **Authoritative API check** (NEW -- L-2026-05-025 lesson). Per audit "where/which/how-many" (scope / privacy / installation / deployment), interrogare API REST/SDK del tool come ground truth primario. Heuristic proxy (branch pattern, log scraping, commit author) usato solo come cross-check o fallback. Documentare in audit body se API NON consultato e perche'. Case study trigger: 2026-05-15 Jules privacy audit (heuristic branch-pattern -> 1 repo, API REST `/v1alpha/sources` -> 15 repos = 93% underestimate).
1. README empirical (starting point, NON authoritative)
2. Release tag history + changelog dedicato (verify version drift)
3. Recent announcement (Twitter/blog/X feed)
4. WebSearch broader context
5. Sibling repos / org repos correlati
6. GitHub Discussions / issues recenti (real-world friction)
7. License + LICENSE file empirical (404 check)
8. Synthesis multi-source con weighting (recent > old, multiple corroborate > single signal, **internal > external**, **empirical > documentation**)

**Trigger**: ogni audit / eval / research significativa. **Step 0 trigger HIGH**: ogni audit di scope/privacy/installation scope (GitHub Apps, MCP servers, OAuth grants, multi-AI deployment).

**Anti-pattern**: one-shot README fetch + verdict confidente. **NEW anti-pattern**: heuristic-only audit di installation scope quando API exists + accessibile (es. `gh pr list --branch-pattern X` per audit "where is Jules installed?" senza chiamare `GET /v1alpha/sources`).

**Self-application validated 2026-05-15 sera**: lesson L-025 applicata 3 volte same-day (Jules privacy audit + frontend breaking-change audit + T2 dogfood-ui field desync audit). Pattern is recursive guard rail: when applying Protocol 2, verify if API ground truth exists for THE audit you're conducting (not just for the original lesson).

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
5. **Protocol 5 if cluster >=3 PR same day OR security/governance files modified** (harsh-reviewer external critic) -- addendum 2026-05-13
6. **Protocol 6 if ADR-class architectural decision generative** (brainstorming structured exploration) -- addendum 2026-05-13

Empirical trial breve è cross-cutting (NOT a separate protocol but enabler per Protocol 2+3+5 validation).

## Addendum 2026-05-13 -- Protocol 5 + Protocol 6 superpowers integration (Option C)

**Trigger session**: 2026-05-13 pomeriggio harsh-reviewer subagent invoked su PR #80+#81 cluster review consegnato 8 finding (3 P0 inclusa CWE-214 process arg list exposure NON identified by main agent) + brainstorming skill loaded per OpenRouter eval architectural decision.

**Empirical evidence valore consegnato (1 sessione, n=1 data point ma rivelatore)**:
- harsh-reviewer P0 #1 catch real security regression che main agent NON aveva identificato → security blocker prevented
- harsh-reviewer narrative correction "VIABLE 6/6" → reality "3/7 PASS default 43%" → onestà intellettuale recuperata
- brainstorming HARD-GATE 3-approaches structure ha forzato decision rigor (A/B/C tradeoff con recommendation) vs ad-hoc proposal
- Cost: ~85K tokens + 21 tool uses + 193s duration per harsh-reviewer invocation = ~$0.30-0.50 (acceptable per high-impact cluster)

**Decision Eduardo 2026-05-13 pomeriggio (4 options A/B/C/D presented)**: **Option C -- toolkit optional con trigger guidance documented**, NON mandatory enforcement. Rispetta principio lean honest execution + framework reference quando trigger emergono.

**Anti-aspirational risk acknowledged**: stesso pattern P2 autoresearch FIRST = aspirational n=2 reactive (L-014+L-015). MITIGATION: aggiungere log field "harsh-reviewer invoked? Y/N" + "brainstorming skill applied? Y/N" parallelo a autoresearch field per measurement empirical post-formalization.

#### Protocol 5 -- External-perspective harsh review via subagent (cluster scrutiny)

**Source**: superpowers harsh-reviewer subagent + AA01 sub-agent ecosystem ADR-0018.

**Rule**: per cluster PR >=3 same day touching shared scope OR file security/governance-critical (wrappers, keys, hooks, ACL, CLAUDE.md authoritative), spawn harsh-reviewer subagent PRE-merge per external-perspective scrutiny:
1. Spawn agent con scope esplicito: file paths + claim narrativa da verify + finding focus areas (security/architecture/methodology/operational)
2. Boundary read-only: agent NO write/edit/commit, solo report markdown
3. Finding format: priority P0/P1/P2 + descrizione + impact + recommendation + file references
4. Integrate findings PRE-merge: P0 obbligatorio fix prima merge, P1 either fix OR documented defer, P2 acknowledge
5. Log entry "harsh-reviewer invoked? Y/N" in cluster commit message OR PR body per measurement empirical

**Trigger STRONGLY recommended** (formally Accepted post 2026-05-14 amendment, see STATUS AMENDMENT below):
- Cluster >=3 PR same day con scope overlap OR consecutive
- File security/governance-critical modified (wrappers, keys, hooks, ACL, CLAUDE.md authoritative)
- Narrative claim "X/Y VIABLE/PASS" senza empirical decomposition default vs mitigation
- Pre-merge ADR-class decision con narrative implication

**Hard cap (ratified 2026-05-13 post harsh-reviewer #2 P1 #5 finding)**: **max 2 invocazioni harsh-reviewer per session**. ECCEZIONE solo per threshold counter Protocol 5 explicit (1st invocation legitimate + 2nd invocation legitimate validate threshold). 3rd invocation same-session = anti-pattern escalation paranoia, defer next session.

**Anti-pattern**: skip per cluster solo doc-only OR <2 PR (over-engineered overhead). Skip se task lean <30min (cost 85K tokens + 193s sproporzionato). **Anti-pattern: cluster-of-clusters infinity loop** (3rd+ invocation same-session = escalation, NOT quality gate).

**Cost**: ~$0.30-0.50 per invocazione (~85K tokens). Sotto budget cap $20/mese ADR-0023 anche con 1-2 cluster significativi/mese = $1/mese. Cumulative session cap = $1 (hard cap 2 invocations).

**Caso studio empirico (n=5+ instances LEGITIMATE cross-PR cross-session)**:
- 1st invocation: PR #80+#81 cluster review 2026-05-13 pomeriggio consegnato 8 finding actionable (3 P0 incluso CWE-214 catch real, 3 P1, 2 P2). Eduardo decisioni 4/4 trigger fix → PR #82 mergeato.
- 2nd invocation: cluster ULTRA-FINAL 8 PR review 2026-05-13 sera consegnato 7 finding META-LEVEL (3 P0 incluso reflexive cherry-picking + scope drift, 2 P1, 2 P2). Eduardo decisioni 4/4 trigger fix → PR consolidamento + STOP next 24h consigliato.
- 3rd invocation: PR #87 spec V3 ciclo 2 harsh-review post-Draft 2026-05-13 sera-tardi-ultra-3 consegnato 12 finding (3 P0 + 5/6 P1 + 3 P2). REWORK verdict triggered v1→v2 archive Component 1 (META anti-pattern L-016 mitigation).
- 4th invocation: PR #91 v0.2 post-build verification 2026-05-14 sera consegnato 18 finding (3 P0 security + 6 P1 + 3 P2). Triggered P0 security fixes 1b34055 + bias mitigation.
- 5th invocation: end-to-end verifica-con-metodo 2026-05-14 sera-tardi-ultra consegnato 4 P0 + 5 P1 + 12 acknowledge. Triggered lessons L-018/019/020 promotion + JOURNAL update + P0 security fixes commit 1b34055.

### STATUS AMENDMENT 2026-05-14 sera-tardi-ultra-2

**Pre-amendment status**: Option C non-mandatory (PR #82 + #84 introduced).
**Post-amendment status**: **ACCEPTED ratified empirical** post-5-invocations cross-PR cross-session 12-14/5.

Threshold n>=3 LEGITIMATE met (per L-016 anti-cherry-picking criteria):
- Cross-session instances: YES (13/5 + 14/5 distinct sessions)
- Cross-scope different real use case: YES (PR cluster review, post-build security verify, end-to-end methodology audit, ADR-class spec review)
- Variability test PASS: trigger varies (cluster size, security scope, governance class), scope varies (PR #80+81 wrappers, PR #82 governance, PR #87 spec, PR #91 dashboard, end-to-end verify), outcome varies (8/7/12/18/21 findings)

**Action concrete**:
- P5 status formally **Accepted**
- Hard cap revised: 2x per session retained (anti-paranoia escalation), but session count not capped (1-2 per session × multiple sessions/week OK)
- Trigger criteria unchanged (cluster >=3 PR OR governance-critical files OR ADR-class decision)

### Reference

Agent definition `~/.claude/agents/harsh-reviewer.md` (codemasterdd .claude/agents/) + ADR-0018 agent readiness protocol.

Effectiveness research doc: `docs/research/methodology-effectiveness-2026-05-14.md`.

#### Protocol 6 -- Brainstorming structured exploration via skill (architectural design)

**Source**: superpowers `brainstorming` skill (`~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/brainstorming/`).

**Rule**: per ADR-class architectural decision generative (new sub-system / replace existing component / strategic platform choice / governance protocol introduction), invoke brainstorming skill flow:
1. Explore project context (files, recent commits, ADR existing)
2. Skip "visual companion" se NON visual question
3. Clarifying questions one-at-a-time (skip se auto-mode + Eduardo authorization explicit)
4. Propose 2-3 approaches con tradeoff esplicito + recommendation + reasoning
5. Present design sections scaled to complexity (ask approval per section)
6. Write spec doc OR direct ADR scaffold se decision è formal
7. Only AFTER approval: invoke implementation skill chain

**Trigger STRONGLY recommended** (NON mandatory enforcement Option C):
- ADR-class decision architectural irreversibile o significativamente costoso reverse
- Replace existing component / pattern / wrapper / tooling
- Strategic platform choice (es. OpenRouter eval, framework adoption)
- Governance protocol introduction o major modification

**Anti-pattern**:
- Apply HARD-GATE per task advisory/review (Eduardo "voglio vedere che ci dicono" NON è new feature)
- Apply per task lean <30min implementation (overhead sproporzionato)
- Sequential clarifying questions in auto-mode (confligge con no-questions instruction)

**Cost**: token consumption marginale (skill è locally loaded, inferenza standard). Process overhead ~5-10min strutturazione 3-approach + design sections.

**Caso studio empirico**: brainstorming skill loaded 2026-05-13 pomeriggio per OpenRouter eval architectural decision. HARD-GATE adattato per advisory context (Eduardo decisione invece di formal spec → user-direct). Output: 4 options A/B/C/D considered + Option C chosen + ADR-0029 scaffold.

**Complementarity con Protocol 3 Archon**:
- P3 Archon = analytic decompose (RESTATE + ENUMERATE + DECOMPOSE + CHALLENGE + RECONSTRUCT + RED-TEAM + CALIBRATE) per high-stakes verifica empirical
- P6 brainstorming = generative design (explore → questions → 3 approaches → design → spec) per design-thinking phase pre-Archon
- Use case combined: brainstorming PRIMA per generate options + Archon DOPO per stress-test + falsifying experiment

**Reference**: superpowers skill definition path sopra + `feedback_external_material_triage` selective adoption pattern.

### Combined methodology UPDATED 2026-05-13 (post Protocol 5 + 6 addendum)

```
[Trigger: audit / eval / decision significativa]
        ↓
Protocol 1: Refresh-verify state interno (OBBLIGATORIO)
        ↓
[Architectural design generative? new sub-system / replace component / strategic choice]
        ├── SI → Protocol 6: brainstorming skill (3 approaches con tradeoff)
        |
[Cluster >=3 PR same day OR file security/governance-critical?]
        ├── SI → Protocol 5: harsh-reviewer subagent PRE-merge
        |          ↓
        |       Findings P0/P1/P2 → integrate pre-commit
        ↓
Protocol 4: AA01 workspace audit trail (start, se >=30min effort)
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

### Measurement empirical post-formalization (anti-aspirational mitigation)

Per evitare protocols 5+6 diventino aspirational reactive (stesso pattern P2 autoresearch FIRST n=2 reactive caso L-014+L-015):

- **Log field aggiunto** `harsh-reviewer invoked? Y/N` (Protocol 5 application)
- **Log field aggiunto** `brainstorming skill applied? Y/N` (Protocol 6 application)
- **Field tracking location**: PR body section "Cognitive protocols applied" OR commit message footer
- **Threshold review**: ogni 3 mesi (~SPRINT_03/04 boundary) → check field empirical adoption rate. Se <30% trigger application su qualifying tasks → ADR-0026 amendment B (declassify mandatory) o C (re-evaluate trigger conditions).

**Trigger Accepted Protocol 5+6**: n>=2 instances application su qualifying trigger conditions con valore empirical documented (es. P0 catch / narrative correction / 3-approach decision rigor).

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

---

## Addendum 2026-05-12 -- AA01 conditional fit assessment

Eduardo (2026-05-12) ha sollevato introspection question post ADR merge: "AA01 è davvero definitivamente parte di codemasterdd?". Applied Protocol 3 Archon 7-step self-assessment (caso studio meta-application).

### Verdict honest post Archon 7-step

**AA01 è CONDITIONAL permanent fit, NOT clean permanent integration.**

ADR-0026 original ha implicitly assumed permanent integration. Honest re-assessment: integration è **conditional**, non strict permanent.

### 4 Conditions per "permanent fit" status

| # | Condition | Verifiable empirico |
|---|-----------|---------------------|
| C1 | Eduardo continues personal workflow | AA01 NON automatable, dipende su personal discipline |
| C2 | AA01 path stability | `C:/Users/edusc/aa01/` location persists (cross-device fragile) |
| C3 | Use case frequency >=1-2 task/settimana | Lessons cumulative growth rate |
| C4 | CLAUDE.md section Cognitive workflow NON drifta | Section "Cognitive workflow protocols" present + memory `project_aa01_studio` not-stale |

### 5 Failure modes (RED-TEAM)

1. **Cambio computer Eduardo** senza AA01 transfer → reference broken
2. **AA01 dormante 30gg+** → drift, lessons fresh non scritte
3. **CLAUDE.md drift**: sessioni future rimuovono section Cognitive → Protocol 4 invisible
4. **Ridondanza vs git**: lesson potrebbe stare direct in `docs/lessons/` codemasterdd → AA01 archive overhead
5. **Memory drift**: `project_aa01_studio` non aggiornata → references invalidate

### Indicatori early-warning

- `bash scripts/status.sh` non-run 7gg+ → segno disuso
- Memory `project_aa01_studio` non-updated 30gg+ → drift starting
- ADR future NON citano AA01 task → de-coupling de facto
- Lesson cumulative <5 in 90gg → insufficient value capture

### Falsifying experiment economico (~30min)

**Trigger**: 30-day review checkpoint **2026-06-12** (e poi quarterly):

1. `cd C:/Users/edusc/aa01 && bash scripts/status.sh` check (1 min)
2. Memory `project_aa01_studio` last-updated date (30s)
3. CLAUDE.md grep "Cognitive workflow protocols" present (30s)
4. Lessons cumulative count vs 30gg ago (1 min)
5. Lesson L-2026-05-004+ candidate emerged? (depends)

**Pass criteria**: tutto green + >=1 lesson cumulative growth/mese.
**Fail criteria**: any rosso → reactivation evaluation o downgrade decision.

### Reactivation NO-GO triggers

Se durante checkpoint emerge:
- Cambio computer without AA01 transfer
- 60gg+ AA01 dormante (no activity)
- <5 lessons cumulative in 90gg

→ ADR-0026 downgrade Protocol 4 da "workflow standard" a "optional discipline".

### Honest re-framing post-assessment

Originale ADR-0026: "AA01 è workflow standard" (implicit permanent)
Re-framing: "AA01 è **conditional workflow standard** con 4 conditions + 30-day review checkpoint"

CLAUDE.md section Cognitive workflow protocols NON cambia (resta authoritative reference) ma ADR governance riflette honest caveat conditional.

### Empirical value preserved (ultimi 30gg)

- 22 decisions aa01-001 PRESERVED cross-session (Hyperspace audit 4-cycle)
- 3 lessons consolidate (L-2026-04-001 + L-2026-05-002 + L-2026-05-003)
- ~5h re-work prevented post mio error 2026-05-11
- Process honesty pattern catturato (recovery via amend transparency)

Value reale > zero. Conditional fit ha sense pragmatic.

### Lesson L-2026-05-004 derived

Meta-lesson "AA01 conditional fit assessment via Archon 7-step self-application":
- Pattern positive: Archon protocol può applicarsi a meta-introspection (governance Protocol stesso applied a Protocol)
- Pattern positive: honest conditional verdict > permissive permanent claim
- Pattern positive: 30-day review checkpoint > one-shot ADR + drift

Vedi `C:/Users/edusc/aa01/learnings/L-2026-05-004-aa01-conditional-fit-meta-assessment.md`.

---

## Addendum 2026-05-12 (E2 review enhancement) -- Protocol 3 Archon conditional fit (symmetric Protocol 4)

Review 4-angoli post-addendum AA01 ha identificato **asimmetria logica**: Protocol 4 AA01 dichiarato CONDITIONAL fit MA Protocol 3 Archon implicitly permanent. Entrambi sono personal workflow Eduardo-tied + filesystem-tied + non-automatable.

Applichiamo conditional fit assessment symmetric a Protocol 3 Archon per coerenza.

### Verdict honest Protocol 3 Archon

**Archon è CONDITIONAL fit symmetric Protocol 4 AA01**, MA con frequency profile diverso:
- AA01 = high-frequency (1-2 task/settimana, ogni audit/eval/research >=30min)
- Archon = low-frequency (>=1 high-stakes decision/mese, irreversibile o cost-recovery >2h se errata)

Value-per-invocation Archon > AA01, MA discipline-fragility maggiore (less practice = more drift risk).

### 4 Conditions Archon (mirror Protocol 4 AA01)

| # | Condition Archon | Mirror Protocol 4 | Verifiable empirico |
|---|------------------|---------------------|---------------------|
| ArC1 | Eduardo continues personal Archon invocation | C1 AA01 personal workflow | NON automatable, depends su personal discipline |
| ArC2 | Archon path `C:/Users/edusc/aa01/archon/system/` stability | C2 AA01 path stability | Subset of AA01 path -- IF AA01 lost THEN Archon lost (linked SPOF) |
| ArC3 | Use case frequency >=1 high-stakes decision/mese applied | C3 use case frequency | Lessons cite "Archon 7-step" / "RESTATE" / "CALIBRATE" |
| ArC4 | ADR-0026 + memory `reference_archon_protocol` NON drifta | C4 CLAUDE.md section NON drifta | Memory last-updated date + ADR cited |

### 5 Failure modes Archon (RED-TEAM mirror)

1. **AA01 path lost** → Archon path lost (linked SPOF, ArC2 fail trigger ArC4 cascade)
2. **Archon mai invocato 60gg+** → discipline drift, lessons future NON applicano 7-step
3. **"High-stakes decision" trigger mai attivato 90gg+** → Eduardo workflow NON ha decisioni irreversibili = over-engineering complaint risk
4. **Memory `reference_archon_protocol` not-updated 60gg+** → drift, trigger phrases obsolete
5. **Lesson methodology references Archon SOLO da L-2026-05-002 (originale)** → no cumulative empirical backing, single-source bias

### Indicatori early-warning Archon

- Lessons cumulative NON cite "Archon 7-step" / "RESTATE" / "CALIBRATE" / "RED-TEAM" → segno non applicato
- Memory `reference_archon_protocol` last-updated 60gg+ → drift starting
- ADR future high-stakes (architectural / pivot) NON applicano Archon → de-coupling de facto
- Decision audit log AA01 task NON cita Archon 7-step references → workflow drift

### Falsifying experiment economico Archon (~15min, checkpoint 30-day 2026-06-12 stesso AA01)

1. Memory `reference_archon_protocol` last-updated date (30s)
2. Grep recente lessons (90gg) per "Archon 7-step" / "RESTATE" / "CALIBRATE" / "RED-TEAM" (2 min)
3. Count high-stakes decisions in archive 90gg che hanno applicato Archon vs decisioni che dovevano (10 min review)
4. Lesson L-2026-05-005+ candidate che riferisce Archon? (depends)

**Pass criteria**: memory <60gg + >=1 lesson cita Archon 90gg + >=1 high-stakes decision con Archon applied 90gg.
**Fail criteria**: any rosso → Protocol 3 downgrade a "optional methodology reference" (NON workflow standard).

### Reactivation NO-GO triggers Archon

- AA01 path lost (linked SPOF)
- Archon NON invocato 90gg+ in lessons
- Eduardo dichiara explicitly "over-engineered, drop Archon"
- High-stakes decisions count >=3 in 90gg che NON hanno applicato Archon

→ ADR-0026 downgrade Protocol 3 da "high-stakes decision workflow" a "optional methodology reference".

### Honest re-framing post-symmetric

Originale ADR-0026: Protocol 3 Archon implicit permanent
Symmetric (post E2): "Protocol 3 Archon = **conditional methodology** con 4 ArC conditions + linked SPOF AA01 + 30-day review checkpoint 2026-06-12"

### Confidence Archon conditional fit: 70%

5% riserva sotto AA01 (75%) perché:
- Use case meno frequent → discipline più fragile
- Value-per-invocation maggiore MA invocation più rara
- Linked SPOF AA01 path → riserva ereditata

### Empirical value preserved Archon (ultimi 30gg)

- Applied 2x in aa01-001 fleet-discovery (D-011 + D-015) cycle audit Hyperspace
- Caso study L-2026-05-002 Pattern positive 3 ("Archon 7-step First Principles per high-stakes")
- Meta-application L-2026-05-004 (Archon to assess Protocol 4 AA01)
- Decision quality empirical: D-011 pivot exo erroneous (Windows non supported falsified) mostrato Pattern positive 4 "falsifying experiment economic check" → Archon ha permesso CONVERGENCE finale a D-017 NO-GO empirico

Value reale > zero. Conditional fit symmetric ha sense pragmatic.

### Combined methodology lock-in awareness

L-2026-05-004 ha catturato **lock-in personal workflow Eduardo** come pattern. Applicato a Protocol 3 Archon symmetric, esplicita:

- Tutto stack cognitive (AA01 + Archon + autoresearch + vault) è personal-tied Eduardo
- Solo Protocol 1 Refresh-verify + Protocol 2 Autoresearch sono governance-portable (NO filesystem AA01 dependency)
- Protocol 3 Archon + Protocol 4 AA01 = personal discipline stack

**Honest implication**: se Eduardo life-change (cross-device / browser-only / browser Projects + Claude), 50% del cognitive workflow ADR-0026 invalidato.

**Mitigation pattern documented**: 30-day checkpoint 2026-06-12 monitora entrambi simultaneously.
