---
id: execution-board
title: EXECUTION-BOARD — control-plane azione cross-repo
type: control-plane
status: active
created: 2026-05-16
last_verified: 2026-05-16
owner: master-dd
language: it
tags: [cross-repo, execution, control-plane, orchestration, od-038]
---

# EXECUTION-BOARD — control-plane azione cross-repo

> **Scopo**: unico punto da cui master-dd vede *fatto / in-corso / prossimo*
> su tutto l'ecosistema senza ri-auditare. Orchestratore (chat-sessione)
> applica OD-038: **verifica-stato = leggi questa board** (1s), non audit
> cross-repo (lento, trap void-pick). Esecutori aggiornano la propria riga
> + linkano PR.
>
> **Confine anti-rot (principio #135)**: questa board = truth-layer
> *esecuzione* (status azionabile). NON duplica git-HEAD (rot in ~2gg su
> repo daily-ship) né la narrativa decisioni (vive nei doc OD vault). Stato
> git fresco → audit on-demand; razionale decisioni → doc OD.
>
> **Regola update**: chi esegue una riga la spunta + mette link PR + data.
> Niente HEAD/SHA hardcoded qui. Stale-check: se una riga `WIP` non si
> muove >5gg → orchestratore verifica stato reale e riconcilia.

## 1. Sequence attiva — OD-024-031 (ratificata master-dd 2026-05-16)

Lens ambizioso "FINISCI". Esecuzione = repo Game/ + Game-Godot-v2 (Quality
Gate + GUT parity + Codex P1/P2 per Envelope). Razionale completo:
vault `docs/decisions/OD-024-031-aistation-reanalysis-2026-05-14.md`.

| # | OD | Cosa | Repo | Env | Effort | Status | PR | Gate |
|--:|----|------|------|:---:|------:|:------:|----|------|
| 1 | OD-030 | Game-Database flag-ON (ratifica #2259 già merged) | Game | A | 0.5h | ✅ DONE | shipped 2026-05-14 | — |
| 3 | OD-028 | Audio: adopt Howler.js middleware (5KB MIT) | Game | A | 2h | ⬜ TODO | — | nessuno — **PROSSIMO** |
| 2 | OD-025 | Promotions: REJECT demolish (code LIVE) + Phase B2 catalog tier elite/master | Game+Godot | A+B | 3.5h | ⬜ TODO | — | engine LIVE; catalog tier mancante |
| 4 | OD-031 | Pack drift: merge core+pack-v2-full-plus + diff audit log | Game | B | 3h | 🟡 PARZIALE | — | ETL `merge_pack_v2_species.py` esiste; consolidamento da verificare |
| 5 | OD-027 | Bridge species: full Species type + ecotypes integration | Game+Godot | B | 3h | 🟡 PARZIALE | — | schema+ETL presenti; triplet species.json/catalog/loader assente. dep #4 |
| 6 | OD-024 | Sentience: full RFC T1-T6 45/45 + 4 traits interocettivi | Game+Godot | B | 3-4h | 🟡 PARZIALE | — | `incoming/sentience_traits_v1.0.yaml` presente; sentience_tier solo 3 file core (non 45/45). dep #5 |
| 7 | OD-029 | Ancestors Path B: neurons_bridge 13→~50 | Game+Godot | B | 5h | ✅ DONE | neurons_bridge.csv = 52 righe | — |
| 8 | OD-026 | Atlas: diegetic mini-map TV + Phone overlay (FDF §16) | Godot | C | 6-8h | 🔒 GATED | — | **master-dd checkpoint pre-impl** (rischio shader) |

> **Reconcile 2026-05-16** (verifica stato Game `84e8c44` vs board-seed): OD-030 + OD-029 erano **già shipped** (board seedata TODO senza verificare codice Game = trap void-pick evitata dalla board stessa). OD-024/027/031 = parziali (tooling presente, output finale assente) → re-audit puntuale a inizio esecuzione, non assumere TODO né DONE. Effort residuo reale ≈ 11-13h (non 23h: -5.5h da 030+029 done, parziali da quantificare). Prossimo exec pulito certo = **OD-028** (audio.js confermato assente).

Totale residuo ≈11-13h (rivisto post-reconcile). PR-strategy = **bundle per Envelope** (A: 025-smoke+028 → 1 PR · B: 024+025-B2+027+031 → 2-3 PR · C: 026 → 1 PR).

Legenda status: ⬜ TODO · 🟡 WIP · ✅ DONE · 🔒 GATED · ⏸ DEFERRED

## 2. Decisioni chiuse (no-action — riferimento)

| Decisione | Esito | Data | Doc |
|---|---|---|---|
| U-5 GitHub-MCP scope | MOOT (gh CLI eccede già opzione C) | 2026-05-16 | vault OD-040 |
| OD-041 gh-token scope | EXECUTED — fine-grained PAT scoped-5, blast-radius ridotto verificato | 2026-05-16 | vault OD-041 |
| OD-039 bulk-ingest method | DECIDED (M1/M2 per-source) | 2026-05-16 | vault OD-039 |
| OD-035 bestiari bio-ref | DONE — 288 card + synthesis | 2026-05-16 | vault OD-035 |
| OD-033 chatgpt recovery | RESOLVED → OD-039 | 2026-05-16 | vault OD-033 |
| Dashboard reconcile cross-repo | DONE — §1-7 decoupled git-truth, 15-repo audit ratified | 2026-05-16 | codemasterdd #130/133/134/135 |
| PR #112 visual-identity spec | MERGED (spec in codemasterdd; vault-write resta gated) | 2026-05-16 | codemasterdd #112 |

## 3. Gated / deferred (trigger-bound — NON azionabili ora)

| Item | Stato | Trigger sblocco |
|---|---|---|
| OD-026 diegetic Atlas | 🔒 in sequence #8 | master-dd checkpoint pre-implementazione (shader risk) |
| Vault-write `45-VISUAL-IDENTITY-CANONICAL.md` | 🔒 | auth esplicita per-task master-dd (L-2026-05-012) — spec PR#112 = il checkpoint |
| pack-v2 atomize-deep | ⏸ | Phase B trigger |
| U-14 diegetic Atlas vault doc | ⏸ | post-Playtest #2 + master-dd |
| vault-roadmap Fase 3 | ⏸ | trigger M2-playtest + repo public |
| OD-032 chatgpt-watcher | ⏸ dormant by design | export-event trigger |
| Synesthesia | ⏸ dormant | riattiva pre-esame UniUPO (~ago 2026) |

## 4. Protocollo orchestrazione (questa chat = control)

1. **Verifica-stato** (OD-038 step 1) = leggi §1 di questa board, non audit.
2. Prossimo = prima riga §1 `⬜ TODO` senza gate aperto (ora: **OD-028**, post-reconcile 2026-05-16).
3. Dispatch a sessione-repo (Game/Godot). Sessione esegue Quality Gate.
4. Sessione esecutrice aggiorna la sua riga (status + PR + data) nel commit.
5. Item gated/deferred (§3) → mai auto-eseguire; sblocco solo via trigger.
6. Stale-guard: riga `🟡 WIP` ferma >5gg → riconcilia stato reale.

## Cross-link
- Sequence razionale: vault `docs/decisions/OD-024-031-aistation-reanalysis-2026-05-14.md`
- Verdict-record permanente: `docs/governance/open-decisions/OD-024-031-verdict-record.md` (staging→Game/)
- Metodo: vault `docs/decisions/OD-038-operating-method-2026-05-16.md`
- Dashboard narrativa (contesto, NON azione): `STATUS_MULTI_REPO.md`
