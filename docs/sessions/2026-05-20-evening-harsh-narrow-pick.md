# Session log 2026-05-20/21 evening — harsh-review + narrow-pick

> Scope: post D-sequence closure (vault PR #139/#140/#141 morning). Eduardo
> request: fusion design AA01+Archon+Compass+codemasterdd+vault unified
> governance. Brainstorm session triggered harsh-reviewer -> RETHINK-FUNDAMENTAL.
> Pivoted to narrow-pick discipline per Protocol 7 SDMG.

## Arc sessione (high level)

1. Plugin canonical re-eval ("autoresearch karpathy missing?") -> ground-truth
   audit (karpathy NON exists as Claude plugin; forrestchang/karpathy-skills
   AUDIT-ONLY LICENSE missing)
2. Eduardo request fusion design HSGF (Hub-and-Spoke Governance Fusion):
   AA01 + Archon + Compass + codemasterdd + vault + harsh-reviewer + brainstorming
3. Superpowers brainstorming skill invoked -> 9 sections drafted with
   step-by-step Eduardo approval (pattern A hub-and-spoke + hub codemasterdd
   + A2 deploy mechanism vault-symmetric + D hybrid storage + F-FULL scope +
   G+H+I cross-repo integration + Strategy A Fix-all-FIRST + G8-c hybrid
   AA01 cross-PC initially)
4. Pre-spec verification -> 6 incongruities (IN-1..IN-6) -> A+B+C investigate
   ground-truth -> G8-NEW-d Lenovo-canonical reformulation
5. **harsh-reviewer dispatch** -> verdict **RETHINK-FUNDAMENTAL**:
   - P0.1: ground-truth corruption (5 falsified premises)
   - P0.2: SDMG Protocol 7 violation in design itself
   - P0.3: effort estimate fiction (127h claimed, ~220-320h realistic)
   - P1.1-P1.4: cross-PC parity ignored drift history, heuristic-as-decider,
     silent failure modes uncatalogued, A-E pain not enumerated
6. Accept harsh verdict ("se rigetta adotto non difendo") per L-2026-05-033
7. 5-line A-E pain doc + refresh-verify both PCs ground-truth (N3+N2)
8. Re-rank pain post-verify -> critical-fixes #1-3 BEFORE narrow-pick
9. R1 critical fixes executed: Ryzen hooks deployed scp binary-safe (#2),
   Lenovo pulls (#3), codemasterdd 52-ahead parallel-session collision
   resolved (#1) via merge+PR
10. PC identity mechanism shipped (Eduardo request): vault PR #142 -> both PCs
11. Narrow-pick #5 evaluation drift: SDMG-gate manual invocation script
    (PR #194) with RED-GREEN test cycle, 2-week empirical period

## DONE / merged this session

| PR | Repo | Subject | merge SHA |
|---|---|---|---|
| #139 | vault | promote L-DRAFT-A..E to L-2026-05-034..038 | fcb5b26ef |
| #140 | vault | Anti-Pattern Catalogue #10-#13 canonical CLAUDE.md | 316bf8c32 |
| #141 | vault | remove supermemory-local extraKnownMarketplaces fix | 00ead5dac |
| #142 | vault | pc identity mechanism (SessionStart hook + CLAUDE.md) | 1b1daedde |
| #193 | codemasterdd | merge parallel-session collision resolve | a9496a5b1 |
| #194 | codemasterdd | sdmg-gate narrow-pick manual invocation | c28d550e6 |

## Infrastructure changes deployed both PCs

- `~/.claude/CLAUDE.md` global: Anti-Pattern Catalogue #10-#13 added; PC Identity
  refresh-verify Protocol 1 extension added
- `~/.claude/settings.json` hooks.SessionStart: PC identity output hook
- `~/.local/share/git-hooks/` Ryzen: commit-msg + pre-commit deployed via scp
  binary-safe (Lenovo parity established)
- `~/.codemasterdd/` Ryzen + Lenovo: nothing (HSGF rejected; no canonical/
  paths created)
- `scripts/sdmg/sdmg-gate.sh` + `tests/sdmg/sdmg-gate-test.sh`: narrow-pick
  spoke shipped codemasterdd, manual invocation, 11/11 smoke RED-GREEN

## Anti-patterns observed real-time

- **L-2026-05-066** parallel-session-coordination-drift: 52 ahead Ryzen vs 13
  behind origin/main same files; resolved via merge-PR #193
- **Anti-Pattern #12** encoding-policy: PowerShell-pipe to bash redirect mojibake;
  workaround scp binary-safe
- **Anti-Pattern #13** SSH-cmd cross-shell: `head` not in cmd default shell;
  workaround PowerShell-native Select-Object
- **Anti-Pattern #8** SDMG self-designed-method: HSGF design auto-violated Protocol 7;
  harsh-reviewer external falsification caught pre-commit
- **L-2026-05-033** ground-truth-not-PR (variant): design authored Ryzen-side
  about Lenovo-authoritative AA01 without SSH-verify; harsh P0.1 caught

## Lessons reinforced (NOT new, recurrence evidence)

- Brainstorming HARD-GATE saved waste (no spec doc written despite 9 sections approved)
- TDD-guard hook enforced test-first on Edit attempts (RED-GREEN validated)
- Commit-msg hook fired empirical on 81-char subject + uppercase first letter
- harsh-reviewer Protocol 5 actual value demonstrated (~$0.40 spent, ~127h saved)

## NOT done this session (deferred)

- **HSGF F-FULL design spec doc**: rejected RETHINK-FUNDAMENTAL, not written
- **Hub canonical scope** (catalog/agents/evaluation-gates/methodology/etc): NOT
  created, narrow-spoke instead
- **deploy_codemasterdd_canonical.ps1**: NOT created (HSGF infrastructure rejected)
- **AA01 cross-store namespace registry G1**: NOT created (premature, no narrow-pick yet
  requires it)
- **6-spoke fusion**: NOT integrated (narrow-pick first, hub-shape re-evaluated post-2-weeks)

## Eduardo next-session queue

1. **First real SDMG invocation** on next architectural/method/install decision:
   ```bash
   bash scripts/sdmg/sdmg-gate.sh <decision-id> <class>
   ```
   class = install | method | architectural | tool-adopt | abandon | other
   Starts 2-week empirical test period from first invocation.

2. **Quarterly review trigger** ~Aug 2026 (~3 months from ship):
   - Adoption rate on qualifying decisions (target >=70%, <30% = ADR-0026 amendment B/C)
   - ADOPT-rate without-executed-experiment (target 0)
   - Real-world friction observed
   - Decide: keep SDMG-gate as-is | extend scope | retire

3. **Cleanup optional (low priority, ~1 week stable)**:
   - codemasterdd branch `backup/ryzen-pre-merge-2026-05-20` (delete after PR #193 stable)
   - Ryzen WIP backup dir `C:/Users/VGit/AppData/Local/Temp/codemasterdd-ryzen-wip-2026-05-20/`
   - vault: 11 untracked worktree dirs + 5 lint-reports (manual review Eduardo)

4. **Hub-shape re-evaluation** post-2-week empirical:
   - If SDMG-gate works narrow -> maybe extend pattern to other pains
   - If too friction -> retire or adjust
   - If gold-plating -> narrow further
   - NEVER auto-extend to HSGF F-FULL without new evidence base

## Cross-PC state snapshot end-of-session

| Dimension | Ryzen (DESKTOP-T77TMKT VGit) | Lenovo (CODEMASTERDD edusc) |
|---|---|---|
| codemasterdd | main...origin/main synced | main...origin/main synced |
| vault | main...origin/main synced | main...origin/main synced |
| AA01 lessons | 36 (L-064..L-068 most recent) | 34 (L-031..L-035 most recent) -- divergent content cross-PC |
| ~/.claude/hooks/ | commit-guard.js | commit-guard.js |
| ~/.local/share/git-hooks/ | commit-msg + pre-commit (NEW today) | commit-msg + pre-commit |
| SessionStart PC identity hook | deployed | deployed |
| CLAUDE.md PC Identity section | propagated | propagated |
| supermemory-local plugin | INSTALLED (Ryzen-only by-design) | NOT installed (canonical removed PR #141, manual install action) |

## References

- L-2026-05-033 self-designed-method-external-falsification (foundational for harsh-reviewer trigger)
- L-2026-05-066 parallel-session-coordination-drift (hit empirically Fix #1)
- L-2026-05-036 encoding-policy-enforcement (hit empirically scp workaround)
- L-2026-05-037 ssh-cmd-cross-shell (hit empirically PowerShell-native workaround)
- ADR-0026 Protocol 5 harsh-reviewer + Protocol 6 brainstorming + Protocol 7 SDMG
- ADR-0011 commit attribution policy (commit-msg hook enforcement)
- ADR-0021 multi-client encoding-policy (Anti-Pattern #12 origin)
