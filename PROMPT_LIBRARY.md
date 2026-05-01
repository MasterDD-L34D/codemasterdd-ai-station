# PROMPT_LIBRARY

Recovery status: active as a prompt catalogue, not as runtime evidence.

This file was originally compiled from
`Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/PROMPT_LIBRARY.md`.
After the transplant, prompts that depend on missing logs, external repos,
or live services are marked as dormant/conditional.

## Current Rule

Use these prompts only after checking the active boundary:

1. Is the target inside this repo?
2. Does the required runtime evidence exist here?
3. Is the target external repo reactivated in `EXTERNAL_REPOS.md`?
4. Is the model/client/tool actually available on this machine?

If any answer is no, treat the prompt as historical or planning-only.

## Universal Prompts

### /INTAKE

```text
Raccogli le informazioni minime mancanti e restituisci un brief pulito.
Evidenzia subito cosa e' verificato, cosa e' assunto, e cosa richiede path o
runtime non presenti.
```

### /STRUCTURE

```text
Trasforma il materiale in struttura, sezioni, cartelle e documenti base.
Se trovi riferimenti a repo esterni, separali in: active, historical, dormant,
requires reactivation.
```

### /PLAN

```text
Crea un piano operativo con ordine, dipendenze e priorita.
Non includere task che richiedono path esterni mancanti; spostali in una sezione
"reactivation candidates".
```

### /BUILD

```text
Produci il deliverable richiesto nella forma piu utile.
Prima di modificare file, conferma che il deliverable appartenga allo scope
attivo del repo corrente.
```

### /REVIEW

```text
Rivedi il materiale per chiarezza, coerenza, qualita e drift rispetto a
PROJECT_STATE.yaml e docs/recovery/active-vs-historical-boundary.md.
```

### /AUDIT

```text
Cerca problemi, omissioni, incoerenze, rischi, edge case e vecchi piani
presentati come live senza evidenza locale.
```

### /COMPACT

```text
Comprimi la sessione in un riassunto operativo trasportabile.
Aggiorna solo fonti attive se la sessione ha cambiato stato reale.
```

### /HANDOFF

```text
Chiudi la sessione con handoff pulito:
- stato branch;
- file modificati;
- check eseguiti;
- cosa e' attivo;
- cosa resta dormant;
- prossimo passo singolo sul PC corretto.
```

## Project-Specific Prompts

### /RECOVERY-CHECK

Status: active.

```text
Verifica lo stato recovery del repo.

Leggi:
- PROJECT_STATE.yaml
- config/system-map.yaml
- docs/recovery/plan-inventory-2026-05-01.md
- docs/recovery/final-review-package.md
- BACKLOG.md

Poi rispondi con:
1. cosa e' done;
2. cosa e' ancora aperto qui;
3. cosa richiede il PC corretto;
4. cosa non va riattivato.
```

### /PLAN-INVENTORY

Status: active.

```text
Rileggi tutti i piani nel repo e classificali:
- active;
- done;
- partly done;
- dormant;
- historical;
- unverifiable here.

Non usare il JOURNAL come stato live senza confronto con PROJECT_STATE.yaml.
```

### /ADR-NEW

Status: active for repo-level decisions.

```text
Crea nuovo ADR in docs/adr/NNNN-topic-kebab.md.

Struttura:
- TL;DR
- Status: Proposed
- Date: YYYY-MM-DD
- Deciders
- Context and Problem Statement
- Decision Drivers
- Considered Options
- Decision Outcome
- Consequences
- Follow-up
- References

Vincoli:
- italiano per documentazione;
- codice e identifier in inglese;
- marca "pending validation" quando manca evidenza;
- collega ADR correlati.
```

### /REVIEW-ADR

Status: active, but evidence-gated.

```text
Review ADR [NUMBER] per eventuale passaggio a Accepted.

Check:
1. i follow-up sono davvero verificati?
2. esistono log, bench o test locali?
3. ci sono conflitti con ADR successivi?
4. la decisione richiede il PC corretto?

Se manca evidenza, non promuovere. Scrivi i gap.
```

### /DELEGATE-CLASSIFY

Status: dormant in this checkout unless Aider wrappers and models are verified.

```text
Classifica il task:
- cosmetic;
- behavior-critical;
- strategic.

Prima di proporre Aider o wrapper locali/cloud, verifica che:
- wrapper esista;
- modello/API key esista;
- target repo sia active;
- privacy scope consenta cloud.
```

### /DOGFOOD-LOG

Status: dormant until `logs/aider-delegation-YYYY-MM.md` exists or is
regenerated.

```text
Aggiungi entry al log dogfood solo se il log runtime esiste davvero in questa
copia. Se manca, non ricostruire da memoria: crea al massimo un report
redatto in docs/recovery/.
```

### /BENCH-PROMPT

Status: scaffold/conditional.

```text
Write a Python DoublyLinkedList class with insert_head, insert_tail,
remove_head, remove_tail, find, and __repr__ methods.

Constraints:
- Use type hints on all method signatures
- Include docstrings on class and each method
- Edge cases: empty list, single element, duplicate values
- Thread-safety NOT required

Do not explain the code. Return only the class definition.
```

### /FASE6-CHECKPOINT

Status: historical/dormant in this checkout.

```text
Review Fase 6 only if dogfood logs, cost evidence, and bench outputs are present.
If evidence is missing, classify the checkpoint as unverifiable here and point
to docs/recovery/runtime-artifacts-policy.md.
```

### /HARDWARE-CHANGE-IMPACT

Status: correct-PC only.

```text
Rivaluta un cambiamento hardware solo dopo verifica della macchina reale:
- RAM;
- GPU/driver;
- Ollama;
- modelli installati;
- bench locale.
```

### /PRIVACY-CHECK

Status: active principle, external execution dormant until repo reactivation.

```text
Per ogni task:
1. identifica repo e path;
2. verifica se il repo e' active o dormant;
3. classifica privacy scope;
4. scegli local/cloud solo se le evidenze sono presenti.

Se il repo e' dormant, fermati e chiedi reactivation.
```

## Historical Framework Prompts

The broader prompt framework remains in:

- `Archivio_Libreria_Operativa_Progetti/02_LIBRARY/05_Prompt_Library_and_Reference_System.md`
- `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/PROMPT_LIBRARY.md`

Those files are reference material. They are not current operating state.
