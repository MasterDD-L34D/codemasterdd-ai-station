# Cross-Repo Goals D1 Implementation Plan

> **Status (2026-06-23):** shipped -- goals layer live (GOALS.md)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Build the D1 read-only goals layer -- a `codemasterdd/GOALS.md` hub synthesis + per-repo `## Goals (S/M/L)` canonical sections -- so every session reads shared direction. No automation (D2 gated separately).

**Architecture:** A+B hybrid. Hub `GOALS.md` (synthesis table + cross-cutting) in codemasterdd = read-only mirror, refreshed by repo-health-auditor. Per-repo goals canonical in each repo's own governance (self-gov respected, branch+PR where needed). Source: spec `2026-05-21-cross-repo-goals-coordination-design.md` section 4.

**Tech Stack:** Markdown docs, git, gh CLI. No code, no build. Validation = markdown parse + link resolve + section presence.

---

## File Structure

- Create: `codemasterdd/GOALS.md` (hub synthesis)
- Modify: `codemasterdd/STATUS_MULTI_REPO.md` (cross-link), `codemasterdd/CLAUDE.md` (reading-order ref)
- Modify: `codemasterdd/.claude/agents/repo-health-auditor.md` (add GOALS.md refresh duty)
- Per-repo (branch+PR each): Game `BACKLOG.md`, Game-Godot-v2 `CLAUDE.md`, Game-Database `CLAUDE.md`, vault `hot.md`, evo-swarm `ROADMAP.md`

Sequencing: Tasks 1-3 = codemasterdd (my lane, direct push), deliver hub value immediately. Task 4 = per-repo sections (branch+PR, collision-aware vs active sessions), lower urgency.

---

### Task 1: GOALS.md hub synthesis

**Files:**
- Create: `codemasterdd/GOALS.md`

- [ ] **Step 1: Write GOALS.md** with frontmatter + synthesis table + cross-cutting section.

```markdown
# GOALS -- Cross-Repo Direction (S/M/L)

> Read-only hub synthesis. Canonical goals live per-repo (each repo's `## Goals (S/M/L)`).
> Refreshed by repo-health-auditor agent. Horizons: Short=sprint(weeks) / Mid=epic(1-2mo) / Long=vision(3-6mo).
> Last refresh: 2026-05-21. Source: docs/superpowers/specs/2026-05-21-cross-repo-goals-coordination-design.md

## Snapshot

| Repo | Short | Mid | Long | Cross-dep |
|------|-------|-----|------|-----------|
| Game (Vue3) | Close M1 Sistema (route #2364 + pilot #2363); hardcore band revision (#2365) | M1 full Game<->Godot; trait completeness | Co-op tactical shippable, TV+phones Jackbox, ~60min, "how you play shapes what you become" | M1 (backend) |
| Game-Godot-v2 | M1 Sistema Godot client (#342); Bond 3.5d residue | M2 generational succession prod; Bond depth | Canonical frontend (Vue3 archive); full systems shippable | M1 (client) |
| Game-Database | Fase 3 schema versioning Phase A (#154); DB hygiene (#155 GIN, slug) | Versioning complete (revertable taxonomy); audit-UI mature | Robust versioned auditable content backend (evo:import) | feeds Game |
| vault | Pathfinder corpus ingest + bloat triage | KB coverage; 7/7 agents stable | Complete personal/project knowledge layer, agent-queryable | -- |
| evo-swarm (Dafne) | dafne/portability-fix | Integrable game content low-manual-validation | Trusted AI content-orchestration meta-layer at scale | feeds Game |
| codemasterdd | This goals layer; whisper SDMG empirical | Sovereign stack maturity (ADR-0030 Hybrid A1); coordination tooling (gated) | Self-sufficient sovereign AI dev station + ecosystem governance | hub |

## Cross-cutting initiatives

- **M1 "Sistema"** (persistent cross-session AI learning). Spans Game backend (route sistema-state #2364 + pilot #2363) + Godot client/mirror (#342, spec #340). **Ordering constraint:** merge Game backend route BEFORE Godot client (avoid client-on-missing-route, drift-seam L-066).

## Notes

- D2 auto-coordination = gated (harsh-reviewer + 2-week SDMG + new-evidence). See spec section 6. This file is READ-ONLY direction, no auto-trigger.
```

- [ ] **Step 2: Validate** -- run `npx markdownlint GOALS.md` if available, else verify table renders + no broken markdown by eye. Expected: parses clean.

- [ ] **Step 3: Commit**

```bash
git add GOALS.md
git commit -m "docs(goals): add cross-repo S/M/L hub synthesis (D1)"
```

---

### Task 2: Cross-link GOALS.md from STATUS + CLAUDE.md

**Files:**
- Modify: `codemasterdd/STATUS_MULTI_REPO.md` (add link near top)
- Modify: `codemasterdd/CLAUDE.md` (reading-order list: add GOALS.md)

- [ ] **Step 1: Add link to STATUS_MULTI_REPO.md** -- after the title/intro block, add line:

```markdown
> Direction layer: see [`GOALS.md`](GOALS.md) for cross-repo Short/Mid/Long goals.
```

- [ ] **Step 2: Add GOALS.md to CLAUDE.md reading-order** -- in the "Ordine di lettura raccomandato" list, insert after STATUS_MULTI_REPO entry:

```markdown
3b. `GOALS.md` -- direzione cross-repo S/M/L (se task tocca pianificazione/priorita)
```

- [ ] **Step 3: Commit**

```bash
git add STATUS_MULTI_REPO.md CLAUDE.md
git commit -m "docs(goals): cross-link GOALS.md from STATUS + reading-order"
```

---

### Task 3: Wire repo-health-auditor to refresh GOALS.md

**Files:**
- Modify: `codemasterdd/.claude/agents/repo-health-auditor.md`

- [ ] **Step 1: Add GOALS.md refresh duty** -- append to the agent's responsibilities/output section a line stating it MAY refresh `GOALS.md` Snapshot table (read-only aggregation from per-repo `## Goals (S/M/L)` + recent PR themes), like it refreshes STATUS_MULTI_REPO. Explicit: read-only, no write-back to other repos, no auto-trigger.

```markdown
- **GOALS.md refresh** (optional, on cross-repo audit): aggregate per-repo `## Goals (S/M/L)` + recent PR themes into the `GOALS.md` Snapshot table. Read-only synthesis (same pattern as STATUS_MULTI_REPO). NEVER write goals back into other repos; NEVER auto-trigger work from goals.
```

- [ ] **Step 2: Commit**

```bash
git add .claude/agents/repo-health-auditor.md
git commit -m "docs(agent): repo-health-auditor refreshes GOALS.md (read-only)"
```

---

### Task 4: Per-repo `## Goals (S/M/L)` canonical sections (branch+PR each)

**Collision-aware:** Game/Godot/Database have active sessions. Add the section to TOP of the target governance file (additive, minimal collision). One branch+PR per repo. codemasterdd does NOT merge (repo self-gov / Eduardo-only for vault).

**Files (per repo):**
- Game: `BACKLOG.md` -- new `## Goals (S/M/L)` section after title block
- Game-Godot-v2: `CLAUDE.md` -- new `## Goals (S/M/L)` section
- Game-Database: `CLAUDE.md` -- new `## Goals (S/M/L)` section
- vault: `hot.md` -- new `## Goals (S/M/L)` section
- evo-swarm: `ROADMAP.md` -- new `## Goals (S/M/L)` section

- [ ] **Step 1 (per repo): branch + add section** -- content = that repo's row from GOALS.md, expanded. Example (Game `BACKLOG.md`):

```markdown
## Goals (S/M/L)

> Canonical per-repo goals. Hub mirror: codemasterdd/GOALS.md. Horizons: Short=weeks / Mid=1-2mo / Long=3-6mo.

- **Short**: close M1 Sistema persistent learning (route #2364 + pilot #2363); finalize hardcore band revision (#2365 OD-032).
- **Mid**: M1 Sistema full wired Game<->Godot; trait system completeness (post-A4).
- **Long**: shippable co-op tactical loop -- 4-8 friends, TV + phones, ~60min runs, "how you play shapes what you become".
```

- [ ] **Step 2 (per repo): commit on branch + push + PR**

```bash
git checkout -b claude/goals-section-2026-05-21
git add <governance-file>
git commit -m "docs(goals): add Goals (S/M/L) section (hub: codemasterdd/GOALS.md)"
git push -u origin claude/goals-section-2026-05-21
gh pr create --title "docs(goals): add Goals (S/M/L) section" --body "Canonical per-repo goals, mirrors codemasterdd/GOALS.md. D1 cross-repo goals rollout."
```

- [ ] **Step 3: Eduardo merges** (repo self-gov / vault Eduardo-only). codemasterdd does NOT merge.

---

## Self-Review

- **Spec coverage:** D1 sections 3a (per-repo, Task 4), 3b (hub, Task 1), 3c (horizons, Task 1 frontmatter), 5 (refresh wiring, Task 3). D2 = out of scope (gated, spec section 6). Covered.
- **Placeholder scan:** GOALS.md content concrete (from spec section 4). Per-repo content = that repo's row expanded (example shown for Game; other repos analogous from GOALS.md rows). No TBD.
- **Consistency:** horizon defs (Short/Mid/Long weeks/1-2mo/3-6mo) consistent across hub + per-repo. M1 ordering constraint stated in both GOALS.md + spec.

## Notes
- Tasks 1-3 = immediate (codemasterdd, direct push). Task 4 = follow-up PRs, collision-aware, lower urgency -- hub (Task 1) already delivers full synthesis.
- D2 auto-coordination NOT in this plan (gated).
