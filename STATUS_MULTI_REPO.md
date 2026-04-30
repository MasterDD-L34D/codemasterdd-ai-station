# STATUS_MULTI_REPO

## Status

Historical / dormant.

This file used to be the live cross-repo dashboard. In the transplanted checkout
audited on 2026-04-30, the external paths it referenced were missing.

Current external repo state lives in:

- `EXTERNAL_REPOS.md`

Current repo recovery state lives in:

- `docs/recovery/2026-04-30-transplant-audit.md`
- `SPRINT_02.md`
- `BACKLOG.md`

## Why this dashboard was demoted

The old dashboard mixed:

- codemasterdd state;
- Game state;
- Synesthesia state;
- Dafne swarm runtime state;
- AA01 local workspace state;
- container and localhost status from the original machine.

Those facts cannot be verified from this checkout because the referenced paths
and runtime evidence are absent.

## Current rule

Do not update this file as a live dashboard until at least one external repo is
reactivated through `EXTERNAL_REPOS.md`.

If cross-repo governance is restored later, rebuild this file from fresh local
evidence instead of editing the old historical content.

## Dormant project list

| Project | Current state |
|---------|---------------|
| Evo-Tactics / Game | dormant |
| Synesthesia | dormant |
| Dafne swarm / evo-swarm | dormant |
| AA01 | dormant |

## Recovery note

The old content was intentionally replaced rather than maintained because it
contained stale HEADs, stale service statuses, and next actions tied to missing
paths.
