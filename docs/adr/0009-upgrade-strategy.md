# ADR 0009 — Strategia evoluzione stack AI locale 2026-2027: trigger upgrade modello, hardware, client

**Status**: Proposed
**Data**: 2026-04-21
**Decisore**: Eduardo Scarpelli
**Tipo decisione**: strategica + tecnica (revisione Fase 2 ADR-0001, follow-up ADR-0007/0008)

## Contesto

### Stato corrente dello stack (post-fase 4.7)

Dal report sessione 2026-04-21:
- **Modelli locali**: Qwen 2.5 Coder 7B Q4_K_M (114 tok/s, cosmetic edits) + Qwen 2.5 Coder 14B Q2_K (25.5 tok/s, behavior-critical via `diff`)
- **Client**: Aider 0.86.2 via hub Claude Code + wrapper cmd.exe fallback
- **Hardware**: Intel Ultra 7 255HX, RTX 5060 8GB VRAM (Blackwell sm_120), 16GB DDR5
- **Reliability matrix empirica n=5**: 80% success, 20% safe fail, 0% corruption (ADR-0008 Addendum)

### Trigger di questo ADR

Febbraio 2026: rilascio di **Qwen3-Coder-Next** (MoE 80B total / 3B active params, 256K context nativo, performance dichiarata comparabile a Claude Sonnet 4 su agentic coding). Apre una nuova generazione di stack locale potenzialmente significativa per il progetto.

Questo ADR **non decide di upgradare subito**. Definisce **trigger espliciti e misurabili** che attiveranno upgrade modello, hardware o client — separando la decisione dal hype di release. Un framework per rispondere a "quando" e "a cosa" senza calendar-driven pressure.

## Opzioni analizzate

### Opzione 0 — Status quo prolungato

Mantenere stack attuale indefinitamente.

**Pro**: zero migration cost; stack validato empiricamente (n=5, ADR-0008); budget aggiuntivo zero fino a expiration Claude Max (19/05/2026) e oltre.
**Contro**: gap capability crescente vs SOTA; Fase 6 misurerà fail rate vs Qwen 2.5, non vs optimum disponibile; opportunity cost su deleghe che falliscono potrebbero essere gestite da modelli 2026.

### Opzione 1 — Upgrade modello only (Qwen3-Coder-Next, hardware invariato)

Switch a Qwen3-Coder-Next su RTX 5060 8GB, senza hardware change.

**Fattibilità tecnica** da verificare:
- MoE active params 3B → footprint inference teorico simile a 7B dense
- Weights totali 80B → serve sufficiente RAM sistema + offloading expert on-demand
- KV cache dipende da context; 256K nativo è oversize per task tipici (usable 8-16K)
- Ollama/llama.cpp supporto Qwen3 MoE specifico + sustained benchmark locale

**Pro**: capability jump significativo; nessun costo hardware; fail rate ridotto potenzialmente riabilita scenario ADR-0001 "full sovereign" $60-180/anno.
**Contro**: prima esperienza MoE locale, performance non predetta; maturity Ollama MoE da confermare; rischio regressione su workflow già funzionanti.

### Opzione 2 — Upgrade modello + hardware

Switch a Qwen3 E upgrade VRAM.

| Hardware option | Costo | Guadagno | Note |
|-----------------|-------|----------|------|
| RTX 5060 Ti 16GB | ~€500 | +8GB VRAM, full-GPU 14B dense, Qwen3 ampio margine | Upgrade incrementale, stesso form-factor |
| Mac mini M4 Pro 48GB | ~€2500 | Unified memory, Qwen3-Coder-30B-A3B viable, scala oltre | Device separato, ecosystem macOS parallelo |
| Status quo 8GB | €0 | Solo se Qwen3-Next MoE fit | Baseline |

**Pro**: garantisce viability Qwen3 anche worst case (MoE non fit); future-proofing vs generazioni successive; Mac mini abilita variants 30B+ e portability.
**Contro**: capex significativo; contraddice budget sovereign minimo; Mac mini introduce ecosystem switch.

### Opzione 3 — Switch cloud-only (exit sovereign)

Abbandonare stack locale per OpenRouter / Claude API pay-per-use.

**Scartata esplicitamente**: non coerente con ADR-0001 target sovereign. Riferimento solo per completezza analitica.

## Decisione

**Approccio trigger-based, non calendar-based**. L'upgrade avviene quando condizioni specifiche sono soddisfatte, non a data fissa. Qui definiamo i trigger; nessun upgrade immediato.

### Trigger T1 — Upgrade modello a Qwen3-Coder-Next

Tutte le condizioni devono essere vere:

1. Ollama rilascia supporto stabile per Qwen3-Coder-Next (verifica `ollama.com/library/qwen3-coder`)
2. ≥2 benchmark community indipendenti confermano performance claim (SWE-Bench o Aider benchmark)
3. Footprint VRAM/RAM su RTX 5060 8GB + 16GB DDR5 fit con sustained ≥10 tok/s
4. Fase 6 tracking data: fail rate attuale Qwen 2.5 stack ≥30% safe fail OR ≥1 corruption bypassato dal hook

**Azione al trigger**: test di 1 settimana su `aider-tty-test` replicando benchmark di ADR-0007 Task 2 e ADR-0008 dogfood battery. Se risultati superiori a 14B Q2 sia su cosmetic che behavior-critical, nuovo ADR (es. ADR-0010) con decisione switch default.

### Trigger T2 — Upgrade hardware

Almeno una condizione:

1. Qwen3-Coder-Next NON fit su 8GB post-test T1 (sustained <5 tok/s o OOM persistente)
2. Fail rate post-Qwen3 resta ≥25% dopo 2 mesi uso reale (stack-gap hardware-bound)
3. Emergenza workflow: task reale bloccante non gestibile dopo escalation Claude Pro fallback
4. Budget straordinario disponibile (es. spese deducibili, sconto retail)

**Decisione hardware al trigger**:
- Se bottleneck SOLO VRAM → RTX 5060 Ti 16GB (€500 incremental)
- Se bottleneck multi-dimensionale (VRAM + CPU + expandability) → Mac mini M4 Pro 48GB (€2500 strategic)

### Trigger T3 — Switch client agentic da Aider

**Nessun trigger attivo al 2026-04-21**. Aider resta primario perché:
- Expanded model support (Gemini 2.5, OpenAI o-series) dimostra longevity
- Diff-first review loop allineato con workflow git-native del progetto
- Hub pattern ADR-0008 consolidato sul binary Aider specifico

Re-evaluate solo se:
- Aider cessa development attivo (>6 mesi nessun commit upstream)
- Concorrente dimostra breakthrough capability senza migration cost significativo

## Implicazioni

### Su roadmap progetto

- **Fase 6 (3-mesi uso reale, post-19/05)**: tracking log deve includere metriche che alimentano trigger T1/T2. Aggiungere a `aider-delegation-log-template.md` campi: `fail_reason` (capability / format / cross-file / hardware) e `task_not_delegatable` (flag + motivo)
- **Fase 7 (decisione budget)**: T1 post Fase 6 introduce una variabile aggiuntiva; scenario "full-sovereign" torna plausibile se T1 attivato con fail rate <10%
- **Nessun impatto immediato** su Fase 5 (migrazione Evo-Tactics/Synesthesia): stack attuale resta operativo per migrazione

### Su budget (scenari aggiornati post-T1/T2)

| Scenario | Cost additional | Break-even vs Claude Pro ($240/anno) | Trigger |
|----------|-----------------|--------------------------------------|---------|
| T1 only (solo modello) | Tempo setup ~4-8h + €0 hardware | Immediato (è solo tempo) | T1 attivato |
| T1 + T2 (RTX 5060 Ti 16GB) | ~€500 one-time | ~2 anni (se skip Claude Pro) | T1 + T2 condizione 1 o 3 |
| T1 + T2 (Mac mini M4 Pro) | ~€2500 one-time | ~10 anni — giustificato solo se valore indipendente (ecosystem, portability) | T2 condizione 4 |

### Su metriche tracciate

Campi nuovi richiesti nel tracking log Fase 6 per alimentare trigger:
- `fail_reason`: enum [`format_variance`, `capability_gap`, `cross_file_scope`, `hardware_limit`, `model_crash`]
- `attempted_escalation`: enum [`none`, `reprompt`, `claude_direct`, `claude_pro`]
- `task_completed`: boolean (delegazione riuscita o escalation risolta)

## Follow-up

### Pre-trigger (preparazione operativa)

- [ ] Monitor Ollama release notes Qwen3-Coder-Next (cadenza ~mensile manuale, fino a disponibilità)
- [ ] Bookmark: `huggingface.co/Qwen/Qwen3-Coder-Next` + aggregator benchmark community
- [ ] Estendere `aider-delegation-log-template.md` con campi `fail_reason`, `attempted_escalation`, `task_completed`
- [ ] Research session trimestrale (prossima ~2026-07) per aggiornare snapshot `docs/research/ai-stack-evolution-2026.md`

### Al trigger T1 attivato

- [ ] `ollama pull qwen3-coder-next:<quant>`
- [ ] Replica benchmark ADR-0007 Task 2 (JSDoc su Synesthesia controller) + ADR-0008 dogfood battery
- [ ] JOURNAL entry con dati raw + raccomandazione
- [ ] Nuovo ADR (es. ADR-0010) con decisione switch default

### Al trigger T2 attivato

- [ ] ADR specifico hardware choice (RTX 5060 Ti vs Mac mini), con cost analysis aggiornata al momento della decisione
- [ ] Piano migration environment dev (solo se Mac mini: `.env` shell, PATH, installed tooling)

## Lezioni meta

### Upgrade trigger-based > calendar-based

Upgrade fissato a "fra 6 mesi" o "quando esce X" spesso arriva troppo presto (stack funzionante distrutto per marketing hype) o troppo tardi (opportunity cost accumulato). Trigger condizionati a metriche empiriche (fail rate, benchmark verificati, footprint misurato) rimuovono pressione temporale e ancorano la decisione ai dati reali.

### Non inseguire SOTA se SOTA non è accessibile

Qwen3-Coder-480B è più capable di Qwen3-Coder-Next ma impraticabile su hardware personal. Model selection non è mai "il più grande che fit": è "il più utile per il workflow a costo accettabile". MoE 80B/3B-active di Next è probabilmente il nuovo sweet-spot, come Q2_K era il sweet-spot su 14B dense (ADR-0007 paradox quantization).

### Research-first, commit-second

ADR di upgrade senza research aggiornato rischia di essere basato su assunzioni 6-12 mesi vecchie. In field fast-moving come local LLMs, research sessions trimestrali mantengono ADR aggiornati senza essere costantemente in mode-upgrade. Prossima research session programmata: ~2026-07.

## Addendum 2026-04-21 (empirical validation)

**Scoperta audit**: `qwen3-coder:30b` (variante 30B-A3B MoE Q4_K_M, 18 GB) **già installato** ~4h prima (pull probabile da tray Ollama). Opportunità test senza attendere monitoring.

### Hardware findings contro-intuitivi

Test empirici su RTX 5060 8GB + 16GB DDR5:

| Config | RAM usato | VRAM | CPU/GPU split | Speed | Viable |
|--------|-----------|------|---------------|-------|--------|
| Default (ctx 256K) | ERROR "12.2 GiB required" | — | — | — | ❌ OOM |
| ctx 2048 | — | — | — | 23.8 tok/s | ✅ ma troppo stretto per Aider |
| ctx 4096 | — | — | — | 24.0 tok/s | ✅ borderline |
| **ctx 8192** | **14.1 GB (1.3 GB free)** | **91%** | **66/34 CPU** | **23.3 tok/s** | ✅ **match 14B Q2 config** |

**Bottleneck revisionato**: non VRAM ma **RAM** (MoE weights devono essere tutti loadable, anche se solo 3B active per token). T2 trigger hardware da rivedere:

- Old framing: VRAM bottleneck → RTX 5060 Ti 16GB (~€500)
- **New framing**: RAM bottleneck → 32GB DDR5 (~€80) sblocca ctx 16384+ e margin confortevole

### Quality validation (dogfood diretto vs 14B Q2)

Test R1, R2, R3 su `aider-tty-test/demo.js` con `aider --model ollama/qwen3-coder:30b --edit-format diff` + R-cosmetic con `--edit-format whole`:

| Test | Edit fmt | 14B Q2 (ref ADR-0008) | **qwen3:30b** | Delta |
|------|----------|-----------------------|----------------|-------|
| R3 extract method | diff | ✅ success clean (37s, 3.1k/331) | ✅ byte-identical (70s, 3.0k/310) | speed 14B Q2 wins 2× |
| R1 value-change 1-line | diff | ❌ **safe-fail 3 retry** (anti-pattern) | ✅ **success first-pass** (41s, 3.0k/84) | **capability jump reale** |
| R2 rename method | diff | ✅ success + drift (25s, 3.0k/150) | ✅ byte-identical + **same drift** (89s, 3.0k/115) | parity, speed 14B Q2 wins 3.5× |
| JSDoc cosmetic (stress whole) | whole | ❌ **silent corruption** (ADR-0008) | ✅ **clean success** (210s, 1.2k/720) | **architectural safety** |

**Finding chiave diff format**: Qwen3:30b **sa scopare SEARCH block al minimo necessario**. Su R1 ha emesso SEARCH con solo la function target, zero preamble — dove 14B Q2 includeva context preamble che poi non byte-matchava. Resolve l'anti-pattern documentato.

**Finding chiave whole format (n=4 test)**: Qwen3:30b **NON ha il silent-corruption bug** che affligge 14B Q2 con whole format (ADR-0008 root cause: double code-block output). Qwen3 emette formato Aider-nativo corretto (filename on own line + single code block) — stessa famiglia architetturale di 7B. Aggiunge un'opzione di fallback safe per task che richiedessero whole format (non primario: speed 8× più lenta di 7B).

**Finding drift (R2)**: il "drift" semantico su rename (rinominare string literal coerente col method name) appare anche con Qwen3 — è comportamento LLM generale, non modello-specifico. Scope constraint "only X" va rafforzato nel prompt se la strict interpretation è critica.

### Decisione empirica rivista

**T1 trigger status aggiornato**:
- ✅ Condition 1 Ollama support → met (tag `qwen3-coder:30b`)
- ✅ Condition 2 benchmark community → met (Qwen docs + Aider SWE-Bench)
- ✅ Condition 3 footprint fit → met con margine stretto (1.3 GB free a ctx 8192)
- ⚠️ Condition 4 fail rate ≥30% → non misurato formalmente, ma R1 è caso concreto

**Decisione operativa** (non switch totale, promozione a tier escalation):

1. **14B Q2 rimane default** behavior-critical (speed 2× + RAM margine 3.7× più largo)
2. **qwen3:30b diventa tier 2 escalation** quando 14B Q2 safe-fail (R1-type 1-line value change, o altri anti-pattern emergenti)
3. **Claude Pro/OpenRouter tier 3** solo se anche qwen3:30b fallisce
4. **T2 hardware trigger ridefinito**: RAM upgrade 32GB DDR5 (~€80) invece di GPU upgrade (€500) sblocca qwen3 senza tight margin

### Routing aggiornato (rimpiazza tabella decision originale T1)

| Task class | Tier 1 (default) | Tier 2 (escalation se T1 fail) | Tier 3 (cloud fallback) |
|------------|------------------|--------------------------------|--------------------------|
| Cosmetic | 7B + whole | 14B Q2 + diff (manuale) | Claude Pro |
| Behavior-critical | **14B Q2 + diff** | **qwen3:30b + diff** | Claude Pro |
| Strategic | Claude Code | Claude Pro/OpenRouter | — |

## Riferimenti

- ADR-0001 Sovereign AI Strategy — questo ADR rivede Fase 2 scenario: `0001-sovereign-ai-strategy.md`
- ADR-0004 Ollama RTX 5060 config — env vars invariati: `0004-ollama-rtx5060-config.md`
- ADR-0007 Aider + Qwen quantization findings — baseline 14B Q2: `0007-aider-qwen-quantization-findings.md`
- ADR-0008 Silent corruption + dual-stack — reliability matrix n=5: `0008-aider-whole-format-silent-corruption.md`
- Research snapshot 2026-Q2: `docs/research/ai-stack-evolution-2026.md`
- Qwen3-Coder project: https://github.com/QwenLM/Qwen3-Coder
- Qwen3-Coder-Next HuggingFace: https://huggingface.co/Qwen/Qwen3-Coder-Next
- Qwen blog: https://qwenlm.github.io/blog/qwen3-coder/
- Aider releases: https://github.com/Aider-AI/aider/releases
