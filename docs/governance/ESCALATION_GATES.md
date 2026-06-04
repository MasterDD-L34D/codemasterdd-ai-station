# Cross-repo escalation gates (Component 3)

> Spec ref: `docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md` V3 Opt 1.5 REDUCED PR #87.
>
> Anti-L-016 discipline: weekly Gate E logging via `scripts/cross-repo/coord-event-log.ps1` + harsh-reviewer subagent week-4 audit.

## Purpose

Criteri **pre-definiti** per evoluzione paradigm cross-repo SE failure trigger empirico emerge. Tracking discipline previene drift "intent to log -> abandoned" (anti-pattern L-2026-05-016).

## Gates definizione

### Gate E (Component 1 FEEDBACK METRIC -- reframe 2026-05-14)

> **REFRAME 2026-05-14 sera-tardi-ultra-2**: Gate E originally framed as "PRE-Component-1 build trigger" (gate before build). Component 1 dashboard MVP shipped 2026-05-14 commit `c2cb816` post Eduardo "userei ogni giorno anche ora" (L-019 trigger validation). Gate E counter is **NO LONGER A BUILD-BLOCKER** since Component 1 already exists.
>
> **NEW framing**: Gate E counter = **FEEDBACK METRIC** measuring how much pain Eduardo feels in coordination events. Informs:
> - Whether v0.3+ iteration priorities are right (high events / specific event type -> feature gap)
> - Whether dashboard adoption succeeds (low events post-build = success signal)
> - Whether Opt 3 (write-direct) or Opt 4 (mesh-bus) escalation is justified (Gate A / Gate B trigger)
>
> Reference: `docs/research/methodology-effectiveness-2026-05-14.md` Gate E reframe section.

**Purpose**: feedback metric for Component 1 adoption + Opt 3/Opt 4 escalation trigger.

**Empirical window**: 30 giorni post-Claude Max expiration (5/20 -> 6/19). Window unchanged.

**Measurement**:
- Eduardo logs coord-event ogni volta che ha "missed-coordination event":
  - grep manuale cross-repo >3 location per state lookup, OR
  - cross-repo policy drift discovered DOPO causing rework >30min, OR
  - two-way communication cross-repo per decision singola che richiede >2 round trip
- Log file: `logs/coord-events-YYYY-MM.md`
- Helper script: `scripts/cross-repo/coord-event-log.ps1` (interactive prompts)
- Weekly reminder: schtasks Sunday 09:00 (installed via `install-gate-e-reminder.ps1`)

**Thresholds REFRAMED** (post Component 1 MVP shipped 2026-05-14):

| Avg events/week | NEW interpretation | Action |
|-----------------|---------------------|--------|
| >=5/wk | **HIGH pain signal** -- Component 1 v0.2 insufficient OR specific feature gap | Iterate v0.3+ urgent based on event type breakdown; Gate A re-evaluate Opt 3 |
| 2-4.99/wk | **MODERATE pain** -- Component 1 v0.2 mostly OK, minor gaps | Iterate v0.3+ on identified gaps opportunistic |
| <2/wk | **LOW pain** -- Component 1 v0.2 adoption successful | Continue v0.2 stable, defer v0.3 iteration unless other trigger emerges |

**Threshold revisability**: post 1-week pilot, threshold revisable se events tipicamente cluster (1 day = revise weekly threshold) vs scattered (mantain). Document revision in `docs/governance/ESCALATION_GATES.md` amendment + JOURNAL entry.

**Audit week 4**: invocare harsh-reviewer subagent (Protocol 5 ADR-0026 addendum) per verificare:
- Logging discipline consistency (no gap weeks)
- Severity tag distribution (NOT all = 1, NOT all = 5)
- Cost minutes documentation present
- Aggregate count plausibility vs JOURNAL entries cross-reference

Cost: ~$0.30-0.50 (~85K tokens). Sotto cap ADR-0023 $20/mese.

### Gate A (Opt 3 write-direct re-evaluation)

**Trigger**: >2 missed-coordination events/week x 4 weeks consecutive WITH severity >=3 (subjective severity tag 1-5, weighted toward "high impact, no work-around").

**Action**: re-evaluate Opt 3 (write-direct cross-repo). Requires ADR amendment cross-repo with governance interna consent of 3 target repos (Game / Godot-v2 / Dafne). Conway's law cost upfront.

### Gate B (Opt 4 mesh-bus re-evaluation)

**Trigger**: repo count >=7 (codemasterdd + Game + Godot-v2 + Dafne + vault + Synesthesia + >=1 NEW = 7+) OR client production work attivo (Eduardo lavoro contrattuale terzi su codemasterdd-tooled workflow).

**Action**: re-evaluate Opt 4 (Dafne swarm extension cross-repo). Setup ~4-8 weeks bootstrap.

### Gate C (Eduardo bandwidth degraded)

**Trigger**: Eduardo bandwidth coordinator <50% available (es. lavoro full-time esterno, healthcare event, family commitment). Qualitative self-report monthly in JOURNAL or COMPACT_CONTEXT.

**Action**: Opt 1.5 enhanced via Dafne specialist routing automatic. Move coord overhead to Dafne agents (existing 11 agent runtime).

### Gate D (Component 2 reversibility threshold)

**Trigger**: >=5 PR cumulative accepted by external governance WITH cross-reference adoption visible (target repo CLAUDE.md o AGENTS.md cita codemasterdd pattern).

**Action**: PAUSE Component 2 + audit lock-in scope cross-repo + ADR formale per ritiro coordinato OR continuation explicit. Soft lock-in converges Opt 1.5 cost toward Opt 3 cost asymmetric advantage lost.

## Tracking files

| File | Gate | Updated by | Refresh cadence |
|------|------|------------|-----------------|
| `logs/coord-events-YYYY-MM.md` | E | `coord-event-log.ps1` interactive | Each event (event-driven) |
| `logs/escalation-gates-YYYY-MM.md` | A/B/C/D | Eduardo manual + weekly | Weekly Sunday checkpoint |
| `logs/cross-repo-pr-YYYY-MM.md` | D | `dry-run-pr.ps1` reminder | Each PR open + outcome |

## Gates interaction

- Gate E continuous post-Component-1-MVP (feedback metric, NOT a build-blocker; informs v0.3+ iteration priority + Gate A re-evaluation input)
- Gate A + Gate B mutually exclusive (Opt 3 OR Opt 4 escalation, NOT both)
- Gate C independent (bandwidth event, doesn't trigger Opt 3/4)
- Gate D Component-2-specific (independent of Component 1 build)

## Reading the gates

This document is checkpoint, NOT prescription. Gate trigger does NOT mean automatic execution -- it means **re-open the decision** with empirical data. Decision belongs to Eduardo + governance interna repo target (Gate A) or strategic context (Gate B/C).
