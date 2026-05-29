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
