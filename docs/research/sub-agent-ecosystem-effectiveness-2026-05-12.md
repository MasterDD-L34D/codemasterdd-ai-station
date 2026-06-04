# Sub-agent ecosystem effectiveness review

> **Audit data**: 2026-05-12 sera (Bundle 3 applicative optimization, AA01 task `2026-05-aa01-001-2026-05-12-bundle-3-applicative-optimiza`)
> **Source**: `.claude/agents/` (18 sub-agent definitions) + `docs/superpowers/tests/` (9 smoke test files) + ADR-0018 agent-readiness-protocol
> **Method**: empirical filesystem inspection + smoke test file count + invocation pattern analysis (JOURNAL grep)

## TL;DR

Ecosystem 18 sub-agent (12 ready / 6 draft) post-ADR-0018 formalizzato 2026-04-24:
- **12 ready empirical**: 9 con smoke test dedicated, 3 grandfathered pre-formalizzazione (mattina batch: harsh-reviewer + delegation-classifier + swarm-cycle-analyzer)
- **6 draft trigger-gated**: scope-specific (game-systems-designer + game-design-validator + lore-consistency-checker + dafne-proposal-triager + database-schema-designer + a11y-wcag-reviewer)
- **Invocation density**: bassa-medio empirica. JOURNAL grep `Agent(` produce 0 match diretti (pattern likely emitted as tool call, not code-cited).
- **Templates Pattern B Bundle 1 PR #48**: SUB_AGENT_TEMPLATE.md + SMOKE_TEST_TEMPLATE.md presenti, NON ancora applicati per new sub-agent (no new sub-agent post-Pattern B adoption).

**Findings actionable**:
- Gap 1 -- 3 grandfathered ready senza smoke test file dedicated (debt accumulato)
- Gap 2 -- 6 draft trigger-gated dormant 18+gg post-batch (validation timeout?)
- Gap 3 -- Invocation telemetry absent (no count empirico cross-session = effectiveness invisibile)

## Findings empirici

### Finding 1 -- Status matrix empirical conferma

Ecosystem 18 agent verificati filesystem `.claude/agents/*.md`:

```
README.md SMOKE_TEST_TEMPLATE.md SOURCES.md SUB_AGENT_TEMPLATE.md
a11y-wcag-reviewer.md adr-drafter.md bench-reporter.md compact-conversation.md
cost-monitor.md dafne-proposal-triager.md database-schema-designer.md
delegation-classifier.md dogfood-analyst.md game-balance-auditor.md
game-design-validator.md game-systems-designer.md harsh-reviewer.md
lore-consistency-checker.md owasp-security-auditor.md privacy-policy-enforcer.md
repo-health-auditor.md swarm-cycle-analyzer.md
```

22 file totali (18 sub-agent + 4 meta: README + SMOKE_TEST_TEMPLATE + SOURCES + SUB_AGENT_TEMPLATE). Matches ADR-0018 codified state.

### Finding 2 -- Smoke test coverage gap

`docs/superpowers/tests/` = 9 file empirici:
```
adr-drafter.md bench-reporter.md compact-conversation.md cost-monitor.md
dogfood-analyst.md game-balance-auditor.md owasp-security-auditor.md
privacy-policy-enforcer.md repo-health-auditor.md
```

Cross-check vs 12 ready agents:
- 9/12 ready agents HANNO smoke test dedicated
- 3/12 ready agents MANCANO smoke test dedicated: **harsh-reviewer + delegation-classifier + swarm-cycle-analyzer** (mattina batch, grandfathered pre-ADR-0018 formalizzazione)

**Gap 1 evidence**: tre agent mattina batch sono "ready" via SUB_AGENT_TEMPLATE.md adherence ma NON hanno passato Gate 1 (smoke test file documented). ADR-0018 strict reading richiederebbe smoke test retroattivo o downgrade a draft.

**Mitigation candidate**:
- (a) Retroactive smoke test 3 agent grandfathered (~30min, 3x ~10min each)
- (b) ADR-0018 addendum: clarifica grandfathered batch status come "ready-grandfathered" (visibile in README matrix)
- (c) Lasciare drift accept (low-stakes, no regress observed)

### Finding 3 -- Draft trigger-gated dormancy

6 draft trigger-gated 18+gg dormant (post-batch P0/P1/P2 24/4):
- **game-systems-designer**: trigger = "design core loop / progetta sistema X" -- NON invocato post-formalizzazione, Sprint Impronta Game in pausa 26/4
- **game-design-validator**: trigger = "valida design / first principles game" -- NON invocato (opus tier, alto costo, situational)
- **lore-consistency-checker**: trigger = "check lore / coerenza narrativa" -- NON invocato
- **dafne-proposal-triager**: trigger = "triage dafne proposals" -- pre-filter pendente Dafne approve workflow, ma 0 proposals new ricevute post-batch
- **database-schema-designer**: trigger = "design schema DB / review Prisma" -- NON invocato (no schema work in 18gg)
- **a11y-wcag-reviewer**: trigger = "check a11y / WCAG review" -- NON invocato (Synesthesia dormant fino ago 2026)

**Pattern**: tutti 6 draft trigger condition specifiche a workflow currently inactive (Game pausa + Dafne batch closed + Synesthesia dormant + no DB schema work).

**Gap 2 evidence**: agent draft NON sono "blocked" -- semplicemente trigger condition assente. Dormancy strutturale, NON failure validation.

**Mitigation candidate**:
- (a) Accept dormancy (workflow-driven, NON bug)
- (b) Trigger condition table esplicita README "When trigger condition expected next" (futuro Sprint Impronta restart / Synesthesia ago 2026 / etc.)
- (c) Audit ratification: deprecation candidate se trigger NON emerge SPRINT_03+ (6+ mesi cumulative dormancy)

### Finding 4 -- Templates Pattern B adoption empirical

`SUB_AGENT_TEMPLATE.md` + `SMOKE_TEST_TEMPLATE.md` presenti (Bundle 1 PR #48 adopt 11/5 notte).

**Empirical adoption post-Pattern B**: 0 new sub-agent creati. Templates NON ancora applicati real-use.

**Verdict**: scaffolding adopted ma NO empirical validation immediate-use. Pattern B value e' "ready when needed", non "actively used now".

**Trigger application future**: prossimo sub-agent NUOVO creato (qualunque trigger Eduardo direct).

### Finding 5 -- Invocation telemetry absent

JOURNAL grep `Agent(` returns 0 matches. Ragione: invocation via Claude Code Tool tool call NON viene documentata literal in JOURNAL (tool call e' in transcript, NON in commit/journal content).

**Cite count alternativo via agent name in JOURNAL**:
- "dogfood-analyst": 8 cite
- "delegation-classifier": 6 cite (incluso Bundle 1 smoke L-002 case study)
- "harsh-reviewer": 4 cite
- Altri agent: <3 cite cumulative

**Gap 3 evidence**: telemetry empirical cross-session ASSENTE. Cite count e' proxy povero per "ha funzionato bene / male / ha dato value".

**Mitigation candidate**:
- (a) AA01 lesson per sub-agent invocazione significativa (gia' pattern emergent L-008 + L-002 menziona delegation-classifier)
- (b) `logs/sub-agent-invocations-YYYY-MM.md` (gitignored) per tracking effort/outcome cross-session
- (c) Accept silenzio empirical (low-stakes, JOURNAL deep dive ricorsivo cattura quando interessante)

## Recommendations

### REC 1 -- Accept grandfathered ready status (Gap 1)

3 agent mattina batch (harsh-reviewer + delegation-classifier + swarm-cycle-analyzer) sono empirical-useful (delegation-classifier smoke 8.2s PASS L-002 documented). Smoke test retroattivo dedicated file effort ~30min vs value marginal. **DEFER smoke test retroattivo** salvo trigger emergente (regress reported).

Alternativa: ADR-0018 addendum minor con "grandfathered-ready" flag visibile README matrix (NO action urgent).

### REC 2 -- Document trigger condition expected per draft dormant (Gap 2)

Aggiungere a `.claude/agents/README.md` colonna "Trigger condition expected next" per 6 draft agent. Helps future-self decide deprecation vs continue dormant.

Esempio:
| Agent | Trigger condition expected | Estimated date |
|-------|---------------------------|---------------|
| game-systems-designer | Sprint Impronta restart | TBR (Game Vue3 vs Godot v2 routing decision) |
| game-design-validator | Major design milestone | TBR (high-stakes architectural design) |
| lore-consistency-checker | Dafne lore-designer output ready | TBR (Atto 2 day 14+ ongoing) |
| dafne-proposal-triager | Dafne approve workflow batch | TBR (no new proposals post-batch) |
| database-schema-designer | Game-Godot-v2 persistence layer | TBR (port progress Game-Godot-v2) |
| a11y-wcag-reviewer | Synesthesia riattiva | 2026-08 (esame UniUPO) |

Effort: ~15min (no code, README update).

### REC 3 -- AA01 lesson pattern per sub-agent invocation high-value (Gap 3 alt-a)

Pattern emergent: L-002 mention delegation-classifier smoke + L-008 mention M11 plugin install Archon validation. Continuare AA01 lesson promotion ogni volta sub-agent invocation reveals non-obvious pattern.

NON action immediata richiesta (pattern gia' emergent). Document su CLAUDE.md o ADR-0018 addendum trigger condition future.

### REC 4 -- STOP all'ulteriore audit pattern

Bundle 3 questo + Bundle 2 + Bundle 1 = ciclo methodology audit completo per questa sessione 12/5 sera. Lesson L-002 anti-pattern "pattern audit churn" applies: STOP fino post-Max (19/05+). SPRINT_02 T2 dogfood organico genera empirical data piu' valuable di nuovi audit.

## Conclusioni

Sub-agent ecosystem 18 (12 ready + 6 draft) e' **structurally consistent ADR-0018** ma **invocation density bassa empirica**. 3 finding identificati con mitigation candidate NON urgent. Templates Pattern B presenti, application empirical attesa NEXT new sub-agent.

**Decisione**: accept current state. Defer mitigation a SPRINT_03+ post-Max scenario A operativo, salvo trigger emergente (regress / new sub-agent need / etc.).

## Cross-link

- ADR-0018: `docs/adr/0018-agent-readiness-protocol.md`
- `.claude/agents/README.md` (status matrix 12 ready + 6 draft)
- `docs/superpowers/tests/` (9 smoke test files)
- Bundle 1 PR #48 Pattern B ADOPT: SUB_AGENT_TEMPLATE.md + SMOKE_TEST_TEMPLATE.md
- L-2026-05-002 caso studio delegation-classifier smoke 8.2s PASS
- L-2026-05-008 caso studio Archon protocol applied to sub-agent invocation pattern
- Bundle 3 companion B8: `docs/research/hook-chain-effectiveness-smoke-2026-05-12.md`
