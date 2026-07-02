# Research -- Jules schema reuse: stato dell'arte + piano di riuso (2026-07-02)

Studio di fine-sessione: inventario degli schemi Jules PROVATI, correzione di una
lettura sbagliata, mappa di riuso sul portfolio corrente (convergenza playtest).
Ground-truth: audit-log wrapper, digest series, JOURNAL, git log cross-repo,
logs/jules-tasks/. Autore sessione: claude-fable-5 (Ryzen).

## 1. Inventario schemi provati (con evidenza)

| # | schema | evidenza | esito |
|---|--------|----------|-------|
| S1 | Strict-prompt verbatim task-file (lista funzioni esatta + testo ## verbatim + hard constraints + acceptance) | 29 batch-PR GGv2 (#407..#447, #561..#564) + 3/3 JS (06-03) | 0 difetti shippati |
| S2 | Wrapper 5-gate fail-closed + audit append-only (`jules-dispatch.ps1`) | pagination-proof (#307) su >100 sessioni lifetime; audit = timeline ricostruibile | robusto |
| S3 | Monitor poll inline background (no .sh file) | ogni batch; 5-14 min/sessione | stabile |
| S4 | Ground-truth gate meccanico (dels==0, only-target, ASCII-add, domain-lint) | 2 difetti respinti (06-03), 0 passati; oggi 4/4 spec-exact | LA safety |
| S5 | Trio-batch + fresh-branch da origin/main + rebase-merge (trailer ADR-0011) | 29 PR; collision-gotcha documentato | standard |
| S6 | Tracker-as-queue + scan-regen (mai hand-patch, mai fidarsi del marker) | 2 volte il marker mentiva (pausa giugno "cream done"; tracker stale 99 vs 107) | Currency-Gate applicato |
| S7a | Reorg-read lane (Jules = free READER, proposta read-only) | 4/4 proposal (159/421/1489/675 doc) in logs/jules-tasks/proposals/ | provato |
| S7b | **Characterization-test lane (NUOVA, altra sessione)**: test-only, single new file, pinna il comportamento CORRENTE di una funzione freeze-zone, spec umana esatta (input/output attesi scritti nel task) | task 2026-06-25 `translatePathfinderStatblock` -> Game #3049 MERGED (JOURNAL: "freeze-zone behavior-pin, test-only") | **estende il perimetro oltre i commenti** |
| S8 | Digest cron + segnale governor (9th R0); "0 awaiting" = segnale sano | serie giugno completa (backfill #450); archive ritual R3-bis | attivo |
| S9 | Anti-pollution clause + activities[] fallback recovery | 0 sessioni FAILED-by-bloat da #299 | preventivo |
| S10 | Runbook handoff tool-agnostic | docs/runbook/godot-doc-comment-campaign-handoff.md (#310) | pronto, non consumato |

Delivery: due varianti provate. (a) **patch-extract** (REST outputs -> apply locale -> PR mio):
usata da tutta la campagna GGv2 -- io controllo il gate PRIMA che esista un PR. (b)
**PR-to-owner** (Jules apre il PR, "do NOT merge"): usata dal statblock #3049 -- gotcha
registrati nel JOURNAL 06-29 (delivery-miss -> salvage; husky/prettier ENOENT su commit
locale). Preferenza: (a) per lane mass-mechanical, (b) per one-off su repo con CI ricca.

## 2. Correzione (onesta') alla mia analisi di oggi

Avevo scritto "giugno 6-30 = zero dispatch Jules". VERO solo per il canale wrapper-Ryzen
(audit-log). FALSO in assoluto: almeno una sessione Jules e' girata ~06-25 su Game
(statblock #3049), dispatchata FUORI wrapper (jules.google manuale o altra macchina) e
gestita da un'altra sessione Claude (oversight nel flusso governor, "R3-bis archive-only").
Lezione: **l'audit-log del wrapper copre SOLO il wrapper**; la vista completa = audit-log
+ digest series + JOURNAL. L'assunzione "sole Jules handler = Ryzen" del brief di giugno
e' superata: il fleet ha ora >=2 vie di dispatch. Il dedup gate-4 resta l'unica guardia
anti-collisione cross-via: NON aggirarlo mai (-ForceBlind vietato).

L'attribuzione dei +8 doc GGv2 interim resta valida (il statblock era Game, test-only).

## 3. Mappa di riuso -> portfolio corrente (convergenza playtest)

Contesto (git 07-02): il baricentro progetto e' il playtest -- analytics pipeline
(session_*.json, VC aggregation, HUD canary dashboard, report ERMES statici), species
pass O8, spec-f cooldown, runbook playtest. La campagna doc-comment e' fuori dal
critical path (polish DX).

| lane candidata | schema | verdetto | note |
|---|---|---|---|
| L1. GGv2 doc-comment tail (~12 clean: surface_role_registry, phone_creature_named_reveal, main_lethal_consent, sense_reveal, telemetry_collector, sistema_intents, phone_coop_vote_wire...) | S1-S5 | **GO opportunistico** | 3-4 giri trio in coda a sessioni future; STOP al tail (>150L / 0-pub / high-NA) |
| L2. Re-scan GGv2 ricorrente (il repo cresce col playtest: +28 file in giugno) | S6 | **GO standing** | ogni sessione campagna: scan prima di batchare; i file nuovi shippano spesso gia' con ## |
| L3. **Characterization-tests sui tool playtest Game** (analyze_telemetry, dashboard pipeline, overcharge/VC helpers) | S7b | **GO CONDIZIONATO** | condizione: file FERMO (oggi churn attivo 15:57-16:18 -- additions su file caldi = conflitti). Criterio: nessun commit sul target da >=3-5 giorni. Freeze-paths esclusi (services/generation, services/rules, apps/backend/services/combat: SOLO behavior-pin test-only come #3049, mai edit). Spec umana esatta obbligatoria (il task 06-25 e' il template) |
| L4. JSDoc su Game tools/ stabilizzati | S1 (variante JS 06-03) | GO dopo-stabilizzazione | valore medio; stesso criterio-fermo di L3 |
| L5. Game docs reorg EXECUTE (1489 doc; proposal Jules gia' pronta in proposals/game-reorg-proposal.md) | metodo provato (git mv + sed #-delim + fence-aware resolver, memory project_docs_reorg_state) | GO ma **non-Jules** | Jules ha gia' fatto il READ; l'execute e' lavoro locale Claude con metodo provato. Chiude l'ultimo repo della reorg multi-repo + 14+3 link deferred |
| L6. Test-coverage REPORT / dead-code / security / findings | -- | **NO-GO confermato** | doctrine giugno: judgment lane, ~85-100% falsi positivi |
| L7. i18n / stringhe player-facing | -- | **NO-GO** | master-dd-authored (ER3); mai delegare wording diegetico |

## 4. Raccomandazioni operative

1. **Cadenza campagna GGv2**: opportunistica -- 1 giro trio (10-15 min) in coda a sessioni
   con altro focus, o quando la quota Jules e' ferma. Niente sessioni dedicate.
2. **Prossima estensione di valore**: L3 (characterization-tests sui tool playtest) appena
   il churn si ferma -- e' il riuso diretto del pattern #3049 sul fronte caldo, e produce
   safety-net per la pipeline analytics che il playtest usera'. Prerequisito: coordinarsi
   con l'arco Game attivo (evitare test su file che l'arco sta ancora ridisegnando).
3. **L5 (reorg execute)** = task Claude autonomo da 1 sessione, non Jules: gia' tutto pronto.
4. **Governance**: wrapper = canale Ryzen (gate-4 dedup anti-collisione cross-via); PR-to-owner
   per one-off Game; auto-merge SOLO campagna GGv2 doc-comments (autorizzazione esistente,
   non estendibile ad altre lane senza ok esplicito). Digest+JOURNAL = vista completa.
5. **Metriche da tenere**: clean-tally per lane (doc-comments 29/29; char-test 1/1);
   respinti-dal-gate (2 storici, 0 recenti); quota/die (oggi 4/100).

## 5. Rischi residui

- **Churn-collision** (nuovo, dal playtest push): additions-only su file caldi puo' confliggere
  al rebase. Mitigazione: criterio-fermo (>=3-5 giorni) + Currency-Gate (fetch pre-branch).
- **Multi-via dispatch senza vista unica**: wrapper-log non vede jules.google manuale.
  Mitigazione: digest daily + gate-4 dedup + JOURNAL come registro delle oversight.
- **Perimetro auto-merge**: il confine e' documentato (solo doc-comment GGv2); ogni nuova
  lane parte PR-to-owner finche' Eduardo non autorizza diversamente.
