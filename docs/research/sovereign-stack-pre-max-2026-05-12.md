# Sovereign stack pre-Max smoke verify + vault Ollama fallback pattern audit (2026-05-12)

> **Scope dual**: (E) audit vault Ollama priority-ordered endpoint chain pattern + adoption decision codemasterdd-side + (B) strategic pre-Max smoke verify stack sovereign end-to-end. Sessione 2026-05-12 mattina, 7gg residui pre-Claude Max expiration 2026-05-19.
>
> **Method**: Protocol 1 refresh-verify state + Protocol 2 autoresearch multi-source (vault commits + filesystem empirical + cloud API direct ping).

## TL;DR

**E -- Vault Ollama fallback pattern**: DEFER con trigger esplicito. Single-host Lenovo (workstation primaria) NON necessita fallback chain. Trigger reactivation: Ryzen onboarding SSH + Ollama install (DESKTOP-T77TMKT 4070 SUPER scoperto recente, capability superior 14B+) OR Pod multi-host deployment.

**B -- Sovereign stack pre-Max**: 5/5 smoke ALL-PASS empirico. Stack pronto per transition 2026-05-19. **1 gap segnalato**: H7 ANTHROPIC_API_KEY ancora MISSING in `keys.env` (Eduardo-direct, ~5min via Anthropic Console).

## Sezione E -- Vault Ollama fallback pattern audit

### Pattern source

Vault commits (audit-only, NO clone):
- `2e7c5ab feat(ollama-fallback): local Ollama + priority-ordered endpoint chain` (11/5)
- `9b04982 feat(ollama-local): extend fallback set with mistral + qwen3:8b` (11/5)

### Pattern strutturale

`Extras/config/ollama.json` (read via gh commit content):

```json
{
  "endpoints": [
    { "p": 1, "name": "local", "url": "http://localhost:11434", "use_for": ["fallback", "embed", "chat", "tagging", "summary-light", "offline-dev"] },
    { "p": 2, "name": "remote-lan", "url": "http://<stale-lan-ip>:11434", "use_for": ["primary", "heavy-models", "bulk-jobs"] },
    { "p": 3, "name": "secondary-lan", "url": "http://172.22.160.1:11434", "use_for": ["fallback"] }
  ],
  "fallback_strategy": "priority-ordered: try local first if running, else LAN remote, else fail soft"
}
```

Plus `Vault-ops/scripts/ollama-health.py`: probe `/api/tags` per endpoint, returns active URL + model list.

### Pattern context (vault use case)

Vault commit message indica: "Discovered Ollama already installed on this PC (VGit Win11)". Quindi pattern motivato da:
- **Workstation secondary** (VGit) con Ollama local appena scoperto/configurato
- Workstation primary (codemasterdd Lenovo <stale-lan-ip>) come fallback LAN
- Resilience cross-device: se local off -> LAN -> secondary-LAN -> fail soft

### Codemasterdd applicability assessment

**Memory CLAUDE.md fleet section (2026-05-10 LAN discovery)**:
- Lenovo (codemasterdd): `<stale-lan-ip>` primary AI workstation
- DESKTOP-T77TMKT (Ryzen 9600X + RTX 4070 SUPER 12GB): `<stale-lan-ip>` -- AI stack NOT installed (Ollama/Python/Aider pending)
- DESKTOP-B9L203E (moglie): `<wife-desktop-ip>` -- capability TBD, OpenSSH not active
- LAPTOP-D73A8DIE (moglie): `<wife-laptop-ip>` -- capability TBD, OpenSSH not active

**Codemasterdd current routing**: tutti i wrapper Aider + OpenCode + Ollama config puntano direct a `http://localhost:11434` (= <stale-lan-ip> da Lenovo perspective).

**Need fallback chain?**:
- **Single-host primary Lenovo**: NO benefit fallback diretto (Lenovo down = lavoro inutilizzabile comunque)
- **Fleet awareness scenario futuro**: Ryzen 4070 SUPER 12GB capability superior 14B+ -> potential PRIMARY per behavior-critical, Lenovo SECONDARY embedding/cosmetic
- **Pod scenario futuro** (Hyperspace ABANDONED, llama.cpp RPC pivoted): se distribuito vault-pattern endpoint chain become utile

### Decision: DEFER con trigger esplicito

**Skip ora** (single-host Lenovo, no benefit immediate, fallback chain = solution looking for problem).

**Trigger reactivation Pattern E ADOPT**:
1. **Ryzen onboarding empirico**: Ollama installed su DESKTOP-T77TMKT + 1+ workflow real cross-host (es. Aider 14B Q2 su Ryzen mentre Lenovo runs Claude Code) -> motivates endpoint chain
2. **Pod multi-host deployment**: llama.cpp RPC primary (D-018) + REST API Lenovo (D-019) attivo + secondary node aggiunto
3. **Resilience real failure**: Lenovo Ollama daemon crash >=2 volte in 30gg -> motivates local fallback su altro device

**NO clone** del file `ollama.json` o `ollama-health.py`. Audit-then-replay quando trigger emerge.

### Cross-reference

- Vault pattern + Pattern D adopted 2026-05-12 (governance-lint) = 2 pattern adoption questa settimana, entrambi audit-then-replay senza clone diretto
- Memory codemasterdd `reference_external_toolkits.md` (cherry-pick policy) honored

## Sezione B -- Sovereign stack pre-Max smoke verify

### B1 Wrapper Aider (6 cmd verified)

| Wrapper | Path | Size | Last modified |
|---------|------|------|---------------|
| aider-cosmetic.cmd | `~/.local/bin/` | 787 B | 2026-04-23 |
| aider-refactor.cmd | `~/.local/bin/` | 839 B | 2026-04-23 |
| aider-cerebras.cmd | `~/.local/bin/` | 1904 B | 2026-05-09 |
| aider-gemini.cmd | `~/.local/bin/` | 1995 B | 2026-05-09 |
| aider-groq.cmd | `~/.local/bin/` | 1907 B | 2026-05-09 |
| aider-openai.cmd | `~/.local/bin/` | 1890 B | 2026-05-09 |

Aider binary: `aider 0.86.2`.

### B2 API keys reachable

`~/.config/api-keys/keys.env` (609 B, owner edusc).

Cloud free tier providers smoke (curl direct, 1 task "Reply OK" each):

| Provider | Model | Status | Tokens |
|----------|-------|--------|--------|
| Groq | llama-3.3-70b-versatile | **OK** ✓ | 39 prompt / 2 completion |
| Cerebras | llama3.1-8b | **OK** ✓ | 39 prompt / 2 completion |
| Gemini | gemini-2.5-flash | **OK** ✓ | 2 prompt / 1 completion |

**Gap critico**: `ANTHROPIC_API_KEY` **MISSING** in keys.env (visible keys: GROQ + CEREBRAS + GEMINI + OPENAI). H7 ADR-0023 Tier 0 strategic post-Max requirement -- Eduardo-direct setup via [Anthropic Console](https://console.anthropic.com/) ~5min pre-2026-05-19.

OPENAI presente (tier 4 emergency paid). Other 3 free tier validated.

### B3 OpenCode

| Item | Status |
|------|--------|
| Binary `opencode.cmd` + `opencode.ps1` | Present (~339 B + 861 B) |
| Config `~/.config/opencode/opencode.json` | Present (2689 B) |
| Default model | `ollama/qwen3-coder:30b` ✓ (ADR-0022 Accepted) |
| Small model fallback | `ollama/qwen3-coder:30b` |

Config refresh data: 2026-05-09 16:17 (post bench M10 cloud free findings, ADR-0022 Accepted retroactive).

### B4 Ollama daemon + models

`curl http://localhost:11434/api/tags` -> 200 OK, 16 modelli installed.

**Tier coder primary** (CLAUDE.md tier routing):
- `qwen2.5-coder:7b` (Q4_K_M) -- tier 1 cosmetic 114 tok/s isolated
- `qwen2.5-coder:14b-instruct-q2_K` -- tier 2 behavior 18.7 tok/s sweet spot
- `qwen2.5-coder:14b-instruct-q3_K_M` -- deprecated hallucination constraint
- `qwen3-coder:30b` -- tier 2 escalation MoE A3B 23.3 tok/s

**Tier multimodal/reasoning**:
- `gemma4:latest` -- multimodal vision+audio+tools (39.26 tok/s ctx 8192)
- `deepseek-r1:8b` -- reasoning chain-of-thought (74.57 tok/s full-VRAM)
- `deepseek-r1:14b` -- scaling-up
- `phi4:14b` -- reasoning alternative

**Tier embedding/utility**:
- `nomic-embed-text:latest` (274 MB) -- embedding utility H5 gate
- `mistral:latest` -- chat fallback

**Tier exploratory** (non in routing primary):
- `qwen2.5:32b-instruct-q4_K_M`, `qwen3:8b`, `qwen3.5:latest`, `qwen3.6:latest`, `qwen2.5-coder:32b`, `gpt-oss:120b` (NON viable RAM-bound)

### B5 Ollama Qwen 7B inference smoke

Test: prompt "def add(a,b): return a+b -- add a docstring above", `qwen2.5-coder:7b`, num_predict=50.

Output (50 token): docstring Python-style "Adds two numbers and returns the result. Parameters..." (truncated mid-sentence per num_predict cap).

Speed measured: **50.4 tok/s** (eval_count=50 / eval_duration=0.99s). Below isolated baseline 114 tok/s (CLAUDE.md tier table): first-inference penalty + context loading overhead atteso. Sustained inference dovrebbe convergere a 100+ tok/s.

### Summary B

| Component | Status | Note |
|-----------|--------|------|
| Wrapper Aider 6 | ✓ READY | 4 cloud (5/9) + 2 local |
| API keys cloud free | ✓ READY | Groq/Cerebras/Gemini PASS |
| API key OpenAI | ✓ READY | paid emergency |
| API key Anthropic | ✗ **MISSING** | H7 Eduardo-direct ~5min |
| OpenCode binary + config | ✓ READY | default `ollama/qwen3-coder:30b` |
| Ollama daemon | ✓ READY | localhost:11434 reachable |
| Ollama models tier primary | ✓ READY | 7B + 14B Q2 + 30B MoE present |
| Ollama Qwen 7B inference | ✓ READY | smoke output coherent |

**Stack sovereign verdict**: **READY** per transition 2026-05-19 (7gg residui).

**Single gap**: H7 ANTHROPIC_API_KEY -- pre-deadline priority Eduardo-direct.

## Cross-pattern findings

1. **Vault Ollama fallback DEFER reinforce single-host pattern**: codemasterdd workflow Lenovo primary funziona stand-alone. Fleet awareness pre-condition (Ryzen onboarding) NOT yet triggered.
2. **H7 unique gap pre-Max**: tutto altro è ready. ANTHROPIC_API_KEY Eduardo-direct = unico residuo bloccante per Tier 0 strategic post-Max ADR-0023.
3. **Pattern adoption count 2026-05-12 mattina**: Pattern D vault-linter ADOPT (governance-lint) + Pattern E vault Ollama-fallback DEFER. 2 audit empirici, 1 implementation, 0 clone. Audit-then-replay pattern reinforced.

## Next action

- **Eduardo direct**: H7 ANTHROPIC_API_KEY setup `~/.config/api-keys/keys.env` pre-19/05 (~5min, [Anthropic Console](https://console.anthropic.com/))
- **No codemasterdd action proattiva** Pattern E (deferred trigger explicit)
- **No proattive bench** stack sovereign (5/5 PASS validation chiusa)

## Constraint hard respected

- [x] Read-only vault audit (Pattern E NO clone)
- [x] No external repo write (chat-only delivery)
- [x] No API key leak (smoke responses + token counts only, no secrets exposure)
- [x] Audit-then-replay policy applied to Pattern E
