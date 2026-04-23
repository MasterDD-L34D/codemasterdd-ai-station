# ROADMAP — CodeMasterDD AI Station

> Rinormalizzata post ADR-0013/0014 (2026-04-23). Numerazione fasi conservata dall'ADR-0001 originale (1-3 = setup/transizione/steady state) + evoluzione operativa 4-7 introdotta in Fase di tracking.
>
> **Scelta strategica**: **Consolidare il non-core e continuare in-place con struttura più stretta**. Motivo: lo stack è già materializzato e funzionante (88% barra), 3 ADR ratificati nelle ultime 48h. Non serve estrarre un core né ricostruire. Serve **raccogliere evidenza empirica in finestra compressa** per ratificare ADR-0015 e chiudere.

---

## Fase 1 — Setup intensivo (aprile 2026) ✅ COMPLETED

**Obiettivo**: build infrastructure + learning con Claude Max attivo.

**Stato**: chiusa 2026-04-20 circa. Hardware hardened, dev stack installato, Ollama + Qwen 7B operativo, repo GitHub live, CLAUDE.md + ADR base.

**Deliverable chiusi**: Lenovo setup + 3 ADR base + 1 modello Ollama + bench 114 tok/s.

---

## Fase 2-5 — Discovery & materialization (20/04 → 22/04) ✅ COMPLETED

**Obiettivo**: scoprire limiti stack agentic, iterare quantization/tools, migrare progetti reali, stabilizzare guard rail.

**Milestone**: 
- Cline ✕ Qwen 7B → NOT viable (ADR-0006).
- Aider + 14B Q2 + diff → sweet spot behavior (ADR-0007/0008).
- Migrazione Evo-Tactics + Synesthesia completata.
- AgentShield baseline + commit-guard PreToolUse + MADR format.

**Stato**: chiusa 2026-04-22.

---

## Fase 6 — Empirical tracking compressa (22/04 → ~20/05/2026) 🟡 IN PROGRESS (30%)

**Obiettivo**: raccogliere dati empirici sufficienti per ratificare ADR-0015 Budget decision post-Claude Max.

**Perché in questa posizione**: lo stack è completo tecnicamente; manca solo evidenza di sostenibilità operativa. 4 settimane sono il tempo proporzionato alle domande rimanenti (Q3 quality + Q4 reliability, entrambe time-bound settimane non mesi — Q1/Q2 risolte infrastrutturalmente da ADR-0013).

**Dipendenze**: nessuna esterna. Richiede solo uso naturale della workstation con trigger delega attivi.

**Rischi**:
- n<20 se pace dogfood rallenta. Mitigazione: H1/H2 backlog priority high.
- Bug cp1252 ricorrente → blocca ciclo retry → workaround manual. Mitigazione: H3 monitoring.
- Emergere gap quality cloud non catturato da toy bench. Mitigazione: dogfood real-world + privacy discriminator + option C (extension mirata).

**Deliverable attesi**:
- `logs/aider-delegation-2026-04.md` + successivi mensili con n≥20 task
- `ccusage` aggregato + cloud costs documentati in JOURNAL
- 1+ sessione Synesthesia per privacy validation
- Memoria/COMPACT_CONTEXT refresh a settimana 2 e 4

**Definition of done** (criteri ADR-0014):
1. Quality bench ≥10 problemi × ≥5 modelli ✅ già fatto (75 test)
2. Reliability: n≥20 dogfood, fail rate <30%, zero silent-corruption
3. Privacy: ≥3 sessioni reali classificazione repo enforced senza violation
4. Cost: <$20/mese (ccusage + cloud) extrapolato

Se tutti PASS → Fase 7. Se 1+ non regge → Fase 6b Addendum mirato (non blank check 3 mesi).

---

## Fase 7 — Budget decision (~20/05/2026) 🔴 BLOCKED

**Obiettivo**: ratificare scenario operativo post-Claude Max via ADR-0015.

**Perché in questa posizione**: decisione informata richiede output Fase 6; non anticipabile.

**Dipendenze**: chiusura Fase 6 + disponibilità decisore (half-day).

**Rischi**: overcorrection (decidere prima che i dati bastino) vs underproof (estendere Fase 6 senza criteri chiari). Mitigazione: 4 criteri closure già formalizzati ADR-0014.

**Deliverable attesi**:
- `docs/adr/0015-budget-decision-post-claude-max.md` (MADR format)
- Scenario scelto (A full-sovereign / B ibrido Pro / C extension) con rationale data-driven
- Aggiornamento CLAUDE.md roadmap + COMPACT_CONTEXT

**Definition of done**: ADR-0015 Accepted + CLAUDE.md + memoria allineati.

---

## Fase 8 — Sovereign steady state (da 20/05/2026) ⚪ PLANNED

**Obiettivo**: operatività autonoma low-cost, stack sovereign come default.

**Perché in questa posizione**: è lo stato target finale di ADR-0001; rappresenta il successo del progetto.

**Dipendenze**: ADR-0015 Accepted con scenario A o B. Non attiva con C (extension rimanda).

**Rischi**: drift silenzioso (stack che degrada senza che me ne accorga). Mitigazione: quarterly review + tracking continuativo `logs/aider-delegation-YYYY-MM.md`.

**Deliverable attesi**:
- Workflow dev quotidiano ≥1 settimana senza Claude Max (validation)
- Logs mensili continuativi
- Eventuale ADR reattivo se emergono regressioni

**Definition of done**: 30 giorni operatività post-Max + ≥1 revisione qualitativa senza gap materiali.

---

## Estensioni future (non pianificate, opzionali)

- **Mac mini M4 Pro 48GB**: se emergono task 30B+ dense critici (OR, budget scherzoso). NOT dependency.
- **ADR retrofit MADR completo**: skippato per ROI basso (ADR-0010). Re-consider se doc consumer esterni (team futuro).
- **Skill ecosystem expansion**: quando uso naturale richiede > 5 skill installate (audit ADR-0010).

---

## Calendario sintetico

```
2026-04-23  ←  Oggi: Fase 6 in corso, ADR 0012/0013/0014 ratificati
2026-04-30  ←  Review settimanale interna (opportunistica)
2026-05-07  ←  Review settimana 2 Fase 6 (ADR-0014 follow-up)
2026-05-19  ←  Claude Max expiration (hard date)
2026-05-20  ←  Target chiusura Fase 6 + ADR-0015 decision
2026-06-01+ ←  Fase 8 sovereign steady state (se scenario A/B)
```
