# First Principles Thinking nel Game Design — Analisi Ragionata

## Natura di questo documento
Questo file nasce da una **sintesi ragionata fornita in chat**.

Va trattato come:
- reference strategica ad alto valore
- ponte tra first principles e game design
- guida per evitare refactor tecnici scollegati dall’esperienza di gioco

Non va trattato come:
- fonte primaria unica
- prova definitiva o universale
- dogma da applicare senza contesto

L’uso corretto è:
**estrarre criteri, test e pattern di validazione**, poi adattarli al progetto reale.

---

## Tesi centrale del documento
Il first principles thinking funziona bene quando:
- stai decidendo architettura o design core
- hai abbastanza contesto e competenza di dominio
- vuoi separare fatti da assunzioni
- sospetti che il progetto stia vivendo di inerzia, imitazione o sovrastruttura

Funziona peggio quando:
- i tuoi assiomi sono sbagliati
- i tuoi principi sono veri ma irrilevanti per il problema concreto
- il costo cognitivo è troppo alto rispetto alla decisione da prendere
- lo applichi a micro-scelte quotidiane che non giustificano questa profondità

Conclusione pratica:
**first principles non sostituisce il pattern matching esperto; lo corregge quando il pattern matching sta trascinando il progetto fuori strada.**

---

## Tre caveat epistemici da non ignorare

### 1. Assiomi sbagliati
Se una tua “verità fondamentale” è falsa, il resto del ragionamento può essere elegante ma sbagliato.

Domande di controllo:
- questa verità viene dal gioco reale o da una preferenza personale?
- è stata osservata in playtest, prototipo o comportamento dei giocatori?
- la stiamo assumendo perché suona giusta o perché l’abbiamo verificata?

### 2. Principi giusti ma non rilevanti
Puoi ragionare bene da principi corretti ma secondari rispetto al vero problema.

Domande di controllo:
- questo principio tocca davvero la chiarezza, l’agency o la qualità del match?
- stiamo risolvendo un difetto reale del gioco o un fastidio teorico del designer/programmatore?

### 3. Costo cognitivo
Il metodo richiede energia mentale e tempo.

Uso consigliato:
- sì per scelte di design core
- sì per ricostruzioni architetturali
- sì per ripartenze di progetto
- no come default per ogni micro-task quotidiano

---

## Pattern utili estratti dal testo

Questi pattern non vanno copiati come ricette.
Vanno usati come **lenti di controllo**.

---

## Pattern 1 — Algoritmo a 5 passi tipo Musk/Rosa

### Forma sintetica
1. rendi i requisiti meno stupidi
2. cancella la parte o il processo
3. semplifica e ottimizza
4. accelera il ciclo
5. automatizza

### Cosa significa nel game dev
Prima chiedi:
- questa feature serve davvero al divertimento o alla leggibilità?
- questa pipeline serve davvero o sta solo proteggendo una scelta vecchia?

Poi tagli:
- feature
- livelli di astrazione
- passaggi di produzione
- processi di review inutili

Solo dopo ottimizzi.

### Uso corretto nell’archivio
Molto utile per:
- backlog trimming
- scope reduction
- refactor del repo
- definizione del primo sprint utile

### Rischio
Tagliare troppo presto senza aver capito l’unità minima di partita.

---

## Pattern 2 — Core Mechanic First

### Tesi
Prima di art, lore, monetizzazione o metastruttura, la meccanica base deve già avere senso.

### Domanda madre
Se tolgo quasi tutto, il gesto principale del gioco è ancora interessante?

### Traduzione pratica
Per un gioco tattico:
- la lettura dello stato
- la decisione di planning
- la risoluzione
- il feedback delle conseguenze

devono già reggersi quasi da soli.

### Uso corretto nell’archivio
Da usare in:
- modulo Game Design
- validazione dell’unità minima di partita
- gate prima di grandi refactor del repo

### Rischio
Scambiare “meccanica core” con “sistema più appariscente”.

---

## Pattern 3 — Rule of Threes

### Tesi
Una meccanica viene capita meglio se introdotta tre volte in forme graduate e variate.

### Principio sottostante
L’apprendimento efficace arriva da variazione sicura, non da punizione precoce.

### Traduzione pratica
Per ogni meccanica chiave, progettare:
1. introduzione semplice
2. variazione con un vincolo nuovo
3. combinazione o aumento di pressione

### Uso corretto nell’archivio
Da usare in:
- tutorialization
- encounter design
- onboarding
- difficulty ramp
- UX di introduzione alle meccaniche

### Rischio
Applicarla come formula meccanica a ogni sistema, invece che come criterio di progressione.

---

## Pattern 4 — Three Cs / Triadi fondamentali

### Tesi
Se i pilastri base di input-percezione-risposta sono fragili, ogni feature successiva amplifica il difetto.

### Traduzione estesa per giochi diversi
La triade precisa cambia col genere, ma il principio resta:
- input/controllo
- percezione/feedback/camera o leggibilità
- entità o avatar o unità controllata

### Per un tactics game
Una possibile triade equivalente potrebbe essere:
- comando / intenzione
- leggibilità dello stato
- conseguenza / risoluzione

### Uso corretto nell’archivio
Da usare in:
- core UX di partita
- debug di confusione sistemica
- audit di leggibilità del match

### Rischio
Importare la triade di un genere in un altro senza adattarla.

---

## Pattern 5 — Player Dynamics First

### Tesi
Specie nei giochi competitivi o cooperativi, il sistema sociale/strategico tra giocatori conta almeno quanto il sistema tecnico.

### Domande chiave
- questa scelta aumenta chiarezza tra i giocatori?
- aumenta agency?
- produce interazione significativa?
- rende il conflitto o la cooperazione più leggibili?

### Uso corretto nell’archivio
Molto utile per:
- multiplayer
- co-op
- giochi tattici di coordinazione
- giochi con informazione distribuita

### Rischio
Feticizzare l’infrastruttura tecnica e perdere il cuore relazionale del gameplay.

---

## Pattern 6 — Rational Design

### Tesi
Una buona idea non si valuta contro il gusto del designer, ma contro il comportamento che produce nel giocatore.

### Domande chiave
- cosa fa davvero il giocatore quando incontra questo sistema?
- il comportamento prodotto coincide con l’esperienza desiderata?
- stiamo misurando bellezza percepita o effetto reale?

### Uso corretto nell’archivio
Da usare in:
- review di design
- test di feature
- valutazione di esperimenti
- backlog prioritization

### Rischio
Ridurre tutto a metriche sterili senza leggere il contesto qualitativo dell’esperienza.

---

## Come usare questi pattern nel refactor del repo

Il principio più importante è questo:

**il repo non va rifatto partendo da ciò che rende il codice più elegante, ma da ciò che rende il gioco più chiaro, interessante e apprendibile.**

### Ordine corretto
1. definisci 2–3 verità fisiche o sistemiche del gioco
2. applica test di cancellazione a feature e moduli
3. valida che la meccanica base sia già forte
4. controlla la progressione di apprendimento
5. solo dopo scegli la forma del refactor

---

## Test pratici da derivare dal testo

### Test 1 — Verità fisiche del gioco
Scrivi in una riga ciascuna le 2–3 verità che il sistema non può violare.

Esempi generici:
- la risoluzione deve essere leggibile
- il giocatore deve poter prevedere abbastanza da pianificare
- la simulazione deve essere coerente con i segnali mostrati

### Test 2 — Test di cancellazione
Per ogni feature o modulo chiedi:
- se lo tolgo, quale verità fondamentale viene violata?
- se nessuna, è candidato al taglio, congelamento o posticipo

### Test 3 — Core Mechanic First
Con quasi tutto rimosso, il nucleo di partita è ancora interessante?

### Test 4 — Curriculum minimo
La meccanica chiave viene introdotta in almeno 3 forme graduate?

### Test 5 — Player Dynamics First
Questa scelta aumenta:
- chiarezza
- agency
- interazione significativa

Se aumenta solo complessità o “fascino teorico”, non basta.

---

## Mapping diretto su Evo Tactics

Questa parte non è una verità definitiva: è una lettura operativa di come usare il testo sul progetto.

### Ipotesi di verità fondamentali da verificare
- la pianificazione deve produrre una decisione interessante e condivisibile
- la risoluzione deve essere coerente e leggibile a posteriori
- la distribuzione dell’informazione deve aumentare tensione strategica, non confusione sterile

### Core Mechanic First applicato
La sequenza minima da validare è:
- informazioni disponibili
- confronto e pianificazione
- inserimento scelte
- risoluzione
- feedback delle conseguenze

Se questa sequenza non è già forte, il refactor tecnico deve fermarsi e tornare al design.

### Rule of Threes applicata
Le meccaniche chiave da introdurre gradualmente potrebbero essere:
- lettura del contesto
- coordinazione tra player/device
- velocità/reazione/ordine di risoluzione
- gestione del rischio informativo

### Player Dynamics First applicata
Ogni scelta sistemica andrebbe valutata chiedendo:
- rende più chiara la collaborazione?
- rende il conflitto più leggibile?
- aumenta agency o solo complessità?

---

## Dove collegare questa reference nell’archivio

### Moduli da rafforzare
- `02_LIBRARY/03_First_Principles_Repo_Game_Claude_Code.md`
- `02_LIBRARY/02_Modules_Starter_Packs_and_Best_Of.md`
- `04_BOOTSTRAP_KIT/FIRST_PRINCIPLES_GAME_CHECKLIST.md`

### Uso consigliato
- lettura prima di un refactor importante
- supporto alla definizione di verità fondamentali
- supporto alla riduzione scope
- supporto alla validazione del core loop

---

## Regola finale della reference
Questa analisi non serve a rendere il progetto “più filosofico”.
Serve a impedire due errori:

1. rifare bene la cosa sbagliata
2. scambiare eleganza tecnica per qualità dell’esperienza

Il suo uso corretto è come filtro di qualità tra:
- design core
- architettura del sistema
- refactor del repo
