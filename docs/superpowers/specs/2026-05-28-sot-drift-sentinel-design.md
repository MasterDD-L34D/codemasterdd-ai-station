# SoT Drift Sentinel -- design

> **Status (2026-06-23):** shipped -- sot-drift-verifier agent live; Game sot-drift-candidate flow

- **Status**: Approved (design) 2026-05-28 -- **IMPLEMENTED + LIVE same day**. Plan `docs/superpowers/plans/2026-05-28-sot-drift-sentinel.md` Tasks 1-8 executed end-to-end. Component A merged Game PR #2406 (`29ac9102`), Component B `codemasterdd/.claude/agents/sot-drift-verifier.md` QG-PASS via live dispatch smoke + verified on a real case (epigenome NO-DRIFT verdict, vault `40992953` already reconciled).
- **Owner**: Eduardo
- **Brainstorm**: questa sessione (superpowers:brainstorming)
- **Problema**: anti-pattern #19 (tracker/SoT lag shipped work) a livello cross-repo

## 1. Contesto & problema

Il runtime Game (public) ship feature che toccano concetti SoT, ma i doc SoT canonici
(vault private `Spaces/Dev/Evo-Tactics/core/` + freeze) restano indietro (lag). Caso
2026-05-28: epigenome shippato Game #2401/#2402/#2404, ma SoT §24.6 + freeze §21.3
dicevano ancora "DEFERRED" -- scoperto e riconciliato a mano (vault PR #203). Pattern
ricorrente: ogni ship Game che tocca un concetto SoT richiede reconcile manuale, oggi
non rilevato fino ad audit fortuito.

L'esistente `evo-tactics-design-watcher` (vault production agent) e' **intra-vault**
(watch diff `Spaces/Dev/Evo-Tactics/`, doc-vs-doc) -- NON copre runtime(Game)-vs-SoT(vault).
Asse diverso. (Inoltre quel watcher ha QG Step-1 "not run".) -> componente NUOVO dedicato.

**Goal**: rilevare automaticamente quando un ship Game tocca un'area mappata a un doc SoT,
e flaggare il SoT-ref da rivedere -- detection deterministica, verdetto semantico gated.

## 2. Vincoli

- Game = **public**; vault = **private/sovereign**. Un Action Game public NON puo' leggere
  il vault private ne' fare verdetto semantico senza un PAT-vault come secret (rischio
  CWE-214 leak in CI public). -> Action = solo detection/flag; verdetto = sovereign gated.
- LLM-as-judge: ~85% accordo umano ma >50% error su bias-test in prod (TrustJudge 2026).
  -> mai verdetto autonomo / mai auto-merge SoT. Multi-signal + human-gate.
- Sovereign-first: nessun secret cross-repo in CI public.

## 3. Architettura (2 componenti + 1 config)

```
[Game push->main]                          [Eduardo review, on-demand]
      |                                            |
      v                                            v
 (A) Detection Action  --apre/aggiorna-->  Game issue            --invoca--> (B) Verdict subagent
     .github/workflows/    label:             "sot-drift-candidate"           sot-drift-verifier
     sot-drift-sentinel.yml #NNNN tocco genetics/ ->                          (codemasterdd .claude/agents/)
        |                   rivedi SoT 24.6                                          |
        +--legge--> watch-map.yml (C)                                  legge vault SoT (sovereign) +
                    path-glob -> SoT-ref                               Game change -> verdetto gated ->
                                                                       se stale: vault branch+PR (merge Eduardo)
                                                                       -> chiude issue
```

- **(A) detection = deterministica** (path-glob, zero LLM, zero secret cross-repo).
- **(B) verdetto = semantico gated** (LLM, mai auto-PR-merge su SoT).
- Separazione netta responsabilita = isolata + testabile indipendente.

## 4. (A) Detection Action -- Game-side

- File: `.github/workflows/sot-drift-sentinel.yml` (PR a Game, merge governance Game).
- Trigger: `on: push: branches: [main]` (post-merge).
- Step: diffa il push vs i pattern in `watch-map.yml`; ogni match = drift-candidate.
- Output: apre **o aggiorna** (idempotente, no-spam: 1 issue aperta riusata) 1 issue Game
  label `sot-drift-candidate`, body = commit/PR + path watched cambiati + SoT-ref mappati.
- Zero accesso vault (by design). Solo flag deterministico.
- Implementazione: shell + `gh issue` (gia' disponibile in Action) o `actions/github-script`.

## 5. (B) Verdict -- subagent sovereign `sot-drift-verifier`

- **Forma = subagent** (codemasterdd `.claude/agents/sot-drift-verifier.md`), NON skill-auto.
  Razionale: task di review esplicito on-demand, read-heavy (SoT vault + Game diff), pattern
  come `harsh-reviewer`/`jules-pr-triager`. Skill-auto scartata (rumore + LLM-judge bias ->
  no auto-trigger; vedi research §7).
- Input: issue `sot-drift-candidate` aperta (o invocazione manuale con SoT-ref).
- Processo: fetch SoT section reale (vault local sovereign) + Game change (gh) -> verdetto
  **multi-signal** (path-match + commit-msg + diff-vs-claim-SoT) con confidence ->
  - se stale: propone vault branch+PR reconcile (merge Eduardo) + summary nel issue.
  - se non-stale: commenta issue "no-drift" + chiude.
- Mai auto-merge SoT. Verdetto = advisory + PR gated.

## 6. (C) watch-map.yml (cuore, versionato in Game)

```yaml
# Game .github/sot-drift/watch-map.yml
- pattern: "apps/backend/services/genetics/**"
  sot_ref: ["core/00-SOURCE-OF-TRUTH.md#24", "core/90-FINAL-DESIGN-FREEZE.md#21.3"]
  concept: "modello genetico D-HEIR/D-REPRO"
- pattern: "apps/backend/services/combat/**"
  sot_ref: ["core/10-SISTEMA_TATTICO.md", "core/11-REGOLE_D20_TV.md"]
  concept: "combat d20 / round loop"
- pattern: "data/core/economy*"
  sot_ref: ["core/26-ECONOMY_CANONICAL.md"]
  concept: "economia PT/PP/SG"
- pattern: "data/core/biomes*"
  sot_ref: ["core/28-NPC_BIOMI_SPAWN.md", "core/15-LEVEL_DESIGN.md"]
  concept: "biomi/spawn"
# estendibile -- pattern-set iniziale da ratificare con Eduardo
```

## 7. Affidabilita (research-grounded)

- **Anti-false-positive**: Action flagga "candidate" (non "drift confermato"); verdetto B
  richiede confidence + human-gate. Detection deterministica (mapping) = layer affidabile
  (pattern doc-drift CI 2026); semantica solo su escalation.
- **Multi-judge opzionale** (TrustJudge / Judge Reliability Harness mar-2026) se serve rigore
  extra sul verdetto B; default single-judge advisory + human-gate sufficiente.
- Fonti: vedi §10.

## 8. Quality Gate (smoke OBBLIGATORIO -- non ripetere "not run" del watcher esistente)

- **Step 1 smoke**: commit fixture che tocca `apps/backend/services/genetics/` su un branch
  test -> Action apre issue `sot-drift-candidate` con SoT-ref `core/00-SOURCE-OF-TRUTH.md#24`
  corretto. Verifica: issue creata + mappa giusta + idempotenza (2o push aggiorna non duplica).
- **Step 2 research**: edge -- push che tocca 0 pattern (no issue), push multi-pattern (1 issue
  multi-ref), issue gia' aperta (update non spam).
- **Step 3 tuning**: subagent verdetto su SoT-fixture stale vs current -> precision verdetto.

## 9. Decisioni (questa sessione)

- Forma trigger: **event-driven (Game PR-merge Action)** [vs cron / skill-auto].
- Scope: **nuovo componente dedicato** [vs estendi intra-vault watcher].
- Flag+verdetto: **Game issue + verdetto subagent sovereign** [vs vault-issue-cross-repo / sovereign-pull-cron]. No secret cross-repo.
- Verdict form: **subagent** [vs skill-auto].

## 10. Open items (pre-implementazione)

- Pattern-set iniziale watch-map: ratificare con Eduardo (genetics/combat/economy/biomi + altri?).
- Dove vive il subagent `sot-drift-verifier`: codemasterdd `.claude/agents/` (proposto) vs vault.
- SoT-ref anchor format (`#24` heading vs line) -- robustezza vs rename heading.

## Riferimenti (research online 2026)

- Doc Drift Detection in CI (mapping + commit-hook): https://understandingdata.com/posts/doc-drift-detection-ci/
- API Documentation Drift prevention: https://zivodoc.com/blog/api-documentation-drift-prevention/
- API Schema Drift Detection Tools 2026: https://dev.to/flarecanary/api-schema-drift-detection-tools-compared-2026-1ib4
- TrustJudge (LLM-as-judge inconsistencies): https://arxiv.org/pdf/2509.21117
- Global Consistency Checking with Noisy LLM Oracles: https://arxiv.org/pdf/2601.13600
- No-Knowledge Alarms for Misaligned LLMs-as-Judges: https://arxiv.org/pdf/2509.08593
