# COMPACT_CONTEXT

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/COMPACT_CONTEXT.md`.
>
> Aggiornare in rituale chiusura sessione (CLAUDE_OPERATING_RULES.md #9).

## Progetto
- **Nome**: CodeMasterDD AI Station
- **Versione del compact**: v6 (post ADR-0016 draft + governance consolidation)
- **Data ultimo aggiornamento**: 2026-04-24 03:00

## Stato attuale
- Barra globale **88%** invariata. Fase 6 al **55%** (11/20 dogfood + quality bench v1+v2 done).
- HEAD `9af4b72`, origin/main aligned, working tree clean.
- **Commit sessione 2026-04-24 notte (11 totali)**: `9ab01e9` (governance drift) → `0fa0016` (fix #9 HEREDOC commit-guard) → `2254706` (compact v4) → `3156edf` (fix #10 command.includes false-positive) → `3231e2e` (polish #11 stderr) → `5539881` (compact v5) → `9bcc2a4` (**ADR-0016 draft** OD-006 formalized) → `4e67a21` (journal entry) → `8de3263` (CLAUDE.md pointer ADR-0016) → `b31ff86` (close H6 + routing refs) → `9af4b72` (backlog refresh). Tutti pushed.
- **Commit sessione 2026-04-23 sera**: `4f5227c` (governance framework) → `e7a4ed0` (JOURNAL framework) → `f80ab3c` (retry logic quality-bench rescue) → `2dccec7` (apostrofo fix Aider auto) → `e687b42` (findings consolidation) → `5ef8e9c` (compact refresh). **6 commit**, pushed.
- Fase 6 dataset attuale: 6 cosmetic full + 1 cosmetic partial + 3 behavior success + 1 behavior **REJECT**. Fail rate 9.1% (vs 30% threshold ADR-0014). Zero silent-corruption working-tree cumulative.
- Framework operativo `Archivio_Libreria_Operativa_Progetti/` integrato come governance layer.

## Obiettivo di questa fase
- **Fase 6 (compressa, ~4 settimane)**: chiudere 4 criteri ADR-0014 entro **~2026-05-20**.
- **Sprint 01 target**: dataset 8 → ≥12 dogfood (di cui ≥3 behavior-critical) + validare cp1252 + review settimana 2.

## Cosa è già stato fatto

### Sessione 2026-04-24 notte (governance drift + 3 dogfood + ADR-0016 + final consolidation)
- **Audit governance drift post-sera**: 4 file allineati (PROJECT_BRIEF, ROADMAP, MODEL_ROUTING, MASTER_PROMPT). Commit `9ab01e9`.
- **Dogfood #9 behavior-critical LOCAL**: fix HEREDOC false-positive in `scripts/hooks/commit-guard.js` via `aider-refactor` (Qwen 14B Q2 diff). 1st-try, 7k/282 tok, 100% compliance + small smell console.log. Constraint-count=2 (fix+preserve). **Primo behavior-critical local Fase 6**. Commit `0fa0016`.
- **Dogfood #10 behavior-critical LOCAL**: fix `command.includes('git commit')` false-positive. Qwen 14B Q2 diff, 1st-try, 7k/169 tok, 100% clean. Constraint-count=3. Commit `3156edf`.
- **Dogfood #11 cosmetic LOCAL polish**: console.log → console.error per #9 smell. Qwen 7B whole, 1st-try edit + 1 auto-commit retry (hook block → retry → valid). 5.3k/656 tok. Commit `3231e2e`. **2° validazione pattern auto-commit retry** post-#8.
- **ADR-0016 Proposed** — `docs/adr/0016-constraint-count-routing-dimension.md`: formalizza OD-006 constraint-count come seconda dimensione routing, estende ADR-0008. Matrice 2D classe × constraint-count. Distinzione transform vs preserve. **Status Proposed**; Accepted trigger = n≥3 data points addizionali (gap constraint=4, 2-transform LOCAL, 5-strict LOCAL). OD-006 chiuso. Commit `9bcc2a4`.
- **Governance consolidation final sweep**: JOURNAL entry (`4e67a21`), CLAUDE.md pointer ADR-0016 (`8de3263`), H6 closed + routing refs updated (`b31ff86`), BACKLOG refresh close M1/M2/M6 (`9af4b72`).
- **Sprint 01 obiettivi superati early** (3° giorno su 14): 11/12 dogfood + **4/3 behavior-critical ✅ superato**.
- **Memory M2 refresh**: `project_session_resumption.md` aggiornato (HEAD, tabella 11 dogfood, Sprint 01 early hit, ADR-0014 status).

### Pre-sessione corrente
- Hardware setup + hardening + migrazione progetti (Fase 1-5 closed).
- Stack AI tier-routing 4 tier + privacy policy per-repo.
- 14 ADR, 4 guard rail commit cross-agent, tracking `ccusage` + dogfood log.
- Quality bench framework (75 test, 100% pass@1 discriminant-limited).
- 11 file governance root-level + 4 aggiuntivi compilati seguendo schema archivio.
- Framework `Archivio_Libreria_Operativa_Progetti/` importato e integrato.

### Sessione 2026-04-23 sera (governance + sprint01 T1/T2)
- **Normalizzazione governance**: 11 file schema archivio, 3 Decisioni non-ADR registrate (001/002/003).
- **T1 behavior-critical cloud REJECT**: Groq 70B ha prodotto 5 constraint violations su retry logic `Invoke-Model`, inclusa 1 BLOCKING (return-value divergence tra branch). **Rescue manuale** Claude Code con helper `Invoke-ModelRequest` — commit `f80ab3c`, syntax validated.
- **T2 cosmetic local partial**: Qwen 7B ha fixato apostrofo elisione in `bench-ollama.ps1` (✅) ma skippato condensazione NOTES (❌). Auto-commit retry ADR-0011 validato (hook block → Aider self-retry → pass 2nd-try) — commit `2dccec7`.
- **OD-006 proposta**: constraint-count come seconda dimensione routing (≥5 constraint strict → manual Claude Code preferito).
- **Consolidamento findings** in `JOURNAL`, `OPEN_DECISIONS`, `MODEL_ROUTING`, `BACKLOG` — commit `e687b42`.

## Decisioni prese

### ADR strategici (15, indice in DECISIONS_LOG)
- **ADR-0008** Hub pattern tier routing (cosmetic/behavior/escalation)
- **ADR-0011** Commit governance cross-agent
- **ADR-0012** RAM 64GB upgrade, qwen3:30b tier 2 stabile
- **ADR-0013** Tier 3 cloud free providers — Groq/Cerebras primary
- **ADR-0014** Fase 6 compressa a ~4 settimane
- **ADR-0016** Constraint-count seconda dimensione routing — **Proposed 2026-04-24**

### Decisioni non-ADR (operative minori, in DECISIONS_LOG)
- **001** Adozione schema framework archivio per governance files
- **002** `FIRST_PRINCIPLES_GAME_CHECKLIST` N/A per questo repo (non game)
- **003** Regole 07_OPERATING_PACKAGE non clonate al root (pointer + adozione)

## Vincoli hard
- RTX 5060 8 GB VRAM → ctx tuning obbligato modelli >7B.
- Windows cp1252 bug Aider → fix deployato ma **validazione empirica pending** (8 dogfood consecutivi senza retry loop naturale; soglia pazienza n=15).
- **Deadline fissa 2026-05-19** (Claude Max expiration). Target Fase 6 closure 2026-05-20.
- Privacy per-repo rigorosa (Synesthesia mixed, cliente sovereign-only).
- No `--force` su main, no `--no-verify`, Conventional Commits enforced.

## Problemi aperti

- **P1** Dogfood behavior-critical n=4 (3 success + 1 REJECT). Target ≥5 — gap 1.
- **P2** Fix cp1252 validation empirica ancora pending (8 dogfood senza trigger retry loop, #9/#10/#11 1st-try).
- **P3** Privacy validation reale 1/3.
- **P6** Qwen 7B commit-prompt 0% compliance (ma auto-retry post-hook-block **funziona** empirically — nuovo dato positivo dogfood #8).
- **P7** Cloud 70B degrada a 20% compliance su behavior-critical con ≥5 strict semantic constraint (dogfood #7). Implicazione: ridimensionamento shift cloud-first di ADR-0013.

Dettaglio e next actions in `BACKLOG.md` (H1-H6) + `OPEN_DECISIONS.md` (OD-001 to OD-006).

## File / output importanti
- Governance root-level (11): `PROJECT_BRIEF`, `COMPACT_CONTEXT` (questo), `DECISIONS_LOG`, `BACKLOG`, `OPEN_DECISIONS`, `ROADMAP`, `SPRINT_01`, `MASTER_PROMPT`, `REFERENCE_INDEX`, `PROMPT_LIBRARY`, `MODEL_ROUTING`
- Convenzioni Claude Code: `CLAUDE.md` (progetto) + `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/*` (meta-rules adottate)
- Diario cronologico: `JOURNAL.md` (4 entries tra 2026-04-23 sera e 2026-04-24 notte)
- Decision history: `docs/adr/` (15 file, ultimo ADR-0016 Proposed)
- Operational log: `logs/aider-delegation-2026-04.md` (11 dogfood entries + breakdown per classe/stack/constraint)
- Framework archivio: `Archivio_Libreria_Operativa_Progetti/` (130 file multi-progetto)

## Prossimi 3 passi
1. **M5 Synesthesia privacy validation** — criterio 3 ADR-0014 ancora 1/3. **Priorità residua principale sprint 01**: ≥2 sessioni reali Synesthesia con classificazione enforced (views/ cloud OK, controllers/ sovereign). Richiede task reale emergente dal lavoro web app.
2. **H1 residuo** — +1 behavior-critical per chiudere target ≥5 (attuale 4). Candidato real emergente.
3. **Review settimana 2** (~2026-05-07) — count + fail rate + cost + ETA. On-track evidente (55% Fase 6 + 9.1% fail rate), formalizzare in JOURNAL entry dedicata + decisione on-track / mid-course.

## Next session restart: cosa leggere per ripartire

Ordine raccomandato:
1. `CLAUDE.md` — convenzioni progetto
2. Questo file (`COMPACT_CONTEXT.md`) — snapshot stato corrente
3. `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/CLAUDE_OPERATING_RULES.md` — regole meta-operative
4. `BACKLOG.md` + `OPEN_DECISIONS.md` — cosa è aperto
5. `SPRINT_01.md` — sprint attivo + task candidates
6. ADR rilevanti solo se task tocca topic noto

Memory auto-caricata via `~/.claude/projects/.../memory/MEMORY.md`.
