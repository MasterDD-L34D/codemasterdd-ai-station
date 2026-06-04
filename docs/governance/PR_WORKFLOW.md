# Cross-repo PR workflow (Component 2)

> Spec ref: `docs/superpowers/specs/2026-05-13-cross-repo-orchestrator-design.md` V3 Opt 1.5 REDUCED PR #87

## Scope

Pattern write-via-PR L-012 (vault sibling-peer auth) esteso a **3 git repo target**:
- `MasterDD-L34D/Game` (Vue3)
- `MasterDD-L34D/Game-Godot-v2`
- `MasterDD-L34D/evo-swarm` (Dafne)

Plus 1 sibling-peer (vault) via L-012 per-task auth pattern esistente.

ESCLUSI da Component 2:
- AA01 (NON-git, alternative channel filesystem-direct via lesson promotion + inbox workflow personale Eduardo)
- Synesthesia (dormant + privacy mixed, fuori scope fino reactivation post UniUPO esame)

## PR type taxonomy

Ogni PR cross-repo deve avere type esplicito in PR title prefix:

| Type | Conv title prefix | When to use | Example |
|------|-------------------|-------------|---------|
| policy-alignment | `chore(policy):` | codemasterdd ADR Accepted impatta repo target | ADR-0021 encoding policy propagation a Game |
| ADR-cross-ref | `docs(adr):` | nuovo ADR codemasterdd cita repo target | ADR-0024 addendum a Game CLAUDE.md |
| drift-fix | `fix(drift):` | state diverge tra codemasterdd doc/memory e repo target reality | vault llm-routing.json IP hardcoded |
| docs | `docs:` | typo / link fix / cross-reference broken | Godot-v2 README link broken |
| governance-suggestion | `chore(governance):` | pattern noto codemasterdd applicable ma not yet adopted, SOFT-suggestion only | Protocol P1 Refresh-verify proposal |

## Workflow steps

1. **Identify cross-repo issue** durante uso normale codemasterdd (NO active scanning policy-driven, opportunistic only)
2. **Run dry-run validator**: `scripts/cross-repo/dry-run-pr.ps1 -RepoTarget <name> -Type <type> -PreviewFiles <paths>`
3. **Verify privacy whitelist** PASS (script auto-checks `~/.config/aider-privacy-whitelist.txt`)
4. **Draft PR** using template `docs/governance/PR_TEMPLATE.md`
5. **Open PR** via `gh pr create` su repo target
6. **Log entry** in `logs/cross-repo-pr-YYYY-MM.md` con outcome PENDING
7. **Governance interna repo target** decide accept/reject/amend (decision time NON-controllable, days-weeks)
8. **Update log entry** con outcome finale + amend type se applicable

## Anti-pattern (avoid)

- Drafting PR senza dry-run (skip risk wrong-target)
- Auto-mode cross-repo PR drafting (richiede Eduardo authorization explicit each PR fino pattern proven >=1 acceptance)
- Bulk batching multiple PR senza tracking individual outcome
- Modifying file in target repo PRESERVED scope (es. Game-Godot-v2 governance interna CLAUDE.md territory)

## Reversibility tier (Gate D awareness)

Track cumulative PR accepted by external governance:
- **0-2 accepted**: full reversibility (~10min)
- **3-4 accepted**: graduated reversibility (~1-2h coordinated cleanup)
- **>=5 accepted**: soft lock-in confirmed → trigger Gate D → ADR formale per ritiro coordinato OR continuation explicit

Update Reversibility tier visible in `logs/cross-repo-pr-YYYY-MM.md` summary post-each accept.

## First 3 PR protocol (empirical validation)

I primi 3 PR accepted by external governance sono pattern-validating. Procedura:
1. Eduardo authorization EXPLICIT per ognuno (no auto-mode)
2. Outcome tracking dettagliato (response time + amend rate + comment count)
3. Post 3 acceptance → pattern validated → auto-mode acceptable per PR type validated

Pre-3rd-acceptance, ANY external governance reject → re-evaluate pattern (potential rescope a Component 2 declined).
