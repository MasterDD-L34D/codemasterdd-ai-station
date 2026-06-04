# Pattern: Self-Designed-Method Governance (SDMG) -- gate ripetibile

**Stato**: RATIFIED 2026-05-17 (validato empiricamente n=7 in una sessione)
**Tipo**: pattern operativo riusabile / meta-protocollo (Cognitive Protocol 7)
**Origine**: sessione Jules-governance 2026-05-16/17 -- ADR-0032->0033, studio RELAUNCH/REDESIGN, A8 rejected
**Lesson**: `L-2026-05-033` (AA01) · **Riferimenti**: ADR-0026, ADR-0033, L-031/L-032

## Principio (invariante)

> Una conclusione o un METODO che progetto io (Claude) e' un'**ipotesi con
> tasso d'errore dimostrato alto**, non una decisione. Non diventa
> governance durevole ne' azione autonoma finche' non e' **falsificato da
> una fonte esterna/ground-truth**. **Fix the base, don't accrete.**

Evidenza n=7 in una sola sessione -- ogni mia conclusione/design NON
falsificato esternamente era errato: (1) gitpatch empty-vs-trapped, (2)
governance-error main-vs-Jules attribution, (3) corrective-safe-vs-backfire,
(4) F4 mis-attribuzione "0 merge", (5) metodo A8 (REJECT arbitro 74%), (6)
contraddizione throttle nel triager (mancata da me, trovata dall'arbitro),
(7) tuning #2314 "balance-critical" -> in realta' comment-only (corretto
dallo specialista). Pattern fortissimo, non aneddotico.

## Trigger (quando applicare)

Quando sto per **integrare in governance durevole** (ADR / agent / policy /
memory) o **rendere autonomo** un METODO/processo/automazione che ho
progettato io -- NON per azioni one-off gia' coperte da protocolli esistenti.

## Il gate (sequenza obbligatoria, in ordine)

1. **DESIGN = ipotesi**, mai decisione. Dichiararlo esplicitamente.
2. **TEST empirico** su dati reali, read-only. *Necessario ma NON
   sufficiente* (caso: RELAUNCH 6/6 "passava" ma metodo poi rigettato).
3. **FALSIFICAZIONE ESTERNA**: arbitro indipendente adversarial
   (`harsh-reviewer` subagent) + Archon CALIBRATE. **Pre-commit**: "se
   l'arbitro rigetta/forza-revisione -> adotto, non difendo." (ADR-0026 P5)
4. **ANTI-ACCRETION CHECK**: l'integrazione e' l'ennesimo emendamento su
   una base con difetto irrisolto? Se si -> STOP, **fix la base prima**
   (caso: contraddizione throttle triager prima di A8). Pattern
   ADR-0032->0033 da non ripetere.
5. **ADOZIONE NARROW**: adotta la forma minima read-only/flag che
   sopravvive alla falsificazione, NON la macchina completa. L'azione
   resta all'umano/specialista (boundary invariato).
6. **TUNING-BEFORE-EXECUTE**: ground-truth prima di applicare. L'euristico
   di selezione e' esso stesso FP-prone -> il **decider** e' lo
   specialista/ground-truth, MAI il mio euristico.
7. **POST-EXEC VALIDATION**: specialista/ground-truth corregge gli errori
   residui dell'euristico. Documenta la correzione (alimenta n).

## Anti-pattern (da NON fare)

- Design -> integra -> "poi vediamo" (salta 3-4).
- Test empirico positivo trattato come sufficiente (salta 3).
- Difendere il proprio metodo quando l'arbitro lo falsifica (viola 3 pre-commit).
- Accumulare emendamenti su base difettosa (viola 4).
- Adottare la macchina completa invece del flag minimo (viola 5).
- Fidarsi del proprio grep-signal/euristico come decider (viola 6 -- caso #2314).
- Applicare SDMG a fix one-off o azioni gia' coperte da P1-P6 (over-engineering).

## Costo/beneficio

1 dispatch arbitro ~$0.30-0.50 + 1 specialista selettivo -> ha prevenuto,
in questa sessione: A8-accretion + re-import action-surface falsificata +
1 difetto-vivo di governance spedito non visto + 1 misroute tuning. ROI
nettamente positivo vs formalizzare/eseguire un metodo difettoso.

## Integrazione operativa

- **Cognitive Protocol 7** (CLAUDE.md, sezione Cognitive workflow
  protocols): pointer + trigger. Dettaglio = questo file.
- Complementare: P3 Archon (decompose analitico) + P5 harsh-reviewer
  (arbitro). SDMG li **sequenzia** specificamente per i metodi self-designed.
