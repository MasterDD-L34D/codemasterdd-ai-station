# Sprint 2026-04-27 sera — Bundle B + Recovery + Spore Moderate FULL

**Sessione cumulative**: 18 PR merged main (continuazione da step 1-7 prior session).

## PR shipped this run

| # | Scope | Pillar |
|---|---|:-:|
| #1908 | Step 3 AI meter frontend wire | P5 |
| #1909 | Step 7 ticket auto-gen runtime | infra |
| #1911 | Step 4 lineage tab placeholder rimosso | P3 |
| #1912 | Step 6 backbone deploy roadmap doc | P5 |
| #1913 | Spore S1 schema (body_slot/derived_ability_id/mp_cost) | P2 |
| #1915 | Spore S2+S3+S6 runtime engine | P2 |
| #1916 | Spore S3+S6 MP pool + hydration | P2 |
| #1917 | QW-1 mp_grants toast | P2 UX |
| #1918 | Sprint B propagateLineage | P2 |
| #1919 | Sprint C backbone Render+CF deploy bundle | P5 |
| #1920 | Sprint A archetype DR/init/sight resolver | P1 |
| #1922 | QW-2 MP badge + QW-3 Mutations tab | P2 UX |
| #1924 | Sprint Y S5 lifecycle hooks | P2 |
| #1926 | RANKED report 312 LOC (recovery) | meta |
| #1927 | 5 indie research docs ~1370 LOC (recovery) | meta |
| #1929 | Indie classification immediate-use vs museum | meta |
| #1930 | 12 museum cards Dublin-Core M-019→M-031 | meta |
| #1932 | Bundle B small (drift + counter HUD) | P1+P4 |
| #1933 | Bundle B big (TBW Undo + Tunic Codex) | P1+cross |

## Spore Moderate FULL stack chiuso (P2 🟡++ → 🟢 def)

End-to-end loop runtime:
1. encounter combat → KO enemy con applied_mutations[] → propagateLineage automatico (lineage pool species+biome)
2. survivor → mp_grants toast viola "+N MP" (Gate 5 Engine wired)
3. characterPanel mostra MP X/30 + chip archetype attivo
4. nestHub Mutations tab → eligible list filtered by slot+MP → apply
5. bingo 3-of-a-kind category → archetype emerge → resolver applica DR-1/init+2/sight+2
6. next encounter STESSO biome → newborn inheritFromLineage (1-2 mutation gratis dal pool)

## Recovery 6 deliverables persi

Audit forensic confermato: `git checkout origin/main` cleanup ha rimosso untracked file mai-committed.

- 5 `2026-04-27-indie-*.md` (~1370 LOC) → rigenerati via narrative-design-illuminator
- 1 `2026-04-26-session-deliverables-RANKED.md` (312 LOC) → rigenerato via general-purpose

**Verification gaps**: 11 game-specific design pattern detail tagged `verification_needed: true` (GDC postmortems richiedono verifica primaria).

## Bundle B Indie Quick-Wins (4 patterns ~16h)

- **B.1 Citizen Sleeper drift briefing** (~3h, P4): `narrativeRoutes.js` POST `/api/v1/narrative/briefing/drift` con condizionale `vcSnapshot.mbti_axes.T_F` (3 varianti per scenario). 9 ink stitches seed (3 scenari × 3 varianti).
- **B.4 Wildfrost counter HUD** (~4h, P1): `render.js drawCounterBadge` canvas-only, max 3 badge per unit + overflow indicator "+1". Priority order: ability_cooldowns > status duration.
- **B.2 TBW Undo libero** (~4h, P1): `POST /api/session/undo-action` LIFO pop main intent (planning-phase only, 409 se phase != planning). Frontend btn `↶ Undo` + Ctrl+Z keybind.
- **B.3 Tunic decipher Codex pages** (~5h, cross): `apps/backend/services/codex/codexState.js` (in-mem) + 5 seed pages YAML + 4 trigger types (always|enter_biome|kill_species|apply_trait|mating_attempt). CSS blur(3px) + decipher hint.

## Conflict resolution (cross-PC race)

PR #1933 vs main #1931 collision: `apps/backend/routes/codex.js` add/add. Solution: **merged 2 endpoint set** in unified createCodexRouter — campaign-scope (glyph progression) + session-scope (decipher pages) coesistono. Fix double `createCodexRouter` import + double `app.use` in app.js.

## Lessons codified

1. **Untracked = ephemeral**: file `??` non sopravvivono `git checkout`. `git add` immediato anche WIP.
2. **Background agent + branch ops = collision risk**: 2x sessione persi work uncommitted per agent operations. Worktree isolation raccomandato per parallel agents.
3. **Audit forensic post-cleanup mandatory**: diff `git log --diff-filter=A` per pattern atteso vs filesystem. Stash + dangling check.
4. **Cross-PC merge conflict**: stesso feature implementato 2x con API diverse → merge endpoint sets con namespace diversi (`/api/codex/*` vs `/api/v1/codex/*`).
5. **Engine LIVE Surface DEAD anti-pattern killer**: `ui-design-illuminator` audit dopo Spore Moderate identifica QW-1/QW-2/QW-3 critici (3 surface mancanti). Tutti shipped same session.

## Cross-PC bonus merged stesso periodo

- #1923 Tier B+E (Isaac Anomaly + FF7R + 3 Python tools)
- #1925 5 indie candidates verdict (2 ADOPT 3 DEFER)
- #1931 Tunic glyph progression (collision resolved con #1933)
- #1934 Sprint 1 backend quick wins (Wesnoth + AI War + Disco + Fallout)

## Next session entry-point

Path A: Resolver adapter+alpha consumption (~3-5h, S6 → 100%).
Path B: Mutation catalog rebalance (~3-4h, bingo physiological fix).
Path C: User decisions D3/D4/D5/TKT-09.
Path D: Userland TKT-M11B-06 playtest live (chiude P5 🟢 def).

**Handoff doc**: `docs/planning/2026-04-27-bundle-b-recovery-handoff.md`.
