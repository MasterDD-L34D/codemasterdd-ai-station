# Jules tasking -- trait-hygiene batch (2026-07-14)

> Sessione "sistemare i trait": recon ground-truth su C:\dev\Game (309 DB traits,
> 5 rappresentazioni parallele, tooling maturo 7+ validator / 3 CI-gate).
> Scope Jules = SOLO la fetta HYGIENE meccanica/CI-verificabile. La fetta creativa
> (46 design-stub) e behavior-critical (wiring combat active_effects.yaml) NON va a
> Jules -- vedi Game `docs/planning/2026-07-14-r1-trait-stub-authoring-istruttoria.md`.
> Il **lancio (Start/:create) = Eduardo**-authorized (Game esterno). Ogni task consegna
> branch+PR, **merge = Eduardo** (classifier hard-block + ADR-0037).

## LESSON load-bearing -- index.json NON si rigenera con build_trait_index.js

Scoperto in salvage J3/J4 (2026-07-14). Errore nel prompt originale ("regenerate via
node scripts/build_trait_index.js"):
- `scripts/build_trait_index.js` scansiona i file trait e scrive **SOLO `data/traits/index.csv`**
  (ignora `index.json` + `species_affinity.json`). NON tocca `index.json`.
- `data/traits/index.json` = **indice-unico SOURCE** (da cui `sync_trait_lists.js` deriva le
  liste). Per una CANCELLAZIONE/dedup di un trait, la sua entry va rimossa **A MANO** da
  `index.json` (chiave = trait id; rimuovere l'oggetto + ogni ref in liste `sinergie`), poi
  `build_trait_index.js` per riallineare il CSV.
- Sintomo se si sbaglia: `trait_template_validator.py` -> "Trait presenti in index.json ma
  senza file dedicato" (coverage parity FAIL). Entrambe le sessioni J3/J4 hanno mancato questo.

### 3 layer derivati CI-drift-guarded (LOCAL GREEN != CI GREEN)

Una change che cambia il COUNT dei trait (delete/dedup) stala TRE bundle derivati; il trio
validator locale (`trait_template_validator` + `trait_audit` + `check_missing_traits`) passa
lo stesso -> verde-locale NON basta. Rigenerare tutti e 3 prima di dire "ready":
1. `data/traits/index.csv` -> `node scripts/build_trait_index.js`.
2. `data/derived/analysis/*` -> `python scripts/generate_derived_analysis.py --update-readme`.
   CI guard ENFORCING: `python tools/py/check_derived_reproducible.py --deep` (required `ci-gate`
   via `dataset-checks`). Deve dire "OK: reproducible".
3. `reports/qa_badges.json` + `reports/trait_baseline.json` -> `npm run export:qa`.
   CI check "Generate QA baselines" (non-required -> UNSTABLE non BLOCKED, ma rosso).

J3 (#3278) ha richiesto 3 commit follow-up post-CI per questi. Una RILOCAZIONE che tiene id+count
(come J4 #3279) NON stala nulla. Dettaglio memory: `reference_game_trait_index_tooling`.

## Ordine dispatch + ESITI

1. **J3 + J4** (sottoalberi disgiunti cognitivo vs difesa) -- DISPATCHED 2026-07-14, ESITI:
   - **J3** session 14788218009007265665 = COMPLETED delivery-miss (PR vuota) -> salvata dal
     changeSet + completato il dedup di index.json a mano -> draft PR #3278.
   - **J4** session 956121496509546387 = FAILED (ha inquinato il tree con scratch plan.md +
     update_index.js) -> rifatta pulita a mano (rilocazione, non dedup) -> draft PR #3279.
2. **J1** -- dispatch DOPO il merge di #3278 + #3279 (spazza tutto l'albero; collide con J3/J4
   su sottoalbero). J1 e' IMMUNE al trap index.json (vedi sotto: non tocca index.json/csv).
3. **J2** -- **locale (Eduardo/Claude)**, NON Jules: gate-2 ASCII del wrapper blocca il report IT
   + sandbox Jules fragile sui generatori.

Decisioni canoniche (ground-truth 2026-07-14):
- J3 slug canonico = `coscienza_d_alveare_diffusa` (i due file byte-identici tranne lo slug).
- J4 canonici = `difensivo` + `locomotorio` (per massa). NB J4 = i 2 trait difesa NON erano dup
  di difensivo, erano da RILOCARE (category fold, non delete).

## Prompt (ASCII, gate-compliant)

### J1 -- schema_version backfill (per-trait files only; IMMUNE al trap index.json)

254 entry su 309 non hanno `schema_version`. Stampare "2.0" SOLO dove la shape gia' conforma.
Regola load-bearing: NON stampare sui file col design-block vuoto (i 46 design-stub).
J1 tocca SOLO i file trait per-categoria, MAI index.json/index.csv (che restano allineati per
esistenza; lo schema_version mancante nell'index e' WARN non-bloccante, fuori scope J1).

```
Repo: MasterDD-L34D/Game   Base: main
Scope: data/traits/<CATEGORIA>/*.json per-trait files ONLY (one category per task).

TASK (single, narrow): add "schema_version": "2.0" to every per-trait JSON in this one
directory that DOES NOT already have the field, BUT ONLY if the file already contains a
populated design block (non-empty "tier" AND "famiglia_tipologia" AND "slot_profile").

HARD CONSTRAINTS:
1. DO NOT add the field to files whose design block is empty/missing -- those are
   intentional design-stubs (completion_flags.design_stub true) and MUST stay unstamped.
2. DO NOT edit any other field or reformat the JSON.
3. DO NOT touch data/traits/index.json, data/traits/index.csv, active_effects.yaml,
   glossary.json, or anything outside the per-trait category files. Do NOT run any
   index generator -- the per-trait edit is the whole task.

VERIFY (must pass, paste output in PR):
  python tools/lint/trait_schema_gate.py
  python tools/py/trait_template_validator.py

Deliver a branch + PR. Do NOT merge.
```

### J2 -- rigenera artefatti stale (LOCALE, non Jules)

`reports/trait_progress.md` = 251 (snapshot 2025-12-02), reale 309. Eseguire in locale:
```
python tools/py/trait_completion_dashboard.py    (-> reports/trait_progress.md)
node scripts/build_trait_index.js                (-> data/traits/index.csv)
node scripts/sync_trait_lists.js
```
Commit dei soli output rigenerati; re-run idempotente (0 diff) come verifica.

### J3 -- merge id near-dup (canonico = coscienza_d_alveare_diffusa) [SHIPPED #3278]

```
Repo: MasterDD-L34D/Game   Base: main

TASK: `coscienza_dalveare_diffusa` and `coscienza_d_alveare_diffusa` are duplicate
traits (byte-identical except the id). Canonical = coscienza_d_alveare_diffusa.
- Delete data/traits/cognitivo/coscienza_dalveare_diffusa.json
- Repoint every SOURCE reference from coscienza_dalveare_diffusa to the canonical id
  in: locales/it/traits.json, locales/en/traits.json, data/core/traits/glossary.json,
  data/core/traits/active_effects.yaml, species_affinity, and any species trait_refs.
- Remove the coscienza_dalveare_diffusa entry (the object AND any synergy-list refs)
  from data/traits/index.json BY HAND -- index.json is the indice-unico source and is
  NOT regenerated by build_trait_index.js. THEN run: node scripts/build_trait_index.js
  to realign data/traits/index.csv.
- DO NOT hand-edit other generated/derived files (logs/, reports/, data/derived/,
  data/external/evo/, docs/generated/, docs/reports/).

VERIFY (must pass): python tools/py/check_missing_traits.py ;
  python scripts/trait_audit.py --check ; python tools/py/trait_template_validator.py
Deliver a branch + PR. Do NOT merge.
```

### J4 -- fold dir difesa into difensivo [SHIPPED #3279]

```
Repo: MasterDD-L34D/Game   Base: main
Coppia 2 residua (dispatch separata): locomotivo -> locomotorio, stessa procedura.

TASK: data/traits/difesa duplicates the defensive category data/traits/difensivo.
1. For each real trait file in data/traits/difesa: if the same id already exists in
   difensivo -> it is a duplicate (merge/delete). If not -> it is a MIS-FILED trait ->
   RELOCATE it (git mv) into data/traits/difensivo, id unchanged.
2. Delete the deprecated data/traits/difesa/index.json redirect and remove the empty dir.
3. IDs unchanged => id-based refs (active_effects, glossary, locales, index.json) stay
   valid; do NOT rewrite them. Only run: node scripts/build_trait_index.js to realign
   data/traits/index.csv. If any id changes, remove the old entry from index.json by hand.
4. DO NOT create any scratch/helper file (no plan.md, no update_index.js). Modify only
   trait data files.

VERIFY (must pass): python tools/py/trait_template_validator.py ;
  python scripts/trait_audit.py --check ; python tools/py/check_missing_traits.py
Deliver a branch + PR. Do NOT merge.
```

## Fuori-scope Jules (per memoria)

- **R1** authoring 46 design-stub -> creativo, canon-gated, rischio fabrication -> Claude/human.
  Istruttoria: Game `docs/planning/2026-07-14-r1-trait-stub-authoring-istruttoria.md` (MERGED #3277).
- **R2** wiring meccaniche combat (active_effects.yaml, 12 PROPOSED #3118 + GAP2 residui)
  -> behavior-critical + freeze-adjacent + AI-playtest gate -> Claude/human.
- **R3** fork TR-NNNN vs slug (71 placeholder) -> decisione SoT-inversion, ADR PRIMA.

## Note ambiente (finding adiacente)

Il clone `C:\dev\Game` ha `.claude/worktrees/` stale (agent-worktree altrui senza glossary.json)
che rompono la raccolta jest (`speciesTraitReferences` + ~690 suite falliscono al require) --
igiene worktree separata. La CI dei PR gira jest in ambiente pulito.
