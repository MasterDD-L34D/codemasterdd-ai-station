---
title: evo-swarm constrained canonical_refs output -- design (lever 3 of 3)
status: proposed
date: 2026-06-20
owner: Eduardo
author: claude-opus-4-8 (hub, supervised)
scope: evo-swarm (Dafne) verification upgrade -- lever 3 of 3 (constrained schema-output)
supersedes: none
related:
  - docs/superpowers/specs/2026-06-18-evo-swarm-entity-grounding-gate-design.md (lever 1, landed)
  - docs/superpowers/specs/2026-06-20-evo-swarm-asymmetric-redundancy-checker-lever2-design.md (lever 2, rejected learning-record)
  - evo-swarm camel-agents/orchestrator.py (call_ollama locus, _CO02_V03_RESPONSE_TEMPLATE, _auto_populate_canonical_refs)
  - PR #89 (weak instruction-following: 0/N canonical_refs populated)
  - evo-swarm DECISIONS_LOG (008 score, 012 lever-1 ratify)
---

# evo-swarm constrained canonical_refs output -- design (lever 3 of 3)

## 1. Contesto e problema

CO-02 v0.3 chiede agli agent di emettere un array `canonical_refs` (ogni claim su
specie/biomi/trait canonical accompagnato da `{ref, claim}`) -- ma e' una PROMPT-instruction
(`_CO02_V03_RESPONSE_TEMPLATE` in orchestrator.py). PR #89 ha provato che e' weak: il modello
(qwen3-coder:30b) ignora l'istruzione e popola 0/N canonical_refs. La pezza attuale e'
server-side, `_auto_populate_canonical_refs` (orchestrator.py:798), che estrae i ref a
posteriori via regex Tier-2.a -- utile ma fragile (copre solo species_biome_affinity, dipende
dall'estrazione).

Lever-3 chiude il gap ALLA FONTE: usa il constrained schema-output di Ollama (`format` + JSON
schema, supportato da 0.5.0+; il fleet gira 0.30.10) per FORZARE strutturalmente la presenza e
il tipo di `canonical_refs` nel response, invece di sperare nell'instruction-following.

**Nuance load-bearing (aspettativa onesta).** `format` garantisce STRUTTURA e TIPO (il campo
esiste, e' un array di `{ref, claim}` ben tipati, JSON valido), NON la VERITA del contenuto: non
puo' forzare ref REALI/canonical. Quindi lever-3 chiude il gap "campo mancante / 0-N", mentre la
verita' del contenuto resta lever-1 (entity-grounding gate). I tre lever sono complementari:
L3 forza la dichiarazione, L1 la verifica.

## 2. Goal e non-goals

**Goal.** Portare il population-rate di `canonical_refs` da ~0/N a near-1/N rendendolo un
vincolo strutturale dell'output (Ollama `format`), riducendo la dipendenza da
`_auto_populate_canonical_refs` e dando a lever-1 piu' ref dichiarati da verificare.

**Non-goals (OUT):**
- Forzare ref REALI/veri (impossibile con `format`; e' lever-1).
- Vincolare l'intero artifact CO-02 (summary/findings/proposal/gaps) -- scope = canonical_refs
  targeted (D1). Over-constraint della prosa creativa = rischio qualita' (vedi 6).
- Rimuovere `_auto_populate_canonical_refs` (resta come fallback, D4).
- Riattivare lo swarm (PARKED; lever-3 validato offline + A/B su generazione campione).

## 3. Decisioni ratificate

| # | Decisione | Razionale |
|---|-----------|-----------|
| D1 | Scope = canonical_refs targeted (non full-artifact schema) | Chiude il gap 0/N (PR #89) col minimo blast-radius; evita over-constraint della prosa. Eduardo 2026-06-20. |
| D2 | Schema = response object con `canonical_refs` REQUIRED (array di `{ref:str, claim:str}`); altri campi loose (string/array); `canonical_refs: []` AMMESSO | Ollama `format` valida l'INTERO output -> serve schematizzare tutto l'object, ma con i campi non-canonical loosely typed. `[]` ammesso perche' task no-citation sono legittimi (non si puo' forzare non-empty senza false-positive; il contenuto e' lever-1). |
| D3 | Fail-graceful: se la call con `format` erra o ritorna JSON non valido -> retry SENZA format | Constrained output non deve rompere la generazione (un modello/quant che rifiuta lo schema degrada, non blocca). fail-open-but-loud. |
| D4 | `_auto_populate_canonical_refs` resta come FALLBACK | Difesa in profondita': se il modello (nonostante lo schema) emette `[]` su un task canon-touching, auto-populate riempie. L3 sposta auto-populate da pezza-primaria a safety-net. |
| D5 | Quality Gate A/B obbligatorio PRE-merge (load-bearing) | Constrained output puo' DEGRADARE la qualita' del contenuto (tradeoff LLM documentato). Misurare schema-vs-no-schema su N>=20: population-rate + content-quality delta. Spirito Quality-Gate + N-sample (non assumere il beneficio). |

## 4. Architettura

### 4.1 Locus
`call_ollama` (orchestrator.py:439). Payload `/api/chat` -> aggiungere il campo opzionale
`format` (JSON schema). Aggiunta di un parametro `response_format: dict | None = None`; se
valorizzato, `payload["format"] = response_format`. Backward-compat: default None = comportamento
attuale invariato.

### 4.2 Schema canonical_refs (CO-02 v0.3)
JSON schema dell'object response, esempio:
```json
{
  "type": "object",
  "properties": {
    "summary": {"type": "string"},
    "findings": {"type": "array", "items": {"type": "string"}},
    "proposal": {"type": "string"},
    "gaps": {"type": "array", "items": {"type": "string"}},
    "canonical_refs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {"ref": {"type": "string"}, "claim": {"type": "string"}},
        "required": ["ref", "claim"]
      }
    }
  },
  "required": ["canonical_refs"]
}
```
Solo `canonical_refs` e' `required` a livello object (targeted). Gli altri campi sono dichiarati
ma non-required (loose) per non forzare prosa vuota/innaturale. Lo schema esatto va allineato ai
field reali emessi dagli agent (step-1 impl: dump dei field correnti, NON assumere -- lezione
recon).

### 4.3 Wiring
`run_agent` passa `response_format=CANONICAL_REFS_SCHEMA` a `call_ollama` SOLO per gli agent/task
che toccano canon (gli stessi che oggi ricevono `_CO02_V03_CANONICAL_REFS_INSTRUCTION`). Task
puramente architetturali: nessuno schema (o schema con `canonical_refs` ammesso `[]`).

### 4.4 Data flow
```
run_agent (canon-touching) -> call_ollama(system, user, response_format=SCHEMA)
  -> Ollama /api/chat con `format` -> output JSON conforme (canonical_refs presente, tipato)
  -> parse; se invalid/err -> retry senza format (D3) -> _auto_populate fallback se refs ancora []
  -> response con canonical_refs popolati -> entity_grounding_gate (lever-1) verifica il CONTENUTO
```

## 5. Error handling e edge case

- **format non supportato / model rifiuta / output non-JSON** -> retry senza format (D3),
  log WARNING. La generazione non si ferma.
- **canonical_refs `[]` su task canon-touching** -> `_auto_populate` (D4) tenta il riempimento;
  se ancora vuoto, lever-1 non ha ref da verificare (residuo noto, non peggiore di oggi).
- **schema drift** (field reali != schema) -> step-1 impl deve dumpare i field live e allineare;
  un campo non previsto nello schema verrebbe droppato dall'output constrained -> data-loss.
  CRITICO: validare lo schema sui field reali PRIMA del lock (vedi 9).
- **latency**: constrained decoding puo' rallentare la generazione -- misurare nel A/B (6).

## 6. Measurement / Quality Gate (load-bearing, D5)

Constrained output puo' degradare il contenuto. PRE-merge, A/B su N>=20 generazioni reali
(stessi prompt, schema ON vs OFF):
- **Population-rate**: canonical_refs non-vuoti su task canon-touching (target: da ~0/N a
  near-1/N). Metrica primaria.
- **Content-quality delta**: la qualita' di summary/findings/proposal cala con lo schema? Giudizio
  su rubrica (o harsh-review campione). Se cala materialmente -> ridurre lo scope (es. schema solo
  sul sotto-oggetto canonical_refs via 2-pass, o tornare a prompt+auto-populate).
- **Latency delta**: overhead accettabile?
- N>=20 = direction-probe; se borderline, N>=40. Report delta before/after (Quality Gate file).

## 7. SDMG falsification plan

Metodo self-designed = ipotesi finche falsificato (ADR-0026 Protocol 7). Lever-3 NON trusted
finche:
- harsh-reviewer (different-model) rivede design + risultati A/B prima del merge.
- Negative-control: un task NO-canon con schema deve poter emettere `canonical_refs: []` SENZA
  rejection (prova che lo schema non forza false-positive).
- Falsificare l'assunto "format fixa lo 0/N": l'A/B DEVE mostrare il population-rate salire; se
  non sale (es. il modello emette `[]` valido a schema), lever-3 non ha valore -> REJECT.

## 8. Testing

- Unit: `call_ollama(response_format=...)` mette `format` nel payload; default None invariato;
  fallback senza-format su errore/JSON-invalid (mock urlopen).
- Schema: validazione del CANONICAL_REFS_SCHEMA (JSON schema ben formato).
- Integration: run_agent passa lo schema solo per agent canon-touching.
- Negative-control: task no-canon -> `[]` accettato, nessun reject.
- A/B harness (6) come script ripetibile.
- TDD: test prima dell'impl.

## 9. Rollout (parked-safe)

1. Step-1: dump dei field reali emessi dagli agent (NON assumere) -> allinea lo schema.
2. Impl `call_ollama` format param + CANONICAL_REFS_SCHEMA + fallback (D3), TDD.
3. A/B measurement (6) OFFLINE su generazione campione -- nessun swarm run.
4. harsh-reviewer external falsification (7); fix.
5. Branch + PR su evo-swarm; merge = Eduardo. DECISIONS_LOG entry su ratify (con A/B delta).
6. Attivo per il prossimo swarm run; non triggera riattivazione.

Reversibilita: `response_format=None` (env-flag) -> comportamento pre-lever-3.

## 10. Open questions / follow-up

1. **Schema field alignment** (BLOCCANTE impl): dumpare i field reali prima del lock (4.2/5).
2. **Quality degradation**: se l'A/B mostra calo qualita' materiale -> 2-pass o rollback a
   prompt+auto-populate (decisione post-dati).
3. **codemasterdd ADR**: un ADR full-arc (lever 1+3 + lever-2-rejected learning) dopo i dati A/B.
4. Lever-2 strutturale resta archiviato (learning-record); rivalutabile separatamente.

## 11. Riferimenti

- evo-swarm: camel-agents/orchestrator.py (call_ollama:439, _CO02_V03_RESPONSE_TEMPLATE:151,
  _auto_populate_canonical_refs:798, run_agent:492), scripts/verify-swarm-claims.py (lever-1)
- Ollama structured outputs (`format` + JSON schema, >=0.5.0; fleet 0.30.10)
- PR #89 (weak instruction-following 0/N); DECISIONS_LOG 008 (score), 012 (lever-1)
- ADR-0026 Protocol 7 (SDMG); global Quality Gate (smoke/research/tuning, N-sample)
