---
title: evo-swarm constrained canonical_refs output -- design (lever 3 of 3)
status: proposed (revised post-SDMG 2026-06-20 -- FIX-THEN-SHIP)
date: 2026-06-20
owner: Eduardo
author: claude-opus-4-8 (hub, supervised)
scope: evo-swarm (Dafne) verification upgrade -- lever 3 of 3 (constrained schema-output)
supersedes: none
related:
  - docs/superpowers/specs/2026-06-18-evo-swarm-entity-grounding-gate-design.md (lever 1, landed)
  - docs/superpowers/specs/2026-06-20-evo-swarm-asymmetric-redundancy-checker-lever2-design.md (lever 2, rejected learning-record)
  - evo-swarm camel-agents/swarm_loop.py (_run LIVE locus, _JSON_SCHEMA, _JSON_INSTRUCTION, entity_grounding_gate wiring)
  - evo-swarm camel-agents/orchestrator.py (call_ollama, _CO02_V03_RESPONSE_TEMPLATE, _auto_populate_canonical_refs -- run_agent path only)
  - PR #89 (weak instruction-following: 0/N canonical_refs in the run_agent path)
  - SDMG falsification 2026-06-20 (FIX-THEN-SHIP; 4 P1 code-verified)
---

# evo-swarm constrained canonical_refs output -- design (lever 3 of 3)

## 0. SDMG outcome (2026-06-20) -- questa e' la revisione post-falsificazione

Panel adversariale 3-lenti, verificato su codice + Ollama live: **FIX-THEN-SHIP**. La premessa
centrale REGGE (test empirico: `format` ALZA la population di canonical_refs su qwen3-coder:30b;
negative-control no-canon emette `[]` corretto; nessun double-encode; backward-compat firma OK).
Ma 4 P1 rendevano la prima stesura non-funzionale sul live; questa revisione li adotta (SDMG:
i finding si adottano, non si difendono). Le 4 correzioni: locus reale = swarm_loop._run (non
run_agent); schema = TUTTI i campi live (format droppa i non-dichiarati); quality-arm =
advisory-probe (no baseline labeled, stesso difetto che ha rejected lever-2); kill-criterion =
matrice simmetrica.

## 1. Contesto e problema

CO-02 v0.3 chiede un array `canonical_refs` per ogni claim canonical. Ground-truth (SDMG): il
loop LIVE (`swarm_loop._run`, generazione a :964/:1029/:1144/:1213) usa il PROPRIO
`_JSON_INSTRUCTION` con uno schema a 13 campi (`_JSON_SCHEMA`, swarm_loop.py:52-69) che **NON
include affatto `canonical_refs`**. Il template CO-02 canonical_refs + `_auto_populate_canonical_refs`
vivono in `orchestrator.run_agent` -- un path che il loop live NON esegue. Conseguenze:
- Sul path live lo swarm non dichiara canonical_refs -> il gate lever-1 (`entity_grounding_gate`,
  wired swarm_loop.py:1039) gira ma ha pochi/zero ref DICHIARATI da verificare (resta la verifica
  delle entita' estratte da prosa, piu' debole).
- PR #89 (0/N) misurava il path run_agent; sul live il problema e' a monte (campo assente).

Lever-3 chiude il gap ALLA FONTE sul path GIUSTO: aggiunge `canonical_refs` allo schema del loop
live E lo rende un vincolo strutturale via Ollama `format` (JSON schema; Ollama 0.30.10 lo
supporta). Effetto collaterale ad alto valore: dichiarare canonical_refs sul live ATTIVA anche
lever-1 (gli da' ref da verificare).

**Nuance load-bearing.** `format` garantisce STRUTTURA/TIPO (campo presente, tipato, JSON valido),
NON la VERITA del contenuto (i ref possono essere allucinati o malformati -- empiricamente lo
erano). L1 verifica la verita'; L3 forza la dichiarazione. Complementari.

## 2. Goal e non-goals

**Goal.** Portare canonical_refs sul loop live da ASSENTE a dichiarato-e-ben-formato, rendendolo
vincolo strutturale (Ollama `format`), SENZA rompere i 13 campi esistenti che il loop consuma, e
attivando cosi' la verifica lever-1 sul live.

**Non-goals (OUT):** forzare ref VERI (lever-1); vincolare la qualita' della prosa; rimuovere
campi esistenti; riattivare lo swarm (PARKED; validazione A/B offline).

## 3. Decisioni ratificate

| # | Decisione | Razionale |
|---|-----------|-----------|
| D1 | Schema = FULL response object (tutti i 13 campi live `_JSON_SCHEMA` + `canonical_refs`), con `required = [canonical_refs]` SOLO | (P1-B) Ollama `format` DROPPA i campi non dichiarati. I 13 campi sono consumati da handoff (swarm_loop:978-987), dispatch Aider (:1104-1108), scoring (:604-613). Dichiararli tutti = no data-loss; required-solo-canonical_refs = vincolo targeted senza forzare prosa. "targeted" = un solo campo required, NON un sub-schema. |
| D2 | `canonical_refs: []` AMMESSO (array vuoto valido) | Task no-citation legittimi; non si forza non-empty senza false-positive. Il contenuto e' lever-1. |
| D3 | Locus = `swarm_loop._run` (:1245), NON run_agent | (P1-A) Il loop live chiama `orch.call_ollama(profile, task, model)` diretto. Passare `response_format` a run_agent = effetto ZERO sul live. |
| D4 | Fallback live = porta una mini-auto-populate nel post-process di `_run` (dopo :1259) OPPURE nessun fallback (honest) -- `_auto_populate` di run_agent NON gira sul live | (P1-A) Il "defense in depth" via _auto_populate era fittizio sul live. Decisione impl: MVP = nessun fallback live (format e' il meccanismo); auto-populate-live = follow-up se l'A/B mostra residuo. |
| D5 | Fail-graceful REALE (P2-A): su HTTP-400 schema-reject o JSON-invalid -> ri-emetti SUBITO senza `format` (fuori dal backoff network) | Il retry loop attuale (call_ollama:464-489) e' network-only; un 400 verrebbe ritentato 3x con lo stesso payload. Serve un branch dedicato. |
| D6 | Quality-arm del gate = ADVISORY PROBE, non hard-gate (P1-C) | Nessun baseline labeled (223 artifact tutti-rejected, 0 integrati), nessuna rubrica nel repo. Stesso difetto che ha rejected lever-2. La metrica HARD e' la population di ref BEN-FORMATI; la qualita'-prosa e' un probe (eyeball/2-judge advisory), non un gate, finche non esiste un baseline frozen + rubrica + >=2 rater. |

## 4. Architettura

### 4.1 Locus
`swarm_loop._run` (swarm_loop.py:1245): `response = orch.call_ollama(profile, task, model=model)`.
Passare `response_format=CANONICAL_REFS_SCHEMA`. Aggiungere a `call_ollama` (orchestrator.py:439)
il param opzionale `response_format: dict | None = None` -> se valorizzato `payload["format"] =
response_format`. Backward-compat: default None invariato (call-site a :535/:561 passano max 3
posizionali -- verificato SDMG).

### 4.2 Schema (14 campi, required-solo-canonical_refs)
Schema dell'INTERO response object = i 13 campi di `_JSON_SCHEMA` (summary, findings, proposal,
gaps, priority, next_action, trigger_reason, target_files, coherence_check{references_existing,
conflicts_with, assumes_pending}, assigned_agent, aider_task, aider_files) + `canonical_refs`
(array di `{ref:str, claim:str}`). `coherence_check` = oggetto nested tipato. `required:
["canonical_refs"]`. Valutare `additionalProperties: true` come difesa anti-data-loss.
**Pre-impl blocker (P1-B, era OQ-1)**: dump dei field reali emessi dal loop live + diff vs schema,
committato, PRIMA dell'impl -- un campo mancante dallo schema viene DROPPATO dall'output.
Aggiungere `canonical_refs` anche a `_JSON_INSTRUCTION`/`_JSON_SCHEMA` (oggi assente) cosi' il
prompt e lo schema concordano.

### 4.3 Data flow
```
swarm_loop._run (canon-touching) -> call_ollama(profile, task, response_format=SCHEMA)
  -> Ollama /api/chat con `format` -> JSON conforme (14 campi, canonical_refs presente+tipato)
  -> _try_parse_json (:1259) -- single json.loads, content gia' pulito (no double-encode, P3-B)
  -> entity_grounding_gate (lever-1, :1039) verifica il CONTENUTO dei ref dichiarati
  -> se canonical_refs `[]` su task canon-touching: residuo (D4 -- no fallback live in MVP)
```

## 5. Error handling e edge case

- **HTTP-400 schema-reject / output non-JSON** (D5): branch dedicato -> retry immediato SENZA
  `payload["format"]`, log WARNING. Mai 3x stesso payload-format. Generazione non si ferma.
- **campo mancante dallo schema -> DROPPATO** (P1-B): mitigato dichiarando tutti i 13 campi +
  field-dump pre-impl. `additionalProperties:true` come cintura.
- **canonical_refs `[]` su task canon-touching**: residuo noto (MVP no fallback live, D4).
- **latency**: constrained decoding su 30b puo' rallentare -> misurato nell'A/B con soglia
  concreta (<=20% mediana wall-clock/gen) altrimenti droppato dal gate (P3-A).

## 6. Measurement / Quality Gate (load-bearing)

A/B OFFLINE su generazione campione (`run_agent`/_run invocabili standalone, `__main__`), schema
ON vs OFF. **Harness specificato (P2-D)**: corpus FROZEN di N prompt+agent canon-touching
committato accanto all'harness; paired prompts; model-id pinnato (qwen3-coder:30b); temperature
fissa (call_ollama hardcoda 0.3); sample/cella dichiarati.

Metriche e kill-criterion (P1-D, matrice simmetrica):
- **HARD -- well-formed-ref rate** (metrica primaria, P1-D + COSA-REGGE caveat): frazione di task
  canon-touching con >=1 canonical_ref BEN FORMATO (shape `<path>#<entity>.<field>`), non mero
  non-empty (i ref erano spesso malformati). SUCCESS floor = >=0.9. Sotto floor -> REJECT.
- **HARD -- quality-delta ceiling**: se la qualita'-prosa cala oltre il ceiling -> REJECT o 2-pass.
  MA il quality-arm e' PROBE finche non c'e' baseline+rubrica (D6) -> in MVP la qualita' e'
  advisory; se appare degrado grossolano si apre la decisione 2-pass.
- **Tiebreak esplicito**: population-UP + quality-DOWN -> 2-pass (genera prosa libera, poi
  estrai/forza i ref in un secondo pass schematizzato) prima di shippare il single-pass.
- **N=40** default per il merge-gate (P2-B; guardrail progetto N=10 probe -> N=40 ratify);
  riportare CI95 su entrambe le metriche; "borderline" = CI95 overlappa la soglia.
- **auto-populate hit-rate** ON vs OFF (P2-C) se si valuta il fallback live.

## 7. SDMG falsification (gia' eseguita -- vedi sez. 0)

Round-1 fatto (FIX-THEN-SHIP, 4 P1 adottati in questa revisione). Pre-impl: un secondo
harsh-review sulla revisione + sui risultati A/B prima del merge. Negative-control: task no-canon
con schema -> `[]` senza rejection (gia' verificato empiricamente).

## 8. Testing

- Unit: `call_ollama(response_format=...)` mette `format` nel payload; default None invariato;
  D5 fallback (mock urlopen: 400 e 200+garbage -> retry no-format).
- Schema: CANONICAL_REFS_SCHEMA ben formato + i 14 campi presenti.
- **Regression (P1-B, critico)**: round-trip di un artifact 14-campi via `call_ollama(format=SCHEMA)`
  preserva `assigned_agent`/`next_action`/`aider_task`/`coherence_check` (no data-loss).
- Integration: `_run` passa lo schema; handoff/Aider/scoring non rompono.
- A/B harness (6) ripetibile. TDD: test prima dell'impl.

## 9. Rollout (parked-safe)

1. **Field-dump** (pre-impl blocker, P1-B): dump dei field reali del loop live + diff vs schema.
2. Aggiungere `canonical_refs` a `_JSON_SCHEMA`/`_JSON_INSTRUCTION`; costruire CANONICAL_REFS_SCHEMA (14 campi).
3. Impl `call_ollama` format param + D5 fallback; wire a `_run:1245`. TDD.
4. A/B (6) OFFLINE, N=40, well-formed-ref rate + quality-probe. Report delta.
5. harsh-review round-2 su revisione + A/B; fix.
6. Branch + PR; merge = Eduardo. DECISIONS_LOG entry con A/B delta.

Reversibilita': `response_format=None` (env-flag) -> pre-lever-3.

## 10. Open questions / follow-up

1. **Fallback live** (D4): MVP nessun fallback; se l'A/B mostra residuo `[]` materiale -> portare
   una mini-auto-populate nel post-process di `_run`.
2. **Quality baseline**: non esiste un set known-good labeled -> il quality-arm resta probe finche
   non se ne costruisce uno (o si decide che non serve).
3. **2-pass** come piano-B se single-pass degrada la prosa (tiebreak sez.6).
4. **codemasterdd ADR** full-arc (lever 1+3 + lever-2 learning) dopo i dati A/B.
5. **lever-1 live-efficacy**: dato che il loop live non dichiarava canonical_refs, quanto era
   inerte lever-1 sul live? Misurare prima/dopo lever-3 (lever-3 dovrebbe attivarlo).

## 11. Riferimenti

- evo-swarm: camel-agents/swarm_loop.py (_run:1224, call-site:1245, _JSON_SCHEMA:52-69,
  _JSON_INSTRUCTION:71, entity_grounding_gate:1039, handoff:978-987, Aider:1104-1108, scoring:604-613),
  orchestrator.py (call_ollama:439, _CO02_V03_RESPONSE_TEMPLATE:151, _auto_populate_canonical_refs:798)
- Ollama structured outputs (`format`+JSON-schema, >=0.5.0; fleet 0.30.10, verificato live)
- PR #89; DECISIONS_LOG 008 (score), 012 (lever-1)
- SDMG falsification 2026-06-20 (FIX-THEN-SHIP, 4 P1); ADR-0026 Protocol 7; Quality-Gate + N-sample (CLAUDE.md)
