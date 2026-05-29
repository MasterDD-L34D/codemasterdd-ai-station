# fleet-tools MCP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a scoped stdio MCP server exposing three tools the hub lacks or needs a different model for -- `tavily_search`, `openai_image`, `cross_check` -- and register it in Claude Code.

**Architecture:** Single Node ESM stdio server using the official `@modelcontextprotocol/sdk` low-level `Server` API with JSON-Schema tool defs (1 direct dependency -- no zod import, minimal drift). Native `fetch` for all three provider APIs. Tool handlers are exported so smokes can import them; the stdio transport only starts when run as the entry point (Windows-safe ESM guard, L-038). Keys read per-call from `~/.config/api-keys/keys.env`, never in argv or logs.

**Tech Stack:** Node 24 ESM, `@modelcontextprotocol/sdk`, native fetch/AbortController, `node:test` for offline unit tests.

**Spec:** `docs/superpowers/specs/2026-05-29-fleet-tools-mcp-design.md`

---

### Task 1: Scaffold package

**Files:**
- Create: `apps/fleet-tools-mcp/package.json`
- Create: `apps/fleet-tools-mcp/.gitignore`

- [ ] **Step 1: Create package.json**

```json
{
  "name": "fleet-tools-mcp",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "description": "Scoped MCP server: Tavily search, OpenAI image gen, non-Claude cross-check judge.",
  "bin": { "fleet-tools-mcp": "server.mjs" },
  "scripts": {
    "start": "node server.mjs",
    "test": "node --test",
    "smoke:protocol": "node smoke/protocol.mjs",
    "smoke:live": "node smoke/live.mjs"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.12.0"
  },
  "engines": { "node": ">=18" }
}
```

- [ ] **Step 2: Create .gitignore**

```
node_modules/
output/
```

- [ ] **Step 3: Install the SDK**

Run: `cd apps/fleet-tools-mcp && npm install`
Expected: creates `node_modules/` + `package-lock.json`, "added N packages" with no error. (If `^1.12.0` is unavailable, npm picks the latest 1.x; the lockfile pins exact.)

- [ ] **Step 4: Commit**

```
git add apps/fleet-tools-mcp/package.json apps/fleet-tools-mcp/.gitignore apps/fleet-tools-mcp/package-lock.json
```
Commit subject: `chore(fleet-tools): scaffold mcp package`

---

### Task 2: keys.mjs (per-call key reader) + offline unit tests

**Files:**
- Create: `apps/fleet-tools-mcp/keys.mjs`
- Test: `apps/fleet-tools-mcp/keys.test.mjs`

- [ ] **Step 1: Write keys.mjs**

```js
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

// Default location of the fleet key file. Portable across Lenovo (edusc) / Ryzen (Vgit).
export const KEYS_PATH = join(homedir(), ".config", "api-keys", "keys.env");

// Read ONE key value, lazily, per call. Never logs the value.
// filePath param exists only so tests can point at a temp file.
export function readKey(name, filePath = KEYS_PATH) {
  let raw;
  try {
    raw = readFileSync(filePath, "utf8");
  } catch (e) {
    throw new Error(`cannot read keys file at ${filePath}: ${e.code || e.message}`);
  }
  for (const line of raw.split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith("#")) continue;
    const eq = t.indexOf("=");
    if (eq === -1) continue;
    if (t.slice(0, eq).trim() !== name) continue;
    let v = t.slice(eq + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    }
    if (v) return v;
    break;
  }
  throw new Error(`key ${name} not found in ${filePath}`);
}

// Remove any secret substring from text before logging/returning.
export function redact(text, ...secrets) {
  let out = String(text);
  for (const s of secrets) {
    if (s && s.length >= 6) out = out.split(s).join("[REDACTED]");
  }
  return out;
}
```

- [ ] **Step 2: Write keys.test.mjs (failing first)**

```js
import { test } from "node:test";
import assert from "node:assert/strict";
import { writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { readKey, redact } from "./keys.mjs";

function tmpKeys(contents) {
  const dir = mkdtempSync(join(tmpdir(), "ft-keys-"));
  const f = join(dir, "keys.env");
  writeFileSync(f, contents);
  return f;
}

test("readKey returns value, ignores comments, strips quotes", () => {
  const f = tmpKeys('# c\nFOO=bar123\nBAZ="q u x"\n');
  assert.equal(readKey("FOO", f), "bar123");
  assert.equal(readKey("BAZ", f), "q u x");
});

test("readKey throws on missing key", () => {
  const f = tmpKeys("FOO=bar\n");
  assert.throws(() => readKey("NOPE", f), /not found/);
});

test("readKey throws on missing file", () => {
  assert.throws(() => readKey("FOO", "/no/such/file.env"), /cannot read keys file/);
});

test("redact removes secret of length >= 6", () => {
  assert.equal(redact("k=abcdef123 z", "abcdef123"), "k=[REDACTED] z");
  assert.equal(redact("short=abc", "abc"), "short=abc"); // too short, untouched
});
```

- [ ] **Step 3: Run tests, expect PASS**

Run: `cd apps/fleet-tools-mcp && node --test`
Expected: `# pass 4  # fail 0`.

- [ ] **Step 4: Commit**

```
git add apps/fleet-tools-mcp/keys.mjs apps/fleet-tools-mcp/keys.test.mjs
```
Commit subject: `feat(fleet-tools): per-call key reader with redaction`

---

### Task 3: server.mjs (3 tools, registry, entry guard) + keyless protocol smoke

**Files:**
- Create: `apps/fleet-tools-mcp/server.mjs`
- Create: `apps/fleet-tools-mcp/smoke/protocol.mjs`

- [ ] **Step 1: Write server.mjs**

```js
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { readKey, redact } from "./keys.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = join(HERE, "output");
const log = (...a) => process.stderr.write(`[fleet-tools] ${a.join(" ")}\n`);

// ---- shared HTTP helper ----
async function postJson(url, { headers = {}, body, timeoutMs }) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "content-type": "application/json", ...headers },
      body: JSON.stringify(body),
      signal: ctrl.signal,
    });
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch { /* leave null */ }
    return { ok: res.ok, status: res.status, json, text };
  } finally {
    clearTimeout(timer);
  }
}

const ok = (text) => ({ content: [{ type: "text", text }] });
const fail = (text) => ({ content: [{ type: "text", text }], isError: true });

// ---- tool: tavily_search ----
export async function tavilySearch({ query, max_results } = {}) {
  if (!query || typeof query !== "string") return fail("ERROR: query is required (string).");
  const n = Math.min(20, Math.max(1, Number.isInteger(max_results) ? max_results : 5));
  const key = readKey("TAVILY_API_KEY");
  const r = await postJson("https://api.tavily.com/search", {
    headers: { authorization: `Bearer ${key}` },
    body: { query, max_results: n, search_depth: "basic", include_answer: true },
    timeoutMs: 30000,
  });
  if (!r.ok) return fail(redact(`ERROR: Tavily ${r.status}: ${r.text}`, key));
  const j = r.json || {};
  const lines = [];
  if (j.answer) lines.push(`ANSWER: ${j.answer}\n`);
  for (const [i, res] of (j.results || []).entries()) {
    lines.push(`${i + 1}. ${res.title} -- ${res.url} (score ${res.score})\n   ${(res.content || "").slice(0, 300)}`);
  }
  return ok(lines.join("\n") || "no results");
}

// ---- tool: openai_image ----
const ALLOWED_SIZES = new Set(["1024x1024", "1024x1536", "1536x1024", "auto"]);
export async function openaiImage({ prompt, size } = {}) {
  if (!prompt || typeof prompt !== "string") return fail("ERROR: prompt is required (string).");
  const sz = ALLOWED_SIZES.has(size) ? size : "1024x1024";
  const key = readKey("OPENAI_API_KEY");
  const r = await postJson("https://api.openai.com/v1/images/generations", {
    headers: { authorization: `Bearer ${key}` },
    // quality hardcoded "medium" (~$0.04-0.07/img); edit here to change cost/quality.
    body: { model: "gpt-image-1", prompt, size: sz, quality: "medium", n: 1 },
    timeoutMs: 120000,
  });
  if (!r.ok) return fail(redact(`ERROR: OpenAI ${r.status}: ${r.text}`, key));
  const d = r.json && r.json.data && r.json.data[0];
  if (!d || !d.b64_json) return fail(redact(`ERROR: no image data in response: ${r.text}`, key));
  mkdirSync(OUTPUT_DIR, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const slug = prompt.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40) || "image";
  const file = join(OUTPUT_DIR, `${stamp}-${slug}.png`);
  writeFileSync(file, Buffer.from(d.b64_json, "base64"));
  const extra = d.revised_prompt ? `\nrevised_prompt: ${d.revised_prompt}` : "";
  return ok(`image saved: ${file}\nsize: ${sz} quality: medium${extra}`);
}

// ---- tool: cross_check ----
export async function crossCheck({ model, prompt } = {}) {
  if (!model || typeof model !== "string")
    return fail("ERROR: model is required, e.g. 'gemini-2.5-flash' (Gemini) or 'llama-3.3-70b-versatile' (Groq).");
  if (!prompt || typeof prompt !== "string") return fail("ERROR: prompt is required (string).");

  if (model.startsWith("gemini")) {
    const key = readKey("GEMINI_API_KEY");
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`;
    const r = await postJson(url, {
      headers: { "x-goog-api-key": key }, // header, not URL query -- key stays out of logs
      body: { contents: [{ parts: [{ text: prompt }] }] },
      timeoutMs: 30000,
    });
    if (!r.ok) return fail(redact(`ERROR: Gemini ${r.status}: ${r.text}`, key));
    const parts = (r.json && r.json.candidates && r.json.candidates[0] && r.json.candidates[0].content && r.json.candidates[0].content.parts) || [];
    const answer = parts.map((p) => p.text || "").join("").trim();
    return ok(`[non-Claude cross-check -- provider: gemini, model: ${model}]\n\n${answer || "(empty answer)"}`);
  }

  // default: Groq (OpenAI-compatible chat completions)
  const key = readKey("GROQ_API_KEY");
  const r = await postJson("https://api.groq.com/openai/v1/chat/completions", {
    headers: { authorization: `Bearer ${key}` },
    body: { model, messages: [{ role: "user", content: prompt }] },
    timeoutMs: 30000,
  });
  if (!r.ok) return fail(redact(`ERROR: Groq ${r.status}: ${r.text}`, key));
  const answer = r.json && r.json.choices && r.json.choices[0] && r.json.choices[0].message && r.json.choices[0].message.content;
  return ok(`[non-Claude cross-check -- provider: groq, model: ${model}]\n\n${(answer || "").trim() || "(empty answer)"}`);
}

// ---- tool registry ----
export const TOOLS = [
  {
    name: "tavily_search",
    description: "Web search via Tavily (richer/alternate to built-in web search). Returns a synthesized answer plus ranked results.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query." },
        max_results: { type: "integer", description: "Max results 1-20 (default 5).", minimum: 1, maximum: 20 },
      },
      required: ["query"],
    },
    handler: tavilySearch,
  },
  {
    name: "openai_image",
    description: "Generate an image with OpenAI gpt-image-1 (the hub cannot generate images). Writes a PNG to disk and returns its path.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "Image description." },
        size: { type: "string", description: "1024x1024 (default), 1024x1536, 1536x1024, or auto.", enum: ["1024x1024", "1024x1536", "1536x1024", "auto"] },
      },
      required: ["prompt"],
    },
    handler: openaiImage,
  },
  {
    name: "cross_check",
    description: "Send a prompt to a NON-Claude model (Gemini or Groq) for a different-model-family second opinion (anti-monoculture). model starting with 'gemini' routes to Gemini; otherwise treated as a Groq model id.",
    inputSchema: {
      type: "object",
      properties: {
        model: { type: "string", description: "e.g. 'gemini-2.5-flash' (Gemini) or 'llama-3.3-70b-versatile' (Groq)." },
        prompt: { type: "string", description: "The prompt / claim to get a non-Claude second opinion on." },
      },
      required: ["model", "prompt"],
    },
    handler: crossCheck,
  },
];

export async function main() {
  const server = new Server({ name: "fleet-tools", version: "0.1.0" }, { capabilities: { tools: {} } });
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: TOOLS.map(({ name, description, inputSchema }) => ({ name, description, inputSchema })),
  }));
  server.setRequestHandler(CallToolRequestSchema, async (req) => {
    const tool = TOOLS.find((t) => t.name === req.params.name);
    if (!tool) return fail(`ERROR: unknown tool ${req.params.name}`);
    try {
      return await tool.handler(req.params.arguments || {});
    } catch (e) {
      return fail(`ERROR: ${e.message}`);
    }
  });
  await server.connect(new StdioServerTransport());
  log("fleet-tools MCP server started (stdio)");
}

// Windows-safe ESM entry guard (L-038: file://${process.argv[1]} literal is POSIX-only).
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((e) => { log("fatal:", e.message); process.exit(1); });
}
```

- [ ] **Step 2: Write smoke/protocol.mjs (keyless -- verifies MCP wiring + entry guard fires)**

```js
// Keyless protocol smoke: spawn the server over stdio, list tools, assert the 3 names.
// Verifies OUTPUT (not just exit code) per L-038.
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const transport = new StdioClientTransport({ command: "node", args: [join(here, "..", "server.mjs")] });
const client = new Client({ name: "protocol-smoke", version: "0.0.0" }, { capabilities: {} });

await client.connect(transport);
const { tools } = await client.listTools();
const names = tools.map((t) => t.name).sort();
console.log("tools listed:", names.join(", "));
await client.close();

const expected = ["cross_check", "openai_image", "tavily_search"];
if (JSON.stringify(names) !== JSON.stringify(expected)) {
  console.error("FAIL: expected", expected.join(", "));
  process.exit(1);
}
console.log("PROTOCOL SMOKE PASS");
```

- [ ] **Step 3: Run protocol smoke, expect PASS**

Run: `cd apps/fleet-tools-mcp && node smoke/protocol.mjs`
Expected output:
```
tools listed: cross_check, openai_image, tavily_search
PROTOCOL SMOKE PASS
```
Exit code 0. (If it hangs or prints nothing, the entry guard did not fire -- check the pathToFileURL guard.)

- [ ] **Step 4: Re-run unit tests (regression)**

Run: `cd apps/fleet-tools-mcp && node --test`
Expected: `# pass 4  # fail 0` (server.mjs import must not break the offline tests; it should not, since handlers do not call network at import time).

- [ ] **Step 5: Commit**

```
git add apps/fleet-tools-mcp/server.mjs apps/fleet-tools-mcp/smoke/protocol.mjs
```
Commit subject: `feat(fleet-tools): three tools + stdio server + protocol smoke`

---

### Task 4: Live functional smoke harness + tavily_search smoke

**Files:**
- Create: `apps/fleet-tools-mcp/smoke/live.mjs`

- [ ] **Step 1: Write smoke/live.mjs**

```js
// Live functional smoke -- imports handlers directly, hits real APIs. Manual run (costs money:
// openai_image ~ $0.04-0.07). Usage: node smoke/live.mjs [tavily|image|gemini|groq|all]
import { tavilySearch, openaiImage, crossCheck } from "../server.mjs";

const which = process.argv[2] || "all";
const run = async (label, p) => {
  const res = await p;
  const text = res.content.map((c) => c.text).join("\n");
  console.log(`\n===== ${label} ${res.isError ? "(isError)" : ""} =====\n${text}`);
  if (res.isError) process.exitCode = 1;
};

if (which === "tavily" || which === "all")
  await run("tavily_search", tavilySearch({ query: "what is the Model Context Protocol", max_results: 3 }));
if (which === "image" || which === "all")
  await run("openai_image", openaiImage({ prompt: "a tiny pixel-art robot mascot, flat colors", size: "1024x1024" }));
if (which === "gemini" || which === "all")
  await run("cross_check/gemini", crossCheck({ model: "gemini-2.5-flash", prompt: "Reply with exactly: FLEET_CROSS_OK" }));
if (which === "groq")
  await run("cross_check/groq", crossCheck({ model: "llama-3.3-70b-versatile", prompt: "Reply with exactly: FLEET_GROQ_OK" }));
```

- [ ] **Step 2: Run tavily smoke, cite output**

Run: `cd apps/fleet-tools-mcp && node smoke/live.mjs tavily`
Expected: an `ANSWER:` line and 3 numbered results with URLs about MCP, no `(isError)`. If `isError`, read the redacted status (e.g. 401 -> key; 432/usage -> Tavily plan) and fix before proceeding.

- [ ] **Step 3: Commit the harness**

```
git add apps/fleet-tools-mcp/smoke/live.mjs
```
Commit subject: `test(fleet-tools): live smoke harness`

(No code change expected from the tavily smoke; if a bug surfaces, fix server.mjs in this commit.)

---

### Task 5: openai_image live smoke

- [ ] **Step 1: Run image smoke, cite output**

Run: `cd apps/fleet-tools-mcp && node smoke/live.mjs image`
Expected: `image saved: <...>/output/<stamp>-a-tiny-pixel-art-robot...png` and `size: 1024x1024 quality: medium`, no `(isError)`.

- [ ] **Step 2: Verify the PNG exists and is non-empty**

Run (PowerShell): `Get-ChildItem apps/fleet-tools-mcp/output/*.png | Select-Object Name,Length`
Expected: at least one `.png` with Length > 10000 bytes.

- [ ] **Step 3: If a bug surfaced, fix server.mjs and commit; else no commit**

(Only commit if server.mjs changed. Subject: `fix(fleet-tools): <what> in openai_image`.)

---

### Task 6: cross_check live smoke (Gemini, required; Groq optional)

- [ ] **Step 1: Run Gemini cross_check smoke, cite output**

Run: `cd apps/fleet-tools-mcp && node smoke/live.mjs gemini`
Expected: `[non-Claude cross-check -- provider: gemini, model: gemini-2.5-flash]` followed by `FLEET_CROSS_OK` (or close), no `(isError)`.
If 404 on the model name, the Gemini model id drifted -- try `gemini-2.0-flash` / `gemini-1.5-flash` and note the working id in README.

- [ ] **Step 2: Optional Groq route check (path already passed 2026-05-29 per eval)**

Run: `cd apps/fleet-tools-mcp && node smoke/live.mjs groq`
Expected: `provider: groq` + `FLEET_GROQ_OK`. Optional; document if run.

- [ ] **Step 3: If a bug surfaced, fix server.mjs and commit; else no commit**

(Only commit if server.mjs changed.)

---

### Task 7: README + .mcp.json registration + ORCHESTRATION.md doc-sync

**Files:**
- Create: `apps/fleet-tools-mcp/README.md`
- Create: `.mcp.json` (repo root)
- Modify: `ORCHESTRATION.md` (stale `llm_call` reference)

- [ ] **Step 1: Write README.md**

Content must cover: the three tools + their args, the keys each needs, how it is registered (`.mcp.json`), security (keys per-call, never argv/logs, Gemini header-not-URL), the quality knob location in server.mjs, the drift-owner note (provider model ids/APIs can drift -- single owner), and how to run smokes (`npm run smoke:protocol` keyless, `npm run smoke:live` keyed/costs money). ASCII-first body.

- [ ] **Step 2: Create root .mcp.json**

```json
{
  "mcpServers": {
    "fleet-tools": {
      "command": "node",
      "args": ["apps/fleet-tools-mcp/server.mjs"]
    }
  }
}
```

- [ ] **Step 3: Fix the stale llm_call reference in ORCHESTRATION.md**

In the "Cloud keys" spoke row (around line 24), the phrase `or \`llm_call\` (MCP llm-fleet once built)` refers to the REJECTED design. Replace it with a reference to the built fleet-tools tools, e.g. `; fleet-tools MCP (\`tavily_search\`/\`openai_image\`/\`cross_check\`) for services + non-Claude cross-check`. Do NOT alter sec 7 (it already states fleet-tools GO); optionally append "(built 2026-05-29)" to its fleet-tools bullet.

Run after editing: `git grep -n "llm_call" ORCHESTRATION.md`
Expected: only the sec-7 REJECTED-design mention(s) remain (which are correct -- they document the rejection); the routing-table "once built" promise is gone.

- [ ] **Step 4: Commit**

```
git add apps/fleet-tools-mcp/README.md .mcp.json ORCHESTRATION.md
```
Commit subject: `feat(fleet-tools): register mcp + readme + doctrine sync`

---

### Task 8: harsh-reviewer pass on the final minimal design (SDMG step)

- [ ] **Step 1: Dispatch the harsh-reviewer subagent**

Use the Agent tool, `subagent_type: harsh-reviewer`, read-only. Provide: the spec path, the plan path, and the final files (`apps/fleet-tools-mcp/server.mjs`, `keys.mjs`, `package.json`, `.mcp.json`). Ask for P0/P1/P2 findings on: secret handling (CWE-214), error/timeout handling, MCP protocol correctness, drift surface, scope creep vs the 3-tool mandate, and the doc-sync.

- [ ] **Step 2: Integrate findings**

P0 -> must fix now. P1 -> fix now or document a defer with rationale. P2 -> acknowledge. Make fixes in `server.mjs`/`keys.mjs`/README as needed; re-run `node --test` + `node smoke/protocol.mjs` after any code change (expect still-green output).

- [ ] **Step 3: Commit fixes (if any)**

Commit subject: `fix(fleet-tools): address harsh-reviewer P0/P1` (only if changes were made).

---

### Task 9: PR + autonomy-ladder gate

- [ ] **Step 1: Check for CI**

Run: `git ls-files .github/workflows`
If a Node CI workflow runs on PRs, ensure it will pass (it runs `node --test` + protocol smoke at most -- both keyless). If NO workflow exists, the gate is local smokes + harsh-reviewer + judge per ORCHESTRATION.md sec 4 ("CI where applicable"); do not add CI unless trivial and keyless.

- [ ] **Step 2: Push branch**

Run: `git push -u origin claude/fleet-tools-mcp-2026-05-29`

- [ ] **Step 3: Open PR**

Use `gh pr create` with a body covering: what (3 scoped tools), why (closes discoverability gap for capabilities with real callers; SDMG human-reframe), the SDMG verification evidence (cite the 3 smoke outputs + harsh-reviewer verdict), security (CWE-214 per-call keys), and links to spec + plan + ADR-0036 + the eval. Add the standard generated-with footer.

- [ ] **Step 4: Auto-merge gate (ORCHESTRATION.md sec 5, own repo)**

Own-repo low-risk + reversible: auto-merge iff CI green (or N/A) + harsh-reviewer judge OK + smokes cited. Squash + delete branch. If any gate is red -> stop, report, do not merge.

---

## Notes for the executor

- Run all `node`/`npm` commands from `apps/fleet-tools-mcp/` unless a repo-root path is shown.
- Commit messages: Conventional Commits, subject <= 72 chars, lowercase description, no trailing period; ADR-0011 trailers on every commit:
  ```
  Coding-Agent: claude-opus-4-8
  Trace-Id: <uuid from: node -e "console.log(crypto.randomUUID())">
  ```
  NO `Co-Authored-By`. Use a PowerShell here-string for multiline messages.
- Never print or commit a key value. The smoke `live.mjs` output is safe to cite (it shows model answers / file paths, not keys), but scan before pasting.
- ASCII-first for all new doc/prose (ADR-0021); code files are ASCII too.
