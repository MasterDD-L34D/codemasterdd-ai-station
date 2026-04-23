# MODEL_ROUTING

## Scopo
Definire **quale strumento / modello / accesso** usare per ogni fase del progetto.

Questo file evita:
- usare sempre lo stesso strumento per tutto
- accumulare troppi modelli senza ruoli chiari
- mandare materiale grezzo nello strumento sbagliato
- perdere tempo e costo su task che potrebbero essere locali o più economici

---

## Regola madre
**Fonte complessa -> Comprensione -> Compressione -> Decisione -> Esecuzione -> Compact -> Archivio**

Per ogni fase, compila:
- strumento
- accesso
- modello
- motivo
- output atteso
- criterio di passaggio alla fase successiva

---

## Profilo progetto
- Nome progetto:
- Tipo progetto:
- Contesto principale: [repo / documentazione / ricerca / brand / misto]
- Vincoli privacy:
- Vincoli costo:
- Vincoli hardware:
- Vincoli velocità:
- Priorità principale: [qualità / velocità / privacy / costo / integrazione repo]

---

## Stack disponibile

### Strumenti disponibili
- [ ] ChatGPT
- [ ] Claude Code
- [ ] NotebookLM
- [ ] OpenCode
- [ ] Ollama
- [ ] Modelli locali
- [ ] API esterne
- [ ] Altro:

### Accessi disponibili
- [ ] Locale puro
- [ ] Cloud integrato
- [ ] API provider esterni
- [ ] Repo aperto nello strumento
- [ ] Fonti documentali caricate

---

## Routing per fase

| Fase | Obiettivo | Strumento scelto | Accesso | Modello | Perché | Output atteso | Quando passare oltre |
|---|---|---|---|---|---|---|---|
| Comprensione fonti | | | | | | | |
| Sintesi / compressione | | | | | | | |
| Strutturazione / planning | | | | | | | |
| Repo map / audit | | | | | | | |
| Coding / implementazione | | | | | | | |
| Review / audit | | | | | | | |
| Compact / archivio | | | | | | | |

---

## Routing consigliato per scenario

### Se ho molte fonti eterogenee
- Strumento preferito:
- Modello / accesso:
- Motivo:
- Output che voglio ottenere:

### Se devo capire e toccare il repo
- Strumento preferito:
- Modello / accesso:
- Motivo:
- Output che voglio ottenere:

### Se devo scrivere documenti, backlog, decision log o prompt
- Strumento preferito:
- Modello / accesso:
- Motivo:
- Output che voglio ottenere:

### Se devo lavorare in locale per privacy o costo
- Strumento preferito:
- Modello locale:
- Limiti hardware:
- Quando passare al cloud:

### Se devo usare il cloud
- Strumento preferito:
- Modello cloud:
- Perché proprio qui:
- Cosa non mandare al cloud:

---

## Policy locale / cloud

### Locale prima?
- [ ] Sì
- [ ] No
- Motivo:

### Quando il locale basta
- 
- 
- 

### Quando il cloud è giustificato
- 
- 
- 

### Materiali che non devono uscire in cloud
- 
- 
- 

---

## Modelli attivi del progetto
Compila solo i modelli che userai davvero.

| Modello | Runtime / accesso | Ruolo | Quando usarlo | Quando NON usarlo |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |

Regola:
meglio **pochi modelli con ruoli chiari** che molti modelli sovrapposti.

---

## Scelte operative minime

### Modello locale principale
- Nome:
- Ruolo:
- Perché lui:

### Modello cloud principale
- Nome:
- Ruolo:
- Perché lui:

### Modello fallback
- Nome:
- Ruolo:
- Quando entra in gioco:

---

## Integrazione con la libreria

### Prompt ponte da usare tra strumenti
- Da NotebookLM a ChatGPT:
- Da ChatGPT a Claude Code:
- Da OpenCode/Ollama a archivio:

### File da aggiornare dopo ogni passaggio importante
- [ ] COMPACT_CONTEXT.md
- [ ] DECISIONS_LOG.md
- [ ] BACKLOG.md
- [ ] REFERENCE_INDEX.md

---

## Regole anti-caos
- non fare la stessa cosa in tre strumenti
- non mandare fonti grezze nel coding tool se prima vanno capite
- non accumulare modelli “per sicurezza”
- non tenere implicito il routing: scrivilo
- se un passaggio aumenta caos invece di ridurlo, fermati e consolida

---

## Decisione finale attuale
- Workflow primario del progetto:
- Strumento principale di comprensione:
- Strumento principale di esecuzione:
- Strumento principale di archivio / orchestrazione:
- Prossimo test da fare sul routing:
