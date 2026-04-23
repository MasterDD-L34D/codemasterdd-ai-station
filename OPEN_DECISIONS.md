# OPEN_DECISIONS

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/OPEN_DECISIONS.template.md`.
>
> Per tutto ciò che è ambiguo ma **non abbastanza bloccante** da fermare l'intera sessione. Decisioni vision-sensitive / core-changing vanno in ADR separato.

---

### [OD-001] Scenario Budget Fase 7 (ADR-0015)

- **Livello**: system / workflow / budget
- **Stato**: in attesa di dati (chiusura Fase 6)
- **Ambiguità**: quale scenario adottare post-Claude Max (2026-05-19)?
  - **A**: full-sovereign free-tier + locale, $0-50/anno
  - **B**: ibrido Claude Pro $20/mese + Ollama + cloud free, ~$240/anno
  - **C**: extension Fase 6 mirata, decisione rimandata 2-4 settimane
- **Perché conta**: definisce spesa annua + confidence operativa post-Max. Anchor dello scenario sovereign ADR-0001.
- **Miglior default proposto**: **A** (full-sovereign). Rationale: ADR-0013 ha spostato il baseline da ibrido a sovereign realistic; Claude Pro diventa spesa ingiustificata se free-tier + locale coprono ≥95% workflow.
- **Rischio se ignorata**: gap di transizione post-19/05 senza scenario definito → stress operativo + decisione reattiva.
- **File o moduli coinvolti**: ADR-0015 (da scrivere), `CLAUDE.md` sezione "Priorità modelli AI", `MODEL_ROUTING.md`.
- **Prossima azione consigliata**: completare Fase 6 criteri (dogfood ≥20, privacy n≥3, cost <$20/mese) → raccogliere dataset → ratificare A in ADR-0015.

---

### [OD-002] Fix cp1252 Windows wrapper — tenere o sostituire

- **Livello**: system / tooling
- **Stato**: proposta (deployato, monitoring)
- **Ambiguità**: il fix `chcp 65001 + PYTHONIOENCODING=utf-8` nei 6 wrapper `.cmd` tiene sotto retry loop reale? Oppure serve switch a PowerShell wrapper (`.ps1`) o `aider --no-pretty` cumulativo?
- **Perché conta**: è l'unico bug noto che blocca stabilità wrapper cloud. Una singola occorrenza rompe retry → Aider crash → manual rescue.
- **Miglior default proposto**: osservare. Se prossima retry loop → safe-fail pulito → mantenere. Se crash ricorrente → M3 backlog (PowerShell wrapper).
- **Rischio se ignorata**: scoperta a chiusura Fase 6 o durante sovereign real-world → blocker critico.
- **File o moduli coinvolti**: `~/.local/bin/aider-*.cmd` (6 file), `logs/aider-delegation-2026-04.md`.
- **Prossima azione consigliata**: T3 di `SPRINT_01.md` — monitoring empirico durante T1/T2 naturali. Documentare esito in JOURNAL.

---

### [OD-003] Default online tier 3: Groq vs Cerebras

- **Livello**: workflow / tooling
- **Stato**: aperta (non bloccante)
- **Ambiguità**: entrambi free tier, entrambi 100% quality bench, speed comparable (630 vs 733 tok/s). Fai default per classe diversa o restano simmetrici?
  - **opzione 1**: Cerebras 8B default cosmetic (più veloce), Groq 70B default behavior (capability >).
  - **opzione 2**: Both-equal, scelta a caso/preferenza sessione.
- **Perché conta**: influenza predictability + potential rate-limit exhaustion su single provider.
- **Miglior default proposto**: **opzione 1** — rationale "modello più potente per task più complessi" è ortogonale a speed. Simmetricizzare non aggiunge valore.
- **Rischio se ignorata**: nessuno critico. Dogfood sample casuale andrà ok comunque.
- **File o moduli coinvolti**: `CLAUDE.md` sezione wrapper, `MODEL_ROUTING.md`, `docs/patterns/delegation-to-aider.md`.
- **Prossima azione consigliata**: decidere dopo ≥5 behavior-critical cloud (post-P1 closure). Empirical se Cerebras 8B safe-fails su behavior → conferma opzione 1.

---

### [OD-004] Schema `DECISIONS_LOG` — indice ADR vs lista Decisione NNN

- **Livello**: repo / documentation
- **Stato**: proposta applicata provvisoria
- **Ambiguità**: il framework archivio prescrive formato "Decisione NNN numerata". Il progetto ha già 14 ADR MADR più ricchi. Come riconciliare?
- **Perché conta**: consistency con framework universale multi-progetto vs preservazione asset ADR.
- **Miglior default proposto**: **ibrido attuale** — ADR index + sezione "Decisioni non-ADR" con formato Decisione NNN per operative minori. Mantiene entrambi i contratti.
- **Rischio se ignorata**: drift latente — future sessioni che seguono template archivio potrebbero scrivere in sezione sbagliata.
- **File o moduli coinvolti**: `DECISIONS_LOG.md`, `CLAUDE.md`.
- **Prossima azione consigliata**: se dopo 2+ sessioni il formato ibrido genera confusione → riconsiderare con ADR dedicato. Finora funziona.

---

### [OD-005] `FIRST_PRINCIPLES_GAME_CHECKLIST` sostituito da cosa?

- **Livello**: workflow / documentation
- **Stato**: aperta (N/A attuale)
- **Ambiguità**: framework prescrive checklist first-principles per game repo. Questo repo è infrastructure-as-code. Skip è documentato in Decisione 002, ma vale la pena produrre un "First principles infrastructure checklist" adattato?
- **Perché conta**: se in futuro Evo-Tactics torna qui come subdirectory o se mi serve first-principles applicato a infrastruttura, il template non esiste.
- **Miglior default proposto**: **skip per ora**. Se emerge necessità concreta → adatta template. Non pre-costruire (YAGNI, ADR-0005).
- **Rischio se ignorata**: zero finché repo resta infrastructure-only.
- **File o moduli coinvolti**: eventuale futuro `FIRST_PRINCIPLES_INFRA_CHECKLIST.md`.
- **Prossima azione consigliata**: nessuna. Rivalutare se repo espande scope.

---

## Regola pratica

Se la decisione:
- blocca davvero il gameplay core / vision strategica (es. ADR-0001 fondamentale)
- cambia scope/priorità prodotto
- impatta più sistemi in modo irreversibile

**non basta questo file**: serve ADR esplicito in `docs/adr/` + approvazione utente esplicita.
