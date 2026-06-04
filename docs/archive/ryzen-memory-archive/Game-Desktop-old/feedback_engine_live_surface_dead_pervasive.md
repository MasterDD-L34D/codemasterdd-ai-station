---
name: Engine LIVE Surface DEAD anti-pattern pervasive across pillars
description: Multi-system audit 2026-05-06 conferma Gate 5 violation diffuso. Pillar status claim post-engine-shipped è aspirational, non reality. Audit verifica con grep frontend caller obbligatoria.
type: feedback
originSessionId: 43af369a-a1ea-416b-87cb-0cbe6f22509e
---
**Pattern dominante audit 2026-05-06**: backend ricco, surface incompleta. Pillar status `🟢` claimed post-engine-ship sono ASPIRAZIONALI, non player-visible.

## Cases trovati audit 4-domain 2026-05-06

| Sistema | Engine LIVE | Surface | Verità Pillar |
|---|---|---|---|
| Ennea voice 9/9 palette × 7 beat × 189 line | ✅ endpoint /:id/voice | ❌ ZERO frontend caller in-session | P4 🟡++ NOT 🟢 |
| Form mech link (form_id) | ✅ form_id propagato | ❌ NO stat modifier combat (cosmetic) | P3 🟡++ NOT 🟢++ |
| Innata trait grant | ❌ campo `innata_trait_id` mai esistito in yaml | ❌ NO grant runtime | P3 drift critical |
| Job D1 resource gating PP/SG/PT | ✅ definito yaml | ❌ skipped MVP `abilityExecutor:542` cosmetic | P3 D1 |
| Job D2 PE resource | ✅ aberrant declared | ❌ session engine non implementa PE → silently ignored | P3 D2 |
| Job D3 mbti_forms.yaml soft_gate | ✅ definito | ❌ ZERO runtime enforcement | P3 D3 |
| World gen 4 livelli SoT | ✅ data 4 livelli | ❌ runtime consume 29% (5/7 campi biome ignorati) | P1 partial |
| L2/L3/L4 ecosystem yaml | ✅ 5 file yaml | ❌ ZERO runtime wire | P1 unclaimed |
| Mutation aspect_token | ✅ 36 mutation + token | ❌ NOT wired runtime | P2 partial |
| Pack d20 trait_T1 token | ✅ pack yaml | ❌ NO resolver — label testuali | P2 D1 |

## Why happens

1. **Sprint declares 🟢 post-engine ship** senza Gate 5 surface verify
2. **Authoring intent gap**: 43/64 species trait_plan IDs silently ignored (33% pool coverage)
3. **Web v1 → Godot phone flow gap**: backend designed host-as-arbiter (web JS drain), Godot phone NO drain logic
4. **forms.yaml canonical NON ESISTE**: doc dichiara file fantasma (massive doc-vs-code drift)

## How to apply

**Audit prima di claim 🟢**:
```bash
# Grep frontend caller per ogni endpoint backend
grep -rn "<endpoint>" apps/play/ --include="*.js"
grep -rn "<setter API>" apps/play/src/

# Se 0 results → Engine LIVE Surface DEAD = NOT 🟢
```

**Multi-system audit prima di major design pivot**: spawn 4 parallel subagent (world-gen + species-forms-traits + job + mbti-ennea) → diff canonical vs runtime + drift matrix. Outputs informano decisione pivot direction.

**Foundation prima di feature scope-large**: se user vision richiede COMBO + vote + world muta (~67-70h), MA pillar foundation surface-DEAD → ship foundation prima (Opt C ~18h), poi feature post-playtest data-informed.

**Ticket gate sequence**: Ennea voice frontend → Innata trait grant → form stat applier prima di N+ COMBO upgrade. Senza foundation, COMBO sarebbe pre-mature.

## Memory pattern

Quando vedi claim "Pillar X 🟢 candidato post PR #YYYY":
1. Verifica grep frontend caller dei key engine
2. Se 0 → claim ASPIRATIONAL, audit needed
3. Audit master doc usable as evidence layer per master-dd review
