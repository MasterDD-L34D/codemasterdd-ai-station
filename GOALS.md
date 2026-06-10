# GOALS -- Cross-Repo Direction (S/M/L)

> Read-only hub synthesis. Canonical goals live per-repo (each repo's `## Goals (S/M/L)`).
> Refreshed by repo-health-auditor agent. Horizons: Short=sprint(weeks) / Mid=epic(1-2mo) / Long=vision(3-6mo).
> Last refresh: 2026-06-10 (ground-truth audit repo-health-auditor: **tutti i 6 Short del 2026-05-22 COMPLETATI** -- PR canonici #2384/#352/#165/#176/#122 tutti MERGED ~2026-05-25, outcome superati dall'evidenza successiva. **Next Short NON settato: decisione umana pendente**, vedi sezione PROPOSTE). Sources precedenti: docs/superpowers/specs/2026-05-21-cross-repo-goals-coordination-design.md + docs/superpowers/specs/2026-05-22-four-repo-short-directions-design.md

## Snapshot

| Repo | Short | Mid | Long | Cross-dep |
|------|-------|-----|------|-----------|
| Game | **DONE + superato** (M1-full loop validation, #2384 merged 05-25): OD-058 wound cutover SHIPPED flip-ON (#2713 -> #2714 -> #2720 + vcSnapshot coop #2722), SPEC-I fork ratificato + flip active (#2705), ER6 StressWave flag-OFF (#2712). **Next Short: UNSET (decisione Eduardo)** | trait completeness (post-A4); M1 loop hardening from playtest | Co-op tactical shippable, TV+phones Jackbox, ~60min, "how you play shapes what you become" | M1 (loop) |
| Game-Godot-v2 | **DONE + superato** (M1-full client validation + Bond 3.5d, #352 merged 05-25): **AI playtest item-3 co-op PASS** (#465, 2026-06-10); sprint corrente co-op + Form Pulse + phone chronicle M-7. **Next Short: UNSET** | M2 generational succession prod; Bond depth | Canonical frontend (Vue3 archive); full systems shippable | M1 (loop) |
| Game-Database | **DONE** (Phase C versioning loop, #165 merged 05-25). Post-Short: wave Jules code-health 12 PR (CWE-290 #170, rate-limit #169, test/JSDoc). **Next Short: UNSET** | versioned reads Biome/Species/Eco; bidi-sync RFC #4 scoping; audit-UI hardening | Robust versioned auditable content backend (evo:import) | feeds Game |
| vault | **DONE** (synthesis fidelity-verify, #176 merged 05-25). Post-Short: 40+ PR (eng-graph SSE daemon #243, OD-059 cloud judge #241, gap-capture daily backstop). **Next Short: UNSET** | KB coverage; 7/7 agents stable (already met) | Complete personal/project knowledge layer, agent-queryable | -- |
| evo-swarm (Dafne) | **DONE** (integration loop close, #122 merged 05-25; digest #123 merged 05-28). **Repo IDLE dal 05-28** (0 attivita' in 13gg). **Next Short: UNSET** | Integrable game content low-manual-validation | Trusted AI content-orchestration meta-layer at scale | feeds Game |
| codemasterdd | **DONE** (Gate-E evidence-logging -> gate review ~06-03 ESEGUITO): ADR-0036 Accepted (spine) 06-01 + ADR-0037 Accepted 06-03; ADR-0038/0039 Proposed (pending ratify). **Next Short: UNSET** | Sovereign stack maturity (ADR-0030 Hybrid A1); coordination tooling (gated) | Self-sufficient sovereign AI dev station + ecosystem governance | hub |

## Cross-cutting initiatives

- **M1 "Sistema"** (persistent cross-session AI learning). **Build CLOSED + validation COMPLETE** -- build: Game route #2364 + pilot #2363 + passthrough #2376 + orphan-removal #2377; Godot client #342. Validation (Short 05-22): loop live validato e superato -- AI playtest item-3 co-op PASS (Godot #465, 2026-06-10); lato Game il loop ha retto lo stream OD-058 wound cutover fino al flip-ON (#2720/#2722).
- **Content supply-chain into Game** (tema 2026-05-22, esito 06-10): Game-Database loop versioning CHIUSO (#165) + wave code-health Jules successiva; vault knowledge layer rafforzato (40+ PR, eng-graph daemon + verdicts OD-058); **evo-swarm ha chiuso il loop (#122) ma il repo e' IDLE dal 05-28** -- la continuita' del canale content e' una decisione Eduardo (resume vs PARK), vedi PROPOSTE.

## Short outcomes (2026-05-22 -> 2026-06-10)

Tutti i 6 Short settati il 2026-05-22 risultano COMPLETATI a ground-truth audit 2026-06-10:
- **Game**: #2384 merged 05-25; valore superato dallo sprint successivo (OD-058 flip-ON, SPEC-I active, ~297 PR nel periodo).
- **Godot-v2**: #352 merged 05-25; AI playtest item-3 co-op PASS #465 chiude la validazione client (105 PR nel periodo).
- **Game-DB**: #165 merged 05-25; seguita wave Jules code-health (12 PR, CWE-290 fix #170).
- **vault**: #176 merged 05-25; 40+ PR successive (eng-graph daemon, OD-059, backstop daily).
- **evo-swarm**: #122 merged 05-25 + digest #123 merged 05-28; poi repo idle.
- **codemasterdd**: Gate-E logging ha alimentato il gate review: ADR-0036 Accepted (spine) 06-01, ADR-0037 Accepted 06-03, ADR-0038/0039 Proposed; 40 PR nel periodo (jules-dispatch fail-closed, R1 rung, docs reorg).

Storico ciclo precedente (2026-05-21 first real cycle) in git history + spec docs. **Setting the next Short remains a human decision** -- nessun nuovo Short e' stato settato in questo refresh.

## PROPOSTE next Short (decisione Eduardo -- NON settate)

> Candidati derivati dall'evidenza audit 2026-06-10. Nessuna riga qui sotto e' attiva finche' Eduardo non ratifica (1 scelta per repo, o skip).

- **Game**: (a) SPEC-I completion -- land ER7 biome population tick (#2723 open, non-draft) + flip; (b) governance stale burn-down campagna (~246 stale doc, piano in Game BACKLOG #2614).
- **Game-Godot-v2**: (a) AI playtest ladder -- item successivi post item-3 PASS (#465, host driver riusabile gia' pronto); (b) phone chronicle M-7 da MVP (#452) a production depth.
- **Game-Database**: (a) versioned reads Biome/Species/Eco (pull-down dal Mid, naturale post-#165); (b) Jules code-health wave 2 (security/test coverage post CWE-290 #170).
- **vault**: (a) eng-graph daemon integration nei workflow quotidiani (post #243 SSE/HTTP + OD-059 cloud judge #241); (b) lint-WARN burn-down (coherence WARN 1 + gap 3/5 nonzero, signals 06-03).
- **evo-swarm**: (a) resume ciclo -- born-ready live-validate -> Game PR (continuazione naturale di #122); (b) PARK esplicito (idle 13gg + Flask down: dichiararlo parked invece di lasciarlo implicito).
- **codemasterdd**: (a) ADR-0038/0039 ratify path (SDMG harsh-review + decisione Eduardo); (b) post-Max readiness -- Claude Max scade ~06-17: attivazione routing ADR-0023 (tier-0 on-demand + spend tracking).
- **Synesthesia**: nessuna proposta (dormant intenzionale fino ~ago-2026; no task inventati).

## Notes

- D2 auto-coordination: gate review ~06-03 ESEGUITO -- ADR-0036 Accepted (spine) + auto-merge rung Deferred; ADR-0037 merge-autonomy Accepted 06-03. Questo file resta READ-ONLY direction, no auto-trigger.
- SDMG empirical window (start 2026-05-20): esito ratificato in ADR-0036/0037; quarterly review ~2026-08-01 (checkpoint in STATUS_MULTI_REPO.md).
