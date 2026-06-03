# CLAUDE.md — CodeMasterDD AI Station

<!-- Index + regole sempre-attive. Detail topic-specifico = on-demand via link.
     Authority: docs/adr/, MODEL_ROUTING.md, STATUS_MULTI_REPO.md, docs/reference/. Target <200 righe. -->

## Ruolo
Dev workstation AI agentic PRINCIPALE Eduardo. Autosufficiente per workflow dev + AI locali.
Piattaforma sovereign-first (locale-prioritario, no-lock-in, multi-provider). Pivot Hybrid A1
2026-05-18 (Pro+Meridian+free-tier ~$240-600/anno; target $0-50 SUPERSEDED). Vedi ADR-0030.
Questo repo = infra-as-code + observability + UI-glue; NON contiene codice progetti reali
(Game/Synesthesia vivono in repo separati).

## Lingua
Utente = italiano. Codice/identifier/commit message = inglese. Doc progetto = italiano.

## Convenzioni operative
- **Comandi**: uno alla volta, spiega prima, approvazione esplicita per azioni non-banali, no concatenazioni multiple.
- **File**: mostra contenuto prima di creare/modificare; preferisci Edit a Write su file esistenti.
- **Git**: Conventional Commits (feat/fix/chore/docs/refactor/test). No `--force` su main, no `--no-verify`. Branch = main.
- **Logging/backup**: `logs/` + `backup/` gitignored; `.env` gitignored (template `.env.example`).
- **Encoding**: ASCII-first body nuovi `.md` (em-dash -> `--`); em-dash OK solo titoli ADR. Enforcement: `~/.claude/rules/encoding.md` + hook pre-commit. Legacy mojibake = frozen.

## API keys (security)
Storage `~/.config/api-keys/keys.env` (ACL-locked edusc+SYSTEM). MAI in repo/registry/commit.
Provider: Groq/Cerebras/Gemini/OpenAI/Anthropic. Load bash: `set -a; source ~/.config/api-keys/keys.env; set +a`.
Detail -> memory `reference_api_keys` + ADR-0013.

## Stack (essenziale)
Git, Claude Code (OAuth Max, Opus), Node 24 LTS, Python 3.12, Ollama, Aider, OpenCode, Bun.
Lista esaustiva (versioni + tool + plugin) -> `docs/reference/stack-installed.md`.

## Capacita AI locali
RTX 5060 8GB: full-GPU fino 7-8B; 14B parziale (GPU+CPU spill); 30B MoE OK post-64GB-RAM.
Sweet-spot agentic = Qwen 2.5 Coder 14B Q2_K (faithful) / qwen3-coder:30b MoE (escalation).
Tabelle tok/s + bench mixed + swap-overhead -> `docs/reference/hardware-and-models.md` + `docs/research/bench-*`.
Batch task per-modello quando possibile (swap = ~42% overhead workflow misto).

## Priorita modelli / tier routing
- **Durante Claude Max (~fino 17/06/2026)**: Opus per tutto.
- **Post-Max tier 0 strategic** (non-delegabile: multi-file >=3, debug-arch, ADR, synthesis, constraint >=5):
  Claude API on-demand, budget cap $10-20/mese, tracking `logs/claude-api-spend-*`. ADR-0023.
- **Routing sovereign** (decision-summary; full -> `MODEL_ROUTING.md` + ADR-0008/0016/0022):
  - Query one-shot / read-explain / create-single -> Qwen 7B (114 tok/s).
  - Cosmetic edit -> `aider-cosmetic` (7B+diff). Behavior-critical -> `aider-refactor` (14B Q2+diff).
  - Escalation 14B-safe-fail -> `aider` + qwen3-coder:30b. Multi-step agentic tool-use -> `opencode run` 30B MoE.
  - Cloud free -> wrapper `aider-groq-bypass`/`aider-cerebras`/`aider-gemini` (privacy-guarded). Lista wrapper full -> MODEL_ROUTING.md.
  - **Seconda dimensione**: constraint-count (ADR-0016) -- 5+ strict -> manual Claude Code.
- **Safety Aider**: `git diff HEAD~1` post-edit; no `--yes-always` su tree sporco; guard rail hooks via `core.hooksPath`.

## Trigger delega in-session (SEMPRE attivo)
Prima di Edit/Write su file esistente, CLASSIFICA + proponi delega:
- **cosmetic** (JSDoc/docstring/rename/lint/typo) + tree clean -> proponi `aider-cosmetic`, attendi OK.
- **behavior-critical** (refactor/bugfix/logic 1-file) -> proponi `aider-refactor`, attendi OK.
- **strategic** (multi-file/synthesis/design/debug-arch/ADR) -> esegui diretto.
- <1 riga meccanica -> skip. Batch >=5 simili -> proponi delega anche se sub-threshold.
- Tracking -> `logs/aider-delegation-YYYY-MM.md`. Anti-pattern: default "faccio io" senza classify.

## Privacy guard rail
Wrapper cloud abortano se repo non in `~/.config/aider-privacy-whitelist.txt` (setup/verify: `scripts/setup/install-privacy-guard.ps1`).
Whitelisted (cloud OK): codemasterdd, Game, Game-Godot-v2. Sovereign-only: Synesthesia, repo cliente.

## Cognitive workflow protocols (ADR-0026 -- 7 trigger; full -> docs/adr/0026-cognitive-workflow-protocols.md)
Per audit/eval/decision/pivot significativo:
1. **Refresh-verify** (PRE-action obbligatorio): AA01 + memory + ADR + git/PR + filesystem prima di azione.
2. **Autoresearch** multi-source (necessario non sufficiente); mai one-shot README.
3. **Archon 7-step** first-principles per high-stakes irreversibile (+ CALIBRATE falsifying experiment).
4. **AA01 audit trail** per work >=30min cross-session (inbox->classify->promote->lesson->archive).
5. **Harsh-reviewer subagent** PRE-merge per cluster >=3 PR same-day o file security/governance-critical.
6. **Brainstorming skill** per ADR-class architectural generative (3 approcci + tradeoff pre-decision).
7. **SDMG**: metodo self-designed = ipotesi alto-errore; falsificazione esterna pre-integrazione governance.

## Repo monitorati (full -> STATUS_MULTI_REPO.md + memory project_multi_repo_overview)
- **Game** (Vue3 d20) `C:\dev\Game` -- gates AI-driven batch-sim (mai human/4-amici); Wave-3 design-data done. Public, cloud-OK.
- **Game-Godot-v2** `C:\dev\Game-Godot-v2` -- Godot 4.x port; self-governed (CLAUDE.md+AGENTS.md). Public.
- **Game-Database** `C:\dev\Game-Database` -- Express+Prisma+Postgres taxonomy CMS; Jules-maintained. Public.
- **Synesthesia** `C:\dev\synesthesia` -- web app UniUPO; dormant fino esame ago-2026. Mixed privacy (controllers/ sovereign).
- **Dafne swarm** `~/Dafne/workspace/swarm` -- orchestratore AI (Flask+Ollama); persona-entita; scrive Game/agents su approve.
- **vault** `C:\dev\vault` -- LLM-wiki Karpathy; sibling-peer sovereign-only; branch+PR OK, MAI merge/direct-main.
- **Boundary**: repo esterni = auth esplicita per write; branch+PR, merge Eduardo. Memory `feedback_external_repo_action_boundary`.

## JOURNAL (fine sessione significativa)
Entry in JOURNAL.md (YYYY-MM-DD newest-first: Completato/Da fare/Note). Poi land via helper (vale Lenovo+Ryzen):
`powershell -File scripts/fleet/journal-land.ps1 -Subject "docs(journal): <desc>"`.
MAI journal su branch `chore/`/`docs/` (resta orfano); MAI `git pull` su feature-branch (`--ff-only` solo su main).

## Ordine lettura nuove sessioni
1. CLAUDE.md (questo) 2. COMPACT_CONTEXT.md 3. STATUS_MULTI_REPO.md (se cross-repo) 3b. GOALS.md (se pianificazione)
4. `.claude/agents/README.md` (16 subagent attivi + 5 dormant in `_dormant/`) 5. Archivio_.../07 operating-rules 6. BACKLOG.md + OPEN_DECISIONS.md 7. ADR rilevanti.
Agent multi-client (Codex/OpenCode/sandbox) -> leggi AGENTS.md prima (ADR-0021). CLAUDE.md autoritativo per decisioni progetto;
regole 07 per pattern operativi generici. Framework governance: `Archivio_Libreria_Operativa_Progetti/`.
