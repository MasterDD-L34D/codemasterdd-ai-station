# Aider wrappers (canonical, repo-tracked)

Risolve harsh-reviewer P1 #4 wrapper bus-factor (PR #80+#81 cluster review 2026-05-13).

## Contesto

Pre-2026-05-13 i 6 wrapper Aider vivevano solo `~/.local/bin/*.cmd` user-side: NO IaC, no installer, no recovery se workstation crash. Bus-factor 1.

Post-fix questa directory (`scripts/wrappers/`) contiene la versione **canonical repo-tracked** dei 6 wrapper. Install/sync via `scripts/setup/install-wrappers.ps1` (idempotente, hash-verified, backup-on-conflict).

## Wrapper attivi (8 totale -- 6 cluster T1 SPRINT_02 + 2 free-LLM audit 2026-05-15)

| Wrapper | Tier | Stack | Default invocation status | Mitigation flags |
|---------|------|-------|---------------------------|------------------|
| `aider-cosmetic.cmd` | 1 sovereign | Qwen 7B local + diff | NON_COMPLIANT whole format (entry #27) | Updated 2026-05-13: `whole->diff` + `--no-auto-commits` -- entry #34 PASS |
| `aider-refactor.cmd` | 1-2 sovereign | Qwen 14B Q2 local + diff | PASS constraint=1 default (entry #30) | Multi-block: decompose pattern in single-block sequential edits |
| `aider-cerebras.cmd` | 3 cloud free | Cerebras llama3.1-8b + diff | FAIL context overflow 8k | Required `--map-tokens 0` -- entry #31 PASS $0.00038 |
| `aider-gemini.cmd` | 3 cloud free | Gemini 2.5 Flash + diff | FAIL 24k tok ignora flag | Required `--map-tokens 0 --no-stream` -- entry #32 PASS $0.0078 |
| `aider-openai.cmd` | 4 cloud paid | gpt-4o-mini + diff | FAIL quota=0 originale | Post 10 EUR funding + Sharing toggle ON = pool free 2.5M tok/day -- viable |
| `aider-groq-bypass.cmd` | 3 cloud free | Groq llama-3.3-70b via openai/ | FAIL "Invalid API Key" senza env-file override | Temp env-file pattern P0 hardened (NTFS-protected, NOT in argv) -- entry #36 PASS |
| `aider-hf.cmd` | 3 cloud free | HF Inference Providers, DeepSeek-R1:fastest default | PROPOSED (free-LLM audit 2026-05-15, no bench entry) | `--map-tokens 0 --no-stream` + temp env-file (HUGGINGFACE_API_KEY, CWE-214 hardened) |
| `aider-github-models.cmd` | 3 cloud free | GitHub Models, gpt-4o-mini (150 req/day free PAT) | PROPOSED (endpoint corretto models.github.ai/inference) | `--map-tokens 0 --no-stream` + temp env-file (GITHUB_MODELS_API_KEY) |

## DEPRECATED removed

- `aider-groq.cmd` (LiteLLM Groq adapter buggy, GitHub Issues #9296+#12660+#4804+#16040 streaming hang). DELETED 2026-05-13 user-side. Use `aider-groq-bypass.cmd` invece.

## Install/Sync workflow

### Da Eduardo workstation (post-clone repo)

```powershell
cd C:\dev\codemasterdd-ai-station
.\scripts\setup\install-wrappers.ps1
```

### Idempotente (safe re-run)
- Hash SHA256 verify pre-overwrite
- Skip se hash match (already installed)
- Backup `.bak.YYYY-MM-DD-HHMMSS` se hash differ + hand-edit detected
- `-Force` flag override (perde hand-edits)
- `-DryRun` flag mostra senza copy

### Pre-req
- Privacy whitelist `~/.config/aider-privacy-whitelist.txt` (creato via `scripts/setup/install-privacy-guard.ps1`)
- API keys `~/.config/api-keys/keys.env` (manual setup, ACL-hardened SYSTEM:(F) + edusc:(F))
- `~/.aider.conf.yml` con `env-file: keys.env` directive

## Cross-references

- ADR-0008: silent-corruption-class fail mode (formato whole vs diff)
- ADR-0011: cross-agent commit governance (commit-prompt + git-commit-verify)
- ADR-0013: tier 3 cloud free providers
- ADR-0016: constraint-count routing dimension (decompose pattern)
- ADR-0022: OpenCode tool-use routing (tier separato da Aider)
- ADR-0023: strategic tier post-Max API on-demand + privacy guard rail H8
- ADR-0026: cognitive workflow protocols (Protocol 5 harsh-reviewer su cluster)
- ADR-0029: OpenRouter eval Decline (sovereign-first BYOK pattern)
- L-2026-05-014: Autoresearch FIRST pattern (caso TIM AGTHP + caso aider-groq bypass)
- L-2026-05-015: PowerShell `&` invocation REM pollution -- fix Option B applied a 6 wrapper

## Last update

2026-06-30: README sync drift fix -- aggiunti `aider-hf` + `aider-github-models` al matrix (esistono da `c04f3e5` 2026-05-15, README era fermo a 6). Install script gia' data-driven (glob `*.cmd`) -> nessun gap funzionale, solo doc.

2026-05-13: harsh-reviewer P1 #4 fix shipped via PR #84 (placeholder fino merge):
- Move 6 wrapper canonical from user-side to `scripts/wrappers/`
- Idempotent install script `scripts/setup/install-wrappers.ps1`
- README documenting wrapper matrix + install workflow
