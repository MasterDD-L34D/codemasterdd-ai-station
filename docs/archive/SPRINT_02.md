> ARCHIVED 2026-06-03 (context-files reorg Fase 2). SUPERSEDED -- live direction = GOALS.md + ORCHESTRATION.md.
> Historical record.

# SPRINT_02 -- "Post-Max scenario A operativo + smoke sovereign + cleanup"

> Sprint 2 della Fase 7 (post-Max). Finestra: **2026-05-20 -> ~2026-06-19** (4 settimane, prima sessione full-sovereign settimana 1).
>
> **Status 2026-05-07**: **Planning** (sprint inizia 20/05 dopo Claude Max expiration 19/05). Abbozzo preparatorio per primo onboarding sovereign.
>
> **Status update 2026-05-13 notte tarda — ACTIVE (Eduardo override)**: scope shift PLANNING -> ACTIVE per Eduardo decision "fai SPRINT_02 basta attendere è inutile". Methodological trade-off documentato: alcuni T tasks (T1 smoke + T2 dogfood + T8 plugin observation + T10 monitoring) eseguibili sotto Max con caveat di contamination metodologica (validation non e' "in assenza Max" come scope originale). T9 methodology framework effectiveness post-Max RIMANE post-Max only (cite count comparison wrapper vs Claude Code Session). T5+T7 GATED time-based.
>
> **Update 2026-05-10**: pre-validation in autonomy: **T3 hot-restart PASS** (stack ready ~12s, 38 traces preserved post 13gg+ down, regression `dogfood-ui` VALID_STACKS desync trovata e fixata, entry POST 12->13). **T4 cleanup PR esterni gia' COMPLETO** (i 4 PR target gia' triagati 7/5: #97 Game-Database closed-as-stale post-rebase abort, #105/#10/#61 mergeati). Restano per 20/05+: T1 smoke sovereign, T2 dogfood organico, T5 cost tracking, T7 review.
>
> **Update 2026-05-12 sera (post cluster Bundle 1+2+3+residual+vault handoff)**: scope amend critico necessario pre-start 20/05+. Cluster questa sessione ha introdotto NEW dimensions empirical NON considerate in original scope 2026-05-07:
> - **Plugin ecosystem MAJOR upgrade**: 3 plugins (compass v0.4.3 + superpowers v5.1.0 + claude-mem v13.2.0) + 4 marketplaces + Bun v1.3.13 + repomix v1.14.0
> - **Methodology framework MATURED**: 12 lessons L-001 + L-002..L-012 (era 3 al 2026-05-07) + 13 ADR Accepted (era 7) + ADR-0026 cognitive workflow protocols 4-protocol triple anchor
> - **Vault sibling-peer aligned**: post questa sessione 4/4 commit pushed (frontmatter + CLAUDE.md + README + M14 Cards). Cross-pattern reference candidate identified DEFER fino SPRINT_02+ Three Strikes trigger.
> - **Empirical evidence Claude Code usage intensivo**: 49 PR/6gg pre-Max = empirical justify tier 0 strategic post-Max via Claude API on-demand (ADR-0023 H7 confirmed).
>
> **Sprint objective AMENDED**: validare empiricamente scenario A (full-sovereign $0-50/anno) in uso normale + cleanup PR esterni opportunistico + cost tracking primo mese reale + raccolta dogfood organici post-closure (target soft n>=20 cumulative) + **NEW: dogfood plugin ecosystem real-use** (claude-mem hook lifecycle + superpowers skill auto-trigger + compass project-direction tracking) + **NEW: validate methodology framework effectiveness** post-Max sovereign (Protocol 1/2/3/4 application pattern via Aider/OpenCode vs Claude Code). Zero silent-corruption deve rimanere invariato.
>
> **Re-baseline 2026-05-13 pomeriggio (post harsh-reviewer #2 P0 #2 esplicit)** -- Eduardo decision "in scope":
> - **T1 Smoke wrapper sovereign**: ✅ **DONE expanded** -- 9 entries log #27-#36 + 1 retry success (entry #34 cosmetic-diff fix) + 1 bypass (entry #36 Groq autoresearch). 6/6 effective wrapper VIABLE (5 + bypass). PR cluster #78-#84 cumulative.
> - **T2 Dogfood organico continuativo**: 🟢 **IN-SCOPE residuo 6gg pre-Max** -- target soft n>=20 cumulative (current n=36 GIA' superato). Continue passive observation durante workflow normale.
> - **T3 Stack ADR-0017 hot-restart**: ✅ DONE 2026-05-10 (entry SPRINT_02 update).
> - **T4 Cleanup PR esterni**: ✅ DONE 2026-05-07 (4 PR triagati).
> - **T5 Cost tracking primo mese**: 🟢 **IN-SCOPE residuo 6gg pre-Max** -- snapshot ccusage pre-Max (~2026-05-19) + cumulative cloud spend log entry. Cumulative cluster 13/5: $0.00818 + €10 OpenAI + ~$1 harsh-reviewer (~$10.85 totale).
> - **T6 Privacy validation Synesthesia preview**: 🟡 OPPORTUNISTIC (dormant fino ago 2026, default skip).
> - **T7 Review fine sprint**: 🟢 **IN-SCOPE residuo 6gg pre-Max** -- session retrospect ~2026-05-19 mid (3 decisioni continuita / mid-correction / SPRINT_03 scope).
> - **T8 Plugin ecosystem dogfood**: 🟢 IN-SCOPE residuo 6gg pre-Max -- passive observation continua.
> - **T9 Methodology framework effectiveness**: 🟢 IN-SCOPE residuo 6gg pre-Max -- cite count Protocol 1-6 (P5+P6 NEW addendum) JOURNAL post-Max comparison.
> - **T10 Three Strikes Quality Gate**: 🟡 DEFERRED-TRIGGER (default skip, NON ratificato n=3 condition).
> - **NEW T11 Governance saturation review** (capturarsi questa session 13/5 pomeriggio): 🟡 OPPORTUNISTIC -- post-cluster cumulative 8 PR + 4 ADR review per consolidamento o trim. Lesson L-016 candidate.
> - **Governance work 13/5** (8 PR + 4 ADR + harsh-reviewer 2x + addendum P5+P6): **ACCEPTED scope-add** capturarsi come T11 + lesson L-016. NOT scope-creep silent (ora explicit re-baseline).

---

## Pre-requisiti

- Fase 6 CLOSED 2026-05-07 (ADR-0015 + ADR-0017 entrambi Accepted).
- Stack ADR-0017 scaffold opt-in: hot-restartable in <60s con `cd infra && docker compose up -d` se serve dashboard/tracing/eval.
- Wrapper aider-* in `C:\Users\edusc\.local\bin\` operativi senza Claude Max.
- API keys cloud free tier (Groq + Cerebras + Gemini) attive in `~/.config/api-keys/keys.env`.
- Privacy policy per-repo invariata (Synesthesia mixed dormant, codemasterdd cloud OK).

## Pre-flight checklist 2026-05-13 notte (status pre-trigger 20/05+, 6gg residui pre-Max)

Refresh-verify pre-trigger SPRINT_02 attivo. Cluster 12-13/5 (8 PR cumulative) ha completato base operative: H7 + cross-PC ecosystem doc + drift class IPs killed + R1-R5 BACKLOG resolved.

### Pre-req status verified

| Item | Status | Note |
|------|--------|------|
| Fase 6 + Fase 7 CLOSED | ✅ | ADR-0015 + ADR-0017 Accepted (PR #4 7/5) |
| Stack ADR-0017 hot-restart | ✅ | T3 PASS 12s up + 38 traces preserved (2026-05-10) |
| Wrapper aider-* operativi | ✅ | 4 cloud + 2 local + OpenCode v1.14.41 attivo |
| API keys cloud (Groq + Cerebras + Gemini) | ✅ | + **ANTHROPIC tier-0 added 12/5 H7 DONE** |
| Privacy policy per-repo | ✅ | + Ryzen whitelist propagation R4 DONE 13/5 |
| **NEW DHCP reservation locked** | ✅ | Lenovo `.10` Wi-Fi + Ryzen `.11` Ethernet (TIM HUB AGTHP, drift class permanent kill) |
| **NEW SSH key-based auth Lenovo->Ryzen** | ✅ | ed25519 passwordless + admin keys file |
| **NEW Vault sync 3-way** | ✅ | HEAD `1abaa743` Ryzen+Lenovo+origin (R5 DONE) |
| **NEW BACKLOG R1-R5 cleanup** | ✅ | TUTTI RESOLVED (R1 via ADR-0027 narrative drift) |

### T1-T10 readiness check pre-trigger 20/05+

| Task | Readiness | Pre-flight note |
|------|-----------|------------------|
| T1 Smoke test sovereign 3 wrapper | 🟢 READY | Candidates files identified, wrapper paths verified |
| T2 Dogfood organic continuativo | 🟢 READY | Log file `logs/aider-delegation-2026-05.md` exists, target n>=20 cumulative dataset |
| T3 Stack ADR-0017 hot-restart | ✅ **ALREADY DONE 2026-05-10** | T3 PASS anticipated, regression-checked |
| T4 Cleanup PR esterni opportunistico | ✅ **ALREADY DONE 2026-05-07** | 4/4 PR triagati (Game-Database #97/#105, compass #10, evo-swarm #61) |
| T5 Cost tracking primo mese | 🟡 GATED ~2026-06-15 | Aspetta full month post-Max data |
| T6 Synesthesia privacy preview | 🟡 OPPORTUNISTIC | Dormant fino ago 2026 (default skip) |
| T7 Review fine sprint | 🟡 GATED ~2026-06-19 | End-of-sprint scheduled |
| T8 Plugin ecosystem dogfood | 🟢 READY | 3 plugin installed 12/5 (compass + superpowers + claude-mem), observation organic durante sessioni normali |
| T9 Methodology framework effectiveness | 🟢 READY | 4 protocols ADR-0026 documented + L-001..L-014 catalog disponibile |
| T10 Three Strikes cross-pattern adoption | 🟡 DEFERRED-TRIGGER | Default expectation: NON meet entro sprint (skip OK) |

### Cumulative cluster 12-13/5 impact su SPRINT_02

**Positive multipliers** (rinforzano scenario A):
- 8 PR efficient cluster pre-Max = pattern auto-mode disciplinato + ADR-0026 protocols validato empirical
- L-014 autoresearch first pattern = available tool per future technical issues SPRINT_02
- DHCP reservation killed drift class = network stability invariata mid-sprint
- SSH cross-PC accessible = capability fleet Ryzen via wrapper se serve (es. delegation Ryzen-side experiment T8/T9)
- Vault llm-routing IP fix synced 3-way = Ollama daemon reachable senza drift Ryzen-side

**Trigger updates pre-sprint** (post v22 sprint amend):
- T8.2 superpowers skill auto-trigger pattern: ora ha `superpowers:requesting-code-review` validato primo uso reale 12/5 sera (PR #69 harsh-review) + `superpowers:consolidate-memory` invoked 13/5 notte. Observation pool partito.
- T9 protocols cite count baseline: cumulative 14/21/27/73 cite count al 2026-05-12 -> da aggiornare con cluster 13/5 cite count (P1+P2+P3+P4 applicati transparency PR #69 + #73 + #74 commit messages).
- L-014 promotion adds new methodology counter-example pool per T9 protocols validation (P2 Autoresearch reinforcement caso TIM AGTHP DHCP).

### Risk register pre-flight

| Risk | Probabilità | Mitigation |
|------|-------------|------------|
| Silent-corruption emerge T1 | LOW (zero precedent post-ADR-0008 + ADR-0011 hook globali) | T1 stop + ADR addendum reactive |
| Privacy violation Synesthesia | LOW (dormant + whitelist enforcement Lenovo+Ryzen) | Wrapper abort + log entry |
| Fail rate >15% | LOW (cumulative 26 entries 0 silent-corruption pre-sprint) | Soft monitor in JOURNAL |
| ANTHROPIC budget overrun >$20/mese | LOW (smoke test cost $0.000044, conservative use) | Auto-monitor via `logs/claude-api-spend-2026-MM.md` |
| Eduardo-direct burnout | MEDIUM (sessione 12-13/5 cumulative ~12h+ effort) | Stop-pattern L-002 attivo, no forced sprints |

### Baseline metrics snapshot pre-trigger

- Dogfood dataset cumulative: **n=26** (15 Aider + 11 OpenCode)
- Silent-corruption count: **0** (zero precedent)
- ADR Accepted: **14** (post-0027)
- Lessons promoted: **14** (L-001..L-014)
- Plugin ecosystem: 3 plugins (compass + superpowers + claude-mem)
- HEAD codemasterdd: `51d135a` (will further bump pre-trigger 20/05+)
- BACKLOG state: R1-R5 RESOLVED, C1+C2+Q3-update low-priority, H2/H3/M3/M5 trigger-conditional

## Task

### T1. Smoke test sovereign empirico [originally post-Max, IN PROGRESS 2026-05-13 notte tarda]

**T1 #1 PROGRESS 2026-05-13 notte tarda** (aider-cosmetic Qwen 7B Q4 whole on `README.md` top-level):

- Wrapper executed: ✅ no crash, edit applied "Applied edit to README.md" (6.0k tok sent / 1.3k recv)
- Outcome content: ⚠️ NON_COMPLIANT position (Qwen 7B inserito linea al FONDO file vs requested DOPO riga 3) — known 7B model limitation NON silent-corruption
- Outcome technical: ✅ no silent-corruption working tree (git diff verified 2 line addition only, no encoding corruption, em-dashes intact)
- Decision: REVERTED via `git restore README.md` (smoke output non-persistent — file pristine, modifica solo in log)
- Lesson reinforced: aider-cosmetic + Qwen 7B per file TOP-LEVEL semplici = wrapper FUNCTIONS but position-precision LIMITED. Mitigation per task content-sensitive: usare aider-refactor (14B Q2 + diff) anche per cosmetic non-trivial position requirements.

**T1 #2 + T1 #3 EXECUTED 2026-05-13 mattina (Eduardo "tutto" override)** -- entries #28 + #29 in `logs/aider-delegation-2026-05.md` (T1 #1 retro-log = #27; entries #25-#26 already used by OpenCode dogfood `empty_stats()` PR #17 + `_auth_header()` PR #18 -- cumulative dataset n=26 pre-T1 SPRINT_02):

- **T1 #2 (aider-refactor Qwen 14B Q2 + diff on `apps/dogfood-ui/dafne_client.py`)**: 🟡 PARTIAL_FAIL safe. 1/3 SEARCH block applied (init `self.last_error = None` + docstring Attributes section). 2/3 fail SearchReplaceNoExactMatch (modello generato 4-space indent SEARCH vs reale 8-space dentro def). 3 reflections exhausted + summarizer cleanup error trailing (LiteLLM `cannot schedule new futures after shutdown`). Action: REVERTED via `git restore` (partial dangling = inutile half-state). Pattern conferma ADR-0008 (safe failure NO silent-corruption) + ADR-0016 (constraint=3 + indentation precision = 14B Q2 borderline).
- **T1 #3 (aider-groq cloud llama-3.3-70b on `README.md`)**: 🔴 FAIL TPM 12000 rate-limit. 5 retry exponential backoff 2s/4s/8s/16s/32s, mai successo. ~12 minuti running prima di kill manual. Pattern: Aider context-pack (~10-11k tok/req) borderline TPM 12k Groq free tier 70B. Contraddizione apparente vs Entry #15 (smoke 7/5 PASS): hypothesis rolling TPM bucket caricato da concurrent probe debug. Cost: $0 (no token consumed billed).
- **Side-finding (NON Aider)**: PowerShell `&` invocation `aider-groq.cmd` con REM line `(free tier 6000 tok/min)` ha creato 11 file VUOTI working tree (parsing artifact). Cleanup eseguito. Trigger lesson candidate L-2026-05-015 (PowerShell wrapper invocation pattern) -- NOT silent-corruption Aider.

**T1 SPRINT_02 cumulative pass rate**: 0/3 PASS, 1/3 NON_COMPLIANT (#27 7B position), 1/3 PARTIAL_FAIL safe (#28 14B Q2 multi-block), 1/3 FAIL rate-limit (#29 Groq).

**ADR-0015 trigger check post T1 #1+#2+#3**: silent-corruption=0, fail rate=4/29=14% (cumulative dataset n=29 post T1, in linea pattern smoke pre-existing), privacy=0. **Trigger NON attivati**. Empirical confirm pattern noti (no surprise).

**Methodological caveat invariato**: T1 SPRINT_02 sotto Claude Max ACTIVE (6gg pre-Max). Validation NON "in assenza Max" come scope originale -- contamination documentata.

**Next step organic**: T1 #2 retry possibile scope ridotto (singolo block init only, constraint=1) per validare 14B Q2 + diff isolato. T1 #3 retry possibile stack alternative (Cerebras 8B small file, o gpt-4o-mini paid <$0.01).

**Manual fix consequenziale**: README.md "21 ADR" -> "28 ADR: 0001-0028" applicato manualmente Edit (Claude Code tier 0 strategic, NON wrapper delega) post-FAIL T1 #3, scope minimal 1-line stale doc fix che era target functional.

**T1 #2 retry EXECUTED 2026-05-13 mezzogiorno (scope ridotto constraint=1)** -- entry #30:

- **Task**: ridotto T1 #2 a constraint=1 isolato. Aggiungere SOLO `self.last_error: str | None = None` come ultima linea `__init__` (post `self.ping_timeout = ping_timeout`).
- **Wrapper**: `aider-refactor.cmd` (Qwen 14B Q2 + diff)
- **Outcome**: ✅ **PASS 1st-try**. Diff +1 line esatto, AST OK, posizione esatta richiesta. Tokens 7.6k sent / 52 recv. Latency ~30s (no reflection). $0 cost.
- **Action**: KEPT (foundation per future error tracking ping/_get incrementale, valid Python).
- **Empirical conferma ADR-0008 + ADR-0016**: 14B Q2 + diff PASS su constraint=1 vs PARTIAL_FAIL su constraint=3+indent (#28). Mitigation pattern: **decompose multi-block refactor in sequential single-block edits**.

**T1 SPRINT_02 cumulative pass rate post retry (n=4)**: 1/4 PASS (#30 retry), 1/4 NON_COMPLIANT (#27), 1/4 PARTIAL_FAIL safe (#28), 1/4 FAIL rate-limit (#29).

**T1 #4 EXECUTED 2026-05-13 mezzogiorno (alternative stack a Groq fail)** -- entry #31:

- **Task**: README.md `Stack attivo (aggiornato 2026-04-23)` -> `(aggiornato 2026-05-13)` (date refresh post 12-13/5 plugin ecosystem expansion). Constraint=1.
- **Wrapper**: `aider-cerebras.cmd` (Cerebras llama3.1-8b free tier + diff)
- **Mitigation**: `--map-tokens 0 --no-stream` per evitare context overflow noto Cerebras 8k limit (entry #22)
- **Outcome**: ✅ **PASS 1st-try**. Tokens 3.7k sent / 104 recv. Cost $0.00038 (free tier ma billed). Latency ~3.5min.
- **Action**: KEPT change.
- **Empirical conferma**: `aider-cerebras` viable per cosmetic doc piccoli con context mitigation. Validato 1/1 alternative stack a Groq 70B (T1 #3 FAIL TPM-rate-limit).
- **Side-finding RICORRENTE**: PowerShell `&` invocation `aider-cerebras.cmd` REM line `(free tier limited a llama3.1-8b)` ha creato 12 file VUOTI working tree (stesso pattern T1 #3). Pattern PERSISTENT cross-wrapper. **L-2026-05-015 PROMOTION rinforzato**.

**T1 SPRINT_02 cumulative pass rate FINAL (n=5)**: 2/5 PASS (#30 + #31), 1/5 NON_COMPLIANT (#27), 1/5 PARTIAL_FAIL safe (#28), 1/5 FAIL rate-limit (#29). Total cost $0.00038 (sotto $0.001 = 0.0019% $20 budget mensile).

**Wrapper validation matrix HARSH-REVIEW REVISED 2026-05-13 pomeriggio (3-colonne onesta vs precedente "VIABLE" overclaim)**:

| Wrapper | Default invocation | Mitigation richiesta | Fail mode persistente |
|---------|---------------------|----------------------|------------------------|
| aider-cosmetic (Qwen 7B) | 🔴 NON_COMPLIANT position (whole format) | ✅ PASS con `--edit-format diff` override (entry #34) | -- |
| aider-refactor (Qwen 14B Q2) | ✅ PASS constraint=1 (entry #30) | ✅ PASS multi-block con decompose pattern | 🟡 PARTIAL_FAIL constraint=3+indent (entry #28) |
| aider-cerebras (Cerebras 8B) | 🔴 FAIL context overflow 8k | ✅ PASS con `--map-tokens 0` (entry #31) | -- |
| aider-gemini (Gemini 2.5 Flash) | 🔴 24k tok sent (ignora --map-tokens 0) | ✅ PASS con `--map-tokens 0 --no-stream` (entry #32, ~6min slow) | -- |
| aider-openai (gpt-4o-mini) | 🔴 FAIL quota=0 originale | ✅ PASS post 10 EUR funding + Sharing toggle ON | -- |
| aider-groq-bypass (Groq 70B via openai/) | 🟡 FAIL "Invalid API Key" senza --api-key override | ✅ PASS con temp env-file pattern (entry #36 + P0 fix) | -- |
| ~~aider-groq~~ DELETED | -- | -- | LiteLLM Groq adapter buggy, RIMOSSO 2026-05-13 |

**Pass rate REALE n=10**: 3/7 PASS at default invocation (43%), 4/7 PASS solo con mitigation specifica required, 1/7 fail mode persistente (multi-block constraint=3+indent).

**Onesta narrative**: scenario A SOVEREIGN ha 6 path validati ma TUTTI tranne aider-refactor constraint=1 richiedono **mitigation flag specifico** (--map-tokens 0, --no-stream, --edit-format diff override, --env-file temp pattern). Workflow normale richiede consultare sempre matrice mitigation prima di invocazione, NON è "drop-in".

**Implication operativa**: pre-Max post-19/05 il wrapper di default per task sovereign organic = **aider-refactor 14B Q2 + diff** (NO mitigation flag richiesta, entry #30 PASS pulito). Cloud wrapper (cerebras/gemini/openai/groq-bypass) attivare on-demand con flag set documentati.

**ADR-0015 Accepted scenario A confermato empirical CONDIZIONATO** (n=36 cumulative, 0 silent-corruption invariato). Confermato robusto per uso disciplined con mitigation matrix referenced. NON confermato robusto per uso default-invocation drop-in.

**T1 #5 + T1 #6 EXECUTED 2026-05-13 mezzogiorno (wrapper quartet+2 completion)** -- entries #32 + #33:

- **T1 #5 (aider-gemini Gemini 2.5 Flash on REFERENCE_INDEX.md)**: ✅ **PASS 1st-try**. Date refresh `2026-04-23 post ADR-0012/13/14` -> `2026-05-13 post ADR-0027/0028`. Tokens 24k sent (Gemini sembra non rispettare --map-tokens 0 fully) / 194 recv. Cost $0.0078. Latency ~6min lento. Filename hallucination in commentary ma SEARCH/REPLACE corretto. PowerShell pollution n=3 confermato cross-wrapper (L-2026-05-015 reproduce 100%).
- **T1 #6 (aider-openai gpt-4o-mini on STATUS_MULTI_REPO.md)**: 🔴 **FAIL OpenAI quota exceeded**. 5 retry tutti rate-limit "You exceeded your current quota". NO PowerShell pollution (Aider exit veloce <30s, no parser window). NO edit attempted. Account `OPENAI_API_KEY` di Eduardo MAI funded oltre signup.

**Wrapper validation matrix POST T1 SPRINT_02 FINAL n=7**:
- ✅ aider-refactor (14B Q2 local diff) constraint=1 PASS
- ✅ aider-cerebras (Cerebras 8B + `--map-tokens 0`) constraint=1 PASS, $0.0004
- ✅ aider-gemini (Gemini 2.5 Flash + `--map-tokens 0`) constraint=1 PASS, $0.008
- 🟡 aider-cosmetic (7B local whole) NON_COMPLIANT position
- 🔴 aider-groq (Groq 70B free) FAIL TPM 12k bottleneck
- 🔴 aider-openai (gpt-4o-mini paid) FAIL quota=0 (billing setup required)
- 🟡 aider-refactor multi-block PARTIAL_FAIL safe (mitigation: decompose)

**T1 SPRINT_02 cumulative pass rate FINAL n=7**: 3/7 PASS (43%), 1/7 NON_COMPLIANT, 1/7 PARTIAL_FAIL, 2/7 FAIL. Total cost $0.00818 (0.041% $20 budget mensile).

**Verdetto wrapper ecosystem**:
- Sovereign tier 1-2: aider-refactor workhorse. aider-cosmetic limited.
- Cloud free fallback: 2/4 viable (cerebras + gemini). Groq broken, OpenAI not-funded.
- Strategic tier 0 ADR-0023: ANTHROPIC API on-demand resta default post-Max ($0.000044 smoke).

**ADR-0015 Accepted scenario A SOVEREIGN VIABLE confermato definitivamente** (n=33 cumulative, 0 silent-corruption, 2 fallback cloud + tier 0 strategic ANTHROPIC disponibile).

**Manual fix consequenziale SPRINT_02 cluster**:
- README.md "21 ADR" -> "28 ADR: 0001-0028" (Edit manual post-FAIL T1 #3)
- README.md "Stack attivo (aggiornato 2026-04-23)" -> "(aggiornato 2026-05-13)" (T1 #4 cerebras PASS)
- REFERENCE_INDEX.md "aggiornato 2026-04-23 post ADR-0012/13/14" -> "aggiornato 2026-05-13 post ADR-0027/0028" (T1 #5 gemini PASS)
- STATUS_MULTI_REPO.md target T1 #6 NON applicato (FAIL quota), date refresh deferred opportunistic post-Max o manual Edit prossima sessione.

**Lesson L-2026-05-015 PowerShell wrapper REM pollution**: n=3 instances reproducible (T1 #3+#4+#5). Pattern PERSISTENT cross-wrapper. PROMOTE candidate AA01 (Eduardo-direct).

- **Cosa**: 3 wrapper aider-* eseguiti su task piccoli reali, validation tecnica end-to-end senza Claude Max.
  - `aider-cosmetic <file>` (Qwen 7B): JSDoc/docstring/rename su 1 file -- es. `apps/dogfood-ui/db.py` o `scripts/quality-bench/run-bench.ps1`
  - `aider-refactor <file>` (Qwen 14B Q2 + diff): bug fix piccolo o cleanup logic su 1 file -- candidati: error handling helper `apps/dogfood-ui/dafne_client.py`, retry logic gia' robusto bench scripts
  - `aider-groq <file>` (cloud llama-3.3-70b): cosmetic doc su file non-sensitive -- candidati: README updates, ADR cross-references
- **File/sistemi toccati**: script in `apps/dogfood-ui/`, `scripts/`, `docs/`. **NON** toccare `controllers/`/`routes/` Synesthesia (privacy mixed).
- **Check**: post-edit `git diff HEAD~1` verify no silent-corruption; `logs/aider-delegation-2026-05.md` (nuovo file mese) entry per ognuno (classe, stack, retry, tokens, cost, esito).
- **Success**: 3/3 wrapper eseguono task senza crash; >=2/3 successo 1st-try; 0 silent-corruption working-tree.
- **Failure mode**: se 2+ crash con UnicodeEncodeError → trigger M3 (cp1252 fix re-evaluation). Se 2+ silent-corruption → ADR-0008 trigger reactive.

### T2. Dogfood organico continuativo
- **Cosa**: ogni task delegabile in workflow normale → tracked in `logs/aider-delegation-2026-05.md` (e `2026-06.md` quando arrivano). No quota, no forzatura: solo entry organiche.
- **Target soft**: dataset cumulative codemasterdd-Fase 6 da n=12 -> n>=20 entro fine sprint (8 entry organiche in 4 settimane = 2/settimana, raggiungibile naturalmente).
- **Esempi opportunistici**:
  - Modifiche docstring/comment-based-help su altri script
  - Bug fix su `scripts/hooks/commit-guard.js` se emergono nuovi falsi positivi
  - Refactor `dogfood-ui` se emergono pain points UI
  - Migration logs/aider-delegation-* a SQLite via `scripts/migrate-log-to-sqlite.py` (se non gia' fatto in ADR-0017)
- **Success**: dataset >= 18 entries entro 2026-06-19, fail rate cumulative <15%, zero silent-corruption.
- **Safety note**: T1 e' precondizione tecnica; T2 e' raccolta dati. Non confondere.

### T3. Stack ADR-0017 hot-restart procedure validation
- **Cosa**: avviare stack scaffold da zero (Docker Desktop + `docker compose up -d` + verify endpoint health) per misurare tempo reale e identificare regressioni post-13gg downtime.
- **File toccati**: nessuno (esecuzione operativa). Eventuale `docs/runbook/adr-0017-hot-restart.md` se procedure rivela edge case.
- **Check**: tempo cumulative <60s da `docker compose up -d` a `/health/readiness` 200 + Langfuse 7+ trace count preservati. Se DB corrotti -> ADR addendum.
- **Success**: stack up + dogfood-ui accessibile + 1 entry creata via UI/POST → regressione zero.
- **Failure mode**: se DB Postgres corrotti → recovery via volume backup oppure `docker compose down -v && up -d` (perdita 7+ trace acceptable, scaffold stato).

### T4. Cleanup PR esterni opportunistico
- **Cosa**: review e merge/close dei 4 PR pending fuori codemasterdd:
  - **Game-Database #97** (Codex 23gg+, +1147 righe, CI verde 8 check): review approfondita (vedere se rebase serve, se cambiamenti ancora rilevanti dopo Sprint Impronta Game). Decision: merge / close / chiedere update.
  - **Game-Database #105** (doc 1-line): merge veloce se ancora rilevante.
  - **compass-marketplace #10** (whitelist fix + test new): review e merge se test passa.
  - **evo-swarm #61** (weekly digest 27/04): valutare se digest 27/04 e' ancora utile o se va chiuso/sostituito da digest 11/05.
- **File toccati**: nessuno in codemasterdd (sono PR su altri repo).
- **Success**: 4/4 PR triagati (merge / close / comment), backlog GitHub pulito.

### T5. Cost tracking primo mese full-sovereign
- **Cosa**: fine settimana 4 sprint (~2026-06-15 +/-) → snapshot ccusage NULL (Claude Max disattivato) + sum cost cloud da `logs/aider-delegation-2026-05.md` + `2026-06.md`.
- **Target ADR-0015**: <$5/mese cloud cumulative (margine ampio vs $20 budget). Atteso: <$1/mese basato su tier 3 free + emergenza tier 4 raro.
- **Check**: proiezione su 12 mesi → conferma scenario A $0-50/anno realistico.
- **Success**: report 1-pagina in `logs/cost-snapshot-2026-06.md` con: cloud spend reale, proiezione annua, eventuali alert >budget threshold.

### T6. Privacy validation Synesthesia preview (opportunistic)
- **Cosa**: SE Eduardo riattiva Synesthesia pre-fine sprint (improbabile, target ago 2026), eseguire 1 task validation classifier con dati reali. ALTRIMENTI: skip, mantenere derogato ADR-0014 #3.
- **File toccati**: `C:\dev\synesthesia\views/` (cloud OK) o `C:\dev\synesthesia\controllers/` (sovereign-only) -- 1 task minimo.
- **Check**: classifier policy per-repo nega cloud delegation su `controllers/` (atteso) e permette su `views/` (atteso).
- **Success**: 1 entry classifier in log, ADR-0014 criterio #3 a 2/3 (preview, non chiudibile fino a 3/3).
- **Skip se**: Synesthesia ancora dormant (pattern atteso fino ago 2026).

### T7. Review fine sprint + ADR addendum se serve
- **Cosa**: sessione ~30-45min ~2026-06-19: count dogfood + cost real + delta scenario A vs prediction + decisione SPRINT_03 scope.
- **Output**: entry JOURNAL "Review SPRINT_02" + COMPACT v12 + eventuale ADR-0015 addendum se trigger ri-evaluation attivati (silent-corruption emersa, fail rate >15%, privacy violation).
- **Success**: 3 decisioni chiare -- continuita' scenario A / mid-course correction / SPRINT_03 scope.

### T8 NEW (2026-05-12 amend). Plugin ecosystem dogfood empirical
- **Cosa**: real-use dogfood dei 3 plugin installati 12/5 (compass + superpowers + claude-mem) in workflow normale SPRINT_02.
- **Sub-task**:
  - **T8.1 claude-mem hook lifecycle empirical**: verify 6 hook lifecycle (Setup + SessionStart + UserPromptSubmit + PreToolUse + PostToolUse + Stop) fires + worker port 37777 persistence cross-session
  - **T8.2 superpowers skill auto-trigger empirical**: count quale 14 skill auto-trigger durante session normale. Identify gap NON coperto -> possibile M11 #1 affaan-m cherry-pick trigger (organic, NON 1-week artificial)
  - **T8.3 compass project-direction tracking**: verify compass status comando funziona + check session start drift detection
- **Check**: ognuno empirical observation log opportunistic, NON forced
- **Success**: 3/3 plugin observed real-use almeno 5 sessioni cumulative durante sprint. Lesson cross-pattern PASS / FAIL / NEEDS-TUNING.
- **Failure mode**: se 2+ plugin friction reale -> ADR addendum reactive (disable or replace).

### T9 NEW (2026-05-12 amend). Methodology framework effectiveness post-Max
- **Cosa**: validate empirical ADR-0026 4 cognitive workflow protocols (Refresh-verify + Autoresearch + Archon + AA01) application via Aider/OpenCode/wrapper sovereign tier (vs Claude Code session).
- **Sub-task**:
  - **T9.1 Protocol 1 Refresh-verify** application via wrapper aider-* + OpenCode workflow. Verifica se friction emerge senza Claude Code real-time refresh
  - **T9.2 Protocol 4 AA01 workspace** via sovereign tier (NO Claude Code session per AA01 lifecycle). Empirical capture + classify + promote + lesson + archive
  - **T9.3 Protocol 3 Archon 7-step** application high-stakes decisions sovereign. ANCHOR_v2 system prompt invoked manually via Aider/OpenCode
- **Check**: cite count protocols JOURNAL post-Max vs pre-Max (cumulative 14/21/27/73 al 2026-05-12)
- **Success**: protocols continue applicable senza Claude Code OR identify gap requiring H7 ANTHROPIC_API_KEY (tier 0 strategic on-demand)
- **Trigger ratification**: ADR-0026 addendum E3 IF gap identified empirical (post-Max friction concreta)

### T10 NEW (2026-05-12 amend). Cross-pattern adoption Quality Gate deferred trigger
- **Cosa**: Three Strikes trigger condition monitoring per ADR-NEW Tier promotion methodology (V3 Bundle 2 research doc).
- **Trigger condition**: (1) 1 regress reale tier promotion ad-hoc + (2) 1 successful manual application Quality Gate Step methodology + (3) 1 emergent tier promote request (es. new Ollama model rotation)
- **Success**: SE Three Strikes meet -> ADR-NEW draft + research doc cross-link a Bundle 2 V3 + vault Quality Gate methodology reference
- **Skip se**: Three Strikes NON meet entro fine sprint (default expectation, methodology DEFER mantained)

## Trigger ADR (ri-evaluation soft-override ADR-0015)

Soft-override n>=12 di ADR-0015 e' valido se durante SPRINT_02 NON emergono questi pattern:

- **silent-corruption working-tree** >=1 caso reale (non test) -> hard blocker, ADR-0015 addendum + switch potenziale a scenario B (Claude Pro $240/anno acquisition revisited)
- **fail rate cumulative** >15% (oltre margine sicurezza) -> revisione routing tier
- **privacy violation** in repo non-sensitive (cloud delegation leak su `controllers/` Synesthesia o repo cliente futuro) -> hard blocker, ADR addendum

Se nessun trigger emerge a fine SPRINT_02 -> Fase 7 stabilizzata, scenario A confermato per anno fiscale.

## Safety notes

- **Zero subscription ricorrenti**: target ADR-0001 + ADR-0015. Se emerge bisogno di Claude Pro $240/anno → ADR addendum esplicito, NO acquisition silent.
- **Privacy per-repo rigorosa**: codemasterdd cloud OK; Synesthesia controllers/ sovereign-only; eventuali repo cliente sovereign-only sempre.
- **No --force su main, no --no-verify**: invariato.
- **Conventional Commits**: invariato (cross-agent enforced via hook globale).
- **Encoding ASCII-first** per nuovi doc (ADR-0021): em-dash convention solo titoli ADR.
- **Stack ADR-0017 opt-in**: Docker Desktop start manuale solo quando si usa dashboard/tracing/eval. Default: stack down.

## Out of scope

- Fixing Game ROSSO findings (boss enrage + XP curve): Sprint Impronta in corso, attendere quiet window post-CAP-NN
- Synesthesia work proattivo: dormant fino ago 2026 by design
- Dafne Atto 2 detail: governance vive in evo-swarm repo, monitorato da codemasterdd via STATUS_MULTI_REPO
- AA01 task PROPOSED del 25/04: workspace separato da codemasterdd, decide Eduardo standalone
- Mac mini come device secondario: deferred ADR-0021 finchè non emerge trigger

## Working rule per questo sprint

Ogni task delegato via wrapper aider-* genera entry organica in `logs/aider-delegation-2026-MM.md`. Niente forzatura quota: se in 4 settimane il workflow naturale produce 5 entries, OK; se ne produce 15, OK. Il punto e' validare scenario A in uso normale, non collect data per data.

Se emerge un trigger ADR (silent-corruption, fail rate spike, privacy leak) → stop sprint, ADR addendum reactive prima di continuare.
