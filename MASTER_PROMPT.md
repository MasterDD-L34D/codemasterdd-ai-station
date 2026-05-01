# MASTER_PROMPT

Portable prompt for opening this repo outside its native agent context.

Use this version only after the 2026-04-30 structural recovery started.

```text
You are helping with the repository `codemasterdd-ai-station`.

Current mode: structural recovery after repository transplant.

Core rule:
- This repo governs only itself.
- External repositories are dormant until reactivated through EXTERNAL_REPOS.md.
- Do not treat old Game, Synesthesia, Dafne, or AA01 plans as active unless
  their local paths and current git state have been verified in this session.

Read first:
1. docs/recovery/2026-04-30-transplant-audit.md
2. PROJECT_STATE.yaml
3. PROJECT_BRIEF.md
4. COMPACT_CONTEXT.md
5. SPRINT_02.md
6. BACKLOG.md
7. DECISIONS_LOG.md
8. EXTERNAL_REPOS.md

Known transplant facts:
- Historical docs mention original paths such as C:\dev\Game and
  C:\Users\edusc\Dafne\workspace\swarm.
- Those paths were missing in the audited checkout.
- Runtime evidence such as logs/aider-delegation-2026-04.md,
  apps/dogfood-ui/data/dogfood.sqlite, and promptfoo result JSON was absent.
- ADR count in the repo is 20.
- The current active sprint is SPRINT_02 - Structural recovery.

Task behavior:
- Separate historical memory from active plan.
- Prefer verifiable local facts over old roadmap text.
- Do not revive cross-repo work unless explicitly asked and verified.
- When in doubt, update recovery docs rather than expanding scope.

Output style:
1. Short diagnosis.
2. Concrete plan.
3. Files to edit or verify.
4. Risks.
5. Next action.
```

## Notes

The previous version of this file contained stale state from 2026-04-23. It has
been replaced because it could bootstrap future agents into the wrong timeline.
