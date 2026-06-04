# Gate-E evidence base (codemasterdd Short, GOALS.md)

> Durable, tracked summary of the Gate-E evidence-logging Short. The detailed
> ledgers are local operational artifacts under `logs/` (gitignored by design,
> `.gitignore` line 49 `logs/*` + line 81 anticipated `logs/sdmg-invocations-*.jsonl`);
> this file is the git-durable, cross-session, cross-fleet-readable summary the
> **~2026-06-03 hub-shape re-eval + D2 gate review** consumes, and the
> **~2026-08-01 SDMG quarterly review** references.
>
> Scope (load-bearing, per spec `docs/superpowers/specs/2026-05-22-four-repo-short-directions-design.md`):
> **LOGGING ONLY.** Writes evidence; never proposes/spawns/auto-triggers D2.
> D2 auto-coordination stays GATED until ~2026-06-03.

## 1. SDMG invocation ledger

Detail: `logs/sdmg-invocations.md` (local). SDMG = ADR-0026 Protocol 7.

| Metric | Value (2026-05-29) | Health |
|--------|--------------------|--------|
| Total invocations (window from 2026-05-20) | 4 | -- |
| ADOPT / REJECT | 2 / 2 | -- |
| Adoption rate | 50% | GREEN (trigger fires < 30%) |
| ADOPT-without-executed-falsifying-experiment | 0 | GREEN (trigger fires > 0) |

Invocations: (1) whisper-local stack -> **ADOPT** (smoke executed); (2) autonomous-next-point protocol -> **REJECT** (harsh-reviewer falsification, archived); (3) ADR-0035 Jules-CLI dispatch routine -> **ADOPT** (N=5 scoped clean-rate 5/5 executed before Accept); (4) MCP "llm-fleet" general completion-routing -> **REJECT** (harsh-reviewer 5/5 NO-GO + Groq REST smoke proved keys reachable without MCP; split: general-routing REJECT, scoped fleet-tools MCP GO deferred to own spec).

**Both ADR-0026 quarterly-review triggers GREEN** -- discipline holding (every ADOPT had a pre-commit executed experiment; both falsified methods were rejected-not-defended, incl. MCP llm-fleet rejected same-day before any build).

## 2. Hybrid A1 cost/cite

Detail: `logs/hybrid-a1-cost-cite-2026-05.md` (local). ADR-0030 Hybrid A1.

| Tier | State | May spend |
|------|-------|----------:|
| Pro + Meridian bridge | config prepared, NOT auth'd | $0 |
| Gemini CLI / Groq / Cerebras / HF / GitHub Models (free) | active | $0 |
| OpenRouter overflow | account PENDING | $0 |
| Local Ollama (Ryzen+Lenovo) | active | $0 |
| **Effective external $ (window)** | | **$0.00** |

Read: sovereign + free + subscription mix carried the workload at **$0 incremental external spend** through the SDMG window; Hybrid A1 paid tiers (Pro, OpenRouter) remain dormant. Decision input for 06-03: activate Pro or stay current-mix.

## 3. H7 strategic API spend

Detail: `logs/claude-api-spend-2026-05.md` (local, ADR-0023). May: **$0** (0 pay-per-use strategic tasks; budget cap $10-20). Scaffold active; first entry expected when a strategic task is explicitly authorized.

## Status

- **Gate-E evidence base: LIVE** (2026-05-29). 3 artifacts populated (1 SDMG ledger backfilled + 2 cost scaffolds).
- Ready for ~2026-06-03 gate review (evidence-driven, not recollection-driven).
- Maintenance: append SDMG invocations as they occur; add cost entries if a paid tier activates; roll spend file monthly.
- Non-gated, logging-only -- structurally cannot trigger D2 early.
