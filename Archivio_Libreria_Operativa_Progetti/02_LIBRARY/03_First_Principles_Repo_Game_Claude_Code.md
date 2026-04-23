# First Principles Repo Game — Claude Code

## Idea centrale
Non stiamo ricostruendo un repo.
Stiamo ricostruendo il **nucleo minimo di una partita corretta, leggibile, testabile e producibile**.
Il repo deve servire quello.

## Quando usare questo modulo
Usalo quando:
- il repo è spaghetti code
- ogni nuova feature rompe altro
- la logica di gioco è mescolata alla UI o a layer secondari
- il prototipo esiste ma non regge la crescita
- c’è odore di over-engineering
- il gioco è cambiato ma l’architettura no
- non è chiaro cosa sia veramente core e cosa sia solo cerimonia
- vuoi capire se rifattorizzare, estrarre un nuovo core o quasi ricostruire

## Obiettivo
1. definire le verità fondamentali del gioco
2. definire le verità fondamentali del sistema
3. definire le verità fondamentali del repo
4. proporre l’architettura minima ricostruita
5. produrre un piano di migrazione realistico

## I 3 layer obbligatori
### Layer A — Verità fondamentali del gioco
- qual è il fantasy del giocatore?
- qual è il core loop minimo?
- qual è il vero job-to-be-done della partita?
- quali decisioni devono risultare interessanti?
- cosa rende la partita leggibile, tesa e soddisfacente?

### Layer B — Verità fondamentali del sistema
- qual è lo stato minimo del match?
- quali sono input, output e trasformazioni irriducibili?
- quali regole devono essere deterministiche?
- cosa deve essere testabile senza UI?
- cosa deve essere replayabile, serializzabile o tracciabile?

### Layer C — Verità fondamentali del repo
- quali moduli servono davvero per sostenere A e B?
- quali parti attuali sono supporto reale?
- quali parti sono cerimonia, duplicazione o accoppiamento inutile?
- dove il repo sta tradendo il sistema di gioco?
- quali dipendenze esistono per necessità e quali per abitudine?

## Sequenza operativa
1. Intake del problema
2. Verità fondamentali del gioco
3. Repo Map / Audit
4. Distrutturazione First Principles
5. Ricostruzione minima
6. Decisione strategica sulla migrazione
7. Piano di migrazione
8. Compact / Handoff

## Checklist pre-sessione per Claude Code
### Preflight obbligatorio
1. chiedi un riassunto della codebase in 5 bullet
2. chiedi quali sono le dipendenze esterne e perché esistono
3. chiedi quali moduli sembrano core vs accessori
4. fornisci i vincoli hard del progetto
5. solo dopo lancia il prompt principale

### Prompt preflight — Step 1
```text
Analizza questa codebase e dimmi in 5 bullet:
1. cosa fa davvero
2. quali sono i moduli o cartelle più importanti
3. dove vive la logica core
4. dove vedi accoppiamento sospetto
5. qual è la parte che probabilmente regge tutto il sistema
```

### Prompt preflight — Step 2
```text
Elenca tutte le dipendenze esterne e spiegami per ciascuna:
1. perché esiste
2. se è veramente necessaria
3. cosa si romperebbe rimuovendola
4. se sembra scelta per principio o per abitudine
```

### Prompt preflight — Step 3
```text
Separa questa codebase in tre categorie:
- core indispensabile
- supporto utile
- cerimonia o complessità sospetta

Per ogni area, spiegami perché la metti lì.
```

## Template vincoli per un game repo
```text
VINCOLI FONDAMENTALI DEL PROGETTO GAME:

Obiettivo core:
[es: creare un tactics game a turni/round con pianificazione leggibile e risoluzione coerente]

Esperienza target:
[es: il giocatore deve percepire strategia, anticipazione, chiarezza delle conseguenze]

Unità minima del gioco:
[es: una singola partita / un singolo encounter / un singolo round simulabile]

Utenti / contesto d’uso:
[es: giocatori che devono capire rapidamente lo stato tattico]

Vincoli tecnici hard:
[es: simulazione deterministica, stato serializzabile, replay/debug possibile, codice modulare]

Vincoli di team:
[es: team piccolo, manutenzione semplice, onboarding rapido]

Vincoli di scope:
[es: priorità al gameplay loop, non alla grafica finale]

Cosa NON è importante ora:
[es: polish visivo, feature secondarie, architetture enterprise, sistemi online]

Rischi da evitare:
[es: over-engineering, accoppiamento UI-logica, sistemi non testabili, classi god object]
```

## Prompt principale — Versione integrata game repo
```text
Agisci come un Principal Engineer e Systems Architect che usa First Principles Thinking.

CONTESTO:
Sto ricostruendo o rifattorizzando questo repo game. Non voglio copiare pattern esistenti o fare cleanup cosmetico. Voglio arrivare alle verità fondamentali del gioco, del sistema e del repo, e ricostruire da lì.

PRIMA DI ANALIZZARE IL REPO, DISTINGUI ESPLICITAMENTE QUESTI 3 LIVELLI:

A. Verità fondamentali del gioco
- qual è il core fantasy del giocatore?
- qual è il core loop minimo?
- qual è il job-to-be-done della partita?
- quali decisioni devono risultare interessanti?

B. Verità fondamentali del sistema
- qual è lo stato minimo del match?
- quali sono input, output e trasformazioni irriducibili?
- quali regole devono essere deterministiche, testabili e separabili dalla UI?
- cosa deve essere serializzabile, replayabile o facilmente ispezionabile?

C. Verità fondamentali del repo
- quali moduli servono davvero per sostenere A e B?
- quali parti del repo attuale sono supporto reale?
- quali parti sono cerimonia, duplicazione, accoppiamento inutile o residui storici?

METODO FIRST PRINCIPLES DA APPLICARE:

1. DISTRUTTURA
Analizza il progetto e identifica:
- Obiettivo fondamentale
- Vincoli reali
- Assunzioni da azzerare
- Atomi: input, output e trasformazioni minime irriducibili

2. RICOSTRUISCI
Partendo solo dagli atomi e dai vincoli:
- progetta la soluzione più semplice che rispetta i vincoli e produca l’output corretto
- giustifica ogni componente con la regola: “Esiste perché senza X fallisce il vincolo Y”
- elimina tutto ciò che non supera il test: “Se lo tolgo, il core job fallisce?”
- scegli stack, pattern e astrazioni solo dopo aver definito la struttura logica
- mantieni separati core simulation, orchestration, adapters, presentation, tooling

3. VALUTA LA STRATEGIA DI MIGRAZIONE
Confronta esplicitamente:
- refactor progressivo
- estrazione di nuovo core in parallelo
- strangler pattern
- reboot quasi totale

OUTPUT RICHIESTO:
1. Verità fondamentali ai 3 livelli
2. Tabella distrutturazione
3. Design ricostruito
4. Strategia di migrazione raccomandata
5. Piano di migrazione
6. Domande bloccanti

REGOLE:
- Zero ragionamento per analogia
- Se un pattern esiste, dimostrami che deriva da un principio fondamentale
- Sii brutale: se gran parte del repo è cerimonia, dillo
- Non ottimizzare per eleganza astratta
- Se non hai abbastanza informazioni, non inventarle: formula domande bloccanti
```

## Iterazioni chiave dopo la prima risposta
### Stress test
```text
Prendi il design ricostruito. Se domani il progetto cresce 10x o 100x in complessità, contenuti o unità in partita, cosa crolla prima? Quale principio abbiamo violato? Cosa proteggeresti subito senza complicare troppo il core?
```

### Prova di eliminazione
```text
Per ogni modulo del design ricostruito: se lo cancello, quale vincolo fondamentale violo? Se non ne violi nessuno, dimmi se il modulo è prematuro, opzionale o cerimoniale.
```

### Versione stdlib / zero-bias
```text
Rifai la distrutturazione fingendo che nessuna libreria esista. Ragiona solo con stdlib, strutture dati base e logica pura. Dimmi cosa rimane davvero necessario.
```

### Primo modulo atomico
```text
Ok. Parti dal modulo più atomico e ad alto leverage del design ricostruito. Scrivimi solo quello, con test, senza importare nulla che non sia ancora giustificato.
```

### Verifica separazione simulazione/UI
```text
Controlla il design ricostruito e dimmi dove la simulazione rischia ancora di dipendere da presentation, input layer, engine callbacks o stato UI. Proponi la separazione minima corretta.
```

### Audit testabilità
```text
Per il design ricostruito, dimmi quali moduli possono e devono essere testati in puro isolamento. Se non possono esserlo, spiegami quale principio di testabilità stiamo violando.
```

## Anti-pattern da evitare
1. Rifare bene la cosa sbagliata
2. Confondere semplice con familiare
3. Saltare i vincoli hard
4. Fare cleanup cosmetico
5. Rifare tutto quando basta estrarre il nucleo
6. Mescolare logica di gioco e logica di esecuzione
7. Introdurre astrazioni premature


## Patch epistemica — come non auto-ingannarsi
Questa sezione rafforza il modulo first principles con tre caveat critici.

### Caveat 1 — Assiomi sbagliati
Se una “verità fondamentale” è falsa, il resto del ragionamento può essere coerente ma sbagliato.

Domande di controllo:
- questa verità è osservata nel gioco reale o solo intuita?
- nasce da playtest, prototipi o comportamento dei giocatori?
- stiamo difendendo un principio reale o una preferenza personale?

### Caveat 2 — Principi giusti ma irrilevanti
Un principio può essere vero ma non toccare il problema più importante.

Domande di controllo:
- questo principio migliora davvero chiarezza, agency o qualità della partita?
- stiamo risolvendo un problema del gioco o un fastidio estetico del team?

### Caveat 3 — Costo cognitivo
Il first principles thinking ha un costo mentale alto.

Uso corretto:
- sì per design core
- sì per refactor architetturali
- sì per scelte che cambiano la traiettoria del progetto
- no come default per ogni micro-task

## Pattern di validazione game-specific da usare durante il refactor
Questi pattern non sono ricette da copiare.
Sono filtri per verificare che la ricostruzione del repo serva davvero il gioco.

### Pattern 1 — Test di cancellazione
Per ogni feature, layer o modulo chiedi:
- se lo tolgo, quale verità fondamentale violo?
- se non ne viola nessuna, è candidato a taglio, congelamento o posticipo

### Pattern 2 — Core Mechanic First
Con quasi tutto rimosso, la sequenza base del gioco è già interessante?

Per un tactics game, la sequenza minima è spesso:
- informazioni disponibili
- pianificazione
- esecuzione o risoluzione
- feedback conseguenze

Se questa sequenza non regge, il refactor tecnico va fermato e riportato al design.

### Pattern 3 — Rule of Threes
Le meccaniche chiave dovrebbero poter essere introdotte in tre passaggi o tre contesti graduati.

Uso corretto:
- tutorialization
- encounter progression
- onboarding
- escalation controllata

### Pattern 4 — Triade fondamentale del genere
Ogni genere ha una propria triade di pilastri base.
Nel tactics game una formulazione utile può essere:
- comando / intenzione
- leggibilità dello stato
- conseguenza / risoluzione

Se uno di questi tre è fragile, il repo non va solo ripulito: va riallineato.

### Pattern 5 — Player Dynamics First
Chiedi sempre:
- questa scelta aumenta chiarezza tra i giocatori?
- aumenta agency?
- produce interazione significativa?
- o aggiunge solo complessità?

### Pattern 6 — Rational Design
Una scelta non va valutata contro il gusto del designer o del programmatore.
Va valutata contro il comportamento che produce nel giocatore.

## Criteri di qualità della ricostruzione
### Sul piano del gioco
- il core loop è esplicito
- l’unità minima di partita è chiara
- la decisione interessante del giocatore è leggibile

### Sul piano del sistema
- stato minimo del match definito
- input/output/trasformazioni documentati
- determinismo chiaro dove necessario
- simulazione separabile dalla UI
- testing del core possibile

### Sul piano del repo
- moduli con responsabilità chiare
- dipendenze giustificate
- meno cerimonia
- meno accoppiamento
- piano di crescita non prematuro ma reale

### Sul piano della migrazione
- esiste un primo step a basso rischio e alto leverage
- ogni step ha definition of done
- è chiaro cosa non fare ancora

## Template di output
### Tabella distrutturazione
```text
| Elemento attuale | Categoria | Verità fondamentale sotto | Necessario ora? | Scartabile? | Motivo | Azione consigliata |
|------------------|-----------|---------------------------|-----------------|-------------|--------|--------------------|
```

### Design ricostruito
```text
DESIGN RICOSTRUITO

1. Obiettivo fondamentale
2. Architettura minima proposta
3. Responsabilità per modulo
4. Flusso principale
Input -> Validazione -> Simulazione -> Risoluzione -> Output stato -> Presentation/adapters
5. Diagramma ASCII
6. Cose volutamente escluse per ora
```

### Strategia di migrazione
```text
STRATEGIA DI MIGRAZIONE

Strategia raccomandata:
Perché questa e non le altre:
Alternative scartate:
Rischi principali:
Primo punto di controllo:
```

### Piano di migrazione
```text
PIANO DI MIGRAZIONE

Step 1:
Obiettivo:
Perché viene prima:
Task:
Definition of done:
Rischi:
...
```

### Domande bloccanti
```text
DOMANDE BLOCCANTI

1. Decisioni di gameplay ancora non definite
2. Vincoli tecnici non confermati
3. Dipendenze o componenti legacy da tenere o eliminare
4. Confini di scope
5. Scelte che richiedono decisione umana prima di codificare
```

## Mini-workflow pratico
1. apri il repo in Claude Code
2. lancia il preflight in 3 step
3. incolla i vincoli hard del progetto game
4. lancia il prompt principale integrato
5. verifica che siano emerse le verità ai 3 livelli
6. fai stress test e prova di eliminazione
7. scegli la strategia di migrazione
8. chiedi il primo modulo atomico implementabile
9. chiudi con COMPACT

## Regola finale
Se alla fine della sessione non è emerso con chiarezza:
- cosa deve fare davvero il gioco
- cosa deve fare davvero il sistema
- cosa deve fare davvero il repo

allora non abbiamo ancora rifattorizzato nulla.
Abbiamo solo guardato codice.
