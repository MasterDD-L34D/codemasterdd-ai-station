# Plan inventory 2026-05-01

## Purpose

This inventory rereads the plans that existed in the repository and separates:

- completed work;
- unfinished but still valid work;
- historical work that must not drive this checkout;
- external work that is dormant until reactivation;
- claims that require runtime evidence from the correct PC.

Current branch at inventory time: `codex/structural-reset`.
Current HEAD at inventory time: `aa71457`.

## Executive verdict

The plans were not lost, but they were layered on top of each other:

1. `SPRINT_01.md` closed the old dogfood/reliability push early, with some
   soft goals incomplete or inconclusive.
2. `SPRINT_02.md` replaced that old focus with structural recovery after the
   transplant.
3. Cross-repo plans for Game, Synesthesia, Dafne, and AA01 are historical or
   dormant in this checkout.
4. Observability and dogfood UI code exists, but runtime evidence is missing
   here.
5. Several ADR follow-ups remain useful, but many depend on the original
   workstation or missing logs.

## Active plan: Sprint 02 structural recovery

Source: `SPRINT_02.md`, `BACKLOG.md`, `ROADMAP.md`, `PROJECT_STATE.yaml`.

### Done in this branch

| Item | Result |
|------|--------|
| S2-01 Recovery audit | Done: `docs/recovery/2026-04-30-transplant-audit.md`. |
| S2-02 External repo quarantine | Done: `EXTERNAL_REPOS.md`. |
| S2-03 Governance root refresh | Done: root governance files rewritten around current scope. |
| S2-04 Dashboard demotion | Done: `STATUS_MULTI_REPO.md` is historical/dormant. |
| S2-05 Agent surface reduction | Done: `.claude/agents/README.md` labels usable vs dormant agents. |
| S2-06 Runtime evidence policy | Done: `docs/recovery/runtime-artifacts-policy.md`. |
| S2-07 Encoding policy | Done as policy, not full cleanup: `docs/recovery/encoding-policy.md`. |
| S2-08 Original system reconstruction | Done: original intent + reconnect playbook. |
| S2-09 Instruction surface cleanup | Done: `AGENTS.md`, `CLAUDE.md`, `MODEL_ROUTING.md`. |
| S2-10 Merge readiness package | Done: checklist + PR description draft. |
| S2-11 Minimal state and anti-regression | Done: `PROJECT_STATE.yaml`, boundary doc, consistency script. |
| S2-12 System map and local profile | Done: `config/system-map.yaml`, profile template. |
| S2-13 Recovery diagnostics/dashboard | Done: `scripts/recovery-status.ps1`, `scripts/check-all.ps1`, `/recovery`, Dafne opt-in. |
| S2-14 Client matrix and ADR-0021 | Done: matrix + ADR-0021. |

### Still open in the active backlog

These are real but low-risk follow-ups for this repo:

- create an index of frozen historical files;
- normalize mojibake only in active files, not globally;
- review `PROMPT_LIBRARY.md`;
- review `MODEL_ROUTING.md` again after the correct PC is checked;
- decide on the correct PC whether OpenCode is only a bridge or a real
  secondary client;
- decide on the correct PC whether to full-merge, cherry-pick, or hybrid-merge;
- decide whether to wire `scripts/check-recovery-consistency.ps1` into a hook or
  lightweight CI;
- reduce or archive `Archivio_Libreria_Operativa_Progetti/` only if the repo
  should become minimal.

## Previous plan: Sprint 01 dogfood/reliability

Source: `SPRINT_01.md`, `JOURNAL.md`, ADR-0014/0015/0016/0017.

### Done historically

- Hard sprint goals marked closed early:
  - 12/12 dogfood entries reached;
  - 5/3 behavior-critical entries reached;
  - 0 silent-corruption maintained;
  - cost snapshot documented;
  - week-2 review performed early.
- Governance files were created during the original Sprint 01 era.
- ADR-0015 and ADR-0016 drafts were created.
- The observability stack was reportedly validated live on the original machine.

### Not fully done or inconclusive

- Cosmetic dogfood target was partial: 7/10, not 10/10.
- cp1252 retry-loop validation was inconclusive: no natural retry-loop trigger
  occurred by the sprint close.
- The n>=20 dogfood target and week-4 ratification were not completed before the
  transplant reset.
- ADR-0015, ADR-0016, and ADR-0017 still need final ratification from fresh or
  restored evidence.

### Current interpretation

Sprint 01 is historical. Its claims may be true for the original PC, but this
checkout lacks the dogfood log, SQLite DB, promptfoo results, and service state
needed to verify them locally.

## ADR plan status

Source: `DECISIONS_LOG.md`, `docs/adr/`.

### Active accepted principles

- ADR-0005 YAGNI/minimalism.
- ADR-0008 Aider whole-format silent-corruption safety lesson.
- ADR-0010 MADR format and skill policy.
- ADR-0011 cross-agent commit governance, principle active but hooks unverified
  here.
- ADR-0018 agent readiness protocol.
- ADR-0020 silent-fail Python guardrail, principle active but hook install
  unverified here.
- ADR-0021 structural recovery and external repo quarantine.

### Proposed, partial, or evidence-dependent

- ADR-0007 is partially superseded by ADR-0008.
- ADR-0009 remains proposed/historical strategy.
- ADR-0015 remains proposed: final budget decision depends on dogfood/runtime
  evidence.
- ADR-0016 remains proposed: constraint-count routing needs more data.
- ADR-0017 was validated live historically but remains scaffold/dormant here
  until services and runtime state are verified.

## Observability, dashboard, and dogfood system

Source: `apps/dogfood-ui/README.md`, `infra/README.md`, ADR-0017, Journal.

### Code present

- `infra/` Docker Compose scaffold exists.
- `apps/dogfood-ui/` Flask app exists.
- quality-bench configs and promptfoo configs exist.
- migration script `scripts/migrate-log-to-sqlite.py` exists.
- `/recovery` dashboard exists and is safe for this checkout.

### Missing here

- `apps/dogfood-ui/data/dogfood.sqlite`;
- `logs/aider-delegation-2026-04.md`;
- promptfoo result outputs;
- Langfuse/Postgres runtime data;
- LiteLLM virtual key state;
- API keys and local Aider wrapper binaries.

### Current status

Scaffold is done. Runtime restoration is not done in this checkout.

## Agent ecosystem

Source: `.claude/agents/README.md`, Journal 2026-04-24.

### Done historically

- The repo contains an 18-agent ecosystem.
- Historical status said 12 ready and 6 draft after smoke tests.
- Source attribution was recorded for the original agent design work.

### Current status

Mixed active/dormant:

- potentially usable for this repo: ADR, bench, cost, dogfood, harsh review,
  security, repo-health, delegation, compact-context style agents;
- dormant until external reactivation: Game, Synesthesia, Dafne, lore, privacy,
  DB, a11y, swarm agents.

### Tralasciato

- Fresh smoke tests were not rerun in this transplanted checkout.
- Cross-repo agents were not moved; they were labelled first.

## External repo plans

Source: `EXTERNAL_REPOS.md`, `STATUS_MULTI_REPO.md`, Journal.

### Game / Evo-Tactics

Historical plan/finding:

- Game had pending red findings around boss enrage and XP curve.
- Swarm/Game agent integration branches existed historically.

Current status:

- dormant here because `C:\dev\Game` is missing.
- no Game fix was done in this repo.

### Synesthesia

Historical plan/finding:

- privacy validation and exam-related work were deferred/dormant.

Current status:

- dormant here because `C:\dev\synesthesia` is missing.
- no privacy validation was done in this repo.

### Dafne swarm

Historical plan/finding:

- persistence wrapper, Day-5 work, chat, voice/widget/always-up ideas, and
  persona/memory archaeology existed in the Journal.

Current status:

- dormant here because `C:\Users\edusc\Dafne\workspace\swarm` is missing.
- `apps/dogfood-ui` now treats Dafne as opt-in via `DAFNE_ENABLED=1`.
- no Dafne runtime repair was done in this repo.

### AA01

Historical plan/finding:

- two AA01 tasks were left proposed for human review in an external workspace.

Current status:

- dormant here because `C:\Users\edusc\aa01` is missing.
- no AA01 review/archive was done in this repo.

## Archive framework and prompt library

Source: `Archivio_Libreria_Operativa_Progetti/`, `PROMPT_LIBRARY.md`.

### Done

- The archive framework was imported historically.
- It influenced the root governance style.
- It is now labelled as historical/reference, not the active sprint.

### Not done

- No complete frozen-file index exists yet.
- `PROMPT_LIBRARY.md` still needs a post-transplant review.
- The archive has not been reduced or moved.

## What was genuinely tralasciato

Important omissions that are still worth remembering:

1. Redacted runtime export format: policy exists, but no concrete manifest was
   generated because runtime files are absent here.
2. Historical frozen-file index: still missing.
3. Active mojibake cleanup: policy exists, full cleanup intentionally deferred.
4. Prompt library review: not done.
5. Final model routing reconstruction: not done; must happen on the correct PC.
6. OpenCode decision: not done; requires install/config check on the correct PC.
7. ADR-0015/0016/0017 ratification: not done; depends on restored evidence.
8. Dogfood n>=20 / week-4 closure: not done here and no longer active without
   logs/DB.
9. External project work: not done here by design.
10. Agent re-smoke-test in this checkout: not done.

## What should be checked on the correct PC

Run `docs/recovery/pre-merge-checklist.md`, then verify:

- whether the external paths exist;
- whether dogfood logs and SQLite DB exist;
- whether Aider wrappers and global hooks exist;
- whether LiteLLM/Langfuse/promptfoo runtime state exists;
- whether OpenCode exists or is only an archived candidate;
- whether Game/Synesthesia/Dafne/AA01 should be reactivated one at a time.

## Bottom line

For this checkout, structural recovery is complete enough to review and merge.

For the original workstation, the work is not "finished" until the correct PC
confirms which historical runtime facts still exist and which old plans should
be reactivated.
