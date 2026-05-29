# fleet-tools MCP -- scoped design spec (2026-05-29)

> Status: APPROVED (Eduardo 2026-05-29). Scope GO'd via SDMG human-reframe.
> Authority chain: `docs/research/2026-05-29-mcp-llm-fleet-eval.md` (CORRECTION section)
> + `docs/adr/0036-unified-orchestration-doctrine.md` (Decision 5) + `ORCHESTRATION.md` (sec 7).
> ASCII-first body prose (ADR-0021). This spec feeds writing-plans, not implementation directly.

## 1. Problem + scope

Eduardo flagged a discoverability gap: cloud API keys in `keys.env` are not first-class
tools the hub (Opus 4.8) can invoke natively. The SDMG gate REJECTED a general
completion-routing MCP (`llm_call` to weaker cloud models) -- no caller, the hub is more
capable than every callable cloud model, LiteLLM-gateway-redux per OD-009. The human reframe
GO'd a NARROW alternative: expose only the capabilities that have real callers -- services
the hub genuinely lacks, plus a different-model judge for anti-monoculture verification.

**In scope -- exactly three tools:**

1. `tavily_search(query, [max_results])` -- Tavily web search (richer/alternate vs the hub's
   built-in WebSearch). Key TAVILY_API_KEY.
2. `openai_image(prompt, [size])` -- OpenAI image generation. The hub cannot generate images.
   Key OPENAI_API_KEY.
3. `cross_check(model, prompt)` -- send a prompt to a NON-Claude model (Gemini or Groq) for a
   different-model-family second opinion. This is the doctrine's anti-monoculture lever: the
   harsh-reviewer subagent is itself Claude (same-family blind spot). Keys GEMINI_API_KEY /
   GROQ_API_KEY.

**Explicitly OUT of scope (anti-scope, do NOT build):** no `llm_call` general completion
router; no cost-routing; no multi-provider fanout / LiteLLM-redux; no Docker / proxy /
Langfuse / observability; no caching, retries, rate-limit logic, config file, or 4th tool.

## 2. Architecture

Single Node ESM stdio MCP server using the official `@modelcontextprotocol/sdk`. Native
`fetch` for all three provider APIs -- one dependency total (the SDK), zero per-provider
SDKs. This minimizes the drift surface the SDMG eval flagged as the main long-term risk
("drift owner = solo, forever"). Stateless except for generated image files on disk.
Spawned by Claude Code via the root `.mcp.json` (`command: node`, relative args path).

Runtime: Node 24.15 (present on both fleet PCs). Transport: stdio (no Docker, no proxy --
OD-009 anti-overhead).

### Components (each one job, independently testable)

- **`keys.mjs`** -- `readKey(name)`: reads `~/.config/api-keys/keys.env` via `os.homedir()`
  (portable Lenovo `edusc` / Ryzen `Vgit`), parses `NAME=value` lines, returns the ONE
  requested value. Lazy, per-call. Throws a clear error if the key is absent. Never logs the
  value. No "load all 10 keys into env" step.
- **`server.mjs`** -- registers the three tools, wires stdio transport, dispatches each
  tool call to its handler. Logs only to stderr (stdout is the MCP protocol channel),
  key-redacted.

## 3. Tool contracts

### 3.1 tavily_search

- Input: `query` (string, required), `max_results` (integer, optional, default 5, clamp 1-20).
- Call: `POST https://api.tavily.com/search`, header `Authorization: Bearer <TAVILY_API_KEY>`,
  body `{ query, max_results, search_depth: "basic", include_answer: true }`.
- Output (text): the synthesized `answer` if present, then a numbered list of results
  (title -- url -- score -- snippet).

### 3.2 openai_image

- Input: `prompt` (string, required), `size` (string, optional, default `1024x1024`;
  allowed: `1024x1024`, `1024x1536`, `1536x1024`, `auto`).
- Call: `POST https://api.openai.com/v1/images/generations`, header
  `Authorization: Bearer <OPENAI_API_KEY>`, body
  `{ model: "gpt-image-1", prompt, size, quality: "medium", n: 1 }`.
  (quality is hardcoded `medium` -- ~$0.04-0.07/image -- and documented as editable in source;
  not exposed per the 2-arg scope.)
- Response handling: `data[0].b64_json` -> decode -> write PNG to
  `apps/fleet-tools-mcp/output/<utc-timestamp>-<slug>.png` (output/ gitignored).
- Output (text): saved file path + the size used + `revised_prompt` if returned.

### 3.3 cross_check

- Input: `model` (string, required), `prompt` (string, required).
- Routing (prefix on `model`):
  - starts with `gemini` -> Gemini:
    `POST https://generativelanguage.googleapis.com/v1beta/models/<model>:generateContent`,
    key via header `x-goog-api-key: <GEMINI_API_KEY>` (NOT a query param -- keeps the key out
    of the URL / logs), body `{ contents: [{ parts: [{ text: prompt }] }] }`. Read
    `candidates[0].content.parts[*].text`.
  - otherwise -> treat `model` as a Groq model id:
    `POST https://api.groq.com/openai/v1/chat/completions`, header
    `Authorization: Bearer <GROQ_API_KEY>`, body
    `{ model, messages: [{ role: "user", content: prompt }] }`. Read
    `choices[0].message.content`.
  - empty/unrecognized model -> error listing valid examples
    (`gemini-2.5-flash`, `llama-3.3-70b-versatile`).
- Output (text): the answering provider + model + the model's answer (clearly labeled as a
  non-Claude second opinion for the hub to weigh, not an authority).

## 4. Data flow

hub (Claude Code / Opus) -> stdio JSON-RPC -> tool handler -> `readKey()` per-call -> HTTPS to
provider -> parse response -> text result back over stdio. No state persisted except
`output/*.png` from `openai_image`.

## 5. Error handling

Each handler is wrapped: on any failure return an MCP result with `isError: true` and a
human-readable `text` message. Any API key substring is redacted from error text before
return. Per-call timeouts via `AbortController`: `tavily_search` / `cross_check` 30s,
`openai_image` 120s (image gen is slow). Non-2xx HTTP -> include status + provider error body
(redacted) so the hub can act on it.

## 6. Security (CWE-214 + secret residency)

- Keys NEVER appear in argv: the server makes in-process `fetch` calls with the key in a
  request header, so there is no child-process argument list to leak (strictly safer than the
  aider-groq-bypass temp-env-file pattern, which exists only because Aider needs the key in
  its environment).
- Keys NEVER logged: stderr logs exclude key values; error paths redact.
- Keys read PER-CALL (only the one key a tool needs), not all 10 loaded resident for the
  whole session -- directly answers the SDMG eval's "secret-residency regression" concern.
- Gemini key travels in a header, not the URL query string.

## 7. Files

- `apps/fleet-tools-mcp/server.mjs`
- `apps/fleet-tools-mcp/keys.mjs`
- `apps/fleet-tools-mcp/package.json` (`type: module`, dep `@modelcontextprotocol/sdk`)
- `apps/fleet-tools-mcp/README.md` (tools, usage, security notes, drift-owner note, quality
  knob)
- `apps/fleet-tools-mcp/.gitignore` (`node_modules/`, `output/`)
- root `.mcp.json` -- register the `fleet-tools` server
- doc-sync: `ORCHESTRATION.md` line ~24 stale `llm_call (MCP llm-fleet once built)` reference
  -> replace with the built `fleet-tools` tool names; note sec 7 build DONE.

## 8. Verification plan (SDMG-minimal -- ADR-0026 Protocol 7)

The scoped design is a HYPOTHESIS, falsified before it counts as done:

1. One executed smoke PER tool, citing real output:
   - `tavily_search` -- a real query, show returned results.
   - `openai_image` -- one generation, show the written PNG path + that the file exists.
   - `cross_check` -- a real Gemini call, show the answer (the Groq REST call-path already
     smoke-passed 2026-05-29 per the eval; a Groq route check is cheap and optional).
2. harsh-reviewer subagent pass on the FINAL minimal design + code (different-model... note:
   harsh-reviewer is Claude -- that limitation is exactly why `cross_check` exists; it remains
   the standing pre-merge judge per ORCHESTRATION.md sec 4).
3. Only after both: register in `.mcp.json`, commit (Conventional Commits + ADR-0011 trailers
   Coding-Agent + Trace-Id, NO Co-Authored-By), open PR, auto-merge iff CI green + judge OK
   (ORCHESTRATION.md sec 5 autonomy ladder, own repo).

## 9. YAGNI / non-goals

No caching. No retry/backoff. No rate-limit handling. No config file. No provider beyond the
three tools' needs. No 4th tool. No streaming. Exactly three tools, smallest sufficient.
