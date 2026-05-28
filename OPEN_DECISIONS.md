# OPEN_DECISIONS

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/OPEN_DECISIONS.template.md`.
>
> Per tutto ciò che è ambiguo ma **non abbastanza bloccante** da fermare l'intera sessione. Decisioni vision-sensitive / core-changing vanno in ADR separato.

---

## Snapshot 2026-05-28 (player-recap)

**Stato**: 6 OD CLOSED (001/002/003/004/006/008), **2 OD EVALUATING** (005, 007). Le decisioni vision/architettura vivono in `docs/adr/` (24+ ADR). Cose che impattano cross-repo o l'utente sono tracciate nei `BACKLOG.md` / `STATUS_MULTI_REPO.md` / `JOURNAL.md` corrispondenti.

**Amendment 2026-05-28 pomeriggio**: chiusura iniziale di OD-005 + OD-007 (commit `93b4810`) era una scorciatoia ("zero friction = chiudo") senza valutare se applicare la proposta originale. Eduardo ha segnalato il pattern. Le due OD sono state riaperte come EVALUATING: metodo corretto = autoresearch + decision build vs strong-skip-with-rationale, non solo conteggio assenza di friction. Le 4 chiusure genuine (001/002/003/004/006/008) restano valide perche' o gia' implementate o decise con metodo all'epoca.

| OD | Domanda originale (in italiano) | Verdict | Cosa devi fare adesso |
|----|----------------------------------|---------|------------------------|
| OD-001 | Quale scenario budget post-Claude-Max? | ✅ CLOSED (A full-sovereign, ADR-0015 Accepted) | Niente |
| OD-002 | Fix cp1252 Windows wrapper tiene? | ✅ CLOSED (n=15 dogfood clean) | Niente (re-trigger solo se crash UnicodeEncodeError in SPRINT_02) |
| OD-003 | Default tier 3 cloud: Groq vs Cerebras? | ✅ CLOSED (Cerebras 8B cosmetic + Groq 70B behavior) | Niente |
| OD-004 | Schema DECISIONS_LOG ibrido funziona? | ✅ CLOSED 2026-05-28 (ratificato empirico: 10 Decisioni in 5 settimane, zero confusione) | Niente. Continua schema attuale |
| OD-005 | Serve FIRST_PRINCIPLES_INFRA_CHECKLIST? | ✅ CLOSED 2026-05-28 (MINIMAL-BUILD shipped: `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` root) | Usalo prima di refactor / reboot / "vale la pena tenere?" |
| OD-006 | Constraint-count come 2a dimensione routing? | ✅ CLOSED (ADR-0016 Proposed n=11 data points) | Niente |
| OD-007 | AA01 capability registry / scan automatico? | 🔄 EVALUATING (chiusura iniziale scorciatoia, riaperta) | Design evaluation + pilot vs strong-skip-with-method in arrivo |
| OD-008 | Cross-repo Phase B Day 7 closure tracking? | ✅ CLOSED 2026-05-28 (codemasterdd-side: Phase B closure 2026-05-14 confermata in STATUS_MULTI_REPO + Game [OD-024..031] post-cutover audit ✅ SHIPPED + ADR-0024 addendum shipped PR #55) | **Lato codemasterdd niente**. Side-note opzionale: Game `OPEN_DECISIONS.md` ha ancora OD-023 marcata "APERTA 2026-05-12" -- housekeeping Game-side quando vuoi (non blocca nulla) |

**Decisioni vision/architettura**: vivono in `docs/adr/` (24+ ADR Accepted). Per cose nuove rilevanti usa ADR-NNNN MADR format (vedi `docs/adr/0000-template.md` se esiste oppure copia struttura ADR esistente).

**Pattern operativo non-ADR** (per future cose minori): apri una nuova OD-NNN qui sotto con i campi standard (Livello / Stato / Ambiguità / Perché conta / Miglior default proposto / Rischio / File / Prossima azione + Trigger reactivation se applicabile).

---

### [OD-001] ~~Scenario Budget Fase 7 (ADR-0015)~~ **CLOSED 2026-04-24 (Proposed) → ratificato 2026-05-07 (Accepted)**

- **Livello**: system / workflow / budget
- **Stato**: **CLOSED + RATIFIED** — formalizzato in **ADR-0015 Proposed 2026-04-24** → **Accepted 2026-05-07** (sessione Fase 6 closure, PR #4 mergeato). Opzione A (full-sovereign $0-50/anno) confermata, con **deroga esplicita criterio #3 privacy** (Synesthesia dormant fino esame UniUPO ~ago 2026, retroattivo a riattivazione).
- **Ambiguità originale**: quale scenario adottare post-Claude Max (2026-05-19)? (A full-sovereign / B ibrido Pro / C extension)
- **Decisione finale**: A — full-sovereign. B declassato (quality parity 5/5 stack + 70B cloud parity vs 14B Q2 local empirically confermata). C scartato (costo bridge 3 mesi ingiustificato senza lavoro reale su Synesthesia).
- **File coinvolti (output)**: `docs/adr/0015-fase7-budget-decision-full-sovereign.md` (Accepted), `DECISIONS_LOG.md` aggiornato.
- **Trigger Accepted ratificati**: soft-override esteso n>=12 con 5 rationale additivi (trigger ADR-0008 confermato a #12, behavior 5/3 superato 167%, fail rate 8.3%, zero silent-corruption, no dogfood sintetici).

---

### [OD-002] ~~Fix cp1252 Windows wrapper — tenere o sostituire~~ **CLOSED 2026-05-07 (soglia raggiunta)**

- **Livello**: system / tooling
- **Stato**: **CLOSED — non bloccante**. n=15 cumulative dogfood + smoke (Fase 6 closure) **senza retry loop naturale osservato**. Trigger di pazienza ADR-0014 raggiunto: il fix `chcp 65001 + PYTHONIOENCODING=utf-8` deployato ha tenuto in tutti i task reali; nessun crash UnicodeEncodeError post-deploy. Switch alternative (PowerShell wrapper M3) **deferred** senza trigger empirico.
- **Ambiguità originale**: il fix tiene sotto retry loop reale? Oppure serve switch a PowerShell wrapper o `aider --no-pretty` cumulativo?
- **Decisione finale**: **mantenere fix `.cmd` deployato**. Re-trigger condizionale: se ≥1 crash UnicodeEncodeError emerge in SPRINT_02 (T1 SPRINT_02 trigger) → riapertura via M3 backlog (PowerShell wrapper alternative).
- **Perché conta originale**: era l'unico bug noto che bloccava stabilità wrapper cloud. Empirically risolto.
- **File o moduli coinvolti**: `~/.local/bin/aider-*.cmd` (6 file invariati), `logs/aider-delegation-2026-04.md` (12 entries clean).
- **Prossima azione**: nessuna proattiva. Solo reactive monitoring durante T2 SPRINT_02 (dogfood organico continuativo).

---

### [OD-003] ~~Default online tier 3: Groq vs Cerebras~~ **CLOSED 2026-05-10 (formalizzazione + drift sync)**

- **Livello**: workflow / tooling
- **Stato**: **CLOSED** — opzione 1 ratificata (Cerebras 8B default cosmetic, Groq 70B default behavior). Convenzione gia' implicita in `MODEL_ROUTING.md` (linee 72-74) ma OD non era stato formalmente chiuso. Drift fix di formalizzazione.
- **Ambiguità originale**: entrambi free tier, entrambi 100% quality bench, speed comparable (630 vs 733 tok/s). Fai default per classe diversa o restano simmetrici?
- **Decisione finale**: **opzione 1** — Cerebras 8B (cosmetic, +16% speed marginal) + Groq 70B (behavior, capability superiore). Rationale "modello piu potente per task piu complessi" ortogonale a speed. Simmetricizzare non aggiunge valore.
- **Perche' chiuso ora**: convenzione gia' applicata empirica in `MODEL_ROUTING.md` matrice routing classe-based; nessun behavior-critical Cerebras n>=5 raccolto perche' workflow naturale ha gia' seguito opzione 1 (memoria muscolare). Non aspettare n=5 e' lean honest: la decisione e' presa, falsificabile retroattivamente solo se emerge evidence contraria.
- **File coinvolti**: `MODEL_ROUTING.md` linee 72-74 (gia' allineato), `CLAUDE.md` sezione wrapper (gia' allineato).
- **Trigger ri-evaluation**: se >=2 task behavior-critical Cerebras 8B PASS reali (1st-try, no retry escalation a Groq 70B) emergono in dogfood organico SPRINT_02+ -> riconsiderare opzione simmetrica con ADR addendum. Pattern atteso opposto (Cerebras 8B safe-fails behavior, fallback Groq 70B).

---

### [OD-004] ~~Schema `DECISIONS_LOG` — indice ADR vs lista Decisione NNN~~ **CLOSED 2026-05-28 (proposta ratificata empirica)**

- **Livello**: repo / documentation
- **Stato**: **CLOSED** — schema ibrido confermato dall'uso reale. Ground-truth `DECISIONS_LOG.md` (2026-05-28): sezioni `## ADR index (strategiche)` + `## Decisioni non-ADR (operative minori)` coesistono pulite; n=10 Decisioni (001..010) raccolte tra 2026-04-23 e 2026-05-18, zero confusione signal cross-sessione, zero misclassification. Trigger "se dopo 2+ sessioni il formato ibrido genera confusione" mai attivato in 5 settimane / decine di sessioni.
- **Ambiguità originale**: il framework archivio prescrive formato "Decisione NNN numerata". Il progetto ha già 14 ADR MADR più ricchi. Come riconciliare?
- **Decisione finale**: **ibrido confermato** — ADR index + sezione "Decisioni non-ADR" con formato Decisione NNN per operative minori. Mantiene entrambi i contratti.
- **File coinvolti**: `DECISIONS_LOG.md` (sezioni live), `CLAUDE.md`.
- **Reactivation trigger**: se in futuro una sessione legge il file + classifica wrong-section una nuova decisione → ADR dedicato per formalizzare convention. Finora N/A.

---

### [OD-006] ~~Routing threshold: constraint count per delegazione cloud vs locale vs manuale~~ **CLOSED 2026-04-24**

- **Livello**: workflow / tooling
- **Stato**: **CLOSED** — formalizzata in ADR-0016 (Proposed 2026-04-24). Pattern confermato da n=6 data points cross-tier + n=11 cumulative. Follow-up raccolta n≥3 data points addizionali verso Accepted tracciato in BACKLOG H6 (chiuso anch'esso).
- **Ambiguità**: Groq 70B cloud degrada significativamente su task behavior-critical con ≥5 constraint espliciti (dogfood #7: 20% compliance). Qwen 7B local degrada su task cosmetic con ≥2 constraint trasformativi (dogfood #8: 50% compliance). **Soglia routing quantitativa va formalizzata**?
- **Perché conta**: routing attuale classifica per **natura task** (cosmetic/behavior/strategic). Il nuovo dato suggerisce **constraint-count** come seconda dimensione discriminante — potenziale revisione della decision matrix CLAUDE.md.
- **Miglior default proposto**:
  - **Task con 1 constraint semplice** (add-only, fix puntuale): 7B local OK
  - **Task con 2-3 constraint fix+transform**: 14B Q2 local o 70B cloud (entrambi ~85% attuali)
  - **Task con ≥5 constraint strict**: **rewrite manuale Claude Code** — delegare è anti-pattern empiricamente
- **Rischio se ignorata**: delegazioni falliscono silently, user deve fare rescue retroattivo — già successo dogfood #7 con return-value divergence blocking bug.
- **File o moduli coinvolti**: `CLAUDE.md` sezione "Priorità modelli AI" + `docs/patterns/delegation-to-aider.md` + `MODEL_ROUTING.md`.
- **Prossima azione consigliata**: raccogliere altri n≥3 dogfood con constraint-count variabile per confermare pattern. Se confermato → ADR dedicato (0016?) formalizza second-dimension routing.

---

### [OD-005] ~~`FIRST_PRINCIPLES_GAME_CHECKLIST` sostituito da cosa?~~ **CLOSED 2026-05-28 pomeriggio (BUILD shipped)**

- **Livello**: workflow / documentation
- **Stato**: **CLOSED -- BUILD**. Artefatto creato: `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` root (~230 righe, adattato dal template game). Risolve la dipendenza circolare di `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/REPO_AUTONOMY_READINESS_CHECKLIST.md` sezione D ("Esiste una checklist first-principles compilabile") per repo infra-only.
- **Metodo applicato**: (1) currency-gate interno -> mapping primitive esistenti (skill `superpowers:first-principles-game` = game-biased; `REPO_AUTONOMY_READINESS_CHECKLIST` sez D punta circolarmente al game-template; ADR-0005 YAGNI = ancora filosofica). (2) Autoresearch industria (WebSearch 2 query, 2026-05-28): SRE Workbook + AWS/Azure Well-Architected + ATAM + ADR best-practices = nessuno offre "test di cancellazione asset non-runtime" + "triade fondamentale + decision gate" in formato lean-checklist. Gap confermato reale.
- **Decisione finale**: **MINIMAL-BUILD**. Adattamento drop-game-only (Rule of Threes / Player Dynamics game-specific) + keep-generic (test cancellazione / triade / rational design / decision gate) + add infra-framing (Operator dynamics = umano + agent multi-CLI; Bootstrap onboarding = nuova sessione/clone vs progressione apprendimento gameplay).
- **File coinvolti (output)**: `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` (nuovo, root). `DECISIONS_LOG.md` Decisione 002 amendment.
- **Reactivation trigger**: se in futuro un altro repo infra-as-code (Synesthesia backend, repo cliente) ha bisogno della stessa checklist -> riutilizzo (artifact e generico).

---

### [OD-008] ~~Cross-repo dependency Game OD-023 -- Phase B Day 7 closure 2026-05-14 sub-event di ADR-0024~~ **CLOSED 2026-05-28 (codemasterdd-side)**

- **Livello**: cross-repo strategic (codemasterdd <-> Game)
- **Stato**: **CLOSED codemasterdd-side**. Ground-truth 2026-05-28: (a) `STATUS_MULTI_REPO.md` riga 603 conferma Phase B Day 7 formal closure eseguita 2026-05-14 come sub-event di ADR-0024; (b) Game `OPEN_DECISIONS.md` cluster `[OD-024..031] ai-station ecosystem audit verdicts` = ✅ 8/8 SHIPPED cross-stack 2026-05-14 (downstream del cutover); (c) codemasterdd ADR-0024 addendum "Sub-events timeline" + scope-disjoint clarification shipped PR #55. **Caveat residuo, NON codemasterdd**: Game `OPEN_DECISIONS.md` OD-023 header marca ancora "APERTA 2026-05-12" -- marker stale Game-side, housekeeping Eduardo opzionale, non blocca nulla. Pregresso Phase B archive riconciliato, codemasterdd dependency tracking completo.
- **Ambiguita originale**: Game `OPEN_DECISIONS.md` OD-023 (APERTA 2026-05-12) cita esplicitamente codemasterdd ADR-0024:
  > "Cross-repo ai-station alignment: ADR-0024 Proposed 2026-05-09 = Vue3 archive soft-deadline 2026-09-30 (4 mesi). Conflict apparente con Game/ ADR-2026-05-05 (7gg grace). Risolto via Opt B+C combined: scope disjoint (Game = FE apps/play/ only, ai-station = Vue3 repo-wide). Amendment ai-station ADR-0024 § Sub-events timeline raccomandato Sprint Q+ NON oggi."
- **Decisione codemasterdd-side**: ADR-0024 addendum shipped questa PR chiarisce scope disjoint senza alterare original decision (soft-deadline 2026-09-30 invariata). Phase B web archive 2026-05-14 = **sub-event** di Vue3 codebase-wide archive 2026-09-30.
- **Perche conta**:
  - Tracciabilita cross-repo dependency (codemasterdd OPEN_DECISIONS riflette stato Game OD-023)
  - Anti-drift: future sessione legge OD-008 + capisce immediate che Phase B 14/5 NON archive Vue3 repo-wide
  - Game OD-023 path verdict (Path C ORA + Path A Day 8) NOT codemasterdd action -- Eduardo direct Game-side
- **File coinvolti questa PR**:
  - `docs/adr/0024-vue3-archive-godot-canonical-timeline.md` (addendum "Sub-events timeline")
  - `STATUS_MULTI_REPO.md` (entry forthcoming 2026-05-14 + Game row OD-023 mention)
  - `OPEN_DECISIONS.md` (questa OD-008)
- **Prossima azione**: monitor Game OD-023 resolution 2026-05-14 post-Phase-B closure. Update OD-008 to CLOSED quando Game OD-023 chiusa + Phase B web archive completata.
- **Reactivation trigger**: Game/ ADR-2026-05-05 amendment (es. grace extension oltre 7gg, scope changes, abort) -> potenziale ADR-0024 follow-up addendum
- **Update 2026-05-12 pomeriggio**: Game local checkout pulled Path A reset --hard origin/main (post Protocol 1+2 investigation safe-confidence). 13 backup branches `aa01/cap-*` preservano Sprint Impronta CAP-02..15b content + stash safety net 295 file WIP refactor abandoned pre-26/04. Game OD-023 monitoring invariato. TKT-P2 Phase D cross-stack chain COMPLETE Godot-v2 (PR #248 + #249 merged questa sessione). Phase B Day 7 closure execution Eduardo-direct 14/5 mattina UTC (NO codemasterdd action).

---

### [OD-007] AA01 capability registry / scan function -- **EVALUATING 2026-05-28 (re-opened post shortcut-closure)**

- **Livello**: workflow / tooling (AA01-side, esterno a codemasterdd)
- **Stato**: **EVALUATING** — la chiusura precedente (2026-05-28 mattina, commit `93b4810`) si appoggiava solo al conteggio "zero learning friction-related" senza valutare il design del registry. Counter task = 18+ senza friction promossa NON e' segnale conclusivo (la friction puo' essere invisibile = bias "scelgo l'agent che ricordo" non genera necessariamente lesson). **Decisione DA prendere**: pilot scan-capabilities (cost moderato, prototype script) per misurare beneficio empirico, oppure strong-skip ratificato con metodo (es. mapping manuale tool->phase nelle AGENTS.md AA01 come baseline alternativa, piu' lean del registry automatico).
- **Ambiguita' originale**: AA01 oggi sceglie tool (sub-agent codemasterdd, skill, plugin, MCP, wrapper aider) a discrezione dell'agent-in-sessione. Es. PR #39 ho usato harsh-reviewer perche' lo sapevo io, non perche' AA01 me l'abbia suggerito. Una funzione `scan-capabilities` che inventaria `.claude/agents/` (18 sub-agent codemasterdd) + skill + plugin + MCP + wrapper aider e mappa per preset/phase ridurrebbe il bias di "chi ha piu' memoria recente vince".
- **Perche' conta**: scaling oltre 1-2 agent-in-sessione, eventuale handoff cross-CLI (Claude Code / Codex / Cursor / Gemini / Cline tutti citati in AA01 AGENTS.md come master entry point), e drift di tool selection task-by-task.
- **Decisione attuale**: **opzione C aspettare 2-3 task AA01 in piu'**. Three Strikes: feature esiste solo dopo 3 task la richiedono. Counter al 11/5: **1 completed + 1 in progress** (`aa01-001` two-repos-analysis SHIP via PR #39; `aa01-002` fleet-discovery-pod-design Phase 1+2 via PR #40 in coda). Nessuna frizione tool-selection osservata in entrambi -> trigger NON ancora attivato (counter task != count frizione). Disciplina, non feature.
- **File coinvolti (futuro)**: eventuale `C:/Users/edusc/aa01/scripts/scan-capabilities.sh` + `.aa01/capability-registry.json` + AGENTS.md AA01 update sezione "Adattabilita' multi-asse".
- **Trigger reactivation**:
  - Task AA01 #2 o #3 dove emerge **frizione concreta** del tipo "quale agent uso per Phase X?" / "duplicazione: scelgo sempre lo stesso agent perche' e' l'unico che ricordo" / "skill X esiste ma non ho saputo usarla"
  - OR Eduardo identifica un caso d'uso specifico (es. AA01 task multi-CLI handoff dove serve sapere cosa puo' fare ogni CLI)
- **Tradeoff principali documentati**:
  - **Boundary**: AA01 in `C:/Users/edusc/aa01/` separato da codemasterdd. Lo scan deve sapere where-to-look (config `aa01-tool-search-paths` o env var). Cross-coupling vs reusabilita'.
  - **Staleness**: skill/agent/plugin cambiano session-by-session. Scan one-shot all'avvio, refresh on-demand, o cache TTL?
  - **Three Strikes governance**: stessa disciplina che AA01 applica a preset/rule, ora applicata a feature-internal AA01.
- **Prossima azione**: nessuna proattiva. Solo reactive monitoring durante task AA01 futuri (aspetta task #2 / #3 per signal).

---

## Regola pratica

Se la decisione:
- blocca davvero il gameplay core / vision strategica (es. ADR-0001 fondamentale)
- cambia scope/priorità prodotto
- impatta più sistemi in modo irreversibile

**non basta questo file**: serve ADR esplicito in `docs/adr/` + approvazione utente esplicita.
