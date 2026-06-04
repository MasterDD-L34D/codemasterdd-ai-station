# SPRINT_02 weekly cadence DELTA — T8/T9/T10 + Gate E + Week 4 audit

> **DELTA — NOT REPLACEMENT.** This plan AMENDS the T8/T9/T10 sub-task breakdown in `SPRINT_02.md` with weekly cadence + Gate E logging integration + Week 4 harsh-reviewer audit. `SPRINT_02.md` rimane AUTORITATIVO per T1/T2/T5/T7 (no duplication here).

> **For agentic workers post-Max**: REQUIRED SUB-SKILL: superpowers:subagent-driven-development OR superpowers:executing-plans. Use checkbox tracking.

**Goal:** Execute SPRINT_02 4-week window (2026-05-20 → 2026-06-19) integrating Gate E logging discipline + Week 4 audit + weekly cadence for SPRINT_02.md sub-tasks T8.1-T8.3 / T9.1-T9.3 / T10.1-T10.3.

**Architecture:** Weekly cadence with concrete weekly checkpoints. Gate E (Component 1 build trigger from spec V3 cross-repo orchestrator) overlaps SPRINT_02 timeline = combined workflow.

**Scope EXPLICITLY NOT IN THIS PLAN** (see SPRINT_02.md as authoritative):
- T1 smoke wrapper sovereign — DONE 13/5
- T2 dogfood organico — SPRINT_02.md target soft n≥20 cumulative (current n=36 superato)
- T5 cost tracking — SPRINT_02.md GATED ~2026-06-15 end-of-month wait
- T6 privacy validation Synesthesia — SPRINT_02.md OPPORTUNISTIC default skip
- T7 review fine sprint — SPRINT_02.md ~2026-06-19 sessione 30-45min

**Effort estimate REVISED** (post P1.1 harsh-review fix): **~1-2h/wk Eduardo direct** + ~3-5h cumulative W4 audit + decision. Original v1 claim "30min/wk" was 3-5x underestimate.

**Confidence:** 60% (plan structurally honest post-rework; depends on logging discipline + Gate E threshold realism).

---

## Pre-flight (pre-5/20)

- [ ] **P.1: Verify Component 2+3 deployed** (post-merge state)

Run: `git -C C:/dev/codemasterdd-ai-station log --oneline | grep "cross-repo orchestrator"` — expected commit `3e580e2`

- [ ] **P.2: Verify cross-repo-pr-whitelist.txt installed**

Run: `cat C:/Users/edusc/.config/cross-repo-pr-whitelist.txt | grep -v "^#" | grep -v "^$" | wc -l` → expected 4

- [ ] **P.3: Verify OR install schtask GateELoggingReminder**

Run:
```powershell
if (-not (schtasks /Query /TN GateELoggingReminder 2>&1 | Select-String "Pronta")) {
  Write-Host "Installing schtask..."; powershell -File C:/dev/codemasterdd-ai-station/scripts/cross-repo/install-gate-e-reminder.ps1
}
schtasks /Query /TN GateELoggingReminder
```
**P1.6 fix**: install if missing (NOT just verify-and-fail).

- [ ] **P.4: Update STATUS_MULTI_REPO.md** with Sprint state

Add row: "SPRINT_02 ACTIVE 2026-05-20 (week 1/4 of 4)"

- [ ] **P.5: Reset coord-events log for fresh window**

If `logs/coord-events-2026-05.md` has pre-window entries → rename to `logs/coord-events-2026-05-pre-window.md`. Create fresh log via first invocation `coord-event-log.ps1`.

---

## Weekly cadence (4 weeks)

### Pattern (applies W1/W2/W3/W4)

Ogni domenica (per matching schtask trigger Sun 09:00):
1. Invoke `coord-event-log.ps1` interactive mode 1× (logs past-week events) — ~10min
2. Update `logs/escalation-gates-2026-05.md` week-row counter — ~5min
3. T8 plugin observation (see SPRINT_02.md T8.1/T8.2/T8.3 sub-tasks) — opportunistic ~10-20min if active week
4. T9 cite count refresh (vedi sub-task sotto W1.cite_count step) — ~5min
5. T5 cost tracking light snapshot (NOT replacing SPRINT_02.md T5 end-of-month) — ~5min

**Realistic time/wk Eduardo direct: ~1-2h cumulative active weeks** (P1.1 fix).

### Week 1 (5/20 → 5/26) — Baseline establishment

T9.1 sub-task NEW: **Baseline cite count pre-Max snapshot** (one-shot W1 init)
```bash
for p in "Protocol 1" "Protocol 2" "Protocol 3" "Protocol 4" "Protocol 5" "Protocol 6"; do echo "$p: $(grep -c "$p" C:/dev/codemasterdd-ai-station/JOURNAL.md)"; done > logs/sprint-02-methodology-baseline-pre-max.txt
```

Create tracking table `logs/methodology-cite-count-tracking-2026-MM.md`:
```markdown
| Week | P1 | P2 | P3 | P4 | P5 | P6 | Total | Notes |
|------|----|----|----|----|----|----|-------|-------|
| pre-Max baseline (5/19) | X | X | X | X | X | X | X | Snapshot |
| W1 (5/26) | | | | | | | | |
```

Gate E.W1: first weekly logging session 5/24 Sun. Verify schtask reminder file marker created `logs/gate-e-reminder-due-2026-W21.md` (Week 21 = 5/18-5/24).

If marker NOT created → **P0 regression** (P0.2 PR #87 fix broken). Re-run install schtask + smoke test.

### Week 2 (5/27 → 6/2)

T8.W2: claude-mem search effectiveness — see SPRINT_02.md T8.1 sub-task. Plus weekly observation log:
```markdown
| Date | Query | Result quality (1-5) | Time saved | Notes |
```
Target: ≥3 queries quality≥3 = operational.

Gate E.W2: Sunday 5/31 logging session + counter update.

### Week 3 (6/3 → 6/9) — Three Strikes Quality Gate audit

T10.W3: assess Three Strikes per **ADR-0028 verbatim wording** (P0.3 fix):

- Strike 1: **1 regress reale tier promotion ad-hoc** (es. promosso modello in routing senza Quality Gate review, regresso operativo emerso)
- Strike 2: **1 successful manual Quality Gate application** (3-step seguito su tier candidate + outcome positive empirico). NOTA: 3-step = Smoke + Research + Tuning fixture run.
- Strike 3: **1 emergent tier promote request** (new model rotation OR wrapper variant request from agent during normale use)

Audit step:
```bash
# Strike 2 source-of-truth: scan docs/research/ for 3-step Quality Gate fixture
grep -l "Smoke\|Research\|Tuning" C:/dev/codemasterdd-ai-station/docs/research/*.md | xargs grep -l "tier candidate\|tier promotion"

# Strike 1 source-of-truth: scan SPRINT_02 dogfood log + JOURNAL for "regress" + "ad-hoc tier"
grep "regress\|ad-hoc" C:/dev/codemasterdd-ai-station/logs/aider-delegation-2026-05.md C:/dev/codemasterdd-ai-station/logs/aider-delegation-2026-06.md C:/dev/codemasterdd-ai-station/JOURNAL.md 2>&1
```

Document audit result `logs/sprint-02-three-strikes-audit-W3.md`:
```markdown
- Strike 1 (regress tier promotion ad-hoc): YES/NO + cita evidence file:line
- Strike 2 (successful manual Quality Gate 3-step application): YES/NO + cita evidence
- Strike 3 (emergent tier promote request): YES/NO + cita evidence
- Status: <FIRE all 3 / partial 1-2 / 0 strikes>
```

If FIRE → activate ADR-0028 Accepted ratification + MODEL_ROUTING.md section formal write per V3 REC 2.

### Week 4 (6/10 → 6/16) — Gate E decision + harsh-reviewer audit

#### Gate E.W4 prep (Sun 6/14)

Final week logging session. Aggregate 4-week count:
```bash
grep "^| 2026-0[5-6]" C:/dev/codemasterdd-ai-station/logs/coord-events-2026-05.md C:/dev/codemasterdd-ai-station/logs/coord-events-2026-06.md 2>/dev/null | wc -l
```

Calculate avg events/week. Update `logs/escalation-gates-2026-05.md` cumulative summary.

#### Week 4 harsh-reviewer audit (Protocol 5 ADR-0026)

**Critical instruction**: when invoking harsh-reviewer, **explicitly exclude** `docs/research/component-1-design-options-archived-2026-05-13.md` from reading list. That file is intentionally archived as bias-mitigation per L-2026-05-018.

Dispatch prompt template:

```
Harsh review boundary read-only on Gate E logging discipline 4-week empirical (SPRINT_02 W1-W4).

Files to read:
- C:/dev/codemasterdd-ai-station/logs/coord-events-2026-05.md
- C:/dev/codemasterdd-ai-station/logs/coord-events-2026-06.md
- C:/dev/codemasterdd-ai-station/logs/escalation-gates-2026-05.md
- C:/dev/codemasterdd-ai-station/JOURNAL.md (entries dated 2026-05-20 to 2026-06-16)

EXPLICITLY DO NOT READ:
- C:/dev/codemasterdd-ai-station/docs/research/component-1-design-options-archived-*.md
  (Pre-design archived per L-2026-05-018 anti-pattern bias mitigation)

Check for:
1. Logging discipline consistency: 4/4 weekly sessions present, no gap weeks?
2. Severity tag distribution sanity: NOT all =1 (under-reporting) OR all =5 (panic)?
3. Cost minutes documentation present: NOT all = 0?
4. Aggregate count plausibility: cross-check JOURNAL entries same week
5. Anti-pattern L-016 detection: did Eduardo skip logging weeks claiming "log later"?
6. **Contamination check**: any evidence Eduardo consulted archived pre-design during 4-week window? Search `git log` or JOURNAL entries.

Output P0/P1/P2 findings + Gate E threshold decision recommendation BASED ON LOGGED DATA ONLY (not on archived pre-design content).

Boundary: read-only, no Write/Edit, only Read/Grep/Glob.
Cost target: ~$0.30 (~85K tokens), under ADR-0023 cap.
HARD STOP if cost >$1, abort and summarize manually.
```

#### Gate E decision finalize

Decision matrix per spec V3 ESCALATION_GATES.md (mutual exclusive post Codex P2 fix):

| Avg events/wk × 4 wk | Threshold | Component 1 decision |
|----------------------|-----------|---------------------|
| ≥5 | PASS | Build Component 1 full scope. **Then** (NOT before) consult `docs/research/component-1-design-options-archived-2026-05-13.md` for Alt A vs B matrix input. Eduardo decides Alt A vs B. Note: Alt A revised cost 3.5-4w (P1.5 fix incl. dogfood-ui promotion prereq); Alt B 2.5w. |
| 2-<5 | PARTIAL | Build Component 1 MINIMAL scope. Alt A reduced OR Alt B minimal. |
| <2 | FALSIFIED | DEFER indefinitely. Archive Alt A vs B research (already archived). Update STATUS_MULTI_REPO trigger #1 empirically falsified. Close spec V3 follow-up. |

Document decision `logs/sprint-02-gate-e-decision-2026-06-15.md`.

#### T9 final methodology cite count + ADR-0026 n≥3 threshold check

```bash
for p in "Protocol 1" "Protocol 2" "Protocol 3" "Protocol 4" "Protocol 5" "Protocol 6"; do echo "$p: $(grep -c "$p" C:/dev/codemasterdd-ai-station/JOURNAL.md)"; done > logs/sprint-02-methodology-final-2026-06-15.txt
```

Compare baseline vs final:
```markdown
| Protocol | Baseline pre-Max | Post-Max W4 | Delta | n≥3 instances reached? | Decision |
|----------|-------------------|--------------|-------|------------------------|----------|
| P5 harsh-reviewer | ? | ? | ? | ? | maintain / formalize / downgrade |
| P6 brainstorming | ? | ? | ? | ? | maintain / formalize / downgrade |
```

**P2.3 fix awareness**: L-016 concluded P5 = **n=2 LEGITIMATE** (NOT 3 — inflated original claim). Reality check before counting future invocations.

---

## Self-review checklist (post P0+P1 fixes)

**Spec coverage** (delta only):
- T8 weekly cadence: W1-W4 pattern + observation log ✓ (sub-tasks T8.1/T8.2/T8.3 see SPRINT_02.md)
- T9 cite count + n≥3 check: W1 baseline + W2/W3 tracking + W4 final ✓
- T10 Three Strikes: W3 audit per ADR-0028 verbatim ✓ (P0.3 fix)
- Gate E logging discipline: W1-W4 weekly + W4 audit ✓
- Harsh-reviewer audit + archive exclusion: W4 prompt template ✓ (P0.1 mitigation)
- Component 1 decision matrix: W4 post-Gate-E with archived-doc reference deferred ✓

**SPRINT_02.md duplication eliminated** (P0.2 fix):
- T1/T2/T5/T7 explicitly NOT covered here ✓
- T8.1/T8.2/T8.3 ref SPRINT_02.md authoritative, only weekly cadence wrapping ✓
- T9.1/T9.2/T9.3 ref SPRINT_02.md, only cite count tracking detail added ✓
- T10 Three Strikes wording verbatim ADR-0028 ✓ (P0.3)

**Placeholder scan**: zero TBD / TODO / "fill in" — all concrete commands + files ✓

**Type consistency**:
- Log file paths: `logs/coord-events-*.md` + `logs/escalation-gates-*.md` + `logs/sprint-02-*.md` consistent
- Date format ISO 8601 consistent
- Threshold ≥5 / 2-<5 / <2 mutual exclusive (post Codex P2 PR #87 fix)
- ADR-0028 Three Strikes wording verbatim ✓

**Effort realism** (P1.1 fix): 1-2h/wk Eduardo + 3-5h W4 cumulative = ~7-13h total ✓

**P1.6 schtask handling**: P.3 now install-if-missing (not verify-and-fail) ✓

---

## References

- `SPRINT_02.md` (AUTHORITATIVE for T1/T2/T5/T7 + T8/T9/T10 main sub-tasks)
- `docs/governance/ESCALATION_GATES.md` (Gate E threshold definition AUTHORITATIVE)
- `docs/research/component-1-design-options-archived-2026-05-13.md` (Alt A vs B research, DO NOT CONSULT pre-Gate-E)
- `docs/adr/0028-tier-promotion-quality-gate-methodology.md` (Three Strikes wording AUTHORITATIVE)
- ADR-0023 H7 ANTHROPIC tier 0 strategic (audit cost cap)
- ADR-0026 cognitive workflow protocols (P1-P6)
- L-2026-05-016 anti-aspirational measurement (warning source)
- L-2026-05-018 (in promotion) META anti-pattern recurrence same-session
