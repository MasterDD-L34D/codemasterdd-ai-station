# ADR 0008 — Silent corruption Aider whole format + Qwen 14B Q2, task-routing come mitigation

**Status**: Accepted
**Data**: 2026-04-21
**Decisore**: Eduardo Scarpelli
**Tipo decisione**: tecnica (revisione critica ADR-0007), safety-level

## Contesto

### Motivazione

ADR-0007 aveva raccomandato **Aider + Qwen 14B Q2_K + edit-format `whole`** come stack sovereign per edit agentic, basato su test `--message` single-shot sul controller Synesthesia (~180 righe). Era stato identificato un fail rate ~10-20% per "format variance" (edit respinti), qualificato come **safe failure** (file intatto, working tree pulito).

Follow-up pianificato in ADR-0007: test Aider in cmd.exe interattivo. Nel corso di questo test è emerso un failure mode **più grave e non documentato** in ADR-0007: **silent corruption**.

### Obiettivi investigazione

1. Isolare se il bug è specifico di modalità interattiva, dimensione file, edit format, o modello
2. Determinare se ADR-0007 ha sottostimato il rischio per uso produttivo
3. Identificare mitigation viable mantenendo target sovereign

## Setup test

- **Client**: Aider 0.86.2 (stessa install ADR-0007)
- **Backend**: Ollama 0.21.0 con env vars Blackwell-optimized (ADR-0004), `OLLAMA_CONTEXT_LENGTH=8192` (ADR-0007 default)
- **Modelli**: `qwen2.5-coder:14b-instruct-q2_K` (primario), `qwen2.5-coder:7b` (confronto)
- **Progetto test**: `C:\dev\aider-tty-test\` — repo isolato throwaway con `demo.js` variabile (9 righe minimali → 46 righe realistiche con class + helpers)
- **Prompt target**: "Add JSDoc comments to all functions and class methods in demo.js. Do not change any logic."

## Test eseguiti

### Test 1-2 — 14B Q2 + whole + interactive (cmd.exe)

**Risultato 2/2 run riprodotto**:
- Aider mostra in output un diff apparentemente corretto (due hunks: uno distruttivo, uno costruttivo con JSDoc)
- Aider stampa `Applied edit to demo.js`
- Auto-genera commit message: `docs: add JSDoc comments to functions in demo.js`
- **Stato su disco**: `demo.js` contiene letteralmente la stringa `demo.js` (1 riga)
- Git stats: `1 insertion(+), 9 deletions(-)` — il contrario dell'intento

### Test 3 — 14B Q2 + whole + `--message` single-shot

Stesso file 9 righe, mode non-interattivo (per escludere interactive come trigger).

**Risultato**: identico ai test 1-2. File → `demo.js`. Commit con messaggio misleading. Output Aider mostra JSDoc applicato, disco ha garbage.

**Conclusione**: il bug **non è interactive-specific**.

### Test 4 — 14B Q2 + whole + file ingrandito (46 righe realistiche)

`demo.js` sostituito con 46 righe (5 funzioni + class `Calculator` con history). Stesso prompt.

**Risultato**: **riprodotto**. File → `// demo.js` (stavolta con commento prefisso). Git stats: `1 insertion(+), 46 deletions(-)`. Output Aider mostra JSDoc applicato.

**Conclusione**: il bug **non è size-dependent**.

Nota collaterale: Qwen ha auto-tradotto il commit message in italiano (`docs: Aggiungi JSDoc a tutte le funzioni...`), behavior inconsistente rispetto a prompt inglese — signal di noise sul model.

### Test 5 — 14B Q2 + **edit-format `diff`** + file 46 righe

Stesso setup ma con `--edit-format diff` (SEARCH/REPLACE) invece di `whole`.

**Risultato**: **safe failure**.
- Qwen produce 8 blocchi SEARCH/REPLACE ben formati
- **Senza** il filename header richiesto da Aider prima del primo fence
- Aider respinge: "Bad/missing filename. The filename must be alone on the line before the opening fence"
- 1 reflection retry → "Ok." (2 token) → stop
- **Zero scritture su disco**, file 46 righe intatto
- Llama runner terminated retry all'avvio (tipico di questa config, recoverable)

**Conclusione**: `diff` edit format **elimina silent-corruption** ma non risolve format compliance di Qwen 14B Q2 → improduttivo ma safe.

### Test 6 — **Qwen 7B** + whole + file 46 righe

Stesso file, prompt, edit format `whole` ma con **modello 7B** al posto di 14B Q2.

**Risultato**: ✅ **SUCCESS pulito**.
- Qwen 7B output whole-file con **filename `demo.js` su riga propria fuori dal code block** (formato nativo Aider)
- Aider parser applica correttamente
- File 93 righe (46 originali + 47 JSDoc)
- Git stats: `47 insertions(+), 0 deletions(-)` — pure additions
- Tutti function/method commentati con JSDoc
- **Logica preservata byte-perfect**

Caveat minore: JSDoc di `sum` posizionato sopra `DEFAULT_PRECISION` (not `sum`) — non semantic, JSDoc non associato al const. Issue cosmetico.

Auto-translate del commit message ancora presente (`docs: Aggiungi JSDoc comments to all functions and class methods in demo.js.`).

**Conclusione**: il bug è **Qwen 14B Q2-specific** (output format preference incompatibile con Aider `whole` parser).

## Matrice risultati

| # | Modello | Edit format | Mode | File size | Esito | Corruption |
|---|---------|-------------|------|-----------|-------|-----------|
| 1 | 14B Q2 | whole | interactive | 9 | silent corruption | sì |
| 2 | 14B Q2 | whole | interactive | 9 | silent corruption | sì |
| 3 | 14B Q2 | whole | --message | 9 | silent corruption | sì |
| 4 | 14B Q2 | whole | --message | 46 | silent corruption | sì |
| 5 | 14B Q2 | diff | --message | 46 | safe failure (no edit) | no |
| 6 | **7B** | whole | --message | 46 | **success** | **no** |

## Root cause

Qwen 14B Q2_K per task "edit single file" emette sistematicamente **due code blocks consecutivi**:

```
<narrative text>

```
demo.js                  ← block 1: solo filename (o `// demo.js`)
```

```javascript
<contenuto completo>     ← block 2: contenuto atteso
```
```

Aider `whole` parser si aspetta:

```
demo.js                  ← filename FUORI dal block
```
<contenuto>              ← UN solo block
```
```

Quando Aider vede il pattern 14B Q2 (filename-dentro-block + separate content block), interpreta il **primo block come contenuto completo** per il file (content = `demo.js` o `// demo.js`), sovrascrive il file con quella stringa, e ignora il secondo block (ma lo stampa nell'output dando impressione che sia stato applicato).

**Qwen 7B** emette il formato corretto (filename fuori dal block), quindi non triggera il bug.

**Conferma comportamento in ADR-0007**: il test controller Synesthesia era andato a buon fine perché Qwen 14B Q2, su contesto più ricco (repo-map grande + controller reale), produsse output nel formato corretto. Il pattern "due block" emerge con contesto povero (file piccolo, prompt semplice). **ADR-0007 non ha fallito — ha testato condizioni dove il bug non si manifesta, e ha generalizzato troppo.**

## Decisione

### Dual-stack task-routing

Adottare **routing esplicito task→stack** invece di uno stack unico:

| Classe task | Stack | Rationale |
|-------------|-------|-----------|
| **Cosmetic edit** (JSDoc, docstrings, comments, rename variabili, lint-fix) | **Aider + Qwen 7B + whole** | 7B output format compatibile; faithfulness non critica (solo commenti/rename) |
| **Behavior-critical edit** (refactor, bug fix, logic change minimale) | **Aider + Qwen 14B Q2 + `diff`** | Safe failure (no silent corruption); richiede retry manuale ma previene danno |
| One-shot query (explain, discuss) | `ollama run qwen2.5-coder:7b` | Invariato da ADR-0007 |
| Read + inference | Aider + Qwen 7B (`--chat-mode ask`) | Invariato da ADR-0007 |
| CREATE single file | Aider + Qwen 7B + whole | Invariato da ADR-0007 |
| Multi-file refactor complesso | Claude API / Pro | Invariato da ADR-0007 |

### Scartato esplicitamente

- **Aider + Qwen 14B Q2 + `whole`** (ex raccomandazione ADR-0007 per edit agentic): **deprecato**. Silent corruption rischio non accettabile per workflow produttivo senza supervisione diff-by-diff manuale.
- **Sostituzioni prompt-engineering** per forzare Qwen 14B Q2 al formato corretto: non valutate come soluzione robusta — dipendenza su istruzioni specifiche per-caller, alta fragilità, nessuna garanzia.

### Safety protocol per uso produttivo

Indipendentemente dallo stack scelto:

1. **Mai `--yes-always` in repo con working tree sporco o cambiamenti non-committati importanti**. Auto-commit di Aider può "sigillare" un silent corruption.
2. **Sempre review diff post-edit** (`git diff HEAD~1` o equivalente) prima di pushare.
3. **Commit messages generati dall'LLM vanno letti con scetticismo** — riflettono l'intent del prompt, non necessariamente il diff applicato.
4. Aider auto-commit può essere disabilitato con `--no-auto-commits` per forzare review manuale; valutare come default per task behavior-critical.

## Implicazioni per ADR-0007

ADR-0007 resta valido per:
- Benchmark throughput (tabella 7B/14B Q3/14B Q2 invariata)
- Config Ollama env vars (invariate)
- Findings su paradox quantization (Q2 > Q3 faithfulness) — confermato su controller test
- Scartare Q3 (varianza output intermittente)
- Scartare Cline per local LLM

ADR-0007 è **superato** per:
- Raccomandazione singola "Aider + 14B Q2 + whole" → sostituita da task-routing (questo ADR)
- Qualifica "safe failure mode" per Aider → **falso** nel caso 14B Q2 + whole; vero solo per diff edit format

Annotare header ADR-0007 con forward reference a questo ADR.

## Implicazioni per Roadmap Sovereign (ADR-0001)

### Budget scenario

Nessun impatto **immediato** su stima budget (ibrido $300-420/anno resta baseline). Però:

- Il task-routing aggiunge **cognitive overhead** per l'utente: "quale stack per questo task?". Se in uso reale risulta frizione alta, può spingere verso Claude Pro fallback più spesso → scenario ibrido si stabilizza.
- Alternative se overhead del dual-stack risulta insostenibile: solo 7B + whole con accettazione hallucination ~20-30%, oppure 14B Q2 + diff accettando fail rate alto ma safe.

### Metriche da tracciare post-19/05

ADR-0007 aveva definito: "3 mesi uso reale → misurare fail rate". Con ADR-0008 aggiungere:

- [ ] Quanti task cosmetic vs behavior-critical in pratica quotidiana (determina utility dual-stack)
- [ ] Fail rate 7B su cosmetic (atteso: 10-20%)
- [ ] Fail rate 14B Q2 + diff su behavior-critical (atteso: 20-40% safe fail, zero corruption)
- [ ] Casi borderline dove user sbaglia routing (cosmetic erroneo su 14B Q2 / behavior-critical su 7B)

### Hardware upgrade priority

Leggermente aumentata. Un RTX 5060 Ti 16GB permetterebbe 14B Q2 full-GPU + eventualmente testare Qwen 3 Coder o deepseek-coder 14B+ alternativi che potrebbero evitare il format quirk di Qwen 14B Q2. Non critico, resta post-19/05.

## Follow-up

### Immediato
- [x] ADR-0008 scritto
- [x] ADR-0007 annotato con forward reference
- [x] CLAUDE.md priority table aggiornata (cosmetic → 7B, behavior-critical → 14B Q2 diff)
- [x] JOURNAL 2026-04-21 entry
- [x] Wrapper script `aider-cosmetic` + `aider-refactor` in `C:\Users\edusc\.local\bin\` (zero-friction invocation)
- [x] Guard rail pre-commit hook installato globale via `git config --global core.hooksPath` — testato 3 scenari (pattern pulito, pattern commentato, edit legittimo)
- [x] Delegation protocol documentato in `docs/patterns/delegation-to-aider.md`
- [x] Hub model consolidato: Claude Code orchestra via bash `--message`, user stays in chat. Delegation doc riscritto hub-first.
- [x] Dogfood completo: 7B cosmetic (commit `9280e1b`) + 14B Q2 refactor (commit `fffcbda`) entrambi success via hub.
- [x] Tracking log template `docs/patterns/aider-delegation-log-template.md` per Fase 6 evaluation.

### Addendum 2026-04-21: reflection retry resilience (diff format)

Durante il dogfood behavior-critical è emerso un comportamento non catturato dai test originali di questo ADR: **Aider diff format + Qwen 14B Q2 ha reflection retry resilience**. Quando Qwen emette SEARCH/REPLACE senza filename header (il failure mode del Test 5 di questo ADR), Aider chiede correzione → Qwen self-corregge al 2° tentativo → edit applicato pulito.

Questo non cambia la decisione ADR-0008 (diff resta strettamente migliore di whole per safety), ma **alza la viability reale della route behavior-critical**. Fail rate stimato ~20-40% era basato su `--yes-always` + nessuna reflection; con reflection default (3 retry), una parte delle "safe-fail" si converte in "delayed success". Dati puliti attesi dal tracking log post-19/05.

### Addendum 2026-04-21: hook coverage extended + cross-language validation

**Battery 9 edge case** testati contro il guard rail pre-commit hook:

| Scenario | Esito iniziale | Post-patch hook |
|----------|----------------|-----------------|
| Filename plain (`demo.js`) | block ✅ | block ✅ |
| Linea-commento (`// file`, `# file`, `; file`, `-- file`) | block ✅ | block ✅ |
| Subdir basename (`src/x/y.js` con content `y.js`) | block ✅ | block ✅ |
| Subdir full path (`src/x/y.js` con content `src/x/y.js`) | block ✅ | block ✅ |
| HTML/XML comment (`<!-- file -->`) | miss ❌ | **block ✅** |
| C-block comment (`/* file */`) | miss ❌ | **block ✅** |
| Trailing whitespace (`file   `) | block ✅ | block ✅ |
| Empty file | pass ✅ | pass ✅ (skip corretto) |
| Legit short content (~40 bytes valido) | pass ✅ | pass ✅ (no false positive) |

Hook esteso con 8 needle addizionali (`<!-- $file -->`, `/* $file */` e loro varianti). **Coverage attuale: 9/9 scenari testati**, rimangono gap teorici solo su pattern non realistici (file >200 bytes con filename ripetuto, documenti completamente a-strutturali).

**Cross-language validation**: hub testato anche su Python (inventory.py 86→159 righe con PEP 257 docstrings, commit `26ee1a5` nel repo `aider-tty-test`). **Reproducibility 7B+whole**: n=3 success cumulativi (JSDoc JS ×2 + docstrings Python ×1). Nessuna modifica config necessaria tra linguaggi.

### Test ulteriori (bassa priorità)
- [ ] `udiff` edit format: se anche diff migliora, potrebbe bypassare i due issue (silent corruption + filename header)
- [ ] Prompt-engineering esplicito per Qwen 14B Q2 "emit filename on its own line before the code block" — verificare se fa cambiare pattern output sufficientemente da recuperare whole format (bassa fiducia, comunque da documentare)
- [ ] Test su task non-cosmetic: refactor funzione, rename API signature — dove entra in gioco il routing a 14B Q2 diff
- [ ] Reproducibility 7B success su ≥3 run (n=1 attuale, tokens-cheap, quick)

### Da valutare quando si userà davvero lo stack (post-19/05)
- [ ] File-watcher/hook che rifiuta commit dove `git show HEAD` contiene solo filename come contenuto (guard rail automatico contro silent corruption)
- [ ] Wrapper script bash/ps1 `aider-cosmetic` e `aider-refactor` che preimpostano modello + edit-format correti per ridurre cognitive load

## Lezioni meta

### "Safe failure mode" è un'asserzione, non una proprietà

In ADR-0007 era data per scontata la safe-failure di Aider (fail → no-edit). Era un'inferenza dal framework "whole-file vs SEARCH/REPLACE = robust-first" (ADR-0007 Findings). Test empirici hanno mostrato che **robust-first non implica safe-failure**: parser può accettare input malformato e scrivere garbage in silenzio.

Per dichiarazioni di safety serve evidenza empirica su failure mode specifico, non inferenza da architettura generale.

### Display output ≠ on-disk state

Aider mostra all'utente ciò che il parser *dichiarava di aver applicato*. Non necessariamente ciò che è stato scritto. Nel flow `whole` con output malformato, il parser applica `block[0]` ma stampa `block[1]` perché è quello "che sembra il contenuto vero".

**Meta-regola**: per client agentici che mostrano diff preview, distinguere tra "cosa l'LLM ha detto" e "cosa hai scritto sul disco". Verification via `git diff HEAD~1` dopo l'auto-commit è rapida e cattura queste divergenze.

### Test di generalizzazione

ADR-0007 ha testato su 1 file reale (controller) + 1 prompt realistico → success. Ha poi generalizzato a "stack viable". Il bug si manifesta in condizioni apparentemente più semplici (file dummy piccolo). Ciò insegna: **test in condizioni "troppo semplici per fallire"** catturano bug che i test complessi mascherano (il context complesso può nascondere il format quirk).

Protocol futuro per validare uno stack LLM-based:
1. Test happy-path su file realistico (come ADR-0007)
2. Test edge-case "trivialmente piccolo" (come ADR-0008)
3. Test edge-case "formato diverso di output" (multi-block, narrative-heavy, conversational)
4. Test con reset repo + diff-check su on-disk state, non affidarsi a display output

### Task-routing come safety net strutturale

Invece di cercare "il modello perfetto per tutti i task", accettare che modelli diversi eccellono in task-space diverso e routare esplicitamente. Overhead cognitivo reale, ma:
- Previene single-point-of-failure
- Permette di spremere value da ciascun modello nel suo sweet-spot
- Naturalmente evolvibile: nuovi modelli si inseriscono nella matrice senza disruption

## Riferimenti

- ADR-0001 Sovereign AI Strategy: `0001-sovereign-ai-strategy.md`
- ADR-0007 Aider + Qwen quantization findings (predecessore, annotato): `0007-aider-qwen-quantization-findings.md`
- Aider edit formats doc: https://aider.chat/docs/more/edit-formats.html
- Test artifacts: `C:\dev\aider-tty-test\` (directory throwaway, history git preservata per ispezione commit malformati)
