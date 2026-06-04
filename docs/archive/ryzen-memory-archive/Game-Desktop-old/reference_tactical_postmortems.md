---
name: Tactical Postmortems — AI War + Fallout Tactics
description: Pattern extraction from 2 seminal postmortems — 10 actionable patterns for Evo-Tactics AI Sistema, co-op balance, level design, and scope discipline
type: reference
originSessionId: ad853972-71c9-44d5-8ef0-7f655955b921
---
# Tactical Postmortems Deep Dive (2026-04-17)

Maps to: Pilastro 1 (Tattica leggibile), Pilastro 5 (Co-op vs Sistema), Pilastro 6 (Fairness), GDD gap "Level Design".

## A. AI War: Fleet Command (Chris Park / Arcen, 4-year postmortem + Designing Emergent AI series)

Co-op RTS vs asymmetric AI. 1.3M$ gross over 5yr on ongoing-support model. Direct analog for Evo-Tactics "Co-op vs Sistema".

### Top 5 patterns

1. **Decentralized Intelligence (per-unit AI, flocking-style)** — MEDIUM effort, HIGH value
   Park's core thesis: abandon centralized decision trees. Each unit runs lightweight logic ("do what's best for me, accounting for group"). Emergent sub-commander behavior (splitting into strike groups, multi-target attacks) was NEVER explicitly coded — it fell out of local rules.
   Apply: `apps/backend/services/declareSistemaIntents.js` already picks per-unit intents. Push further: each SIS unit scores targets independently via `services/ai/utilityBrain.js` considerations, then a cheap post-pass resolves conflicts (two units targeting same PG → lower-score one re-picks). No global plan needed. Drop `ai_intent_scores.yaml` "team coordination" column if present; let it emerge.
   **Verdict: ADAPT**. Evo-Tactics already partly there via utility AI; formalize "no global planner" as invariant.

2. **Asymmetric AI rules (don't mimic humans)** — LOW effort, HIGH value
   AI War's AI ignores fog-of-war, has reinforcement budgets players never see, never builds economy. Park: AIs that try to play by player rules "fall apart in advanced play". Make AI good at computer strengths (bookkeeping, parallel decisions), avoid its weaknesses (spatial reasoning, long-term planning).
   Apply: SIS should have its own resource model. `packs/evo_tactics_pack/data/balance/ai_profiles.yaml` — add `sistema_resource_model` that's separate from player PT pool. SIS gets "intent budget" per round based on pressure/difficulty, not trait costs. Document as design invariant in `docs/hubs/combat.md`.
   **Verdict: ADOPT**. Cheap, clarifies a fuzzy boundary, prevents future "make SIS fair" refactor that kills feel.

3. **AI Progress — single escalation meter controlling pressure** — LOW effort, HIGH value
   One visible integer rises as players achieve objectives. Higher value = bigger reinforcements, nastier attack waves, unlocked unit types. Players have agency: Data Centers + Superterminals lower it. Entire difficulty curve derives from one dial.
   Apply: introduce `sistema_pressure` integer on session state (0..100). Rises on PG victories, trait unlocks, biome clears. Gates SIS intent pool size + unlocks new intent types. Expose to player via Mission Console telemetry. Replaces ad-hoc per-encounter CR tuning.
   Files: `apps/backend/services/sessionHelpers.js` (state field), `apps/backend/services/roundOrchestrator.js` (read dial when sizing SIS intents), new `packs/evo_tactics_pack/data/balance/sistema_pressure.yaml` (thresholds → reinforcement tables).
   **Verdict: ADOPT**. Highest-ROI item in this file. Solves Pilastro 6 Fairness + makes co-op vs Sistema legible to players.

4. **Stateless tactical decisions (chess grandmaster exhibition model)** — MEDIUM effort, MEDIUM value
   Park inspired by grandmasters playing 40 boards at once: no memory of prior moves, evaluate current position. AI War SIS decisions per-round use only current board state. Benefits: deterministic replay, cheap serialization, no "AI confusion" bugs from stale state.
   Apply: audit `utilityBrain.js` + `declareSistemaIntents.js` for hidden state (last-turn memory, grudge lists, cooldowns that persist across saves). If found, either move to explicit session state or eliminate. Add invariant test: "SIS intent output is pure function of current session state" in `tests/ai/`.
   **Verdict: ADAPT**. Worth doing as hardening pass, not urgent refactor.

5. **Ongoing-support content model (expansions > sequels)** — N/A effort (business), HIGH value (roadmap)
   AI War earned steady revenue 4+ years via 6 DLC expansions, not sequel. Expansion cost << base game cost; each expansion re-sells base game. Community stays in one ecosystem.
   Apply: for Evo-Tactics business model (one of 7 blocked Open Questions). Default stance = "expansion packs of trait families + biomes + species", NOT "Evo-Tactics 2". Pack schema (`pack_manifest.yaml`, already scaffolded per Tier 0 Deep Dive item B4) is the enabler.
   **Verdict: ADOPT** as roadmap stance. Resolves 1 of 7 Business Open Questions.

### Priority matrix

| Pattern | Effort | Value | Verdict |
|---|---|---|---|
| Decentralized unit AI | Medium | High | ADAPT |
| Asymmetric AI rules | Low | High | ADOPT |
| AI Progress meter | Low | High | ADOPT |
| Stateless SIS decisions | Medium | Medium | ADAPT |
| Ongoing-support model | N/A | High | ADOPT (roadmap) |

---

## B. Fallout Tactics (Micro Forte / Tony Oakden, 2001 Gamasutra postmortem)

Turn-based squad, d20-adjacent (SPECIAL), 3 combat modes (CTB/ITB/STB). Shipped 4mo late after last-minute pivot from RPG to tactics. Direct analog for Pilastro 1 + level design gap.

### Top 5 patterns

1. **Single combat mode, not three** — LOW effort, HIGH value (prevention)
   Fallout Tactics shipped CTB + ITB + STB. All three modes were half-balanced; none was canonical. Reviewers + players split. Postmortem acknowledges confusion.
   Apply: Evo-Tactics already chose round model (ADR-2026-04-16). RESIST future pressure to add "quick mode" or "real-time variant". Codify in `docs/hubs/combat.md`: "Round model is the only combat model. Any alt mode is a breaking change, not a feature flag."
   **Verdict: ADOPT as invariant**. Costs nothing now, saves months later.

2. **In-house tool investment pays off** — already paying off
   Micro Forte's biggest "what went right" was early investment in level editor + mission scripting tools. Enabled 21 core missions + 30 unique encounters + hundreds of random variants.
   Apply: Evo-Tactics equivalents = `tools/py/game_cli.py`, `tools/automation/evo_batch_runner`, `apps/trait-editor/`, mock generator. Keep investing. Specific gap: **encounter editor**. `encounter.schema.json` exists (SoT deep dive) but no authoring UI. Low-effort win: a CLI command `game_cli.py author-encounter --interactive` that guides through schema, writes YAML, validates.
   **Verdict: ADOPT** — build encounter authoring CLI. Unblocks level design content volume.

3. **Design spec detail level — NPCs, progression, experience curves** — MEDIUM effort, HIGH value
   Biggest "what went wrong": design doc too shallow. Level builders + programmers had to guess on NPC stats, XP curves, progression unlocks. Ad-hoc decisions by non-designers shipped.
   Apply: audit `docs/core/` for same gap. Spot-check: do we have numeric progression table (PT pool growth per level, trait slot unlocks, VC thresholds)? If gaps → close before onboarding external contributors. Matches existing "28 Open Questions" work; prioritize the numeric/systems ones over art/business.
   **Verdict: ADAPT** — merge into existing Canonical Refactor Plan.

4. **Focus group on demo build, not final** — LOW effort, HIGH value
   Micro Forte used the Christmas 2000 single-player demo for first full-system playtest. Caught critical combat issues 3mo before ship. Postmortem calls this a major save.
   Apply: schedule explicit "vertical slice playtest" milestone BEFORE feature freeze. Use Mission Console pre-built bundle + 3 canonical encounters (already in `encounter.schema.json` tests). Record sessions, run vcScoring, diff against expected MBTI/Ennea distributions. File: new `docs/playtest/VERTICAL_SLICE_PLAN.md`.
   **Verdict: ADOPT**.

5. **Scope lock before localization / asset pipeline commits** — MEDIUM effort, MEDIUM value
   Fallout Tactics had to start dialogue recording + translation months before gameplay was stable. Result: mismatched VO, wasted asset work. Producer: "we had no choice to meet deadline."
   Apply: Evo-Tactics has Italian-first docs + English code identifiers. If ever adding localized strings or VO, do NOT start until combat+progression numbers are frozen. Add to `docs/process/`: "Localization Gate = post-balance-freeze". Not urgent (no VO yet) but cheap to codify.
   **Verdict: ADOPT** as process rule.

### Priority matrix

| Pattern | Effort | Value | Verdict |
|---|---|---|---|
| Single combat mode invariant | Low | High | ADOPT (invariant) |
| Encounter authoring CLI | Medium | High | ADOPT |
| Design spec numeric detail | Medium | High | ADAPT |
| Vertical slice playtest | Low | High | ADOPT |
| Localization gate | Low | Medium | ADOPT (process) |

---

## Cross-cutting insights

- **Both postmortems converge on scope discipline**. AI War won by staying small + deep (one combat model, one business model); Fallout Tactics bled from 3 modes + scope pivot. Evo-Tactics round-model commitment + pack-based roadmap echoes AI War's winning stance.
- **Complexity should live in data, not rules**. AI War: emergent behavior from simple unit rules. Fallout Tactics: hundreds of random mission variants from one editor. Evo-Tactics analog: more YAML content (encounters, trait families, sistema_pressure tables) beats more engine branches.
- **Asymmetry is a feature**. Both games worked because co-op players and the opponent played by different rules. Resist fairness-by-symmetry; pursue fairness-by-feel + measurable outcomes (vcScoring).

## Sources

- AI War 4yr postmortem: https://arcengames.com/ai-war-first-four-years-postmortem-and-by-extension-arcen-history/
- Designing Emergent AI series: https://arcengames.com/designing-emergent-ai-part-1-an-introduction/
- AI War wiki (AI Design page): https://wiki.arcengames.com/index.php?title=AI_War:AI_Design
- Fallout Tactics postmortem: https://www.gamedeveloper.com/design/postmortem-micro-forte-s-i-fallout-tactics-i-
- Fallout Tactics postmortem mirror: https://fallout.wiki/wiki/Fallout_Tactics_Developer_Statements/Interviews/Tony_Oakden/Postmortem:_Micro_Forte's_Fallout_Tactics
