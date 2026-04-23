# ADR-0013 — Tier 3 cloud escalation via free-tier providers (Groq/Cerebras/Gemini/OpenAI)

> *TL;DR: acquisite 4 API keys gratuite o a basso costo (Groq/Cerebras/Gemini/OpenAI) il 2026-04-22. Ridefiniscono lo scenario post-Claude Max: non più "pay-per-use $1200/mese" ma "free-tier cloud sovereign" con Groq/Cerebras come tier 3 primario (LPU/WSE velocissimi). OpenAI resta pay-per-use ma tenuto come ultimo resort capability-max. Storage file-based ACL-hardened, zero registry, zero commit.*

- **Status**: **Accepted** (2026-04-23 02:05 — quality bench v1+v2 75 test 100% pass@1 + approvazione utente)
- **Data**: 2026-04-22 (Proposed), 2026-04-23 (Accepted)
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

## Context and Problem Statement

Il 2026-04-22 (stessa giornata dell'upgrade RAM ADR-0012) sono state acquisite 4 API keys cloud non previste nella roadmap originale ADR-0001:

1. **Groq** — LPU inference, free tier 6000 tok/min sostenuto, modelli open-weight (Llama 3.3 70B, Qwen 2.5 Coder 32B, ecc.)
2. **Cerebras** — WSE inference, free tier generoso, Llama 3.3 70B veloce
3. **Google Gemini** — 60 req/min free, Gemini 2.0 Flash (coder-capable)
4. **OpenAI** — pay-per-use, nessun free tier significativo, GPT-4o/4o-mini

Il baseline economico pre-ADR-0013 (vedi memory `project_sovereign_evaluation.md`):
- Claude Max scade 2026-05-19 (€200/mese = $215)
- Pay-per-use Opus 4.7 estimata $1200/mese (6× Max) su baseline $118.76/3g ccusage
- Scenario budget Fase 7: ibrido Claude Pro ($20/mese) + Ollama locale

Con l'acquisizione di Groq/Cerebras free-tier, **lo scenario "full-sovereign" torna realistico senza ricorrere a Claude Pro**:
- Tier 1-2 locale (Qwen 14B Q2 + qwen3:30b MoE) copre ~80% task (assumed da Fase 6 pending validation)
- Tier 3 **free-tier cloud** (Groq/Cerebras) copre task strategici dove locale safe-fails
- OpenAI resta reserve capability-max per task estremi

Serve un ADR che:
1. Documenti l'acquisizione e il decision framework di routing
2. Proponga storage sicuro (già implementato 2026-04-22, confermato empiricamente via test Groq)
3. Rivaluti scenario budget Fase 7 alla luce dei nuovi dati

## Decision Drivers

- **YAGNI**: integrare solo quando serve, non pre-configurare wrapper per ogni provider
- **Sicurezza credenziali**: file-based + ACL preferito a registry (`setx`) per supply-chain safety
- **Compatibilità stack esistente**: Aider (LiteLLM) supporta tutti e 4 provider nativamente via env vars
- **Reversibility**: revoca rapida (rimuovi file, ruota keys dai provider UI)
- **Cost control**: prioritizzare free-tier (Groq/Cerebras) in routing automatico, OpenAI/Gemini come fallback
- **Fase 6 integrità**: non inquinare tracking in corso con cambio baseline; tier 3 si attiva post-Max (19/05)

## Considered Options

### Opzione A — Ignorare le keys, mantenere roadmap pre-esistente (Claude Pro ibrido)

**Pro**: zero configurazione, zero superficie leak credenziali; roadmap stabile.

**Contro**: spreco opportunità — free tier Groq+Cerebras copre 90%+ task cloud senza costo; Claude Pro $20/mese non necessario se sovereign è viable; l'utente ha già speso tempo ad acquisire keys.

### Opzione B — setx di tutti e 4 i keys (Windows User env vars)

**Pro**: disponibile in ogni shell, Aider le legge senza config aggiuntiva.

**Contro**: keys in Windows registry (visibili via `reg query HKCU\Environment`, strumenti inspection); difficile revoca rapida (serve setx delete + restart); pattern anti-YAGNI (tutte e 4 pre-configurate anche se 3/4 potrebbero non essere mai usate).

### Opzione C (chosen) — File-based + ACL + Aider auto-load

**Implementato 2026-04-22**:
- `C:\Users\edusc\.config\api-keys\keys.env` (file dotenv-format)
- ACL: solo `CODEMASTERDD\edusc` Full Control, inheritance disabilitata
- Backup gitignored: `backup/api-keys-2026-04-22.env`
- Aider globale `~/.aider.conf.yml` con `env-file:` → auto-load zero-config
- Bash sessions: source on-demand (`set -a; source ~/.config/api-keys/keys.env; set +a`)

**Pro**:
- Nessuna chiave in registry
- Revoca rapida: `Remove-Item` + rotation dai provider UI
- Pattern allineato con esistente `~/.env` per `OLLAMA_API_BASE`
- Aider funziona senza setup per-progetto
- ACL-protection NTFS robusto

**Contro**:
- Non disponibile automaticamente in sessioni bash interattive (serve source manuale)
- Doppia copia (primario + backup) raddoppia superficie leak — mitigato da ACL identiche e backup gitignored

### Opzione D — Windows Credential Manager

**Pro**: massima sicurezza OS-level (encrypted at rest, per-user).

**Contro**: Aider non legge nativamente Credential Manager; serve wrapper che `Get-StoredCredential` + `$env:VAR=...` prima del launch; overhead sviluppo wrapper + manutenzione. Over-engineering per workflow sovereign.

## Decision Outcome

**Scelta Opzione C**. Implementazione 2026-04-22 sera, validata via test Groq (response `"content":"ok"` end-to-end).

### Routing strategy proposto (post-Claude Max 19/05/2026)

Il routing tier 3 si attiva **solo** quando tier 1 (14B Q2) E tier 2 (qwen3:30b) safe-fails. Decision tree:

| Scenario | Provider preferito | Fallback | Rationale |
|----------|--------------------|---------:|-----------|
| Task behavior-critical safe-fail tier 2 | **Groq** llama-3.3-70b-versatile | Cerebras llama3.3-70b | LPU veloce, 70B dense capability > qwen3:30b |
| Task multi-file strategico | **Cerebras** llama3.3-70b | Groq qwen-2.5-coder-32b | WSE sostiene long context |
| Task capability-max (refactor complesso, debug strategico) | **OpenAI** gpt-4o | Claude Pro (se attivato) | capability ceiling superiore |
| Task quick query / code explain generico | **Gemini** 2.0 flash | Groq llama | 60 req/min free sufficiente |

**Priorità free-tier first**: Groq > Cerebras > Gemini > OpenAI. OpenAI solo quando free-tier providers non bastano.

### Impact Fase 7 budget decision

**Scenario rivalutato**:
- Pre-ADR-0013: Ibrido Claude Pro $20/mese + Ollama = **$240/anno**
- Post-ADR-0013 (se free-tier copre 95%+ task cloud): Full-sovereign free + Ollama = **$0-50/anno** (solo eventuali OpenAI overflow)

**Il target ADR-0001 "full-sovereign $60-180/anno" ora è sub-$60/anno**.

Caveat: **da validare in Fase 6**. I free tier hanno rate limit, quality non misurata vs Claude. Se Fase 6 rivela che Groq llama 70B non copre i task che Claude Pro avrebbe coperto, rivalutare.

### Non fatto in questo ADR (da sviluppare in corso d'opera)

- **Wrapper `aider-cloud`** dedicato: non creato. Se l'uso diventa frequente creo wrapper CMD che esplicita provider preferito. Per ora: `aider --model groq/...` diretto quando serve.
- **Rate-limit handling**: Groq/Cerebras hanno limiti — monitorare in Fase 6 se emergono 429. Retry logic eventuale in wrapper.
- **Quality benchmark**: Groq llama 70B vs qwen3:30b MoE locale su task reali. Rimandato a Fase 6 dati empirici.
- **OpenRouter non incluso**: non acquisita key. Se emerge necessità (unified API, accesso a modelli non disponibili altrove) → add in futuro.

## Consequences

**Positive**:
- Scenario sovereign Fase 7 diventa $0-50/anno (miglioramento +$190/anno vs baseline ibrido)
- Capability ceiling aumentato: llama 70B + gpt-4o > qwen3:30b locale
- Pattern di storage riutilizzabile per future credenziali (ACL + dotenv + Aider config)

**Negative / rischi**:
- 4 superfici di leak in più (ogni chiave è credenziale attiva)
- Free tier possono ridurre limiti nel tempo → scenario budget fragile vs unilateral provider changes
- Rate limit possibile blocker su task iterativi (Aider multi-edit)

**Neutral**:
- Il locale rimane il default; cloud è escalation reale (come già tier 2 qwen3:30b)
- Test validato solo Groq end-to-end — altri 3 provider assumed compatibili via LiteLLM (standard)

## Follow-up

- [x] Validare endpoint Cerebras (combo F 2026-04-22: llama3.1-8b PASS; gpt-oss-120b e qwen-3-235b free tier BLOCKED, paid-only)
- [x] Validare endpoint Gemini (combo F 2026-04-22: gemini-2.5-flash PASS con `thinkingConfig.thinkingBudget=0`; gemini-2.0-flash quota 0 effective deprecated)
- [x] Validare endpoint OpenAI (combo F 2026-04-22: gpt-4o-mini PASS)
- [x] **Fase 6 dogfood** tier 3 (n=3 cumulative 2026-04-22/23): dogfood #4 Groq direct cosmetic + #5 Groq wrapper cosmetic + #6 Groq wrapper **behavior-critical**. 100% success, $0.0089 total cost free tier.
- [x] Wrapper dedicati creati (opzione D 2026-04-23): `aider-groq.cmd`, `aider-cerebras.cmd`, `aider-gemini.cmd`, `aider-openai.cmd` in `~/.local/bin/`
- [ ] Fase 7 (~**2026-05-20** post ADR-0014 compression): rivalutare budget scenario con dati Fase 6. Se free-tier basta → full-sovereign definitivo. Se no → Claude Pro residuale.
- [ ] Se una delle keys viene esposta (git history leak, scraper, etc.): revoca immediata via provider UI + rotation + update `keys.env`.

## Status changes

Proposed 2026-04-22. Passerà a **Accepted** dopo review utente + primo dogfood Fase 6 (task safe-fail locale risolto da Groq end-to-end).

## Riferimenti

- **CLAUDE.md** sezione "API keys tier 3 cloud" — paths + provider list
- **Memory** `reference_api_keys.md` — pointer-style per future sessioni Claude
- **ADR-0001** `0001-sovereign-ai-strategy.md` — target budget originale $60-180/anno, ora sub-$60/anno
- **ADR-0008** `0008-aider-whole-format-silent-corruption.md` — hub pattern tier routing rafforzato
- **ADR-0009** `0009-upgrade-strategy.md` — trigger framework; questo ADR non materializza trigger T1/T2/T3 esistenti ma estende dimensione "cloud providers" non prima prevista
- **ADR-0012** `0012-ram-upgrade-64gb-impact.md` — contesto stessa giornata (hardware upgrade + bench tier 2 rafforzato)
- **Aider LiteLLM providers**: https://docs.litellm.ai/docs/providers
- **Groq API docs**: https://console.groq.com/docs
- **Cerebras API docs**: https://inference-docs.cerebras.ai

---

## Addendum 2026-04-22 sera tardi — Validation combo F (A + B + E)

Eseguite 3 operazioni stessa serata dell'ADR-0013 Proposed:

### A — Validazione endpoint 4 provider
- **Groq** llama-3.3-70b-versatile: ✅
- **OpenAI** gpt-4o-mini: ✅
- **Gemini** gemini-2.5-flash: ✅ (richiede `thinkingConfig.thinkingBudget=0` altrimenti thinking mode consuma budget output)
- **Cerebras** llama3.1-8b: ✅ (ma `gpt-oss-120b` e `qwen-3-235b` nel catalog **NON accessibili free tier** — paid tier required)

**Gemini 2.0-flash** = quota 0 effettiva (deprecato o limitato), usare **gemini-2.5-flash** come default.

### B — Primo dogfood Aider + Groq (cosmetic task, file del repo)
- Target: `scripts/bench-ollama.ps1` — 2 `.EXAMPLE` extra + `.NOTES` section
- Config: `aider --model groq/llama-3.3-70b-versatile --edit-format diff --no-auto-commits`
- Risultato: ✅ SUCCESS, 11 insertions additive, 1 retry format, **~10s wall clock**, **$0.0033 cost** (free tier: $0)
- Glitch minore: "è un implementazione" (manca apostrofo elisione, lingua non core issue)
- Log Fase 6: `logs/aider-delegation-2026-04.md` dogfood #4

### E — Bench speed cloud vs locale (stesso prompt DoublyLinkedList)

| Model | Speed tok/s | vs locale equivalente |
|-------|------------:|----------------------|
| `groq/llama-3.3-70b-versatile` | **630.86** | **20.6×** vs qwen3:30b (30.67) |
| `cerebras/llama3.1-8b` | **733.5** | **6.4×** vs qwen2.5-coder:7b (114) |

Script riusabile: `scripts/bench-cloud.ps1`.

### Implicazioni per routing strategy

**Online mode (internet up + free quota)**: cloud è **dominante su tutti i fronti** — speed 6-20× maggiore, capability 70B/8B ≥ equivalente locale, cost $0.

**Pattern routing proposto** (pending Fase 6 quality validation):
- Tier 1 cosmetic ONLINE: `cerebras/llama3.1-8b` → fallback `qwen2.5-coder:7b`
- Tier 2 behavior ONLINE: `groq/llama-3.3-70b-versatile` → fallback `qwen2.5-coder:14b-q2`
- Tier 3 escalation: `groq/qwen-2.5-coder-32b` se disponibile (da verificare) / `qwen3-coder:30b` locale
- Tier 4 capability-max: `openai/gpt-4o` / `gemini-2.5-pro`

### Caveat critici (bloccanti shift definitivo)

1. **Privacy**: send source code → data retention per Groq/Cerebras ToS. **Sovereign-first obbligatorio** per codice cliente/proprietario. Cloud OK per repo personali (questo ADR OK).
2. **Quality coder**: bench speed dice nulla su qualità output coder. Llama general vs Qwen Coder specialist → possibile gap quality. Richiede quality bench (HumanEval-like) prima di promote definitivo.
3. **Cerebras paid models**: `gpt-oss-120b`, `qwen-3-235b` catalog ma free tier blocca. Paid tier costs da verificare prima di considerare.
4. **Rate limit**: Groq 6k tok/min → task Aider iterative (multi-turn) possibile throttle.
5. **n=1**: speed bench singolo. Variability non misurata.

### Status updates

- **ADR-0013**: da **Proposed** a **Validation-in-progress** (speed PASS, quality + reliability pending Fase 6).
- **CLAUDE.md tier routing**: NON aggiornato in questa sessione. Aspetta dogfood Fase 6 prima di shift paradigmatico.
- **Follow-up critico**: quality bench (HumanEval pass@1 o equivalente) su Qwen Coder 7B/14B vs Llama 3.1-8B / 3.3-70B, per decidere se i coder-specialist locali hanno edge qualitativo che compensa lo speed gap.

### Privacy guard aggiunto

Per questo repo (`lenovo-ai-station`) = **OK cloud** (infrastructure-as-code personale, niente segreti — le keys sono fuori repo via `.config/` + `backup/*` gitignored).
Per `Evo-Tactics` e `Synesthesia`: revisione caso-per-caso. Se contengono logica proprietaria cliente o dati sensibili → sovereign-first.
