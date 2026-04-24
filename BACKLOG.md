# BACKLOG

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/BACKLOG.md` + sezione "Primo sprint consigliato" inline.
>
> Normalizzato da: follow-up ADR non chiusi + "Da fare" JOURNAL recenti + criteri closure ADR-0014 + bug noti aperti.

## Priorità alta

- [x] ~~**H1** — Dogfood behavior-critical n+1 (target ≥5).~~ **DONE 2026-04-24 auto-mode**: #12 retry-logic parity bench-ollama (14B Q2 local), partial success con inherited-bug finding. Dataset behavior: 3 full + 1 partial + 1 reject = **5/5 target ✅**. Commit `dce8ee4`.
- [ ] **H2** — Dogfood cosmetic fino n≥10 cumulativo (attuale 7 dopo #11). Gap 3. Mix local/cloud. Opportunistic batch.
- [ ] **H3** — Monitoring empirico fix cp1252 durante retry loop naturale. **ANCORA PENDING**: 9 dogfood consecutivi (#4-#12) sono stati 1st-try o 2nd-try auto senza retry loop naturale. Soglia pazienza: se nessun trigger entro n=15, considerare test sintetico controllato.
- [x] ~~**H4** — Cost tracking cumulativo mensile `ccusage` + cloud logs.~~ **DONE 2026-04-24 auto-mode** (anticipato vs target fine-mese): sezione "Aggregati aprile 2026" popolata in `logs/aider-delegation-2026-04.md`. Cumulative cloud $0.0148 / 0.074% budget. ccusage Max $383.36 (non-OOP). Trigger ADR-0008 FULL-SOVEREIGN VIABLE confermato empiricamente. Refresh finale fine-mese (2026-04-30) residuo tracked.
- [x] ~~**H5** — Review settimana 2 formale (~2026-05-07): count dogfood, fail rate, ETA chiusura. Decisione on-track / extension.~~ **DONE 2026-04-24 (anticipata)**: sprint 01 early-hit ha reso review immediata sensata. Esito: **on-track, no mid-course correction**. 2/4 criteri ADR-0014 PASS (quality, cost), 2/4 on-track (reliability 11/20, privacy 1/3). Next checkpoint settimana 4 (~2026-05-17). Dettaglio in JOURNAL entry `2026-04-24 (review settimana 2 anticipata)`.
- [x] ~~**H6** — Validare empiricamente OD-006 (routing threshold constraint-count).~~ **DONE 2026-04-24**: n=6 data points cross-tier raccolti (dogfood #6/#7/#8/#9/#10/#11). OD-006 **chiuso via ADR-0016** (Proposed 2026-04-24). Follow-up: raccogliere n≥3 data points addizionali per gap (constraint=4, 2-transform LOCAL, 5-strict LOCAL) verso ADR-0016 Accepted.

## Priorità media

- [x] ~~**M1** — JOURNAL entry 2026-04-23 documentando integrazione framework archivio + 11 file governance + rationale.~~ **DONE**: entry in JOURNAL `2026-04-23 (sera — integrazione framework archivio)` + follow-up `2026-04-24 notte` aggiunta.
- [x] ~~**M2** — Memory refresh `project_session_resumption.md`.~~ **DONE 2026-04-24**: HEAD 9bcc2a4, tabella 11 dogfood, ADR-0016 reference, Sprint 01 early hit.
- [ ] **M3** — Wrapper PowerShell alternative (`aider-groq.ps1` etc.) **se H3 fallisce**. Condizionale. Trigger: 1° crash cp1252 post-deploy fix. Finora nessun crash osservato (8 dogfood consecutivi clean).
- [x] ~~**M4** — Integrate bench framework ↔ dogfood tracking: colonna "quality pass" nel log.~~ **DONE 2026-04-24**: insight = "colonna per-entry" non ha senso (quality bench è per-modello fisso). Implementato come reference table aggregata: template esteso con sezione "Quality bench ↔ reliability correlation" + diagnostic patterns. Log reale popolato con snapshot (5 stack al 100% pass@1 vs reliability variabile → conferma constraint-specific fail mode ADR-0016). Commit `70f4f69`.
- [ ] **M5** — Synesthesia privacy first-violation test: ≥1 sessione che tocchi `views/` (cloud OK) + `controllers/` (sovereign-only). Criterio 3 ADR-0014. **Priorità residua principale Sprint 01** (1/3 ancora).
- [x] ~~**M6** — Commit delle 11 modifiche governance + entry JOURNAL.~~ **DONE 2026-04-23/24**: 11 commit sessione cumulative (sera + notte).

## Priorità bassa

- [ ] **L1** — Re-bench discriminant hard problems custom (non-Leetcode). Fuori scope Fase 6.
- [ ] **L2** — Deepseek-r1 num_predict=5000 + extract thinking migliorato. Diminishing returns.
- [ ] **L3** — Cerebras paid tier evaluation (gpt-oss-120b, qwen-3-235b). Trigger: gap quality reale.
- [ ] **L4** — Gemma 4 multimodal dogfood reale. Opportunistic.
- [ ] **L5** — Skill install policy audit periodico (cadence 3 mesi).

## ADR-0017 rollout (Sprint 02, aperto 2026-04-24)

- [x] ~~**U0-scaffold** — Stack scaffolding completo (code + config + docs)~~ **DONE 2026-04-24 auto-mode maratona**: `infra/` + `scripts/quality-bench/promptfoo.*` + `apps/dogfood-ui/` + `.claude/agents/*` (5 sub-agent). 31 file nuovi, ~2700 LOC validati (Python AST + YAML parse + docker-compose config OK). Commit `6924482`. Eduardo può avviare stack quando pronto.
- [ ] **U0-test** — Step 0 quick-win: abilita `aider --browser`, prova 1-2 sessioni dev-loop. Gate: UX accettabile? Se sì → procedi. Se no → deferred step 1+.
- [x] ~~**U1-test** — Step 1 LiteLLM Proxy live infrastructure~~ **DONE 2026-04-24/25 sessione successiva auto-mode**: container `codemasterdd-litellm` UP 6h+, `/health/readiness` 200 (DB connected, success_callback `langfuse` attivo + 8 altri hook, v1.82.6). Config `infra/litellm/config.yaml` espone 10 modelli (7 local + 3 cloud free + 1 cloud paid) + master key via env + budget cap 50$/30d. **Gap residuo**: creazione virtual key via admin UI (`http://localhost:4000/ui`) richiede azione manuale Eduardo pre U3-test eval.
- [x] ~~**U2-test** — Step 2 Langfuse live~~ **DONE 2026-04-24/25**: container `codemasterdd-langfuse-web` UP 6h+, `/api/public/health` 200 (v2.95.11). Callback LiteLLM → Langfuse validato (7+ traces + 7 observations persistiti in Postgres durante sessione maratona). **Gap residuo**: creazione project + API key via UI (`http://localhost:3000`) se si vuole dashboard separato per queries.
- [ ] **U3-test** — Step 3 promptfoo live: promptfoo v0.121.7 installed ✅. `scripts/quality-bench/promptfoo.config.yaml` valid, punta a Proxy `:4000` con virtual key `sk-local-testkey` (placeholder — da creare via LiteLLM admin UI). Eval run `cd scripts/quality-bench && promptfoo eval` bloccato fino a virtual key setup. Target ~15min manual.
- [x] ~~**U4-test** — Step 4 dogfood-ui live~~ **DONE 2026-04-24/25**: HTTP 200, v0.2.0, `/api/health` returns status ok (litellm/langfuse reachable, dafne unreachable atteso, db.count=0). 11 route registered (UI + API + Dafne proxy). **Finding side-effect**: Flask host process lanciato da worktree `mystifying-keller-84cb03`, DB path hardcoded a quel worktree → DB separato per-worktree non intenzionale. Non bloccante finché si legge dati dal log markdown (source of truth), ma U6 migrazione va orientata al worktree main/canonical.
- [ ] **U5** — ADR-0017 ratification: se U0-U4 test completati entro ~2026-05-17 review settimana 4 senza blocker → Status → Accepted + update CLAUDE.md scope repo evolution. **U1/U2/U4 validated 2026-04-25 auto-mode**; U3 gate su virtual key manuale (Eduardo ~15min); U0-browser tangenziale.
- [ ] **U6** — Migrazione entries existing log → dogfood.sqlite: parser markdown che legge `logs/aider-delegation-2026-*.md` e popola DB. Opportunistic post-U4. ~1h effort. **Caveat post U4-test**: DB path dipende da CWD di launch; pattern corretto è lanciare da worktree canonical (main) o passare path esplicito via env var.

## Bloccato da

- **B1** — ADR-0015 Budget decision: richiede chiusura Fase 6 (tutti 4 criteri ADR-0014). ETA sblocco ~2026-05-20.
- **B2** — Fase 7 migration finalization (rinuncia Claude Max): dipende da 2026-05-19 (hard date) + B1.
- **B3** — Extension Fase 6 mirata con ADR-0014 Addendum: dipende da review settimana 2+4.

---

## Primo sprint consigliato

> Dettaglio completo in `SPRINT_01.md`. Sintesi qui per navigazione rapida.

- **Obiettivo sprint**: portare dataset Fase 6 da 6 → ≥12 dogfood (di cui ≥3 behavior-critical) + validare empiricamente fix cp1252 + mantenere cost tracking attivo. Finestra: **2026-04-23 → 2026-05-06** (2 settimane).
- **Task 1** — Dogfood behavior-critical cloud #2-3 [H1]: identificare 2 task behavior-critical reali in `scripts/` del repo e delegarli via `aider-groq`/`aider-cerebras` con diff + no-auto-commits. Candidato primario: retry logic su `scripts/quality-bench/run-bench.ps1`.
- **Task 2** — Dogfood cosmetic mix n+5 [H2]: JSDoc/help sections su script PS1/SH residui, portare cumulativo a ≥10.
- **Task 3** — Monitoring empirico fix cp1252 [H3/OD-002]: osservare durante T1/T2, decisione "tiene/fallisce".
- **Definition of done**:
  - ≥12 dogfood totali, ≥3 behavior-critical, 0 silent-corruption cumulative
  - 1 decisione chiara su fix cp1252
  - 1 snapshot cost mid-sprint + 1 review settimana 2 documentata
  - M6 commit eseguito

---

## Dead weight / sospetti (da NON riaprire senza trigger)

- `docs/reference/agno-ollama-snippets.md` Pattern 2 → fixato, no-op pendente.
- `docs/reference/subagents-skills-candidates.md` → catalogo dormiente, nessun install pianificato.
- `final-research-and-snippets-2026-04-21-v3.md` (root) → source material esterno, triato.
- `docs/sessions/` → log historiche, congelate.
- Task #13/#14 vecchi (deepseek eval + API keys setup) → chiusi de-facto.
- `FIRST_PRINCIPLES_GAME_CHECKLIST.md` → skipped (Decisione 002 in `DECISIONS_LOG.md`).
