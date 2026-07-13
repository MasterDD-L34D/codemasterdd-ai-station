# Jules tasking -- trait-hygiene batch (2026-07-14)

> Sessione "sistemare i trait": recon ground-truth su C:\dev\Game (309 DB traits,
> 5 rappresentazioni parallele, tooling maturo 7+ validator / 3 CI-gate).
> Scope Jules = SOLO la fetta HYGIENE meccanica/CI-verificabile. La fetta creativa
> (46 design-stub) e behavior-critical (wiring combat active_effects.yaml) NON va a
> Jules -- vedi Game `docs/planning/2026-07-14-r1-trait-stub-authoring-istruttoria.md`.
> Il **lancio (Start/:create) = Eduardo** (Game esterno). Ogni task consegna branch+PR,
> **merge = Eduardo** (classifier hard-block + ADR-0037). Uso: jules.google -> apri/edit
> -> incolla il prompt sotto -> Start.

## Ordine dispatch

1. **J1 + J2 in parallelo** (indipendenti, rischio basso).
2. **J3 poi J4 SERIALI** -- entrambi rigenerano `data/traits/index.json`; in parallelo
   collidono. Attendere merge/rebase di J3 prima di J4.

Decisioni canoniche sciolte (ground-truth 2026-07-14):
- J3 slug canonico = `coscienza_d_alveare_diffusa` (i due file sono byte-identici
  tranne lo slug; underscore preserva la posizione dell'apostrofo "d'alveare").
- J4 canonici = `difensivo` (25 vs difesa 3) + `locomotorio` (23 vs locomotivo 12),
  per massa; Jules deve comunque verificare l'overlap semantico per-file.

## Prompt (ASCII, gate-compliant)

### J1 -- schema_version backfill (UN dispatch per categoria)

254 entry su 309 non hanno `schema_version`. Stampare "2.0" SOLO dove la shape gia'
conforma. Regola load-bearing: NON stampare sui file col design-block vuoto (sono i
46 design-stub) -- li maschererebbe come completi.

```
Repo: MasterDD-L34D/Game   Base: main
Scope: data/traits/<CATEGORIA>/*.json ONLY (one category directory per task).

TASK (single, narrow): add "schema_version": "2.0" to every trait JSON in this one
directory that DOES NOT already have the field, BUT ONLY if the file already contains
a populated design block (non-empty "tier" AND "famiglia_tipologia" AND "slot_profile").

HARD CONSTRAINTS:
1. DO NOT add the field to files whose design block is empty/missing -- those are
   intentional design-stubs (completion_flags.design_stub=true) and must stay unstamped.
2. DO NOT edit any other field or reformat the JSON.
3. DO NOT touch active_effects.yaml, glossary.json, or any file outside this directory.

VERIFY (must pass, paste output in PR):
  python tools/lint/trait_schema_gate.py
  python tools/py/trait_template_validator.py

Deliver a branch + PR. Do NOT merge.
```

### J2 -- rigenera artefatti stale

`reports/trait_progress.md` riporta 251 trait (snapshot 2025-12-02), ora sono 309.
Index/csv da riallineare.

```
Repo: MasterDD-L34D/Game   Base: main

TASK: regenerate stale trait artifacts by running the existing generators, then
commit ONLY their output. Run:
  python tools/py/trait_completion_dashboard.py    (-> reports/trait_progress.md)
  node scripts/build_trait_index.js                (-> data/traits/index.json + .csv)
  node scripts/sync_trait_lists.js

HARD CONSTRAINTS:
1. DO NOT hand-edit any generated file.
2. DO NOT change any generator logic.

VERIFY (must pass, paste output in PR): re-run all three commands a SECOND time and
confirm `git diff` is empty (idempotent), then:
  python scripts/trait_audit.py --check

Deliver a branch + PR. Do NOT merge.
```

Caveat: se `trait_progress.md` contiene prose IT non-ASCII (em-dash/accenti), il gate
ASCII del dispatch wrapper puo' bloccare -> in quel caso J2 lo esegue Eduardo/Claude in
locale (3 comandi), Jules non serve.

### J3 -- merge id near-dup (canonico = coscienza_d_alveare_diffusa)

```
Repo: MasterDD-L34D/Game   Base: main

TASK: `coscienza_dalveare_diffusa` and `coscienza_d_alveare_diffusa` are duplicate
traits (byte-identical except the id). Canonical = coscienza_d_alveare_diffusa.
- Delete data/traits/cognitivo/coscienza_dalveare_diffusa.json
- Repoint every SOURCE reference from coscienza_dalveare_diffusa to the canonical id
  in: locales/it/traits.json, locales/en/traits.json, data/core/traits/glossary.json,
  data/core/traits/active_effects.yaml, species_affinity, and any species trait_refs.

HARD CONSTRAINTS:
1. DO NOT hand-edit generated/derived files (logs/, reports/, data/derived/,
   data/external/evo/, docs/generated/, docs/reports/). Regenerate them instead:
     node scripts/build_trait_index.js
     python tools/py/trait_completion_dashboard.py
2. DO NOT change the canonical trait's content.

VERIFY (must pass, paste output in PR):
  python tools/py/check_missing_traits.py
  python scripts/trait_audit.py --check
  npx jest tests/scripts/speciesTraitReferences.test.js

Deliver a branch + PR. Do NOT merge.
```

### J4 -- merge dir-doppione (una dispatch per coppia)

Coppia 1: `difesa`(3) -> `difensivo`(25). Coppia 2 (dispatch separata, stessa
procedura): `locomotivo`(12) -> `locomotorio`(23).

```
Repo: MasterDD-L34D/Game   Base: main
Coppia: difesa -> difensivo  (lancia la coppia locomotivo -> locomotorio a parte)

TASK: merge the duplicate category directory into the canonical one.
1. FIRST verify each file in data/traits/difesa/ is a true concept-duplicate of the
   defensive category (compare famiglia_tipologia + uso_funzione). Merge only true
   duplicates into data/traits/difensivo/, keeping the difensivo id as canonical.
   If any difesa trait is genuinely distinct, LEAVE IT and note it in the PR body --
   do not force-merge.
2. Move/rename merged files; delete the emptied difesa directory.
3. Repoint SOURCE references (species trait_refs, active_effects.yaml, glossary.json,
   locales, category enums) from difesa ids to canonical ids.
4. Regenerate derived artifacts (node scripts/build_trait_index.js); do NOT hand-edit
   them.

VERIFY (must pass, paste output in PR):
  python tools/py/trait_template_validator.py
  python scripts/trait_audit.py --check
  python tools/py/check_missing_traits.py

Deliver a branch + PR. Do NOT merge.
```

## Fuori-scope Jules (per memoria)

- **R1** authoring 46 design-stub -> creativo, canon-gated, rischio fabrication ->
  Claude/human. Istruttoria: Game `docs/planning/2026-07-14-r1-trait-stub-authoring-istruttoria.md`.
- **R2** wiring meccaniche combat (active_effects.yaml, 12 PROPOSED #3118 + GAP2 residui)
  -> behavior-critical + freeze-adjacent + AI-playtest gate -> Claude/human.
- **R3** fork TR-NNNN vs slug (71 placeholder) -> decisione SoT-inversion, ADR PRIMA.
