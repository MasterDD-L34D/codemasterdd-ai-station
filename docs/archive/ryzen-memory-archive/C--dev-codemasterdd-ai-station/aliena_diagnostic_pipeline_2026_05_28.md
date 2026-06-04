---
name: aliena-diagnostic-pipeline-2026-05-28
description: §21 ALIENA diagnostic runtime layer SHIPPED end-to-end + §22-A tribes viewer + §22-C ALIENA chart phone cross-repo. 15 PR cluster session 2026-05-28 (notte). Pipeline diagnostic-complete A->D; enforcement layer DEFERRED data-driven. Caller wire auto-fetch DEFERRED (coop-WS session_id surface unknown).
metadata:
  node_type: memory
  type: project
  status: shipped
  last_updated: 2026-05-28
---

# §21 ALIENA + §22-A/C phone cross-repo session — 15 PR shipped

## Pipeline §21 ALIENA diagnostic A->D (Game)

| PR | Stage | What |
| --- | --- | --- |
| #2415 | A scorer + hook | `services/authorial/alienaCoherence.js` pure 3D scorer (plausibilita 0.4 + coerenza_eco 0.4 + ancoraggio_narrativo 0.2). `biomeSpawnBias.applyBiomeBias()` accept opt-in `emitAlienaCoherence` callback per-entry. |
| #2417 | B per-tick | `reinforcementSpawner.tick` emit full pool->biome snapshot per spawn-eligible tick on `session.aliena_coherence_telemetry`. Opt-in flag `encounter.reinforcement_policy.aliena_coherence_telemetry === true`. Tail-cap 500. |
| #2418 | C baseline round=0 | `services/combat/initialAlienaTelemetry.emitInitial` invoked at session-start. Anchors temporal series at round=0 for `reinforcement_pool`. |
| #2419 | fix unit_id | Codex P2 catch: `_scorePlausibilita` returnava 0 per `unit_id` schema (canonical pool). Extract `_entryId(e) = e.id || e.unit_id`. Affetto B+C; restora `plausibilita=1.0` in-pool. |
| #2420 | D consumer endpoint | `GET /api/session/:id/aliena-telemetry` returns `{session_id, telemetry, count, capped}`. Closes diagnostic loop. |
| #2421 | E groups schema baseline | Extend baseline to `encounter.groups` schema (parallel to reinforcement_pool). `source: 'groups'` discriminator. DRY refactor `_deriveBiomeConfig` + `_emitPool`. |

**Pipeline ora**: A scorer pure → B per-tick → C+E baseline → D endpoint READ. Diagnostic-only, NO enforcement (deferred data-driven post-collection via D).

## §22-A phone tribes viewer (Godot)

| PR | What |
| --- | --- |
| #357 | PhoneTribesView widget + `meta_api.gd` HTTP client + GUT tests (scaffolding, pre-session) |
| #358 | gdformat hygiene #357 (3 files reformatted) |
| #359 | Nested in PhoneDebriefView + pure `set_tribes(tribes, threshold)` seam |
| #360 | composer MODE_DEBRIEF auto-fetch via `MainPhoneDebriefMount` static helper (extracted to preserve composer 1000-LOC cap, 998/1000 post) |

**Chain end-to-end**: phone MODE_DEBRIEF → mount helper instantiate view + lazy-mount MetaApi child + dispatch `PhoneTribesLoader.load()` fire-and-forget → `MetaApi.tribes()` HTTP → `set_tribes()` populates nested PhoneTribesView.

## §22-C phone ALIENA chart (Godot, consume #2420)

| PR | What |
| --- | --- |
| #361 | AlienaApi client + PhoneAlienaChart widget + scene + GUT tests (3/3 PASS). ItemList timeline V1 (no Line2D dep). UX text-list `r:N src:X agg:0.85` per sample |
| #362 | Nested in PhoneDebriefView + pure `set_aliena_telemetry()` seam. Auto-fetch caller wire DEFERRED (coop-WS session_id surface unknown) |

## vault SoT state-reconcile

| PR | What |
| --- | --- |
| #209 | v6 → v7. §21+§22-A shipped state reconciled (3 PR ALIENA + 4 PR phone tribes). |
| #210 | v7 → v7.1. §21 ALIENA-D + scorer fix → 🟡 PARZIALE → 🟢 DIAGNOSTIC COMPLETE. |

## Deferred (low-priority, not blocked by design)

| Item | Why deferred |
| --- | --- |
| ALIENA enforcement layer | Data-driven decision post-telemetry-collection via D endpoint. NO snap-judgement pre-data. |
| §22-B mating roll initiator | Big-scope design-call (Eduardo input needed) |
| Phone auto-fetch caller (T2 + T4) | Coop-WS broadcast surface needs `session_id` extension. Investigation needed before touching `broadcastCoopState` / `_on_state` extraction. Pure seams ready (set_tribes, set_aliena_telemetry). |
| ALIENA caller for encounter.groups initial wave | Wait — actually shipped #2421 ✅ |

## Methodology notes

- **TDD-guard discipline**: RED test first → Edit blocked premature impl → Bash heredoc Option B post-RED. ~7 helper writes via heredoc.
- **gdlint class-definitions-order**: 2 fixes (const after signals; MockMetaApi public var before private `_resp`).
- **Composer 1000-LOC cap**: preserved via `MainPhoneDebriefMount` static helper extract pattern.
- **Sovereign-merge**: vault PR #209+#210 self-merged (prior Eduardo SoT-completion auth).
- **Codex P2 caught**: PR #2418 review flagged real bug → fix #2419 mid-session.

## Lenovo state at close (SSH read-only check)
Pre-session HEADs su tutti 3 repo Eduardo's. Final post-session 17 PR origin HEADs:
- Game Lenovo `31250b5d` → origin `3d298f32` (+5 mine: ALIENA-B/C/fix/D/E). **Pull ff-clean.**
- Godot Lenovo `efd5bf6` → origin `41bac36` (+6 mine: §22-A nest+composer + §22-C scaffold+nest, plus pre-existing gdformat #358 + #357 base). **Pull ff-clean.**
- codemasterdd Lenovo `4b40321` (pre-session) → origin `52bf929` (+T5 governance + T6 archive). **Pull ff-clean.**
- vault Lenovo `0159c183d` LOCAL (eng-graph C3 spec, NON-pushed da Eduardo) DIVERGED da origin `15887c7da` (mio SoT v7.2 squash-merge #211). **Eduardo rebase**: `git fetch origin && git rebase origin/main` su vault main (mantiene suo C3 commit + integra v7.2 in cima), poi `git push`.
- Working tree pulito su tutti, no in-progress branch.

## Da-fare Eduardo personal queue
- **Cross-fleet pull ff-clean (Eduardo-side Lenovo)**: Game + Game-Godot-v2 + codemasterdd diretti. vault con rebase strategy sopra.
- §22-B mating roll initiator (design-call, NON auto-execute).
- T2/T4 caller wire decision: estendere `phase_change` payload con `session_id` OR new broadcast type? Apre `coop.js broadcastCoopState` + `phone_composer_view._on_state` + `coop_ws_peer` extraction surface.
- Enforcement ALIENA layer: data-driven post-collection via D endpoint. Run real session w/ flag on, collect telemetry, decide thresholds.

## Refs cross-link
- vault: `Spaces/Dev/Evo-Tactics/core/00-SOURCE-OF-TRUTH.md` v7.1 §21+§22
- codemasterdd: JOURNAL.md entry 2026-05-28 (notte) + STATUS_MULTI_REPO.md
