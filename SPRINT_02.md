# SPRINT_02 -- "Post-Max scenario A operativo + smoke sovereign + cleanup"

> Sprint 2 della Fase 7 (post-Max). Finestra: **2026-05-20 -> ~2026-06-19** (4 settimane, prima sessione full-sovereign settimana 1).
>
> **Status 2026-05-07**: **Planning** (sprint inizia 20/05 dopo Claude Max expiration 19/05). Abbozzo preparatorio per primo onboarding sovereign.
>
> **Update 2026-05-10**: pre-validation in autonomy: **T3 hot-restart PASS** (stack ready ~12s, 38 traces preserved post 13gg+ down, regression `dogfood-ui` VALID_STACKS desync trovata e fixata, entry POST 12->13). **T4 cleanup PR esterni gia' COMPLETO** (i 4 PR target gia' triagati 7/5: #97 Game-Database closed-as-stale post-rebase abort, #105/#10/#61 mergeati). Restano per 20/05+: T1 smoke sovereign, T2 dogfood organico, T5 cost tracking, T7 review.
>
> **Sprint objective**: validare empiricamente scenario A (full-sovereign $0-50/anno) in uso normale + cleanup PR esterni opportunistico + cost tracking primo mese reale + raccolta dogfood organici post-closure (target soft n>=20 cumulative). Zero silent-corruption deve rimanere invariato.

---

## Pre-requisiti

- Fase 6 CLOSED 2026-05-07 (ADR-0015 + ADR-0017 entrambi Accepted).
- Stack ADR-0017 scaffold opt-in: hot-restartable in <60s con `cd infra && docker compose up -d` se serve dashboard/tracing/eval.
- Wrapper aider-* in `C:\Users\edusc\.local\bin\` operativi senza Claude Max.
- API keys cloud free tier (Groq + Cerebras + Gemini) attive in `~/.config/api-keys/keys.env`.
- Privacy policy per-repo invariata (Synesthesia mixed dormant, codemasterdd cloud OK).

## Task

### T1. Smoke test sovereign empirico [primo task post-Max]
- **Cosa**: 3 wrapper aider-* eseguiti su task piccoli reali, validation tecnica end-to-end senza Claude Max.
  - `aider-cosmetic <file>` (Qwen 7B): JSDoc/docstring/rename su 1 file -- es. `apps/dogfood-ui/db.py` o `scripts/quality-bench/run-bench.ps1`
  - `aider-refactor <file>` (Qwen 14B Q2 + diff): bug fix piccolo o cleanup logic su 1 file -- candidati: error handling helper `apps/dogfood-ui/dafne_client.py`, retry logic gia' robusto bench scripts
  - `aider-groq <file>` (cloud llama-3.3-70b): cosmetic doc su file non-sensitive -- candidati: README updates, ADR cross-references
- **File/sistemi toccati**: script in `apps/dogfood-ui/`, `scripts/`, `docs/`. **NON** toccare `controllers/`/`routes/` Synesthesia (privacy mixed).
- **Check**: post-edit `git diff HEAD~1` verify no silent-corruption; `logs/aider-delegation-2026-05.md` (nuovo file mese) entry per ognuno (classe, stack, retry, tokens, cost, esito).
- **Success**: 3/3 wrapper eseguono task senza crash; >=2/3 successo 1st-try; 0 silent-corruption working-tree.
- **Failure mode**: se 2+ crash con UnicodeEncodeError → trigger M3 (cp1252 fix re-evaluation). Se 2+ silent-corruption → ADR-0008 trigger reactive.

### T2. Dogfood organico continuativo
- **Cosa**: ogni task delegabile in workflow normale → tracked in `logs/aider-delegation-2026-05.md` (e `2026-06.md` quando arrivano). No quota, no forzatura: solo entry organiche.
- **Target soft**: dataset cumulative codemasterdd-Fase 6 da n=12 -> n>=20 entro fine sprint (8 entry organiche in 4 settimane = 2/settimana, raggiungibile naturalmente).
- **Esempi opportunistici**:
  - Modifiche docstring/comment-based-help su altri script
  - Bug fix su `scripts/hooks/commit-guard.js` se emergono nuovi falsi positivi
  - Refactor `dogfood-ui` se emergono pain points UI
  - Migration logs/aider-delegation-* a SQLite via `scripts/migrate-log-to-sqlite.py` (se non gia' fatto in ADR-0017)
- **Success**: dataset >= 18 entries entro 2026-06-19, fail rate cumulative <15%, zero silent-corruption.
- **Safety note**: T1 e' precondizione tecnica; T2 e' raccolta dati. Non confondere.

### T3. Stack ADR-0017 hot-restart procedure validation
- **Cosa**: avviare stack scaffold da zero (Docker Desktop + `docker compose up -d` + verify endpoint health) per misurare tempo reale e identificare regressioni post-13gg downtime.
- **File toccati**: nessuno (esecuzione operativa). Eventuale `docs/runbook/adr-0017-hot-restart.md` se procedure rivela edge case.
- **Check**: tempo cumulative <60s da `docker compose up -d` a `/health/readiness` 200 + Langfuse 7+ trace count preservati. Se DB corrotti -> ADR addendum.
- **Success**: stack up + dogfood-ui accessibile + 1 entry creata via UI/POST → regressione zero.
- **Failure mode**: se DB Postgres corrotti → recovery via volume backup oppure `docker compose down -v && up -d` (perdita 7+ trace acceptable, scaffold stato).

### T4. Cleanup PR esterni opportunistico
- **Cosa**: review e merge/close dei 4 PR pending fuori codemasterdd:
  - **Game-Database #97** (Codex 23gg+, +1147 righe, CI verde 8 check): review approfondita (vedere se rebase serve, se cambiamenti ancora rilevanti dopo Sprint Impronta Game). Decision: merge / close / chiedere update.
  - **Game-Database #105** (doc 1-line): merge veloce se ancora rilevante.
  - **compass-marketplace #10** (whitelist fix + test new): review e merge se test passa.
  - **evo-swarm #61** (weekly digest 27/04): valutare se digest 27/04 e' ancora utile o se va chiuso/sostituito da digest 11/05.
- **File toccati**: nessuno in codemasterdd (sono PR su altri repo).
- **Success**: 4/4 PR triagati (merge / close / comment), backlog GitHub pulito.

### T5. Cost tracking primo mese full-sovereign
- **Cosa**: fine settimana 4 sprint (~2026-06-15 +/-) → snapshot ccusage NULL (Claude Max disattivato) + sum cost cloud da `logs/aider-delegation-2026-05.md` + `2026-06.md`.
- **Target ADR-0015**: <$5/mese cloud cumulative (margine ampio vs $20 budget). Atteso: <$1/mese basato su tier 3 free + emergenza tier 4 raro.
- **Check**: proiezione su 12 mesi → conferma scenario A $0-50/anno realistico.
- **Success**: report 1-pagina in `logs/cost-snapshot-2026-06.md` con: cloud spend reale, proiezione annua, eventuali alert >budget threshold.

### T6. Privacy validation Synesthesia preview (opportunistic)
- **Cosa**: SE Eduardo riattiva Synesthesia pre-fine sprint (improbabile, target ago 2026), eseguire 1 task validation classifier con dati reali. ALTRIMENTI: skip, mantenere derogato ADR-0014 #3.
- **File toccati**: `C:\dev\synesthesia\views/` (cloud OK) o `C:\dev\synesthesia\controllers/` (sovereign-only) -- 1 task minimo.
- **Check**: classifier policy per-repo nega cloud delegation su `controllers/` (atteso) e permette su `views/` (atteso).
- **Success**: 1 entry classifier in log, ADR-0014 criterio #3 a 2/3 (preview, non chiudibile fino a 3/3).
- **Skip se**: Synesthesia ancora dormant (pattern atteso fino ago 2026).

### T7. Review fine sprint + ADR addendum se serve
- **Cosa**: sessione ~30-45min ~2026-06-19: count dogfood + cost real + delta scenario A vs prediction + decisione SPRINT_03 scope.
- **Output**: entry JOURNAL "Review SPRINT_02" + COMPACT v12 + eventuale ADR-0015 addendum se trigger ri-evaluation attivati (silent-corruption emersa, fail rate >15%, privacy violation).
- **Success**: 3 decisioni chiare -- continuita' scenario A / mid-course correction / SPRINT_03 scope.

## Trigger ADR (ri-evaluation soft-override ADR-0015)

Soft-override n>=12 di ADR-0015 e' valido se durante SPRINT_02 NON emergono questi pattern:

- **silent-corruption working-tree** >=1 caso reale (non test) -> hard blocker, ADR-0015 addendum + switch potenziale a scenario B (Claude Pro $240/anno acquisition revisited)
- **fail rate cumulative** >15% (oltre margine sicurezza) -> revisione routing tier
- **privacy violation** in repo non-sensitive (cloud delegation leak su `controllers/` Synesthesia o repo cliente futuro) -> hard blocker, ADR addendum

Se nessun trigger emerge a fine SPRINT_02 -> Fase 7 stabilizzata, scenario A confermato per anno fiscale.

## Safety notes

- **Zero subscription ricorrenti**: target ADR-0001 + ADR-0015. Se emerge bisogno di Claude Pro $240/anno → ADR addendum esplicito, NO acquisition silent.
- **Privacy per-repo rigorosa**: codemasterdd cloud OK; Synesthesia controllers/ sovereign-only; eventuali repo cliente sovereign-only sempre.
- **No --force su main, no --no-verify**: invariato.
- **Conventional Commits**: invariato (cross-agent enforced via hook globale).
- **Encoding ASCII-first** per nuovi doc (ADR-0021): em-dash convention solo titoli ADR.
- **Stack ADR-0017 opt-in**: Docker Desktop start manuale solo quando si usa dashboard/tracing/eval. Default: stack down.

## Out of scope

- Fixing Game ROSSO findings (boss enrage + XP curve): Sprint Impronta in corso, attendere quiet window post-CAP-NN
- Synesthesia work proattivo: dormant fino ago 2026 by design
- Dafne Atto 2 detail: governance vive in evo-swarm repo, monitorato da codemasterdd via STATUS_MULTI_REPO
- AA01 task PROPOSED del 25/04: workspace separato da codemasterdd, decide Eduardo standalone
- Mac mini come device secondario: deferred ADR-0021 finchè non emerge trigger

## Working rule per questo sprint

Ogni task delegato via wrapper aider-* genera entry organica in `logs/aider-delegation-2026-MM.md`. Niente forzatura quota: se in 4 settimane il workflow naturale produce 5 entries, OK; se ne produce 15, OK. Il punto e' validare scenario A in uso normale, non collect data per data.

Se emerge un trigger ADR (silent-corruption, fail rate spike, privacy leak) → stop sprint, ADR addendum reactive prima di continuare.
