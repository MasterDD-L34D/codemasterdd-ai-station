# FIRST_PRINCIPLES_INFRA_CHECKLIST

Checklist first-principles per repo **infrastructure-as-code / governance / workflow-glue** (NON gameplay). Adatta del template `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/FIRST_PRINCIPLES_GAME_CHECKLIST.md`: tenute le sezioni generiche (test di cancellazione, triade, rational design, decision gate), riformulate quelle game-only (Rule of Threes -> Bootstrap onboarding; Player Dynamics -> Operator dynamics).

Risolve la dipendenza circolare di `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/REPO_AUTONOMY_READINESS_CHECKLIST.md` sezione D ("Esiste una checklist first-principles compilabile") per i repo infra-only come codemasterdd.

Origine OD-005 (closed 2026-05-28). Anchor filosofico: `docs/adr/0005-yagni-minimalism-approach.md`.

Usala prima di:
- un refactor importante del repo infra
- una ricostruzione del core workflow / governance scaffolding
- una decisione su cosa tenere, tagliare, congelare (es. eliminazione di un wrapper, un ADR superseded, una skill non usata)
- una valutazione "questo repo vale la propria complessita?"

Legenda:
- [ ] non verificato
- [~] parziale / dubbio
- [x] verificato

---

## 1. Verita fondamentali del repo

### 1.1 Verita in una riga ciascuna
- [ ] Ho scritto le 2-3 verita fondamentali del repo in una riga ciascuna.
- [ ] Ogni verita descrive qualcosa che il repo NON puo violare (non un goal, un invariante).
- [ ] Le verita non sono slogan ("infrastructure-first!") ma vincoli reali di workflow.

Scrivile qui:

1. 
2. 
3. 

### 1.2 Verifica degli assiomi
- [ ] Ogni verita nasce da uso reale (sessioni effettive, bug visto, decisione presa), non solo da gusto.
- [ ] Nessuna "verita" e in realta una preferenza tecnica (es. "tutto sovereign") travestita da principio (sovereign-where-it-matters e diverso da sovereign-everywhere).
- [ ] Ho distinto cio che e certo (n>=3 evidenze) da cio che e ancora ipotesi.

Ipotesi ancora da validare:
- 
- 

---

## 2. Core Capability First

L'equivalente infra del "Core Mechanic First" gameplay: qual e la sequenza minima di workflow che il repo deve gia supportare bene?

- [ ] Ho definito l'unita minima di workflow operativo (es. "session start -> delegate task -> review -> commit -> push").
- [ ] Ho descritto la sequenza minima end-to-end che deve gia funzionare senza attriti.
- [ ] Se tolgo quasi tutti i tool/script/template, la sequenza minima resta operabile.
- [ ] Se la sequenza minima non regge, non sto nascondendo il problema con feature secondarie (es. skill esoteriche, agent ridondanti, dashboard non usate).

Sequenza minima end-to-end:
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

- [ ] Ho elencato tool, script, agent, skill, ADR principali del repo.
- [ ] Per ciascuno ho chiesto: "se lo tolgo, quale verita fondamentale violo? quale workflow concreto si ferma?".
- [ ] Ho distinto tra core, supporto utile, opzionale, cerimoniale.
- [ ] Ho identificato almeno un'area tagliabile o congelabile.

### Tabella di lavoro
| Asset (tool / script / agent / skill / ADR / doc) | Verita fondamentale servita | Se lo tolgo cosa si rompe? | Categoria | Azione |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

Categorie consigliate:
- core (il workflow minimo lo richiede)
- supporto utile (riduce attrito senza essere strict-required)
- opzionale (nice-to-have, attivabile su trigger)
- cerimoniale (esiste per inerzia / template / ricordo storico)

Azioni consigliate:
- tieni
- congela (sposta in `Archivio_*/` o marca DEFERRED)
- posticipa (riapri solo su trigger esplicito)
- taglia (rimuovi)

---

## 4. Triade fondamentale del repo

L'equivalente infra della triade gameplay: i 3 pilastri stabili che giustificano l'esistenza del repo. Solitamente: **mission** (perche esiste) + **scope** (cosa fa e cosa NON fa) + **constraint dominante** (il vincolo non-negoziabile, es. sovereign-first / zero-subscription / cross-fleet-coordinated).

- [ ] Ho definito la triade fondamentale del repo.
- [ ] Ho verificato che nessuno dei tre pilastri sia fragile (es. constraint che non regge sotto pressione costo o tempo).
- [ ] Il repo non sta nascondendo debolezze di uno dei tre con complessita aggiunta (es. wrapper su wrapper per evitare di affrontare il vero constraint).

Triade:
1. mission: 
2. scope: 
3. constraint dominante: 

Punti deboli rilevati:
- 
- 

---

## 5. Bootstrap onboarding (l'equivalente infra della "Rule of Threes")

Per un repo infra, la "progressione di apprendimento" e il path di onboarding: nuovo clone (Lenovo->Ryzen / Ryzen->macchina-x), nuova sessione Claude Code, nuovo agent che eredita lo stato. Se richiede 30 step la prima sessione, qualcosa non va.

- [ ] Esiste un entry-point chiaro per nuova sessione (es. `CLAUDE.md` + `COMPACT_CONTEXT.md` + `STATUS_MULTI_REPO.md`).
- [ ] In <=3 letture concettuali il nuovo arrivato (umano o agent) capisce: ruolo del repo, stato corrente, prossime azioni.
- [ ] Onboarding non salta subito alla complessita interna (es. ADR-storia-15-decisioni) prima del big-picture.
- [ ] L'onboarding e costruito con variazione controllata (light reading -> deeper if needed), non solo accumulo.

Path di onboarding minimo:
1. (entry-point primario)
2. (snapshot stato)
3. (next-action layer)

Note onboarding:
- 

---

## 6. Operator dynamics

L'equivalente infra del "Player Dynamics First" gameplay. Gli "operator" sono Eduardo + gli agent in-sessione (Claude Code, Codex, Aider, Jules, ecc.). Le scelte di setup tool/workflow devono **aumentare chiarezza** (chi fa cosa quando), **aumentare agency** (operator puo agire senza chiedere), **aumentare interazione significativa** (handoff tra operator non perde contesto).

- [ ] Le scelte di tool/wrapper/agent aumentano chiarezza tra operator (umano <-> agent, agent <-> agent).
- [ ] Le scelte aumentano agency operativa (es. delegare senza ogni volta riconfigurare).
- [ ] Le scelte aumentano interazione significativa cross-fleet (es. session su Lenovo -> handoff a Ryzen senza perdita stato).
- [ ] Non sto premiando complessita tool che non migliora l'esperienza operativa.

Valutazione rapida:
- chiarezza: 
- agency: 
- interazione significativa: 
- complessita utile: 
- complessita tossica (rituali senza valore reale): 

---

## 7. Rational Design

- [ ] Sto valutando i tool/workflow contro il comportamento operativo che producono, non contro il mio gusto estetico (es. "questo wrapper e bello" != "questo wrapper viene usato 5x/settimana e fa risparmiare 20min").
- [ ] Posso descrivere quale comportamento operativo desidero (es. "delega <=1-line task a Aider locale in <30s").
- [ ] Posso descrivere quale comportamento indesiderato il setup attuale produce (es. "ogni nuova sessione perde 15min a ricaricare context").

Comportamento desiderato:
- 

Comportamento attuale indesiderato:
- 

---

## 8. Implicazioni per il repo

- [ ] Le verita fondamentali del repo sono state tradotte in vincoli concreti (path, naming, gitignore, hook, ADR-policy).
- [ ] So quali moduli/script devono restare semplici, testabili, isolati (es. `commit-guard.js` deve essere idempotent + offline).
- [ ] So quali parti del repo sembrano servire piu la storia tecnica che il workflow corrente (template legacy, framework adopt-half).
- [ ] Ho identificato almeno un confine architetturale da stabilizzare per primo (es. boundary cloud-OK vs sovereign-only via privacy whitelist).

Moduli che devono restare semplici/puri:
- 
- 

Parti del repo sospette / storiche / cerimoniali:
- 
- 

Primo confine da stabilizzare:
- 

---

## 9. Decisione finale prima del refactor

- [ ] So se devo fare refactor progressivo, nuovo core parallelo, strangler-pattern o reboot quasi totale.
- [ ] So qual e il primo step a piu alto leverage e rischio controllato.
- [ ] So cosa NON devo toccare ancora (es. governance ADR Accepted, scheduled task in produzione).

Strategia scelta:

Primo step utile:

Cosa NON toccare ancora:
- 
- 

---

## 10. Gate finale

Prima di partire col refactor / hardening / cleanup grosso, devo poter dire di si a queste domande:

- [ ] So cosa deve fare davvero il repo (mission concreta, non slogan).
- [ ] So cosa deve fare davvero il workflow operativo che il repo abilita.
- [ ] So cosa deve fare davvero la triade (mission + scope + constraint dominante).
- [ ] Sto rifattorizzando per migliorare l'esperienza operativa / l'affidabilita / il costo, non solo l'eleganza del codice.
- [ ] Il primo sprint tecnico e gia leggibile e motivato (concretamente: 1 paragrafo che spiega cosa e perche).

Se non riesci a spuntare queste 5 voci, fermati e chiarisci verita / scope / constraint prima di procedere (anti-pattern: refactor-driven-by-tool-discovery).

---

## Confronto con framework adiacenti

| Framework | Cosa offre | Cosa NON offre | Quando preferirlo |
|---|---|---|---|
| **Questa checklist (first-principles)** | Test di cancellazione, triade, gate decisionale, ADR-0005 YAGNI anchor | SLO/error-budget operativo, alert design | Refactor / reboot / "vale la pena tenere?" |
| **Google SRE Workbook** | SLO, error budget, toil reduction, on-call | Test di cancellazione di asset non-runtime (template/agent/skill) | Production runtime con uptime concerns |
| **AWS/Azure Well-Architected** | Pillar-checklist (reliability, security, cost, performance, operational, sustainability) | Eliminazione asset / "questo serve davvero?" | Cloud workload deployed |
| **ATAM (Architecture Trade-off Analysis Method)** | Trade-off rigorous tra quality attributes | Lean checklist editabile in-line | Pre-architecture review formale |
| **ADR (Architecture Decision Records)** | Cattura decisioni con context+consequences | Validate periodically se decisione ancora vale | Decisione architetturale specifica |

I framework off-the-shelf coprono "come operare un sistema in produzione" o "come catturare una decisione". Nessuno copre **"questo asset del repo serve ancora una verita fondamentale?"** (anti-cimitero) che e il valore unico di questa checklist.

---

## Note di mantenimento

- Aggiorna le sezioni 1/4 (verita + triade) ogni volta che fai una decisione architetturale (ADR Accepted) che le ridefinisce.
- Run completo della checklist consigliato: 1x ogni 3 mesi (cadence Sprint) o prima di un refactor grosso. Non e un must-pass continuo.
- Se una sezione resta sistematicamente vuota dopo 2 run = signal che il repo non ha bisogno di quel filtro (es. sez. 6 Operator dynamics e overkill per repo solo-author senza agent multi-CLI). Modifica la checklist locale, non forzare la compilazione.
