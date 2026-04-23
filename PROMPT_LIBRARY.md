# PROMPT_LIBRARY

> Compilato dal template `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/PROMPT_LIBRARY.md`.
>
> Prompt riutilizzabili specifici di questo progetto. Per prompt universali (`/INTAKE`, `/STRUCTURE`, etc.) vedi `Archivio_.../02_LIBRARY/05_Prompt_Library_and_Reference_System.md`.

## Sezione 1 — Prompt universali (copiati dal framework)

### /INTAKE
```text
Raccogli le informazioni minime mancanti e restituisci un brief pulito.
```

### /STRUCTURE
```text
Trasforma il materiale in struttura, sezioni, cartelle e documenti base.
```

### /PLAN
```text
Crea un piano operativo con ordine, dipendenze e priorità.
```

### /BUILD
```text
Produci il deliverable richiesto nella forma più utile.
```

### /REVIEW
```text
Rivedi il materiale per chiarezza, coerenza e qualità.
```

### /AUDIT
```text
Cerca problemi, omissioni, incoerenze, rischi, edge case.
```

### /COMPACT
```text
Comprimi la sessione in un riassunto operativo trasportabile. Aggiorna COMPACT_CONTEXT.md.
```

### /HANDOFF
```text
Chiudi la sessione con handoff pulito: aggiorna COMPACT_CONTEXT + BACKLOG + JOURNAL entry + memory refresh. Produci "Prossimo passo singolo più utile" esplicito.
```

---

## Sezione 2 — Prompt specifici progetto

### /DOGFOOD-LOG
Prompt per aggiungere entry conforme al log dogfood Aider (schema `docs/patterns/aider-delegation-log-template.md`).

```text
Aggiungi entry in logs/aider-delegation-2026-04.md per la delegazione Aider appena eseguita.

Raccogli da contesto sessione:
- Data/ora (ISO 8601)
- Task 1-riga descrittivo
- Classe: cosmetic | behavior | strategic
- Stack: modello + edit-format + flag rilevanti (es. "7B-whole", "Groq 70B via wrapper", "14B Q2 + diff + no-auto-commits")
- Esito: success | success-amended | safe-fail | gate-blocked | corruption | error
- Retry count (integer)
- Tokens s/r (sent/received, k per migliaia)
- Durata wall-clock
- Commit/note: hash commit + eventuali findings rilevanti

Formato: riga tabella Markdown | col1 | col2 | ... |

Se un campo non è derivabile, scrivi "-" (non inventare). Segnala valori dubbi.

Al termine: conta entries cumulative e stampa breakdown per classe (cosmetic / behavior / strategic).
```

### /ADR-NEW
Prompt per inizializzare nuovo ADR MADR (da ADR-0010 format in poi).

```text
Crea nuovo ADR in docs/adr/NNNN-topic-kebab.md (sostituisci NNNN con prossimo numero disponibile).

Struttura MADR obbligatoria:
- TL;DR (1 paragrafo italics, sintesi decisione + outcome atteso)
- Status: Proposed (default iniziale)
- Data: YYYY-MM-DD
- Decisore: Eduardo Scarpelli
- Deciders: solo-dev

Sezioni:
1. Context and Problem Statement
2. Decision Drivers (bullet)
3. Considered Options (A, B, C, D minimo — "chosen" marcato)
4. Decision Outcome (scelta + rationale)
5. Consequences (Positive / Negative / Neutral)
6. Follow-up (checkbox actionable)
7. Riferimenti (link ad ADR correlati + research + patterns)

Vincoli:
- Italiano (tranne codice/identifier)
- No speculazione: ogni claim o ha data empirico o ha rationale strutturale esplicito
- Marca incertezza con "pending validation" / "assumed" esplicito
- Collega ad ADR esistenti quando topic si tocca

Dopo Proposed → pass a Accepted solo dopo approvazione esplicita utente + eventuale validation empirica richiesta in Follow-up.
```

### /DELEGATE-CLASSIFY
Prompt per classificare task prima di Edit/Write (policy CLAUDE.md "Trigger delega in-session").

```text
Task proposto: [DESCRIZIONE BREVE]
File target: [PATH]

Classifica il task secondo docs/patterns/delegation-to-aider.md:

1. Cosmetic? (JSDoc, docstring, rename, lint-fix, typo, 1-liner)
   → se sì E working tree clean → proponi `aider-cosmetic <file>` con task short-description, attendi OK
2. Behavior-critical? (refactor singolo file, bug fix, logic change)
   → proponi `aider-refactor <file>` (local) o `aider-groq <file>` (cloud online), attendi OK
3. Strategic? (multi-file, synthesis da conversazione, design, debug architetturale, ADR writing)
   → esegui direttamente, nessuna delega

Eccezioni:
- Task <1 riga meccanica: skip proposta (overhead > savings)
- Batch operazioni simili ≥5: proponi delega anche se singolarmente sub-threshold

Output:
- Classe: cosmetic / behavior / strategic
- Stack proposto: [wrapper]
- Azione richiesta: proponi / esegui direct / batch

Default inerziale "faccio io direct" senza classification è anti-pattern esplicito CLAUDE.md.
```

### /BENCH-PROMPT
Prompt standard per bench speed modelli (usato in `scripts/bench-ollama.ps1` / `bench-cloud.ps1`).

```text
Write a Python DoublyLinkedList class with insert_head, insert_tail, remove_head, remove_tail, find, and __repr__ methods.

Constraints:
- Use type hints on all method signatures
- Include docstrings (PEP 257) on class and each method
- Edge cases: empty list, single element, duplicate values
- Thread-safety NOT required

Do not explain the code. Return only the class definition.
```

### /REVIEW-ADR
Prompt per review stato ADR prima di pass da Proposed → Accepted.

```text
Review ADR [NUMBER] docs/adr/NNNN-topic.md per pass a Accepted.

Check:
1. Tutti i Follow-up marked [x] come done SONO davvero done? (verifica file, hook, bench, test reali — non solo claim)
2. Quality evidence sufficiente per claim? (es. se claim "quality parity", bench n≥10 disponibile?)
3. Dipendenze con altri ADR: nessun conflict non risolto?
4. Risk mitigation elencate hanno counter-misura applicata o documented-as-accepted?
5. Revisione utente ricevuta? (se decisione strategica)

Se tutti check PASS → scrivi commit "docs: promote ADR-NNNN to Accepted" + edit Status line + entry JOURNAL.
Se 1+ check FAIL → lista gap in output, proponi remediation o extension Proposed.
```

---

## Sezione 3 — Prompt per scenari specifici

### /FASE6-CHECKPOINT
```text
Review stato Fase 6 rispetto criteri chiusura ADR-0014:

1. Quality bench ≥10 × ≥5 modelli: done/pending?
2. Reliability: n=? fail rate=? corruption=?
3. Privacy: sessioni enforced n=?
4. Cost: proiezione mensile $?

Per ogni criterio:
- PASS: ✅
- PARTIAL: 🟡 + gap specifico + azione per chiudere
- FAIL: 🔴 + deadline rischio + remediation proposta

Output: tabella + verdetto (on-track / extension needed / ready to close).
```

### /HARDWARE-CHANGE-IMPACT
```text
Nuovo cambiamento hardware: [DESCRIZIONE].

Rivaluta impact su:
1. Modelli locali attuali (speed, RAM headroom, VRAM offload %)
2. Decisione matrix task → stack (CLAUDE.md "Priorità modelli AI")
3. ADR rilevanti (0004, 0007, 0008, 0012, 0013)
4. Env vars Ollama persistenti
5. Scenario budget (ADR-0001, 0013)

Output:
- Cosa cambia SUBITO (zero rischio)
- Cosa DEFERRED a bench empirico
- Se serve ADR nuovo → schematic draft
- Memory refresh da fare
```

### /PRIVACY-CHECK
```text
Task proposto tocca repo/file: [PATH]

Check privacy routing (ADR-0013 + CLAUDE.md):
- repo codemasterdd-ai-station: cloud OK
- repo Game (Evo-Tactics): cloud OK
- repo synesthesia:
  - controllers/ / routes/ / middlewares/: sovereign-only
  - views/ / public/: cloud OK
- repo cliente: sovereign-only sempre

Se cloud OK → procedi con wrapper cloud.
Se sovereign-only → usa wrapper locale (aider-cosmetic / aider-refactor).
Se mixed repo → verifica file-by-file.

Se dubbio → abort e segnala.
```

---

## Sezione 4 — Prompt best-of (riferimenti framework)

- Best-of mettere ordine → usa `/STRUCTURE` + Project Architect mode
- Best-of da caos a piano → usa `/PLAN` + Systems Designer mode
- Best-of audit spietato → usa `/AUDIT` + QA Auditor mode
- Best-of decisione tra opzioni → usa `/ADR-NEW` + Project Architect mode
- Best-of compact perfetto → usa `/COMPACT` + Archivist mode

Dettaglio pattern universali: `Archivio_Libreria_Operativa_Progetti/02_LIBRARY/05_Prompt_Library_and_Reference_System.md`.
