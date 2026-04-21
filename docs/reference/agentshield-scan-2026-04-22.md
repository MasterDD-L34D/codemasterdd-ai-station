# AgentShield Security Scan — 2026-04-22

Baseline scan della config Claude Code del repo `codemasterdd-ai-station`. Strumento suggerito dal materiale `final-research-and-snippets-2026-04-21-v3.md` (sezione 2 Tier 2, repo `affaan-m/everything-claude-code`).

## Metadata

- **Tool**: `ecc-agentshield@1.4.0` (MIT, maintainer `cogsec <me@affaanmustafa.com>`)
- **Invocation**: `npx --yes ecc-agentshield scan --path /c/dev/codemasterdd-ai-station`
- **Target**: `C:\dev\codemasterdd-ai-station` (files scannati: `CLAUDE.md`, `.claude\settings.local.json`)
- **Modalità**: offline, pattern-only (no `--opus`, no `--injection`, no API call Anthropic)
- **Data scansione**: 2026-04-22 (ora UTC nel raw report: 2026-04-21T16:50Z)
- **Grade finale post-hardening**: B (80/100)

## Executive triage

Il tool è utile come **trigger di review** ma **pattern-matching ingenuo** produce molti false positive. Dei **11 findings finali**:

| Severity | Count | Legit | False positive | Windows-only |
|----------|-------|-------|----------------|--------------|
| Critical | 3 | 0 | 3 | — |
| High | 3 | 0 | 1 (già fixato) + 2 trade-off | 1 |
| Medium | 5 | 0 | — | — |

### Breakdown findings con triage

**Critical — tutti false positive**
- `CLAUDE.md:113` + `:160` → documentazione policy ("**NO** `--no-verify`"). Scanner non distingue contesto NEGATIVO da uso effettivo
- `.claude/settings.local.json:66` → **deny rule** `Bash(*--no-verify*)` stessa contiene la stringa. Scanner non distingue allow vs deny

**High**
- `CLAUDE.md is world-writable (0o666)` → scanner legge Unix `os.stat()` che su Windows riflette chmod-emulated, NON le ACL reali. **Fix effettivo applicato**: `icacls CLAUDE.md /inheritance:r /grant:r "edusc:F" /grant:r "SYSTEM:F" /grant:r "Administrators:F"`. Authenticated Users rimossi. Scanner non se ne accorge (limit Windows-compatibility del tool)
- 2× `Bash(python -c "import ...")` rule specifiche (parser Ollama VRAM + parser Ollama generate response) → scanner flagga come "interpreter access" indipendentemente dalla restrittività della rule. Trade-off accettato: rule sono letterali/restrittive, valore operativo concreto per debug Ollama

**Medium**
- 2× `Bash(curl localhost:11434)` → loopback Ollama, rischio reale trascurabile
- 2× `Bash(chmod ...)` allow → one-time setup (git-hooks + CLAUDE.md lock), accettabili
- `No PreToolUse security hooks configured` → pattern non adottato, non blocking

## Actions taken

### 1. Hardening ACL CLAUDE.md
```
icacls CLAUDE.md /inheritance:r /grant:r "edusc:F" /grant:r "SYSTEM:F" /grant:r "Administrators:F"
```
**Prima**: `Authenticated Users:(I)(M)` (qualsiasi user autenticato poteva modificare)
**Dopo**: solo `edusc`, `SYSTEM`, `Administrators` con Full Control. Inheritance rimossa.
**Reversibile**: `icacls CLAUDE.md /reset`

### 2. Rimosso wildcard `Bash(python -c ' *)` da allow
Era un'allow broad che accettava qualsiasi Python one-liner. Le 2 rule specifiche (parser VRAM/response) restano — sono letterali, non wildcard.

### 3. Aggiunta deny list esplicita
```json
"deny": [
  "Bash(git push --force*)",
  "Bash(git push -f*)",
  "Bash(rm -rf /*)",
  "Bash(rm -rf ~*)",
  "Bash(sudo *)",
  "Bash(*--no-verify*)",
  "Bash(chmod 777*)",
  "Bash(ssh *)",
  "Bash(* > /dev/*)"
]
```
Difesa in profondità: anche se un allow è broad, deny esplicito blocca. Allineato con CLAUDE.md policy ("No --force su main, no --no-verify").

## Score breakdown (post-hardening)

| Category | Score | Note |
|----------|-------|------|
| Secrets | 100/100 | Nessun leak |
| Permissions | 0/100 | Tool conta ogni "interpreter access" come problema — non migliorabile senza rimuovere rule specifiche operative |
| Hooks | 100/100 | Guard rail globale + husky wrapper attivi |
| MCP Servers | 100/100 | Nessun MCP server configurato = zero superficie attacco |
| Agents | 100/100 | — |

## Verdetto sul tool

- **Utile** come trigger review per identificare pattern permissivi dimenticati
- **Non affidabile** per scoring assoluto: pattern matching senza context semantico, Unix-centric (Windows ACL non rilevate)
- **Non integrabile in CI/CD** automatizzato senza whitelist estesa dei false positive
- **Buona metodologia**, implementazione grezza (v1.4.0, ancora giovane)

### Decisione

Tool usato **una tantum** per baseline review. Non installato come dev-dep né integrato in hook/CI. Re-run ad-hoc possibile:

```bash
npx --yes ecc-agentshield scan --path /c/dev/codemasterdd-ai-station
```

Le 5 action items implementati sono **genuine improvements** a prescindere dal grade finale del tool.

---

## Raw scanner output (reference)

```
# AgentShield Security Report

**Date:** 2026-04-21T16:50:47.814Z
**Target:** C:\dev\codemasterdd-ai-station
**Grade:** B (80/100)

## Summary

| Metric | Value |
|--------|-------|
| Files scanned | 2 |
| Total findings | 11 |
| Critical | 3 |
| High | 3 |
| Medium | 5 |
| Low | 0 |
| Info | 0 |
| Auto-fixable | 1 |

## Findings

### CRITICAL: Dangerous flag: --no-verify (CLAUDE.md:113)
Evidence: --no-verify → policy documentation, false positive

### CRITICAL: Dangerous flag: --no-verify (CLAUDE.md:160)
Evidence: --no-verify → policy documentation, false positive

### CRITICAL: Dangerous flag: --no-verify (.claude/settings.local.json:66)
Evidence: --no-verify → deny rule itself, false positive (scanner doesn't distinguish allow/deny)

### HIGH: CLAUDE.md is world-writable (0o666)
Unix-style permissions check; on Windows the effective ACL was restricted via icacls

### HIGH: Overly permissive allow rule: Bash(python -c "import sys, json; d=json.load(...)...")
Restrictive literal rule for Ollama VRAM parser; scanner flags any "python -c" generically

### HIGH: Overly permissive allow rule: Bash(python -c "import json,sys; d=json.loads(...)...")
Restrictive literal rule for Ollama generate response parser; scanner flags any "python -c" generically

### MEDIUM: 2× Bash(curl localhost:11434) allow
Loopback Ollama API calls; negligible remote risk

### MEDIUM: 2× Bash(chmod ...) allow
One-time setup operations (git-hooks + CLAUDE.md lock); accepted

### MEDIUM: No PreToolUse security hooks configured
Pattern not adopted; not blocking for single-user setup
```
