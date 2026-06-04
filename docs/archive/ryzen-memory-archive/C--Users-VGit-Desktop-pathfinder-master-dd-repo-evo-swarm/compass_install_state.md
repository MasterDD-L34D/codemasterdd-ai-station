---
name: Compass plugin install state (evo-swarm)
description: Compass v0.4.2 installato user scope con workaround locale, fix v0.4.3 in PR upstream — stato del primo dogfood sul repo
type: project
originSessionId: 49bdf0f6-aa96-453b-b334-ad6e42ca615d
---
Compass plugin (`compass@compass-marketplace`) installato user scope su Windows il 2026-04-25, slot serale. Funziona: `/compass:check`, `/compass:drift`, `/compass:boot` operativi. Baseline DI 65/100 (4/6 pilastri toccati, P3+P4 untouched, coerente con DAY-5 famiglia non ancora eseguito).

**Why:** Step 2 di `COMPASS-HANDOFF.md` (`claude plugin marketplace add MasterDD-L34D/compass-marketplace`) fallisce per schema bug — `marketplace.json` v0.4.2 dichiara `plugins[].source` come oggetto `{"source": "local", "path": "..."}`, rifiutato da claude CLI 2.1.104. Form corretta è stringa (es. `"./plugins/compass"`).

**How to apply:**
- Workaround locale: `~/.claude/plugins/marketplaces/compass-marketplace/.claude-plugin/marketplace.json` patchato a string-form, backup in `marketplace.json.bak`. Re-add da path locale.
- Fix upstream: issue #7 + PR #8 aperti su `MasterDD-L34D/compass-marketplace`, branch `fix/marketplace-schema-source-string`, bump 0.4.2→0.4.3.
- Post-merge PR #8: eseguire `claude plugin marketplace update compass-marketplace` → pull v0.4.3 e rimuove necessità del workaround.
- Step 4 handoff (SessionStart hook auto-brief) non testato — richiede restart Claude Code in evo-swarm.
- Documentazione completa in `HANDOFF-COMPASS-INSTALL-2026-04-25.md` nel repo.
