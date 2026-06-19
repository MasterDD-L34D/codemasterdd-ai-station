# GOALS -- Cross-Repo Direction (S/M/L)

> Read-only hub synthesis. Canonical goals live per-repo (each repo's `## Goals (S/M/L)`).
> Refreshed by repo-health-auditor agent. Horizons: Short=sprint(weeks) / Mid=epic(1-2mo) / Long=vision(3-6mo).
> Last refresh: **2026-06-19** (delta sotto la Snapshot supersedes il baseline 06-11 dove diverge). Precedente 2026-06-10 (ground-truth audit repo-health-auditor: **tutti i 6 Short del 2026-05-22 COMPLETATI** -- PR canonici #2384/#352/#165/#176/#122 tutti MERGED ~2026-05-25, outcome superati dall'evidenza successiva). **Next Short RATIFICATI da Eduardo 2026-06-11** (AskUserQuestion strutturato, sessione coordinatore -- vedi "Short ratificati 2026-06-11"). Sources precedenti: docs/superpowers/specs/2026-05-21-cross-repo-goals-coordination-design.md + docs/superpowers/specs/2026-05-22-four-repo-short-directions-design.md

## Snapshot

| Repo | Short | Mid | Long | Cross-dep |
|------|-------|-----|------|-----------|
| Game | **DONE + superato** (M1-full loop validation, #2384 merged 05-25): OD-058 wound cutover SHIPPED flip-ON (#2713 -> #2714 -> #2720 + vcSnapshot coop #2722), SPEC-I fork ratificato + flip active (#2705), ER6 StressWave flag-OFF (#2712). **Next Short (ratificato 06-11): SPEC-I completion** -- ER7 flip + chiusura fork (ER1/ER6 flip-ON #2725, ER7 built flag-gated #2723); esecutore = lane Ryzen | trait completeness (post-A4); M1 loop hardening from playtest | Co-op tactical shippable, TV+phones Jackbox, ~60min, "how you play shapes what you become" | M1 (loop) |
| Game-Godot-v2 | **DONE + superato** (M1-full client validation + Bond 3.5d, #352 merged 05-25): **AI playtest item-3 co-op PASS** (#465, 2026-06-10); sprint corrente co-op + Form Pulse + phone chronicle M-7. **Next Short (ratificato 06-11): AI playtest ladder** -- item-4+ con host driver riusabile | M2 generational succession prod; Bond depth | Canonical frontend (Vue3 archive); full systems shippable | M1 (loop) |
| Game-Database | **RFC #4 traits DONE end-to-end** (06-14): loop DB->Game live (glossary Game#2750 + canon #2752 + reference #2755 + mirror #2758; GATE G1->G6 verde, 10 cicli, fidelity-gated). **Species export ACTIVE (06-17)**: scope ratificato (RFC #209: S-Q1 sourceExtras parity / S-Q2 description non-exported / S-Q3 per-file, index+canonical-index downstream) -> **Sp1a SHIPPED #214** (provenance + snapshot determinism) -> **Sp1b SHIPPED #216** + **Sp1c SHIPPED #219** (5 fidelity gaps closed). **Fidelity GREEN** (run 27706615133: catalog-tier 17 species, 0 divergent / 0 unexpected / 0 targetMissing; only model-gap description+last_synced_at). Species DB->Game loop fidelity-complete. **S2 next** (export-on-release) gated on Q8 canon-authority (Game authority-map entry) + OQ5 cross-repo actor + OQ7 sync-narrow | (PARKED) biome/eco export: YAML (js-yaml + order-preserve + eco model-gap extend-vs-sourceExtras), scope-doc+ratifica prima del dispatch; audit-UI hardening | Robust versioned auditable content backend (evo:import) | feeds Game |
| vault | **DONE** (synthesis fidelity-verify, #176 merged 05-25). Post-Short: 40+ PR (eng-graph SSE daemon #243, OD-059 cloud judge #241, gap-capture daily backstop). **Next Short (ratificato 06-11): eng-graph daemon integration** nei workflow quotidiani | KB coverage; 7/7 agents stable (already met) | Complete personal/project knowledge layer, agent-queryable | -- |
| evo-swarm (Dafne) | **DONE** (integration loop close, #122 merged 05-25; digest #123 merged 05-28). **Repo IDLE dal 05-28**. **PARKED esplicito (ratificato 06-11)** -- reactivation = decisione Eduardo (candidati trigger: post-Max routing attivo / SPEC-I closed) | Integrable game content low-manual-validation | Trusted AI content-orchestration meta-layer at scale | feeds Game |
| codemasterdd | **DONE** (Gate-E evidence-logging -> gate review ~06-03 ESEGUITO): ADR-0036 Accepted (spine) 06-01 + ADR-0037 Accepted 06-03; ADR-0038/0039 Proposed (pending ratify). **Next Short (ratificato 06-11): post-Max readiness** (attivazione ADR-0023, Max scade ~06-17) + ADR-0038/0039 ratify in-sprint | Sovereign stack maturity (ADR-0030 Hybrid A1); coordination tooling (gated) | Self-sufficient sovereign AI dev station + ecosystem governance | hub |

## 2026-06-19 refresh delta (vs 06-11 baseline)

Ground-truth audit 2026-06-19 (repo-health-auditor). Supersedes la Snapshot 06-11 dove diverge:

- **Game**: taxonomy reconciliation (Phase A/B/D) + 5-stub honest-stub deploy + S0-S3 calibration + steep-lever band-widen + jsonschema-shadow ALL MERGED. **RFC#4 CHIUSO end-to-end** (S1 traits / S2 species fidelity-shadow + biome/eco import-only / S3 NO-GO ratified `ADR-2026-06-19` #2877). **PE_ratio PR2/PR2b DONE** (#2867/#2869; finding: signal marginale -> decisione band residua). Open: solo #2765 DRAFT weekly-drift.
- **Game-Database**: RFC#4 S2 chiuso (#226/#227) + S3 stamp (#230, pointer Game ADR). 0 open.
- **evo-swarm**: **REACTIVATED** (non piu' IDLE) -- entity-grounding pre-emit gate Lever-1 #124 + 2 fix trait-source #125/#126 (06-19, suite 471 green). Runtime ancora PARKED. Lever-2/Lever-3 = spec future.
- **Game-Godot-v2**: Ferrospora UI art-pass v2 + style-LoRA v1 DONE; SPEC-K K-05 phone/TV client #507. 2 PR open (#509 ForecastPanel frame, #510 K-05 QA).
- **vault**: ADR-2026-06-03 asset-pipeline ratificato 06-18; 7 WARN carry-forward.
- **codemasterdd**: **Claude Max scaduto ~06-17 -> post-Max routing ADR-0023 ATTIVO** (`logs/claude-api-spend-2026-06.md`, spend ~$0). ADR-0038/0039 Accepted 06-11.

**Pending trigger-gated / deferred** (nessuna azione ora): RFC#4 GO_NARROW (3 trigger); swarm Lever-2/Lever-3 spec; gap-audit P5 live-emission + SDMG corpus run; ferrospora SD spike (Ryzen .11); GD1 Godot TV LobbyView; prod-auto-restart residue (Game chip task_3ce69e8d). **Scheduled**: SDMG quarterly review ~2026-08-01; governor reconcile settimanale (R2 earn-window).

I 'Next Short (ratificato 06-11)' nella tabella sopra restano il baseline d'intento; il setting dei prossimi Short = decisione Eduardo.

## Cross-cutting initiatives

- **M1 "Sistema"** (persistent cross-session AI learning). **Build CLOSED + validation COMPLETE** -- build: Game route #2364 + pilot #2363 + passthrough #2376 + orphan-removal #2377; Godot client #342. Validation (Short 05-22): loop live validato e superato -- AI playtest item-3 co-op PASS (Godot #465, 2026-06-10); lato Game il loop ha retto lo stream OD-058 wound cutover fino al flip-ON (#2720/#2722).
- **Content supply-chain into Game** (tema 2026-05-22, esito 06-10): Game-Database loop versioning CHIUSO (#165) + wave code-health Jules successiva; vault knowledge layer rafforzato (40+ PR, eng-graph daemon + verdicts OD-058); **evo-swarm ha chiuso il loop (#122), repo PARKED esplicito dal 2026-06-11** (ratifica Eduardo, reactivation trigger-gated) -- il canale content riprende a reactivation.

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
