# ADR-0038 — Doctrine carve-out completion (amends ADR-0037 decision 2)

> Status: **Accepted** 2026-06-11 (Eduardo; ratify dossier
> `docs/research/adr-0038-0039-ratify-dossier-2026-06.md` -- ACCEPT with 4 textual amendments,
> applied below, + the actor-activation-criteria sec 7 sync landed in the same ratify PR).
> Proposed 2026-06-03. SDMG harsh-reviewer falsification (Cognitive Protocol 7)
> done 2026-06-03 -- see "Falsification". This is a doctrine file
> (`docs/adr/**`) = Eduardo-only-merge per ADR-0037 dec.2, so the hub does NOT self-merge it
> (ratify PR merge = Eduardo).
> Amends ADR-0037 decision 2 only; everything else in ADR-0037 stands. ASCII-first (ADR-0021).
> **This amendment RESTRICTS hub self-merge (anti-self-licensing). It grants NOTHING.**

## TL;DR

ADR-0037 decision 2 made "governance-doctrine files = Eduardo-only-merge regardless of repo",
listed via a **closed 6-item enumeration**. A harsh-reviewer SDMG falsification (run on a
separate, REJECTED merge-authority-grant draft, 2026-06-03) found that enumeration is
**incomplete + gameable**: rule/decision/charter-defining governance files are uncovered --
notably `GOALS.md` (root direction/rule file the hub operates under; the G1/G4 autonomy goals
live in `docs/superpowers/jules/2026-06-03-jules-autonomy-gaps.md`, deliberately NON-doctrine
as inputs -- attribution re-founded at ratify 2026-06-11, amendment 1), `DECISIONS_LOG.md`
(binding decisions), `AGENTS.md`, `docs/governance/**` (governor mechanics), and `.claude/agents/**`
(subagent charters, including `harsh-reviewer.md` -- the falsifier's own charter). A future
merge-authority loosening could route through the gap, or through a NEW governance file
created outside the enumerated set. This amendment completes the carve-out via **globs** (so
new files under high-risk dirs are doctrine by default) plus the missing named root rule-files.

## Context

- ADR-0037 dec.2 carve-out (the 6): `ORCHESTRATION.md`, `docs/adr/**`,
  `docs/governance/actor-activation-criteria.md`, authoritative `CLAUDE.md`,
  `.claude/settings.json`, `~/.config/aider-privacy-whitelist.txt`.
- harsh-reviewer findings (2026-06-03, verbatim gist):
  - **P0.1** the set is a closed enumeration; ~25 governance artifacts exist; "non-doctrine"
    default captures `GOALS.md`, `DECISIONS_LOG.md`, `OPEN_DECISIONS.md`, `AGENTS.md`,
    `docs/governance/*` (siblings of actor-criteria), `.claude/agents/*`.
  - **P0.2** (as re-founded at ratify 2026-06-11, amendment 1 / dossier P2-3): `GOALS.md` is
    doctrine as a root direction/rule file the hub operates under -> self-merge = direct loop.
    The G1/G4 autonomy goals live in `docs/superpowers/jules/2026-06-03-jules-autonomy-gaps.md`,
    deliberately NON-doctrine as inputs; the original finding's attribution ("G1/G4 ARE the
    merge-autonomy doctrine") was mis-founded. No file changes classification -- only the WHY
    is corrected.
  - **P1.2** a new governance file created OUTSIDE the set is "non-doctrine" by default ->
    gameable. Fix = invert toward globs / a positive allow-list, not a static blacklist.
- This gap exists on `origin/main` TODAY, independent of any grant. Closing it is pure
  tightening.

## Decision -- amend ADR-0037 decision 2

**Governance-doctrine files (Eduardo-only-merge, regardless of repo; hub proposes branch+PR)
= the union of:**

- **GLOBS (new files under these are doctrine by default):**
  `docs/adr/**`, `docs/governance/**`, repo `.claude/**` (settings, agents, rules, skills, hooks),
  `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/**` (the meta-operating
  rules CLAUDE.md elevates to authority -- `SAFE_CHANGES_ONLY.md`/`CHANGE_BUDGET.md`/
  `CLAUDE_OPERATING_RULES.md` = the hub autonomous-change envelope; editing them loosens what
  the hub may do without a human).
- **GLOBAL `~/.claude/` governance subpaths (explicit positive list -- NOT the whole dir, which is
  mostly machine-local junk: credentials, cache, sessions, plugins):** `~/.claude/CLAUDE.md`,
  `~/.claude/rules/**`, `~/.claude/reference/**`, `~/.claude/agents/**`, `~/.claude/commands/**`,
  `~/.claude/skills/**`, `~/.claude/settings.json`, `~/.claude/hooks/**` (`~/.claude/agents/**`
  is prospective -- not on disk today; the live agents dir is the repo-level `.claude/agents/**`,
  e.g. `harsh-reviewer.md` -- amendment 2 at ratify 2026-06-11).
- **NAMED root rule/decision/governance files:** `CLAUDE.md` (authoritative, any level),
  `AGENTS.md`, `ORCHESTRATION.md`, `GOALS.md`, `DECISIONS_LOG.md`, `OPEN_DECISIONS.md`.
- `~/.config/aider-privacy-whitelist.txt`.
- **CATCH-ALL (makes the Principle operative, not just descriptive; human-review-enforced -- no
  path-classifier can evaluate content, see ADR-0039 dec.2 -- amendment 3 at ratify 2026-06-11):**
  ANY file -- regardless of
  path, including newly-created ones outside the globs above (e.g. a future `docs/policy/*` or a
  new root rule-file) -- whose content defines rules/gates/decisions/charters the hub operates
  under is doctrine pending classification. When in doubt -> treat as doctrine + ask Eduardo.
  This closes the "create a governance file at an unforeseen path and self-merge it" hole.

**Explicitly NON-doctrine (hub self-merge OK per ADR-0037 dec.1 classifier-per-call):**
`scripts/**`, `docs/research/**`, `docs/handoffs/**`, `docs/reference/**`,
`docs/superpowers/**`, `JOURNAL.md`, `README.md`, code/tests, and the OPERATIONAL/STATUS/
REFERENCE root files that do NOT define rules about the hub itself: `MODEL_ROUTING.md`
(operational routing), `BACKLOG.md`, `COMPACT_CONTEXT.md`, `STATUS_MULTI_REPO.md`,
`REFERENCE_INDEX.md`, `PROMPT_LIBRARY.md`, `PROJECT_BRIEF.md`,
`FIRST_PRINCIPLES_INFRA_CHECKLIST.md`, and `MASTER_PROMPT.md` (a portability prompt for
out-of-native sessions; runtime-inert in native Claude Code where `CLAUDE.md` supersedes it --
if it ever becomes a live runtime constraint-source, promote it to doctrine).

**Principle (the test for "doctrine"):** a file is doctrine if editing it could loosen the
hub's own governance/autonomy/merge gates, OR it defines rules/decisions/charters the hub
operates under. Operational routing, status, backlog, and reference files fail that test ->
they stay hub-mergeable (keeps routine friction down). The high-risk DIRS are glob'd so a
newly-created governance file inherits doctrine status (closes P1.2). Any NEW autonomous
write-path (beyond the ADR-0039 rung) must re-implement both the construction-time doctrine
gate and the human classification checkpoint -- the rung's guards do not transfer automatically
to future write-paths (amendment 4 at ratify 2026-06-11).

## Consequences

- **Positive:** `GOALS.md`, `DECISIONS_LOG.md`, `OPEN_DECISIONS.md`, `AGENTS.md`,
  `docs/governance/**`, `.claude/**` are now Eduardo-only-merge. The "new file outside the
  set" hole is closed for the glob'd dirs. ADR-0037's anti-self-licensing intent is made
  whole. Hub self-merge is limited to genuinely non-rule-defining files.
- **Negative / accepted:** more files are Eduardo-only-merge (this is the point -- tightening).
  Editing `GOALS.md`/`DECISIONS_LOG.md`/etc. now needs an Eduardo merge. Accepted: these are
  exactly the files where a hub must not merge its own rule-book.
- **No authority granted:** the merge-authority-grant proposal (separate draft) was KILLED by
  this same falsification and is NOT part of this ADR (recorded in memory
  `feedback_external_repo_action_boundary` v3).

## Falsification (SDMG Protocol 7, 2026-06-03)

External harsh-reviewer falsification PRE-merge. Verdict **SURVIVE-WITH-CHANGES** (the tightening
is real, not a disguised grant -- "grants nothing" confirmed clause-by-clause). Adopted PRE-merge:
- **BLOCKING** -- added `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/**` to the doctrine globs:
  it defines the hub autonomous-change envelope (`SAFE_CHANGES_ONLY.md`) and is CLAUDE.md-elevated
  ("le regole 07 vincono per pattern operativi") -- was a live uncovered self-licensing path.
- **BLOCKING** -- `MASTER_PROMPT.md` classification was unargued; now justified (runtime-inert,
  CLAUDE.md-superseded in native sessions) with a promote-if-it-changes note.
- **SIGNIFICANT** -- replaced the over-broad `~/.claude/**` glob with an explicit
  governance-subpath positive list (excludes credentials/cache/sessions/plugins).
- **SIGNIFICANT** -- added the content-based CATCH-ALL clause, making the Principle operative and
  closing the residual "new governance file at an unforeseen path" hole (P1.2 family).
- **MINOR** -- `docs/superpowers/jules/**` left NON-doctrine (goals = inputs to doctrine, like a backlog, not
  doctrine themselves; `GOALS.md` root IS doctrine). Noted to pre-empt the next falsifier.

Pre-commit stance "se rigetta adotto, non difendo" honored: all blocking + significant findings
adopted before this PR; verdict flips to Accepted only on Eduardo's merge.

## References

- ADR-0037 (merge-autonomy model -- this amends decision 2), ADR-0026 (Protocol 7 SDMG).
- harsh-reviewer report 2026-06-03 (the falsification that found the carve-out gap).
- memory `feedback_external_repo_action_boundary` v2/v3 (the reconciliation + killed grant).
- Ratify dossier `docs/research/adr-0038-0039-ratify-dossier-2026-06.md` (2026-06-11: evidence
  check + harsh-review SDMG run; source of amendments 1-4 and of the same-PR
  `actor-activation-criteria.md` sec 7 sync).
