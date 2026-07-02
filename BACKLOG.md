# BACKLOG

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/BACKLOG.md` + sezione "Primo sprint consigliato" inline.
>
> **Archivio item chiusi**: `docs/archive/BACKLOG-archive.md` (tutti i `[x]` H1-H12, M1-M13, B1-B8, R1-R5, C1/C2/Q3, U-tasks, X1/X2, ADR-ratification, re-eval + "Bloccato da" RISOLTI estratti 2026-06-03).

## Snapshot 2026-06-03 (player-recap)

**Stato sezioni** (storia chiusa -> `docs/archive/BACKLOG-archive.md`):
- **Priorita' alta**: H1-H12 chiuse (12/12). Residui = nessuno open in alta.
- **Priorita' media**: M1-M13 chiusi. Residui OPEN = **M5 dormant** (Synesthesia UniUPO ago 2026) + **M14 deferred** Eduardo-direct (AA01 Task D, vault Card 3/4 sibling-peer boundary).
- **Priorita' bassa**: L1-L5 opportunistic, keep-with-trigger (no action proattiva).
- **ADR-0017 rollout**: U0-scaffold/U1-U6 chiusi; stack DECOMMISSIONED via OD-009 opzione B 2026-05-28. **U0-test SUPERSEDED 2026-06-20** (ADR-0017 step 1+ morto via ADR-0030; non piu' task).
- **Bloccato da**: B1-B3 tutti chiusi 2026-05-28.
- **X cross-repo orchestrator**: X1/X2 done. **X3/X4/X5 CHIUSI** -- re-verify 2026-06-10 (0 eventi in-window, window mai instrumentata) + ratifica Eduardo 2026-06-11: X4 = DEFER + retire counter, X5 = superseded.

**Cose che devi fare adesso** (7 item OPEN; U0-test superseded 2026-06-20):
- ~~U0-test~~: **SUPERSEDED 2026-06-20** -- ADR-0017 step 1+ morto via ADR-0030; aider --browser usabile ad-hoc, non e' un task.
- **M5 Synesthesia**: dormant UniUPO -- riapri ago 2026.
- **M14 AA01 Task D**: Eduardo-direct, vault Card 3/4 (sibling-peer boundary, non codemasterdd action).
- **L1-L5**: opportunistic, no action proattiva.
- **X3/X4/X5**: CHIUSI (X4 ratificato DEFER + retire counter 2026-06-11; dolori reali coperti dal canale fleet governor R0/R1).

Pattern di chiusura applicato: marker stale = anti-pattern #19 -> ground-truth verify (log conteggi + ADR status + sprint scope) prima di assumere "open".

---

## Item OPEN

### Priorità media

- [ ] **M5** — Synesthesia privacy first-violation test: ≥1 sessione che tocchi `views/` (cloud OK) + `controllers/` (sovereign-only). Criterio 3 ADR-0014. **Dormant** UniUPO esame ~ago 2026 (1/3 ancora).
- [ ] **M14** — AA01 Task D: guides + awesome + design. **PARTIAL DEFERRED** Eduardo-direct: #2 + #6 + #12 vault Card 3/4 sibling-peer boundary pending. #9 dair-ai/Prompt-Engineering-Guide REFERENCE_INDEX link bookmark candidate.
- [x] **M15** -- MAP-Elites v2 closeout: **card RUN_MONITORS `map-elites-hc06-v2-edm` LANDED 2026-07-02** (+ fix conteggio progress da checkpoint.jsonl per iter SPRT-evicted senza iter-json). Game PR #3183 CI verde + 0 P1 + advisory entity-grounding = falsi positivi tooling: resta solo ready+merge = atto Eduardo (`gh pr ready 3183` poi `gh pr merge 3183 --squash`). Ref memory `project_map_elites_v2` + OD-012.

### Priorità bassa

- [ ] **L1** — Re-bench discriminant hard problems custom (non-Leetcode). Fuori scope Fase 6.
- [ ] **L2** — Deepseek-r1 num_predict=5000 + extract thinking migliorato. Diminishing returns.
- [ ] **L3** — Cerebras paid tier evaluation (gpt-oss-120b, qwen-3-235b). Trigger: gap quality reale.
- [ ] **L4** — Gemma 4 multimodal dogfood reale. Opportunistic.
- [ ] **L5** — Skill install policy audit periodico (cadence 3 mesi).

### Godot design-work (human + AI, NON Jules-mechanical)

- [ ] **GD1** -- TV LobbyView spectator mode (`?room=XXXX` URL boot -> REST poll `/api/lobby/list` ogni POLL_INTERVAL_SEC, render party display-only: no input, no host_token). REST-only, `Game/` list_rooms gia' esiste -> nessun endpoint nuovo. Refs (Game-Godot-v2): `scripts/ui/lobby_spectator_poll.gd` (Eval A / PR #284 / P3-gap doc), `scripts/net/web_origin_resolver.gd:82`, `scripts/phone/phone_lobby_join_view.gd` (`?room=` deep-link). **NON un task Jules** -- Jules lo auto-proponeva come "implement" (over-reach su design differito da commento, 2026-06-04 triage). Design-work umano+AI: scope insieme alla prossima sessione feature Godot.

### ADR-0017 rollout (residuo)

- [x] **U0-test** -- **SUPERSEDED 2026-06-20** (ground-truth audit): il test sbloccava ADR-0017 step 1+, ma ADR-0017 e' SUPERSEDED-by-ADR-0030 (stack DECOMMISSIONED `672728c`, OD-009 closed 2026-05-28). Il downstream e' morto -> nessun razionale live. `aider --browser` resta usabile ad-hoc ma non e' piu' un task backlog.

### Cross-repo orchestrator (Gate E CHIUSO -- X4 ratificato DEFER 2026-06-11)

- [x] **X3** Gate E empirical window 30gg post-Max (2026-05-20 -> 2026-06-19): **re-verify DONE 2026-06-10**. (a) Claim "window elapsed al 2026-06-03" ERRATO: la window scade il 06-19 (al 06-03 erano 2 settimane; al 10-06 sono 3 su 4.3). (b) Eventi REALI loggati in-window = **0**: `logs/coord-events-2026-05.md` contiene solo 2 probe del 05-14 pre-window (marcate "NOT a real event"); `coord-events-2026-06.md` inesistente; `logs/escalation-gates-2026-05.md` = template con placeholder `<fill in>` mai compilati; 0 reminder-marker in-window (solo W20 pre-window; schtask `GateELoggingReminder` attivo, last-run 06-01, next 06-14). (c) Verdetto: window NON instrumentata = L-016 materializzato nonostante design anti-L-016; conferma indipendente JOURNAL 2026-06-01 ground-truth ("Gate-E coord-pain log = 0 eventi reali... logging-gap, non zero-dolore: tutti e 4 i dolori confermati reali").
- [x] **X4** Gate E decision -- **RATIFICATO Eduardo 2026-06-11: DEFER + retire counter** (via AskUserQuestion strutturato, sessione coordinatore). Dati: 0 eventi/wk loggati su 3 settimane elapsed (<2/wk). Framing "BUILD full / MINIMAL / DEFER" superato: Component 1 gia' shipped v0.2 (`c2cb816` 05-14) -> v0.3 (`bcd0f45`) -> unify in dogfood-ui (#196); Gate E reframed 05-14 a FEEDBACK METRIC (`ESCALATION_GATES.md`: <2/wk = "continue v0.2 stable, defer v0.3 iteration"). **Raccomandazione data-driven: DEFER + retire del counter** -- (1) criterio letterale: 0 < 2/wk; (2) il counter misura logging-discipline, non pain (zero = gap, non zero-dolore); (3) re-instrument = ripetere esperimento gia' fallito (auto-instrument ucciso da SDMG 06-01 come self-licking); (4) i 4 dolori reali hanno gia' canale segnale nel fleet governor R0/R1. Alternative: re-run window instrumentata / iterate v0.3 su segnale qualitativo.
- [x] **X5** Component 1 dashboard implementation: **CHIUSO superseded 2026-06-11** (conseguenza ratifica X4 DEFER) -- la dashboard era gia' implementata e iterata PRIMA della window (v0.2 -> v0.3 -> dogfood-ui unify #196); nessun esito X4 poteva piu' triggerare una build.

---

## Dead weight / sospetti (da NON riaprire senza trigger)

- **L6** `governor/act.py` dead-import (presunto `import json as _json` inutile in `_real_create`) -> NO-OP verificato 2026-06-03: l'import sta in `_real_find_open` (act.py:129) ed e' usato (142); nessun import morto in `_real_create`. WIP transitorio auto-swept pre-merge (come il self-gate L6 stesso prevedeva). Origine: nota Ryzen-local 2026-06-02, mai pushata su origin (overlap concorrenza cross-fleet sul work-stream governor). Non riaprire.
- `docs/reference/agno-ollama-snippets.md` Pattern 2 → fixato, no-op pendente.
- `docs/reference/subagents-skills-candidates.md` → catalogo dormiente, nessun install pianificato.
- `final-research-and-snippets-2026-04-21-v3.md` (root) → source material esterno, triato.
- `docs/handoffs/` → log historiche, congelate.
- Task #13/#14 vecchi (deepseek eval + API keys setup) → chiusi de-facto.
- `FIRST_PRINCIPLES_GAME_CHECKLIST.md` → skipped (Decisione 002 in `DECISIONS_LOG.md`).
