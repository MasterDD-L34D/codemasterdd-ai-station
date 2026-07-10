# GOALS -- Cross-Repo Direction (S/M/L)

> Read-only hub synthesis. Canonical goals live per-repo (each repo's `## Goals (S/M/L)`).
> Refreshed by repo-health-auditor agent. Horizons: Short=sprint(weeks) / Mid=epic(1-2mo) / Long=vision(3-6mo).
> Last refresh: **2026-07-10** (audit delta vs 07-03, post fleet-verify 07-09 + flag-set ratify). Prec. **2026-07-03** (game-family fleet-verify). Prec. **2026-06-30** (audit delta vs 06-23, currency note in fondo). Prec. **2026-06-23** (audit delta vs 06-19). Prec. **2026-06-19** (delta sotto la Snapshot supersedes il baseline 06-11 dove diverge). Precedente 2026-06-10 (ground-truth audit repo-health-auditor: **tutti i 6 Short del 2026-05-22 COMPLETATI** -- PR canonici #2384/#352/#165/#176/#122 tutti MERGED ~2026-05-25, outcome superati dall'evidenza successiva). **Next Short RATIFICATI da Eduardo 2026-06-11** (AskUserQuestion strutturato, sessione coordinatore -- vedi "Short ratificati 2026-06-11"). Sources precedenti: docs/superpowers/specs/2026-05-21-cross-repo-goals-coordination-design.md + docs/superpowers/specs/2026-05-22-four-repo-short-directions-design.md

## Snapshot

| Repo | Short | Mid | Long | Cross-dep |
|------|-------|-----|------|-----------|
| Game | **DONE + superato** (M1-full loop validation, #2384 merged 05-25): OD-058 wound cutover SHIPPED flip-ON (#2713 -> #2714 -> #2720 + vcSnapshot coop #2722), SPEC-I fork ratificato + flip active (#2705), ER6 StressWave flag-OFF (#2712). **Next Short (ratificato 06-11): SPEC-I completion** -- ER7 flip + chiusura fork (ER1/ER6 flip-ON #2725, ER7 built flag-gated #2723); esecutore = lane Ryzen | trait completeness (post-A4); M1 loop hardening from playtest | Co-op tactical shippable, TV+phones Jackbox, ~60min, "how you play shapes what you become" | M1 (loop) |
| Game-Godot-v2 | **DONE + superato** (M1-full client validation + Bond 3.5d, #352 merged 05-25): **AI playtest item-3 co-op PASS** (#465, 2026-06-10); sprint corrente co-op + Form Pulse + phone chronicle M-7. **Next Short (ratificato 06-11): AI playtest ladder** -- item-4+ con host driver riusabile | M2 generational succession prod; Bond depth | Canonical frontend (Vue3 archive); full systems shippable | M1 (loop) |
| Game-Database | **RFC #4 traits DONE end-to-end** (06-14): loop DB->Game live (glossary Game#2750 + canon #2752 + reference #2755 + mirror #2758; GATE G1->G6 verde, 10 cicli, fidelity-gated). **Species export ACTIVE (06-17)**: scope ratificato (RFC #209: S-Q1 sourceExtras parity / S-Q2 description non-exported / S-Q3 per-file, index+canonical-index downstream) -> **Sp1a SHIPPED #214** (provenance + snapshot determinism) -> **Sp1b SHIPPED #216** + **Sp1c SHIPPED #219** (5 fidelity gaps closed). **Fidelity GREEN** (run 27706615133: catalog-tier 17 species, 0 divergent / 0 unexpected / 0 targetMissing; only model-gap description+last_synced_at). Species DB->Game loop fidelity-complete. **S2 next** (export-on-release) gated on Q8 canon-authority (Game authority-map entry) + OQ5 cross-repo actor + OQ7 sync-narrow | (PARKED) biome/eco export: YAML (js-yaml + order-preserve + eco model-gap extend-vs-sourceExtras), scope-doc+ratifica prima del dispatch; audit-UI hardening | Robust versioned auditable content backend (evo:import) | feeds Game |
| vault | **DONE** (synthesis fidelity-verify, #176 merged 05-25). Post-Short: 40+ PR (eng-graph SSE daemon #243, OD-059 cloud judge #241, gap-capture daily backstop). **Next Short (ratificato 06-11): eng-graph daemon integration** nei workflow quotidiani | KB coverage; 7/7 agents stable (already met) | Complete personal/project knowledge layer, agent-queryable | -- |
| evo-swarm (Dafne) | **DONE** (integration loop close, #122 merged 05-25; digest #123 merged 05-28). ~~PARKED esplicito (06-11)~~ -> **ARCHIVED+PRIVATE 2026-06-22** (Dec-013 accelerator FALSIFIED + Dec-014 retire riconfermato; nessuna reactivation pendente) | ~~Integrable game content low-manual-validation~~ (chiuso con l'archive) | ~~Trusted AI content-orchestration meta-layer at scale~~ (chiuso) | feeds Game (storico) |
| codemasterdd | **DONE** (Gate-E evidence-logging -> gate review ~06-03 ESEGUITO): ADR-0036 Accepted (spine) 06-01 + ADR-0037 Accepted 06-03; ADR-0038/0039 Proposed (pending ratify). **Next Short (ratificato 06-11): post-Max readiness** (attivazione ADR-0023, Max scade ~06-17) + ADR-0038/0039 ratify in-sprint | Sovereign stack maturity (ADR-0030 Hybrid A1); coordination tooling (gated) | Self-sufficient sovereign AI dev station + ecosystem governance | hub |

## 2026-06-19 refresh delta (vs 06-11 baseline)

Ground-truth audit 2026-06-19 (repo-health-auditor). Supersedes la Snapshot 06-11 dove diverge:

- **Game**: taxonomy reconciliation (Phase A/B/D) + 5-stub honest-stub deploy + S0-S3 calibration + steep-lever band-widen + jsonschema-shadow ALL MERGED. **RFC#4 CHIUSO end-to-end** (S1 traits / S2 species fidelity-shadow + biome/eco import-only / S3 NO-GO ratified `ADR-2026-06-19` #2877). **PE_ratio arc CLOSED 2026-06-24** (#3022: contestedness FALSIFIED N=40 multi-policy -> PE term droppato, composite=0.70*WR+0.30*KD; negative-result SDMG-ratified, sblocca SPEC-J/SPEC-H). Open: 0 PR (verificato 06-30).
- **Game-Database**: RFC#4 S2 chiuso (#226/#227) + S3 stamp (#230, pointer Game ADR). 0 open.
- **evo-swarm**: **verification arc CLOSED 2026-06-20** -- 3-lever gate done (L1 #124/ratified #127, L2 REJECTED SDMG, L3 SHIPPED #129). **Decisione 013 #130: swarm-as-production-accelerator FALSIFIED** (12 artifact -> 11 rejected 91.7% halluc; generator archiviato, verify-swarm-claims promosso linter). Pivot OBSERVABILITY: dashboard fase 2-8 (#97-#102). Runtime PARKED. **Remote ARCHIVED+PRIVATE 06-22** (push 403) -> swarm->Game digest pipeline CHIUSA; 13 report post-mortem in docs/archive/evo-swarm-digest-archive/. Nessuna decisione pendente.
- **Game-Godot-v2**: Ferrospora UI art-pass v2 + style-LoRA v1 DONE; SPEC-K K-05 phone/TV client #507. #509 (ForecastPanel frame) + #510 (K-05 QA) **MERGED 2026-06-19** -- 0 PR open da questo batch.
- **vault**: ADR-2026-06-03 asset-pipeline ratificato 06-18; 7 WARN carry-forward.
- **codemasterdd**: **Claude Max scaduto ~06-17 -> post-Max routing ADR-0023 ATTIVO** (`logs/claude-api-spend-2026-06.md`, spend ~$0). ADR-0038/0039 Accepted 06-11.

**Pending trigger-gated / deferred** (nessuna azione ora): RFC#4 GO_NARROW (3 trigger); swarm Lever-2/Lever-3 spec; gap-audit P5 live-emission + SDMG corpus run; ferrospora creature-LoRA + ControlNet silhouette-lock / roster coherence (Ryzen .11 -- opt-2 ComfyUI/`/prompt` seam-spike DONE 2026-06-21); GD1 Godot TV LobbyView; prod-auto-restart residue (Game chip task_3ce69e8d). **Scheduled**: SDMG quarterly review ~2026-08-01; governor reconcile settimanale (R2 earn-window).

I 'Next Short (ratificato 06-11)' nella tabella sopra restano il baseline d'intento; il setting dei prossimi Short = decisione Eduardo.

## 2026-06-23 audit delta (vs 06-19)

Ground-truth gh/git 7 repo (repo-health-auditor manuale, post tool-fix):

- **Game**: open-PR set ruotato -- #2765 (weekly-drift) chiuso; ora 4 PR content/chore (#2981 bestiary canonize, #2980 aa01 imprint disposition, #2957 lore-name polish, #2918 tracker). Working tree su detached HEAD (#2973 merged) ma con WIP attivo master-dd + 8 worktree concorrenti -> sessione ATTIVA, non un cleanup target.
- **Godot-v2**: branch `feat/creature-lora-fase2` attivo (creature-LoRA); 1 PR open #512 (Ferrospora UI canonical).
- **codemasterdd / Game-DB / evo-swarm / vault / Synesthesia**: 0 PR open.
- I 6 Next-Short ratificati 06-11 = **TUTTI DONE** (verifica gh 06-23): Game SPEC-I ER7 flip-ON #2737 / Godot ladder item-4/5/6 #468/#471 / vault eng-graph daily-daemon #257 / Game-DB species export / codemasterdd post-Max ADR-0023 / evo-swarm PARK. Nuovi Short -> sezione sotto.

## Short ratificati 2026-06-23 (decisione Eduardo)

> Tutti i 6 Short ratificati 06-11 = DONE (ground-truth gh 2026-06-23). Nuovi Short via AskUserQuestion recommended-first, 1 per repo. Stato progetto = inflection "Short consegnati -> next set".

- **Game**: trait completeness (post-A4) -- Mid-item promosso a Short.
- **Game-Godot-v2**: Ferrospora UI per-surface rebuild, **dock-first** (ActionDock fixa il socket-centering by-construction; roadmap PR #512; color-reconcile via issue #544 + chip task_a15add23).
- **vault**: 7 WARN cleanup carry-forward + 2 cross-repo currency drift (canonical-config Claude-Max-stale post-scadenza 06-17 + model-names sonnet-4.7 -> claude-sonnet-4-6).
- **Game-Database**: nessun Short proattivo (Jules-maintained; RFC#4 chiuso end-to-end).
- **codemasterdd**: nessun Short proattivo (hub reattivo; steering-tools rinfrescati 06-23; SDMG quarterly review ~2026-08-01 schedulato).
- **evo-swarm**: PARK esplicito (reactivation Eduardo-gated, invariato).
- **Synesthesia**: dormant fino ~ago 2026 (invariato).

## 2026-06-30 audit delta (vs 06-23) -- currency note

> Ground-truth gh/git (repo-health-auditor + spot-verify). I 'Short ratificati 06-23' sopra restano direttive Eduardo; questa e' solo nota di currency (cosa risulta consegnato), il re-set dei prossimi Short = decisione Eduardo.

- **Godot-v2 Short "Ferrospora dock-first"**: risulta consegnato/superato -- remote main e' a #557 (terrain-cost telegraph Gate-5) + portrait-loader loop CLOSED #556; 0 PR open. -> candidato a next-Short da ri-settare.
- **vault Short "7 WARN cleanup + 2 currency drift"**: WARN reale = **9** (non 7), confermato coherence PASS-4 06-30 (carry-forward, 0 BLOCK; #262/#263 toccavano lint-status NUL, non i 9 coherence-WARN). I 9 = W-1..W-9 user-gated (incl. W-2 Claude-Max expiry, W-4 canonical-config OD-059-stale = i 2 currency drift citati). Clone Lenovo synced 06-30.
- **Game / Godot / codemasterdd**: 0 PR open. **evo-swarm**: ARCHIVED, Decisione 014 retire-reconfirmed (post-013).

## 2026-07-03 audit delta (vs 06-30) -- currency note (game-family fleet-verify)

> Ground-truth gh/git, scope game-family (Workflow 5-probe + 3-vote adversariale). Solo currency (cosa risulta consegnato/rotto-e-riparato); il re-set dei prossimi Short = decisione Eduardo.

- **Game-Database**: evo-import-sync **riparato** -- PR #233 MERGED 07-03 dopo 8+/8 scheduled-run failing (bot-403 + `_game` gitlink); verificato GREEN via manual dispatch (run 28656614132). Prisma no-drift. Questo filone non era tracciato nei layer precedenti (gap chiuso).
- **Game**: MAP-Elites v2 arc CLOSED (#3183 merged 07-02); 1 PR open #3195 (do-NOT-merge, Eduardo review). Design-direction AMBER: finestra recente governance-heavy, ma balance-thread (calibrazione) vivo.
- **Godot-v2**: 1 PR open #585 (sessione Ryzen attiva, gdformat lint FAIL -- monitor-only, non pushare). Supera il "#557 / 0 PR open" del 06-30.

## 2026-07-10 audit delta (vs 07-03) -- currency note (post fleet-verify 07-09 + flag-set ratify)

> Ground-truth gh/git 2026-07-10. Solo currency (cosa risulta consegnato); il re-set dei prossimi Short = decisione Eduardo.

- **Game**: maratona 07-06/07 landed -- **LOS default ON prod** (#3226 + GGv2 #588/#589), big-maps arc 3 encounter grid_sized (#3229/#3230/#3237, ADR-2026-07-03 board_scale), **seed-fix #3232** (full-loop finalmente seedabile), D4 A/B negative (#3231 flag OFF), App-token #3242 MERGED. **0 PR open su tutta la family** (Game/GGv2/Game-DB).
- **Flag-set prod ratificato Eduardo 07-09/10 (LIVE Lenovo, backend riavviato)**: route-choice (META_NETWORK_ROUTING) + terrain-cost + form-pulse v2 (anchor 1.15) + xp-geometry (D9) + imprint (regressione sanata 07-09) + **Nido APERTO** (NIDO_UNLOCKED=true + setx client TV); lethal OFF-until-K07 (decisione owner). Prod = per la prima volta il loop con Nido raggiungibile. Riconcile doc -> draft-PR GGv2 #595 + vault #269 (merge = Eduardo).
- **Correzioni currency**: **Claude Max ATTIVO** (riconfermato Eduardo 07-03) -- le voci "scaduto ~06-17" dei layer 06-19/06-30 = credenza dell'epoca, superata (ADR-0023 = contingency). **evo-swarm ARCHIVED+PRIVATE dal 06-22** (Dec-013/014): la riga Snapshot "PARKED, reactivation Eduardo-gated" e' superata, nessun trigger pendente.
- **Jules**: campagna GGv2 a 149/285 (52%), pool filler 5 -> ~2 trio all'hard-stop; lane L3 tally 11/12 + primo merge delegato #3241.

## Cross-cutting initiatives

- **M1 "Sistema"** (persistent cross-session AI learning). **Build CLOSED + validation COMPLETE** -- build: Game route #2364 + pilot #2363 + passthrough #2376 + orphan-removal #2377; Godot client #342. Validation (Short 05-22): loop live validato e superato -- AI playtest item-3 co-op PASS (Godot #465, 2026-06-10); lato Game il loop ha retto lo stream OD-058 wound cutover fino al flip-ON (#2720/#2722).
- **Content supply-chain into Game** (tema 2026-05-22, esito 06-10): Game-Database loop versioning CHIUSO (#165) + wave code-health Jules successiva; vault knowledge layer rafforzato (40+ PR, eng-graph daemon + verdicts OD-058); **evo-swarm ha chiuso il loop (#122), poi ARCHIVED+PRIVATE 2026-06-22** (Dec-013 FALSIFIED + Dec-014 retire riconfermato) -- canale content CHIUSO, nessuna reactivation pendente.

## Short outcomes (2026-05-22 -> 2026-06-10)

Tutti i 6 Short settati il 2026-05-22 risultano COMPLETATI a ground-truth audit 2026-06-10:
- **Game**: #2384 merged 05-25; valore superato dallo sprint successivo (OD-058 flip-ON, SPEC-I active, ~297 PR nel periodo).
- **Godot-v2**: #352 merged 05-25; AI playtest item-3 co-op PASS #465 chiude la validazione client (105 PR nel periodo).
- **Game-DB**: #165 merged 05-25; seguita wave Jules code-health (12 PR, CWE-290 fix #170).
- **vault**: #176 merged 05-25; 40+ PR successive (eng-graph daemon, OD-059, backstop daily).
- **evo-swarm**: #122 merged 05-25 + digest #123 merged 05-28; poi repo idle.
- **codemasterdd**: Gate-E logging ha alimentato il gate review: ADR-0036 Accepted (spine) 06-01, ADR-0037 Accepted 06-03, ADR-0038/0039 Proposed; 40 PR nel periodo (jules-dispatch fail-closed, R1 rung, docs reorg).

Storico ciclo precedente (2026-05-21 first real cycle) in git history + spec docs. **Setting the next Short remains a human decision** -- i next Short sono stati ratificati da Eduardo il 2026-06-11 (sezione sotto).

## Short ratificati 2026-06-11 (decisione Eduardo)

> Ratifica via AskUserQuestion strutturato recommended-first (sessione coordinatore 2026-06-11), 1 scelta per repo dalle PROPOSTE dell'audit 06-10. Le alternative non scelte restano nel log di PR #318.

- **Game**: SPEC-I completion -- ER7 flip + chiusura fork. Esecutore = lane Ryzen (gia' in corsa: ER1/ER6 flip-ON #2725, ER7 built #2723).
- **Game-Godot-v2**: AI playtest ladder -- item-4+ post item-3 PASS, host driver riusabile (#465). Lane Lenovo (precedente item-3).
- **Game-Database**: ~~versioned reads~~ **DONE** (#180) -> ~~RFC #4 scoping + S1 trait shadow-exporter~~ **DONE** (RFC ratified #182/#183; traits loop DB->Game live 06-14). **Active (06-17)**: species export -- scope ratificato #209, **Sp1a SHIPPED #214** (provenance + snapshot determinism), **Sp1b SHIPPED #216** + **Sp1c SHIPPED #219**. **Fidelity GREEN** (run 27706615133: 17 catalog-tier, 0 divergent/unexpected/targetMissing). S2 export-on-release next, gated on Q8 + OQ5 + OQ7. biome/eco still parked. Eduardo-sovereign gate.
- **vault**: eng-graph daemon integration nei workflow quotidiani (post #243 + OD-059 #241).
- **evo-swarm**: **PARK esplicito** -- reactivation = decisione Eduardo (candidati trigger: post-Max routing attivo / SPEC-I closed). Stato onesto invece di idle implicito.
- **codemasterdd**: post-Max readiness (attivazione routing ADR-0023: tier-0 on-demand + spend tracking; Max scade ~06-17) + ADR-0038/0039 ratify come task in-sprint ("entrambi in sequenza").
- **Synesthesia**: nessun Short (dormant intenzionale fino ~ago-2026; no task inventati).

## Notes

- D2 auto-coordination: gate review ~06-03 ESEGUITO -- ADR-0036 Accepted (spine) + auto-merge rung Deferred; ADR-0037 merge-autonomy Accepted 06-03. Questo file resta READ-ONLY direction, no auto-trigger.
- SDMG empirical window (start 2026-05-20): esito ratificato in ADR-0036/0037; quarterly review ~2026-08-01 (checkpoint in STATUS_MULTI_REPO.md).
