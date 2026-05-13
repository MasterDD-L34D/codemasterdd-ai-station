# SPRINT_02 detailed plan — T8/T9/T10 + Gate E integration (pre-Max preparation)

> **For agentic workers post-Max**: REQUIRED SUB-SKILL: superpowers:subagent-driven-development OR superpowers:executing-plans. Use checkbox tracking.

**Goal:** Execute SPRINT_02 4-week window (2026-05-20 → 2026-06-19) integrating T8 plugin ecosystem dogfood + T9 methodology framework effectiveness + T10 Three Strikes Quality Gate + Gate E logging discipline + Week 4 audit.

**Architecture:** Weekly cadence with concrete deliverables. Gate E (Component 1 trigger) overlaps SPRINT_02 timeline = combined workflow.

**Tech Stack:** PowerShell scripts esistenti (`coord-event-log.ps1` for Gate E) + JOURNAL entries weekly + harsh-reviewer subagent week 4 + ccusage cost tracking.

**Spec/SPRINT references:**
- [SPRINT_02.md](../../SPRINT_02.md) — task headlines + Eduardo override notes
- [docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md](../specs/2026-05-13-cross-repo-orchestrator-design.md) — Component 3 Gate E spec
- [docs/superpowers/specs/2026-05-13-component-1-dashboard-design.md](../specs/2026-05-13-component-1-dashboard-design.md) — Component 1 pre-design (Gate E result-dependent)

**Effort estimate:** 4 weeks elapsed (calendar) + ~30min/wk Eduardo direct (logging discipline) + ~3-5h cumulative concentrated (week 4 audit + decision).

**Confidence:** 60% (mid: SPRINT_02 base shipped already with ACTIVE override, this plan amends scope with deliverable specifics).

---

## Pre-flight (pre-5/20)

- [ ] **P.1: Verify Component 2+3 deployed** (post-merge state)

Run: `git -C C:/dev/codemasterdd-ai-station log --oneline | grep "cross-repo"` — expected commit `3e580e2 feat(cross-repo): orchestrator opt 1.5 reduced design + impl (#87)`

- [ ] **P.2: Verify cross-repo-pr-whitelist.txt installed**

Run: `cat C:/Users/edusc/.config/cross-repo-pr-whitelist.txt | grep -v "^#" | grep -v "^$" | wc -l`
Expected: 4 (Game / Game-Godot-v2 / Dafne / vault)

- [ ] **P.3: Verify schtask GateELoggingReminder installed**

Run: `schtasks /Query /TN GateELoggingReminder | findstr "Pronta"`
Expected: task ready, next run domenica successiva 09:00

- [ ] **P.4: Update STATUS_MULTI_REPO.md** with Sprint state

Add row in apps section: "SPRINT_02 ACTIVE 2026-05-20 (week 1/4)"

- [ ] **P.5: Reset coord-events log for fresh window**

Per Gate E spec V3: 30gg window starts 5/20. If `logs/coord-events-2026-05.md` has pre-window entries (test smoke from impl session), Eduardo manual: rename to `logs/coord-events-2026-05-pre-window.md` and create fresh `logs/coord-events-2026-05.md` via first invocation `coord-event-log.ps1`.

---

## Week 1 (5/20 → 5/26) — Sovereign tier baseline + Gate E start

### T8.W1: Plugin ecosystem first-touch dogfood

**Goal**: validate 3 plugins ESSENTIAL (compass + superpowers + claude-mem) operational sovereign.

- [ ] **Step T8.W1.1: claude-mem cross-session resumption test**

Run: avvia nuova Claude Code session, verify auto-injection di memory cross-session. Open `~/.claude-mem/` directory + check SQLite + Chroma vector DB populating.

Expected: nuova session opens con context preserved (no `claude-mem status` shows uninitialized).

- [ ] **Step T8.W1.2: superpowers skill auto-trigger observation**

During normale workflow week 1, observe which skill auto-triggers (brainstorming / writing-plans / using-superpowers / etc.). Log osservazione in `logs/sprint-02-plugin-observations.md`:

```markdown
| Skill | Auto-trigger event | Worked as expected? | Notes |
|-------|-------------------|---------------------|-------|
```

Target: ≥3 distinct skill invocations Week 1 to validate auto-trigger working.

- [ ] **Step T8.W1.3: compass project-direction tracking**

Run: `compass:compass-check` (project initialized 2026-05-10).
Expected: Direction Index 0-100 + drift signals. Log result in JOURNAL week 1.

### T9.W1: Methodology framework cite count baseline

**Goal**: empirical baseline cite count P1-P6 nei JOURNAL entries pre-Max vs post-Max (comparison T9 finale).

- [ ] **Step T9.W1.1: Baseline cite count pre-Max snapshot**

Run pre-Max (idealmente 5/19 sera tardi):
```bash
grep -c "Protocol 1\|Protocol 2\|Protocol 3\|Protocol 4\|Protocol 5\|Protocol 6" C:/dev/codemasterdd-ai-station/JOURNAL.md
```
Save in `logs/sprint-02-methodology-cite-count-baseline-2026-05-19.txt`.

Per-protocol breakdown:
```bash
for p in "Protocol 1" "Protocol 2" "Protocol 3" "Protocol 4" "Protocol 5" "Protocol 6"; do echo "$p: $(grep -c "$p" C:/dev/codemasterdd-ai-station/JOURNAL.md)"; done
```

- [ ] **Step T9.W1.2: Update tracking template**

Create `logs/methodology-cite-count-tracking-2026-MM.md` con week-by-week counter table:

```markdown
| Week | P1 | P2 | P3 | P4 | P5 | P6 | Total | Notes |
|------|----|----|----|----|----|----|-------|-------|
| pre-Max baseline (5/19) | X | X | X | X | X | X | X | Snapshot |
| W1 (5/26) | | | | | | | | |
```

### Gate E.W1: Logging discipline kickoff

**Goal**: anti-L-016 weekly cadence start.

- [ ] **Step Gate-E.W1.1: First weekly logging session**

Domenica 5/24: invoke `coord-event-log.ps1` interactive mode 1 volta + log eventi past week (es. 0 events legit if no missed-coordination occurred).

Update `logs/escalation-gates-2026-05.md` Week 1 row.

- [ ] **Step Gate-E.W1.2: Reminder schtask verify firing**

Domenica 5/24 09:00: verify schtask trigger + reminder file marker `logs/gate-e-reminder-due-2026-W21.md` (week 21 = 5/18-5/24) created.

If marker NOT created → P0 escalation: schtask broken empirical (P0.2 fix regression).

### Cost tracking T5.W1

- [ ] **Step T5.W1.1: First sovereign week ccusage snapshot**

End-of-week 5/26: run `ccusage` (Claude Code usage tracker) + cumulative cloud LLM spend log.

Save snapshot `logs/sprint-02-cost-2026-05-W1.md`:
```markdown
- Date: 2026-05-26
- Claude API spend cumulative: $X (target <$10 week)
- Cloud free tier usage: Groq X% / Cerebras X% / Gemini X%
- OpenAI emergency: $X (target $0 week 1)
- Total: $X (target <$5 week 1)
```

---

## Week 2 (5/27 → 6/2) — Plugin dogfood depth + Gate E mid-pulse

### T8.W2: Plugin ecosystem deeper dogfood

- [ ] **Step T8.W2.1: claude-mem search effectiveness**

Use `claude-mem:mem-search` skill ≥3 volte during week 2 lookup pattern (es. "ho già risolto X?", "come faccio Y?"). Log effectiveness in `logs/sprint-02-plugin-observations.md`:

```markdown
| Date | Query | Result quality (1-5) | Time saved vs manual | Notes |
|------|-------|----------------------|----------------------|-------|
```

Target: ≥3 queries with quality ≥3 = claude-mem operational

- [ ] **Step T8.W2.2: superpowers skill harsh-reviewer real-use**

If ≥1 PR opened during week 2, invoke harsh-reviewer subagent post-Draft (Protocol 5 cite increment). Cost cap awareness: <$2 week 2.

Validates P5 empirical use beyond aspirational. Cite in JOURNAL.

### T9.W2: Methodology adaptation observation

- [ ] **Step T9.W2.1: Mid-sprint cite count**

End-of-week 6/2: re-run cite count + delta calc:
```bash
for p in "Protocol 1" "Protocol 2" "Protocol 3" "Protocol 4" "Protocol 5" "Protocol 6"; do echo "$p: $(grep -c "$p" C:/dev/codemasterdd-ai-station/JOURNAL.md)"; done
```

Update tracking table W2 row.

**Honesty discipline**: if P6 brainstorming OR P5 harsh-reviewer NOT invoked during week 2, that's data not failure — log "0 invocations" honestly.

### Gate E.W2: Logging continues

- [ ] **Step Gate-E.W2.1: Sunday 5/31 logging session**

Invoke `coord-event-log.ps1` interactive past week events. Update `logs/escalation-gates-2026-05.md` Week 2.

Mid-point sanity check: if Week 1 + Week 2 cumulative <2 events → trend toward Gate E falsification (consistent <2/wk).

### Cost tracking T5.W2

- [ ] **Step T5.W2.1: ccusage Week 2 snapshot**

Same pattern. Cumulative target: <$10 first 2 weeks.

---

## Week 3 (6/3 → 6/9) — Three Strikes evaluation + Gate E mid-late

### T10.W3: Three Strikes Quality Gate trigger check

**Goal**: assess if Three Strikes condition (1 regress + 1 manual application + 1 emergent tier promote request) for vault MODEL_ROUTING Quality Gate pattern has fired.

Reference: ADR-0028 Quality Gate vault adoption Three Strikes trigger.

- [ ] **Step T10.W3.1: Audit Three Strikes condition counter**

Read `~/aa01/learnings/L-2026-05-012-vault-sibling-peer-write-under-explicit-authorization.md` + `~/aa01/learnings/L-2026-05-013-re-eval-calendarizzati-pattern.md` for Quality Gate pattern emergent instances.

Check `logs/aider-delegation-2026-MM.md` Week 1-3 entries for:
- Regression mentions (1 strike if found)
- Manual Quality Gate application (1 strike if found)
- Emergent tier promote request from agent (1 strike if found)

- [ ] **Step T10.W3.2: Document Three Strikes status**

Create `logs/sprint-02-three-strikes-audit-W3.md`:
```markdown
- Strike 1 (regression): YES/NO + reference
- Strike 2 (manual application): YES/NO + reference
- Strike 3 (emergent request): YES/NO + reference
- Status: <FIRE / 1-2 strikes / 0 strikes>
```

If FIRE → activate ADR-0028 Accepted ratification + MODEL_ROUTING.md section formal write per V3 REC 2.

### T8.W3 + T9.W3 + Gate E.W3 + T5.W3

Same pattern weekly. Update all tracking files.

---

## Week 4 (6/10 → 6/16) — Gate E threshold evaluation + harsh-reviewer audit + decisions

### Gate E.W4: Threshold evaluation prep

- [ ] **Step Gate-E.W4.1: Final week logging session 6/14 Sunday**

Last weekly invocation `coord-event-log.ps1` interactive past week.

- [ ] **Step Gate-E.W4.2: Aggregate 4-week count**

Run:
```bash
grep -c "^| 2026-05-[2-3]\|^| 2026-06-0\|^| 2026-06-1[0-6]" C:/dev/codemasterdd-ai-station/logs/coord-events-2026-05.md C:/dev/codemasterdd-ai-station/logs/coord-events-2026-06.md
```

Calculate avg events/week. Update `logs/escalation-gates-2026-05.md` cumulative summary.

### Week 4 audit (harsh-reviewer subagent invocato)

**Critical: P5 cite increment WITH empirical value (anti-aspirational).**

- [ ] **Step Audit.1: Invoke harsh-reviewer Gate E logging audit**

Dispatch harsh-reviewer subagent (Protocol 5 ADR-0026 addendum) with prompt:

```
Harsh review boundary read-only on Gate E logging discipline 4-week empirical (SPRINT_02 W1-W4).

Files to read:
- C:/dev/codemasterdd-ai-station/logs/coord-events-2026-05.md
- C:/dev/codemasterdd-ai-station/logs/coord-events-2026-06.md (if exists)
- C:/dev/codemasterdd-ai-station/logs/escalation-gates-2026-05.md

Check for:
1. Logging discipline consistency: no gap weeks (4/4 weekly sessions present)?
2. Severity tag distribution sanity: NOT all = 1 (under-reporting) OR all = 5 (panic logging)?
3. Cost minutes documentation present: NOT all = 0?
4. Aggregate count plausibility: cross-check with JOURNAL entries same week
5. Anti-pattern L-016 application: did Eduardo skip logging weeks claiming "intent to log later"?

Output P0/P1/P2 findings + Gate E threshold decision recommendation.

Boundary: read-only, no Write/Edit, only Read/Grep/Glob.
Cost target: ~$0.30 (~85K tokens), under ADR-0023 cap.
```

- [ ] **Step Audit.2: Review harsh-reviewer findings**

Read subagent output. Integrate P0 findings (must fix pre-decision) + P1/P2 findings (acknowledge).

- [ ] **Step Audit.3: Gate E decision finalize**

Based on:
- Aggregate avg events/week
- harsh-reviewer audit findings
- Honest Eduardo self-assessment

Decision matrix:

| Avg events/wk × 4 wk | Threshold | Component 1 decision |
|----------------------|-----------|---------------------|
| ≥5 | PASS | Build Component 1 full scope (Alternative A vs B Eduardo decides) |
| 2-<5 | PARTIAL | Build Component 1 MINIMAL scope (Alternative A extension only) |
| <2 | FALSIFIED | DEFER indefinitely. Archive pre-design `docs/superpowers/specs/2026-05-13-component-1-dashboard-design.md` → `docs/research/component-1-pre-design-archived-2026-06-15.md`. Update STATUS_MULTI_REPO trigger #1 empirically falsified. |

Document decision in `logs/sprint-02-gate-e-decision-2026-06-15.md`.

### T9.W4: Final methodology cite count + comparison

- [ ] **Step T9.W4.1: Post-Max cumulative cite count**

End-of-sprint 6/14 (or 6/16):
```bash
for p in "Protocol 1" "Protocol 2" "Protocol 3" "Protocol 4" "Protocol 5" "Protocol 6"; do echo "$p: $(grep -c "$p" C:/dev/codemasterdd-ai-station/JOURNAL.md)"; done
```

- [ ] **Step T9.W4.2: Delta vs baseline + analysis**

Compute delta per Protocol. Document in `logs/sprint-02-methodology-effectiveness-2026-06-15.md`:

```markdown
## Methodology effectiveness post-Max vs pre-Max baseline

| Protocol | Pre-Max baseline | Post-Max 4 weeks | Delta | Interpretation |
|----------|------------------|-------------------|-------|----------------|
| P1 Refresh-verify | X | X | +X | <interpretation> |
| P2 Autoresearch | X | X | +X | <interpretation> |
| P3 Archon 7-step | X | X | +X | <interpretation> |
| P4 AA01 workspace | X | X | +X | <interpretation> |
| P5 harsh-reviewer | X | X | +X | (already validated 3+ instances this preparation session) |
| P6 brainstorming | X | X | +X | (already validated 2+ instances this preparation session) |

## Empirical n=3 threshold check (P5/P6 ADR-0026 amendment B/C trigger)

- P5 invocations cumulative: X (threshold: ≥3 to remain Protocol)
- P6 invocations cumulative: X (threshold: ≥3 to remain Protocol)
- Decision: <maintain Protocol / downgrade to optional / formalize Accepted>
```

### Sprint-end retrospect T7.W4

- [ ] **Step T7.W4.1: 4-week retrospective write**

Create `logs/sprint-02-retrospective-2026-06-15.md`:

```markdown
## SPRINT_02 retrospective (2026-05-20 -> 2026-06-15)

### Empirical outcomes
- Gate E decision: <FALSIFIED / PARTIAL / PASS>
- Methodology framework cite delta: <summary>
- Three Strikes Quality Gate: <fired / not fired>
- Plugin ecosystem operational: <claude-mem ok / superpowers ok / compass ok>
- Cost cumulative: $<total> (target <$20)
- Dogfood organic count: <n cumulative>

### Continuita / mid-correction / SPRINT_03 scope

1. **Continuita**: <items continuing into SPRINT_03>
2. **Mid-correction**: <pattern changes mid-sprint>
3. **SPRINT_03 scope**: <new scope based on empirical findings>

### Lessons cumulative

- L-2026-05-XXX: <pattern observed>
- L-2026-06-XXX: <pattern observed>
```

- [ ] **Step T7.W4.2: BACKLOG + JOURNAL update**

- BACKLOG: mark SPRINT_02 tasks complete (X1-X5 + T8 + T9 + T10)
- JOURNAL: sprint closure entry (parallel ai sera-tardi-ultra-2 entry attuale, ma sprint scale)

### Cost final T5.W4

- [ ] **Step T5.W4.1: Cumulative cost log**

Final ccusage + cloud spend. Target verify <$5 cumulative (sovereign tier success criterion).

---

## Self-review checklist

**Spec coverage** (T8 + T9 + T10 + Gate E + harsh-reviewer audit):
- T8 plugin dogfood: W1-W3 tasks ✓
- T9 methodology cite count: W1 baseline + W2/W3/W4 tracking ✓
- T10 Three Strikes: W3 audit ✓
- Gate E logging discipline: W1-W4 weekly + W4 audit ✓
- Harsh-reviewer audit: W4 Audit.1-Audit.3 ✓
- Sprint retrospect: W4 T7 ✓

**Placeholder scan**: no TBD / TODO / "fill in details" — all concrete bash commands + files + thresholds ✓

**Type consistency**:
- Log file paths: `logs/sprint-02-*.md` + `logs/coord-events-*.md` + `logs/escalation-gates-*.md` consistent ✓
- Date format: 2026-MM-DD ISO consistent ✓
- Threshold ≥5 / 2-<5 / <2 (mutual exclusive post Codex P2 fix) ✓

**YAGNI**: no Component 1 BUILD pre-Gate-E (gated). NO speculation post-SPRINT_02.

**Scope**: 4 weeks elapsed + ~30min/wk Eduardo + ~3-5h cumulative concentrated = realistic.

---

## References

- SPRINT_02.md (base task headlines)
- ADR-0017 stack scaffolding
- ADR-0023 strategic tier post-Max API on-demand
- ADR-0026 cognitive workflow protocols (P1-P6)
- ADR-0028 Quality Gate vault adoption Three Strikes trigger
- Spec V3 cross-repo orchestrator Component 3 (Gate E spec)
- Component 1 pre-design (this PR companion)
- L-2026-05-016 anti-aspirational measurement
