# OPEN_DECISIONS

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/OPEN_DECISIONS.template.md`.
>
> Per tutto ciò che è ambiguo ma **non abbastanza bloccante** da fermare l'intera sessione. Decisioni vision-sensitive / core-changing vanno in ADR separato.

---

### [OD-001] ~~Scenario Budget Fase 7 (ADR-0015)~~ **CLOSED 2026-04-24 (Proposed) → ratificato 2026-05-07 (Accepted)**

- **Livello**: system / workflow / budget
- **Stato**: **CLOSED + RATIFIED** — formalizzato in **ADR-0015 Proposed 2026-04-24** → **Accepted 2026-05-07** (sessione Fase 6 closure, PR #4 mergeato). Opzione A (full-sovereign $0-50/anno) confermata, con **deroga esplicita criterio #3 privacy** (Synesthesia dormant fino esame UniUPO ~ago 2026, retroattivo a riattivazione).
- **Ambiguità originale**: quale scenario adottare post-Claude Max (2026-05-19)? (A full-sovereign / B ibrido Pro / C extension)
- **Decisione finale**: A — full-sovereign. B declassato (quality parity 5/5 stack + 70B cloud parity vs 14B Q2 local empirically confermata). C scartato (costo bridge 3 mesi ingiustificato senza lavoro reale su Synesthesia).
- **File coinvolti (output)**: `docs/adr/0015-fase7-budget-decision-full-sovereign.md` (Accepted), `DECISIONS_LOG.md` aggiornato.
- **Trigger Accepted ratificati**: soft-override esteso n>=12 con 5 rationale additivi (trigger ADR-0008 confermato a #12, behavior 5/3 superato 167%, fail rate 8.3%, zero silent-corruption, no dogfood sintetici).

---

### [OD-002] ~~Fix cp1252 Windows wrapper — tenere o sostituire~~ **CLOSED 2026-05-07 (soglia raggiunta)**

- **Livello**: system / tooling
- **Stato**: **CLOSED — non bloccante**. n=15 cumulative dogfood + smoke (Fase 6 closure) **senza retry loop naturale osservato**. Trigger di pazienza ADR-0014 raggiunto: il fix `chcp 65001 + PYTHONIOENCODING=utf-8` deployato ha tenuto in tutti i task reali; nessun crash UnicodeEncodeError post-deploy. Switch alternative (PowerShell wrapper M3) **deferred** senza trigger empirico.
- **Ambiguità originale**: il fix tiene sotto retry loop reale? Oppure serve switch a PowerShell wrapper o `aider --no-pretty` cumulativo?
- **Decisione finale**: **mantenere fix `.cmd` deployato**. Re-trigger condizionale: se ≥1 crash UnicodeEncodeError emerge in SPRINT_02 (T1 SPRINT_02 trigger) → riapertura via M3 backlog (PowerShell wrapper alternative).
- **Perché conta originale**: era l'unico bug noto che bloccava stabilità wrapper cloud. Empirically risolto.
- **File o moduli coinvolti**: `~/.local/bin/aider-*.cmd` (6 file invariati), `logs/aider-delegation-2026-04.md` (12 entries clean).
- **Prossima azione**: nessuna proattiva. Solo reactive monitoring durante T2 SPRINT_02 (dogfood organico continuativo).

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

### [OD-006] ~~Routing threshold: constraint count per delegazione cloud vs locale vs manuale~~ **CLOSED 2026-04-24**

- **Livello**: workflow / tooling
- **Stato**: **CLOSED** — formalizzata in ADR-0016 (Proposed 2026-04-24). Pattern confermato da n=6 data points cross-tier + n=11 cumulative. Follow-up raccolta n≥3 data points addizionali verso Accepted tracciato in BACKLOG H6 (chiuso anch'esso).
- **Ambiguità**: Groq 70B cloud degrada significativamente su task behavior-critical con ≥5 constraint espliciti (dogfood #7: 20% compliance). Qwen 7B local degrada su task cosmetic con ≥2 constraint trasformativi (dogfood #8: 50% compliance). **Soglia routing quantitativa va formalizzata**?
- **Perché conta**: routing attuale classifica per **natura task** (cosmetic/behavior/strategic). Il nuovo dato suggerisce **constraint-count** come seconda dimensione discriminante — potenziale revisione della decision matrix CLAUDE.md.
- **Miglior default proposto**:
  - **Task con 1 constraint semplice** (add-only, fix puntuale): 7B local OK
  - **Task con 2-3 constraint fix+transform**: 14B Q2 local o 70B cloud (entrambi ~85% attuali)
  - **Task con ≥5 constraint strict**: **rewrite manuale Claude Code** — delegare è anti-pattern empiricamente
- **Rischio se ignorata**: delegazioni falliscono silently, user deve fare rescue retroattivo — già successo dogfood #7 con return-value divergence blocking bug.
- **File o moduli coinvolti**: `CLAUDE.md` sezione "Priorità modelli AI" + `docs/patterns/delegation-to-aider.md` + `MODEL_ROUTING.md`.
- **Prossima azione consigliata**: raccogliere altri n≥3 dogfood con constraint-count variabile per confermare pattern. Se confermato → ADR dedicato (0016?) formalizza second-dimension routing.

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
