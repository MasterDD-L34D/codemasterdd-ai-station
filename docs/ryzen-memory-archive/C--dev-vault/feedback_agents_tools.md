---
name: feedback-agents-tools
description: "Eduardo expects systematic use of right agents + skills + tools, not linear execution. Caveman terseness ≠ skipping orchestration."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5639ec97-2e1a-44fc-99a8-39e7cc37946e
---

Eduardo reminded 2026-05-19: "dovresti sempre accompagnarti con l'uso di agent e tool giusti."

**Why:** caveman mode trims words, NOT orchestration. Skipping skill-invocation / agent-delegation = under-leveraging Claude Code platform. Skills exist for a reason — `using-superpowers` rule applies. Even small tasks have applicable skills (code-review on diff, verification-before-completion before push, brainstorming before changes, caveman-commit for messages).

**Lessons:**
- 2026-05-19: suggested `/ultrareview <URL>` syntax without verifying skill arg parsing → Eduardo burned 1/3 free attempt. NEVER suggest skill arg syntax not documented/verified. Default = cwd-resolution (skill reads repo from `git remote` of cwd). Triple-check repo target BEFORE expensive/quota-limited skill launch.
- 2026-05-19: PC-confusion drift. Eduardo had MULTIPLE Claude sessions (Lenovo + Ryzen) coordinating. I kept saying "su Lenovo" when current session was Ryzen (hostname `DESKTOP-T77TMKT` verified turn-1). Track `hostname` of THIS session explicitly. When user says "ho sprecato X", verify which session/PC the action originated from BEFORE prescribing fix. Multi-PC coord = label each action with origin-PC explicitly.

**How to apply:**
- ANY task → first invoke `using-superpowers` Skill check (if not already loaded session).
- Before non-trivial edits → `brainstorming` skill (creative/design work).
- Before push/PR → `engineering:code-review` skill on diff + `verification-before-completion`.
- Commit messages → `caveman:caveman-commit` skill (caveman session).
- Multi-step research/heavy reads → delegate Agent (Explore/general-purpose) to protect main context.
- Parallel independent work → `dispatching-parallel-agents` skill.
- Caveman text style is orthogonal to tool/skill discipline. Apply both.

Linked: [[caveman-mode-preferences]] (if exists), `using-superpowers` rule (skills-first).
