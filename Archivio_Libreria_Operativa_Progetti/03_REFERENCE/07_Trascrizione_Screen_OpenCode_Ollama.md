# Trascrizione — Screen OpenCode / Ollama / Model Routing

Questa raccolta contiene la trascrizione fedele dei 5 screen aggiuntivi relativi a:
- installazione di OpenCode
- collegamento a Ollama
- scelta dei modelli locali
- scelta delle chiavi API
- ranking dei modelli cloud

Nota archivistica:
- i ranking e le preferenze presenti negli screen vanno trattati come **reference contestuali** dell'autore del carosello, non come regole universali del sistema
- i principi operativi, invece, sono riusabili e vengono estratti nel file `08_OpenCode_Ollama_Model_Routing_Extracted.md`

---

## Screen A — Installa OpenCode

**Titolo**  
`1. INSTALLA OPENCODE`

**Sottotitolo**  
`Primo passaggio. Due minuti.`

**Passi**
1. Apri il terminale.
2. Lancia: `curl -fsSL https://opencode.ai/install | bash`
3. Apri una nuova shell o ricarica il profilo.
4. Controlla con: `opencode --version`
5. Avvia con: `opencode`

**Contenuto sul laptop**
- `curl -fsSL https://opencode.ai/install | bash`
- `Downloading installer...`
- `Verifying signature...`
- `Installing OpenCode CLI...`
- `Linking binary...`
- `Setting up completions...`
- `install complete.`
- `Success! OpenCode is ready.`
- `opencode --version`
- `opencode v0.1.0`
- `opencode`
- `OpenCode CLI is ready.`

**Badge**
- CLI installata
- Terminale pronto
- Versione OK

**Chiusura**  
`Installa. Verifica. Parti.`

---

## Screen B — Collegalo a Ollama

**Titolo**  
`2. COLLEGALO A OLLAMA`

**Sottotitolo**  
`La via locale: privata, economica, pratica.`

**Passi**
1. Installa Ollama sul computer.
2. Scarica i modelli: `ollama pull codestral / mistral / gemma3`
3. Setup rapido: `ollama launch opencode`
4. Se vuoi il manuale, usa `baseURL`: `http://localhost:11434/v1`
5. Se i tool call faticano, alza il context window.

**Contenuto sul laptop**
- `ollama list`
- `codestral:latest`
- `mistral:latest`
- `gemma3:latest`
- `ollama serve`
- `Ollama is running on http://localhost:11434`
- `opencode`
- `OpenCode connected to Ollama`

**Widget laterale**
- Ollama
- Connesso localmente
- `http://localhost:11434`
- Modelli disponibili:
  - Codestral
  - Mistral
  - Gemma3

**Mini box**
- `ollama pull codestral`
- `ollama launch opencode`

**Chiusura**  
`Locale prima. Cloud dopo.`

---

## Screen C — Modelli locali da usare

**Titolo**  
`3. MODELLI LOCALI DA USARE`

**Sottotitolo**  
`Qui si sceglie. Non si accumula.`

**Ranking sintetico**
1. Codestral — Per coding puro. Prima scelta locale.
2. Mistral — Miglior equilibrio tra qualità e velocità.
3. Gemma — Più leggera. Buona se l'hardware è stretto.

**Nota**  
`Niente modelli cinesi in vetrina.`

**Benchmark — Coding (HumanEval)**

### 1. Codestral
- Pass@1: 63.4%
- Pass@10: 81.7%
- RAM min.: 16 GB
- VRAM min.: 8 GB

### 2. Mistral
- Pass@1: 56.1%
- Pass@10: 74.3%
- RAM min.: 12 GB
- VRAM min.: 6 GB

### 3. Gemma
- Pass@1: 45.2%
- Pass@10: 63.8%
- RAM min.: 8 GB
- VRAM min.: 4 GB

**Footer**
- Linguaggi: Python, JS, TS, Go, Rust, C++
- License: Aperti. Locali. Senza sorprese.
- Privacy: 100% locale. I tuoi dati, tuoi.

**Chiusura**  
`Codestral per spingere. Mistral per bilanciare. Gemma per stare leggeri.`

---

## Screen D — Chiavi API da usare

**Titolo**  
`4. CHIAVI API DA USARE`

**Sottotitolo**  
`Qui conta quale accesso stai usando.`

### Chiavi API esterne
- Prima scelta: Mistral
- Seconda: Codestral
- Buone opzioni se usi provider esterni.

### Chiavi OpenCode
- Prima scelta: Nemotron
- Seconda: GPT-5 Nano
- Nemotron è il migliore.
- GPT-5 Nano è il piano B serio.

**Nota**
- Gli altri modelli cinesi?
- Solo emergenza. Non sono il focus.

**Widget laptop — API esterne**
1. Mistral — Più equilibrato e veloce.
2. Codestral — Perfetto per coding puro.

**Widget laptop — OpenCode**
1. Nemotron — Miglior qualità complessiva.
2. GPT-5 Nano — Piano B serio, molto valido.

**Chiusura**  
`Accesso giusto. Modello giusto.`

---

## Screen E — Modelli cloud da tenere

**Titolo**  
`5. MODELLI CLOUD DA TENERE`

**Sottotitolo**  
`Questo è il ranking. Il resto è contorno.`

**Ranking sintetico**
1. Nemotron — Prima scelta cloud. La più solida.
2. GPT-5 Nano — Seconda scelta. Molto affidabile.
3. Gli altri modelli cinesi — Solo fallback di emergenza. Non puntarci.

### Card #1 — Nemotron
- La scelta migliore per coding cloud.
- Potente, stabile, coerente.
- La più completa in ogni scenario.
- Badge:
  - Consigliato
  - Top Choice

### Card #2 — GPT-5 Nano
- Perfetto equilibrio tra velocità e qualità.
- Leggero, veloce e preciso.
- Ideale per la maggior parte dei casi.
- Badge:
  - Affidabile
  - Seconda Scelta

### Box finale — Altri modelli cinesi
- Solo fallback di emergenza.
- Non puntarci mai come prima opzione.

**CTA**  
`SALVA IL CAROSELLO`

**Chiusura**  
`Nemotron davanti. GPT-5 Nano subito dietro.`
