# CLAUDE.md — CodeMasterDD AI Station

<!-- Index + regole sempre-attive. Detail topic-specifico = on-demand via link.
     Authority: docs/adr/, MODEL_ROUTING.md, STATUS_MULTI_REPO.md, docs/reference/. Target <200 righe. -->

## Ruolo
Dev workstation AI agentic PRINCIPALE Eduardo. Autosufficiente per workflow dev + AI locali.
Piattaforma sovereign-first (locale-prioritario, no-lock-in, multi-provider). Pivot Hybrid A1
2026-05-18 (Pro+Meridian+free-tier ~$240-600/anno; target $0-50 SUPERSEDED). Vedi ADR-0030. Oggi = piano di riserva: abbonamento Max attivo.
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

## Baseline / quality gates
- **Definition of Done**: una change e DONE solo con test/build verdi (output mostrato, no "sembra fatto") + zero TODO/stub/placeholder + doc/commit aggiornati + nessun self-merge che salta il review-gate. Vedi Quality Gate globale + protocollo `verification-before-completion`.
- **Testing**: prima di dire done -> `py -m pytest -q scripts/tests` (launcher `py`, NON `python`: user-PATH espone un venv hermes senza pytest; pytest `--import-mode=importlib`) + ASCII-guard ADR-0021 (la "lint" di questo repo infra/scripts, via hook pre-commit / CI). No typecheck (no TS). Preferisci test mirati > full-suite.
- **PR review (pre-merge, OBBLIGATORIO)**: leggi i commenti review (`gh api repos/<owner>/<repo>/pulls/<N>/comments`) + triage P1 (block, fix obbligatorio) / P2 (should) / P3 (nice). No silent-merge senza risolvere i P1.
- **Dependencies**: chiedi conferma prima di aggiungere una prod-dependency; niente version-bump/update senza approval esplicito; rispetta il lockfile (no edit manuale).

## API keys (security)
Storage `~/.config/api-keys/keys.env` (ACL-locked edusc+SYSTEM). MAI in repo/registry/commit.
Provider: Groq/Cerebras/Gemini/OpenAI/Anthropic. Load bash: `set -a; source ~/.config/api-keys/keys.env; set +a`.
Detail -> memory `reference_api_keys` + ADR-0013.

## Stack (essenziale)
Git, Claude Code (OAuth Max, Opus), Node 22 attivo (Game-canonical; +24.15.0 via nvm-windows, ADR-0003 addendum 2026-06-17 -- MAI `nvm use 24` per lavoro Game), Python 3.12, Ollama, Aider, OpenCode, Bun.
Lista esaustiva (versioni + tool + plugin) -> `docs/reference/stack-installed.md`.

## Capacita AI locali
Fleet 2 macchine: Ryzen (RTX 4070S 12GB, 31GB RAM) + Lenovo (RTX 5060 8GB, 64GB RAM). Dettaglio -> `MODEL_ROUTING.md`.
**Ruoli dei modelli locali = fonte esterna** (non copiare qui nomi o numeri): `C:\dev\codemasterdd-workspace\test-llm\INDICE-VALUTAZIONE-LLM.md`
+ riga Ruoli (sezione LLM locali) di `C:\dev\codemasterdd-workspace\user-config\REGOLE-COMUNI.md`. Modelli installati: solo `ollama list` sull'host.
SUPERATO (27/11/2026): lo sweet-spot "Qwen 2.5 Coder 14B Q2_K" -- famiglia qwen2.5 non piu' installata su nessun host.
Tabelle tok/s storiche + bench mixed + swap-overhead -> `docs/reference/hardware-and-models.md` + `docs/research/bench-*`.
Batch task per-modello quando possibile (swap = ~42% overhead workflow misto: misura storica su modelli rimossi).

## Priorita modelli / tier routing
- **Tier 0 strategic** (non-delegabile: multi-file >=3, debug-arch, ADR, synthesis, constraint >=5): Claude Code (abbonamento Max attivo).
  Piano di riserva se Max cessa: ADR-0030 (Pro) + ADR-0023 (Claude API on-demand, cap $10-20/mese, tracking `logs/claude-api-spend-*`).
- **Routing locale**: default locale solo dove il ruolo ha un riferimento o una promozione nelle fonti (vedi "Capacita AI locali"). Altri ruoli: nessun default locale; uso di prova libero e dichiarato, non default.
  - SUPERATO (27/11/2026): Qwen 7B per query one-shot; `aider-cosmetic` (qwen2.5-coder 7B); `aider-refactor` (qwen2.5-coder 14B Q2);
    escalation "14B safe-fail". I modelli non esistono piu' e i due wrapper puntano a tag rimossi.
  - Multi-step agentic tool-use: `opencode run` + `qwen3-coder:30b` (Lenovo, ADR-0022) = uso di prova libero e dichiarato, non default (il ruolo "tool" non ha locali promossi).
- **Routing cloud**:
  - Cloud free -> wrapper `aider-groq-bypass`/`aider-cerebras`/`aider-gemini` (privacy-guarded). Lista wrapper full -> MODEL_ROUTING.md.
- **Seconda dimensione**: constraint-count (ADR-0016) -- 5+ strict -> manual Claude Code.
- **Safety Aider**: `git diff HEAD~1` post-edit; no `--yes-always` su tree sporco; guard rail hooks via `core.hooksPath`.

## Trigger delega in-session (SEMPRE attivo)
Prima di Edit/Write su file esistente, CLASSIFICA + proponi delega:
- **cosmetic** / **behavior-critical**: SOSPESO dal 27/11/2026 -- `aider-cosmetic` e `aider-refactor` puntano a modelli rimossi.
  Non proporli finche' i wrapper non puntano a un modello installato con ruolo promosso. Classificare resta obbligatorio;
  delega solo verso cloud-free privacy-guarded, altrimenti esegui diretto.
- **strategic** (multi-file/synthesis/design/debug-arch/ADR) -> esegui diretto.
- <1 riga meccanica -> skip. Batch >=5 simili -> proponi delega (oggi solo cloud-free) anche se sub-threshold.
- Tracking -> `logs/aider-delegation-YYYY-MM.md`. Anti-pattern: "faccio io" senza classify (eseguire diretto DOPO aver classificato e' ok).

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
- **Game** (Evo-Tactics backend/sim/canon) `C:\dev\Game` -- Node backend + d20 sim + balance authority + canon (server cross-stack per Godot via HTTP/WS); gates AI-driven batch-sim (mai human/4-amici). Vue web frontend archiviato 2026-05-14 (cutover ADR-2026-05-05); repo NON archiviato (backend preservato by design). Public, cloud-OK.
- **Game-Godot-v2** `C:\dev\Game-Godot-v2` -- **frontend canonico** Evo-Tactics (cutover 2026-05; consuma Game backend); Godot 4.x, self-governed (CLAUDE.md+AGENTS.md). Public.
- **Game-Database** `C:\dev\Game-Database` -- Express+Prisma+Postgres taxonomy CMS; Jules-maintained. Public.
- **Synesthesia** `C:\dev\synesthesia` -- web app UniUPO; dormant fino esame ago-2026. Mixed privacy (controllers/ sovereign).
- **Dafne swarm** `~/Dafne/workspace/swarm` -- orchestratore AI (Flask+Ollama); persona-entita; scrive Game/agents su approve.
- **vault** `C:\dev\vault` -- LLM-wiki Karpathy; sibling-peer sovereign-only; branch+PR OK, MAI merge/direct-main.
- **Boundary**: repo esterni = auth esplicita per write; branch+PR, merge Eduardo. Memory `feedback_external_repo_action_boundary`.

## JOURNAL (fine sessione significativa)
Entry in JOURNAL.md (YYYY-MM-DD newest-first: Completato/Da fare/Note). Poi land via helper (vale Lenovo+Ryzen):
`powershell -File scripts/fleet/journal-land.ps1 -Subject "docs(journal): <desc>" -CodingAgent <model-id-sessione>`
(model-id = quello del proprio system prompt, es. `claude-fable-5`; omesso -> trailer generico `claude-code`).
MAI journal su branch `chore/`/`docs/` (resta orfano); MAI `git pull` su feature-branch (`--ff-only` solo su main).

## Ordine lettura nuove sessioni
1. CLAUDE.md (questo) 1b. AGENTIC_OS.md (mappa OS: layer -> authority) 2. COMPACT_CONTEXT.md 3. STATUS_MULTI_REPO.md (se cross-repo) 3b. GOALS.md (se pianificazione)
4. `.claude/agents/README.md` (19 subagent attivi + 5 dormant in `_dormant/`) 5. Archivio_.../07 operating-rules 6. BACKLOG.md + OPEN_DECISIONS.md 7. ADR rilevanti.
Agent multi-client (Codex/OpenCode/sandbox) -> leggi AGENTS.md prima (ADR-0021). CLAUDE.md autoritativo per decisioni progetto;
regole 07 per pattern operativi generici. Framework governance: `Archivio_Libreria_Operativa_Progetti/`.
