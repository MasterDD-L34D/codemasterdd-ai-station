> ARCHIVED 2026-06-03 (context-files reorg Fase 2). SUPERSEDED -- live direction = GOALS.md + ORCHESTRATION.md.
> Historical record.

# ROADMAP — CodeMasterDD AI Station

> Rinormalizzata post ADR-0013/0014 (2026-04-23) + refresh post Fase 6 closure (2026-05-08). Numerazione fasi conservata dall'ADR-0001 originale (1-3 = setup/transizione/steady state) + evoluzione operativa 4-8 introdotta in Fase di tracking.
>
> **Scelta strategica originale**: consolidare il non-core e continuare in-place con struttura più stretta. **Esito 2026-05-07**: Fase 6 CLOSED anticipata 10gg vs target sett.4. ADR-0015 + ADR-0017 entrambi Accepted. Scenario A full-sovereign $0-50/anno confermato per post 19/05.
>
> **Nomenclatura fasi**: ROADMAP usa numerazione Fase 6/7/8 (granulare). SPRINT_02.md usa "Fase 7 (post-Max)" come ombrello budget+steady-state. Convergenza semantica accettata: Fase 7 ROADMAP = ADR-0015 ratification (DONE), Fase 8 ROADMAP = sovereign steady state operativo (= "Fase 7 SPRINT_02" colloquiale).

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

## Fase 6 — Empirical tracking compressa (22/04 → 07/05/2026) ✅ CLOSED 2026-05-07

**Obiettivo**: raccogliere dati empirici sufficienti per ratificare ADR-0015 Budget decision post-Claude Max.

**Esito**: chiusura **anticipata 10gg** vs target sett.4 originale. ADR-0015 (scenario A full-sovereign) + ADR-0017 (UI + observability stack) entrambi Accepted 2026-05-07.

**Definition of done finale (criteri ADR-0014)**:
1. Quality bench ≥10×≥5 → ✅ **PASS** (75 test 100% pass@1, validato 23/04)
2. Reliability n≥20, fail <30%, zero corruption → ✅ **PASS soft-override** (n=12 + 3 smoke = 15 cumulative, fail rate 8.3%, behavior 5/3 superato 167%, zero silent-corruption working-tree)
3. Privacy ≥3 sessioni enforced → ⏸️ **DEROGATO** (Synesthesia dormant fino esame UniUPO ~ago 2026, retroattivo a riattivazione documentato in ADR-0015)
4. Cost <$20/mese → ✅ **PASS** (cumulative $0.0217, 0.108% budget mensile, scenario A proiettato $2.6/anno)

**Deliverable consegnati**:
- `logs/aider-delegation-2026-04.md` (dataset 12 dogfood) + smoke 2026-05-07 (3 wrapper, 2 PASS)
- `ccusage` aggregato + cloud cumulative documentati in JOURNAL
- COMPACT_CONTEXT v8 → v12 (refresh sequenziale)
- ADR-0015 + ADR-0017 Accepted (PR #4 + #6 mergeati)

**Trigger ri-evaluation soft-override (validi durante Fase 7-8 SPRINT_02)**:
- silent-corruption working-tree ≥1 caso reale → ADR-0015 addendum + scenario B revisited
- fail rate cumulative >15% → revisione routing tier
- privacy violation in repo non-sensitive → ADR addendum reactive

---

## Fase 7 — Budget decision (07/05/2026) ✅ CLOSED 2026-05-07

**Obiettivo**: ratificare scenario operativo post-Claude Max via ADR-0015.

**Esito**: ADR-0015 **Accepted 2026-05-07** (anticipato vs target ~20/05). **Scenario A full-sovereign $0-50/anno** selezionato con deroga esplicita criterio #3 privacy (Synesthesia dormant). Scenario B (Claude Pro $240/anno) declassato (parity 70B cloud vs 14B Q2 confermata). Scenario C (extension Fase 6) scartato (overhead non giustificato).

**Dipendenze**: chiusura Fase 6 ✅ + disponibilità decisore ✅ (sessione 7/5 sera 12h auto-mode).

**Deliverable consegnati**:
- `docs/adr/0015-fase7-budget-decision-full-sovereign.md` (MADR format, Accepted)
- `docs/adr/0017-ui-observability-stack.md` (MADR format, Accepted)
- CLAUDE.md roadmap aggiornato + COMPACT_CONTEXT v11/v12 + STATUS_MULTI_REPO refresh

**Definition of done**: ADR-0015 Accepted ✅ + CLAUDE.md ✅ + memoria allineati ✅.

---

## Fase 8 — Sovereign steady state (da 20/05/2026) 🟡 PLANNING (transition window 11gg residui)

**Obiettivo**: operatività autonoma low-cost, stack sovereign come default. Equivalente a "Fase 7 post-Max" in nomenclatura SPRINT_02.md.

**Perché in questa posizione**: è lo stato target finale di ADR-0001; rappresenta il successo del progetto. ADR-0015 Accepted (scenario A) ha sbloccato la fase.

**Dipendenze**:
- ✅ ADR-0015 Accepted scenario A
- ✅ Pre-Max checklist tecnica (8/5): 6 wrapper sovereign + API keys + Aider 0.86.2 + stack hot-restart-ready
- ⏳ 2026-05-19 Claude Max expiration (hard date, 11gg residui)
- ⏳ SPRINT_02 prima sessione full-sovereign (~20/05+)

**Rischi**:
- Drift silenzioso stack che degrada → mitigazione: dogfood organico continuativo (T2 SPRINT_02), cost tracking mensile (T5).
- Trigger ADR reactive (silent-corruption, fail rate >15%, privacy leak) → mitigazione: T7 review fine sprint con decisione continuita'/correzione/SPRINT_03.

**Deliverable attesi (sprint window 20/05 → ~19/06)**:
- T1 Smoke test sovereign empirico ✅ **DONE 2026-05-07 anticipato** (PR #6, 2/3 wrapper PASS, pattern wrong-target-file documentato)
- T2 Dogfood organico continuativo (target soft n>=20 cumulative entro 19/06)
- T3 Stack ADR-0017 hot-restart procedure validation (<60s up + endpoint health)
- T4 Cleanup PR esterni opportunistico ✅ **DONE 2026-05-07** (4/4 PR triagati: #97 closed-stale, #105 #61 #10 merged)
- T5 Cost tracking primo mese full-sovereign (~15/06): target <$5/mese, atteso <$1
- T6 Privacy validation Synesthesia preview (opportunistic, deroga ADR-0014 #3 retroattiva ago 2026)
- T7 Review fine sprint: decisione continuita'/mid-course correction/SPRINT_03

**Definition of done**: 30 giorni operatività post-Max + ≥1 revisione qualitativa senza gap materiali + zero silent-corruption invariato.

**Riferimento operativo**: `SPRINT_02.md` (planning, finestra 20/05 → ~19/06).

---

## Estensioni future (non pianificate, opzionali)

- **Mac mini M4 Pro 48GB**: se emergono task 30B+ dense critici (OR, budget scherzoso). NOT dependency.
- **ADR retrofit MADR completo**: skippato per ROI basso (ADR-0010). Re-consider se doc consumer esterni (team futuro).
- **Skill ecosystem expansion**: quando uso naturale richiede > 5 skill installate (audit ADR-0010).

---

## Calendario sintetico

```
2026-04-23  ←  Fase 6 entry (ADR 0012/0013/0014 ratificati)
2026-04-24  ←  Sprint 01 early-hit (ADR-0014 H5 review settimana 2 anticipata)
2026-05-07  ←  Fase 6 CLOSED + Fase 7 CLOSED (ADR-0015 + ADR-0017 entrambi Accepted, 12h auto-mode)
2026-05-08  ←  Oggi: governance refresh + pre-Max checklist DONE; 11gg residui Claude Max
2026-05-19  ←  Claude Max expiration (hard date)
2026-05-20+ ←  Fase 8 sovereign steady state operativo (SPRINT_02 prima sessione full-sovereign)
2026-06-19  ←  Target chiusura SPRINT_02 + decisione SPRINT_03 scope
2026-08+    ←  Synesthesia riattivazione → criterio ADR-0014 #3 retroattivo
```
