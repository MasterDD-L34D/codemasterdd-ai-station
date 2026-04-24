# Sources & attribution — agent design rationale

Questo documento traccia le fonti usate per progettare i 15 sub-agent in `.claude/agents/`. Trasparenza su ispirazione e licenze di riferimento.

## Fonti primarie

### 1. Archivio_Libreria_Operativa_Progetti (locale)

Framework prescrittivo multi-progetto importato 2026-04-23. 13 personas estratti + 4 framework operativi.

**Personas riutilizzati** (istanziati come agent parametrici):
- Project Architect + PM + Archivist → coverage via `adr-drafter` + policy hub agents
- Principal Engineer + Systems Architect → copertura implicita via Claude Code default
- AI Workflow Architect (routing) → `delegation-classifier`
- Game Systems Designer → `game-balance-auditor` + `game-design-validator`
- Systems Designer + Game QA → `game-balance-auditor`
- Product Designer Gameplay → `game-design-validator`
- First Principles Validator → `game-design-validator`
- Software Architect (Repo Mapper) → `database-schema-designer` (scope DB)
- Tech Lead + PM Tecnico → `adr-drafter` (scope decisioni)
- Security Auditor → `owasp-security-auditor`
- Research Analyst → implicito nei Claude Code default
- Strategic Decision Maker → implicito nel hub pattern
- **Harsh Reviewer → `harsh-reviewer`** (adozione diretta)

**Framework adottati**:
- Sequenza "Reference → Adattamento → Workflow → Output → Compact → Archivio" → applicato in `compact-conversation`
- Modalità operative toggle (`/INTAKE`, `/STRUCTURE`, `/PLAN`, etc.) → pattern multi-mode in molti agent
- First Principles Game Reconstruction → core di `game-design-validator`
- Multi-AI Routing → core di `delegation-classifier`

### 2. TikTok screenshots (drive-download-20260423T154054Z-3-001.zip, 30 immagini)

Eduardo ha fornito 30 screenshot TikTok con prompt AI e tecniche. Estratti e mappati:

#### @okaashish — "7 Hacks To Cut Claude's Token Usage By 80%" (10 slides)
- Hack #1 Caveman Method — filosofia applicata in `harsh-reviewer` (no filler, direct)
- Hack #2 Code Review Graph (github.com/tirth8205/code-review-graph) — non adottato (overlap con Claude Code codebase awareness)
- Hack #4 PDF via ChatGPT first — tecnica documentata, non agent
- Hack #5 Session Timing Trick — pattern non-agent
- Hack #6 "Compact" Skill → **`compact-conversation`** (adozione diretta)

#### Evolving AI @evolving.ai — "7 Hacks" dettagliati (9 slides)
- Hack #3 Opus/Sonnet/Haiku routing → principio applicato nel model tier dei nostri agent
- Hack #6 Compact Skill (versione più strutturata) → informato `compact-conversation`
- Hack #7 Peak Hours → pattern operativo, non agent

#### Blue Viper @blueviper.ai — "20 AI Prompts" (11 slides)
- #5 Database Designer → **`database-schema-designer`**
- #6 Security Auditor → **`owasp-security-auditor`** (esteso con OWASP Agentic Top 10)
- #17 Technical Interviewer → non adottato (non fit per workstation)
- #18 Career Strategist → non adottato (fuori scope)

#### The Shift @ai.theshift — tre serie
- **Slash Commands** (`/AUDIENCE`, `/TONE`, `/DEV`, `/PM`, `/SWOT`, `/FORMAT`, `/COMPARE`, `/MULTI-PERSPECTIVE`) — non adottati come agent (sono slash command Claude Code, già supportati nativamente)
- **Personas**: Brand Identity Strategist (non fit), UI/UX Systems Thinker → informato `a11y-wcag-reviewer` estensione, Design Ops + Figma (non fit, no Figma)
- **Weaponized prompts**: IQ score, "Obviously" trap, Fake constraint, Fake audience → tecniche documentate inline in `harsh-reviewer` guardrail (no padding)

#### Roman.Knox / knoxhub.io/hub — "Claude-Cowork" framework (12 slides)
- Folders About Me / Projects / Templates / Claude Outputs → non adottato (conflicts con scope repo codemasterdd; noi usiamo memory system + governance files)
- Master template "Stop Writing Prompts" → informato pattern system prompt modulare
- "Let Claude Prompt You" (AskUserQuestion) → pattern adottato nei mode 1/2/3 multi-agent
- Install One Plugin → non adottato (preferiamo `.claude/agents/` versioned nel repo, non plugin marketplace)
- Connectors (Google/Notion/Slack) → non adottato (sovereign preference, ADR-0001)

#### Drew Huibregtse @drewskidigital — AI Art for coloring books (9 slides)
- Non adottato (fuori scope — Eduardo non produce coloring books)

### 3. Research web esterna (subagent 2026-04-24)

Query: "awesome-claude-code-agents", security/database/ui/game/swarm-specific agents.

**Top collections identificate** (licenza permissiva):
- **wshobson/agents** (MIT, 34.2k stars, 184 agent) — reference canonical, cherry-pick pattern
- **VoltAgent/awesome-claude-code-subagents** (MIT, 18.1k, 131 agent) — installer selettivo + quality-security dir
- **0xfurai/claude-code-subagents** (MIT, ~855 stars, 100+ agent) — verticale DB (Prisma/SQLAlchemy/Drizzle)

**Fonti specifiche riutilizzate**:
- `dl-ezo fork database-schema-designer` → informa `database-schema-designer`
- `agamm/claude-code-owasp` skill → base per `owasp-security-auditor`
- `TarkinLarson/asvs-auditor` → evidence-backed pattern per `owasp-security-auditor`
- `Community-Access/accessibility-agents` (WCAG 2.2 AA) → base per `a11y-wcag-reviewer`
- `Donchitos/Claude-Code-Game-Studios/balance-check` → informa `game-balance-auditor`
- Game Design Framework skill (mcpmarket) — Numbers Policy + 5-Component Filter → adottato in `game-balance-auditor`
- `jayminwest/overstory` tiered watchdog → pattern per `swarm-cycle-analyzer`

**Fonti NON adottate (con rationale)**:
- `hesreallyhim/awesome-claude-code` — licenza CC BY-NC-ND (no derivatives), usabile solo come indice
- `ruvnet/ruflo` (ex claude-flow) — overhead marketing, pattern "agent Olympics" non fit per solo-dev
- D&D Dungeon Master skills — play-oriented non design, skip per Evo-Tactics
- OpenHands — Windows richiede WSL+Docker, viola "zero-overhead Windows-native"

## Licenze

Tutti gli agent nostri sono scritti da zero (non copiati verbatim). Hanno licenza del repo codemasterdd (private repository Eduardo).

**Pattern ispirati da**:
- MIT licensed sources: riutilizzo liberamente pattern strutturali
- Apache 2.0 sources: idem
- CC BY-NC-ND (awesome-claude-code): usato solo come link-aware directory
- CLAUDE.md anthropic.com: public docs, pattern OK

## Changelog

**2026-04-24 (auto-mode maratona)**:
- Creati 5 agent iniziali (dogfood-analyst, bench-reporter, cost-monitor, repo-health-auditor, adr-drafter) via ADR-0017 Phase 4
- Estesa Dafne monitoring integration via `swarm-cycle-analyzer`

**2026-04-24 (auto-mode maratona continuata con TikTok sources)**:
- Aggiunti 10 agent nuovi: game-balance-auditor, game-design-validator, lore-consistency-checker, privacy-policy-enforcer, a11y-wcag-reviewer, owasp-security-auditor, database-schema-designer, swarm-cycle-analyzer (upgrade), delegation-classifier, harsh-reviewer, compact-conversation
- **Totale 15 agent** registrati

## Next evolution (tracked in BACKLOG)

Se in futuro emerge necessità, candidati validi da research:
- **release-notes-writer**: genera from git log + ADR accepted
- **monorepo-boundary-guardian**: cross-language Game Node+Python (wshobson derived)
- **memory-consolidator-wrapper**: invoca skill anthropic consolidate-memory
- **bench-post-upgrade-runner**: automatizza pattern da bench-post-ram-upgrade-2026-04-22

Attualmente non urgenti — 15 agent copre i gap identificati.
