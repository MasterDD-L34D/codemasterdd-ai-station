# ADR-0029 -- OpenRouter eval declined for sovereign-first BYOK pattern

**Status**: Proposed 2026-05-13 pomeriggio (post harsh-reviewer P2 #7 trigger Eduardo decision "si" + autoresearch doc-only)
STATUS-CHECK: 2026-06-13 | trigger: >$5/mese x2 mesi consecutivi OR >8 wrapper | default-if-elapsed: Accept (decline regge se nessun trigger)

**Context**: harsh-reviewer (PR #80+#81 cluster review 2026-05-13) ha sollevato P2 #7: "OpenRouter NON valutato -- 6 wrapper potrebbero essere 1 wrapper unificato (`aider-router --model openrouter/...`) con OpenAI-compatible single endpoint verso N provider con 1 key. Sostituirebbe 5 wrapper cloud con 1, unificando privacy guard, key handling, error mode."

Eduardo trigger esplicito (2026-05-13): autorizza eval OpenRouter per decision "stabilizzare 6-wrapper matrix vs simplification single-endpoint".

## Decision

**Decline OpenRouter adoption per current sovereign-first BYOK pattern**. Mantenere 5 wrapper cloud direct + 1 sovereign-bypass (aider-groq-bypass). Reconsider trigger: se cumulative cloud spend >$5/mese × 2 mesi consecutivi, OR se proliferation wrapper continua (>8 wrapper future).

## Context completo

### Componente attuale (post-cluster 2026-05-13)

5 wrapper cloud + 2 sovereign in `~/.local/bin/`:
- `aider-cosmetic` (Qwen 7B + diff, sovereign)
- `aider-refactor` (Qwen 14B Q2 + diff, sovereign)
- `aider-cerebras` (Cerebras 8B + `--map-tokens 0`)
- `aider-gemini` (Gemini 2.5 Flash + `--map-tokens 0`)
- `aider-openai` (gpt-4o-mini, post 10 EUR funding)
- `aider-groq-bypass` (Groq 70B via openai/, P0 hardened temp env-file)

### OpenRouter alternative

OpenRouter è 1 endpoint OpenAI-compatible (`https://openrouter.ai/api/v1`) verso 290+ modelli con 1 API key. Pricing model: passthrough rates dei provider underlying + 5% margin. BYOK opzionale: bring your own provider keys via OpenRouter settings -> bypass 5% markup -> stesso costo direct.

### Empirical eval results (doc-only, NO key in keys.env per smoke)

Autoresearch multi-source 2026-05-13:
- **Free tier OpenRouter**: 29 modelli curated free (DeepSeek V3 + R1, Llama, Qwen variants). **llama-3.3-70b-versatile NON è nel free pool** (= il workaround Groq-bypass nostro rimane unica via per Groq 70B free)
- **Markup**: 5% standard, 0% BYOK (settings -> insert provider key direct)
- **Modelli premium** (Anthropic Claude, OpenAI gpt-4o, Gemini): stesso prezzo direct OR 5% markup OR BYOK 0%
- **Single endpoint OpenAI-compat**: drop-in replacement per qualsiasi tool che usa OpenAI client

## Considered options

### Option A -- Adopt OpenRouter unified, retire 5 wrapper cloud (RECOMMENDED da harsh-reviewer)

- 1 wrapper `aider-router` con `--openai-api-base https://openrouter.ai/api/v1` + `--model openrouter/<provider>/<model>`
- 1 key OPENROUTER_API_KEY in keys.env, retire 4 keys provider direct (Cerebras + Gemini + OpenAI keys)
- Mantenere 2 wrapper sovereign (aider-cosmetic + aider-refactor)
- 6 wrapper effettivi -> 3 wrapper

**PRO**:
- Surface area -50% (1 wrapper cloud vs 5)
- 1 key rotation invece di 4
- Privacy guard rail H8 unified su 1 file
- Add new model = no new wrapper (just `--model` arg change)

**CONTRA**:
- 5% markup standard (su nostro $0.01/mese cumulative = $0.0005/mese, IRRILEVANTE)
- BYOK negate il valore: se mantieni 4 keys per provider per evitare 5% markup, perdi simplification
- SPOF cloud: OpenRouter down = TUTTI provider cloud unreachable (vs current direct = independent)
- llama-3.3-70b-versatile NON free su OpenRouter (paid passthrough Groq) -- perdiamo Groq free tier 300K TPM
- Migration cost: rewrite 5 wrapper + retest matrix completa + update CLAUDE.md + ADR
- Lock-in vendor: future OpenRouter pricing change o policy ToS impatta nostro stack

### Option B -- Adopt OpenRouter only for cloud paid tier 4 (gpt-4o-mini, Anthropic strategic)

- 1 wrapper `aider-router-paid` per tier 4 cloud paid (openai gpt-4o-mini + claude sonnet/haiku)
- Mantenere 4 wrapper cloud free direct (cerebras + gemini + groq-bypass)
- Mantenere 2 wrapper sovereign

**PRO**:
- Tier paid centralized via OpenRouter = unified billing
- Free tier providers restano direct (Cerebras + Gemini + Groq) preservando free 300K TPM
- Surface area -16% (5 wrapper cloud -> 4)
- Anthropic tier-0 strategic anche via OpenRouter = 1 key rotation per tutti paid

**CONTRA**:
- Marginal benefit: 1 wrapper fewer, mismatch direct vs router pattern
- Anthropic ADR-0023 strategic NON richiede router (ANTHROPIC_API_KEY direct funziona in keys.env)
- Eduardo dovrebbe gestire 2 paradigmi (direct provider per free, router per paid)
- 5% markup su tier paid = $0.0005/mese (IRRILEVANTE) ma nessun saving dimostrato

### Option C -- Decline OpenRouter, mantieni current 6-wrapper sovereign-first BYOK pattern (CHOSEN)

- Mantieni 5 wrapper cloud direct (Cerebras + Gemini + OpenAI + groq-bypass + future ANTHROPIC se serve)
- Mantieni 2 wrapper sovereign
- Document trigger reactivation per re-eval futuro

**PRO**:
- Free tier providers preservati (Cerebras + Gemini + Groq via bypass) = 300K TPM Groq + 250K TPM Cerebras + 250K TPM Llama 8B
- Direct API = lower latency vs router intermediate hop
- NO 5% markup ON ANY tier (irrilevante per nostro volume MA principio sovereign-first preserved)
- NO SPOF cloud: 5 provider independent fallback chain
- NO vendor lock-in OpenRouter pricing/policy
- NO migration cost adesso

**CONTRA** (acknowledged):
- Surface area 6 wrapper vs 1 (proliferation pattern)
- 5 keys to rotate (key management overhead)
- Privacy guard rail H8 must repeat per wrapper template (template script copia + L-015 regression risk)
- Add new provider = new wrapper file (NON solo `--model` arg)
- Bus-factor 1: wrapper user-side, IaC gap

### Option D -- Adopt OpenRouter via BYOK (best of both worlds)

- 1 wrapper `aider-router` ma BYOK: invia le NOSTRE Groq/Cerebras/Gemini/OpenAI keys via OpenRouter settings
- 0% markup per BYOK requests
- 1 endpoint, N provider via own keys

**PRO**:
- Simplification 1 wrapper achieved
- 0% markup (BYOK pattern documented OpenRouter docs)
- Free tier providers preservati (BYOK -> direct quota underlying)

**CONTRA**:
- BYOK richiede inserire 4 keys in OpenRouter UI (1 key OpenRouter + 4 keys upstream) = TOTAL 5 keys vs 4 currently
- OpenRouter sees i nostri provider keys (additional trust surface)
- BYOK setup complexity = perdiamo clean simplification "1 key rules them all"
- SPOF cloud OpenRouter remains
- Migration cost still applies (wrapper rewrite + ADR + matrix retest)

## Decision rationale

**Option C chosen** per principio **sovereign-first + BYOK negate Option A/D value**:

1. **Free tier preservation matters**: Groq llama-3.3-70b-versatile gratuito via direct (post bypass) NON è gratuito via OpenRouter (passthrough paid). Adopting OpenRouter = perdiamo $0 cost path on 70B
2. **Volume-cost analysis irrilevante**: $0.01/mese cumulative cloud (nostro current) -> 5% margin = $0.0005/mese. Saving NULLO. OpenRouter unified-billing benefit nullo.
3. **SPOF + vendor lock-in**: direct providers = 5 independent chains. OpenRouter = 1 dependency. Sovereign-first principle conflicts.
4. **Bus-factor argument is wrapper-pattern issue NOT OpenRouter solution**: 6 wrapper user-side = problema IaC. Risolvibile con `scripts/wrappers/` + install script (P1 #4 harsh-reviewer separate ADR if needed). Adopting OpenRouter NON risolve bus-factor (1 wrapper user-side in `~/.local/bin/` resta).
5. **Add-new-provider argument valid**: SE in futuro Eduardo aggiunge provider 7+ (es. Mistral, Together AI), il pattern direct scala male. MA al momento 5 cloud + 2 sovereign sono SUFFICIENT per 100% dei use case validati (T1 SPRINT_02 dimostra).

**Trigger reactivation per re-eval futuro**:
- Cumulative cloud spend >$5/mese × 2 mesi consecutivi (cost-justified migration)
- Wrapper proliferation >8 (operational complexity threshold)
- OpenRouter offre llama-3.3-70b free tier (parity con direct Groq)
- LiteLLM Groq adapter bug RESOLVED upstream (rimuove bisogno bypass wrapper, riduce a 4 cloud wrapper = ulteriore review)

## Consequences

### Positive

- Stabilità current pattern (no migration risk)
- Free tier providers preservati (Groq 300K + Cerebras 250K + Gemini 60 RPM + ANTHROPIC tier-0 + OpenAI 2.5M tok/day post 10 EUR)
- Sovereign-first principle ADR-0001 preservato (no intermediate router for sovereign+free path)
- Cost $0.0005/mese saving forgone = NULL (acceptable)

### Negative

- Bus-factor 1 wrapper user-side persiste (separate fix via `scripts/wrappers/` + install script)
- Add-new-provider future = nuovo wrapper file (NON 1-line `--model` change)
- 5 keys management overhead (rotazione manual)
- Privacy whitelist guard rail repeat in N template (acceptable, automated via shared template)

### Neutral

- OpenRouter rimane reference per future pivot se trigger reactivation hit
- BYOK pattern documented case future use ad-hoc (es. testing 1-off model paid)

## Implementation

**No implementation required** -- decision = NON adottare OpenRouter. Status quo wrapper matrix preservato.

**Documentation deliverables** (questa PR):
- ADR-0029 written (this file)
- CLAUDE.md NO change (current wrapper section accurate)
- DECISIONS_LOG entry: "Decisione 008: OpenRouter eval declined sovereign-first BYOK"

## Cross-references

- harsh-reviewer P2 #7 (PR #80+#81 review trigger)
- ADR-0001 sovereign AI strategy (foundation)
- ADR-0013 tier 3 cloud free providers
- ADR-0023 strategic tier post-Max API on-demand
- L-2026-05-014 + L-2026-05-015 wrapper-related lessons
- entry #36 logs/aider-delegation-2026-05.md (Groq bypass autoresearch resolution)

## Trigger Accepted

ADR-0010 early-acceptance flag NON applicabile -- decision è "decline" not "adopt", no implementation to validate empirical. Status resta Proposed fino emergence trigger reactivation oppure 6 mesi senza trigger -> auto-Accepted.
