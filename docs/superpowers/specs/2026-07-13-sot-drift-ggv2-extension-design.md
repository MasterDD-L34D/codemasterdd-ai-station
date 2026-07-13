# SoT Drift Sentinel -- GGv2 (frontend) extension -- design

> **Status:** Approved (forks) 2026-07-13 -- awaiting spec review before writing-plans.
> **Owner:** Eduardo
> **Parent spec:** `docs/superpowers/specs/2026-05-28-sot-drift-sentinel-design.md` (Game-keyed sentinel, shipped)
> **Brainstorm:** questa sessione (superpowers:brainstorming)
> **Problema:** il sentinel esistente e' Game-keyed; un ship di Game-Godot-v2 (frontend canonico) che tocca un concetto SoT vault NON e' rilevato. Caso 2026-07-13: audio (GGv2 #599) + VFX combat (GGv2 #601) shippati e MERGED, ma le ADR vault `audio-direction-placeholder` / `art-direction-placeholder` dicevano ancora deferred/Non-MVP -- scoperto solo per smoke manuale, riconciliato a mano (vault PR #270).

## 1. Contesto & problema

Il SoT Drift Sentinel (2026-05-28, shipped) rileva quando un ship **Game** (backend public)
tocca un'area mappata a un doc SoT vault e apre un issue `sot-drift-candidate` che il
subagent sovereign `sot-drift-verifier` verdice + riconcilia (branch+PR, merge Eduardo).

Tre pezzi, tutti agganciati a **Game**:
- (A) Detection Action -- vive in Game, trigger `push:main` Game, diffa vs `watch-map.yml` Game.
- (B) Verdetto -- subagent `sot-drift-verifier` (codemasterdd, sovereign, on-demand). **Repo-agnostico**: verdice qualsiasi SoT-ref, non solo Game.
- (C) watch-map -- path-glob backend Game -> SoT-ref.

**Il gap**: Game-Godot-v2 (GGv2) e' il **frontend canonico** (cutover 2026-05, consuma il backend Game).
I suoi ship (audio, VFX, screen, surfaces player-facing) NON fanno scattare la Action Game
(diverso repo, diverso trigger, diversi path). Risultato: drift frontend-vs-SoT non rilevato.

**Goal**: rilevare automaticamente quando un ship GGv2 tocca un'area mappata a un doc SoT vault,
e flaggare il SoT-ref da rivedere -- **senza toccare GGv2** (Ryzen-active, self-governed).

## 2. Vincoli

- **Zero GGv2 write** (boundary standing: Ryzen-active + self-governed). Il detector polla GGv2
  in **sola-lettura** (`gh api`, repo public). Nessuna Action/CI/issue dentro GGv2.
- **Sovereign-first**: nessun secret cross-repo in CI public. Il detector gira sul fleet
  (codemasterdd, Lenovo canonical), non in CI GGv2.
- **No LLM in detection**: detection deterministica (path-glob). Il verdetto semantico resta
  nel subagent B, human-gated (LLM-as-judge >50% error su bias-test -> mai auto-merge SoT).
- **Anti-collisione** (finding load-bearing, vedi sez. 6): l'Action Game riusa "il primo issue
  aperto per label" (`gh issue list --label sot-drift-candidate --jq '.[0].number'`, solo per
  label). Un secondo producer sullo STESSO label si contende/sovrascrive lo stesso issue.

## 3. Architettura (detector sovereign; riusa B + governor)

```
GGv2 push->main (Ryzen)                        [Eduardo, on-demand]
       |                                              |
       v  [daily fleet task, Lenovo]                  v
 (A') detector sovereign  --apre/aggiorna-->  Game issue                --invoca--> (B) sot-drift-verifier
   scripts/fleet/               label:         "sot-drift-candidate-ggv2"           [INVARIATO]
   sot-drift-ggv2-detect.py     #NNN GGv2 audio ->                                  legge vault SoT + GGv2
      |  polla PR merged GGv2     rivedi ADR audio                                  change -> verdetto gated ->
      |  (gh api, READ-ONLY)                                                        se stale: vault branch+PR
      +--legge--> ggv2-watch-map.yml (C')                                          (merge Eduardo)
                  GGv2 path-glob -> vault SoT-ref                |
                                                                 v
                                        governor pane conta il nuovo label [source aggiunta]
```

- **(A') detection = deterministica** (path-glob PATH-FIRST, esclusi solo i commit-type senza behavior docs/chore/style/test/ci/build; zero LLM, zero GGv2 write).
- **(B) verdetto = INVARIATO** (subagent gia' repo-agnostico; invocato per numero issue).
- **Label DISTINTO** `sot-drift-candidate-ggv2` -> nessuna collisione con l'Action Game.
- **governor** = +1 source (conta il nuovo label separatamente -> "frontend drift" vs "backend drift").

## 4. (A') Detector sovereign -- fleet-side

- File: `scripts/fleet/sot_drift_ggv2_detect.py` (Python stdlib-only, test pytest).
- Input: `ops/sot-drift/ggv2-watch-map.json` (C') + checkpoint (seen-set di PR-number).
- Logica (rivista post harsh-review):
  1. Checkpoint = un SET bounded di PR-number gia' processati (`logs/sot-drift-ggv2-checkpoint.json`,
     gitignored), NON un watermark `mergedAt`: un PR merged fuori-ordine da un branch long-lived
     scavalcherebbe il watermark (fuori dalla finestra "newest N" mentre il watermark avanza) = miss
     permanente. Il seen-set elimina il leapfrog.
  2. `gh search prs --merged --sort updated --order desc` (READ-ONLY): un merge bumpa `updatedAt`,
     quindi un PR appena merged (anche da branch vecchio) emerge in cima ed e' processato UNA volta
     via seen-set. Per ogni PR unseen -> i file via `gh pr view N --json files`.
  3. **PATH-FIRST** (recall-safe, scelta Eduardo): flagga QUALSIASI PR merged che tocca un path
     sorvegliato; il commit-type e' solo etichetta di triage. Un detector di sicurezza non deve
     mai perdere silenziosamente un drift shippato come fix/refactor. Esclusi solo i type che per
     definizione NON shippano behavior (docs/chore/style/test/ci/build) = rumore puro, zero perdita
     di recall.
  4. Match dei path vs i glob della watch-map (stesso matcher dell'Action Game, backslash-exact).
  5. Se match: apre **o ACCUMULA** UN issue Game label `sot-drift-candidate-ggv2` (append delle nuove
     PR-section al body esistente -- lossless: il seen-set garantisce che le PR sono nuove, niente
     dup ne' perdita di candidate non ancora riconciliati), marker `<!-- sot-drift-ggv2 -->`.
  6. Il checkpoint avanza (seen |= tutti i PR-number esaminati) SOLO a fine pass riuscito; un errore
     `gh` solleva prima del save -> reprocess al run successivo (nessun leapfrog). Finestra piena ->
     warning nel result (no silent cap). `run_gh` ha timeout 120s.
- Auth: legge GGv2 (public) + apre issue Game (owned) via `gh`. Sotto S4U (logged-off) il profilo e'
  parziale e `gh auth` puo' mancare -> passare `GH_TOKEN` dal keys-store ACL-locked cosi' funziona
  anche loggato-fuori.
- **Nessun accesso vault** (by design). Solo flag deterministico; verdetto = subagent (B).

## 5. (C') watch-map GGv2 -- ospitata in codemasterdd (NON in GGv2)

File: `ops/sot-drift/ggv2-watch-map.json` (stdlib json, no PyYAML dep). Stesso schema della watch-map Game
(`{pattern, sot_ref, concept}`); `sot_ref` = path vault `Spaces/Dev/Evo-Tactics/<ref>` di doc **esistenti**
(verificati origin/main 2026-07-13). Mapping ampio (scelta Eduardo), scoped ai path che hanno un
doc SoT canonico:

| GGv2 path-glob | vault SoT-ref | concept |
|---|---|---|
| `assets/audio/**`, `default_bus_layout.tres`, `scripts/audio/**` | `adr/ADR-2026-04-18-audio-direction-placeholder.md`, `core/00F-ART_AUDIO_BUSINESS.md` | audio direction / impl |
| `assets/vfx/**`, `scripts/vfx/**` | `adr/ADR-2026-04-18-art-direction-placeholder.md`, `core/41-ART-DIRECTION.md`, `core/45-VISUAL-IDENTITY-CANONICAL.md` | VFX / art direction |
| `assets/ui/**`, `scripts/ui/**` | `core/30-UI_TV_IDENTITA.md`, `core/42-STYLE-GUIDE-UI.md`, `core/44-HUD-LAYOUT-REFERENCES.md` | UI / HUD identity |
| `scenes/**` | `core/17-SCREEN_FLOW.md` | screen flow / schermate |
| `scripts/combat/**` | `core/10-SISTEMA_TATTICO.md`, `core/11-REGOLE_D20_TV.md` | combat d20 / tattico |
| `scripts/campaign/**` | `core/03-LOOP.md`, `core/15-LEVEL_DESIGN.md`, `core/40-ROADMAP.md` | campaign loop / descent |
| `scripts/progression/**` | `core/25-REGOLE_SBLOCCO_PE.md`, `core/26-ECONOMY_CANONICAL.md` | progression / economy |
| `scripts/narrative/**` | `core/24-TELEMETRIA_VC.md` | narrative / VC telemetry |
| `scripts/**/*nido*`, `scripts/**/*mating*`, `scripts/**/*genetic*`, `scripts/**/*offspring*` | `core/27-MATING_NIDO.md` | Nido / mating surfaces |

Note: `scripts/{ai,coop,net,data,lifecycle,services}` NON mappati (no doc SoT canonico dedicato,
o coperti dal backend Game -> evitare rumore). Species/Forma (`20-SPECIE_E_PARTI`, `22-FORME_BASE_16`)
sono DB-generated + backend-owned -> gia' nel perimetro Game/DB, non ri-mappati qui.
La precisione dei glob e' calibrata da un QG Step-3 smoke (il mapping largo phone/session->Nido era un mis-mapping: 11 falsi -> 0 dopo lo scope a filename). Il rumore residuo dei glob larghi (combat/ui/scenes, scelta "keep broad") e' contenuto dall'esclusione dei commit-type no-behavior (sez. 4) + dal verdetto on-demand.

## 6. Anti-collisione (finding load-bearing)

L'Action Game `flag-issue.sh` (parent spec, Task 4) fa:
`EXISTING=$(gh issue list --label sot-drift-candidate --state open --json number --jq '.[0].number')`
-> riusa il PRIMO issue aperto **per solo-label**. Se il detector GGv2 usasse lo stesso label, i
due producer si contenderebbero lo stesso issue (l'Action Game potrebbe pescare e sovrascrivere il
mio issue GGv2, e viceversa) = **clobber / mislabel** appena backend-drift e frontend-drift sono
aperti insieme. Verificato: attualmente 0 issue aperti (`gh issue list ... = []`), quindi nessuna
collisione live, ma il rischio e' strutturale.

**Decisione**: label **distinto** `sot-drift-candidate-ggv2`. Il detector GGv2 riusa il suo issue
per label proprio + marker `<!-- sot-drift-ggv2 -->`. L'Action Game resta invariata (non tocco Game).
Costo: micro-modifica al governor (sez. 7) per contare anche il nuovo label. Giustificato: clobber =
classe data-loss.

## 7. Governor -- +1 source (micro-change)

`apps/cross-repo-dashboard/governor/ingest.py`:
- Nuova const URL: `SOT_GGV2_ISSUES_URL = ".../repos/MasterDD-L34D/Game/issues?labels=sot-drift-candidate-ggv2&state=open"`.
- Nuova entry in `SOURCES`: `{"id": "game-sot-drift-ggv2", "style": "gh-issues-ggv2"}` (o riuso dello
  stile `gh-issues` con URL parametrico).
- Il parser `parse_sot_drift_issues` (parsers.py) e' gia' generico (conta issue) -> riuso, cambiando
  solo `source=`/`ref=` per distinguere il segnale nel pane ("frontend SoT drift" vs "backend").
- Test: estendere `test_governor_ingest.py` / `test_governor_parsers.py` col nuovo source.

## 8. Schedule

`scripts/fleet/register-sot-drift-ggv2-task.ps1` -- Windows Scheduled Task **daily** su Lenovo
(CODEMASTERDD, canonical), mirror di `register-governor-ingest-task.ps1`:
- `-At` default ~09:00 (dopo governor-ingest 08:45).
- S4U per logged-off + `GH_TOKEN` iniettato (sez. 4) cosi' `gh` funziona anche loggato-fuori.
- `-Unregister` / `-Unattended` come il pattern esistente. ASCII-first (ADR-0021).
- **Baseline governor (rising-edge):** eseguire `governor.ingest` UNA volta prima del primo run del detector, cosi' il source `game-sot-drift-ggv2` ha un baseline `ok`; altrimenti il primo drift viene riportato ma puo' non escalare (il classifier escala sul fronte di salita ok->warning). Il ri-arm avviene quando Eduardo chiude l'issue riconciliato.

## 9. (B) Verdetto -- subagent sot-drift-verifier -- INVARIATO

Nessuna modifica. Gia' repo-agnostico: invocato per numero-issue, legge il vault SoT reale + il
change GGv2 (via `gh`), verdetto multi-signal gated, se stale propone vault branch+PR (merge Eduardo).
L'unico adattamento e' operativo (non di codice): il body dell'issue GGv2 gli fornisce PR-ref GGv2 +
SoT-ref, esattamente come per Game.

## 10. Data flow / error handling

- No-match (o solo PR non-`feat`) -> avanza checkpoint, nessun issue.
- gh api fail (GGv2 unreachable / rate-limit) -> log + exit non-zero, **non** avanza checkpoint (retry next run).
- Checkpoint missing/corrotto -> lookback bounded 7g, non full-history (evita valanga al primo run).
- Idempotenza: un solo issue GGv2 aperto riusato (reuse-by-marker) -> no spam.
- GGv2 read-only: il detector non scrive MAI GGv2 ne' vault; apre solo l'issue Game (owned, pattern gia' sanzionato).

## 11. Quality Gate (3-step, OBBLIGATORIO -- `py -m pytest scripts/tests`)

- **Step 1 smoke**: fixture payload PR-files che tocca `assets/audio/**` con title `feat(audio): ...`
  -> il matcher mappa alla audio ADR ref corretta + aprirebbe issue label `sot-drift-candidate-ggv2`.
  Idempotenza: 2o run stesso PR -> update (marker) non duplica. Filtro: PR `fix(...)` sullo stesso
  path -> nessun match (heuristic scarta polish). Unit test con gh mockato.
- **Step 2 research**: edge -- PR 0-pattern (no issue), PR multi-pattern (1 issue multi-ref),
  checkpoint-missing (lookback 7g), GGv2 unreachable (no checkpoint-advance), collisione (issue Game
  label-base aperto in parallelo -> il detector GGv2 NON lo tocca, marker-scoped).
- **Step 3 tuning**: precisione glob -- i larghi (`scripts/ui/**`, `scenes/**`) su un PR di polish
  `feat(ui): tweak` -> misura false-positive rate; tuning glob-specificity o restringere concept.
  Metrica delta before/after su un campione di PR GGv2 storici (audio/vfx = veri-positivi noti).

## 12. SDMG / governance

Metodo self-designed (detector + heuristic + collision-avoidance) = ipotesi alto-errore.
Pre-merge: **harsh-reviewer** subagent (protocollo 5, infra governance-critical) sul detector +
watch-map + governor-change. Falsificazione mirata: il filtro `feat(...)` e i glob larghi sono le
assunzioni piu' fragili -> QG Step-3 e' la CALIBRATE (falsifying experiment su PR storici).

## 13. Decisioni (questa sessione)

- Host detection: **sovereign fleet-side** (zero GGv2 write) [vs Action-in-GGv2]. -- forzato dal boundary.
- Surface: **issue Game label distinto `sot-drift-candidate-ggv2`** [vs stesso-label / issue-codemasterdd / report-json]. -- anti-collisione.
- Filtro: **PATH-FIRST recall-safe** (flagga ogni tocco di path sorvegliato; esclusi solo i type no-behavior) [vs feat-only / feat|fix|refactor|perf]. -- harsh-review: feat-only = recall hole.
- Checkpoint: **seen-PR-set** [vs mergedAt-watermark]. -- watermark leapfroggava i merge fuori-ordine.
- Scope watch-map: **ampio "keep broad"** (nido mis-mapping corretto a filename-scope) [vs minimale].
- Cadenza/host: **daily su Lenovo** [vs weekly / on-demand].
- Verdetto (B) + subagent: **INVARIATO**.

## 14. File structure

| File | Repo | Net | Responsabilita' |
|------|------|-----|-----------------|
| `ops/sot-drift/ggv2-watch-map.yml` | codemasterdd | NEW | GGv2 path-glob -> vault SoT-ref |
| `scripts/fleet/sot-drift-ggv2-detect.py` | codemasterdd | NEW | Detector: poll GGv2 (read-only) -> match -> issue Game idempotente |
| `scripts/tests/test_sot_drift_ggv2_detect.py` | codemasterdd | NEW | Unit test matcher + filtro + idempotenza (gh mockato) |
| `scripts/fleet/register-sot-drift-ggv2-task.ps1` | codemasterdd | NEW | Windows Scheduled Task daily (Lenovo, S4U + GH_TOKEN) |
| `apps/cross-repo-dashboard/governor/ingest.py` | codemasterdd | MOD | +1 source (label `sot-drift-candidate-ggv2`) |
| `apps/cross-repo-dashboard/governor/parsers.py` | codemasterdd | MOD (poss.) | source/ref distinti per il nuovo segnale |
| `apps/cross-repo-dashboard/tests/test_governor_*.py` | codemasterdd | MOD | copertura nuovo source |
| `.claude/agents/sot-drift-verifier.md` | codemasterdd | UNCHANGED | verdetto (gia' repo-agnostico) |
| GGv2 (qualsiasi) | Game-Godot-v2 | UNCHANGED | mai toccato (read-only poll) |
| `docs/KNOWLEDGE_MAP.md` | codemasterdd | MOD | wire estensione GGv2 nella sez. Drift automation |

## 15. Riferimenti

- Parent: `docs/superpowers/specs/2026-05-28-sot-drift-sentinel-design.md` + plan `2026-05-28-sot-drift-sentinel.md`
- Caso drift 2026-07-13: GGv2 #599 (audio), #601 (VFX); reconcile vault PR #270
- GGv2 build-status: `Game-Godot-v2/docs/godot-v2/PRD-BUILD-STATUS-GODOT-V2.md`
- Schedule pattern: `scripts/fleet/register-governor-ingest-task.ps1`
