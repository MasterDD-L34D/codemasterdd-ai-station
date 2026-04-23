# OpenCode / Ollama / Model Routing — Principi Estratti

Questo file non conserva gli screen come trascrizione pura.
Li trasforma in **principi operativi riusabili** da integrare nel workflow.

---

## 1. Messaggio centrale

Gli screen non sono soprattutto una libreria di prompt.
Sono una **micro-guida operativa** su tre livelli:
- tooling
- runtime locale
- model routing locale/cloud

In forma compatta, il messaggio è questo:

**Installa il tool giusto. Collega il runtime giusto. Scegli pochi modelli con ruoli chiari. Locale prima, cloud dopo.**

---

## 2. Principi operativi forti

### P01 — Local first
Prima usa il locale quando è abbastanza buono.
Passa al cloud quando serve davvero.

Perché:
- privacy
- costo
- praticità
- iterazione rapida
- minore dipendenza da provider esterni

### P02 — Non accumulare modelli
Regola esplicita dagli screen:

**Qui si sceglie. Non si accumula.**

Implica:
- pochi modelli
- ruoli chiari
- niente zoo ingestibile
- routing esplicito per scenario

### P03 — Il canale di accesso conta
Non basta chiedere “qual è il modello migliore?”.
Bisogna chiedere:
- uso locale?
- uso API esterne?
- uso cloud integrato?
- uso un client come OpenCode?

Quindi il routing dipende da:
- task
- accesso
- hardware
- budget/privacy

### P04 — Hardware-aware selection
Per il locale, la scelta del modello deve rispettare i limiti reali della macchina.

### P05 — Cloud come secondo livello, non default cieco
Il cloud è utile quando serve:
- qualità più alta
- maggiore stabilità
- accesso a modelli non disponibili in locale
- task più pesanti o più generalisti

---

## 3. Classi d'uso implicite negli screen

### Classe A — Coding puro locale
Preferenza suggerita negli screen:
- Codestral

### Classe B — Equilibrio locale qualità/velocità
Preferenza suggerita negli screen:
- Mistral

### Classe C — Locale leggero per hardware stretto
Preferenza suggerita negli screen:
- Gemma

### Classe D — API esterne
Preferenza suggerita negli screen:
- Mistral
- Codestral

### Classe E — Cloud integrato / fallback serio
Preferenza suggerita negli screen:
- Nemotron
- GPT-5 Nano

Nota archivistica:
queste preferenze vanno conservate come **ranking del carosello**, non come verità universali.

---

## 4. Distinzione fondamentale da preservare

### Da trattare come principi utili
- locale prima, cloud dopo
- non accumulare modelli
- scegliere per scenario
- tenere conto dell'hardware
- distinguere tra accesso locale, API esterne e cloud

### Da trattare come preferenze contestuali dell'autore
- ranking assoluti tra provider o modelli
- esclusioni drastiche di intere famiglie di modelli
- claim di superiorità non verificati nel nostro workflow reale

---

## 5. Reverse engineering in forma SOP

## SOP — OpenCode Local/Cloud Setup
1. installa OpenCode
2. verifica CLI e versione
3. collega OpenCode a Ollama
4. scegli un solo modello locale iniziale
5. usa locale come default per coding iterativo e task semplici
6. passa a cloud o API esterne quando locale non basta
7. documenta nel progetto quale modello usi per quale tipo di task

---

## 6. Routing sintetico derivato dagli screen

### Se vuoi...
- coding puro locale -> Codestral
- equilibrio locale -> Mistral
- hardware stretto -> Gemma
- provider esterno -> Mistral / Codestral
- cloud integrato -> Nemotron / GPT-5 Nano

Nota:
questa tabella va letta come **routing tratto dagli screen**, non come standard assoluto del sistema.

---

## 7. Collegamento con la libreria operativa

Questi screen si inseriscono bene in tre punti:

### Modulo Multi-AI
Aggiungono il sotto-livello:
**non solo quale AI usare, ma anche quale runtime/accesso usare.**

### Modulo Repo Game / Coding
Aggiungono una variante locale/cloud del workflow di coding:
- preflight locale
- coding iterativo locale
- cloud per task più pesanti o più stabili

### Workflow pratici
Aggiungono una SOP concreta di setup e routing.

---

## 8. Regola finale estratta

Se il sistema diventa “troppi modelli, troppi accessi, troppi fallback”, allora il workflow peggiora.

La regola sana da tenere è:

**pochi strumenti, ruoli chiari, routing esplicito, locale dove basta, cloud dove serve davvero.**
