# ADR-0019 — Persistenza processo Dafne swarm su Windows 11

> *TL;DR: Il server Dafne (`START-SWARM.ps1`) muore 2× in sessione auto-mode 2026-04-24 dopo ~10-30min quando lanciato da PowerShell con `Start-Process -WindowStyle Minimized`. Tre opzioni valutate: wrapper auto-restart PowerShell (leggero, richiede shell aperta), Windows Task Scheduler (always-on, modifica di sistema), Docker container (consistente con infra ADR-0017, complessità alta). Decisione: **Opzione A (wrapper)** per sviluppo attivo corrente, con Opzione B (Task Scheduler) come upgrade non-bloccante post-Fase 6. Opzione C deferred a post-transizione sovereign.*

- **Status**: **Accepted** (2026-04-24 — wrapper Opzione A già implementato e committato in swarm repo `c638098`. Nessun trade-off controverso, zero friction adoption, Eduardo ha delegato carta bianca durante sessione live.)
- **Data**: 2026-04-24
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

> **Addendum 2026-04-25**: wrapper rinominato da `START-DAFNE-PERSISTENT.ps1` → `START-SWARM-PERSISTENT.ps1` per separazione concettuale: Dafne è **entità** (persona, con strumento proprio `openclaw tui`), la swarm è **collettivo di agenti** (server Flask :5000 che Dafne coordina). Il wrapper riguarda la swarm, non Dafne come individua. Rename propagato in tutti i doc operativi; ADR preserva nome vecchio solo in citation storica di questo addendum.

## Context and Problem Statement

Dafne swarm (`C:\Users\edusc\Dafne\workspace\swarm`) è un server Python/Flask avviato tramite `START-SWARM.ps1`. Il dogfood-ui (ADR-0017, panel `/dafne`) lo consuma via HTTP su `:5000` con `ping_timeout=2s`.

### Situazione attuale

`START-SWARM.ps1` lancia un processo Python foreground. Se la shell PowerShell parent chiude — o esce dopo un `Start-Process` senza `Wait` — il processo figlio perde il suo tty parent e può terminare silenziosamente. Non c'è supervisor, non c'è restart automatico, non c'è log della causa di morte.

### Input / trigger

Sessione auto-mode 2026-04-24: Dafne è stato rilanciato 2× in ~30 minuti (via `Start-Process -WindowStyle Minimized`). Entrambe le volte il processo è morto senza traceback visibile. Il panel `/dafne` del dogfood-ui mostrava `reachable: false`, causando loss of visibility su Dafne Atto 1 day-3.

Workaround immediato creato: `START-SWARM-PERSISTENT.ps1` con loop auto-restart + circuit breaker (max 20 restart/ora). Documento operativo in `docs/reference/dafne-persistence.md` con 3 opzioni.

## Options

### Opzione A — Wrapper PowerShell auto-restart `START-SWARM-PERSISTENT.ps1` ✅ RACCOMANDATA

Uno script PS che wrappa `python app.py` in un `while ($true)` loop. Se il processo esce per qualsiasi ragione, ripartisce dopo 10 secondi. Circuit breaker conta i restart nell'ultima ora: se supera 20, si ferma e logga un warning (evita bootloop).

Il wrapper è già implementato e testato in sessione 2026-04-24.

**Pro**:
- Zero modifica di sistema (no admin, no registro, no Task Scheduler)
- Visibilità immediata: log stdout nella finestra PS, crash traceback catturato
- Reversibile: chiudi la shell, niente rimane in background
- Circuit breaker previene bootloop su crash strutturale
- Già implementato, testabile subito

**Contro**:
- Richiede una shell PowerShell dedicata aperta (o minimized) per tutta la sessione
- Se l'utente chiude la finestra PS per errore, Dafne muore (no warning)
- Non sopravvive a riavvio macchina senza riaprire manualmente
- Non integrato con Windows service lifecycle

**Cost**: 0 (wrapper già scritto)

### Opzione B — Windows Task Scheduler (always-on)

Registra Dafne come Scheduled Task con trigger `AtLogOn`. Task Scheduler gestisce restart-on-failure e la task sopravvive a chiusura shell e riavvio macchina.

**Pro**:
- Always-on: parte automaticamente al logon, sopravvive a riavvio
- Integrato con Windows: visibile in Task Scheduler UI, log in Event Viewer
- Non richiede shell aperta
- `RestartOnFailure` nativa OS (più robusta del wrapper PS)

**Contro**:
- Modifica di sistema (richiede admin una tantum, task visibile a livello OS)
- Debugging più opaco: log non in finestra diretta, serve Task Scheduler UI o Event Viewer
- Task Scheduler riprova silenziosamente — può mascherare crash strutturale
- Overhead governance: ricordare `Unregister-ScheduledTask` se Dafne viene abbandonato

**Cost**: setup admin ~10 min

**Verdict**: soluzione superiore per always-on, ma overhead governance > benefit in Fase 6 attiva dove Dafne è ancora in sviluppo (Atto 1, day-3/10). Candidata per post-Fase 6 o quando Dafne raggiunge stabilità operativa.

### Opzione C — Dockerize Dafne swarm

Spostare `evo-swarm` in un container con `restart: unless-stopped`. Integrerebbe con `infra/docker-compose.yml` (ADR-0017). Ollama via `host.docker.internal:11434`.

**Pro**:
- Consistenza con stack infra ADR-0017
- `restart: unless-stopped` soluzione più robusta per persistence
- Isola dipendenze Python
- Log unificati con `docker compose logs`

**Contro**:
- Richiede Dockerfile nel repo `evo-swarm` (cross-repo change non banale)
- Dafne scrive su `C:\dev\Game\agents/` quando Eduardo approva: dal container servirebbe bind-mount Windows (complessità alta, rischio permessi)
- Dafne è in sviluppo attivo (Atto 1): containerizzare processo in rapid iteration aggiunge friction
- Latenza Ollama via `host.docker.internal` non misurata
- Scope: cambia architettura di un repo esterno per risolvere QoL locale

**Cost**: ~2-3h setup + testing bind-mount + Dockerfile authoring in `evo-swarm`

**Verdict**: scartata per Fase 6. Candidata per Fase 7 post-sovereign se Dafne diventa infrastruttura stabile.

## Decision

**Opzione A — wrapper `START-SWARM-PERSISTENT.ps1`** per il periodo Fase 6 (fino a ~2026-05-20).

**Rationale**: il problema è QoL, non blocco critico. Opzione A risolve il 90% del problema (crash recovery, log capture) con zero modifica di sistema. Dafne è Atto 1 day-3/10 — processo in rapid iteration — containerizzarlo (C) o task scheduler (B) prima che si stabilizzi aggiungerebbe overhead governance sproporzionato. Il wrapper è già scritto e testato.

Principi rispettati:
- **YAGNI / minimalismo** (ADR-0005): non aggiungere complessità di sistema finché non necessaria
- **Sovereign by default** (ADR-0001): nessuna dipendenza esterna
- **Observability integrata** (ADR-0017): Dafne reachable = panel dogfood-ui funzionante

### Implementation plan

- Step 1 — Verificare commit `START-SWARM-PERSISTENT.ps1` in `evo-swarm` repo. Effort: 5 min.
- Step 2 — Aggiornare `docs/reference/dafne-persistence.md` sezione "Decisione ADR-0019". Effort: 2 min.
- Step 3 — Aggiornare `STATUS_MULTI_REPO.md` sezione Dafne con "avvio: `START-SWARM-PERSISTENT.ps1`". Effort: 2 min.
- Step 4 (deferred, post-Fase 6) — Rivalutare Opzione B se Dafne stabilità operativa confermata.

## Consequences

### Positive

- Dafne non muore più silenziosamente durante sessioni lunghe
- Panel dogfood-ui `/dafne` mantiene `reachable: true`
- Log crashdump catturato in `logs/dafne-YYYY-MM-DD.log`
- Circuit breaker previene bootloop

### Negative

- Richiede disciplina manuale: ricordarsi di lanciare wrapper invece di `START-SWARM.ps1` diretto
- Shell PowerShell deve restare aperta
- Non sopravvive a riavvio macchina

### Mitigations

- Aggiornare shortcut desktop Dafne (`start-dafne.cmd`) per puntare al wrapper persistente
- Se Dafne diventa servizio stabile post-Atto-1, upgrade a Opzione B via `Register-ScheduledTask`
- Rollback: nessuno necessario — si torna a `START-SWARM.ps1` semplicemente non usando il wrapper

## Related

- **ADR-0017** — Stack osservabilità + dogfood-ui: panel `/dafne` è consumer diretto di questa decisione
- **ADR-0018** — Agent readiness protocol: questo ADR è Gate 1 smoke test per agent `adr-drafter`
- **ADR-0005** — YAGNI / minimalismo: razionale primario per Opzione A su B/C
- **ADR-0001** — Sovereign AI strategy: nessuna dipendenza cloud introdotta
- `docs/reference/dafne-persistence.md` — documento operativo con comandi pratici

## Notes

- **Trigger review**: se Dafne crashloop supera 3 eventi/settimana nonostante wrapper (circuit breaker interviene costantemente), rivalutare Opzione B
- **Ratification target**: Accepted dopo prima settimana di uso stabile senza interventi manuali. Target: 2026-05-01
- Non richiede ADR-0010 skill policy review (nessun tool esterno installato)
