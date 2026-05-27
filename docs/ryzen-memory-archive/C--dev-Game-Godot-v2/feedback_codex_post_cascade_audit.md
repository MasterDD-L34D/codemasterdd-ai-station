---
name: feedback-codex-post-cascade-audit
description: ALWAYS post-cascade audit codex review comments via gh api. Wave 2026-05-20 master-dd richiesto audit revealed 1 P1 + 4 P2 findings ignored across 5 merged PR. P1 = bond engine dead code in produzione (test fixtures hide bug). Reviewer subagents APPROVED non catch call-order issues across files.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7c08f071-f7f8-4cf0-a16b-fcd6aba717fa
---

Post-cascade audit codex review comments OBBLIGATORIO. Lesson catastrofica avoided wave 2026-05-20 sera P4 storytelling cascade (PR #284→#318 = 7 merged PR).

**Master-dd richiesto audit verbatim:** _"controlla il lavoro fatto fin ora prima di procedere, controlla se nei pr fatti c'erano comment di codex che abbiamo ignorato! e controlla di non aver solo abbazzato le risposte ma di aver realmente completato i compiti fin ora"_

**Triplice audit eseguito:**
1. Codex comments survey via `gh api repos/.../pulls/$pr/comments`
2. Spot-check ground-truth: claimed symbols/methods present in actual files via Read+grep
3. Full GUT regression fresh: 2603/2608 + 5 pre-existing pending

**Reality vs claims:** subagents NON abbozzato. All claimed code present. 28 nuovi GUT test reali + pass. Implementer + reviewer chain integri.

**MA 5 codex findings IGNORED (1 P1 + 4 P2):**

| PR | Sev | File | Bug | Why missed by reviewers |
|---|:--:|---|---|---|
| #318 | P1 | main.gd | Bond engine **dead code in produzione** — `_seed_tutorial_01_units` runs BEFORE `combat_lifecycle_hook` instantiation → `register_unit` lands on null hook. Test fixtures call `register_unit` manually post-setup = bug invisible to unit tests. | Reviewer subagents controllano file modificati. Call-order across DIVERSI files (main.gd vs combat_lifecycle_hook.gd) = blind spot. |
| #315 | P2 | cronaca_text_renderer.gd | `fumble` outcome routed to ATTACK_HIT_TEMPLATES (narrated as hit). Combat emits "fumble" via combat_session.gd critical-fail path. | Reviewer non controllato downstream consumers of outcome values. |
| #316 | P2 | custode_voice_engine.gd | `_status_label` matches "stun" but combat emits "stunned" past-participle (Sprint P.2 status_applies shape). Italian output leaked English. | Reviewer non cross-checked actual status_id format from RoundOrchestrator emit. |
| #316 | P2 | addons/gdtracery/tracery.gd | UniversalModifiers vendor bug: dict maps camelCase keys to camelCase method names but methods are snake_case → runtime crash if grammar uses these modifiers. | Vendor code not in scope of G2 smoke (we don't use those modifiers). Slip past adoption gate. |
| #317 | P2 | combat_lifecycle_hook.gd | `_resolve_lineage_ts` uses orchestrator counter (EndTurnAction-incremented) but Cronaca attack entries use per-event `turn`. ts mismatch ledger attacks vs lineage events. | Reviewer non cross-checked actual ts source semantics RoundOrchestrator emit. |

**Anti-pattern codified:**

1. **Reviewer subagent blind spot — cross-file call order**: spec-compliance + code-quality reviewers focused on diff scope. Production wiring (main.gd init order vs hook setup) outside diff scope → bug invisible.

2. **Test fixture hiding production bug**: GUT tests setup hook + manually register_unit. Real main.gd flow seeds units PRIMA hook init → registrazioni perse. Tests passed false-positive.

3. **Codex review NOT auto-checked post-merge**: cascade 7 PR with 5 findings — none surfaced fino a master-dd manual audit request. Codex review happens asynchronously post-merge, agent flow non-aware.

**Pattern obbligatorio future cascade:**

```bash
# Post-merge OGNI PR (or batch end-of-cascade):
for pr in $PR_LIST; do
  echo "=== PR #$pr ==="
  gh api repos/$REPO/pulls/$pr/comments \
    --jq '.[] | select(.user.login | test("codex"; "i")) | "[\(.path):\(.line)] \(.body[0:200])"'
done
```

**Filter by P severity badge** in body (P1 orange / P2 yellow) for triage priority.

**Hotfix bundle pattern viable:** 5 codex findings across 4 PRs batched in single follow-up PR (#319). Saved 4-5 separate hotfix PRs. Cleaner main history.

**Verification fix #1 P1 production-real:**
- Pre-#319 main.gd: `_seed_tutorial_01_units` line 165 → `combat_lifecycle_hook` line 193 → `register_unit` no-op
- Post-#319: `MainCombatSetup.register_tutorial_units(hook)` extracted helper called AFTER `combat_lifecycle_hook.setup(round_orchestrator)` → real registrations
- main.gd held 999 LOC (under 1000 cap via helper extract pattern, mirrors PR #251 β.1 + #258 MainSeasonal precedent)

**Skill workflow gap identified:**
- `subagent-driven-development` skill says "two-stage review: spec compliance + code quality" but NEITHER stage explicitly checks cross-file production wiring.
- Should ADD third stage: "production-flow audit" — trace call sites of new public APIs in production callers (main.gd, scene scripts).
- OR add to code-quality reviewer prompt: "verify public API consumers in production scripts (main.gd / scenes) actually call new methods in correct order vs init lifecycle."

**Cumulative wave 2026-05-20 post-#319 final:**
- 8 PR shipped (#284/#313/#314/#315/#316/#317/#318/#319)
- DF L2+L3+L4 ❌→✅ with PRODUCTION-VERIFIED bond wire
- 2608/2613 GUT pass + 5 pre-existing pending
- 30+ subagent dispatches
- 5 codex findings resolved (1 P1 catastrophic + 4 P2)

Related: [[feedback-peer-review-blocker-pattern]] [[project-p4-storytelling-cascade-2026-05-20]] [[project-pr-284-cascade-closure]]
