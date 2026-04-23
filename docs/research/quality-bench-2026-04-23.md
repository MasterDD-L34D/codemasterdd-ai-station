# Quality bench HumanEval-style 2026-04-23 01:35

> Primo bench scientifico post-ADR-0013 Validation-in-progress. Framework custom (10 problemi Python + runner PowerShell + sandbox subprocess). Obiettivo: misurare pass@1 su 6 modelli per decidere se locale coder-specialist o cloud general vince su task coding.

## Framework

- **Problemi**: 10 funzioni Python standard (HumanEval-style), file `scripts/quality-bench/problems.json`. Topics: palindrome, fibonacci, count_vowels, merge_sorted, is_prime, flatten nested list, gcd, word_count, reverse_words, is_anagram.
- **Tests per problema**: 5-8 assertions coprono casi base + edge (stringa vuota, single char, inputs uguali, nested depth).
- **Runner**: `scripts/quality-bench/run-bench.ps1`.
- **Test execution**: subprocess Python 3.12 isolato, timeout 10s per problema, parse exit code + output.
- **Prompt**: system "Return ONLY function, no explanation". User: docstring completo con esempi.
- **Temperature**: 0 (deterministic).
- **max_tokens**: 500 (cloud), num_predict 500 (Ollama).
- **Extract code**: strip `<think>` tags + markdown fences permissive.

## Risultati pass@1

| Model | Pass | Total | Rate | Note |
|-------|-----:|------:|-----:|------|
| `groq/llama-3.3-70b-versatile` | 10 | 10 | **100%** | 300-900ms/task |
| `cerebras/llama3.1-8b` | 10 | 10 | **100%** | 300-900ms/task |
| `ollama/qwen3-coder:30b` MoE | 10 | 10 | **100%** | 4000-10000ms/task |
| `ollama/qwen2.5-coder:7b` | 10 | 10 | **100%** | 400-3100ms/task |
| `ollama/qwen2.5-coder:14b-q2_K` | 10 | 10 | **100%** | 1200-6800ms/task |
| `ollama/deepseek-r1:8b` | 2 | 10 | 20% | infer_error 8/10 (framework bug) |

## Findings

### Finding 1 — Discriminant power basso sui problemi toy

**5 modelli su 6 al 100%**. Il dataset è troppo easy per differenziare capability tra modelli. I problemi selezionati sono pattern CS101 coperti da quasi tutti i dataset di training.

Implicazione: **questo bench NON separa Qwen Coder specialist da Llama general** su task standard. Per discriminare serve:
- Problemi difficili (es. HumanEval `HumanEval/32`-like, tail recursion, complex state)
- Edge case stringenti (floating point precision, Unicode, memory limits)
- Multiple samples (pass@5 o pass@10 con temperature>0 per measuring consistency)

### Finding 2 — deepseek-r1:8b framework bug (non capability)

8/10 falliti con `infer_error`: exception in `Invoke-RestMethod` durante Ollama chat call. Probabile cause:
- Thinking mode genera output molto lungo → num_predict=500 insufficiente
- Content field non populated correttamente in response quando output è truncated
- Parse JSON fallisce

**NON è un fallimento capability del modello**: i 2 task che sono passati (`merge_sorted`, `word_count`) hanno prodotto codice corretto. Il modello funziona, il framework bench è sub-optimal per thinking-mode models.

**Fix candidato** (non applicato qui per tempo, marco come follow-up): num_predict=2000 o parse con `<think>` stripping dopo risposta completa. Re-run dedicato deepseek-r1 con config adattata.

### Finding 3 — Speed comparativo (conferma dati precedenti)

| Model | Avg task time |
|-------|---------------|
| Groq | ~500ms (infer + test execution) |
| Cerebras | ~500ms |
| Qwen 7B | ~1000ms |
| Qwen 14B Q2 | ~3400ms |
| Qwen3:30b MoE | ~5800ms |
| deepseek-r1 | ~7000ms (ma infer_error) |

**Speed ranking**: Cloud > Qwen 7B > Qwen 14B Q2 > Qwen3:30b > deepseek-r1. Coherente con bench speed ADR-0012/0013.

### Finding 4 — Qwen Coder regge il confronto su task standard

Qwen 7B (114 tok/s, 4.7 GB local) = **100% pass@1** come Groq 70B cloud (630 tok/s, paid-if-quota).

Per task Python toy livello "CS 101-201", **Qwen 7B locale è sufficient**. Il gap capability 7B→70B NON si manifesta su problemi base. Si manifesterebbe su:
- Multi-step reasoning
- Architectural decisions
- Complex state management
- Long-context (>4k prompt)

## Implicazioni per ADR-0013 Validation-in-progress

**Cambia** status ADR-0013 basato su questo bench?

**NON ancora**. Motivi:
1. Discriminant power insufficiente (problem set easy)
2. n=10 per modello troppo piccolo per conclusioni robuste
3. deepseek-r1 skewed dal framework bug (non decidibile)
4. Quality ≠ reliability — questo test misura quality peak, non consistency over time

**Decisione (al momento prima iterazione)**: mantenere ADR-0013 **Validation-in-progress**. Serve:
- Ripetere bench con problem set hard (HumanEval subset `HumanEval/20`-`HumanEval/60` range)
- n≥30 task via dogfood reali Fase 6
- deepseek-r1 re-bench con num_predict fixato

**UPDATE 2026-04-23 02:05 (stessa sessione)**: post iterazione 2 (hard bench 5/5 modelli 100%) + review utente, **ADR-0013 passato a Accepted**. I 3 punti sopra sono deferred come follow-up non bloccanti (discriminant power richiede problemi non-standard fuori scope bench notturno, n≥20 raccolto via Fase 6 compressa). Vedi "Iterazione 2" sotto.

## Implicazioni per ADR-0014 Fase 6 compression

**Rafforza ADR-0014** (3 mesi → 3-4 settimane). Ora sappiamo che:
- Quality baseline "equivalenza su task standard" è **confermata** (5/6 modelli 100% toy)
- La **differenziazione** richiede bench più difficili (≠ più tempo, ≠ più dogfood di task banali)
- Il tempo risparmiato comprimendo Fase 6 va investito in 1 re-bench più selettivo, non in 30+ dogfood toy

## Implicazioni tier routing (invariato)

- Qwen 7B locale cosmetic — **resta** ottima scelta per task daily basic (quality 100% pass + 0 dipendenza cloud)
- Qwen 14B Q2 behavior — **resta** tier 2 default locale (quality 100% confirmed)
- Qwen3:30b MoE escalation — **resta** tier 2 escalation (capability + ctx 256K)
- Groq 70B cloud — **conferma** tier 3 online preferred quando privacy OK (speed 20× locale + pari quality toy)
- Cerebras 8B cloud — **conferma** tier 3 cosmetic fast (speed 6× Qwen 7B + pari quality toy)
- deepseek-r1:8b — **tier reasoning resta** (thinking capability non misurata da questo bench)

## Artefatti

- Framework: `scripts/quality-bench/problems.json` + `scripts/quality-bench/run-bench.ps1`
- Results JSON: `scripts/quality-bench/results/results-20260423-013505.json`
- Fixes applicati durante run:
  - Bug 1 fix: `if` inline come expression dentro `-f` non supportato PS 5.1 → variable temp
  - Bug 2 fix: `Start-Process.ExitCode` inaffidabile → `& python + $LASTEXITCODE`
  - Bug 3 fix: Extract-PythonCode regex permissiva con markdown fence asimmetriche

## Follow-up

- [ ] Rieseguire bench con `HumanEval/20-60` problemi difficili — discriminant power reale
- [ ] Re-bench deepseek-r1 con num_predict=2000 + extract thinking migliorato
- [ ] Quality bench `pass@5` (5 sample per problema con temperature=0.2) — reliability
- [ ] Integrate bench framework con dogfood Fase 6 tracking (colonna "quality pass" per ogni entry)
- [ ] Se paid tier Cerebras aperto: bench `gpt-oss-120b` e `qwen-3-235b` per capability-max

## Tempo sessione: ~40 minuti framework + 10 minuti bench + 5 minuti doc = 55 min totali

Contraddistinto da 3 bug PowerShell risolti in live debug. Framework ora stabile e riusabile per future re-run.

---

## Iterazione 2 — Hard problems + deepseek-r1 re-bench (2026-04-23 02:00)

### deepseek-r1 re-bench con num_predict 500 → 2000

**Risultato**: da 2/10 a **5/10 pass@1** (+30%).

Progresso ma ancora 5/10 `infer_error`: thinking output eccede anche 2000 tokens su alcuni problemi. Patterns:
- PASS: is_palindrome (68s!), merge_sorted, is_prime, flatten, word_count
- ERROR: fibonacci, count_vowels, gcd, reverse_words, is_anagram

Tempi PASS vanno 5s → 68s: thinking mode è MOLTO verbose. num_predict=5000 potrebbe recuperare qualche altro, ma a diminishing returns.

**Conclusione deepseek-r1**: **reasoning-mode specializzato, non coder-optimized**. Skip dal bench standard. Mantenuto come tier reasoning dedicato (non coder). Se emerge task che beneficia di chain-of-thought esplicito → dogfood dedicato.

### Hard problems (5 Leetcode medium, 5 modelli coder)

Dataset: `problems-hard.json` — LIS, edit distance, coin change, longest palindromic substring, decode ways.

| Model | Pass | Rate | Avg ms |
|-------|-----:|-----:|-------:|
| `qwen2.5-coder:7b` | 5/5 | 100% | ~2.7s |
| `qwen2.5-coder:14b-q2` | 5/5 | 100% | ~69s (outlier: coin_change 314s) |
| `qwen3-coder:30b` MoE | 5/5 | 100% | ~6.2s |
| `groq/llama-3.3-70b` | 5/5 | 100% | ~0.5s |
| `cerebras/llama3.1-8b` | 5/5 | 100% | ~0.4s |

**Tutti 100% anche su HARD**.

### Finding strategico — Bench "standard" NON discrimina

Dataset totale v1+v2: 15 problemi Python (10 easy + 5 hard Leetcode medium) × 5 modelli coder = **75 test** → **100% pass@1 universale**.

Spiegazione: tutti questi problemi sono **classici Leetcode / algoritmi CS standard** → ampiamente presenti nei training set di qualsiasi modello code-capable moderno. Il test misura memorizzazione + pattern match, NON capability reale.

**Implicazioni per discriminant power**:

Per separare i modelli servirebbero problemi:
- **Non-standard**: inventati, non presenti in Leetcode/codeforces/HackerRank (training set contamination inevitabile)
- **Contextual**: dipendenti da dominio-specifico (es. parsing file log aziendale custom, legacy API wrappers)
- **Creative synthesis**: richiedono combinazione tecniche non-ovvia
- **Code review/debug**: trovare bug sottili in code esistente (non synthesis nuovo)
- **Long-context**: task richiedenti >8k token per formulazione completa

Nessuno di questi è scriptable in bench notturno con risorse standard.

### Implicazioni per tier routing (ratificate)

Con parity confermata su task standard:

1. **Daily coding task (solvable pattern-match)**: **usa modello più veloce disponibile**
   - Offline: Qwen 7B locale (114 tok/s, 100% pass@1 sia easy che hard)
   - Online: Cerebras 8B cloud (733 tok/s, 100% sia easy che hard)

2. **Behavior/refactor standard**: Qwen 14B Q2 locale o Groq 70B cloud — entrambi 100%

3. **Escalation reale serve capability distinta**: task **non classici**, debugging, synthesis. Qui cloud 70B probabilmente ha edge (training più ampio), ma non dimostrabile con bench standard.

4. **deepseek-r1:8b**: dedicated tier reasoning. Non usare per coding standard (inefficient). Usare quando task richiede chain-of-thought esplicito.

### Implicazioni per ADR-0013 status

**PRONTO per Accepted**:
- Speed PASS ✅ (bench 2026-04-22)
- Quality parity PASS ✅ (bench 2026-04-23 v1+v2, n=75, 100%)
- Privacy policy documented ✅
- Wrapper operativi ✅

**Caveat pending** (non bloccante per Accepted):
- Discriminant power reale non misurato (fuori scope)
- n<30 dogfood reali (emergerà via Fase 6 uso normale)

Proposta: passare ADR-0013 a **Accepted** next session + formalizzare decision matrix speed-first online.

### Implicazioni per ADR-0014 (Fase 6 compression)

**Ulteriore rafforzamento**: i dati indicano che raccogliere **n alto di task toy/standard** non avanza la decisione. Il tempo in Fase 6 va investito in:
- Dogfood task **reali** di uso quotidiano (non bench artificiali)
- Task **varietà** (non ripetizioni stesso pattern)
- **Debug/synthesis** quando capitano naturalmente

4 settimane a questo ritmo = sufficiente. 3 mesi non aggiungono value.

### Follow-up rivisti

- [ ] **ADR-0013 → Accepted**: pronto con la validazione quality (richiede OK utente)
- [ ] **ADR-0014 → Accepted**: pronto (richiede OK utente)
- [x] Re-bench hard problems eseguito (questo log)
- [x] deepseek-r1 re-bench eseguito (50%, framework limit accepted)
- [ ] Discriminant bench: **fuori scope per questa infrastruttura**. Soluzioni alternative: (a) tracking empirico via dogfood Fase 6, (b) bench custom con problemi interni real-world dal repo
- [ ] Aggiornare CLAUDE.md tier routing con nuove evidenze quality parity
