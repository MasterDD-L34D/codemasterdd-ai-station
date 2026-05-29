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

test("redact strips secret embedded mid-string with surrounding context", () => {
  assert.equal(
    redact("ERROR: auth Bearer sk-LIVE-7777 failed", "sk-LIVE-7777"),
    "ERROR: auth Bearer [REDACTED] failed",
  );
});
