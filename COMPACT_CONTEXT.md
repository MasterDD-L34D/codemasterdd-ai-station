# COMPACT_CONTEXT

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/COMPACT_CONTEXT.md`.
>
> Aggiornare in rituale chiusura sessione (CLAUDE_OPERATING_RULES.md #9).

## Progetto
- **Nome**: CodeMasterDD AI Station
- **Versione del compact**: v11 (sessione 2026-05-07: resume post-gap 12gg + Codex review + ADR-0021 + Fase 6 closure anticipata)
- **Data ultimo aggiornamento**: 2026-05-07 sessione corrente

## Stato attuale
- **Barra globale ~95%** (+4 da v10): Fase 6 CLOSED -- ADR-0015 e ADR-0017 entrambi Accepted 2026-05-07. Resta solo finestra transition 07/05 -> 19/05 (Claude Max expiration) + opzionale smoke test sovereign post-closure.
- HEAD `39f97da` su origin/main (post merge PR #2 ADR-0021). Branch corrente di lavoro `claude/fase6-closure-prep` (3 ADR/governance updates da committare).
- **Stack ADR-0017**: scaffold opt-in (Docker Desktop non auto-start). Hot-restartable in <60s con `docker compose up -d`. DB persistence Postgres+SQLite preservata. 7+ Langfuse traces ancora persistiti.
- **Agent ecosystem ADR-0018**: 12/18 ready, 6/18 draft trigger-gated. Status invariato dal 24/04.
- **Codex `/structural-reset` REJECTED in toto + chiuso + delete remote**: branch difensivo Codex Cloud sandbox-confusion (assunzione "transplanted, paths missing" smentita empiricamente, 9/9 path target presenti). Cherry-pick astratto: ADR-0021 + AGENTS.md + encoding policy.
- **PR pulito post-sessione**: #1 ADR-0020 mergeato 25/04. #2 ADR-0021 mergeato 07/05. #3 [REJECTED] chiuso 07/05.

### Gap operativo 25/04 -> 07/05 (non-stagnation)

Eduardo ha lavorato attivamente in altri repo (silent driver mode):
- **Game**: Sprint Impronta Ondata 1, 8+ commit, branches `aa01/cap-11..15` (telemetry + onboarding v2 + imprint phase V2). HEAD `5f42757a`.
- **Dafne swarm**: Atto 2 day 11+, 4 commit (weekly digest, IDENTITY refresh, gitignore cycle-log, health flag draft 07/05 PR #65). HEAD `1e14253`.
- **AA01**: silent driver del Sprint Impronta Game, capability-by-capability. 2 task PROPOSED del 25/04 (#001 voice-test + #002 day-5-post-session-ritual) restano in workspace.
- **codemasterdd**: dataset Fase 6 fermo a n=12 dal 24/04 -- shift naturale di focus quando policy hub ha completato il ciclo (trigger ADR-0008 confermato a #12).

## Obiettivo di questa fase

**Transition window 07/05 -> 19/05** (12 giorni residui Claude Max):
- Validation tecnica scenario A (smoke test 3 wrapper sovereign empirico) -- non bloccante per closure, gia' decisa
- SPRINT_02 abbozzo (post-Max operativo) come handoff per prima sessione 20/05+
- Cleanup PR esterni opportunistico (Game-Database #97 Codex 23gg + #105 + compass-marketplace #10 + evo-swarm #61)
- 19/05: disattivazione Claude Max, transizione a wrapper sovereign + Ollama

## Cosa e' gia' stato fatto

### Sessione 2026-05-07 (corrente -- resume + Codex + Fase 6 closure)

#### Triage PR cross-repo
5 PR open su 5 repo. Identificato branch `codex/structural-reset` su codemasterdd (no PR aperto, push 1° maggio) come priorita' sopra tutti gli altri PR.

#### Review sistematica `codex/structural-reset`
43 file +3690/-2186, premessa "transplanted/paths missing". Verifica empirica: tutti 9 path target esistono fisicamente. Codex operava da Codex Cloud sandbox.
Classificazione: 36 REJECT + 4 ADAPT-concept + 0 ACCEPT. Branch REJECTED in toto.

#### Cherry-pick ADR-0021
ADR-0021 "Multi-client instruction files" Accepted (MADR format). AGENTS.md ~70 righe come preamble Codex anti-confusion. CLAUDE.md +10 righe (encoding policy + pointer multi-client). PR #2 mergeato.

#### Cleanup `codex/structural-reset`
PR #3 [REJECTED] formal aperto e chiuso (audit trail). Delete remote ref con conferma esplicita Eduardo.

#### Fase 6 closure anticipata
Dataset n=12 fermo dal 24/04. Decisione: closure anticipata vs target sett.4 originale per evitare dogfood sintetici (anti-pattern ADR-0014).

- **ADR-0015** (Proposed -> Accepted): Scenario A full-sovereign $0-50/anno confermato. Soft-override esteso n>=12 con 5 rationale additivi. Claude Pro NOT acquired, scenario B declassato definitivamente.
- **ADR-0017** (Validated live + Proposed -> Accepted): 5/5 criteri ratification PASS. Stack scaffold opt-in (Docker Desktop manual start).

#### Governance refresh
JOURNAL entry +87 righe (questa sessione). COMPACT v11 (questo file). STATUS_MULTI_REPO refresh + DECISIONS_LOG entry pending in corso branch.

### Pre-sessione corrente
- 14 ADR + ADR-0020 silent-fail Python (Accepted 25/04). 21 ADR totali post-ADR-0021.
- 4 guard rail commit cross-agent + tracking ccusage + dogfood log.
- Quality bench framework (75 test, 100% pass@1).
- 11 file governance root-level + 4 aggiuntivi.
- Framework `Archivio_Libreria_Operativa_Progetti/` integrato.
- 12 dogfood Fase 6 cumulative al 24/04 (cosmetic 93%, behavior 70-80%, corruption 0).

## Decisioni prese

### ADR strategici (21 totali, indice in DECISIONS_LOG)
- **ADR-0008** Hub pattern tier routing (cosmetic/behavior/escalation)
- **ADR-0011** Commit governance cross-agent
- **ADR-0012** RAM 64GB upgrade
- **ADR-0013** Tier 3 cloud free providers
- **ADR-0014** Fase 6 compressa
- **ADR-0015** Fase 7 budget full-sovereign + deroga #3 Synesthesia -- **Accepted 2026-05-07**
- **ADR-0016** Constraint-count routing -- Proposed (n>=3 data points trigger pending)
- **ADR-0017** UI + observability stack -- **Accepted 2026-05-07** (5/5 criteri PASS)
- **ADR-0018** Agent readiness protocol 3-gate -- Accepted 2026-04-24
- **ADR-0019** Dafne process persistence -- Accepted 2026-04-24
- **ADR-0020** Silent-fail Python guardrail -- Accepted 2026-04-25 (PR #1 mergeato)
- **ADR-0021** Multi-client instruction files (AGENTS.md + Codex anti-confusion) -- **Accepted 2026-05-07** (PR #2 mergeato)

### Decisioni non-ADR (operative minori, in DECISIONS_LOG)
- **001** Adozione schema framework archivio
- **002** `FIRST_PRINCIPLES_GAME_CHECKLIST` N/A per questo repo
- **003** Regole 07_OPERATING_PACKAGE pointer + adozione (no clone root)
- **004** (pending entry) Codex `/structural-reset` REJECTED 2026-05-07

## Vincoli hard
- RTX 5060 8 GB VRAM -> ctx tuning obbligato modelli >7B
- Windows cp1252 bug Aider -> fix deployato + 9 dogfood consecutivi senza retry loop naturale (n=15 trigger raggiunto -- gap closure not bloccante)
- **Deadline fissa 2026-05-19** (Claude Max expiration). Fase 6 closure anticipata a 2026-05-07.
- Privacy per-repo rigorosa (Synesthesia mixed dormant fino ago 2026)
- No `--force` su main, no `--no-verify`, Conventional Commits enforced

## Problemi aperti

- **P3** Privacy validation Synesthesia 1/3. Retroattivo a riattivazione ~ago 2026 (deroga ADR-0015 documentata).
- **P6** Qwen 7B commit-prompt 0% compliance (auto-retry post-hook funziona empirically).
- **P7** Cloud 70B degrada a 20% compliance su behavior-critical con >=5 strict semantic constraint (dogfood #7).

P1, P2 chiusi tramite ADR-0015 closure (P1 behavior-critical n>=5 superato; P2 cp1252 monitoring chiuso a soglia).

## File / output importanti
- Governance root-level (12, +AGENTS.md): `PROJECT_BRIEF`, `COMPACT_CONTEXT` (questo), `DECISIONS_LOG`, `BACKLOG`, `OPEN_DECISIONS`, `ROADMAP`, `SPRINT_01`, `MASTER_PROMPT`, `REFERENCE_INDEX`, `PROMPT_LIBRARY`, `MODEL_ROUTING`, `AGENTS.md` (nuovo per multi-client)
- Convenzioni: `CLAUDE.md` (autoritativo) + `AGENTS.md` (Codex preamble) + `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/*` (meta-rules)
- Diario: `JOURNAL.md` (entry 2026-05-07 +87 righe)
- Decision history: `docs/adr/` (21 file, ultimi ADR-0015 e ADR-0017 e ADR-0020 e ADR-0021 Accepted)
- Operational log: `logs/aider-delegation-2026-04.md` (12 dogfood, fermo dal 24/04)
- Framework archivio: `Archivio_Libreria_Operativa_Progetti/`

## Prossimi 3 passi

1. **Commit + push branch `claude/fase6-closure-prep` + PR** (sessione corrente). Contiene: ADR-0015 closure + ADR-0017 closure + JOURNAL entry + COMPACT v11 + STATUS_MULTI_REPO refresh + DECISIONS_LOG entry.
2. **A3 Smoke test full-sovereign** (sessione successiva ~30-60min): 3 wrapper aider-cosmetic + aider-refactor + aider-groq su task piccoli reali. Non bloccante per closure (gia' avvenuta), validation tecnica end-to-end.
3. **D SPRINT_02 abbozzo** (sessione 19/05 o prima): post-Max scenario A operativo. Bullet "stack ADR-0017 hot-restart procedure" + tier routing operative + privacy validation Synesthesia (post-agosto).

Side-tasks opzionali: cleanup PR esterni (#97 Game-Database 23gg vecchio, #105 doc 1-line, #10 compass, #61 evo-swarm digest) -- non bloccanti.

## Next session restart: cosa leggere per ripartire

Ordine raccomandato:
1. `CLAUDE.md` -- convenzioni progetto autoritative
2. Questo file (`COMPACT_CONTEXT.md`) -- snapshot stato corrente
3. `AGENTS.md` SE sessione e' Codex/OpenCode/sandbox-based -- preamble anti-confusion
4. `STATUS_MULTI_REPO.md` -- dashboard cross-repo (Game Sprint Impronta, Dafne Atto 2)
5. `BACKLOG.md` + `OPEN_DECISIONS.md` -- cosa e' aperto
6. `SPRINT_01.md` (close imminente) o `SPRINT_02.md` (quando creato)
7. ADR rilevanti se task tocca topic noto

Memory auto-caricata via `~/.claude/projects/.../memory/MEMORY.md`.
