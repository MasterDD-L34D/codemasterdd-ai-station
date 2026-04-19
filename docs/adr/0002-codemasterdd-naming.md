# ADR 0002 — Naming: CodeMasterDD invece di Lenovo

**Status**: Accepted
**Data**: 2026-04-20
**Decisore**: Eduardo Scarpelli
**Tipo decisione**: naming, branding, identità

## Contesto

### Situazione

Il 19 aprile 2026, dopo setup della workstation, ho inizializzato un repo
Git locale chiamato `lenovo-ai-station` in `C:\dev\lenovo-ai-station\`.

Il giorno successivo, poco prima di pushare il repo su GitHub, mi sono
fermato. Il nome "lenovo-ai-station" non mi convinceva.

### Gli identificatori coinvolti

Il mio ecosistema ha 4 identificatori diversi potenzialmente rilevanti:

1. **GitHub username**: `MasterDD-L34D` (con leet speak "L Three Four D")
2. **Nome PC Windows**: `CodeMasterDD` (chosen da me, non default Lenovo)
3. **Windows user account**: `edusc`
4. **Email**: `eduscarpelli@gmail.com`

Il nome repo iniziale `lenovo-ai-station` era coerente con il modello
hardware (LOQ Tower 17IAX10, brand Lenovo) ma **non rifletteva l'identità
che io avevo scelto** per il PC (`CodeMasterDD`).

### Il problema

**Vincolo brand = fragilità identitaria**.

Se un giorno:
- Cambio hardware (upgrade, sostituzione)
- Lenovo va in conflitto reputazionale
- Mi stufo del modello

Il nome `lenovo-ai-station` diventa legacy/obsoleto.

Invece `CodeMasterDD` è:
- Nome **mio**, non vendor
- Parte del mio handle GitHub (MasterDD)
- Durerà finché io voglio che duri
- Identifica il **concetto di macchina**, non il brand

## Decisione

Rinomino il repo **GitHub** da `lenovo-ai-station` a `codemasterdd-ai-station`.

Il suffisso `-ai-station` si mantiene (descrive lo scopo: infrastructure
per dev workstation AI).

**Cartella locale** `C:\dev\lenovo-ai-station\` rimane invariata per ora,
per evitare:
- Claude Code ha paths memorizzati
- Eventuali script con path hardcoded
- Disallineamento temporaneo minore

Il disallineamento tra nome cartella locale e nome repo GitHub è
**accettabile temporaneamente** — GitHub è la "source of truth" per il
nome ufficiale, la cartella locale è implementation detail.

### Modifiche ai file

**README.md**:
```diff
-# Lenovo LOQ Tower 17IAX10 AI Workstation
+# CodeMasterDD AI Workstation

-**Infrastructure-as-code** del desktop Lenovo LOQ Tower 17IAX10 dedicato allo sviluppo AI agentic.
+**Infrastructure-as-code** del desktop CodeMasterDD (Lenovo LOQ Tower 17IAX10) dedicato allo sviluppo AI agentic.
```

**CLAUDE.md**:
```diff
-# CLAUDE.md — Lenovo AI Station
+# CLAUDE.md — CodeMasterDD AI Station

 ## Hardware (definitivo)
-- **Lenovo LOQ Tower 17IAX10** (desktop)
+- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10, desktop)

 ## Ecosistema device
-- **Lenovo LOQ Tower 17IAX10**: workstation primaria AI agentic
-- **Ryzen 9600X desktop**: PC appoggio corrente, dismissione graduale quando Lenovo ha tutto
+- **CodeMasterDD** (Lenovo LOQ Tower 17IAX10): workstation primaria AI agentic
+- **Ryzen 9600X desktop**: PC appoggio corrente, dismissione graduale quando CodeMasterDD ha tutto
```

**JOURNAL.md**:
```diff
-# Journal — Lenovo AI Station
+# Journal — CodeMasterDD AI Station
```

**Totale**: 7 edit su 3 file.

### Comando GitHub

```bash
gh repo create MasterDD-L34D/codemasterdd-ai-station \
  --private \
  --source=. \
  --remote=origin \
  --push
```

Commit dedicato prima del push:
```
docs: rename workstation label to CodeMasterDD
```

## Conseguenze

### Positive

**Identità coerente**:
- Repo name ↔ PC name ↔ tuo handle GitHub
- Una singola visione unificata

**Future-proof**:
- Se cambio hardware, nome valido
- Se upgrade componenti, nome valido
- Se vendo Lenovo, nome valido

**Professionale**:
- `codemasterdd-ai-station` suggerisce device specifico (non vendor-generic)
- Si integra bene nel portfolio GitHub sotto handle MasterDD-L34D

**Brand personale**:
- Rafforza identità `CodeMasterDD` come "my primary dev machine"
- Se un domani avrò altre macchine (Mac mini?) le chiamo coerentemente
  (es. `<other-machine-name>-ai-station`)

### Negative

**Disallineamento cartella vs repo** (temporaneo):
- Cartella: `C:\dev\lenovo-ai-station\`
- Repo: `MasterDD-L34D/codemasterdd-ai-station`
- Risolvibile in futuro con rename cartella (operazione separata)

**Se altri clonano il repo** (caso ipotetico):
- Di default Git clona in cartella chiamata come il repo (`codemasterdd-ai-station`)
- Quindi disallineamento solo sul mio PC

**Confusione mentale breve**:
- Ricordare "locale si chiama lenovo, remoto si chiama codemasterdd"
- Finché non rinomino la cartella, devo tenerlo a mente

**Mitigation**: ho documentato il disallineamento in README.md + JOURNAL.md.

## Alternative considerate

### Alternative 1: Mantieni `lenovo-ai-station`
**Pro**: zero rework
**Contro**: vendor-vincolato, non identitario
**Perché scartata**: vale i 20 minuti di rework per identità migliore durevole

### Alternative 2: Solo `codemasterdd`
**Pro**: nome breve, memorabile
**Contro**: non comunica scopo (cosa c'è dentro? progetto? infrastructure?)
**Perché scartata**: troppo generico, leggibilità ridotta

### Alternative 3: `ai-workstation` (generico, no machine)
**Pro**: neutrale, future-proof multi-device
**Contro**: richiederebbe ristrutturazione tipo `machines/lenovo-xxx/`
**Perché scartata**: over-engineering per un solo device attuale

### Alternative 4: `dev-infrastructure`
**Pro**: molto generico, pulito
**Contro**: troppo generico, poca informazione specifica
**Perché scartata**: perde legame con macchina

### Alternative 5: `codemasterdd-workstation`
**Pro**: esplicita dev workstation
**Contro**: ridondante (workstation è già "infrastructure")
**Perché scartata**: `-ai-station` è più preciso dello scopo

### Alternative 6: `eduardo-ai-station`
**Pro**: nome personale proprio
**Contro**: se un domani diventa public, privacy name-based
**Perché scartata**: `codemasterdd` è nome virtuale, meno esposto

## Cambiamento del GitHub username?

**Non considerato**. Il mio handle GitHub `MasterDD-L34D` è:
- Identità **storica** (dal 2019+, molti anni di attività)
- Tatuato (metaforicamente — è parte di chi sono come dev)
- Linkato a commit history di tutti i repo (cambiarlo romperebbe continuità)

Il leet speak "L-3-4-D" sembra strano ma è il mio nome **dev** consolidato.
**Non si cambia un tattoo per estetica**. Si lascia com'è.

## Meta-learning

### Perché "fermarsi prima di azioni lente-reversibili"

Rinominare un repo su GitHub è **semi-reversibile**:
- GitHub permette rename con redirect automatico
- Ma link vecchi possono rompersi in edge cases
- CI/CD, webhook, bookmarks possono avere vecchio URL

Quindi **meglio scegliere nome giusto la prima volta**.

Il momento di maggiore attrito è il push iniziale (prima che nome diventi
noto). Dopo, il costo aumenta col tempo.

**Regola**: **fermarsi 5 minuti prima di push iniziale** per riflettere
sul nome. Può risparmiare ore di rework dopo.

### Identità tecnica = identità personale

Il nome del mio PC è parte di come io mi percepisco come dev.
Quando digito `CodeMasterDD` in uno script, sento "questo è il mio
ambiente, il mio setup, il mio spazio".

Brand `Lenovo` è utile per assistenza tecnica, warranty, ecc.
Ma **non è identity** per me.

Separare questi due livelli mi aiuta mentalmente:
- "CodeMasterDD" = identity layer (personale)
- "LOQ Tower 17IAX10" = hardware layer (tecnico)

### L'importanza di essere "pickable"

Quando ho presentato al Claude AI le opzioni A/B/C/D per scegliere il nome,
non ho semplicemente accettato il suo suggerimento. Ho valutato tutte e 4.
Ho anche considerato Alternatives (E, F) non nel menu.

**Questo pattern di pensiero è l'opposto del copy-paste**. È **decision-making
deliberato**.

Claude AI ha funzione di **thinking partner** (opzioni + pro/contro),
non di decider. Io mantengo autorità decisionale.

### Quando accettare un nome imperfetto?

**Mai per fretta**. Sempre per scelta.

Se il nome è "abbastanza buono" e non sono sicuro del migliore,
lo documento come scelta consapevole (come sto facendo ora in questo ADR).
Rileggendo, **so che non è stato accident** ma decisione.

## Riferimenti

- GitHub repo: https://github.com/MasterDD-L34D/codemasterdd-ai-station
- Commit rinomina: `eb425d1 docs: rename workstation label to CodeMasterDD`
- File modificati: README.md, CLAUDE.md, JOURNAL.md (7 edit totali)

## Follow-up

**Possibile futuro**: rename anche della cartella locale
`C:\dev\lenovo-ai-station\` → `C:\dev\codemasterdd-ai-station\`.

**Quando farlo**:
- In sessione dedicata con Claude Code chiuso
- Con verifica che non ci siano script con path hardcoded
- Con aggiornamento eventuale memoria Claude Code

**Non urgente**: è estetica, non funzionale.

## Appendice: messaggio che ho scritto a Claude Code per il rework

```
Decisione finale: rinominiamo il repo in "codemasterdd-ai-station".

Motivazione: "CodeMasterDD" è il nome del PC Lenovo e identifica
l'identità del device, non il brand Lenovo. Più personale e future-proof
(se cambio hardware).

Correzioni da fare PRIMA di gh repo create:
[...dettaglio edit...]

La cartella locale rimane C:\dev\lenovo-ai-station (cambiare nome cartella
è separato e rischioso, lo facciamo dopo se vuoi).

Approva manualmente ogni passo. Mostrami gli edits prima.
```

Questo è un buon **template** per future decisioni di rinomina:
1. Enuncia **decisione finale** (non "sto pensando di...")
2. Esplicita **motivazione** (future-proof, identity)
3. Lista **edit specifici** (file + diff)
4. Scope **esplicito** (cosa NON tocchiamo)
5. Preferenza **review before apply** (mostrami prima)
