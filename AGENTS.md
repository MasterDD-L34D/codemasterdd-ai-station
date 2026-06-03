# AGENTS.md

Entry point per agent multi-client (Codex, OpenCode, agent web-based o sandbox-confined). Convenzione `agents.md`. Per dettaglio operativo completo leggere `CLAUDE.md` (autoritativo).

## Anti-confusion preamble (leggere prima di tutto)

Questo repo gira su **CodeMasterDD**, una workstation Windows reale (Lenovo LOQ Tower 17IAX10). I path assoluti `C:\dev\...` e `C:\Users\edusc\...` referenziati nei doc **sono validi e i file esistono**.

Se stai operando da Codex Cloud / sandbox web / container senza accesso al filesystem locale Windows e non riesci a verificare i path assoluti, **non concludere che siano "missing", "transplanted", o "obsoleti"**. Significa solo che tu non hai accesso al filesystem reale. Il PC corretto vede tutto.

In particolare i seguenti progetti esterni sono **attivi**, non dormant:

- `C:\dev\Game` — Evo-Tactics, repo `MasterDD-L34D/Game`
- `C:\dev\synesthesia` — repo `MasterDD-L34D/synesthesia` (dormant intenzionale fino esame UniUPO ~ago 2026, non perso)
- `C:\Users\edusc\Dafne\workspace\swarm` — repo `MasterDD-L34D/evo-swarm`
- `C:\Users\edusc\aa01` — workspace personale non-git

Stack tier routing, wrapper Aider, API keys cloud, dogfood log, dogfood SQLite, promptfoo results: tutti presenti localmente. Per la mappa completa vedi CLAUDE.md sezione "Hardware" + "Stack installato" + "API keys tier 3 cloud".

Se hai dubbi sullo stato di un path, chiedi a Eduardo prima di modificare governance o creare branch "recovery". Il pattern `codex/structural-reset` (1° maggio 2026, rejected 7 maggio) è il caso da non ripetere — ADR-0021.

## Read first (ordine)

1. Questa preamble (sopra)
2. `CLAUDE.md` — convenzioni progetto autoritative
3. `COMPACT_CONTEXT.md` — snapshot stato corrente (HEAD, Fase, sprint)
4. `STATUS_MULTI_REPO.md` — dashboard cross-repo (Game/Synesthesia/Dafne/AA01)
5. `BACKLOG.md` + `OPEN_DECISIONS.md` — cosa è aperto

## Rule

`CLAUDE.md` è autoritativo per decisioni progetto (stack, hardware, tier routing, convenzioni operative). AGENTS.md è preamble sandbox-awareness, non override.

In caso conflitto:

- CLAUDE.md > AGENTS.md su decisioni progetto
- AGENTS.md > CLAUDE.md su preamble anti-confusion sandbox

## Branch convention

- Branch principale: `main`
- Branch agent: `<agent>/<topic>` (es. `claude/...`, `codex/...`)
- Conventional Commits enforced via hook globale (vedi CLAUDE.md "Stack installato" guard rail chain)
- No `--force` su `main`, no `--no-verify` (se non esplicitamente richiesto)
- PR review obbligatoria prima di merge per branch agent — non auto-merge, anche se CI verde

## Encoding policy (per nuovi doc)

- Nuovi file `.md` creati da agent: ASCII-first per body prose
- Caratteri non-ASCII consentiti: emoji status (warning/check/red), simboli `>=`, `<=`, `->` se semanticamente rilevanti
- **Evitare** in body nuovi doc: em-dash, middot, smart quotes -- usare `--`, `|`, `'`, `"`
- **Eccezione**: titoli ADR (`# ADR-NNNN -- Title`) e headers sintetici possono usare em-dash per coerenza convention progetto.
- File legacy con mojibake (`A-tilde`, `a-circumflex-euro-em`): **frozen**, no riscrittura globale cieca. Fix mirato solo se file diventa attivamente confusing per task corrente.

## Out of scope per AGENTS.md

Non duplicare in questo file:

- Stack hardware/software (vive in `CLAUDE.md` "Hardware" + "Stack installato")
- Tier routing modelli AI (vive in `CLAUDE.md` "Priorità modelli AI" + `MODEL_ROUTING.md`)
- Privacy policy per-repo (vive in `CLAUDE.md` "Progetti monitorati")
- Lista ADR (vive in `DECISIONS_LOG.md` + `docs/adr/`)
- Direzione corrente (vive in `GOALS.md`; sprint storici archiviati in `docs/archive/`)

Se cambia uno di questi, aggiorna il file autoritativo, NON AGENTS.md.

## Riferimenti

- ADR-0021 — Multi-client instruction files: `docs/adr/0021-multi-client-instruction-files.md`
- Convenzione `agents.md`: https://agents.md/
- Case-study branch rejected: `codex/structural-reset` (HEAD `4b7c84a`, rejected 2026-05-07 per false-premise sandbox-confusion)
