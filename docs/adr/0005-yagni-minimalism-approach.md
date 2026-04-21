# ADR 0005 — YAGNI e approccio minimalista

> *TL;DR: formalizzo YAGNI come principio trasversale del progetto: no tool/struttura/complessità finché non serve un problema reale. Trade-off: rischio mancata preparazione per future needs, mitigato dalla natura reversibile della maggior parte dei tool dev.*

**Status**: Accepted (as ongoing principle)
**Data**: 2026-04-20 (formalizzato)
**Decisore**: Eduardo Scarpelli
**Tipo decisione**: filosofia, metodologia

## Contesto

### Il principio YAGNI

**YAGNI** = **You Aren't Gonna Need It**

Principio di software engineering formulato nell'Extreme Programming (XP)
degli anni '90 da Kent Beck e Ron Jeffries. Si applica in origine al codice,
ma ha validità **universale** in decisioni architetturali, setup di strumenti,
e scelte quotidiane dev.

**Formulazione classica**: "Non implementare funzionalità prima che
effettivamente servano".

**Mia formulazione estesa**: "Non installare strumenti, non creare strutture,
non aggiungere complessità finché non hai un problema reale che le richiede".

### Perché questo ADR

Durante il setup workstation ho fatto **molte piccole decisioni YAGNI**,
spesso contro suggerimenti AI o best practice generiche. Voglio formalizzare
il pattern perché:

1. Applicato inconsciamente, YAGNI protegge da over-engineering
2. Applicato consciamente, permette di difendersi da "nice to have"
3. Serve linguaggio condiviso per decisioni future (io e AI)

### Tentazioni evitate durante questo setup

**Tentazione 1**: installare nvm-windows pre-emptively
**Motivazione pro-install**: "ogni dev senior ce l'ha, potrebbe servire"
**Decisione YAGNI**: installo solo se emerge conflitto reale Node versions
**Risultato**: Node 24 da solo sta funzionando bene, risparmiato setup + learning curve

**Tentazione 2**: installare 5+ MCP servers raccomandati online
**Motivazione pro-install**: "aumenta capacità Claude Code, blogpost X consiglia Y"
**Decisione YAGNI**: nessun MCP finché non emerge problema specifico
**Risultato**: Claude Code base ha già tutto per il mio workflow attuale

**Tentazione 3**: creare 9 subagents (rules-engineer, trait-curator, ecc.)
**Motivazione pro-create**: "utile per workflow strutturato su Evo-Tactics"
**Decisione YAGNI**: 0 subagents stanotte, forse 1 quando pattern emerge
**Risultato**: Claude Opus 4.7 di base è già capace, subagent quando pattern ripetitivo identificato

**Tentazione 4**: Mac mini subito come "upgrade AI inference"
**Motivazione pro-buy**: "Lenovo 8GB è limitato per modelli grandi"
**Decisione YAGNI**: benchmarkare Lenovo, comprare solo se necessario
**Risultato**: Qwen 7B su Lenovo = 93 tok/s, Mac mini diventa opzionale non necessario

**Tentazione 5**: multi-device repo structure (`machines/lenovo-xxx/`, `machines/mac-mini/`)
**Motivazione pro-structure**: "future-proof, scalabile"
**Decisione YAGNI**: flat structure, refactor quando secondo device esiste davvero
**Risultato**: meno complessità mentale, struttura evolve con bisogni reali

## Decisione

Adotto YAGNI come **principio guida** per tutte le decisioni su workstation,
infrastructure, tooling.

### Regole operative

**Regola 1 — "Aggiungi solo quando hai un problema specifico"**

NON aggiungere:
- Tool "perché potrebbe servire"
- Config "pre-emptive"
- Struttura "per futuro"
- Dipendenze "per completezza"

Aggiungere SOLO quando:
- Un task specifico è bloccato senza quel tool
- Un errore ricorrente richiede quel config
- Un pattern di uso reale giustifica la struttura
- Una feature esistente richiede la dipendenza

**Regola 2 — "Default sicuro: non aggiungere"**

Quando ho dubbi su aggiungere qualcosa → **non aggiungo**.
Aggiungere è più facile dopo che rimuovere prima.

**Regola 3 — "Documenta la decisione di NON aggiungere"**

Se valuto consciamente di non installare X, lo documento (come sto facendo qui).
Così evito di ri-valutare ogni volta la stessa cosa.

**Regola 4 — "Revisione periodica"**

Ogni 1-2 mesi, controllo: questi "not now" sono ancora validi?
Se emerge problema → aggiungo. Se stabile → conferma YAGNI.

### Differenza tra YAGNI e negligenza

**YAGNI NON significa**:
- "Fallo in modo sciatto perché poi si aggiusta"
- "Ignora best practice senza comprenderle"
- "Rifiuta tutto il nuovo"

**YAGNI significa**:
- "Fai bene ciò che serve ora, resta flessibile per il futuro"
- "Conosci le best practice, ma applica solo quelle pertinenti al tuo caso"
- "Aggiungi nuovo quando c'è valore reale, non per FOMO"

## Conseguenze

### Positive

**Simplicity as default**:
- Meno tool = meno complessità da gestire
- Meno config = meno superficie bug
- Meno strutture = meno cognitive load

**Velocità setup**:
- Non spendo ore pre-configurando cose "che potrebbero servire"
- Mi concentro su task reali subito

**Budget e risorse**:
- Meno storage sprecato (tool non usati accumulano)
- Meno memoria (servizi in background di tool ignorati)
- Meno tempo di manutenzione (update, conflitti, security patches)

**Apprendimento graduale**:
- Imparo tool uno alla volta, quando serve
- Ogni tool appreso è "earned" da un problema reale
- Conoscenza profonda > conoscenza superficiale estesa

**Resilienza**:
- Setup minimale è facile da replicare/ricreare
- Meno dipendenze = meno breaking changes da gestire

### Negative

**Possibile reinvenzione della ruota**:
- A volte scopro che avrei potuto usare tool X invece di soluzione custom
- Mitigation: se realizzo gap, valuto tool X quando l'ho capito bene

**Momenti di "potevi farlo subito"**:
- Qualche volta dovrò installare cosa X che rimandavo
- Mitigation: install quando serve è 5 min, pianificare preventivamente sarebbe ore

**Comunicazione con dev pre-configurati**:
- Altri dev potrebbero "normalizzare" tool che io non uso
- Mitigation: conosco i tool anche se non li uso, spiego scelta

### Perché accetto i contro

Il mio workflow è:
- Solo-dev (no team)
- 2-3 progetti attivi principali
- Budget limitato
- Tempo mentale limitato

In team grandi o startup veloci, YAGNI può costare di più. Per me è
**ottimale**.

## Alternative considerate

### Alternative 1: "Install everything preemptively" (kitchen sink)

**Filosofia**: meglio avere tutto pronto, poi usare quello che serve.

**Pro**:
- Zero friction quando serve un tool
- "Pre-loaded" per qualsiasi task imprevisto

**Contro**:
- Hours spese in setup di tool mai usati
- Background services consumano risorse
- Update fatigue
- Cognitive load aumentato

**Perché scartata**: costo > beneficio nel mio caso.

### Alternative 2: "Follow popular guide strictly"

**Filosofia**: seguire blogpost "perfect dev setup 2026".

**Pro**:
- Veloce (copia-incolla)
- Coperto su casi comuni

**Contro**:
- Setup generico non ottimizzato per me
- Includerebbe tool non necessari (FOMO guidelines)
- Nessuna comprensione profonda

**Perché scartata**: ho visto troppi dev con setup "perfetti" che non sanno
come funzionano. Zero sovereignty mentale.

### Alternative 3: "Lean by default, premium when needed"

**Filosofia**: parti essenziale, paga complessità per funzionalità premium.

**Pro**:
- Copertura casi avanzati quando servono
- Budget riservato per high-value tool

**Contro**:
- Costi fissi per tool premium poco usati

**Perché scelta**: fondamentalmente è quello che sto facendo.
YAGNI per free/local, willingness-to-pay per value-critical (Claude Max ora,
OpenRouter futuro).

### Alternative 4: "Copy senior dev setup"

**Filosofia**: imita setup di dev esperti noti.

**Pro**:
- Presumibilmente buono
- Social proof

**Contro**:
- Il loro setup riflette i **loro** bisogni, non i miei
- Senza capire il perché, non posso adattare

**Perché scartata**: il mio contesto è unico.

## Applicazioni concrete di YAGNI in questo setup

### Tool/strumenti NON installati (YAGNI-validated)

| Tool | Raccomandato da | Perché NO (per ora) |
|------|-----------------|---------------------|
| nvm-windows | Claude, common sense | Node 24 basta per ora, install se conflitti |
| Docker Desktop | Blog "perfect setup" | Nessun container workload attuale |
| WSL2 | "Every Windows dev needs it" | Dev nativo Windows va bene per i miei progetti |
| Postman | API dev guides | `curl` + `gh api` bastano per ora |
| Insomnia | Postman alternative | Come sopra |
| TablePlus | DB management GUI | SQLite CLI va bene per Synesthesia |
| Conda / Miniconda | ML workflows | pip venv basta per progetti Python attuali |
| Syncthing | Backup multi-device | GitHub + external drive bastano |
| Tailscale | Remote access mesh | No need finché non viaggio con 2 PC |
| Obsidian sync | Notes multi-device | Notes in repo Git = sync gratis |
| 5+ VS Code extensions | Tutti i "must have" list | 2-3 estensioni base, aggiungo su pattern |
| 3+ MCP servers | Claude Code guides | 0 MCP ora, aggiungo quando serve |
| Subagent suite | Cuore dell'agentic dev | 0 subagent, creo quando pattern emerge |
| Claude Desktop App | Integrazione Anthropic | Browser + Claude Code bastano |
| Mac mini hardware | Futuro sovereign stack | Lenovo basta 93 tok/s |

### Tool installati SOLO perché serviti

| Tool | Perché installato |
|------|-------------------|
| Git 2.53.0 | Obbligo version control |
| Claude Code | Agente primario di questa fase |
| GitHub CLI | Necessario per gh repo create |
| Node.js 24 | Evo-Tactics e Synesthesia richiedono Node |
| Python 3.12 | Evo-Tactics services/rules richiede Python |
| VS Code | Editor primario (già installato prima ma attivato ora) |
| NVIDIA driver 595.79 | Ottimizzazioni LLM Blackwell |
| Ollama 0.21.0 | Target sovereign AI |
| Qwen 2.5 Coder 7B | Primo modello AI locale |

Ogni tool ha **una giustificazione specifica**, non "consigliato da X".

## Meta-learning

### YAGNI come antidoto a FOMO dev

FOMO (Fear Of Missing Out) è endemico nel mondo dev:
- "Tutti usano X ora, dovrei provarlo"
- "Sto rimanendo indietro sul tech stack"
- "Questo tutorial dice che è il modo giusto"

**YAGNI è l'antidoto pratico**:
- "Tutti" ≠ pertinente al mio caso
- "Rimanere indietro" è illusione, il tech cambia ogni settimana
- "Il modo giusto" dipende dal contesto, non esiste universale

Quando sento FOMO → applico YAGNI rigoroso.

### YAGNI è decisione attiva, non passività

**Differenza chiave**:
- **Passività**: "non ho installato X perché non ci ho pensato"
- **YAGNI**: "non ho installato X perché ho valutato e deciso non servire ora"

**Passività** è rischiosa (potrebbero mancarmi cose fondamentali).
**YAGNI** è robusta (ho consapevolezza di cosa ho scelto di non avere).

La documentazione YAGNI (come in questo ADR) trasforma passività in
decisione attiva.

### YAGNI e l'AI assistant

Claude AI è tendenzialmente **anti-YAGNI**:
- È trained su documentazione che copre "best practice complete"
- Preferisce suggerire "approach completo" a "approach minimal"
- Non vede costo cognitivo/tempo di setup che tu sostieni

**Mia responsabilità**: filtrare suggerimenti Claude con lente YAGNI.

**Esempio concreto**: quando Claude ha proposto Z.ai nel piano iniziale,
io l'ho fermato perché:
1. Non l'avevo chiesto
2. Non risolveva problema specifico mio
3. Violava filosofia sovereign

**Pattern**: Claude suggerisce → io filtro → Claude implementa mia scelta.

### Il "earned complexity"

Ogni tool aggiunto al setup deve essere **earned**:
- Ha risolto un problema che avevo
- L'ho capito abbastanza da maintain e debug
- Il beneficio ongoing giustifica il costo ongoing

Complessità unearned è debt:
- Non capisco come funziona
- Non so quando/come update
- Se si rompe non so fixare
- Consuma risorse senza valore

**Earned complexity** è sostenibile.
**Unearned complexity** collassa prima o poi.

### Quando YAGNI fallisce

YAGNI è principio, non dogma. Fallisce quando:

**1. Security/privacy crucial**:
- Non puoi "aggiungere sicurezza quando serve" dopo un breach
- Defensive install upfront OK (es. firewall, backup strategy)

**2. Setup expensive se fatto dopo**:
- Se rifare costa 10x di pre-farlo, pre-fare può valere
- Es: database schema scelto male da subito è nightmare after
- Es: Git init da 500 file esistenti vs iniziale è più complesso

**3. Lock-in fisici (hardware)**:
- Una volta comprato PC con 16GB, non posso aggiungere RAM se mobo non supporta
- Need upfront consideration vs YAGNI

**Per la maggior parte dei tool software, YAGNI vince**.

## Regole operative rapide

**Quick decision framework**:

```
Sto pensando di installare/configurare X.

Domande:
1. Ho un problema CONCRETO e ATTUALE che X risolverebbe?
   - NO → YAGNI, non installo
   - SÌ → continua

2. X è il tool MIGLIORE per questo problema, o first-thought?
   - First-thought → research 15 min alternative
   - Best → continua

3. Capirò X abbastanza da maintain e debug?
   - NO → aspetta a imparare basics, poi valuta
   - SÌ → continua

4. Beneficio ongoing > costo ongoing (update, complexity, risorse)?
   - NO → YAGNI, non installo
   - SÌ → installo

5. Documento perché installo (ADR)?
   - SEMPRE → rende decisione tracciabile e revocabile
```

## Follow-up

### Revisione YAGNI

**Cadenza**: mensile (ogni 1° del mese).

**Domande da pormi**:
1. Ho avuto frustrazioni per NON aver installato qualcosa?
2. Se sì, quella cosa meriterebbe installazione ora?
3. Ho installato qualcosa che non sto usando?
4. Se sì, meriterebbe disinstallazione?

**Obiettivo**: mantenere setup **usato al 100%**, nessun dead weight.

### Aggiornamento lista YAGNI

Se passo da "NO YAGNI" a "SÌ install", aggiorno:
- Questo ADR (nota transizione)
- Nuovo ADR specifico per quel tool (perché ora sì)
- CLAUDE.md (stack installato)
- JOURNAL.md (storia decisione)

## Riferimenti

- Wikipedia YAGNI: https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it
- Kent Beck, "Extreme Programming Explained" (1999)
- Ron Jeffries, "We Tried Baseball and It Didn't Work" (famosa critica anti-YAGNI)
- "The Art of Agile Development" - James Shore
- Concept correlato: KISS (Keep It Simple, Stupid), Principle of Least Power
