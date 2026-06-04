---
name: Session 2026-05-10 cross-domain audit + 10/17 ticket shipped
description: 4 parallel audit (trait+morph+MBTI+Ennea) revealed 17 gap ticket cross-domain. Shipped 10 via PR #2160. 6 cumulative PR Game/ + 1 PR open #2156 sweep YAML loader. Tier L2 deferred master-dd verdict.
type: project
originSessionId: eee74a8e-ebbd-4132-9f61-1a9667d8d169
---
# Sessione 2026-05-10 cross-domain audit + 10/17 ticket shipped

## Trigger

User: "ci sono altri gap soprattutto nei trait e nelle combo per la parti e i morph o le combo mbti job ed ennea?" → 4 audit paralleli spawned + verdict 17 ticket cross-domain → user "vogli orisolverli tutti e 17!" + "confermo" + "continua" → autonomous batch ship.

## 4 audit paralleli verdict

| Domain | Agent | Findings |
|--------|-------|----------|
| Trait coverage | balance-auditor | 4 effect.kind unhandled + 31 trait_mechanics no handler + 59 orphan active_effects + 7 ae no glossary |
| Form/morph/mutation | creature-aspect-illuminator | 30 mutations no auto-trigger evaluator + circular trait_swap + bond HUD DEAD + skiv pool unwired |
| MBTI×Job combo | balance-auditor | 0/176 combo resolve (vocab mismatch) + 64/176 expansion jobs absent + no runtime wire |
| Ennea combo | balance-auditor | 9/9 voices+handlers OK ma 1+5 double-trigger + raw_metrics solo missing fallback + skiv 0/9 ennea |

Total: **17 ticket** (3 P0 + 8 P1 + 6 P2). Aggregate effort ~27-35h.

## PR #2160 ship — 10/17 ticket

8 commit cumulative su `claude/tier-s-data-fixes` branch:

### Tier S (5 + 1 rejected)

| Commit | Ticket | Priority |
|--------|--------|:---:|
| `5226674d` | TKT-MUT-CIRCULAR-SWAP — `simbionte_batteri_termofili` empty trait_swap | P1 |
| `5226674d` | TKT-TRAIT-AE-GLOSSARY-MISS — 7 entries (597→604) | P2 |
| `5226674d` | TKT-FORMPACK-EXP-JOB-BIAS — 5 jobs added (ranger + 4 expansion) | P2 |
| `5226674d`+`dfc056c8` | TKT-ENNEA-1-5-DOUBLE-TRIGGER — dedup applyEnneaBuffs + applyEnneaToStatus canonical | P1 |
| `b5fbd2cf` | **TKT-MBTI-JOB-VOCAB** — vocab remap canonical job IDs (0/176 → resolve) | **P0** |
| `b5fbd2cf` | **TKT-MBTI-EXP-JOBS** — 4 expansion jobs additive | **P0** |
| _rejected_ | TKT-VCSCORING-ITER2-DEFAULT — comment 849-851 documenta REVERT 2026-04-27 | P2 |

### Tier M (3)

| Commit | Ticket | Priority |
|--------|--------|:---:|
| `a6a60041` | TKT-TRAIT-EFFECT-KIND-MISS — `persistent_marker` + `triggers_on_ally_attack` recognition | P1 |
| `435db6ba` | TKT-ENNEA-METRICS-FALLBACK — zero-default per assists/low_hp_time in solo | P1 |
| `82061bc3` | TKT-SKIV-ENNEA-ARCHETYPE — `ennea_archetype_bias` per 8 biome | P2 |

### Tier L1 (2)

| Commit | Ticket | Priority |
|--------|--------|:---:|
| `a93a3e5b` | TKT-MBTI-AFFINITY-RUNTIME — wire job_affinities runtime (formStatApplier.applyJobAffinityBonus) | P1 |
| `4a571d45` | TKT-SKIV-COMPANION-SERVICE — companionPicker emit ennea_archetype field | P1 |

## Tier L2 deferred (4 — master-dd verdict gated)

| Ticket | Priority | Effort | Gate |
|--------|:---:|:---:|------|
| **TKT-MUT-AUTO-TRIGGER** | **P0** | 5-8h | ADR mutation engine new evaluator service |
| TKT-BOND-HUD-SURFACE | P1 | 3h | Frontend coord pure work |
| TKT-TRAIT-MECH-NO-HANDLER | P1 | 5-8h | Design call per 31 trait |
| TKT-TRAIT-ORPHAN-ACTIVE | P2 | design | Accept/reject 59 entries |

## Cumulative Day 5+1 (2026-05-09 sera + 2026-05-10)

PR shipped main 2026-05-10:
- #2155 `48eaf24a` nightly cron P0
- #2152 `5466cf45` Skiv Monitor
- #2159 `7dd18ad0` BASELINE_WR.cautious 0.85→0.95 empirical

PR open:
- #2156 sweep YAML loader (DRAFT→ready-review, master-dd verdict)
- #2157 registry sync + 17-ticket gap inventory
- #2160 **Tier S+M+L1 — 10 ticket gap fixes** (8 commit, +3300/-3035 LOC)

**Cumulative Day 5+1 = 16 PR Game/ shipped main** (#2140-#2151 + #2153 + #2155 + #2152 + #2159) + 3 PR open.

## Cron 02:00 UTC NON fired

Watcher btwtu0q56 polling `gh run list --event schedule`. Result: zero scheduled events da 02:18 UTC ad oggi (~30min past schedule). GitHub Actions scheduler skip — known issue. Manual workflow_dispatch tests verde con BASELINE_WR.cautious=0.95 update.

## Lessons

1. **yaml.dump drops comments** — js-yaml dump produces canonical YAML losing inline comments. Use regex-targeted text edit per preserve structure (mbti_forms vocab remap iter1 abandoned, iter2 OK).
2. **replace_all caveat** — replace_all="tattico" caught description text ("Creativo tattico") → use regex anchored to `job_affinities:[...]` lists only.
3. **canonical runtime path matter** — Ennea audit fix iter1 only patched `applyEnneaBuffs` (legacy path) ma `applyEnneaToStatus` (sessionRoundBridge canonical) needed iter2 patch. Always grep canonical caller pre-fix.
4. **audit ticket scope can mismatch** — TKT-VCSCORING-ITER2-DEFAULT flagged "1h flag flip" ma comment doc 849-851 documenta revert 2026-04-27 per real bug. Real fix ~2-3h. Reject + flag actual scope.
5. **GH scheduler unreliable** — cron 02:00 UTC daily can skip. Workflow_dispatch fallback canonical pattern.

## Resume trigger

> _"merge PR #2156 sweep + #2157 registry + #2160 audit fixes (master-dd verdict cascade), poi Tier L2 4 ticket: TKT-MUT-AUTO-TRIGGER ADR draft + TKT-BOND-HUD-SURFACE frontend + TKT-TRAIT-MECH-NO-HANDLER design call 31 trait + TKT-TRAIT-ORPHAN-ACTIVE accept/reject 59 entries"_
