# ADR-0032 -- Jules-PR governance: unified active model across monitored repos

> *TL;DR: Riconcilia una divergenza cross-sessione non formalizzata. Sessione conversazionale 2026-05-16/17 (Lenovo) ha costruito ed empiricamente validato un modello ATTIVO per i PR Jules su codemasterdd (triage -> ground-truth verify -> sendMessage correttivo alle sessioni Jules L-030 -> fix sovereign dei residui -> merge/close batch con auth esplicita Eduardo). Sessione Ryzen 2026-05-17 ha committato in parallelo l'agent `jules-pr-triager` con stance read-only-puro (solo triage, Eduardo fa tutto) per Game. Decisione master-dd: adottare il **Modello 3 -- modello attivo pieno su TUTTI i repo monitorati, Game incluso (esterno)**. Il gate merge/close resta Eduardo-only explicit (SPOF oversight invariato, come pattern vault-shared L-012). Cambia: estensione write-to-repo (commit + branch push per fix sovereign) a Game per scope Jules-PR-remediation; canale sendMessage correttivo repo-agnostico autorizzato ovunque. `jules-pr-triager.md` riconciliato come strumento-di-triage dentro il workflow attivo, non policy autonoma. Status Proposed; ratification: OK esplicito Eduardo + primo ciclo Model-3 su Game senza incidente boundary.*

- **Status**: **Proposed** (2026-05-17 pre-ratification)
- **Data**: 2026-05-17
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

## Context and Problem Statement

Due sessioni Claude su macchine diverse hanno prodotto, in parallelo e senza riconciliazione, due modelli di governance divergenti per i PR aperti dall'agent autonomo Jules (`google-labs-jules[bot]`, lanciato manualmente da Eduardo via jules.google):

- **Modello A (attivo)** -- costruito e validato empiricamente nella sessione conversazionale Lenovo 2026-05-16/17 sul repo `codemasterdd-ai-station` (repo proprio):
  1. triage cluster (harsh-reviewer subagent)
  2. ground-truth verify dei claim agente (L-029/L-025: API/diff reale > affermazione)
  3. `sendMessage` correttivo alle sessioni Jules via Jules API con evidenza file:line (L-030 -- Jules scope-adjusta la PR, non termina; validato n=3/4)
  4. chiusura loop review-bot (Codex) via commenti PR
  5. fix sovereign dei residui che Jules non puo' chiudere (Aider locale / merge manuale)
  6. merge/close batch con autorizzazione esplicita per-batch di Eduardo
  Risultato: 15/16 PR cluster integrate, 2 P0 sicurezza + 1 Codex-P1 risolti, 0 regressioni.

- **Modello B (read-only)** -- agent `.claude/agents/jules-pr-triager.md` committato dalla sessione Ryzen 2026-05-17 (#153 + policy #156) per `MasterDD-L34D/Game` (repo esterno monitorato): solo triage read-only -> tabella verdetti + batch consigliato. Esplicitamente: "MAI gh pr merge/close", "non commentare sui PR", "Read-only puro". Eduardo esegue ogni azione manualmente.

I due non sono contraddittori in linea di principio (stesso principio, tier-boundary diversi: `codemasterdd` proprio vs `Game` esterno -- cfr. memory `feedback_external_repo_action_boundary`). Ma il Modello B e' **incompleto**: ignora del tutto il canale `sendMessage` correttivo (che e' repo-agnostico -- parla alle sessioni Jules, non scrive sul repo) e il tier "fix sovereign", entrambi validati empiricamente. La capacita' sendMessage e' gia' stata abilitata stabilmente (regola `autoMode.allow` in `~/.claude/settings.json`). Senza riconciliazione formale, sessioni/macchine diverse continueranno a divergere (anti-pattern gia' osservato: narrative drift cross-sessione, cfr. L-002).

Trigger della decisione: triage 2026-05-17 su Game ha rilevato **32 PR Jules aperti** (0 MERGE-OK, 13 CLOSE, 19 NEEDS-REVIEW, 44% rumore -- no-op + artifact-pollution), structural lever scattato. Volume e qualita' dei residui rendono il modello passivo (Eduardo fa tutto a mano) operativamente insostenibile.

## Decision

Adottare il **Modello 3 -- modello attivo pieno, unificato su tutti i repo monitorati, Game (esterno) incluso**.

Workflow canonico per i PR Jules su qualsiasi repo monitorato (codemasterdd, Game, Game-Godot-v2, Game-Database, e futuri):

1. **Triage** -- `jules-pr-triager` (Game) / harsh-reviewer (codemasterdd) come strumento read-only di pre-filtro. Resta read-only: e' lo STEP di analisi, non la policy completa.
2. **Ground-truth verify** -- diff/API reale > title/claim (L-025/L-029).
3. **Correzione attiva sessione Jules** -- `sendMessage` correttivo con evidenza file:line alle sessioni Jules con premessa falsa/scope-creep/regressione (L-030). Repo-agnostico, autorizzato ovunque (capability `autoMode.allow` gia' attiva).
4. **Fix sovereign dei residui** -- per cio' che Jules non chiude correttamente: fix locale (Aider/manuale) su branch, con verifica test obbligatoria.
5. **Batch merge/close** -- **resta azione esplicita per-batch di Eduardo**. INVARIATO. Claude prepara i set (MERGE-OK / CLOSE / NEEDS-REVIEW) + comandi pronti; l'esecuzione merge/close e' Eduardo-only-explicit.

### Boundary -- cosa cambia e cosa NO

- **Cambia**: estensione write-to-repo (commit + branch push per fix sovereign su branch Jules) a Game e agli altri repo esterni monitorati, limitatamente allo **scope Jules-PR-remediation**. Commenti PR di chiusura-loop tecnica consentiti.
- **NON cambia (SPOF oversight preservato)**: il gate **merge/close resta Eduardo-only explicit per-batch**. Mai merge/close autonomo. Stesso pattern del boundary vault-shared (L-012 / OD-033 amend 2026-05-16): branch+PR+fix OK automatici, il merge e' il gate umano.
- **NON cambia**: throttle/config Jules (jules.google + GitHub-App) resta Eduardo org-level.

## Consequences

**Positive**: un solo modello coerente cross-sessione/cross-macchina (ferma il narrative drift); sfrutta il canale L-030 validato (n=3/4) e il tier fix-sovereign; riduce il carico manuale Eduardo mantenendo il gate decisionale critico (merge/close).

**Negative / rischi**: maggiore superficie write su repo esterni (mitigato: scope ristretto a Jules-PR-remediation + gate merge invariato + test obbligatori pre-push); il modello attivo costa piu' token/sessione del triage passivo.

**Reconciliation richiesta da questo ADR**:
- `.claude/agents/jules-pr-triager.md` -- riformulato: resta lo strumento di triage read-only, ma il "Cosa NON fare / Read-only puro" e' riscoped al solo agent, NON alla sessione-Claude che lo invoca (che opera Model-3). Punta a questo ADR.
- memory `feedback_external_repo_action_boundary` -- emendata per lo scope Jules-PR (sendMessage + fix sovereign + comment consentiti su Game; merge/close resta explicit-auth).

**Ratification trigger**: OK esplicito Eduardo su questo ADR + primo ciclo Model-3 applicato su Game (32-PR backlog) chiuso senza incidente boundary (nessun merge/close non autorizzato).

## Riferimenti

- L-030 (Jules session premise pre-verify + corrective sendMessage), L-029/L-025 (ground-truth), L-002 (cross-repo narrative drift), L-012 (vault sibling-peer write-under-auth)
- `.claude/agents/jules-pr-triager.md` (#153) + policy cadenza #156
- memory `feedback_external_repo_action_boundary`, `autoMode.allow` rule (`~/.claude/settings.json`)
- ADR-0026 (cognitive workflow protocols)
