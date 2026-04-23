# OpenCode + Ollama + Routing Locale/Cloud

Questo modulo traduce i 5 screen aggiuntivi in un workflow reale da inserire nella libreria operativa.

Non è una prompt library.
È una **guida di tooling + runtime + model routing** per lavoro tecnico e coding assistito.

---

## 1. Obiettivo del modulo

Usare OpenCode e modelli locali/cloud in modo ordinato, con queste priorità:
- semplicità
- privacy
- costo controllato
- iterazione rapida
- passaggio al cloud solo quando porta valore reale

---

## 2. Principio guida

**Locale prima. Cloud dopo.**

Traduzione pratica:
- usa locale per task di coding iterativi, debugging, prove, tool calls semplici, lettura di porzioni di codice
- usa cloud per task più pesanti, più stabili o quando il modello locale non basta
- non collezionare modelli senza bisogno

---

## 3. Setup rapido operativo

### Step 1 — Installa OpenCode
```bash
curl -fsSL https://opencode.ai/install | bash
opencode --version
opencode
```

### Step 2 — Collega Ollama
```bash
ollama pull codestral
ollama pull mistral
ollama pull gemma3
ollama serve
ollama launch opencode
```

### Step 3 — Se serve configurazione manuale
Usa `baseURL`:
```text
http://localhost:11434/v1
```

### Step 4 — Se i tool call faticano
- aumenta il context window
- prova un modello più adatto al task
- verifica che stai usando il runtime giusto per il problema giusto

---

## 4. Routing minimo consigliato

### Scenario A — Coding puro locale
Usa un modello focalizzato sul coding.
Negli screen: **Codestral**.

### Scenario B — Equilibrio qualità/velocità in locale
Usa un generalista locale più bilanciato.
Negli screen: **Mistral**.

### Scenario C — Hardware limitato
Usa un modello più leggero.
Negli screen: **Gemma**.

### Scenario D — Provider esterni via API
Usa provider esterni quando vuoi qualità o velocità senza gestire tutto in locale.
Negli screen: **Mistral** o **Codestral**.

### Scenario E — Cloud integrato / fallback serio
Usa cloud quando ti serve più qualità complessiva o più affidabilità.
Negli screen: **Nemotron** o **GPT-5 Nano**.

---

## 5. Regola di scelta

Scegli il modello in base a 4 fattori:
1. tipo di task
2. accesso disponibile
3. limiti hardware
4. costo/privacy

Non scegliere in base a:
- hype
- collezionismo di modelli
- ranking assoluti presi come dogmi

---

## 6. Integrazione col workflow repo game

### Fase 1 — Comprensione progetto
Se hai documentazione dispersa:
- NotebookLM per fonti e corpus
- ChatGPT per sintesi operativa

### Fase 2 — Setup runtime tecnico
- OpenCode installato
- Ollama collegato
- un solo modello locale iniziale selezionato

### Fase 3 — Lavoro sul repo
- locale per esplorazione iterativa, piccoli task, refactor assistito, prove
- cloud o Claude Code quando serve contesto più robusto, reasoning più forte o stabilità superiore

### Fase 4 — Consolidamento
Riporta nella libreria:
- cosa hai usato
- per quale task
- cosa ha funzionato meglio
- quali fallback sono stati davvero utili

---

## 7. Protocollo pratico da adottare

### Profilo minimo consigliato
- 1 modello locale primario
- 1 modello locale secondario o leggero
- 1 opzione cloud affidabile

Esempio coerente con gli screen:
- locale primario: Codestral o Mistral
- locale leggero: Gemma
- cloud: Nemotron o GPT-5 Nano

---

## 8. Anti-pattern da evitare

### Anti-pattern 1 — Zoo di modelli
Troppi modelli, nessun criterio.

### Anti-pattern 2 — Cloud di default per tutto
Paghi e complichi anche quando il locale basta.

### Anti-pattern 3 — Locale usato oltre il suo limite
Forzi un modello locale su task che richiedono più contesto o più stabilità.

### Anti-pattern 4 — Nessuna documentazione del routing
Dopo una settimana non ricordi più quale modello usare per cosa.

---

## 9. Template rapido da salvare nel progetto

```text
MODEL ROUTING DEL PROGETTO

Locale primario:
Locale secondario:
Cloud principale:
Provider esterni disponibili:

Task locali ideali:
- 
- 

Task da portare in cloud:
- 
- 

Fallback ammessi:
- 
- 

Note reali dopo uso:
- 
- 
```

---

## 10. Collegamenti archivistici

Reference sorgente collegate:
- `03_REFERENCE/07_Trascrizione_Screen_OpenCode_Ollama.md`
- `03_REFERENCE/08_OpenCode_Ollama_Model_Routing_Extracted.md`

Modulo collegato:
- `04_MultiAI_Routing_NotebookLM_ChatGPT_Claude_Code.md`

---

## 11. Regola finale del modulo

Questo modulo funziona bene se ogni strumento e ogni modello hanno un ruolo semplice e stabile.

La forma sana è:
- pochi modelli
- ruoli chiari
- locale dove basta
- cloud dove serve
- routing scritto, non improvvisato
