import { test } from "node:test";
import assert from "node:assert/strict";
// Importing server.mjs must NOT start the stdio transport (entry guard) -- if this import
// hangs or crashes, the argv[1] entry guard is broken.
import { scrubSecrets, TOOLS } from "./server.mjs";

test("scrubSecrets removes Bearer tokens and known key prefixes", () => {
  assert.equal(scrubSecrets("Groq 401: Bearer gsk_abc123DEF"), "Groq 401: Bearer [REDACTED]");
  assert.equal(scrubSecrets("leaked tvly-secret999 here"), "leaked tvly-[REDACTED] here");
  assert.equal(scrubSecrets("AIzaXYZ123 token"), "AIza[REDACTED] token");
});

test("server exports exactly the three scoped tools", () => {
  assert.deepEqual(TOOLS.map((t) => t.name).sort(), ["cross_check", "openai_image", "tavily_search"]);
});
