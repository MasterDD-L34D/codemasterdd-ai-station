# Context-Files Reorg Fase 1 — Implementation Plan

> **Status (2026-06-23):** shipped -- context reorg Fasi 1-6 complete

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline) or
> superpowers:subagent-driven-development to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Snellire `~/.claude/CLAUDE.md` (435->~72 righe) + `codemasterdd/CLAUDE.md` (569->~150 righe)
spostando il detail on-demand in reference/rules/authority-file, senza perdere contenuto, riducendo
il carico sempre-attivo da ~25k a ~6-8k token/sessione.

**Architecture:** Approccio "index + moduli on-demand" (spec 2026-06-03). Due track: (A) non-git in
`~/.claude/` Lenovo-local con backup `.bak`; (B) git in worktree-isolato del repo codemasterdd ->
branch + PR + auto-merge. Verify-no-loss PRIMA di ogni taglio.

**Tech Stack:** Markdown, Git (worktree), PowerShell (verifica line-count + grep no-loss), Claude Code
`.claude/rules/` path-scoped + `~/.claude/reference/` on-demand.

**Spec:** `docs/superpowers/specs/2026-06-03-context-files-governance-reorg-design.md`

---

## File Structure (Fase 1)

**Track A — non-git (`~/.claude/`, Lenovo-local, edit+backup):**
- Backup: `~/.claude/CLAUDE.md.bak-2026-06-03` (NEW, safety)
- Modify: `~/.claude/CLAUDE.md` (435 -> ~72 righe; contenuto verbatim Task 4)
- Create: `~/.claude/reference/anti-patterns.md` (catalogo 19 full, copia 1:1 dal global attuale)
- Create: `~/.claude/rules/encoding.md` (policy ASCII path-scoped)

**Track B — git (repo codemasterdd, worktree):**
- Modify: `CLAUDE.md` (project, 569 -> ~150 righe; contenuto verbatim Task 7)
- Create: `docs/reference/stack-installed.md` (estratto verbatim sezioni stack)
- Create: `docs/reference/hardware-and-models.md` (estratto verbatim hardware+bench+modelli)
- Modify: `REFERENCE_INDEX.md` (linka i 2 reference doc nuovi)
- Already authored: spec + this plan (commit nel branch)

**Responsabilita per file:**
- `~/.claude/CLAUDE.md` = index globale cross-progetto + regole sempre-attive.
- `~/.claude/reference/anti-patterns.md` = catalogo lezioni completo (on-demand).
- `~/.claude/rules/encoding.md` = policy encoding, carica solo su edit file matchanti.
- `codemasterdd/CLAUDE.md` = index progetto + routing + protocolli-trigger + repo-list.
- `docs/reference/stack-installed.md` = inventario tool/versioni esaustivo.
- `docs/reference/hardware-and-models.md` = HW + tabelle bench + modelli Ollama.

---

## Task 1: Setup worktree-isolato + branch + migra spec/plan

**Files:**
- Worktree: nuovo, off `main`, branch `claude/context-files-reorg-2026-06-03`
- Migrate into worktree: spec + this plan

- [ ] **Step 1: Crea worktree isolato** (REQUIRED SUB-SKILL: superpowers:using-git-worktrees)

Motivo: shared-clone Lenovo concurrency (memory `shared-clone-session-concurrency`) -> evita
HEAD-switch nel checkout condiviso. Branch: `claude/context-files-reorg-2026-06-03`.

- [ ] **Step 2: Porta spec + plan nel worktree**

Lo spec e il plan sono stati scritti nel checkout main (uncommitted). Nel worktree:
copia/riscrivi `docs/superpowers/specs/2026-06-03-context-files-governance-reorg-design.md` e
`docs/superpowers/plans/2026-06-03-context-files-reorg-fase1.md` (contenuto identico).

- [ ] **Step 3: Commit iniziale**

```
git add docs/superpowers/specs/2026-06-03-context-files-governance-reorg-design.md docs/superpowers/plans/2026-06-03-context-files-reorg-fase1.md
git commit
```
Message (Conventional + ADR-0011 trailer):
```
docs(governance): spec+plan context-files reorg Fase 1

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
```
- [ ] **Step 4: Cleanup checkout main**

Rimuovi le copie uncommitted di spec/plan dal checkout main (ora vivono nel branch).
Verify: `git -C <main-checkout> status` -> niente untracked spec/plan residui.

---

## Task 2: [Track A] Backup global + crea reference/anti-patterns.md

**Files:**
- Create: `~/.claude/CLAUDE.md.bak-2026-06-03`
- Create: `~/.claude/reference/anti-patterns.md`

- [ ] **Step 1: Backup del global attuale**

```powershell
Copy-Item "C:\Users\edusc\.claude\CLAUDE.md" "C:\Users\edusc\.claude\CLAUDE.md.bak-2026-06-03"
```
Verify: `Test-Path "C:\Users\edusc\.claude\CLAUDE.md.bak-2026-06-03"` -> True.

- [ ] **Step 2: Crea dir reference + estrai catalogo anti-pattern**

```powershell
New-Item -ItemType Directory -Force "C:\Users\edusc\.claude\reference" | Out-Null
```
Crea `~/.claude/reference/anti-patterns.md`. Contenuto = copia **verbatim 1:1** della sezione
"## Anti-Pattern Catalogue (session learnings)" del global CLAUDE.md attuale (tutti i 19 entry
#1-#19, completi, incluso il grounding sorgentato #6 e tutti i Rif). Header del nuovo file:

```markdown
# Anti-Pattern Catalogue (session learnings)

<!-- Spostato da ~/.claude/CLAUDE.md 2026-06-03 (context-files reorg Fase 1).
     On-demand reference. Catalogo completo; lezioni #8+ anche in ~/aa01/learnings/L-*.md. -->

[... 19 entry verbatim dal global attuale ...]
```

- [ ] **Step 3: Verify no-loss (grep marker chiave)**

```powershell
$f = "C:\Users\edusc\.claude\reference\anti-patterns.md"
@("Subprocess cold-load","Stdout buffered","trailing space","MinerU","Force push to default","Shallow-research ADOPT","DRY-RUN smoke","LOBBY_WS_PORT","lucky-sample","Stale tracker") | ForEach-Object { if (Select-String -Path $f -SimpleMatch $_ -Quiet) { "OK: $_" } else { "MISSING: $_" } }
```
Expected: 10x "OK" (copre #1,#2,#3,#4,#7,#8,#9,#16,#14,#19). Se un MISSING -> STOP, non tagliare dal global.

---

## Task 3: [Track A] Crea rules/encoding.md (path-scoped)

**Files:**
- Create: `~/.claude/rules/encoding.md`

- [ ] **Step 1: Crea dir rules + file**

```powershell
New-Item -ItemType Directory -Force "C:\Users\edusc\.claude\rules" | Out-Null
```
Contenuto `~/.claude/rules/encoding.md`:

```markdown
---
paths:
  - "**/*.md"
  - "**/*.ps1"
  - "**/*.sh"
  - "**/*.py"
  - "**/*.js"
  - "**/*.json"
  - "**/*.yaml"
  - "**/*.yml"
  - "**/*.bat"
  - "**/*.cmd"
---

# Encoding policy (ADR-0021)

Quando crei/modifichi questi file:

- **ASCII-first** nel body prose dei nuovi `.md`.
- **Evita**: em-dash, middot, smart quotes. Usa `--`, `|`, `'`, `"`.
- **Consentiti**: emoji status, simboli matematici (>=, <=, ->) se semanticamente rilevanti.
- **Eccezione**: titoli ADR (`# ADR-NNNN -- Title`) mantengono em-dash (coerenza 20+ ADR).
- **Script** (.ps1/.sh/.py/.js): NO non-ASCII in string literals (mojibake cross-shell
  PS5.1/Bash/SSH). Marker bypass: `# encoding-non-ascii-ok: <reason>`.
- Hard-enforcement: hook pre-commit globale blocca non-ASCII su file nuovi/modificati.
- Legacy mojibake: frozen, no rewrite cieco; fix mirato solo se confusing per task corrente.

Ref: ADR-0021 + anti-pattern #12 (`~/.claude/reference/anti-patterns.md`).
```

- [ ] **Step 2: Verify**

```powershell
Test-Path "C:\Users\edusc\.claude\rules\encoding.md"
```
Expected: True. (Behavior-load verificato in Task 9 via `/memory`.)

---

## Task 4: [Track A] Slim global CLAUDE.md

**Files:**
- Modify: `~/.claude/CLAUDE.md` (sovrascrivi con contenuto slim approvato)

- [ ] **Step 1: Sovrascrivi con il contenuto slim (approvato 2026-06-03)**

Contenuto integrale (verbatim approvato in brainstorming):

```markdown
# Global CLAUDE.md — Eduardo (MasterDD-L34D)

<!-- Index + regole sempre-attive. Detail topic-specifico = on-demand via link (NON inline).
     Authority file citati = SoT. Target <200 righe (Anthropic memory best-practice). -->

## Fleet (2 macchine, profili opposti)
- **Lenovo** `CodeMasterDD` / `edusc` / `<hub-ip>` -- AI-hub, Ollama primario, keys.env. 64GB RAM / RTX 5060 8GB VRAM (RAM-rich). Canonical host.
- **Ryzen** `DESKTOP-T77TMKT` / `Vgit` / `<ryzen-ip>` -- inference-2nd. 31GB RAM / RTX 4070S 12GB VRAM (VRAM-rich).
- **PRE azione cross-PC** (deploy/SSH/AA01-write/lesson-promote): verifica identita ->
  `powershell -NoProfile -Command "Write-Output ('PC=' + $env:COMPUTERNAME + ' USER=' + $env:USERNAME)"`.
  Mismatch -> STOP + re-verify. Cross-PC action authoring = dal PC che possiede il canonical, o SSH read-only verify. Wife-PC `.37`/`.130` = SSH-PENDING.
- SSH bidirezionale Ryzen<->Lenovo WORKING. Read-ops = libero; mutating-remote = gated-ma-noto.
  Gotcha: account-admin -> sshd legge SOLO `C:\ProgramData\ssh\administrators_authorized_keys`.
  SoT completo: codemasterdd `docs/runbook/ssh-inbound-fleet-setup.md`.

## LLM locali -- routing
- **Authority** (consulta, NON scegliere a occhio): cross-machine `C:\dev\tools\llmfit\LOCAL-LLM-STANDARD.md`;
  per-machine `ryzen-llm-fit.json` (Ryzen) / `~/llmfit-lenovo-*.json` (Lenovo).
- Rapido: dense <=14B in-VRAM -> Ryzen. MoE/grandi/offload -> Lenovo. small-instruct judgment -> macchina piu scarica.
- Lenovo 8GB VRAM: modelli >9GB = heavy RAM-offload = lento; routine sovereign .10 -> `mistral:latest` / `qwen3:8b`.
- **Caveat load-bearing**: llmfit dice "cosa gira bene sul HW", NON "quale fa meglio il MIO task".
  Pipeline 2-stage: llmfit = shortlist -> task-eval N-sample sul prompt reale (anti lucky-sample).

## Quality Gate -- release standard (ogni agent / skill / feature)
3 step prima di production: **(1) Smoke** verde happy-path + output verificabile documentato.
**(2) Ricerca** >=3 edge case + comportamenti inattesi flaggati. **(3) Tuning** >=1 iterazione + metrica delta before/after.
No "ship and pray". Gate salta -> resta in `wip/`/`draft/`. Production = file `QUALITY.md` con 3 step + evidenze.
Report ricerca -> `docs/research/<componente>-<date>.md`. Override "done" concreti nel CLAUDE.md di progetto.

## Commit attribution (ADR-0011, non-negoziabile, identico ogni repo/PC)
- **VIETATO** trailer `Co-Authored-By:`. **OBBLIGATORIO** su commit agent-generati:
  `Coding-Agent: <agent-id>` + `Trace-Id: <uuidv7>`.
- Enforcement 2-layer: `commit-guard.js` PreToolUse + global `commit-msg` hook.
  Authority: codemasterdd `docs/adr/0011-cross-agent-commit-governance.md` §Addendum 2026-05-17.

## Agent-scanner (anti-shadow-duplicate -- STRONG-PURE, no eccezioni)
PRIMA di selezionare / raccomandare / creare un subagent / skill / agent -> invoca skill `agent-scanner`.
Trigger: BOOTSTRAP (nuova sessione progetto) / TEAM_FORMATION (pre-creazione) / DELTA (inizio sessione) / ON_DEMAND.
Build-on-existing, never recreate. Fires anche su task meccanici (no bypass via "triviality"). Ref: OD-007.

## Background task (>5min ETA)
Flush stdout per-linea + progress ogni N items + checkpoint file (resume idempotente) + log persistente
`Extras/ollama-runs/<date>-<task>.log`.

## Lessons / anti-pattern
Catalogo completo (19+ pattern) = `~/.claude/reference/anti-patterns.md` + `~/aa01/learnings/L-*.md` (37 lezioni).
**Consulta prima di**: tool adoption, script idempotent-write, optimizer/calibration, bot-rewrite/merge, PDF-heavy, atomize.
Guardrail sempre-attivi (distillati, i piu universali):
- **Force-push a main**: MAI senza consent-string esplicito ("autorizzo force push"). Lavoro perso = definitivo.
- **Ground-truth > surface**: issue-state / git-blame / source > PR-list / agent-report / tracker-marker.
  Verifica PRIMA di dire "done"; marker BACKLOG/OD = ipotesi, git = verita (Currency Gate).
- **N-sample**: no upgrade-claim metrica da N=10 se CI95 spanna band-ceiling. N=10 = direction-probe -> N=40 = ratify.
- **SDMG**: un metodo che ho progettato IO = ipotesi alto-errore, non decisione. Pre-integrazione governance:
  falsificazione esterna (harsh-reviewer + Archon), adozione narrow read-only/flag, decider = specialista non euristico.
- **Encoding**: ASCII-first body nuovi doc (em-dash -> `--`). Enforcement path-scoped: `.claude/rules/encoding.md`.
```

- [ ] **Step 2: Verify line-count + no-loss pointer**

```powershell
$g = "C:\Users\edusc\.claude\CLAUDE.md"
"lines: " + (Get-Content $g).Count
@("LOCAL-LLM-STANDARD","ssh-inbound-fleet-setup","anti-patterns.md","0011-cross-agent","agent-scanner","autorizzo force push") | ForEach-Object { if (Select-String -Path $g -SimpleMatch $_ -Quiet) { "OK: $_" } else { "MISSING: $_" } }
```
Expected: lines <= 80; 6x "OK" (tutti i pointer presenti).

---

## Task 5: [Track B] Crea docs/reference/stack-installed.md

**Files:**
- Create: `docs/reference/stack-installed.md`

- [ ] **Step 1: Crea dir + estrai inventario stack**

Crea `docs/reference/stack-installed.md`. Contenuto = copia **verbatim** delle sezioni del
project CLAUDE.md attuale: "## Stack installato" (completa, tutti i tool + versioni + plugin +
modelli locali list) + "## Stack da installare questa settimana" + "## Stack da installare
settimana prossima". Header:

```markdown
# Stack installato — CodeMasterDD AI Station

<!-- Spostato da CLAUDE.md 2026-06-03 (context-files reorg Fase 1). On-demand reference.
     Verifica runtime: `ollama list`, `<tool> --version`. -->

[... sezioni Stack installato + Stack da installare verbatim ...]
```

- [ ] **Step 2: Verify no-loss**

```powershell
$f = "docs\reference\stack-installed.md"
@("Aider 0.86","superpowers v5","claude-mem","repomix","Gemini CLI","faster-whisper","Bun v1.3","opencode-with-claude") | ForEach-Object { if (Select-String -Path $f -SimpleMatch $_ -Quiet) { "OK: $_" } else { "MISSING: $_" } }
```
Expected: 8x "OK".

---

## Task 6: [Track B] Crea docs/reference/hardware-and-models.md

**Files:**
- Create: `docs/reference/hardware-and-models.md`

- [ ] **Step 1: Estrai hardware + bench + modelli**

Crea `docs/reference/hardware-and-models.md`. Contenuto = copia **verbatim** delle sezioni del
project CLAUDE.md attuale: "## Hardware (definitivo)" + "## Capacita AI locali (Lenovo da solo)"
(incluse tutte le tabelle tok/s isolato/mixed/swap) + la lista dettagliata "Modelli locali"
(dentro Stack installato -- la parte modelli Ollama con digest/quant/tier). Header:

```markdown
# Hardware + modelli locali — CodeMasterDD AI Station

<!-- Spostato da CLAUDE.md 2026-06-03 (context-files reorg Fase 1). On-demand reference.
     Tabelle tok/s misurate (vedi docs/research/bench-* per metodologia). -->

[... Hardware + Capacita AI + tabelle bench + modelli Ollama verbatim ...]
```

- [ ] **Step 2: Verify no-loss**

```powershell
$f = "docs\reference\hardware-and-models.md"
@("RTX 5060","Ultra 7 255HX","64GB DDR5","qwen2.5-coder:7b","qwen3-coder:30b","deepseek-r1:8b","gpt-oss:120b","mixed-workload") | ForEach-Object { if (Select-String -Path $f -SimpleMatch $_ -Quiet) { "OK: $_" } else { "MISSING: $_" } }
```
Expected: 8x "OK".

---

## Task 7: [Track B] Slim project CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` (project root)

- [ ] **Step 1: Sovrascrivi con contenuto slim**

```markdown
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

## Privacy guard rail (H8, ADR-0019/0023)
Wrapper cloud abortano se repo non in `~/.config/aider-privacy-whitelist.txt`.
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
4. `.claude/agents/README.md` (18 subagent) 5. Archivio_.../07 operating-rules 6. BACKLOG.md + OPEN_DECISIONS.md 7. ADR rilevanti.
Agent multi-client (Codex/OpenCode/sandbox) -> leggi AGENTS.md prima (ADR-0021). CLAUDE.md autoritativo per decisioni progetto;
regole 07 per pattern operativi generici. Framework governance: `Archivio_Libreria_Operativa_Progetti/`.
```

- [ ] **Step 2: Verify line-count + no-loss pointer**

```powershell
$p = "CLAUDE.md"
"lines: " + (Get-Content $p).Count
@("docs/reference/stack-installed","docs/reference/hardware-and-models","MODEL_ROUTING.md","0026-cognitive","STATUS_MULTI_REPO.md","aider-privacy-whitelist","journal-land.ps1","keys.env") | ForEach-Object { if (Select-String -Path $p -SimpleMatch $_ -Quiet) { "OK: $_" } else { "MISSING: $_" } }
```
Expected: lines <= 160; 8x "OK".

---

## Task 8: [Track B] Aggiorna REFERENCE_INDEX.md

**Files:**
- Modify: `REFERENCE_INDEX.md`

- [ ] **Step 1: Aggiungi link ai 2 reference doc nuovi**

Aggiungi una sezione/voce in `REFERENCE_INDEX.md` che linka:
- `docs/reference/stack-installed.md` -- inventario stack esaustivo (spostato da CLAUDE.md)
- `docs/reference/hardware-and-models.md` -- hardware + bench + modelli (spostato da CLAUDE.md)

Usa Edit (file esistente). Match lo stile delle voci esistenti.

- [ ] **Step 2: Verify**

```powershell
@("stack-installed","hardware-and-models") | ForEach-Object { if (Select-String -Path "REFERENCE_INDEX.md" -SimpleMatch $_ -Quiet) { "OK: $_" } else { "MISSING: $_" } }
```
Expected: 2x "OK".

---

## Task 9: Verifica finale (no-loss + counts + behavior)

- [ ] **Step 1: Line-count gate entrambi i CLAUDE.md**

```powershell
"global: " + (Get-Content "C:\Users\edusc\.claude\CLAUDE.md").Count + " (target <=80)"
"project: " + (Get-Content "CLAUDE.md").Count + " (target <=160)"
```
Expected: global <=80, project <=160. Se sfora -> rivedi.

- [ ] **Step 2: Behavior smoke (QG Step-1)** -- nuova sessione o /clear, poi chiedere:
  (a) "qual e la policy encoding?" -> deve citare ASCII-first / rules/encoding.md.
  (b) "dove sono gli anti-pattern completi?" -> deve citare ~/.claude/reference/anti-patterns.md.
  (c) "regola force-push su main?" -> deve citare consent-string esplicito.
  (d) "che modelli Ollama ho?" -> deve puntare a docs/reference/hardware-and-models.md / `ollama list`.
  Pass = risponde corretto usando i pointer (on-demand recall funziona).

- [ ] **Step 3: Rules-load check**

In sessione, apri un `.md` qualunque -> `/memory` deve elencare `encoding.md` tra i loaded rules.

- [ ] **Step 4: Token-budget delta documentato**

Stima before/after (~25k -> target ~6-8k sempre-caricato). Annota nel PR body.

---

## Task 10: PR + auto-merge + flag Ryzen deploy

- [ ] **Step 1: Commit Track B nel branch**

```
git add CLAUDE.md docs/reference/stack-installed.md docs/reference/hardware-and-models.md REFERENCE_INDEX.md
git commit
```
Message:
```
docs(governance): slim project CLAUDE.md + extract reference docs (Fase 1)

569->~150 lines. Stack/hardware/bench moved to docs/reference/ (on-demand).
Spec: docs/superpowers/specs/2026-06-03-context-files-governance-reorg-design.md

Coding-Agent: claude-opus-4-8
Trace-Id: <uuidv7>
```

- [ ] **Step 2: Push + PR**

```
git push -u origin claude/context-files-reorg-2026-06-03
gh pr create --fill --base main
```
PR body: include before/after counts (global+project), no-loss checklist results, behavior-smoke
results, "Cognitive protocols applied: brainstorming Y, harsh-reviewer <Y/N>".

- [ ] **Step 3: Auto-merge (autorizzato R2) dopo verifica verde**

Solo se Task 9 tutto verde:
```
gh pr merge --squash --delete-branch
```
Poi rimuovi worktree (using-git-worktrees cleanup).

- [ ] **Step 4: Flag Ryzen deploy follow-up**

Il global `~/.claude/CLAUDE.md` e Lenovo-local. Per parita fleet, deploy su Ryzen via il
meccanismo esistente (es. `deploy_claude_global.ps1` se presente, o scp+verify). NON eseguito in
questa sessione -- annota come follow-up esplicito a Eduardo (anti-pattern #9: idempotent-write
deploy = test -Apply su target reale, verify artefatto). Track A (reference/rules) idem se serve parita.

---

## Self-Review (writing-plans gate)

**1. Spec coverage:**
- Standard/rubrica -> applicata in Task 4/7 (comandi diretti, <200 righe, pointer on-demand). OK.
- Metodologia safe-slim (audit/verify-no-loss/riloca/measure) -> Task 2-9 (grep no-loss PRIMA del taglio). OK.
- Fase 1 design 1a (global) -> Task 4. 1b (project) -> Task 7. 1c (file nuovi) -> Task 2/3/5/6. OK.
- R1 docs/reference/ -> Task 5/6/8. R2 branch+PR+auto-merge -> Task 1/10. R3 piano-scritto -> questo doc. R4 split+Ryzen-flag -> Track A/B + Task 10 Step4. OK.
- Verifica no-loss + behavior + rollback -> Task 9 + backup Task 2. OK.

**2. Placeholder scan:** I `<uuidv7>` sono token-da-generare a commit-time (non placeholder di
contenuto). I "[... verbatim ...]" in Task 2/5/6 = istruzione di copia-esatta da sorgente nota
(il CLAUDE.md attuale), source deterministica -- NON placeholder. Contenuto autorato (global slim
Task 4, project slim Task 7) = completo inline. OK.

**3. Type/naming consistency:** path `docs/reference/stack-installed.md` +
`docs/reference/hardware-and-models.md` + `~/.claude/reference/anti-patterns.md` +
`~/.claude/rules/encoding.md` coerenti tra File-Structure, task, e i pointer dentro i CLAUDE.md slim. Branch
`claude/context-files-reorg-2026-06-03` coerente Task 1/10. OK.

**Note:** lavoro doc-refactor (non TDD-code); "test" = line-count gate + grep no-loss + behavior smoke.
Ordine sicuro: reference/rules creati e verificati PRIMA di tagliare dai CLAUDE.md (no-loss garantito).
