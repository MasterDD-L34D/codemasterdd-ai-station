# ADR-0030 — Post-Max orchestration architecture: Hybrid A1 (Pro + Meridian + OpenCode + Gemini CLI)

> *TL;DR: Eduardo realization 2026-05-15 mattina: sovereign post-Max ADR-0015 scenario A è INCOMPLETO — copre solo code-editing tier (Aider/OpenCode), NON copre orchestration + reasoning + methodology + sub-agents + skills layer fornito da Claude Code desktop. Eduardo usage 75% Max settimanale = volume incompatibile con free-tier-only. Autoresearch deep ha identificato meridian + opencode-with-claude plugin che bridge official Anthropic SDK a OpenCode = preserva methodology + Pro subscription $20/mo. Decisione: **Hybrid A1** = CC Pro $20/mo + Meridian + OpenCode (orchestration heavy) + Gemini CLI free 1000 req/day (routine fallback) + OpenRouter (emergency pay-per-use). Cost realistico: $240-600/anno = ADR-0015 target $50/anno VIOLATED + amendment necessario.*

- **Status**: **Accepted 2026-05-18** (pivot sovereign->hybrid-paid ratificato esplicitamente da Eduardo — vedi DECISIONS_LOG Decisione 009). Originale Proposed 2026-05-15 mattina.
> Consolidated under ADR-0036 (ORCHESTRATION.md) 2026-05-29: routing surface unified; this ADR stays Accepted as detail. Cross-executor entry point = ORCHESTRATION.md.
- **Data**: 2026-05-15 (P) -> 2026-05-18 (A)
- **Decisore**: Eduardo Scarpelli
- **Type decisione**: architectural post-Max strategy + financial commitment
- **Supersedes**: parziale ADR-0015 scenario A (full-sovereign $0-50/anno target unrealistic at Eduardo usage)
- **Extends**: ADR-0022 (OpenCode routing) + ADR-0023 (strategic tier post-Max)
- **Reactivates**: ADR-0029 (OpenRouter as fallback, was declined for primary)

## Context and Problem Statement

ADR-0015 scenario A (full-sovereign $0-50/anno) treated Claude Code Max OAuth subscription as "expensive Anthropic dependency replaceable with Aider + OpenCode + cloud free tier providers". Reality 2026-05-15 mattina post Eduardo statement:

> "non ho un modo effettivo per affrontare il tutto senza claude code desktop! capisci cosa dico?"

**Gap identified**: Aider/OpenCode replace CODE EDITING tier. They do NOT replace:
- 🗣️ Conversation + reasoning interface
- 🧠 Multi-source synthesis (ADR draft / research / strategic)
- 🛠️ Tool orchestration multi-step coordinated
- 🤖 Sub-agents (harsh-reviewer, repo-health-auditor, brainstorming skill)
- 📦 Plugin ecosystem (superpowers, claude-mem, compass)
- 🔄 Methodology Protocols P1-P6 application

**Eduardo usage volume**: 75% Max settimanale = ~2M tokens/mese. Free-tier only insufficient.

## Decision Drivers

1. **Methodology preservation** ottimo (Protocols + skills + sub-agents)
2. **Cost predicibilità** (subscription flat vs pay-per-use variable)
3. **UX continuity** (Eduardo familiar workflow)
4. **Migration effort** acceptable (<1 settimana setup)
5. **Sovereign-compatible** (BYOK, no Anthropic lock-in)
6. **Privacy compatible** (keys.env + whitelist + sovereign repos)

## Considered Options

### Option A — OpenRouter pay-per-use Anthropic (ADR-0023 original)
- Cost: $20-50/mo variable
- Pros: BYOK, multi-provider single endpoint
- Cons: cost unpredicable, no methodology auto-preservation
- Rejected: cost variability + methodology effort

### Option B — Hybrid A1 (THIS DECISION)
- Components: CC Pro $20/mo + Meridian + OpenCode + Gemini CLI free fallback
- Cost: $240/anno + 0-30/mo variable = $240-600/anno realistic
- Pros: methodology mostly preserved + cost predicibile + multi-provider via OpenCode + Gemini free routine
- Cons: ADR-0015 target violation explicit
- **Accepted**: best tradeoff per analyzed criteria

### Option C — CC Pro $20/mo solo (no OpenCode migration)
- Cost: $240/anno
- Pros: zero migration effort, full methodology preserved
- Cons: vendor lock-in Anthropic, no multi-provider flexibility
- Rejected: misses OpenCode flexibility opportunity

### Option D — Gemini CLI free tier solo
- Cost: $0
- Pros: 1000 req/day FREE + 1M context Gemini 2.5 Pro
- Cons: Google model not Claude (different methodology + strengths)
- Rejected: methodology framework Claude-centric, switching = retraining

### Option E — Dashboard custom Anthropic API integration build
- Cost: $20-50/mo API + 4-8 weeks build
- Pros: full control + integrated UX
- Cons: re-build CC features massive effort
- Rejected: cost > benefit at Eduardo solo-dev scope

### Option F — Other CLI alternatives (Cline / Cursor / Codex / Aider standalone)
- Various tradeoffs not Claude-quality OR not free-tier-feasible
- Rejected: option B captures benefits without locked-in switch

## Decision

**Hybrid A1**:

### Primary orchestration tier
- **Claude Code Pro $20/mo subscription** (Eduardo manual subscribe)
- **OpenCode + Meridian plugin** bridges Pro to OpenCode TUI/desktop/mobile-drivable
- Use for: methodology application (Protocols P1-P6), multi-source synthesis, ADR drafts, sub-agent dispatch, conversation + reasoning + tool orchestration

### Secondary routine tier
- **Gemini CLI free** 1000 req/day Gemini 2.5 Pro 1M context
- Use for: routine queries, lower-stakes tasks, fallback when Pro daily limit hit

### Emergency overflow tier
- **OpenRouter pay-per-use** (re-activation ADR-0029 as fallback, NOT primary)
- Multi-provider: Anthropic + OpenAI + Mistral + etc.
- Use for: rare overflow / specific model needs

### Existing tiers preserved
- **Aider wrappers**: cosmetic + behavior single-file delegations (Groq + Cerebras free)
- **Local Ollama**: cosmetic 7B + behavior 14B Q2 + escalation 30B MoE
- **Dashboard v0.3 LIVE**: cross-repo visibility + Component 2/3 workflow integration

### Cost realistic post-Max

| Component | Cost/mo | Cost/anno |
|-----------|---------|-----------|
| CC Pro subscription | $20 | $240 |
| Gemini CLI free | $0 | $0 |
| OpenRouter overflow | $0-30 variable | $0-360 |
| Aider cloud free (Groq+Cerebras+Gemini) | $0 | $0 |
| Local Ollama | $0 (hardware sunk) | $0 |
| **Total realistic** | **$20-50** | **$240-600** |

**vs ADR-0015 target $0-50/anno**: VIOLATED. Amendment required.
**vs Claude Max $100/mo current**: ~60-80% riduzione.

## Consequences

### Positive
- Methodology framework mostly preserved (skills/sub-agents via Pro + OpenCode bridge)
- Cost predicibile (~$20/mo flat + minor overflow)
- Multi-provider flexibility via OpenCode (Anthropic + OpenAI + Gemini + local + Groq)
- Mobile-drivable (OpenCode client/server architecture)
- BYOK preservation (sovereign-compatible)
- Privacy guard rail unchanged (whitelist + wrappers + sovereign repos)

### Negative
- ADR-0015 scenario A target violated (acknowledged via amendment)
- $240/anno subscription commitment (vs $0-50 fanta-target)
- Methodology partial port to OpenCode (skills format may need adaptation)
- Vendor relationship Anthropic continues (mitigated by multi-provider OpenCode)

### Neutral
- Setup ~3h Max-tier work (within current budget)
- Eduardo decision authorized 2026-05-15 mattina (this ADR ratification trigger)

## Implementation Plan

### Pre-Max immediate (5gg residui 15-19/5)

1. **Eduardo manual subscribe Pro $20/mo** ([anthropic.com/claude/upgrade](https://www.anthropic.com/claude/upgrade)) — 5min when convenient. Timing: anytime pre-19/5 OR week of 19/5 to avoid gap.

2. **OpenCode + Meridian plugin install** (~30min):
   ```bash
   # Install opencode-with-claude plugin
   npm install -g opencode-with-claude
   # OR per OpenCode plugin convention
   opencode plugin install opencode-with-claude
   ```

3. **Configure OpenCode** ~/.config/opencode/opencode.json:
   - Add Anthropic provider via Meridian bridge
   - Default to Pro subscription instead of API tokens
   - Test session: `opencode` → select Claude Opus/Sonnet → verify connection

4. **Gemini CLI install** (~15min):
   - Follow [Google AI documentation](https://ai.google.dev) for Gemini CLI setup
   - Auth with Google account free tier
   - Verify 1000 req/day quota

5. **OpenRouter optional config** (~15min):
   - Sign up [openrouter.ai](https://openrouter.ai)
   - Add OPENROUTER_API_KEY to `~/.config/api-keys/keys.env`
   - Add OpenRouter provider to opencode.json (anthropic models routing)

### ADR amendments cumulative

- **ADR-0015 amendment** (companion this ADR): scope honest update sovereign $0-50/anno → $240-600/anno realistic; sovereign target rescoped "no Max + multi-provider flexibility" NOT "$0".
- **ADR-0029 reactivation**: OpenRouter from "declined for primary" to "accepted for emergency fallback only".
- **ADR-0023 supersession partial**: Strategic tier post-Max API on-demand replaced by Pro subscription primary (still valid for ad-hoc strategic if Pro daily limit hit).

### Methodology framework migration

- **Skills**: brainstorming + writing-plans + subagent-driven-development → port to OpenCode patterns (effort opportunistic post-setup empirical use)
- **Sub-agents**: harsh-reviewer + repo-health-auditor + brainstorming etc. → leverage OpenCode agent system OR maintain CC sub-agents via Pro session orchestration
- **Plugin ecosystem** (compass + superpowers + claude-mem): re-evaluate post-OpenCode bridge live
- **Protocols P1-P6**: ADR-0026 invariata, application via OpenCode session orchestration

### Validation criteria

| Metric | Threshold | Window |
|--------|-----------|--------|
| Cost actual / mese | ≤$50 (1 mese empirical) | 1 mese post-Max (19/5 → 19/6) |
| Daily orchestration feasibility | empirical pass / fail (Eduardo daily use post-Pro) | 1 settimana post-setup |
| Methodology cite count maintained | ≥80% baseline (per JOURNAL.md) | 4 settimane post-Max |
| Sub-agent dispatch viability | n>=2 invocations OpenCode-mediated | 4 settimane post-Max |

**Trigger Accepted ratification**: 1 mese post-Max empirical validation 4/4 criteria PASS → flip Proposed → Accepted.

**Trigger reactivation pivot**: SE 1 mese empirical violation 2+ criteria → re-open architectural decision (Option A pay-per-use OR Option C Pro-only OR scenario reset).

## Cognitive protocols applied

- **Protocol 1 Refresh-verify**: state check current capabilities pre-decision
- **Protocol 2 Autoresearch multi-source**: 3 web searches (alternative CLI + Meridian + OpenCode comparison) + internal scan (ADRs 0015/0022/0023/0029)
- **Protocol 3 Archon 7-step**: RESTATE + ENUMERATE assunti + DECOMPOSE + CHALLENGE + RECONSTRUCT + RED-TEAM + CALIBRATE applied inline this ADR
- **Protocol 6 Brainstorming**: 6 options A-F analyzed with explicit tradeoffs
- **Protocol 5 harsh-reviewer**: DEFER (apply post-implementation validation 1 settimana)

## Falsifiability

This decision is falsifiable via 1 mese empirical post-Max. Specifically:
- IF cost actual >$50/mo consistently → pivot to Option C (Pro only, less variable)
- IF methodology cite count drops <50% baseline → migration effort failed, re-evaluate
- IF OpenCode + Meridian breaks (Meridian deprecated / Anthropic blocks SDK access) → fallback Option A (OpenRouter pay-per-use)

## References

- ADR-0015 (sovereign-first $0-50/anno target — superseded partial)
- ADR-0022 (OpenCode tool-use model routing — extended)
- ADR-0023 (strategic tier post-Max API — partial supersession)
- ADR-0026 (cognitive protocols — invariata, applied this ADR)
- ADR-0029 (OpenRouter declined — reactivated as fallback)
- L-2026-05-019 (trigger validation window > single-session decision fatigue)
- [Meridian repo](https://github.com/rynfar/meridian)
- [OpenCode with Claude plugin](https://github.com/ianjwhite99/opencode-with-claude)
- [OpenRouter Anthropic pricing](https://openrouter.ai/anthropic/claude-opus-4.7)
- [Gemini CLI free tier docs](https://ai.google.dev)
- Eduardo statement 2026-05-15 mattina: "non ho un modo effettivo per affrontare il tutto senza claude code desktop"
- Eduardo screenshot Max usage 75% settimanale (high-volume validation)

## Effective date

**Active from 2026-05-15 sera-tardi-ultra-3** post Eduardo authorization "AUTORIZZA setup + ADR-0030 ship NOW".
