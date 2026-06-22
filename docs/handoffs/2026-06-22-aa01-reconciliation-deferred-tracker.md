# aa01 reconciliation -- deferred tracker + change log (2026-06-22)

> **Hub mirror.** Canonical SoT = Game repo
> `docs/planning/2026-06-22-aa01-deferred-tracker.md` (PR #2959). This copy lives in the
> codemasterdd hub for cross-repo visibility. aa01 / L'Impronta is its own reconciliation
> track, NOT part of the Game SPEC-A..Q reconstruction suite; SPEC / meta-network links
> are noted only where a deferred item genuinely touches them.
>
> **Update 2026-06-22 (chip done):** D1 phone surface + cosmetic hint chip DONE -- GGv2
> #531 MERGED (stage 1; TV cinematic = follow-up). D2 (flip `IMPRINT_BEAT_ENABLED`) is now
> the NEXT gate -- consumer exists, gated only on playtest + master-dd. All 4 Game PR
> merged (#2958 / #2970 / #2959 / #2972).

## 1. Shipped this session (Game PRs)

| PR | Content | Status |
| --- | --- | --- |
| #2958 | CAP-06 elevation refactor (`computePositionalDamage` -> `elevationDamageMultiplier` helper) + test | MERGED |
| #2970 | C2-imprint backend MVP (additive device-authority beat + `imprintBiomeWeights` producer + cosmetic hint; flag `IMPRINT_BEAT_ENABLED` OFF, band-neutral) | MERGED |
| #2959 | Docs: aa01 plan + harsh-review (10 findings) + Track A (CHANGELOG, README de-drift) + B1 verdict + C1 spec (ratified) + C2 build-spec + this tracker | merged-pending |

Per-CAP (13 branches, all preserved on `origin/aa01/cap-*`): CAP-02 DROP; CAP-03/04/06
Track A; CAP-07 SUPERSEDED (main already has the live stateful `tile_state_map`); CAP-11
-> AFFINITY (built as `imprintBiomeWeights`); CAP-12 DEFER; CAP-13/13b/14b UX
museum-reference; CAP-14/15/15b reconciled into the additive imprint beat (built).

## 2. Deferred items (the tracker)

| # | Item | What | Gated on | Track / link |
| --- | --- | --- | --- | --- |
| D1 | C2-imprint Godot surface | phone input + hint chip **DONE** (GGv2 #531 merged); TV cinematic = follow-up | TV cinematic = GGv2 follow-up | aa01 / build-spec sec.6; GGv2 #531 |
| D2 | `IMPRINT_BEAT_ENABLED` flip | turn the beat ON in prod | **D1 surface landed -> playtest + master-dd (NEXT gate)** | aa01 (Gate-5) |
| D3 | publicSessionView in-match field | additive combat-session hint field (today the hint rides coop-state) | a combat-only consumer | aa01 / build-spec STEP 3 |
| D4 | imprint auto-timer defaulting | silent auto-default of unmarked axes (host `force` exists) | master-dd design call | aa01 open-risk |
| D5 | route-vote affinity weighting | 2nd affinity consumer (master-dd picked hint + route-vote; only hint built) | `META_NETWORK_ROUTING` flip + Godot route-UI | aa01 + meta-network / GAP-C |
| D6 | axis->trait grant | make the 4 axes grant mechanical traits | master-dd + separate spec (non-band-neutral) | aa01 |
| D7 | diegetic prose + hint-string | player-facing copy + "il tuo branco tende verso X" | master-dd-authored (codex-lore HITL) | aa01 |
| D8 | CAP-07 chain-lightning propagation | `chainElectrified` multi-tile BFS over `tile_state_map` | master-dd balance (radius + per-tile damage) | terrain (M14-A legacy) |
| D9 | CAP-12 telemetry canon-home | where `vcSnapshot` + `selectedForm` cross-run telemetry lives | dedicated design-spec (home + producer + auth/PII); migration = forbidden-path + ADR | aa01 + SPEC-M (Form-Pulse/MBTI) + reconstruct-from-ledger doctrine |

**Correction recorded** (D9): the prior "PlayerRunTelemetry aligned ADR-2026-06-07 pt3"
framing is OVERSTATED -- the only ADR-2026-06-07 is `device-authority-tv-mirror-canon` (no
"pt3"; does not sanction vcSnapshot/selectedForm persistence). `selectedForm` is
non-canonical backend naming today.

## 3. SPEC A..Q mapping

aa01 / L'Impronta is a distinct track, not a SPEC-A..Q item. Genuine cross-links only:

- **D9 telemetry** -> **SPEC-M** (Onboarding Identity / Form-Pulse / MBTI) + the canon
  reconstruct-from-ledger doctrine (vcSnapshot is session-scoped, reconstructed, not
  independently persisted). The Game SPEC-M roadmap section now points to this tracker.
- **D5 route-vote weighting** -> **meta-network / GAP-C** (`META_NETWORK_ROUTING`, OFF +
  Godot-route-UI gated).

The L'Impronta imprint beat (built #2970) is a canon-neutral COSMETIC precursor, NOT the
SPEC-M biome-seed mechanic (SPEC-M proper stays DESIGN-ONLY). No deferred item blocks any
SPEC-A..Q acceptance criterion.

## 4. Where tracked

- This tracker (mirror) -- hub `docs/handoffs/`; SoT = Game `docs/planning/`.
- Game `BACKLOG.md` (aa01 reconciliation section, D1-D9 list).
- Game plan + C1 spec + C2 build-spec (sec.11 status) under `docs/planning/`.
- Memory: `project_aa01_impronta_reconciliation.md`.
