# fleet-tools MCP

Scoped stdio MCP server exposing three cloud-key capabilities the hub (Claude Code / Opus
4.8) genuinely lacks or needs a different model for. Used WITH Opus inside multi-agent steps,
NOT as a cheaper completion router.

- Authority: `docs/adr/0036-unified-orchestration-doctrine.md` (Decision 5) + `ORCHESTRATION.md`
  (sec 7) + `docs/research/2026-05-29-mcp-llm-fleet-eval.md` (CORRECTION section).
- Spec: `docs/superpowers/specs/2026-05-29-fleet-tools-mcp-design.md`. Plan:
  `docs/superpowers/plans/2026-05-29-fleet-tools-mcp.md`.

A general `llm_call` completion-router was SDMG-REJECTED (no caller -- the hub is more capable
than every callable cloud model; LiteLLM-gateway-redux per OD-009). Do NOT re-add one.

## Tools

| Tool | Args | Key | Returns |
|------|------|-----|---------|
| `tavily_search` | `query` (string, req), `max_results` (int 1-20, default 5) | TAVILY_API_KEY | synthesized answer + ranked results (title, url, score, snippet) |
| `openai_image` | `prompt` (string, req), `size` (1024x1024 default / 1024x1536 / 1536x1024 / auto) | OPENAI_API_KEY | writes a PNG to `output/` and returns the file path |
| `cross_check` | `model` (string, req), `prompt` (string, req) | GEMINI_API_KEY or GROQ_API_KEY | a NON-Claude model's answer (different-model-family second opinion) |

`cross_check` routing: a `model` starting with `gemini` (e.g. `gemini-2.5-flash`) goes to
Gemini; anything else is treated as a Groq model id (e.g. `llama-3.3-70b-versatile`). This is
the doctrine's anti-monoculture lever -- the standing `harsh-reviewer` judge is itself Claude
(same family), so a non-Claude opinion catches shared blind spots. The hub weighs the answer;
it is not an authority.

## Registration

Registered for Claude Code in the repo-root `.mcp.json`:

```json
{
  "mcpServers": {
    "fleet-tools": { "command": "node", "args": ["apps/fleet-tools-mcp/server.mjs"] }
  }
}
```

After install (`npm install` in this directory), restart Claude Code so it spawns the server.
The three tools then appear natively.

## Security (CWE-214 + secret residency)

- Keys NEVER appear in argv: the server makes in-process `fetch` calls with the key in a
  request header, so there is no child-process argument list to leak.
- Keys NEVER logged: stderr logs exclude key values; error text is run through `redact()`.
- Keys read PER-CALL (only the one key a tool needs) from `~/.config/api-keys/keys.env` via
  `os.homedir()` (portable Lenovo `edusc` / Ryzen `Vgit`) -- not all keys loaded resident for
  the session.
- The Gemini key travels in the `x-goog-api-key` header, never in the URL query string.

## Cost / quality knob

`openai_image` hardcodes `quality: "medium"` (about $0.04-0.07 per image). Change it in
`server.mjs` (the `openaiImage` body) to `low` (cheaper) or `high` (pricier). The 2-arg tool
surface (`prompt`, `size`) deliberately does not expose quality.

## Drift owner

Provider model ids and API shapes drift (e.g. Gemini model names, Groq model availability).
This server has a single owner; if a tool starts failing, check the provider's current model
id / endpoint first. Keep the dependency surface minimal (one direct dep: the MCP SDK; native
fetch otherwise) to limit that drift. The SDK pulls ~90 transitive packages (including an HTTP
transport unused on stdio) -- that footprint is the SDK's, not this server's code.

## Smokes

- Keyless protocol smoke (CI-safe, verifies the server lists the 3 tools):
  `npm run smoke:protocol`
- Live functional smoke (manual; hits real APIs; `openai_image` costs money):
  `npm run smoke:live -- [tavily|image|gemini|groq|all]`
- Offline unit tests (keys parser + redaction): `npm test`

## Files

- `server.mjs` -- tools + stdio server + Windows-safe ESM entry guard.
- `keys.mjs` -- per-call key reader + `redact()`.
- `keys.test.mjs` -- offline unit tests.
- `smoke/protocol.mjs` -- keyless protocol smoke.
- `smoke/live.mjs` -- keyed live smoke harness.
- `output/` -- generated images (gitignored).
