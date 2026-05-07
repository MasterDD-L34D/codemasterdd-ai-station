# COMPACT_CONTEXT

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/COMPACT_CONTEXT.md`.
>
> Aggiornare in rituale chiusura sessione (CLAUDE_OPERATING_RULES.md #9).

## Progetto
- **Nome**: CodeMasterDD AI Station
- **Versione del compact**: v12 (sessione 2026-05-08: audit coerenza doc + governance refresh post 7/5 sera + Dafne 4 PR closure batch)
- **Data ultimo aggiornamento**: 2026-05-08 sessione corrente

## Stato attuale
- **Barra globale ~96%** (+1 da v11): Fase 6 CLOSED -- ADR-0015 e ADR-0017 entrambi Accepted 2026-05-07. Tutti i PR cleanup esterni completati 7/5. Resta finestra transition 07/05 -> 19/05 (Claude Max expiration, 11gg residui).
- HEAD `5828909` su origin/main (post merge PR #4-#10 in giornata 7/5). Worktree corrente `mystifying-thompson-82bb43` allineato a main, working tree pulita.
- **Stack ADR-0017**: scaffold opt-in (Docker Desktop non auto-start). Hot-restartable in <60s con `docker compose up -d`. DB persistence Postgres+SQLite preservata. 7+ Langfuse traces ancora persistiti.
- **Agent ecosystem ADR-0018**: 12/18 ready, 6/18 draft trigger-gated. Status invariato dal 24/04.
- **Codex `/structural-reset` REJECTED + chiuso + delete remote**: branch difensivo Codex Cloud sandbox-confusion (assunzione "transplanted, paths missing" smentita empiricamente, 9/9 path target presenti). Cherry-pick astratto: ADR-0021 + AGENTS.md + encoding policy.
- **PR pulito post-7/5**: #1 ADR-0020 mergeato 25/04. #2 ADR-0021 + #3 [REJECTED] + #4 fase6-closure + #5 sprint-02 + #6 smoke-sovereign + #7+#8 godot-v2 governance + #9 aider-pattern + #10 master_prompt-handoff tutti chiusi 7/5. Coda PR codemasterdd vuota.

### Gap operativo 25/04 -> 07/05 (non-stagnation)

Eduardo ha lavorato attivamente in altri repo (silent driver mode):
- **Game**: Sprint Impronta Ondata 1, 8+ commit clusterati 25-26/04, branches `aa01/cap-11..15` (telemetry + onboarding v2 + imprint phase V2). HEAD `5f42757a` (26/04 12:53 CET). **Pausa Sprint Impronta dal 26/04 (~12gg)**. PR #2108 Claude Code session swarm-distillation aperto 7/5 sera (non triagato).
- **Dafne swarm**: Atto 2 day 11+ -> day 12+, 10 commit cumulative (5 al 7/5 mattina + **4 nuovi 7/5 sera che chiudono OD-002+OD-003+OD-006** + 1 nuovo 8/5 00:29 PR #71 lock fix). HEAD `a87da39`. Decision debt cleanup massiccio.
- **Game-Godot-v2**: 215 PR mergeati totali (+4 dal 7/5 sera). Path A canonical CHIUSO end-to-end 7/5.
- **AA01**: silent driver del Sprint Impronta Game, capability-by-capability. 2 task PROPOSED del 25/04 (#001 voice-test + #002 day-5-post-session-ritual) restano in workspace.
- **codemasterdd**: dataset Fase 6 fermo a n=12 dal 24/04 -- shift naturale di focus quando policy hub ha completato il ciclo (trigger ADR-0008 confermato a #12).

## Obiettivo di questa fase

**Transition window 08/05 -> 19/05** (11 giorni residui Claude Max):
- Smoke test 3 wrapper sovereign empirico -- gia' eseguito PR #6 in giornata 7/5 (T1 SPRINT_02 anticipato)
- SPRINT_02 abbozzo -- gia' eseguito PR #5 in giornata 7/5
- Cleanup PR esterni opportunistico -- **TUTTI completati 7/5**: Game-Database #97 closed-stale, #105 merged, compass-marketplace #10 merged, evo-swarm #61 merged
- Triage opzionale: PR #2108 Game (swarm-distillation routine 7/5 sera, governance interna Game decide)
- 8/5: governance refresh post 7/5 sera (questa sessione) -- STATUS_MULTI_REPO + COMPACT v12
- 19/05: disattivazione Claude Max, transizione a wrapper sovereign + Ollama

## Cosa e' gia' stato fatto

### Sessione 2026-05-08 (corrente -- audit coerenza doc + governance refresh)

#### Audit coerenza doc + scope cross-repo
Reality-check 6 governance file vs stato reale post 7/5 sera + 8/5 mattina. Drift identificati:
- COMPACT v11: HEAD `39f97da` claim vs reale `5828909` (mergiate PR #4-#10)
- STATUS Game-Godot-v2: 211 PR vs reale 215 (+4 post 7/5 sera)
- STATUS Game: "0 PR open" vs reale 1 (PR #2108 swarm-distillation Claude Code session 7/5 22:19 UTC)
- STATUS Game: claim "in pieno corso" 7/5 vs reale pausa Sprint Impronta dal 26/04 (~12gg, drift accuracy preesistente perpetuato in v1 refresh, fixato in v2)
- STATUS Dafne: HEAD `1e14253` vs reale `a87da39` (+5 commit: 4 il 7/5 sera + 1 il 8/5 00:29 CET)
- STATUS Dafne open items: OD-002+OD-003+OD-006 chiusi vs status precedente "open"

Cross-repo positives confermati: JOURNAL 7/5 entry completa, DECISIONS_LOG ha Decisione 004+005, ADR coerenti, BACKLOG H-items chiusi correttamente, OPEN_DECISIONS OD-001+OD-006 chiusi, AGENTS.md aderente ADR-0021.

#### Governance refresh chirurgico (questa sessione)
Branch dedicato `claude/governance-refresh-2026-05-08`:
- STATUS_MULTI_REPO: refresh date 8/5, sezioni Game/Dafne/Game-Godot-v2 aggiornate, header tabella, scheduled checkpoint riga aggiunta
- COMPACT v11 -> v12 (questo file)
- CLAUDE.md sezione Game-Godot-v2 PR count cosmetic fix (211 -> 215) + sezione Game pausa Sprint Impronta corretta + Stack installato +1 riga "modelli aggiuntivi"

Nessun file core toccato (JOURNAL/DECISIONS_LOG/ADR/BACKLOG/OPEN_DECISIONS/SPRINT_02/AGENTS.md preservati).

#### Pre-Max checklist tecnica (locale read-only, eseguita questa sessione)
Verifica wrapper sovereign + API keys + stack hot-restart-ready in vista 19/05 expiration:
- 6 wrapper aider-* presenti in `C:/Users/edusc/.local/bin/` (cosmetic, refactor, groq, cerebras, gemini, openai) + aider-log + aider.exe v0.86.2
- API keys `~/.config/api-keys/keys.env` 609 bytes presente; Aider config global `~/.aider.conf.yml` 235 bytes presente
- Aider 0.86.2, promptfoo 0.121.7 (vs latest 0.121.10, lag minor), 16 modelli Ollama presenti
- Docker compose `infra/docker-compose.yaml` config validation OK (`docker compose config --quiet` exit 0)
- Drift trovato: CLAUDE.md "Stack installato" Ollama documentava 8 modelli, reali 16. +1 riga "modelli aggiuntivi" added.

Esito: sovereign stack pronto per 19/05 transition. Nessun blocker tecnico.

#### Triage operativo PR #2108 Game (chat-only delivery)
PR #2108 Game (docs research distillation run #5 evo-swarm). Analisi codemasterdd:
- Safety: docs-only additive (1 file nuovo +211/-0), no edit `data/core/`, gate ratifica preservato (5 open questions per game-side review)
- CI: governance + paths-filter SUCCESS, altri SKIPPED (atteso docs-only)
- Branch: `claude/swarm-distillation-2026-05-08` -> Claude Code session, NON Dafne automation
- Conflitti: nessuno, mergeable
- Pattern coerente vs altri `docs/research/2026-04-25-skiv-*.md` esistenti

Raccomandazione: **merge-ready** dal POV codemasterdd. Decisione merge resta Game-side per ownership boundary CLAUDE.md ("monitora solo"). Tentato `gh pr comment 2108` -> sandbox correttamente bloccato (External System Write su repo non-codemasterdd richiede auth esplicita, non coperta da Auto Mode generico). Lezione salvata in `feedback_external_repo_action_boundary.md`.

### Sessione 2026-05-07 (resume + Codex + Fase 6 closure)

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

1. **Commit + PR governance refresh 2026-05-08** (sessione corrente). STATUS_MULTI_REPO + COMPACT v12 + CLAUDE.md cosmetic fix. Branch `claude/governance-refresh-2026-05-08`.
2. **Pre-Max checklist tecnica** (sessione opzionale ~30min ~10/05-15/05): verifica wrapper sovereign aider-* funzionanti senza Max OAuth, API keys cloud ancora valide, stack ADR-0017 hot-restart prova singola. Non bloccante.
3. **Triage opzionale PR #2108 Game** (5min, low priority): valutare merge/comment/close swarm-distillation run #5 routine. Governance interna Game-driven (non codemasterdd-driven).

Side-tasks gia' DONE 7/5: cleanup 4 PR esterni completato. Smoke test sovereign T1 SPRINT_02 anticipato (PR #6). SPRINT_02 abbozzo (PR #5).

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
