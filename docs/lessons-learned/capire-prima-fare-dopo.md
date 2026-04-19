# Lezione appresa: Capire prima, fare dopo

**Data formalizzazione**: 2026-04-20
**Origine**: principio emerso dal trauma Victus e consolidato nelle sessioni setup Lenovo
**Scopo**: documentare il principio più importante che ho interiorizzato

## La frase

> **"Capire prima, fare dopo."**

Semplice. Potente. Cambia tutto.

## Il contrario (antipattern che evitavo senza saperlo)

**"Fare prima, capire dopo"**:
- Lancio comando, vedo cosa succede
- Se funziona, good
- Se non funziona, "tanto lo aggiusto"
- Copy-paste da Stack Overflow senza leggere
- Accept defaults perché "è lo standard"

**Questo è il modo in cui ho perso il Victus**.

Il debloat script l'ho eseguito senza capire cosa facesse.
Ho accettato BitLocker default senza capire le implicazioni.
Ho installato 14 tool in batch senza capire le interazioni.

Tre "fare prima, capire dopo" in sequenza = disastro.

## Il principio spiegato

### Definizione pratica

**Prima di eseguire un comando non-banale**, mi fermo e:
1. Leggo cosa fa il comando
2. Capisco gli effetti collaterali
3. Identifico cosa può andare storto
4. Penso a come tornare indietro
5. **Poi** eseguo

### "Non-banale" cosa significa

**Comando banale** (può skip comprensione profonda):
- `ls`, `cat`, `pwd` (read-only)
- `git status`, `git log` (read-only)
- `npm list` (read-only)

**Comando non-banale** (richiede comprensione):
- Qualsiasi modifica a registry
- Install/uninstall software
- Qualsiasi modifica a services
- Network configuration
- Permessi file
- Group policy
- Driver install
- Git operations modifying history (amend, rebase, force-push)

**Criterio di cutoff**: se il comando **modifica stato del sistema** o
**ha effetti potenzialmente non reversibili**, è non-banale.

### Il costo del "capire prima"

**Tempo**: 5-30 minuti extra per comando.

**Esempio concreto**: prima di `manage-bde -off C:`:
- Lettura documentazione manage-bde (10 min)
- Capire cosa succede durante decrittazione (5 min)
- Planning fasi successive (policy, service) (10 min)
- **Totale**: 25 min

**Benefit**: quando ho eseguito, sapevo esattamente cosa aspettarmi.
Zero sorprese. Zero rework.

### Il costo del "fare prima"

**Tempo apparente**: 0 (lanci subito).

**Tempo reale quando va storto**:
- 30 min - ore: diagnosi errore
- 30 min - 1 giorno: recovery
- Giorni - settimane: se disastro (es. Victus)

**Ratio costo/beneficio**:
- Fare prima: speed-up illusorio di 10 min
- Capire prima: risk reduction 90%+
- **Aritmetica ovvia** quando calcoli expected value.

## Applicazioni specifiche

### 1. Install di nuovo software

**Fare prima**: `winget install <package>` e via.
**Capire prima**:
- Cosa fa il package?
- Quali dipendenze installa?
- Modifica PATH? Registry? Services?
- Come si disinstalla se non mi piace?
- C'è una versione pinnable?

**Applicato al Lenovo**: per ogni tool (Node, Python, VSCode, Ollama),
15-30 min di research prima di winget install.

### 2. Modifiche registry

**Fare prima**: `Set-ItemProperty -Path ... -Value 1`.
**Capire prima**:
- Cosa fa esattamente questa key?
- Quale default esiste?
- Come testare che il cambio è efficace?
- Come tornare indietro (backup .reg)?

**Applicato**: sempre `reg export` prima di `Set-ItemProperty` invasivi.

### 3. Git operations

**Fare prima**: `git rebase -i HEAD~5`.
**Capire prima**:
- Cosa succede se rebase fallisce a metà?
- C'è un branch di backup?
- Gli altri hanno basato lavoro su questi commit?
- Posso testare su branch temporaneo prima?

**Applicato**: per amend + force-push (sessione 20/04), 10 min di
reading --force-with-lease doc prima di eseguire.

### 4. Config env vars

**Fare prima**: set 5 env vars.
**Capire prima**:
- Cosa fa ciascuna var?
- Valore default?
- Impact performance/sicurezza?
- Interazioni tra le var?

**Applicato**: per OLLAMA_* vars (sessione 20/04), ho studiato ogni var
prima di settare. Risultato: ADR-0004 con giustificazione documentata.

### 5. Dipendenze progetto

**Fare prima**: `npm install <package>`.
**Capire prima**:
- Il package è maintained? Quando ultimo update?
- Quante dep transitive?
- Licenza compatibile?
- Alternative simili?
- È davvero necessario?

**Applicato in passato**: mi ha salvato da package abandonware e da
bloat di dipendenze.

## "Capire" non significa "sapere tutto"

### Livelli di comprensione

**Livello 1 (minimo accettabile)**:
- So cosa fa a grandi linee
- So gli effetti principali
- So come disfare l'azione

**Livello 2 (buono)**:
- Conosco i parametri principali
- Capisco interazione con resto del sistema
- Posso spiegare a qualcun altro

**Livello 3 (profondo)**:
- Ho letto source code
- So edge cases documentati
- Posso debuggare problemi

**Minimo per "capire prima, fare dopo"**: **Livello 1**.
Non serve essere esperti. Serve non essere **completamente al buio**.

### Quando bisogna Livello 2 o 3

- Comandi irreversibili (dd, rm -rf, drop database)
- Production systems con utenti reali
- Operazioni security-critical
- Quando non c'è backup
- Debug di problemi rari

## Il ruolo dell'AI in "capire prima, fare dopo"

### AI come strumento di comprensione

Prima di eseguire un comando, chiedere a Claude:
- "Spiegami cosa fa questo comando esattamente"
- "Quali sono i rischi?"
- "Come posso verificare che abbia funzionato?"
- "Come posso tornare indietro?"

**Claude è eccellente** come spiegatore di comandi Unix/Windows/Git.

### AI come accelerator, non shortcut

**Antipattern**: "Claude, fai il setup" → skip my understanding.
**Pattern**: "Claude, spiegami il setup, poi eseguiamo step-by-step con approvazione".

**Differenza chiave**: Claude sa molto più di me, ma è **io** che devo
**decidere** e **capire**. Non posso delegare comprensione.

### Esempio concreto

**Antipattern che evito**:
```
Me: "Claude, imposta Ollama bene per la mia GPU."
Claude: [setta 5 env vars]
Me: [approvo senza leggere]
Risultato: setup funziona ma non so perché; se si rompe non so fixare.
```

**Pattern che applico**:
```
Me: "Claude, quali env vars ottimali per Ollama su RTX 5060 Blackwell?"
Claude: [lista 5 var con spiegazione ciascuna]
Me: [leggo, chiedo domande, capisco]
Me: "Ok, procedi con setup uno per uno, approvazione singola"
Claude: [set var 1, spiega impact, attende approval]
Me: [approvo, verifico]
... (ripete per 5 var)
Risultato: setup funziona E so perché; posso fixare + documentare ADR.
```

## Quando "capire prima" fallisce

### Caso 1: Non ho tempo di capire

**Situazione**: scadenza imminente, task critico, no time to learn.

**Opzioni**:
1. **Skip task** (meglio non farlo che farlo male)
2. **Pair programming** con chi capisce
3. **Fare con supervisore** (Claude + attenzione massima)
4. **Eseguire e documentare** (con piano di comprensione post-fact)

**Mai**: eseguire blindly con "lo capirò dopo".

### Caso 2: Devo imparare facendo

**Situazione**: nuovo tool/tecnica, no way to know senza provare.

**Approccio safe**:
1. Sandbox environment (VM, Docker, repo test)
2. Read documentation basic
3. Small experiments prima di real usage
4. Poi apply su real task con confidenza

**Esempio mio**: quando ho iniziato con Claude Code, ho prima
sperimentato su repo test, poi applied al lenovo-ai-station.

### Caso 3: Legacy system nessuno capisce più

**Situazione**: devo modificare sistema dove nessuno (incluso me) ha
comprensione completa.

**Approccio**:
1. Documentazione cio che so
2. Investigation rigorosa prima di change
3. Change minimal viable
4. Test immediate
5. Rollback plan obbligatorio

**Non applicabile al mio caso attuale** (setup fresco tutto nuovo).

## Il collegamento con YAGNI

**YAGNI** dice: non fare cose non necessarie.
**Capire prima** dice: cosa che fai, capirla.

**Insieme**:
- **Meno cose fatte** (YAGNI)
- **Ognuna fatta bene** (Capire prima)

Risultato: setup minimal but deep.

**Opposto catastrofico**:
- Molte cose fatte (anti-YAGNI)
- Senza capire (anti-Capire prima)

Risultato: complessità inmaintaibile, setup fragile.

## Il collegamento con sovereign AI

**Sovereign** significa **controllo**.
**Controllo** richiede **comprensione**.
**Comprensione** richiede **capire prima**.

Se io uso Ollama ma **non so** come funziona, è diverso da "vero sovereign".
Il server è locale, i dati miei, ma la **conoscenza** è esternalizzata a blog post.

**True sovereign** = hardware locale + **comprensione** locale.

**Questa lezione è un pilastro** della filosofia sovereign.

## Meta-learning

### Il ribaltamento del dev-stereotipo

**Stereotipo dev**:
- "Moving fast and breaking things"
- "Ship it and iterate"
- "Done is better than perfect"

**Valido in alcuni contesti** (startup MVP, prototype).

**Non valido**:
- Infrastructure personale (il mio setup, il mio repo)
- Systems con dati importanti
- Operazioni irreversibili

**Mio principio attuale**: "Slow is smooth, smooth is fast"
(dall'addestramento militare, applicato a dev).

### Il paradosso della velocità

**Lento** nel capire prima → **veloce** nell'eseguire.
**Veloce** nell'eseguire subito → **lento** nel ripararе.

**Net velocity**: "capire prima" è **più veloce** nel lungo termine.

### Il debito tecnico della confusion

Ogni azione fatta senza capire genera **debito tecnico mentale**:
- Non so come funziona il mio setup
- Non posso spiegare a qualcuno
- Se si rompe non posso debuggare
- Ogni nuova aggiunta moltiplica la confusion

**Capire prima** non genera debito. Ogni azione aggiunge capital.

### La disciplina è investimento, non rinuncia

"Capire prima, fare dopo" sembra **rallentare**.
È **investimento** che si ripaga 10x nelle sessioni future.

**Mio caso concreto**:
- Sessione 19/04 notturna: molto "capire" (8 ore totali)
- Sessione 20/04 serale: meno "capire" necessario (infrastructure understood)
- Sessioni future: very fast thanks to deep foundation

## Applicazioni concrete future

### Pattern per nuovi tool

```
1. Research 30-60 min (docs, blog, video)
2. Decide se vale install (YAGNI check)
3. Capire install method (winget vs script vs manual)
4. Plan install (con backup + restore point)
5. Execute step-by-step
6. Verify after each step
7. Document decision in ADR if non-trivial
```

### Pattern per nuovi progetti

```
1. Define scope (cosa fa, cosa non fa)
2. Choose tech stack (capendo ogni choice)
3. Research patterns applicabili
4. Minimal viable setup
5. Build iteratively with understanding
```

### Pattern per debugging

```
1. Reproduce error (capire quando succede)
2. Isolate cause (capire perché)
3. Plan fix (capire come)
4. Apply fix (capire effetto)
5. Verify + regression test
6. Document lesson if interesting
```

## Template mentale

Prima di ogni azione non-banale, chiedo a me stesso:

```
☐ So cosa sto per fare?
☐ So perché lo sto facendo?
☐ So cosa può andare storto?
☐ So come tornare indietro?
☐ Ho backup/restore point?
☐ Se non capisco, ho studiato abbastanza?
```

Se anche uno solo è **No**, mi fermo e studio prima.

## Fonti di ispirazione

- Principio generale militare: "Slow is smooth, smooth is fast"
- Pratica Zen giapponese: "Shoshin" (beginner's mind — sempre curiosità)
- Kaizen: miglioramento continuo attraverso comprensione
- Toyota Production System: "Stop the line" quando c'è problema

## Follow-up

### Da osservare nei prossimi mesi

- Con quale frequenza rispetto questo principio?
- Quando mi trovo a violarlo (under pressure, fatigue)?
- Outcomes comparison: sessioni "capire prima" vs sessioni "fare prima"?

### Da espandere

- Template specifici per tipi di task comuni
- Library di "comandi già capiti" per riferimento veloce
- Checklist pre-flight per operazioni rischiose

## La frase finale

**"Il tempo speso a capire non è tempo perso. È tempo investito in non doverlo
spendere a recuperare da errori."**

Il trauma Victus mi ha insegnato questo nel modo più doloroso.
Il setup Lenovo mi sta insegnando questo nel modo più fruttifero.

Questa lezione è probabilmente la più importante che ho mai appreso come dev.
