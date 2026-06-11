# Task: i18n NF3 -- migrate 4 core panels to t() label-map (batch PR-7)

Repo: MasterDD-L34D/Game
Target files (all under apps/play/src/): abilityPanel.js, formsPanel.js, helpPanel.js,
onboardingPanel.js

## Scope (mechanical label migration, no logic change)

- Migrate the hardcoded user-facing label strings in the 4 target panels to the t()
  label-map pattern, EXACTLY as done in the merged reference PRs:
  - PR #2664 (biomeChip.js / characterPanel.js / enneaVoiceRender.js / innerVoiceRender.js)
  - PR #2671 (debriefPanel.js)
  i.e. import t from the local i18n module, replace literals with t('key'), and add every
  new key to BOTH data/i18n/en/common.json and data/i18n/it/common.json (en/it parity).
- Idempotent guard: if any target file ALREADY uses the t() import on current main, SKIP
  that file and note the skip in the PR description.
- NO logic change, NO markup/structure change -- labels only.

## Acceptance (tests must pass)

- Where a per-panel test exists, extend it following the tests/play/characterPanel.test.js
  convention; otherwise add a key-presence test asserting en/it parity for every new key
  in the two locale JSON files.
- The full existing test suite passes (repo CI). CI green is required.

## Constraints

- ASCII-only in code and comments; non-ASCII characters are allowed ONLY inside the
  Italian locale string VALUES of data/i18n/it/common.json, consistent with that file.
- One PR for the whole batch. Conventional Commit subject, lowercase description, e.g.
  `feat(i18n): nf3 pr-7 -- 4 panel label-maps to t()`.
- Deliver as a PR. Do NOT merge -- human gate (Eduardo) disposes.
