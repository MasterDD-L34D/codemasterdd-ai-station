# BACKLOG

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/BACKLOG.md` + sezione "Primo sprint consigliato" inline.
>
> **Archivio item chiusi**: `docs/archive/BACKLOG-archive.md` (tutti i `[x]` H1-H12, M1-M13, B1-B8, R1-R5, C1/C2/Q3, U-tasks, X1/X2, ADR-ratification, re-eval + "Bloccato da" RISOLTI estratti 2026-06-03).

## Snapshot 2026-06-03 (player-recap)

**Stato sezioni** (storia chiusa -> `docs/archive/BACKLOG-archive.md`):
- **Priorita' alta**: H1-H12 chiuse (12/12). Residui = nessuno open in alta.
- **Priorita' media**: M1-M13 chiusi. Residui OPEN = **M5 dormant** (Synesthesia UniUPO ago 2026) + **M14 deferred** Eduardo-direct (AA01 Task D, vault Card 3/4 sibling-peer boundary).
- **Priorita' bassa**: L1-L5 opportunistic, keep-with-trigger (no action proattiva).
- **ADR-0017 rollout**: U0-scaffold/U1-U6 chiusi; stack DECOMMISSIONED via OD-009 opzione B 2026-05-28. **U0-test aider --browser** ancora open (no completion evidence).
- **Bloccato da**: B1-B3 tutti chiusi 2026-05-28.
- **X cross-repo orchestrator**: X1/X2 done. **X3/X4/X5 window elapsed** -- le finestre post-Max (2026-05-20..06-19) sono ormai trascorse; il tracking cross-repo `ESCALATION_GATES.md` e' live. Re-verificare scope/rilevanza.

**Cose che devi fare adesso** (8 item OPEN):
- **U0-test** (~10min): prova aider --browser per 1-2 dev-loop session. Gate UX accettabile -> ADR-0017 step 1+ deferred.
- **M5 Synesthesia**: dormant UniUPO -- riapri ago 2026.
- **M14 AA01 Task D**: Eduardo-direct, vault Card 3/4 (sibling-peer boundary, non codemasterdd action).
- **L1-L5**: opportunistic, no action proattiva.
- **X3/X4/X5**: window elapsed -> re-verify contro `ESCALATION_GATES.md` live prima di decidere BUILD/DEFER.

Pattern di chiusura applicato: marker stale = anti-pattern #19 -> ground-truth verify (log conteggi + ADR status + sprint scope) prima di assumere "open".

---

## Item OPEN

### Priorità media

- [ ] **M5** — Synesthesia privacy first-violation test: ≥1 sessione che tocchi `views/` (cloud OK) + `controllers/` (sovereign-only). Criterio 3 ADR-0014. **Dormant** UniUPO esame ~ago 2026 (1/3 ancora).
- [ ] **M14** — AA01 Task D: guides + awesome + design. **PARTIAL DEFERRED** Eduardo-direct: #2 + #6 + #12 vault Card 3/4 sibling-peer boundary pending. #9 dair-ai/Prompt-Engineering-Guide REFERENCE_INDEX link bookmark candidate.

### Priorità bassa

- [ ] **L1** — Re-bench discriminant hard problems custom (non-Leetcode). Fuori scope Fase 6.
- [ ] **L2** — Deepseek-r1 num_predict=5000 + extract thinking migliorato. Diminishing returns.
- [ ] **L3** — Cerebras paid tier evaluation (gpt-oss-120b, qwen-3-235b). Trigger: gap quality reale.
- [ ] **L4** — Gemma 4 multimodal dogfood reale. Opportunistic.
- [ ] **L5** — Skill install policy audit periodico (cadence 3 mesi).

### ADR-0017 rollout (residuo)

- [ ] **U0-test** — Step 0 quick-win: abilita `aider --browser`, prova 1-2 sessioni dev-loop. Gate: UX accettabile? Se sì → procedi. Se no → deferred step 1+. (No completion evidence.)

### Cross-repo orchestrator (window elapsed -- re-verify)

- [ ] **X3** Gate E empirical window 30gg post-Max (era 2026-05-20 -> 2026-06-19): **window elapsed al 2026-06-03**. Cross-repo `ESCALATION_GATES.md` ora live -> re-verify se la finestra empirica e' stata loggata o se ridefinire.
- [ ] **X4** Gate E decision evaluation (~2026-06-20): BUILD full / BUILD MINIMAL / DEFER based on empirical events count. **Re-verify** contro eventi reali raccolti (window ormai trascorsa).
- [ ] **X5** Component 1 dashboard implementation (CONDITIONAL on X4 outcome >=5 events/wk OR 2-5 events/wk minimal scope). Resta CONDITIONAL su X4 ri-valutato.

---

## Dead weight / sospetti (da NON riaprire senza trigger)

- `docs/reference/agno-ollama-snippets.md` Pattern 2 → fixato, no-op pendente.
- `docs/reference/subagents-skills-candidates.md` → catalogo dormiente, nessun install pianificato.
- `final-research-and-snippets-2026-04-21-v3.md` (root) → source material esterno, triato.
- `docs/sessions/` → log historiche, congelate.
- Task #13/#14 vecchi (deepseek eval + API keys setup) → chiusi de-facto.
- `FIRST_PRINCIPLES_GAME_CHECKLIST.md` → skipped (Decisione 002 in `DECISIONS_LOG.md`).
