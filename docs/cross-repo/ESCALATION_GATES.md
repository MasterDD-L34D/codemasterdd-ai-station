# Cross-repo escalation gates (Component 3)

> Spec ref: `docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md` V3 Opt 1.5 REDUCED PR #87.
>
> Anti-L-016 discipline: weekly Gate E logging via `scripts/cross-repo/coord-event-log.ps1` + harsh-reviewer subagent week-4 audit.

## Purpose

Criteri **pre-definiti** per evoluzione paradigm cross-repo SE failure trigger empirico emerge. Tracking discipline previene drift "intent to log -> abandoned" (anti-pattern L-2026-05-016).

## Gates definizione

### Gate E (PRE-Component-1 build)

**Purpose**: validate trigger #1 visibility gap empirically post-Max prima di commit Component 1 build effort.

**Empirical window**: 30 giorni post-Claude Max expiration (5/20 -> 6/19).

**Measurement**:
- Eduardo logs coord-event ogni volta che ha "missed-coordination event":
  - grep manuale cross-repo >3 location per state lookup, OR
  - cross-repo policy drift discovered DOPO causing rework >30min, OR
  - two-way communication cross-repo per decision singola che richiede >2 round trip
- Log file: `logs/coord-events-YYYY-MM.md`
- Helper script: `scripts/cross-repo/coord-event-log.ps1` (interactive prompts)
- Weekly reminder: schtasks Sunday 09:00 (installed via `install-gate-e-reminder.ps1`)

**Thresholds** (after 4 weeks consecutive measurement):

| Avg events/week | Decision | Component 1 scope |
|-----------------|----------|-------------------|
| >=5/wk | BUILD justified empirical | Full scope (extension dogfood-ui OR standalone, alternative A vs B decision) |
| 2-4.99/wk | BUILD MINIMAL | Extension dogfood-ui ONLY (drop standalone alternative + reduce SPRINT_02 T1-T2 scope) |
| <2/wk | NOT BUILT | Trigger #1 falsified empirical, defer indefinitely. Update STATUS_MULTI_REPO + close spec V3 |

**Threshold revisability**: post 1-week pilot, threshold revisable se events tipicamente cluster (1 day = revise weekly threshold) vs scattered (mantain). Document revision in `docs/cross-repo/ESCALATION_GATES.md` amendment + JOURNAL entry.

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

- Gate E precedes ALL altri (until Gate E resolved, Component 1 NOT built)
- Gate A + Gate B mutually exclusive (Opt 3 OR Opt 4 escalation, NOT both)
- Gate C independent (bandwidth event, doesn't trigger Opt 3/4)
- Gate D Component-2-specific (independent of Component 1 build)

## Reading the gates

This document is checkpoint, NOT prescription. Gate trigger does NOT mean automatic execution -- it means **re-open the decision** with empirical data. Decision belongs to Eduardo + governance interna repo target (Gate A) or strategic context (Gate B/C).
