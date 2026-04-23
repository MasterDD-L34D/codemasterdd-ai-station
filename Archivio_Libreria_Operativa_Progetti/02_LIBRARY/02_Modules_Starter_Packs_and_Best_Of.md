# Modules, Starter Packs and Best-Of

## Moduli verticali inclusi
- Game Design
- Software / Coding
- Ricerca / Deep Research
- Creativo / Brand / Writing
- UX / Product / Systems

## Modulo 1 — Game Design
### Obiettivi
- chiarire il fantasy del giocatore
- definire core loop e sub-loop
- progettare sistemi coerenti
- controllare leggibilità e complessità
- trasformare idee in documenti di design utili

### Prompt — Core Loop Architect
```text
Agisci come Game Systems Designer senior.
Analizza questa idea di gioco e definisci:
1. player fantasy centrale
2. core loop in 3–7 passaggi
3. sub-loop principali
4. decisioni ricorrenti del giocatore
5. fonti di tensione, rischio e ricompensa
6. dove il sistema rischia di diventare noioso, confuso o troppo costoso da produrre

Contesto:
[incolla idea]

Output come mini design brief leggibile da team creativo e tecnico.
```

### Prompt — Combat / Systems Audit
```text
Agisci come Systems Designer e QA di game design.
Esamina questo sistema di combattimento o di regole.

Voglio:
1. punti forti reali
2. complessità utile vs complessità tossica
3. exploit possibili
4. problemi di leggibilità per il giocatore
5. edge case
6. suggerimenti di semplificazione senza perdere profondità

Materiale:
[incolla sistema]
```

### Prompt — One Match Experience
```text
Agisci come Product Designer del gameplay.
Descrivi come si vive una singola partita dall’inizio alla fine.

Copri:
1. onboarding
2. fase di lettura situazione
3. decisioni interessanti
4. momenti di tensione
5. feedback e chiarezza
6. condizioni di confusione o frustrazione
7. sensazione finale della partita

Restituisci il risultato come esperienza completa di play session.
```


### Pattern di design core derivati da first principles
Questi pattern vanno usati come lenti di validazione, non come ricette.

#### Core Mechanic First
Prima di espandere sistemi, contenuti o repo, verifica che la meccanica base regga da sola.

Domande chiave:
- il gesto o ciclo principale è già interessante?
- la sequenza minima della partita è leggibile?
- la tensione nasce dal sistema o da sovrastrutture cosmetiche?

#### Rule of Threes
Le meccaniche chiave dovrebbero poter essere introdotte in tre contesti graduati.

Usi consigliati:
- onboarding
- tutorialization
- encounter progression
- aumento progressivo del carico cognitivo

#### Triade fondamentale del genere
Per ogni progetto definisci la triade di pilastri che non possono essere fragili.

Esempio per un tactics game:
- comando / intenzione
- leggibilità dello stato
- conseguenza / risoluzione

#### Player Dynamics First
Valuta ogni sistema chiedendo:
- aumenta chiarezza?
- aumenta agency?
- aumenta interazione significativa?
- o aumenta solo complessità?

#### Rational Design
Misura le idee contro il comportamento prodotto nel giocatore, non contro il gusto del designer.

### Prompt — First Principles Game Validation
```text
Agisci come Game Systems Designer che usa first principles.

Analizza questo gioco o sistema e dimmi:
1. quali sono le 2–3 verità fondamentali che non possiamo violare
2. se la meccanica core regge già quasi da sola
3. quale sarebbe la triade fondamentale del genere o del progetto
4. se le meccaniche chiave hanno una progressione tipo Rule of Threes
5. se le scelte attuali migliorano davvero chiarezza, agency e interazione significativa
6. quali feature o sistemi sembrano sopravvivere solo per inerzia

Materiale:
[incolla design notes, loop, sistema o brief]
```

### Prompt — Feature Cancellation Test
```text
Agisci come Systems Designer e PM di design.

Prendi questa lista di feature o moduli e valuta per ciascuna:
1. quale verità fondamentale serve
2. se la sua assenza violerebbe davvero una verità del gioco
3. se è core, supporto utile, opzionale o cerimoniale
4. se va tenuta, congelata, posticipata o tagliata

Materiale:
[incolla lista feature, moduli o backlog]
```

## Modulo 2 — Software / Coding
### Prompt — Repo Mapper
```text
Agisci come Software Architect.
Voglio una mappa leggibile del repository.

Per favore:
1. identifica le cartelle principali
2. spiega la funzione di ogni area
3. evidenzia dipendenze tra moduli
4. individua i file più critici
5. segnala zone incomplete, fragili o ridondanti
6. concludi con la migliore prossima area da stabilizzare

Materiale:
[repo tree / file list / documentazione]
```

### Prompt — Technical Task Breaker
```text
Agisci come Tech Lead e PM tecnico.
Trasforma questo obiettivo in task implementabili.

Restituisci:
1. sottoproblemi tecnici
2. ordine consigliato
3. dipendenze
4. rischi
5. definizione di fatto per ogni task
6. backlog finale prioritizzato

Obiettivo:
[incolla obiettivo]
```

### Prompt — Security Review
```text
Agisci come Security Auditor.
Esamina questo codice o questa feature per:
- SQL injection
- XSS
- auth flaws
- input validation issues
- data exposure
- privilege escalation risks

Voglio:
1. vulnerabilità trovate
2. gravità
3. exploit plausibile
4. patch consigliata
5. versione corretta del codice se possibile

Materiale:
[incolla codice]
```

## Modulo 3 — Ricerca / Deep Research
### Prompt — Research Structurer
```text
Agisci come Research Analyst.
Organizza questa richiesta di ricerca in modo professionale.

Voglio:
1. domanda centrale
2. sotto-domande
3. criteri di confronto
4. dati da cercare
5. rischi di bias o fonti deboli
6. formato finale del report

Tema:
[incolla tema]
```

### Prompt — Dense Summary
```text
Leggi questo materiale e restituisci una sintesi ad alta densità.

Preserva:
1. fatti
2. numeri
3. date
4. nomi
5. istruzioni pratiche
6. struttura logica del documento

Rimuovi:
- filler
- ripetizioni
- marketing language
- formattazione non essenziale

Output solo in plain text ben organizzato.

Materiale:
[incolla testo o documento]
```

### Prompt — Research to Action
```text
Agisci come analista strategico.
Partendo da questa ricerca, dimmi:
1. cosa è veramente importante
2. cosa cambia nelle decisioni da prendere
3. cosa possiamo ignorare
4. quali sono i 3 prossimi passi più utili

Ricerca:
[incolla sintesi o report]
```

## Modulo 4 — Creativo / Brand / Writing
### Brand Voice Builder
```text
Study these 3 samples of my content: [paste]. Define my brand voice in clear terms: tone, vocabulary I use, topics I own, how I open posts, how I close them. Then write me a brand voice guide I can paste into any AI tool so every piece of content sounds like me, not a robot.
```

### Data to Content Plan
```text
You're a social media analyst. Here's my data: [paste]. Tell me what's working, what's killing my reach, where my content gaps are, how often I should post, and a 90-day growth plan with clear KPIs. Be specific.
```

### Strategic Brand Identity
```text
You are a Brand Strategist and Creative Director who builds category-defining brands. Build a strategic brand identity for [COMPANY].

Rules:
- Treat brand as a market positioning tool, not a visual exercise
- Every decision must answer: "Why does this help the brand win?"
- No moodboards, no logo concepts without strategic rationale

Deliver in this order:
1. Competitive landscape
2. Brand narrative
3. Visual system rationale
4. Identity behavior
5. Decision filter

Output must read like a CMO-level strategy brief.
```

## Modulo 5 — UX / Product / Systems
### UX Systems Thinker
```text
You are a Senior Product Designer who optimizes for user behavior, not screen aesthetics. Design a complete experience system for [APP TYPE].

Rules:
- Design friction intentionally, some should stay, some must go
- Assume real users, incomplete data, errors, and skill variance
- No wireframes without behavioral rationale

Deliver in this order:
1. Intent mapping
2. Behavioral design
3. Interface systems
4. Edge cases
5. Skill-level adaptation
6. Anti-patterns

Output must read like a behavioral design brief, not a UX checklist.
```

### Design Ops / Figma System
```text
You are a Design Operations Specialist who builds Figma systems that survive team growth and product pivots. Convert [IDEA/DESIGN] into a scalable Figma system.

Rules:
- Treat Figma architecture as infrastructure, not craft
- Optimize for onboarding speed, decision speed, zero-rework updates
- Assume 3–10 designers, multiple surfaces, ongoing dev handoff

Deliver in this order:
1. System architecture
2. Component logic
3. Naming system
4. Handoff infrastructure
5. Maintenance protocol
6. Onboarding standard

Output must read like a systems spec, not a design handoff note.
```

## Prompt best-of selezionati
### Best-of universale — mettere ordine
```text
Agisci come Project Architect + PM + Archivist.

Partendo da questo materiale:
[incolla idea, note o materiali]

1. crea un brief pulito
2. separa obiettivi, vincoli, problemi e materiali esistenti
3. proponi la struttura di cartelle e file
4. crea un backlog iniziale prioritizzato
5. indica la prossima azione singola più utile

Mantieni tutto ordinato, riusabile e leggibile fuori contesto.
```

### Best-of universale — da caos a piano
```text
Trasforma questo caos in un piano operativo.

Voglio:
1. cosa stiamo cercando davvero di fare
2. cosa conta e cosa è rumore
3. ordine corretto di esecuzione
4. blocchi e dipendenze
5. primi 5 task concreti

Materiale:
[incolla appunti, idee, chat o testo grezzo]
```

### Best-of universale — audit spietato
```text
Agisci come revisore severo ma utile.
Analizza questo materiale e dimmi:
1. cosa funziona davvero
2. dove è confuso, debole o incompleto
3. quali parti sono fumo e quali sostanza
4. i 3 problemi più importanti da correggere subito
5. come correggerli nel modo più semplice possibile

Materiale:
[incolla testo, sistema, documento, piano o codice]
```

### Best-of universale — decisione tra opzioni
```text
Confronta queste opzioni come un decisore strategico.

Per ciascuna valuta:
- vantaggi reali
- costi nascosti
- rischi
- complessità
- velocità di esecuzione
- probabilità di successo

Poi raccomanda una scelta unica e spiega perché.

Opzioni:
[incolla opzioni]
```

### Best-of universale — compact perfetto
```text
Riassumi questa sessione in formato riutilizzabile per una nuova chat.

Includi solo:
1. obiettivo iniziale
2. contesto davvero utile
3. decisioni prese e perché
4. output prodotti
5. problemi aperti
6. prossimi 3 passi

Niente filler. Niente small talk. Nessuna spiegazione inutile.
```

## Varianti italiane forti
- Database Designer
- Security Auditor
- Brand Voice Builder
- Data to Action
- UX Systems Thinker
- Design Ops / Figma
- Compact Skill

## Starter pack inclusi
1. Nuovo Progetto Generico
2. Game Design
3. Repo Software / Coding
4. Deep Research
5. Brand / Prodotto / Contenuti
6. Scrittura / Worldbuilding / Creativo
