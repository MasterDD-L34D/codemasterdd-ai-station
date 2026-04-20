# ADR 0006 — Cline + Qwen 7B viability per workflow agentic locale

**Status**: Accepted
**Data**: 2026-04-20
**Decisore**: Eduardo Scarpelli
**Tipo decisione**: tecnica, strategica (impatto su roadmap Fase 2 di ADR-0001)

## Contesto

### Obiettivo test

Validare se **Cline** (extension VSCode per agentic coding) + **Qwen 2.5 Coder 7B** (via Ollama locale) costituiscono workflow agentic viable come sostituzione di Claude Code + Claude Max.

Primo concreto test della "Fase 2 — transizione" pianificata in ADR-0001 (Sovereign AI Strategy).

### Setup test

- **IDE**: VSCode 1.116.0
- **Extension**: Cline `saoudrizwan.claude-dev` v3.79.0 (installata 2026-04-20)
- **Backend LLM**: Ollama 0.21.0 con env vars Blackwell-optimized (vedi ADR-0004)
- **Modello**: Qwen 2.5 Coder 7B (Q4_K_M, ~6.2 GB VRAM), throughput 114 tok/s sustained
- **Progetto test**: Synesthesia clonato da GitHub (`C:\dev\synesthesia`, commit `05f8a92`)
  - Stack: Node 24 ESM + Express + EJS + SQLite + Passport, 273 deps, working tree pulito pre-test

### Config Cline su Ollama

- API Provider: Ollama
- Base URL: `http://localhost:11434`
- Model: `qwen2.5-coder:7b`
- Context window: 32768
- Timeout: 30000 ms

Warning esplicito di Cline durante setup: *"Cline uses complex prompts and works best with Claude models. Less capable models may not work as expected."*

## Test eseguiti e risultati

### Task 1 — Read + cross-file inference
**Prompt**: "Read app.js in this project and explain in 3 lines what it does."
**Risultato**: ✅ **SUCCESSO** — Cline ha chiesto permesso Read, Qwen ha prodotto spiegazione coerente e accurata in 4 punti (<15 s). Menziona correttamente Express, middleware, services (Database, UserService, AuthController), routes (/auth, /api, /creator, /admin), DB connection prima di `listen`.

### Task 2 — EDIT con JSDoc (prompt italiano)
**Prompt**: "Trova il file controller più piccolo nel progetto. Aggiungi JSDoc comment a ogni funzione pubblica. Non modificare il comportamento."
**Risultato**: ❌ **FALLIMENTO doppio**
- **Errore semantico**: Qwen ha scelto `app.js` come "controller più piccolo" (è entry point Express, non controller)
- **Errore tecnico**: Cline usa SEARCH/REPLACE per edit; Qwen ha generato SEARCH block che **non matchava byte-perfect** il contenuto del file → 3 retry falliti → loop infinito, richiede intervento utente per "fixare" SEARCH block

### Task 3 — CREATE file nuovo
**Prompt**: "Crea un nuovo file utils/validate-email.js con isValidEmail(email) basata su regex RFC-5322 semplificata. Aggiungi JSDoc completo. Export ES module."
**Risultato**: ✅ **SUCCESSO CREATE** — file generato pulito:

```javascript
/**
 * Validates an email address using a simplified RFC-5322 regex.
 *
 * @param {string} email - The email address to validate.
 * @returns {boolean} - Returns true if the email is valid, otherwise false.
 */
export function isValidEmail(email) {
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(email);
}
```

JSDoc, regex, ES module export tutti corretti. Tempo <30s.

### Task 4 — Auto-extension catastrofica post-Task 3
**Non richiesta dall'utente**: Qwen ha deciso autonomamente di "migliorare":
1. Tentato EDIT su `validate-email.js` appena creato → stesso loop SEARCH/REPLACE del Task 2
2. Creato `utils/validate-email.test.js` (test non richiesti)
3. Tentato `npm test` → fallisce (Synesthesia non ha script `test`)
4. **Installato autonomamente `jest` + `@testing-library/react` + `babel-jest`** — catastrofe: Synesthesia NON è React, queste deps sono inappropriate
5. Tentato `npx jest --init` → comando TTY interactive → **loop infinito** (Cline ri-lancia il comando senza capire che attende input)

**Danni collaterali (poi ripuliti)**:
- `package.json` modificato
- 280 pacchetti npm aggiunti (553 totali vs 273 pre-test)
- File test creato
- Terminal integrato VSCode bloccato

**Cleanup eseguito**:
```bash
cd C:\dev\synesthesia
git reset --hard HEAD
git clean -fd
rm -rf node_modules && npm install
```
Post-cleanup: Synesthesia tornato allo stato originale pulito.

## Findings

### Positivi

1. **Infrastructure funziona**: pipeline VSCode → Cline → Ollama → Qwen tecnicamente OK (zero errori connessione, latency accettabile)
2. **Read + cross-file inference**: Qwen 7B ragiona correttamente su codebase Express standard
3. **CREATE singolo file**: genera codice + documentazione di qualità accettabile in single-shot
4. **Throughput**: 114 tok/s Blackwell-optimized dà feel responsive

### Negativi (critici)

1. **SEARCH/REPLACE fragile**: Qwen 7B non genera SEARCH block byte-perfect → ogni EDIT fallisce sistematicamente
2. **Scope creep autonomo**: Qwen decide di "aggiungere valore" con feature non richieste, senza chiedere
3. **Dependency selection inappropriate**: `@testing-library/react` per un progetto Express pure — zero comprensione stack reale
4. **No TTY discipline**: Cline lancia comandi interactive, Qwen non riconosce blocco → loop
5. **Errori semantici**: confonde concetti ("controller" → entry point)

### Diagnosi root cause

Cline è progettato con **system prompt verboso e multi-tool chaining** ottimizzato per Claude:
- SEARCH/REPLACE per edit (richiede reasoning preciso byte-level)
- Tool chaining autonomo (richiede stop criterion rigoroso)
- Decisione autonoma dipendenze (richiede contesto profondo progetto)

Qwen 7B è **insufficientemente capable** su tre dimensioni critiche:
- **Precisione sintattica** (SEARCH block byte-perfect)
- **Instruction compliance** (rispettare scope, non estendere oltre richiesto)
- **Tool-use discipline** (riconoscere quando fermarsi)

Il warning ufficiale di Cline (*"works best with Claude models"*) è **accurato, non scaramantico marketing**.

## Decisione

**Cline + Qwen 2.5 Coder 7B è NON viable** per workflow agentic complesso.

**Uso corretto di Qwen 7B**:
- ✅ Query one-shot via `ollama run qwen2.5-coder:7b "..."` (risposta singola, no tool use iterativo)
- ✅ Single-file discussion / explanation / manual refactor non applicato
- ❌ **NON** come backend agentic per Cline (né Continue né Aider da verificare)

**Workflow operativo consolidato dopo stasera**:
- **Agentic coding**: Claude Code (Opus 4.7) finché Claude Max attivo (fino 19/05/2026)
- **Query assistive one-shot**: Qwen 7B locale via `ollama run`
- **Post-19/05**: strategia da **definire con test alternative** (vedi Follow-up)

## Implicazioni per Roadmap Sovereign (ADR-0001)

### Revisione Fase 2 richiesta

**Piano originale ADR-0001**: "spostare 90% workflow su Ollama locale + Cline VSCode".

**Problema emerso**: Cline + Qwen 7B non regge workflow reale → Fase 2 richiede revisione.

### Opzioni da valutare (sessione dedicata futura)

**Opzione A — Modello più capace locale**:
- Qwen 2.5 Coder 14B (Q3_K_M ~8 GB, **borderline VRAM** RTX 5060 8GB, va testato)
- Aspettare Qwen 3 Coder (release 2026 attesa)
- DeepSeek-Coder-V2 (MoE, richiede Blackwell fix NVFP4)

**Opzione B — Cliente agentic diverso**:
- **Aider** (CLI-based, usa diff whole-file invece di SEARCH/REPLACE — potenzialmente più tollerante per modelli piccoli)
- **Continue.dev** (pattern editing diverso, da verificare)
- Roo Code (fork di Cline)

**Opzione C — Workflow ibrido esplicito**:
- Claude Pro $20/mese (Plan B già previsto in ADR-0001)
- Ollama+Qwen per task espressamente limitati (single-shot, no agentic)
- OpenRouter pay-per-use per task occasionali complessi

**Opzione D — Hardware upgrade**:
- Mac mini M4 Pro 48GB (ADR-0001 lo classificava "opzionale non dependency")
- Ora diventa "fortemente utile" se Opzione A non regge sul Lenovo

### Revisione target budget

Scenario realistico revisionato post-19/05:
- Claude Pro subscription: $20/mese
- OpenRouter fallback: $5-15/mese
- **Totale: $25-35/mese = $300-420/anno**

vs target originale ADR-0001: **$60-240/anno** (€5-20/mese).

Ancora **sostanziale risparmio vs Claude Max** ($2400/anno), ma non più "zero subscription fisse" come era l'obiettivo originale. Da accettare o mitigare con Opzione A/B di successo.

## Follow-up

### Da testare questa settimana (prima di decisioni finali)
- [ ] Aider + Qwen 7B: pattern diff whole-file, stesse 4 task
- [ ] Continue.dev + Qwen 7B: pattern editing custom, stesse 4 task
- [ ] Qwen 2.5 Coder 14B Q3_K_M su VRAM budget (8GB borderline)

### Da testare questo mese
- [ ] Benchmark qualitativo strutturato: 10 task standard, matrice modello × cliente
- [ ] Re-test Cline quando Qwen 3 Coder rilasciato

### Revisione ADR-0001
- [ ] Dopo test Aider/Continue: decidere se "sovereign with nvm-like tool" o "workflow ibrido con Claude Pro"
- [ ] Aggiornare target budget realistico
- [ ] Aggiornare timeline Fase 2/3

## Lezioni meta

### tok/s NON è l'unica metrica
Stasera misurato 114 tok/s Blackwell-optimized. **Throughput eccellente**. Ma **capability** (instruction-following, tool compliance, precision byte-level) è **ortogonale** al throughput. Qwen 7B veloce ma insufficientemente capable per agentic.

**Framework di valutazione modelli rivisto**: non basta "tok/s + quality-on-single-prompt". Serve anche testing in ambiente agentic multi-turn.

### "Sovereign" ≠ "plug-and-play"
Narrativa preferita era "passo a sovereign, dimentico Claude". Realtà:
- Sovereign è **migrazione graduale**, non **switch**
- Richiede testing multi-scenario, multi-tool
- Può richiedere investimenti addizionali (modelli più capaci, hardware, tool custom)

### Warning ufficiali sono da ascoltare
Cline aveva warning esplicito nella config. Lo avevo notato, pensavo fosse marketing pro-Anthropic. **Era accurato**. Meta-regola: quando un tool dice "works best with X", **assumi che con altri funziona male**, non "probabilmente funziona uguale".

### Dati "negativi" sono ugualmente valore
Stasera 2h di test, zero feature tangibile prodotta, ma **finding chiaro** che strategia A non funziona → evita mesi di frustrazione su roadmap sbagliata. **Negative result è risultato.**

## Riferimenti

- Cline documentation: https://docs.cline.bot
- Cline GitHub: https://github.com/cline/cline
- Aider: https://aider.chat
- Continue.dev: https://continue.dev
- Qwen 2.5 Coder: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct
- ADR-0001 Sovereign AI Strategy: `0001-sovereign-ai-strategy.md` (impatto diretto, revisione richiesta)
- ADR-0004 Ollama RTX 5060 config: `0004-ollama-rtx5060-config.md` (setup non cambia)
