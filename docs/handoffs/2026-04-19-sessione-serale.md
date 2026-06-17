# Sessione serale 2026-04-19: GitHub, dev stack, Ollama bonus

> Seconda sessione operativa su CodeMasterDD.
> Durata: ~4 ore (19:25 → 23:30 circa), con pause asincrone
> Stato finale: repo online privato, dev stack completo, Ollama operativo

## Contesto

### Dopo la sessione notturna

La mattina del 19/04 avevo chiuso con:
- Lenovo hardened (BitLocker, OneDrive, bloatware)
- Claude Code installato e autenticato con Claude Max
- Repo `lenovo-ai-station` inizializzato localmente
- Primo commit `9de5254` creato

Poi ho dormito 9 ore, pranzato in famiglia, trascorso tempo con mia moglie
e mia madre. La domenica alle 19:23 ero fresco, lucido, pronto per continuare.

### Piano della serata

Due obiettivi in sequenza, 90 minuti stimati:

**Obiettivo 1 — GitHub push** (10 min):
- Verifica/install GitHub CLI
- Auth OAuth
- Create repo privato
- Push dei commit esistenti

**Obiettivo 2 — Dev stack base** (30-40 min):
- Node.js 22 LTS
- Python 3.12
- VS Code

**Obiettivo 3 — Commit progressione** (10 min):
- Aggiornamento JOURNAL
- Commit + push

**Stop target**: 20:50, per cena in famiglia alle 21:00.

### La realtà: piano esteso

La cena è saltata (famiglia asincrona anche la domenica sera). Dopo cena
sono tornato verso le 22:00 con ancora più energia. Ho deciso di sfruttare
il flow per aggiungere un obiettivo **bonus** non pianificato: Ollama install.

Risultato: sessione estesa fino alle 23:30 con risultati oltre le aspettative.

## Fase 1: Revisione nome repository (19:25-20:15)

### Il dubbio iniziale

Claude Code era pronto per eseguire `gh repo create MasterDD-L34D/lenovo-ai-station`.
Mi sono fermato un attimo e ho pensato: "lenovo-ai-station" non mi convince.

**Perché**: il nome è vincolato al brand hardware (Lenovo). Ma io ho
rinominato il PC `CodeMasterDD` per avere identità mia. Il repo dovrebbe
riflettere la stessa scelta.

### Le opzioni considerate

**Opzione A — Mantieni `lenovo-ai-station`**:
- Pro: zero rework, tutto pronto
- Contro: vincolato a "Lenovo", brand fragility

**Opzione B — Rinomina `codemasterdd-ai-station`**:
- Pro: identità personale, future-proof
- Contro: 15-20 min di rework su README/CLAUDE/JOURNAL

**Opzione C — Nome generico `ai-workstation`**:
- Pro: neutrale, future-proof per multi-device
- Contro: ristrutturazione pesante (cartelle `machines/xxx/`)

**Opzione D — Solo `codemasterdd`**:
- Pro: nome breve, memorabile
- Contro: non comunica scopo del repo

### La decisione: Opzione B

**Ragionamento**:
1. "CodeMasterDD" è nome PC che **io** ho scelto, non vendor
2. Contiene parte del mio handle GitHub (MasterDD) — continuità identità
3. Se un giorno cambio hardware, nome resta valido finché PC si chiama CodeMasterDD
4. `-ai-station` dice comunque cosa fa il repo

### Rework applicato

**File modificati**: README.md, CLAUDE.md, JOURNAL.md
**Numero edit**: 7 totali (1+5+1)
**Commit**: `eb425d1 docs: rename workstation label to CodeMasterDD`

**Nota**: cartella locale rimane `C:\dev\lenovo-ai-station`. Rinominare
anche la cartella era separato e rischioso (Claude Code ha path memorizzato).
Rinominata solo su GitHub. Disallineamento temporaneo accettabile.

### Lezione appresa
**Nome cose con la massima cura possibile stra early**. Rinominare costa
poco all'inizio (pochi file), costa molto dopo (link, import, reference, doc).
Vale la pena perdere 20 minuti stasera per avere identità giusta per anni.

## Fase 2: GitHub CLI install (20:15-20:30)

### Install via winget

```powershell
winget install GitHub.cli --accept-package-agreements --accept-source-agreements
```

Versione installata: **GitHub CLI 2.90.0** (release 2026-04-16).

Download: 2.83 MB. Install silent. Durata: ~30 secondi.

### Il problema del PATH stantio

Dopo install, Claude Code non vedeva `gh`. Né via bash, né via PowerShell
interna di Claude Code. Motivo: **le sessioni aperte prima di winget install
hanno una copia "congelata" del PATH**.

**Soluzione Claude Code**: usa path assoluto
```bash
"/c/Program Files/GitHub CLI/gh.exe" auth status
```

**Soluzione mia**: apro PowerShell nuova per verifiche manuali.

### Verifica mia in PowerShell fresca
```
PS C:\Windows\system32> gh --version
gh version 2.90.0 (2026-04-16)
https://github.com/cli/cli/releases/tag/v2.90.0
```

OK.

### Lezione appresa
**PATH refresh su Windows richiede riapertura shell** (o script esplicito).
Patterns alternativi:
```powershell
# Force refresh senza riaprire
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

Oppure pattern Claude Code: path assoluti per workaround immediato.

## Fase 3: GitHub auth OAuth (20:30-20:45)

### gh auth login wizard

Lanciato in PowerShell fresca:
```powershell
gh auth login
```

Risposte wizard:
1. "Where do you use GitHub?" → **GitHub.com**
2. "What is your preferred protocol for Git operations?" → **HTTPS**
3. "Authenticate Git with your GitHub credentials?" → **Yes**
4. "How would you like to authenticate GitHub CLI?" → **Login with a web browser**

### Browser OAuth flow

Codice one-time mostrato (es. `ABCD-1234`). Enter premuto, browser aperto
su `github.com/login/device`. Codice incollato. Autorizzazione approvata
per scopes: `gist`, `read:org`, `repo`, `workflow`.

### Verifica
```
✓ Authentication complete.
✓ Logged in to github.com account MasterDD-L34D (keyring)
- Active account: true
- Git operations protocol: https
- Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

### Lezione appresa
**Device OAuth flow è pattern standard** per CLI moderne (gh, Claude Code, ecc.).
Sicuro (no password in terminale), user-friendly (un codice, un click).
Codice scade in ~15 min se non usato.

## Fase 4: Creazione repo privato + push (20:45-21:00)

### Comando unificato
```bash
"/c/Program Files/GitHub CLI/gh.exe" repo create MasterDD-L34D/codemasterdd-ai-station \
  --private \
  --source=. \
  --remote=origin \
  --push
```

Cosa fa in un colpo:
1. Crea repo privato su GitHub
2. Aggiunge remote `origin` al repo locale
3. Push del branch `main` con tutti i commit presenti (3 al momento)

### Output
```
✓ Created repository MasterDD-L34D/codemasterdd-ai-station on GitHub
  https://github.com/MasterDD-L34D/codemasterdd-ai-station
✓ Added remote https://github.com/MasterDD-L34D/codemasterdd-ai-station.git
Enumerating objects: 11, done.
...
To https://github.com/MasterDD-L34D/codemasterdd-ai-station.git
 * [new branch]      HEAD -> main
branch 'main' set up to track 'origin/main'.
```

### Perché PRIVATO

**Ho scelto private non public** per queste ragioni:
- Contiene info hardware specifiche (SSD size, seriale, RAM)
- CLAUDE.md ha strategie personali (budget, roadmap, filosofia)
- JOURNAL.md ha storia sessioni con dettagli operativi
- Script di setup rivelano scelte di sicurezza
- È infrastructure, non codice condiviso

**Sempre meglio restrittivo di default**. Se un domani decido di pubblicare,
ribaltabile con 1 click su GitHub settings.

### Description impostata
```bash
gh repo edit --description "Infrastructure-as-code e journal della workstation CodeMasterDD (Lenovo desktop) -- setup, scripts, config, decisioni architetturali. Target: AI dev workstation sovereign."
```

Description in **italiano** (coerente con CLAUDE.md: docs italiano).

### Lezione appresa
**`gh repo create --source=. --remote=origin --push` è il comando più
efficiente per inizializzare repo da progetto locale esistente**. Un solo
comando, 3 effetti, reversibile (delete repo da GitHub).

## Fase 5: Dev stack install (21:00-21:40)

### Node.js LTS — la sorpresa Node 24

**Comando**:
```powershell
winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
```

**Risultato**: installato **Node.js 24.15.0**, non 22 come previsto.

**Perché**: dal 28 ottobre 2025 Node 24 ("Krypton") è Active LTS.
Node 22 ("Jod") è passato a Maintenance LTS. Il manifest winget
`OpenJS.NodeJS.LTS` punta sempre alla Active LTS corrente.

**Decisione**: tengo Node 24.
- Ragionamento: Node 24 supportato fino aprile 2029 (3 anni di tranquillità)
- Retrocompatibile con Node 22 nella stragrande maggioranza dei casi
- Synesthesia (mio progetto) già testato su Node 24
- Evo-Tactics usa `engines.node: ^22` → Node 24 al peggio emette warning

**Piano nvm-windows**: differito (YAGNI). Lo installerò solo se durante
migrazione progetti emergeranno incompatibilità reali.

### Verifica Node

PowerShell fresca:
```
PS C:\Windows\system32> node --version
v24.15.0
PS C:\Windows\system32> npm --version
11.12.1
```

### Python 3.12 install

```powershell
winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
```

Versione: **Python 3.12.10**.
Install path: `C:\Users\edusc\AppData\Local\Programs\Python\Python312\`
(user-install, non system-wide).

### Verifica Python
```
PS C:\Windows\system32> python --version
Python 3.12.10
PS C:\Windows\system32> pip --version
pip 25.0.1 from C:\Users\edusc\AppData\Local\Programs\Python\Python312\Lib\site-packages\pip (python 3.12)
```

**Nota**: pip 25.0.1 è l'ultima versione, ottimo.

**Perché 3.12 non 3.13**: 3.12 ha ecosistema più maturo (torch, tensorflow,
ollama-python, langchain tutti stabili). 3.13 ha alcune regression
performance note. Per Evo-Tactics (services/rules/) serve Python 3.10+,
3.12 è dentro range sicuro.

### VS Code install

```powershell
winget install Microsoft.VisualStudioCode --accept-package-agreements --accept-source-agreements
```

Versione: **1.116.0** (commit `560a9dba96f961efea7b1612916f89e5d5d4d679`).
Install path: `C:\Users\edusc\AppData\Local\Programs\Microsoft VS Code\`.
Add to PATH: sì (default installer).

### Verifica VS Code
```
PS C:\Windows\system32> code --version
1.116.0
560a9dba96f961efea7b1612916f89e5d5d4d679
x64
```

**Non ho aperto VS Code stasera**. Prima apertura lunedì, per evitare
interferenze con Claude Code operativo.

## Fase 6: Update CLAUDE.md (21:40-22:00)

### Reconciliazione stack

Prima delle modifiche, CLAUDE.md aveva:
- Stack installato: Git, Claude Code, Driver NVIDIA
- Stack da installare: Node 22, Python 3.10+, VS Code, Ollama, gh CLI

Dopo il dev stack install, servono 2 tipi di edit:
1. **Muovere** le voci installate da "Stack da installare" a "Stack installato"
2. **Aggiornare** le versioni (Node 22 → Node 24, Python 3.10+ → Python 3.12.10)

### Diff applicato

```diff
 ## Stack installato
 - Git 2.53.0.windows.3
 - Claude Code 2.1.114 (OAuth Claude Max, Opus 4.7)
 - NVIDIA Driver 595.79 + CUDA 13.2
+- GitHub CLI 2.90.0 (installato 2026-04-19, auth MasterDD-L34D)
+- Node.js 24.15.0 LTS + npm 11.12.1 (installato 2026-04-19, Active LTS fino aprile 2029)
+- Python 3.12.10 (installato 2026-04-19)

 ## Stack da installare questa settimana
-- Node.js 22 LTS
-- Python 3.10+
-- VS Code
+- VS Code (prossimo step)
 - Ollama 0.21+ + Qwen 2.5 Coder 7B
-- GitHub CLI (gh)
```

Più aggiunta nota Evo-Tactics:
```diff
 - **Evo-Tactics**: co-op tactical game d20, monorepo Node+Python
   - GitHub: `github.com/MasterDD-L34D/Game`
   - Path Lenovo: `C:\dev\Game`
   - Stack: Node 22 + Python 3.10, xstate@5, inkjs, Vue3 bundle
+  - Compat runtime: useremo Node 24 a livello di sistema; installeremo nvm-windows solo se emergono incompatibilità
   - 710+ test
```

### Lezione appresa
**La documentazione deve essere a livello reale, non pianificato**.
"Stack da installare" vs "Stack installato" deve essere fedele a
stato corrente. Altrimenti serve solo a ingannare te stesso del futuro.

## Fase 7: Ollama install + Qwen 7B (22:00-23:15)

### Questo non era pianificato stasera

Il piano iniziale era fermarsi dopo dev stack. Ma:
- Dopo cena sono tornato con più energia
- Claude Code era ancora attivo con contesto
- Ollama install è modulare (pulito) — non inquina setup
- Volevo vedere benchmark reale su RTX 5060

Decisione: **procedo**. Si può sempre chiudere dopo download modello.

### Ollama install
```powershell
winget install Ollama.Ollama --accept-package-agreements --accept-source-agreements
```

Versione: **Ollama 0.21.0**.
Install path: `C:\Users\edusc\AppData\Local\Programs\Ollama\`.
Service: `Ollama` (Windows Service), auto-start.

### Config env vars ottimali per Blackwell

Su RTX 5060 (Blackwell sm_120), settings ottimali:

```powershell
[System.Environment]::SetEnvironmentVariable("OLLAMA_FLASH_ATTENTION", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KV_CACHE_TYPE", "q8_0", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_MAX_LOADED_MODELS", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "30m", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_CONTEXT_LENGTH", "16384", "User")
```

**Significato**:
- `FLASH_ATTENTION=1`: attiva Flash Attention (fino +20% throughput)
- `KV_CACHE_TYPE=q8_0`: quantizza KV cache a 8-bit (risparmia VRAM, qualità ok)
- `MAX_LOADED_MODELS=1`: 8GB VRAM non sopporta 2 modelli simultaneamente
- `KEEP_ALIVE=30m`: tiene modello in memoria 30 min dopo ultima richiesta
- `CONTEXT_LENGTH=16384`: 16K context (sufficiente per coding, non troppo VRAM)

### Pull Qwen 2.5 Coder 7B

```bash
ollama pull qwen2.5-coder:7b
```

Durata: ~2 minuti (connessione veloce).
Size: 4.7 GB (Q4_K_M quantizzazione).

### Primo benchmark

Task: generazione funzione Python di esempio (parser CSV con gestione errori).

```bash
ollama run qwen2.5-coder:7b --verbose "Scrivi una funzione Python che legge un file CSV..."
```

**Risultati**:
- **Tok/s sustained**: **93.51 tok/s** ⚡
- VRAM usage: ~6.2 GB / 8 GB
- Quality: **alta** (codice funzionante, pattern idiomatici Python)

### Analisi del benchmark

**Target atteso da research pre-sessione**: 40-55 tok/s
**Risultato effettivo**: 93.51 tok/s
**Deviazione**: **+70% sopra massimo atteso**

**Perché così veloce?**
1. Blackwell sm_120 ha ottimizzazioni LLM migliori di Ampere/Ada
2. Flash Attention + KV cache Q8 hanno impatto maggiore del previsto
3. Q4_K_M quantizzazione ben ottimizzata su GDDR7
4. No altri carichi GPU concorrenti (setup pulito)

**Implicazione strategica**:
Lenovo da solo **supera le attese** per workflow AI locale.
La filosofia "sovereign AI" è **ancora più realistica** di quanto pensavo.
Mac mini futuro = bonus, non necessità.

### Lezione appresa
**Benchmarkare sempre su hardware reale prima di pianificare**.
Le research online sono indicative ma la tua setup specifica
(driver, OS, config env vars) può dare risultati molto diversi.

## Fase 8: Commit finale + force-push (23:15-23:30)

### Problema: commit già fatto senza Ollama

Avevo fatto commit `feat: install dev stack (node 24, python 3.12, vscode)`
**prima** di installare Ollama. Ollama era bonus unplanned.

**Opzioni**:
- A) Nuovo commit separato per Ollama (storia "sporca" con 5 commit stasera)
- B) `git commit --amend` per includere Ollama nel commit precedente

Ho scelto **B** perché:
- Ollama è parte dello stesso "arco" dev stack
- Storia git più pulita con commit semanticamente coerenti
- Commit non ancora pushato in una variante era force-push safe

### Amended commit

**File modificati aggiunti**:
- CLAUDE.md: sezione Ollama (versione + config env vars + benchmark 93 tok/s)
- JOURNAL.md: entry 2026-04-20 estesa con fase Ollama

**Nuovo SHA**: `0059d45` (sostituisce precedente `087442c`).
**Nuovo messaggio**:
```
feat: install complete dev stack (node, python, vscode, ollama)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### Force-push con --force-with-lease

Il commit `087442c` era già pushato su GitHub. Amended commit → hash diverso
→ push normale fallisce. Serve `--force`.

**Ma `--force` brutale è pericoloso** (sovrascrive lavoro altrui se esistesse).
**Safer alternative**: `--force-with-lease`.

```bash
git push --force-with-lease=main:087442c origin main
```

**Semantica**:
- Push solo se `origin/main` è **esattamente** `087442c` (il nostro ultimo hash conosciuto)
- Se qualcun altro avesse pushato sopra, il lease fallisce → abort safe
- Se lease valido, force-push va a buon fine

**Output**:
```
To https://github.com/MasterDD-L34D/codemasterdd-ai-station.git
 + 087442c...0059d45 main -> main (forced update)
```

### Verifica finale

```bash
git log --oneline
```

```
0059d45 feat: install complete dev stack (node, python, vscode, ollama)
e8c372c chore: gitignore Claude Code local settings
eb425d1 docs: rename workstation label to CodeMasterDD
9de5254 chore: initial project structure
```

4 commit puliti. Storia coerente.

### Lezione appresa
**`git push --force-with-lease` è il modo corretto** di force-pushare su
repo condivisi (o potenzialmente tali). `--force` nudo è antipattern.
Lease = "verifica che nulla sia cambiato sotto" prima di sovrascrivere.

## Bilancio sessione serale

### Tempo per fase
- Decisione rinomina repo: 50 min (rework incluso)
- GitHub CLI install + auth: 30 min
- Repo create + push: 15 min
- Dev stack Node/Python/VSCode: 40 min
- Update CLAUDE.md reconciliation: 20 min
- Ollama install + benchmark: 75 min
- Commit finale + amend + force-push: 15 min
- **Totale**: ~4h15min di lavoro attivo

### Metriche qualità
- **Errori**: 0
- **Rework**: 1 (rinomina repo, deliberato con motivazione)
- **Rollback**: 0
- **Commit atomici**: 4 puliti
- **Force-push**: 1 safe (con --force-with-lease)

### Stato finale
- Repo privato online: `MasterDD-L34D/codemasterdd-ai-station`
- 4 commit su main, sincronizzati con origin
- Dev stack completo: Node 24, Python 3.12, VS Code 1.116
- Ollama operativo: Qwen 2.5 Coder 7B @ 93.51 tok/s
- CLAUDE.md allineato con stato reale
- JOURNAL.md con entry 2026-04-19 + 2026-04-20

## Meta-learning personale

### Cosa ho imparato stasera

**1. Le decisioni importanti vanno prese a mente fresca, non in flusso**
Quando Claude Code era pronto per `gh repo create lenovo-ai-station`, mi
sono fermato. Ho chiesto "è davvero il nome giusto?". Rework di 50 min
che ha portato a decisione migliore. Ne è valsa la pena. **Fermarsi per
riflettere non è perdere tempo, è investire**.

**2. winget può sorprenderti — leggi sempre l'output**
Ho chiesto Node 22, ha installato Node 24. Normalmente un dev frettoloso
avrebbe ignorato o frustrato. Invece: leggi, capisci, decidi informato.
Node 24 è migliore per il mio caso, lo documenti in ADR.

**3. Il flow va cavalcato con disciplina, non con frenesia**
Ero in flow buono dopo cena. Potevo installare 10 altre cose senza pensare.
Invece: **1 obiettivo bonus mirato** (Ollama), pianificato anche se non previsto,
con cura come se fosse il primo. Il flow è un'onda, non un tsunami.

**4. Benchmark reale > ipotesi documentazione**
Research diceva 40-55 tok/s. Realtà: 93 tok/s. Senza provare, mi sarei
perso l'informazione che il mio piano sovereign è più robusto del previsto.
**Misura sempre tu stesso, non fidarti di "generic benchmarks"**.

**5. git --force-with-lease > git --force**
`--force-with-lease` è amend-friendly + safety net. Ogni volta che serve
force-push, usalo come default. `--force` nudo solo in scenari molto specifici.

**6. Documentazione durante > documentazione dopo**
Ho scritto JOURNAL.md entry 2026-04-20 **mentre** facevo setup, non dopo.
Tra 3 mesi rileggerò e saprò esattamente perché ho scelto Node 24, perché
ho rinominato il repo, perché ho usato force-with-lease. **Il me stesso
del passato continua a essere gentile con il me stesso del futuro**.

### Differenze tra sessione notturna e serale

**Sessione notturna (sabato 19/04)**:
- Stato: post-trauma, ansia attiva
- Ritmo: lento, iper-cauto
- Errori: zero (grazie alla paura)
- Output: infrastructure di sicurezza

**Sessione serale (domenica 19/04)**:
- Stato: riposato, lucido
- Ritmo: focused ma fluido
- Errori: zero (grazie al metodo consolidato)
- Output: infrastructure operativa

**Osservazione**: il metodo appreso sotto stress (notte) è rimasto valido
sotto condizioni migliori (sera). La disciplina non è legata all'emozione
di partenza. **Il sistema diventa stabile quando funziona in entrambi i casi**.

### Il ruolo di Claude (l'AI) in questa sessione

**Claude è stato**:
- Rubber duck tecnico per articolare decisioni
- Ricercatore per confermare scelte con dati (es. Node 24 LTS fino 2029)
- Assistente sintattico per comandi complessi (force-with-lease)
- Archivista automatico per JOURNAL e CLAUDE

**Claude NON è stato**:
- Decisore (ho sempre scelto io)
- Autorità (ho corretto Claude 3 volte: Z.ai rimosso, Mac mini declassato, Ryzen clarificato)
- Oracolo (i benchmark reali hanno smentito research online)

**Questo è il pattern giusto**: AI come **thinking partner**, non come **substitute for thinking**.

### Emozione dominante durante la sessione

**19:00-20:00**: curiosità (il lavoro di ieri ha funzionato?)
**20:00-21:30**: determinazione focused (un pezzo alla volta)
**21:30-22:30**: soddisfazione crescente (repo online + stack installato)
**22:30-23:30**: stupore (Ollama 93 tok/s — sovereign è reale)

**Fine sessione**: senso di **solidità**. Non euforia. Solidità.
L'ho costruito passo passo, so come ogni pezzo funziona, so come ripararlo se si rompe.

## Riferimenti

- GitHub CLI v2.90.0: https://github.com/cli/cli/releases/tag/v2.90.0
- Node.js 24 LTS Active schedule: https://nodejs.org/en/about/previous-releases
- Python 3.12.10: https://www.python.org/downloads/release/python-31210/
- VS Code 1.116: https://code.visualstudio.com/updates
- Ollama 0.21.0: https://github.com/ollama/ollama/releases
- Qwen 2.5 Coder: https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct

## Output tangibili

Alla fine di questa sessione:
- Repo GitHub privato online con 4 commit: `MasterDD-L34D/codemasterdd-ai-station`
- Node.js 24.15.0 + npm 11.12.1 operativi
- Python 3.12.10 + pip 25.0.1 operativi
- VS Code 1.116.0 installato (non aperto stasera)
- Ollama 0.21.0 + Qwen 2.5 Coder 7B operativi (93 tok/s)
- CLAUDE.md + JOURNAL.md allineati con stato reale
- GitHub CLI 2.90.0 autenticato come MasterDD-L34D

Prossimi step pianificati:
- Migrazione progetti reali (Evo-Tactics, Synesthesia) dal Ryzen al Lenovo
- Eventuale rinomina cartella locale `lenovo-ai-station` → `codemasterdd-ai-station`
- Benchmark comparativo Opus 4.7 vs Qwen 7B su task reali
