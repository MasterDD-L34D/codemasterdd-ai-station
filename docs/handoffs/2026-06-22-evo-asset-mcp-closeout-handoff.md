---
title: Handoff -- evo-asset-mcp close-out (review + live gate + finish + C2PA + merge)
date: 2026-06-22
doc_status: active
workstream: cross-cutting (evo-content-mcp host + Game-Godot-v2 + codemasterdd hub)
last_verified: 2026-06-22
source_of_truth: false
language: it
---

# Handoff -- evo-asset-mcp close-out -- 2026-06-22

Continua da `2026-06-21-content-gen-asset-pipeline-handoff.md` (spike opt-2 SEAM validato).

## TL;DR

- **evo-asset-mcp MERGED to main** (host `C:/dev/tools/evo-content-mcp`, local-only, ff `44b5e47 -> 91b704d`). 7 tool MCP, **123 test + 1 skip opt-in**, 0 rossi.
- Pipeline agent-callable completa + **validata dal vivo** (Ryzen .11 <- Lenovo .10): generate -> finish (alpha-cut) -> validate -> promote+sign -> provenance verify.
- Code-review convergente (mia 4-dim + handoff creature-lore 20-bug): **4 RED + 13/16 YELLOW** chiusi + gate **ADR-0041** (local-SD solo ornate; flat/functional rifiutati).
- **C2PA embedded WIRED + verificato** (c2pa-python 0.35.1, opt-in) + sidecar (sha256) offline-default.
- Residuo -> **5 chip** spawnati (sotto). Niente merge bloccante.

## Cosa e' shippato (commit)

Host `evo-content-mcp` (branch `feat/evo-asset-mcp` -> main `91b704d`):

| Commit | Scope |
| --- | --- |
| 035be8d | P1 registry glob (famiglia!=filename) + gate ADR-0041 |
| 4d18ce4 | R1 base64 runner (anti prompt-injection) + C2PA_EMBED default off |
| 98f3888 | YELLOW: validate open-failure / registry per-item status / recraft try-except / promote phantom-claim |
| bf376e4 + 77bb507 | seam path reali (C:/AI/ferrospora-spike) + retry-until-up + remote-scratch mkdir |
| c49e823 | asset_finish (alpha-cut, wrap cut_flat_bg.py) -- loop chiude |
| fa6cbe0 | C2PA embedded provenance (verificato) + sidecar fallback |
| 700a51c / 0fce45d / 91b704d / 23e8605 / f1a0333 | QUALITY.md gate records |

(sopra i 3 creature-lore: baf9abd R2 sanitize, 19eb9fc R3 sha256, 8faf902 findings doc)

Altri repo:
- Game-Godot-v2 `8fa8c5f` (branch docs/evo-content-mcp-creature-lore-spec): manifest `local_sd_eligible` + reconcile spec/plan con ADR-0041.
- codemasterdd hub: PR [#406](https://github.com/MasterDD-L34D/codemasterdd-ai-station/pull/406) (GOALS narrowing, OPEN) + `437a304` su questo branch (spike-record 2026-06-21).

## Blockers / residual -> tutti in chip

- [ ] **task_05ae4a09** cut-quality: raw SDXL bg non flat -> transparent_frac ~0.05; tuning prompt/cut o cut_alpha (rembg). Copre anche tuning Task-16.
- [ ] **task_407e81a0** provisioning cert C2PA reale (CA->leaf chain + TSA) per embed runtime (oggi opt-in, test usa cert effimero).
- [ ] **task_a8c61b57** creature-domain LoRA (v1 e' UI-frame-domain -> creature = style-bleed); reconcile con 3D->pixel roster (ADR-2026-06-03).
- [ ] **task_b1822781** 3 YELLOW deferiti (#2 parse robustness, #6 downgrade signal, #9 promote test realism).
- [ ] **task_c1b07fd6** continua-sessione (stessi modi: caveman full + ultracode).
- [ ] PR #406 (GOALS narrowing) da mergiare a main hub (Eduardo).

## Next entry point

1. **First action**: avvia il chip che serve (cut-quality = piu' alto valore: sblocca asset usabili). O `task_c1b07fd6` per riprendere il workstream a tutto tondo.
2. **Reference**: questo handoff + `evo-content-mcp/QUALITY.md` (gate status) + `docs/asset-review-findings-2026-06-22.md` (host) + ADR-2026-06-03 (vault, roster=3D->pixel).
3. **Live-gate gotcha**: `asset_generate` promote CLOBBERA l'asset shipped -> `git restore` Game-Godot-v2 dopo i test-gen. Identity check pre cross-PC.

## Memory (gia' aggiornata, no save pendente)

- `evo-asset-mcp-build-state` -- stato completo (merge, 123 test, C2PA embedded, gotchas cert/TSA, residui).
- `ferrospora-asset-gen-seam-validated` -- seam opt-2.
- `check-existing-specs-before-designing-infra` -- il near-miss (spec+impl gia' esistevano; 2 sessioni stesso working tree).
