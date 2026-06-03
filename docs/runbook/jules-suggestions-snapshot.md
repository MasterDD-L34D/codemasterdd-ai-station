# Runbook -- Jules suggestions snapshot (read-only, Claude-in-Chrome)

> G2 of the Jules-autonomy gap plan. Jules **proactive suggestions have NO API**
> (404 on 10 path-variants, CLI blind) -- they are readable ONLY in the browser.
> Per the sec-9 finding (`docs/jules/JULES-CAPABILITIES-MASTER.md`, verified live
> 2026-06-02) the READ is a Claude read-op (navigate + screenshot/get_page_text),
> NOT classifier-blocked. This runbook makes that read a repeatable sweep that
> writes `docs/jules-batch/suggestions-<date>.md`. ASCII-first (ADR-0021).
>
> **Boundary (SDMG R6, invariant):** this flow only READS + drafts verdict-stubs
> for a human/triage pass. **Start / edit+submit / close / toggle = Eduardo**
> (generative external = SDMG-rejected for autonomy). The snapshot never acts.

## Precondition (Eduardo, one-time per sweep)

The browser connection is Eduardo's: this flow cannot run headless.
- Chrome with the Claude extension **connected to this account** (verify:
  `mcp__Claude_in_Chrome__list_connected_browsers` returns a non-empty list).
- That Chrome is **logged into Eduardo's Google account** with jules.google access
  (suggestions are account-scoped, PRO plan, Gemini 3.1 Pro, refresh "every few days").
- If `list_connected_browsers` returns `[]` -> STOP, ask Eduardo to open Chrome +
  the extension. Do not fabricate an inventory; an absent browser = no snapshot.

## Procedure (Claude, read-only)

1. `list_connected_browsers` -> `select_browser` (Eduardo's Chrome).
2. `tabs_context_mcp` / `tabs_create_mcp` to get a working tab id.
3. `navigate` to `https://jules.google` (the suggestions surface).
4. **Per-repo sweep** (opt-in repos only, cap <=5). For each enabled repo:
   - Switch the repo via the **repo dropdown/selector** (the suggestions are
     per-repo; the dropdown re-renders the list).
   - For each suggestion: read **title + category** (Cleanup / Performance /
     Security / Code Health / Testing), then **expand the chevron** to read the
     full structure: **DESCRIPTION + LOCATION (file:line) + RATIONALE + CODE CONTEXT**.
   - **Reading caveat (load-bearing):** `get_page_text` is unreliable here --
     jules.google is an SPA and returns **stale/partial fragments after a
     client-side nav** (dropdown switch / expand do not trigger a full reload).
     **Prefer `screenshot`** to read the rendered list + the expanded panel; use
     `get_page_text` only as a secondary cross-check, never as the sole source.
5. Write `docs/jules-batch/suggestions-<date>.md` with the schema below.

## Output schema (`docs/jules-batch/suggestions-<date>.md`)

```
# Jules suggestions snapshot <date> (READ-ONLY, browser sweep; Start = Eduardo)
> Source: jules.google per-repo suggestions (no API). Verdicts ADVISORY/stub for a
> human/triage pass. Start/edit/submit/close/toggle = Eduardo (SDMG R6).

## <repo> (ENABLED)
- **[<Category>]** <title>
  - LOCATION: <file:line>
  - DESCRIPTION: <one line>
  - VERDICT-STUB: <triage / likely-resolved-verify / defer-freeze / edit-before-Start>
...

## Repos OFF / not-configured
- OFF: <repo, ...>   not-configured: <repo, ...>

## Triage notes
- edit-before-Start: the generic "Start" template lacks our anti-#10 / anti-S5
  constraints -> for a high-signal suggestion, Eduardo uses "edit" to paste the
  guard-rail (zero-behavior, single-file, minimal-diff/no-rewrite, grep-before-
  remove, lock-test CI-green) THEN Starts. Verdict-stubs flag which deserve it.
```

## Verdict-stub vocabulary

- **triage** -- genuine + actionable; draft a scoped dispatch (G6 per-instance) or flag for Eduardo Start.
- **likely-resolved-verify** -- a prior PR may have shipped it; ground-truth before acting (anti-pattern #19).
- **defer-freeze** -- touches a freeze-sensitive path (`services/generation|rules|combat`); Eduardo-review only.
- **edit-before-Start** -- high-signal but needs the guard-rail pasted via "edit" before Start.
- **drop** -- noise / false-positive / contradicts a deliberate design choice (e.g. a stdlib-only fallback).

## Cadence

Suggestions refresh "every few days" -- a snapshot is worth re-running ~weekly or
when the daily digest (G3) is thin. This sweep is NOT cronnable (needs Eduardo's
live browser); it is an on-demand read Eduardo triggers by connecting Chrome.
