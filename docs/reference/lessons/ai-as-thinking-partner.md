# AI come thinking partner, non oracolo

**Data formalizzazione**: 2026-04-22

## La lezione

I modelli conversazionali (Claude, altri LLM) vanno usati come **rubber duck tecnico con opinione**, non come oracoli che producono risposte finali senza interrogazione.

Il valore reale emerge quando il modello aiuta ad **articolare decisioni** prima di eseguirle — non quando "fa il lavoro" al posto tuo.

## Perché questo pattern deve essere documentato

Sembra ovvio ma gli AI hanno forte tendenza a:
- Produrre output definitivo ("ecco la soluzione") anche quando dovrebbero produrre domande
- Accettare il primo framing del problema invece di sfidarlo
- Evitare di dire "non lo so" o "servono più dati"
- Compiacere l'utente con risposte sicure invece di esporre incertezza

Senza esplicita guida contraria, questi default dei modelli degradano il lavoro tecnico.

## Come applicare in pratica

### Segnali di modalità "oracolo" (da evitare)
- Risposta lunga e "completa" su query ambigua senza chiedere chiarimenti
- Mai "dipende da X, qual è il tuo X?"
- Zero alternative considerate / presentate
- Commit affrettato su una decisione complessa

### Segnali di modalità "thinking partner" (da cercare)
- Domande di chiarimento prima di agire su input ambiguo
- Enumeration di opzioni con trade-off esplicito
- Esposizione chiara di incertezza ("non ho evidenza che X")
- Proposta di verifica empirica invece di asserzione teorica
- Ammissione di errori passati quando stress-tested (steelman review)

### Pattern pratici che funzionano
1. **Decisioni complesse → tabella opzioni con pro/contro**. MADR-style `Considered Options` (ADR-0010).
2. **Ambiguità → chiedere clarifying question prima di assumere**.
3. **Steelman review periodico** — chiedere al modello di difendere al meglio le opzioni scartate, non solo confermare le decisioni prese. Caso emerso 2026-04-22: la seconda analisi ha scoperto 2 scarti basati su bias/pigrizia (Agno Pattern 2 "richiede Postgres" = falso; VoltAgent "non Aider-compat" = category error).
4. **Empirico > teorico**: verificare con test concreto quando fattibile. Esempio: guard rail wrapper 2026-04-22 testato con file che triggera silent-corruption check (validation catena end-to-end), non "trust the wiring".

## Conseguenza per il codex

- CLAUDE.md "Approvazione esplicita per azioni non banali" è diretta applicazione di questo pattern
- Convention ADR con `Considered Options` + `Pros/Cons` (MADR, ADR-0010) forza enumeration trade-off
- Memory `feedback_external_material_triage.md` cattura ratio curation (~25%) che riflette il "thinking partner vs oracle" applicato a materiale esterno

## Quando questo pattern si rompe

Con lavori meccanici/routine (format, rename, lint-fix) il modello deve essere oracle — ci sono risposte uniche e context non richiede deliberation. Documentato in ADR-0008 task-routing: cosmetic → 7B whole (oracle mode), behavior-critical → 14B diff + retry manuale (thinking partner mode).

## Reference

- ADR-0005 YAGNI minimalism (principio contro over-engineering)
- ADR-0010 MADR + skill policy (Considered Options sistematici)
- MEMORY `feedback_external_material_triage.md` (curation attiva invece di dump)
- MEMORY `feedback_communication_style.md` (approvazione esplicita, italiano, conciso)
