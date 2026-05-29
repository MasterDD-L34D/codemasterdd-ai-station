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
