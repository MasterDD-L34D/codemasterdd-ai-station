# Orchestration Doctrine Rollout Implementation Plan

> **Status (2026-06-23):** shipped -- ADR-0036 Accepted + ORCHESTRATION.md + fleet-tools-mcp live

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate the fragmented multi-LLM/Jules/Opus-4.8 coordination surface into one authoritative orchestration doctrine (ADR-0036 + ORCHESTRATION.md), enable evidence-based autonomy (auto-merge gate + allow-rules, full rollout), and add the missing first-class cloud-key tooling (MCP llm-fleet, SDMG-gated), deployed cross-fleet.

**Architecture:** Hub-and-spoke orchestrator-worker. Opus 4.8 = hub (keeps judgment + verification). Five spokes: inline-Opus, local Ollama fleet, cloud keys, Jules async, in-session subagents/Workflow. Routing by capability x cost x privacy x async-fit. Mandatory different-model verification gate. Autonomy ladder: auto-merge low-risk + external-merge-auto (CI + Codex-resolved + fix + judge); irreducible human residue for irreversible/outward-facing/architecture.

**Tech Stack:** Markdown docs (ADR + doctrine); JSON (`.claude/settings.json` allow-rules, `.mcp.json`); the MCP llm-fleet (Node or Python stdio, decided at its falsification gate); existing Bash wrappers + `jules` CLI + Ollama REST; git + gh; SSH cross-fleet (Lenovo .10 + Ryzen .11).

**Source spec:** `docs/superpowers/specs/2026-05-29-orchestration-doctrine-design.md`

---

## File structure

- Create: `docs/adr/0036-unified-orchestration-doctrine.md` -- the decision record + supersession map.
- Create: `ORCHESTRATION.md` (repo root) -- operational doctrine (single authority / entry point).
- Modify: `MODEL_ROUTING.md` -- add a top banner: superseded-as-top-authority by ORCHESTRATION.md; retained as local-fleet detail.
- Modify: `docs/adr/0013,0022,0023,0030,0034,0035-*.md` -- add a one-line "consolidated under ADR-0036" note (NOT status change; they stay Accepted, ORCHESTRATION.md is the routing entry point).
- Modify: `~/.claude/settings.json` (or project `.claude/settings.json`) -- allow-rules for verified-safe action classes.
- Create (gated): `docs/superpowers/specs/<date>-mcp-llm-fleet-design.md` + the MCP server -- produced by Task 4's SDMG gate, NOT pre-built here.
- Modify: `STATUS_MULTI_REPO.md` -- record doctrine live + autonomy rollout.

---

## Task 1: ADR-0036 (full decision record)

**Files:**
- Create: `docs/adr/0036-unified-orchestration-doctrine.md`

- [ ] **Step 1: Write the ADR (full MADR)**

Use the project ADR convention (em-dash title allowed; ASCII body per ADR-0021). Required sections + exact content:

- Title: `# ADR-0036 — Unified Orchestration Doctrine (multi-LLM + Jules + Opus 4.8)`
- `> Status: **Proposed** — 2026-05-29 (ratify after full rollout + first auto-merge cycle observed)`
- **TL;DR**: hub-and-spoke orchestrator-worker; Opus 4.8 hub + 5 spokes; one ORCHESTRATION.md authority; capability x cost x privacy routing; mandatory different-model verification gate; autonomy ladder incl. external-merge-auto; lightweight MCP llm-fleet tooling (no heavy gateway); anti-framework scope.
- **Context**: fragmentation problem (MODEL_ROUTING local-only + scattered cloud ADRs + ADR-0035 Jules); evidence basis (cite the spec's research appendix sources); OD-009 decommissioned LiteLLM/Langfuse (so: no heavy gateway).
- **Decision**: the doctrine (point to ORCHESTRATION.md as operational authority). Enumerate the 5 spokes, the routing ladder, the verification gate (different-model judge = anti-monoculture), the autonomy ladder + Codex sub-gate, the MCP llm-fleet (SDMG-gated), and the anti-scope.
- **Options considered**: A streamline-unify (CHOSEN); B + lightweight tooling only; C heavy framework (REJECTED -- evidence: failure-surface, solo-dev underperform); D do-nothing/stay-fragmented (REJECTED).
- **Supersession map** (table): ADR-0013 (cloud-free) / 0022 (OpenCode) / 0023 (strategic API) / 0030 (Hybrid A1) / 0034 (Jules mandate) / 0035 (Jules dispatch) -> "routing surface consolidated under ADR-0036 + ORCHESTRATION.md; individual ADRs remain Accepted as detail". MODEL_ROUTING.md -> "reframed as local-fleet detail under ORCHESTRATION.md".
- **Consequences**: positive (single entry point, evidence-based autonomy, first-class key tooling); negative/risk (external-merge-auto full rollout = aggressive; mitigated by judge+Codex+CI+reversibility); ratify trigger (observe >=1 clean auto-merge cycle per repo + zero bad-merge incidents over 2 weeks).
- **References**: the spec + the 8 research sources + OD-009.

- [ ] **Step 2: Verify ASCII + commit**

Run: `perl -ne 'exit 1 if /[^\x00-\x7F]/' docs/adr/0036-unified-orchestration-doctrine.md && echo ASCII-OK`
Expected: `ASCII-OK`
Commit (conventional, ADR-0011 trailers, subject <=72 lowercase desc):
```
docs(adr): add ADR-0036 unified orchestration doctrine (Proposed)
```

---

## Task 2: ORCHESTRATION.md (operational doctrine, single authority)

**Files:**
- Create: `ORCHESTRATION.md` (repo root)
- Modify: `MODEL_ROUTING.md` (top banner)

- [ ] **Step 1: Write ORCHESTRATION.md**

ASCII-first. Sections (operationalize spec sections 1-7, concrete + actionable):
1. **Purpose + authority**: this is the single routing/orchestration entry point; `CLAUDE.md` = how, this = which-executor-and-autonomy; MODEL_ROUTING = local-fleet detail (linked); ADR-0036 = why.
2. **Core model**: hub Opus 4.8 + 5 spokes (table: spoke | role | exact invocation). Copy the invocation commands from spec sec 1-2 (ollama run / aider-* wrappers / jules CLI+REST / Agent tool / Workflow).
3. **Routing decision-tree**: the spec sec-3 fenced tree verbatim + cost-ladder + adoption rule ("cheapest-sufficient spoke before inline-Opus").
4. **Verification gate**: CI + ground-truth triage + different-model judge (harsh-reviewer) + schema/scope. Mandatory for non-inline output.
5. **Autonomy ladder**: the spec sec-5 table + the precise Codex sub-gate procedure (wait for Codex auto-review -> evaluate every comment -> fix real / dismiss nit-with-rationale -> re-CI -> judge -> auto-merge). Irreducible-human residue list.
6. **Standing permission classes**: which action classes are allow-listed (read-ops, local commit, branch push non-main, local-LLM dispatch, Jules list/pull/archive/sendMessage) vs never-allow-listed (irreducible residue).
7. **Spoke invocation layer**: 10 keys, Bash invocation reality, the MCP llm-fleet (once built) as the native `llm_call` path; adoption rule.
8. **Anti-scope**: no heavy framework/gateway; evidence pointer to ADR-0036.

- [ ] **Step 2: Add MODEL_ROUTING.md banner**

At top of `MODEL_ROUTING.md` after the title, insert:
```
> **Consolidated 2026-05-29:** the cross-executor routing authority is now `ORCHESTRATION.md`
> (ADR-0036). This file is the LOCAL-FLEET detail (llmfit / Ollama 2-machine). For
> "which executor for task X" (local vs cloud vs Jules vs inline) see ORCHESTRATION.md.
```

- [ ] **Step 3: Verify ASCII + commit**

Run: `perl -ne 'exit 1 if /[^\x00-\x7F]/' ORCHESTRATION.md && echo ASCII-OK`
Expected: `ASCII-OK`
Commit:
```
docs(orchestration): add ORCHESTRATION.md doctrine + MODEL_ROUTING banner
```

---

## Task 3: Consolidation notes on superseded ADRs

**Files:**
- Modify: `docs/adr/0013-*.md`, `0022-*.md`, `0023-*.md`, `0030-*.md`, `0034-*.md`, `0035-*.md`

- [ ] **Step 1: Add one-line note to each**

Under each ADR's status line, add (ASCII):
```
> Routing surface consolidated under ADR-0036 (ORCHESTRATION.md) 2026-05-29. This ADR remains Accepted as detail; the cross-executor entry point is ORCHESTRATION.md.
```
Do NOT change their Accepted status. Do NOT alter their bodies.

- [ ] **Step 2: Commit**

```
docs(adr): cross-link 6 routing ADRs to ADR-0036 consolidation
```

---

## Task 4: MCP llm-fleet (SDMG-GATED -- research + falsify before build)

> This task does NOT build the server blind. Per SDMG (Protocol 7) + anti-pattern #8 (no shallow-adopt), the build is gated by external falsification. It PRODUCES a go/no-go + (if go) a dedicated spec+plan.

**Files:**
- Create: `docs/research/<date>-mcp-llm-fleet-eval.md` (the falsification record)
- Create (only if GO): `docs/superpowers/specs/<date>-mcp-llm-fleet-design.md`

- [ ] **Step 1: Research the minimal viable shape**

Decide: build-custom (thin stdio MCP, ~100 lines, reads keys.env, one `llm_call(provider, model, prompt, [max_tokens])` over OpenAI-compatible endpoints + Gemini) vs adopt-existing (e.g. `lior-ps/multi-llm-cross-check-mcp`). Document tradeoffs. Constraint: NO heavy gateway (LiteLLM/Bifrost) per OD-009. Record in the eval doc.

- [ ] **Step 2: External falsification (harsh-reviewer + smoke)**

Spawn `harsh-reviewer` (different-model judge) on the proposed shape: does it add more failure-surface than value? secret-handling (keys not in argv)? maintenance burden? Run a 1-call smoke against ONE provider (e.g. Groq via the existing key) to prove the call path works. Pre-commit: "if harsh-reviewer rejects, I adopt-not-defend (no build)."

- [ ] **Step 3: Decision gate**

If survives falsification -> write `docs/superpowers/specs/<date>-mcp-llm-fleet-design.md` + a dedicated TDD plan (separate writing-plans cycle), then build. If rejected -> record NO-GO in the eval doc; the Bash wrappers + REST remain the invocation path; update ORCHESTRATION.md sec-7 to drop the MCP reference. Log the SDMG invocation in `logs/sdmg-invocations.md` (ADOPT or REJECT, with executed-experiment = the smoke).

- [ ] **Step 4: Commit the eval record**

```
docs(research): mcp llm-fleet SDMG falsification eval + verdict
```

---

## Task 5: Autonomy enablement (allow-rules + auto-merge procedure)

**Files:**
- Modify: `.claude/settings.json` (project) -- allow-rules
- The auto-merge procedure lives in ORCHESTRATION.md sec-5 (Task 2)

- [ ] **Step 1: Add allow-rules for verified-safe classes**

In `.claude/settings.json` `permissions.allow`, add rules for the verified-safe action classes (read-ops, local git commit, branch push non-main, local-LLM dispatch, `jules remote list/pull`, Jules archive/sendMessage). Use the harness allow-rule syntax (Bash command prefixes / tool matchers). Do NOT allow-list irreducible classes (force-push main, account-credential, external-comms, destructive). Verify against the `update-config` skill format.

- [ ] **Step 2: Smoke-verify a previously-prompted action now passes**

Pick one verified-safe action that was classifier-prompted earlier (e.g. `jules remote list`) and confirm it runs without prompt after the allow-rule. Record in commit body.

- [ ] **Step 3: Commit**

```
chore(settings): allow-rules for verified-safe orchestration action classes
```

---

## Task 6: Cross-fleet deploy + status

**Files:**
- Modify: `STATUS_MULTI_REPO.md`

- [ ] **Step 1: Merge the doctrine branch to main**

PR the `claude/orchestration-doctrine-2026-05-29` branch (codemasterdd own repo). Self-review + CI green -> squash-merge + delete branch.

- [ ] **Step 2: Record live status**

In `STATUS_MULTI_REPO.md`, add a row/note: orchestration doctrine (ADR-0036 + ORCHESTRATION.md) LIVE 2026-05-29; autonomy full-rollout; MCP llm-fleet status (per Task 4 verdict). Commit:
```
docs(status): orchestration doctrine live + autonomy rollout
```

- [ ] **Step 3: Sync Ryzen**

The doctrine governs both PCs. SSH Ryzen: `git pull origin main` (SSH origin now works). Verify `git rev-parse --short HEAD` matches Lenovo. Allow-rules: settings.json is per-machine -- replicate the allow-rules on Ryzen (`~/.claude/settings.json` or its project settings) OR note it as Ryzen-side follow-up if the file differs.

---

## Self-review

- **Spec coverage:** sec1 core-model -> Task 2; sec2 invocation+tooling -> Task 2 + Task 4; sec3 routing -> Task 2; sec4 verification gate -> Task 2; sec5 autonomy+Codex -> Task 2 + Task 5; sec6 allow-rules -> Task 5; sec7 Opus angle -> Task 2; anti-scope -> Task 1+2; ADR-0036 -> Task 1; supersession -> Task 1+3; MCP -> Task 4; rollout full + deploy -> Task 5+6. All covered.
- **Placeholder scan:** doc-content tasks reference exact spec sections + provide the exact banners/notes/commit messages. The MCP build is intentionally gated (not a placeholder -- it is a real SDMG decision gate that produces its own spec+plan; writing blind TDD code for it would itself be the violation).
- **Consistency:** branch name `claude/orchestration-doctrine-2026-05-29` consistent; ADR number 0036 consistent; `llm_call(provider, model, prompt, [max_tokens])` signature consistent across spec + plan.

## Notes for the executor

- These deliverables are docs + config + 1 gated-software-eval, NOT a typical TDD codebase. "Verification" for docs = ASCII check + commit-hooks pass + supersession-map accuracy. The only TDD is inside the MCP llm-fleet's OWN plan (produced at Task 4 if GO).
- Commit hooks: subject <=72 chars, lowercase description after `type(scope):`, ADR-0011 trailers (`Coding-Agent` + `Trace-Id`, NO Co-Authored-By). Use PowerShell here-string for multiline commit messages (proven reliable; printf/$() mangles them).
- ASCII-first (ADR-0021) on every new doc; `perl -ne 'exit 1 if /[^\x00-\x7F]/'` (NOT grep -P, GNU-only).
