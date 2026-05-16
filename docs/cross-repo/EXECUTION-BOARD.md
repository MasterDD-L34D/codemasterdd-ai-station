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
| 1 | OD-030 | Game-Database flag-ON | Game | A | — | ✅ SHIPPED | Envelope A **PR #2261** | — |
| 2 | OD-025 | Promotions REJECT demolish + B2 catalog elite/master | Game | A+B | — | ✅ SHIPPED | A: PR #2261 · B2: envelope-b 2026-05-14 (`promotions.yaml` v0.2.0) | — |
| 3 | OD-028 | Audio Howler.js middleware | Game | A | — | ✅ SHIPPED | Envelope A PR #2261 (`apps/play/src/audio.js`) | — |
| 4 | OD-031 | Pack v2-full-plus merge → species_catalog.json | Game | B | — | ✅ SHIPPED | envelope-b 2026-05-14 (15 species consolidated) | — |
| 5 | OD-027 | Full Species type + ecotypes | Game | B | — | ✅ SHIPPED | envelope-b (`species_catalog.json` v0.2.0) | — |
| 6 | OD-024 | Sentience full + 4 traits interocettivi | Game | B | — | ✅ SHIPPED | envelope-b (15/15 `sentience_index` T0-T3 + active_effects.yaml) | — |
| 7 | OD-029 | Ancestors neurons_bridge 13→51 | Game | B | — | ✅ SHIPPED | envelope-b (`neurons_bridge.csv` 51 entries v0.2) | — |
| 8 | OD-026 | Atlas diegetic mini-map TV + Phone overlay | Godot | C | — | ✅ SHIPPED | Godot `afaa656`: diegetic_atlas.gd 270r + phone_atlas_overlay.gd 200r + atlas_pulse_adapter.gd + tscn TV/Phone, wired main.gd:240, 5 GUT test. doc `scaffold-shipped`. Design call risolto 2026-05-14 = Skiv-reuse, NO shader, ColorRect tint (asset commission evitata) | — (opt: arte biomi Wildermyth = enhancement non-blocker, defer post-playtest#2) |
| 9 | Godot v2 cross-stack mirror | species_catalog.gd + neurons_bridge_catalog.gd + promotion_engine.gd elite/master | Godot | B | — | ✅ SHIPPED | Godot `afaa656`: species_catalog.gd (151r, facade+wired 6 callers) · neurons_bridge_catalog.gd (137r) · promotion_engine.gd (419r, OD-025-B2 elite/master 2026-05-14). `species_loader.gd` = redundant non-creato (YAGNI: catalog Resource È la facade, 0 consumer per loader separato) | — |

> **🔴 Reconcile DEFINITIVO 2026-05-16** (truth-layer trovato: Game `docs/governance/open-decisions/OD-024-031-envelope-b-summary.md` `status: shipped` + `OD-024-031-verdict-record.md` + Envelope A **PR #2261**):
>
> **7/8 OD GIÀ SHIPPED 2026-05-14** (stesso giorno della reanalisi — sequence eseguita in blocco da sessioni-Game subito dopo approvazione). Envelope A (OD-030+025-smoke+028) = PR #2261. Envelope B (OD-031/027/024/029/025-B2) = shipped 2026-05-14.
>
> **Fallimento metodo board (onesto)**: la prima board-seed era TODO **speculativo non verificato**; il reconcile intermedio usò un path-check errato (`apps/play/public/` invece di `src/`). Il truth-layer autoritativo (`envelope-b-summary status:shipped`, PR #2261) **esisteva già in Game** e doveva essere la fonte di seed. Board pre-reconcile = ~88% errata (7/8 mis-stati). **Lezione OD-038**: seed control-plane SEMPRE dal truth-layer esecuzione esistente (execution-summary nei repo), MAI da inferenza/ratifica-doc. Aggiunta §regola 0 protocollo.
>
> **Stato reale (3° reconcile 2026-05-16, regola-0 applicata)**: anche #9 Godot mirror era **già shipped** (verifica Godot `afaa656`: 3/3 file presenti+wired; species_loader.gd redundant non-creato by-design). **Sequence OD-024-031 INTERAMENTE COMPLETA** (Game+Godot). Unico residuo = **OD-026 deferred-gated** (master-dd design call). Effort exec aperto = **0h**. Regola-0 ha intercettato 3 board-row speculative consecutive (030/029/028 → 7/8 → #9): seed-da-truth-layer ora obbligatorio.

> **4° reconcile 2026-05-16 (regola-0, 5ª intercettazione)**: anche OD-026 era **già shipped 2026-05-14** (diegetic_atlas+phone+adapter wired main.gd:240, 5 GUT test, doc scaffold-shipped). Il "design call necessario" non esisteva come gate: fu già deciso (Skiv-pulse reuse, NO shader custom, ColorRect biome-tint, asset-commission evitata). Unico residuo = arte biomi Wildermyth-style = **enhancement opzionale non-blocker**, defer post-playtest#2.

**Sequence OD-024-031 = 8/8 COMPLETA end-to-end (Game+Godot). Exec aperto = 0h. Zero gate residui.** L'intera sequence "23h ratificata" era già fatta il giorno stesso della ratifica (2026-05-14). Board ora 100% agganciata a truth-layer verificato.

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
| ~~skiv-monitor redesign (OD-042-A)~~ | ✅ SHIPPED | Game **PR #2281 merged** (workflow orphan-push `skiv-monitor/state` + backend fetch-branch + ADR amend). #2257 CLOSED, branch `auto/skiv-monitor-update` deleted, Game 0 PR. Block + bloat 8MB/4h risolti insieme. OD-041 PAT aveva Workflows-perm (verificato empirico, spec era errata). Runbook 2c = moot |
| Arte biomi Wildermyth-style (OD-026 polish) | ⏸ enhancement opzionale | post-playtest#2 — non-blocker (ColorRect tint funzionale già shipped) |
| ~~Vault-write `45-VISUAL-IDENTITY-CANONICAL.md`~~ | ✅ DONE | 45 creato+raffinato (vault PR #43); follow-up 2b (42/43 Ferrospora) catturato; conflitto proiezione RISOLTO ortogonale (vault PR #44, master-dd 2026-05-16). Visual-identity = chiuso |
| pack-v2 atomize-deep | ⏸ | Phase B trigger |
| U-14 diegetic Atlas vault doc | ⏸ | post-Playtest #2 + master-dd |
| vault-roadmap Fase 3 | ⏸ | trigger M2-playtest + repo public |
| OD-032 chatgpt-watcher | ⏸ dormant by design | export-event trigger |
| Synesthesia | ⏸ dormant | riattiva pre-esame UniUPO (~ago 2026) |

## 4. Protocollo orchestrazione (questa chat = control)

0. **Seed da truth-layer (regola anti-illusione)**: una riga board nasce/aggiorna SOLO da execution-summary verificato nel repo target (es. Game `docs/governance/open-decisions/*-envelope-*-summary.md`, PR merged), MAI da doc-ratifica/inferenza. Doc decisione = razionale; execution-summary repo = verità stato. Violata 2026-05-16 (board seedata speculativa, 7/8 errati) → questa regola.
1. **Verifica-stato** (OD-038 step 1) = leggi §1 di questa board, non audit.
2. Prossimo = prima riga §1 `⬜ TODO` senza gate aperto (ora: **NESSUNO** — sequence OD-024-031 = 8/8 completa, zero gate residui. Prossimo lavoro = nuovo trigger esterno: playtest#2, nuova decisione, o item §3).
3. Dispatch a sessione-repo (Game/Godot). Sessione esegue Quality Gate.
4. Sessione esecutrice aggiorna la sua riga (status + PR + data) nel commit.
5. Item gated/deferred (§3) → mai auto-eseguire; sblocco solo via trigger.
6. Stale-guard: riga `🟡 WIP` ferma >5gg → riconcilia stato reale.

## Cross-link
- Sequence razionale: vault `docs/decisions/OD-024-031-aistation-reanalysis-2026-05-14.md`
- Verdict-record permanente: `docs/governance/open-decisions/OD-024-031-verdict-record.md` (staging→Game/)
- Metodo: vault `docs/decisions/OD-038-operating-method-2026-05-16.md`
- Dashboard narrativa (contesto, NON azione): `STATUS_MULTI_REPO.md`
