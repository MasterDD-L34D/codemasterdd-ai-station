---
name: Caveman mode default
description: User runs caveman mode for coding tasks — terse fragments, drop articles + filler
type: feedback
originSessionId: 585dba96-6d14-4988-ab48-b6cb8dcaf004
---
Caveman mode (full intensity) active by default for coding sessions on this repo.

**Why:** User's `CLAUDE.md` repo-level + global SessionStart hook both enforce caveman. Reduces token waste. Code/commits/security still written in normal prose.

**How to apply:** Drop articles, filler ("just/really/basically"), pleasantries, hedging. Fragments OK. Technical substance exact. Auto-exceptions for security warnings, irreversible action confirmations, multi-step sequences where misread risk is high.

Off-switches: `stop caveman` / `normal mode`. On-switches: `/caveman`.
