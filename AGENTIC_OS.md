# AGENTIC_OS.md -- CodeMasterDD Personal Agentic OS (mappa)

> **Indice puro, zero authority nuova.** Ogni layer punta al documento/tool che GIA'
> governa quella funzione: l'OS e' la composizione dell'esistente (ADR-0044), non un
> sistema nuovo. Convenzione: i riferimenti a file del repo sono link markdown
> relativi (verificati da `scripts/tests/test_agentic_os_map.py`); i path fuori repo
> sono in backtick e NON verificabili dal test.
> ASCII-first (ADR-0021). Vale per entrambi i PC della flotta (Lenovo .10 + Ryzen .11).

## I 7 layer -> authority esistente

| # | Layer | Authority (dove vive) | Note |
|---|-------|----------------------|------|
| 1 | Kernel / dottrina | [ORCHESTRATION.md](ORCHESTRATION.md) + [ADR-0036](docs/adr/0036-unified-orchestration-doctrine.md) + [ADR-0037](docs/adr/0037-merge-autonomy-model.md) | hub-and-spoke, routing tree, verification gate, autonomy ladder R0->R2 |
| 2 | Routing modelli | [MODEL_ROUTING.md](MODEL_ROUTING.md) + agent `delegation-classifier` + llmfit (`C:\dev\tools\llmfit\LOCAL-LLM-STANDARD.md`) | 2 dimensioni: tier capacita' + constraint-count (ADR-0016) |
| 3 | Esecutori (processi) | [.claude/agents/README.md](.claude/agents/README.md) (16 attivi + 5 dormant) + skill globali (`~/.claude/skills/`) + wrapper Aider ([scripts/wrappers](scripts/wrappers)) + Jules ([docs/jules/JULES-GOVERNANCE-INDEX.md](docs/jules/JULES-GOVERNANCE-INDEX.md)) + Workflow tool | selezione SEMPRE via skill `agent-scanner` (anti shadow-duplicate, OD-007) |
| 4 | Memoria (stato) | auto-memory `~/.claude/projects/<proj>/memory/` + [COMPACT_CONTEXT.md](COMPACT_CONTEXT.md) + [JOURNAL.md](JOURNAL.md) + AA01 (`~/aa01/`, 41+ lessons) | **per-machine BY DESIGN**: [sync-claude-global.ps1](scripts/fleet/sync-claude-global.ps1) esclude `memory/` deliberatamente; pattern index+topic-file (MEMORY.md: caricati solo primi 200 righe / 25KB) |
| 5 | Scheduling | task Windows `jules-daily-digest` + cron R0 (vault coherence 6h + `playtest2-board-sync` weekly) + [journal-land.ps1](scripts/fleet/journal-land.ps1) | `/loop` e cron di sessione SCADONO a 7 giorni: durabile = Desktop scheduled task / Routines. Espansione act-layer = solo via earn-path governor ([spec](docs/superpowers/specs/2026-06-01-unified-fleet-governor-design.md)) |
| 6 | Apprendimento (self-maintenance) | AA01 inbox->lesson (protocollo ADR-0026 P4) + skill `continuous-learning-v2` + skill `consolidate-memory` + plugin compass (direction index) + skill `fleet-verify` | loop: sessione -> lesson L-NNN -> (promozione) skill/hook |
| 7 | Safety / governance | hook (commit-guard ADR-0011, ASCII ADR-0021, tdd-guard, journal-drift in [.claude/settings.json](.claude/settings.json)) + privacy guard (`~/.config/aider-privacy-whitelist.txt`) + keys (`~/.config/api-keys/keys.env`) + allow-glob permissions | principio verificato: CLAUDE.md = advisory, enforcement = SOLO hook (PreToolUse) |

## Boot di sessione (gia' operativo)

1. Ordine lettura in [CLAUDE.md](CLAUDE.md) (questo file e' lo step 1b).
2. Hook SessionStart automatici (marker, tdd-guard seed, compass mini-brief).
3. Skill `agent-scanner` in trigger BOOTSTRAP prima di ogni routing agent.

## Principi verificati (ricerca 2026-07-12, fonti in [report](docs/research/personal-agentic-os-2026-07-12.md))

- "Skill teaches the how, Hook enforces the rule, Subagent isolates the work."
- I subagent tornano SOLO summary al parent: composizione = file condivisi, non contesto condiviso.
- Multi-agente costa ~15x token di una chat: si orchestra solo task ad alto valore (gia' codificato nel cost ladder ORCHESTRATION.md sec 3).
- Memoria: indice conciso + topic file on-demand; "se lo rispiegheresti a un neoassunto, va in memoria persistente".
- CLAUDE.md <200 righe, procedure -> skill (gia' policy reorg 2026-06-03).

## Gap onesti / roadmap (tutti Eduardo-gated)

- **G1 heartbeat/morning-brief -- DONE 2026-07-12** (ratifica Eduardo): `scripts/fleet/morning-brief.ps1` (landa via PR #540) R0 report-only, task daily 08:30 su Lenovo, no-LLM, log locale gitignored.
- **G2 last30days sorgenti -- YouTube DONE, X pendente 1 azione Eduardo** (login x.com in Firefox; yt-dlp + Firefox installati 2026-07-12).
- **G3 continuous-learning-v2 -- NARROW GO 2026-07-12** (eval nel [report](docs/research/personal-agentic-os-2026-07-12.md)): observation gia' live (hook globali), analisi = ritual on-demand (observer Haiku via Agent tool + `instinct-cli.py status/prune`), observer background resta OFF; promotion instinct -> AA01/CLAUDE.md via curation umana.
- **Non-gap ratificati**: memoria per-machine (design, non bug); NESSUN framework orchestrazione esterno (ADR-0036 sec 8 anti-scope); NESSUN gateway LLM (OD-009).
