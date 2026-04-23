# FIRST_PRINCIPLES_GAME_CHECKLIST

Questa checklist serve a evitare un refactor tecnico scollegato dal gioco.

Usala prima di:
- un refactor importante del repo
- una ricostruzione del core system
- una ripartenza del design tecnico
- una decisione su cosa tenere, tagliare o congelare

Legenda:
- [ ] non verificato
- [~] parziale / dubbio
- [x] verificato

---

## 1. Verità fondamentali del gioco

### 1.1 Verità in una riga ciascuna
- [ ] Ho scritto le 2–3 verità fondamentali del gioco in una riga ciascuna.
- [ ] Ogni verità descrive qualcosa che il gioco non può violare.
- [ ] Le verità non sono slogan vaghi ma vincoli reali di esperienza.

Scrivile qui:

1. 
2. 
3. 

### 1.2 Verifica degli assiomi
- [ ] Ogni verità nasce da osservazione, prototipo o playtest, non solo da gusto personale.
- [ ] Nessuna “verità” è in realtà una preferenza estetica o tecnica travestita da principio.
- [ ] Ho distinto ciò che è certo da ciò che è ancora ipotesi.

Ipotesi ancora da validare:
- 
- 

---

## 2. Core Mechanic First

- [ ] Ho definito l’unità minima di partita o esperienza.
- [ ] Ho descritto la sequenza minima che deve già funzionare bene.
- [ ] Se tolgo quasi tutto, questa sequenza resta interessante o almeno promettente.
- [ ] Se questa sequenza non regge, non sto nascondendo il problema con feature secondarie.

Sequenza minima:
1. 
2. 
3. 
4. 
5. 

Problemi della sequenza minima:
- 
- 

---

## 3. Test di cancellazione

- [ ] Ho elencato feature, sistemi o moduli principali.
- [ ] Per ciascuno ho chiesto: “se lo tolgo, quale verità fondamentale violo?”
- [ ] Ho distinto tra core, supporto utile, opzionale, cerimoniale.
- [ ] Ho identificato almeno un’area tagliabile o congelabile.

### Tabella di lavoro
| Feature / Modulo | Verità fondamentale servita | Se lo tolgo cosa si rompe? | Categoria | Azione |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

Categorie consigliate:
- core
- supporto utile
- opzionale
- cerimoniale

Azioni consigliate:
- tieni
- congela
- posticipa
- taglia

---

## 4. Triade fondamentale del progetto

- [ ] Ho definito la triade fondamentale del genere o del progetto.
- [ ] Ho verificato che nessuno dei tre pilastri sia fragile.
- [ ] Il repo non sta nascondendo debolezze di uno dei tre pilastri con complessità aggiunta.

Triade del progetto:
1. 
2. 
3. 

Punti deboli rilevati:
- 
- 

---

## 5. Rule of Threes / progressione di apprendimento

- [ ] Ho individuato la meccanica o le meccaniche chiave da insegnare.
- [ ] Ogni meccanica importante può essere introdotta in almeno 3 passaggi o contesti graduati.
- [ ] La progressione non salta subito alla punizione piena.
- [ ] L’apprendimento è costruito con variazione controllata, non solo con difficoltà crescente.

### Schema minimo
Meccanica chiave:

Introduzione 1:

Introduzione 2:

Introduzione 3:

Note:
- 

---

## 6. Player Dynamics First

- [ ] Le scelte di sistema aumentano chiarezza tra i giocatori o tra giocatore e sistema.
- [ ] Le scelte di sistema aumentano agency.
- [ ] Le scelte di sistema aumentano interazione significativa.
- [ ] Non sto premiando complessità che non migliora l’esperienza.

Valutazione rapida:
- chiarezza: 
- agency: 
- interazione significativa: 
- complessità utile: 
- complessità tossica: 

---

## 7. Rational Design

- [ ] Sto valutando le idee contro il comportamento che producono, non contro il mio gusto.
- [ ] Posso descrivere quale comportamento desidero vedere nel giocatore.
- [ ] Posso descrivere quale comportamento indesiderato il sistema produce oggi.

Comportamento desiderato:
- 

Comportamento attuale indesiderato:
- 

---

## 8. Implicazioni per il repo

- [ ] Le verità fondamentali del gioco sono state tradotte in vincoli per il repo.
- [ ] So quali moduli devono restare puri, testabili e separati dalla UI.
- [ ] So quali parti del repo sembrano servire più la storia tecnica che il gioco.
- [ ] Ho identificato almeno un confine architetturale da stabilizzare per primo.

Moduli che devono restare puri:
- 
- 

Parti del repo sospette / storiche / cerimoniali:
- 
- 

Primo confine da stabilizzare:
- 

---

## 9. Decisione finale prima del refactor

- [ ] So se devo fare refactor progressivo, nuovo core parallelo, strangler o reboot quasi totale.
- [ ] So qual è il primo step a più alto leverage e rischio controllato.
- [ ] So cosa non devo toccare ancora.

Strategia scelta:

Primo step utile:

Cosa NON toccare ancora:
- 
- 

---

## 10. Gate finale

Prima di partire col refactor, devo poter dire di sì a queste domande:

- [ ] So cosa deve fare davvero il gioco.
- [ ] So cosa deve fare davvero il sistema.
- [ ] So cosa deve fare davvero il repo.
- [ ] Sto rifattorizzando per migliorare l’esperienza, non solo l’eleganza del codice.
- [ ] Il primo sprint tecnico è già leggibile e motivato.

Se non riesco a spuntare queste cinque voci, devo fermarmi e chiarire il design o i vincoli prima di procedere.
