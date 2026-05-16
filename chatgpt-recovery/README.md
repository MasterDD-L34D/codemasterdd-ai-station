# ChatGPT Recovery Workspace -- 2026-05-14

Workspace operazionale per recupero completo ChatGPT Business workspace "Area di lavoro di Master DD Business" -> vault Obsidian.

## Obiettivo

Esportare **tutto** (chat regolari + archiviate, Projects, Custom GPTs config, Memory items, Custom Instructions, files/canvas/images) in singolo bulk run, poi classificare offline.

## Status mapping

| Phase | Tool | Status | Output target |
|---|---|---|---|
| **0. Pre-flight audit** | Manuale UI ChatGPT | `01-PREFLIGHT-AUDIT.md` | counts + decisions matrix |
| **1a. Bulk export conversations + projects + files** | `brianjlacy/export-chatgpt` | runbook `02-bulk-export-runbook.md` | `vault/Sources/raw/chatgpt-export-2026-05-14/` |
| **1b. Memory items** | MemPort Chrome ext | manual step in 02 | `memory-items.csv` |
| **1c. Custom Instructions** | Manual copy | manual step in 02 | `custom-instructions.md` |
| **1d. Custom GPTs config** | `scripts/scrape-custom-gpts.js` Playwright | scaffold ready | `custom-gpts/{slug}/config.md + knowledge/` |
| **2. Staging** | rsync/cp | manual step | `vault/Sources/raw/chatgpt-export-2026-05-14/` |
| **3. Classification** | `pipeline/classify.py` BERTopic + nomic + Qwen 14B Q2 | scaffold ready | topic clusters + atom candidates |
| **4. Vault integration** | `pipeline/atomize.py` + manual MOC | scaffold ready | `vault/Cards/`, `vault/Atlas/MOC-*.md` |

## Privacy posture

100% sovereign per default:
- Bulk export: bearer JWT scope tuo workspace, no 3rd party
- MemPort: 100% browser-local
- Playwright: persistent context tuo profilo Chrome, save locale
- Embeddings: nomic-embed-text via Ollama locale
- Classification: BERTopic Python + Qwen 14B Q2 via Aider/Ollama
- Vault integration: file system locale + Obsidian native

Zero cloud calls default. Cloud opt-in possibile per accelerare labeling (Cerebras llama-70B free), solo se autorizzi esplicitamente e data non-sensitive.

## Execution sequence

```
1. [10 min]  Pre-flight audit UI       -> 01-PREFLIGHT-AUDIT.md (compila)
2. [15 min]  Smoke test brianjlacy     -> verifica output structure
3. [30-60m]  Full bulk export          -> exports/ locale
4. [15 min]  Memory + Instructions     -> CSV + MD
5. [variable] Custom GPTs Playwright  -> scripts/scrape-custom-gpts.js
6. [5 min]   Staging to vault          -> rsync
7. [30-90m]  Classification pipeline   -> topics + atoms
8. [1-3h]    Vault integration final   -> Cards + MOC
```

## File index

- `01-PREFLIGHT-AUDIT.md` — checklist UI ChatGPT da eseguire PRIMA del bulk
- `02-bulk-export-runbook.md` — commands brianjlacy + MemPort + manual steps
- `scripts/scrape-custom-gpts.js` — Playwright stub Option B per Custom GPTs
- `scripts/setup-playwright.ps1` — install Playwright + Chromium
- `scripts/package.json` — Node deps
- `pipeline/classify.py` — BERTopic + nomic + Qwen 14B Q2 labeling
- `pipeline/atomize.py` — per-conversation message extraction -> Cards
- `pipeline/requirements.txt` — Python deps

## Note operative

- Workspace temporaneo, NON commit auto. Eduardo decide se promuovere a vault-shared o archive AA01 post-run.
- Output data destinazione: `vault/Sources/raw/chatgpt-export-2026-05-14/` (Lenovo path `C:/dev/vault-shared/Sources/raw/...` o Ryzen origin path `C:/Users/VGit/Vault/Sources/raw/...` -- vedi lineage reframe 2026-05-12).
- Token bearer ChatGPT ha vita 10gg (rare long-lived). Export resumable (`.export-progress.json`). Refresh + re-run senza re-download.

## Status live (2026-05-15)

**Pivot eseguito**: 2026-05-15 mattina, da regular-first a projects-only fetch (target high-value data Evo-Tactics + Hao Jin + Master DD).

| Phase | Status | Output |
|---|---|---|
| Pre-flight audit (API auto) | ✅ done | audit-result.yaml + cross-reference-map.yaml |
| Memory items (83) + Custom Instructions | ✅ done | memory-items.json + .md + custom-instructions.json + .md |
| Memory atomize → 83 vault-convention Cards | ✅ done | `_processed/memory/Cards/` + INDEX.md |
| Bulk regular+archived (661/1264 frozen) | 🟡 pivot-paused | Sources/json/, markdown/, files/ |
| **Bulk projects (12 target, Evo-Tactics first)** | 🔵 in progress | task `btf9fsv0h`, 1/12 projects (Evo-Tactics ~6/541 conv at slow pace) |
| Partial classify 661 → 25 topic | ✅ done | `test-fixtures/partial-classification-661/` |
| Partial atomize 18,194 Cards | ✅ done | `test-fixtures/partial-cards-661/` |
| MOC stub + entity index + collisions + review-sample | ✅ done | `test-fixtures/*.md` |
| 7 agent specialist invocati (harsh + OWASP + adr + privacy + Explore + Plan x2) | ✅ done | `agent-lessons-2026-05-14.md` + 4 P0 + 6 P1 fix applicati |
| ADR-0030 + DECISIONS_LOG retrocover | ✅ done | `docs/adr/0030-chatgpt-recovery-classification-pipeline.md` |
| Phase 4 final classify+atomize on full target | ⏳ pending bulk completion | TBD post-projects |
| Phase 5 remaining 603 regular (no-flag restart) | ⏳ pending Phase 4 | TBD |

## Pipeline scripts inventory

- `pipeline/classify.py` (BERTopic + nomic + Qwen 14B Q2, tuned UMAP+HDBSCAN)
- `pipeline/atomize.py` (per-message Cards vault-convention)
- `pipeline/atomize-memory.py` (memory items con PII tags + canonical_audience)
- `pipeline/sample-cards.py` (Plan Phase 4 stratified review)
- `pipeline/promote-cards.py` (Plan Phase 5 selective canonical promotion + dry-run)
- `pipeline/build-moc-stub.py` (Atlas MOC generator)
- `pipeline/extract-entities.py` (proper-noun heuristic taxonomy seed)
- `pipeline/vault-collision-scan.py` (pre-promotion duplicate check)
- `scripts/auto-audit.py` (API-based audit replace manual UI)
- `scripts/fetch-memories-and-instructions.py` (direct API)
- `scripts/scrape-custom-gpts.js` (Playwright Option B, NOT used questo run -- 0 GPTs owned)
- `scripts/setup-playwright.ps1` + `scripts/package.json`
- `scripts/stage-to-vault.ps1` (robocopy + provenance.json)
- `scripts/run-post-export-pipeline.ps1` (orchestrator end-to-end con `-Force`/`-NonInteractive` + trap cleanup)

## Rate limit reality

OpenAI rate limit server-side per-account = bottleneck. Adaptive throttle climbed 8s→60s+ before pivot. Fixed `--throttle 30 --no-adaptive` + 60-120-300s backoff su 429 = ~5 min/conv su project bucket. ETA 45h+ solo per Evo-Tactics 541 conv. Autoresearch confermato no bypass legitimate. Resumable: laptop sleep OK.

## Token security

Bearer JWT salvato in `%TEMP%/chatgpt-bearer.env` con NTFS ACL edusc+SYSTEM, no inheritance. Bearer ANCHE in Claude Code session jsonl (`C:/Users/edusc/.claude/projects/.../session-*.jsonl`) — P0 OWASP da rotate POST-pipeline (logout all sessions + re-login = new bearer). orchestrator ha trap cleanup + stale env-file purge.
