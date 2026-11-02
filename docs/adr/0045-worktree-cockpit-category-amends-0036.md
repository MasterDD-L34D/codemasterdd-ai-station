# ADR-0045 -- Cockpit di worktree: categoria propria, emendamento ad ADR-0036 decisione 6

> *TL;DR: ADR-0036 decisione 6 vieta framework multi-agente e gateway LLM, e resta. Un cockpit di worktree (Orca) e' un'altra cosa: crea worktree, lancia una CLI, mostra diff. Lo si ammette solo a quattro regole verificabili, dopo uno spike con criterio di uscita misurabile, nel solo hub. Non compra la parte difficile di Board-LINK 1B, che resta.*

- Status: Proposed
- Data: 2026-11-02
- Ratifica del testo: Eduardo, 2026-11-02 in chat ("ho riletto, e' ok"), con
  l'inserimento di `Master-DD-Taverna` nel perimetro. Lo stato resta Proposed
  finche' lo spike non e' concluso (ADR-0010).
- Decisore: Eduardo Scarpelli (ratifica)
- Autore draft: Claude, sessione cloud, su richiesta di Eduardo
- Amends: ADR-0036 decisione 6; ORCHESTRATION.md sez 8 (solo dopo spike superato)
- Protocolli applicati: refresh-verify (ADR-0026 P1); autoresearch (P2) con fonti
  primarie GitHub e rilettura dell'appendice ricerca di ADR-0036; grilling Pocock
  in due giri; brainstorming a quattro opzioni (P6); harsh-reviewer pre-merge
  (P5), i cui sei P1 sono incorporati qui. Archon (P3) non applicato: la
  decisione e' reversibile per costruzione (regola 1), gated da spike e da
  ratifica; scatta se lo spike propone di estendere oltre hub e Taverna.

## Context and Problem Statement

L'hub `pathfinder-hub` coordina Kimi Work, Claude Code, OpenCode, Codex e Ollama
con `AGENTI_BOARD.md` (blackboard Markdown v2, writer atomico, lease advisory) e
`CODA_LAVORI.md` (coda unica). Il cantiere Board-LINK 1B progetta worktree
dedicati, confinamento provato, lease sull'intero worktree, reconcile.

Eduardo riferisce che "la Board non funziona ancora": e' un registro, non
un'esecuzione. Propone di usare Orca o Vibe Kanban come base, e chiede di
rivalutare l'anti-scope che sembra vietarlo.

**Provenienza delle scelte.** Dal grilling (nota di ricerca, sez 4): Eduardo ha
risposto in prima persona a Q1 (tutti i dolori), Q2, Q3 (umano e agenti) e Q5
(perimetro). Ha delegato a chi scrive Q4, Q6, Q7, Q8 e ha accettato i consigli
da Q9 a Q14. La forma "categoria con regole" e' quindi una proposta dell'autore,
non una richiesta di Eduardo. Dei quattro dolori di Q1 questo ADR affronta la
visibilita' e il parallelismo con tetto; il telefono resta fuori (regola 3); la
coda resta fuori (Q10).

**Cosa dice davvero l'anti-scope.** Due divieti con due prove: framework
multi-agente, perche' il multi-agente "e' un POOR fit per lavoro a contesto
condiviso come la maggior parte del coding" (Anthropic, appendice
`2026-05-29-orchestration-doctrine-design.md` righe 26-28); gateway LLM, per
OD-009. La stessa appendice, righe 196-198, cita Osmani a favore di "worktrees;
WIP 3-5; one-file-one-owner". Quindi: le fonti **non** vietano i worktree, li
raccomandano con un tetto; vietano il coordinamento fra LLM in un runtime.
Orca e Vibe Kanban esistevano gia' quando ADR-0036 fu scritto (Orca dal
2026-03-17): l'ADR non li considera, non perche' non esistessero ma perche'
guardava altro. La prima stesura di questo ADR diceva "non esisteva": falso,
corretto dal harsh-reviewer.

**Cosa compra davvero un cockpit.** Orca sostituisce `git worktree add` e
l'apertura di un terminale con l'agente dentro, e aggiunge una finestra con
diff, terminali e notifiche. **Non** fornisce la parte difficile della 1B:
confinamento provato, canary di scrittura, Job Object, idempotenza, reconcile,
verifica di diff e test. Quella resta nostra in ogni opzione.

**Misure** (nota di ricerca, sez 3, SHA hub `0ef8b48`): 60 commit su 178 negli
ultimi 30 giorni con board, coda o handoff nel messaggio, regex a confine di
parola. E' un contesto, non un criterio: la finestra contiene il picco di
costruzione della Board v2 e i commit "coda" sono imposti dalla regola 2 della
coda stessa.

## Decision Drivers

- Le prove di ADR-0036 riguardano coordinamento fra LLM e gateway, non cockpit.
- Sovereign-first e no-lock-in: uscita a costo noto e dichiarato, non "gratis".
- Coda unica e Board in Git: difese due volte (design v2 opzione C respinta).
- Spec Board-LINK: "senza orchestratore persistente", "gli agenti non fanno
  commit", "parallelismo fuori scope". Un cockpit la tocca in tre punti e va
  emendata esplicitamente, non aggirata.
- Supply chain: app Electron con rilascio quotidiano che apre shell con
  l'ambiente dell'utente.
- Meta-lavoro gia' sopra il tetto del 10%: questo ADR, lo spike e la misura ci
  vanno a carico.

## Considered Options

### Opzione A -- Lasciare l'anti-scope e finire Board-LINK 1B com'e'

**Pro**: nessuna dipendenza; 1B approvata; `git worktree add` dal dispatcher
copre la creazione del worktree; coerenza letterale con 0036 e con la spec.
**Contro**: nessuna visibilita' oltre la Board desktop read-only; nessuna data
di fine per la 1B; i dolori (b) e (d) di Eduardo restano senza risposta.

### Opzione B (chosen) -- Categoria "cockpit di worktree", quattro regole, spike

**Pro**: precisa il divieto senza indebolirlo; compra solo UI, worktree e lancio;
lo stato autoritativo non entra nel cockpit; spike con criterio di uscita prima
di ogni pratica; tetto WIP preso dalla stessa fonte di 0036.
**Contro**: una categoria in piu'; Orca e' Electron, 7.904 issue aperte, "ship
daily"; doc non lette dalla sessione cloud; la spec 1B va emendata in tre
punti; costo di uscita reale (sotto).

### Opzione C -- Revocare la decisione 6

**Pro**: liberta' di adozione.
**Contro**: butta prove ancora valide; riapre OD-009; le eccezioni diventano
regole non scritte.

### Opzione D -- 1B + Agentlocks per i lease (opzione B del design Board v2)

**Pro**: affronta la causa delle collisioni (lease eseguibili, lock
`@git/index`) senza app desktop; MIT; nessuna UI nuova da governare.
**Contro**: CLI pre-1.0 da provare su Windows (survey 2026-10-26); non da'
visibilita'; e' gia' "spike successivo" nel design v2 e non e' alternativa a B
ma complementare. Scansione overlap (OD-007): Agentlocks copre i lease, Orca i
worktree e la UI; `.claude/worktrees/` nativo copre solo Claude Code.

## Decision Outcome

Scelta **Opzione B**, nel perimetro `pathfinder-hub` + `Master-DD-Taverna`, con D lasciata come spike
separato gia' previsto dal design v2. ADR-0036 decisione 6 resta in vigore per
framework multi-agente e gateway LLM.

### Checklist di appartenenza alla categoria

Un'app e' un cockpit di worktree se, e solo se, passa tutti e quattro:

1. il processo dell'app non chiama endpoint LLM (lo fanno solo le CLI figlie);
2. nessun canale di messaggi fra agenti dentro l'app;
3. nessuno store autoritativo dei task: la Board e la coda restano in Git;
4. relay remoto e companion spenti, e verificabili spenti.

Chi fallisce un punto ricade nella decisione 6 di ADR-0036.

### Quattro regole della categoria

1. **Stato in Git.** Presenze, lavori, decisioni e coda restano in
   `AGENTI_BOARD.md` e `CODA_LAVORI.md`. Il cockpit compare solo come
   riferimento in una riga (worktree, branch, agente). Verifica meccanica:
   uno script confronta `git worktree list --porcelain` con il campo `output`
   delle righe Lavori; un worktree senza riga e' una violazione. Esercizio di
   uscita a fine spike: Orca chiuso, tutto il lavoro ricostruito dalla sola Board.
2. **Uso via CLI dentro il protocollo Board.** Il dispatcher (nello spike: la
   sessione coordinatrice Kimi o Claude, a mano, con `board_write.py`) chiede
   il worktree con `orca worktree create ... --json` e registra l'esito col
   writer. Il cockpit non apre, chiude ne' assegna task. Gli agenti non fanno
   commit: il coordinatore verifica e committa, come nella spec 1B.
3. **Privacy per repo e per processo.** Prima di vedere un repo, il cockpit
   passa il controllo 1 dello spike. Versione bloccata, auto-update spento,
   aggiornamento solo dopo lettura del diff di release e ripetizione del
   controllo 1. I terminali del cockpit non ereditano `keys.env` (verifica:
   `Get-ChildItem env:` in un terminale Orca non mostra chiavi). Perimetro di
   questo ADR: `pathfinder-hub` e `Master-DD-Taverna` (repo pubblico,
   sotto-progetto canonico dell'hub in `tooling/`; aggiunto da Eduardo alla
   ratifica). Il controllo 1 si esegue una volta per repo. Le estensioni che Eduardo ha indicato
   (repo cloud-ok, `repo-libri`, `vault` con i soli agenti del suo routing;
   `Synesthesia` mai) richiedono ciascuna un emendamento con controllo 1
   ripetuto: `repo-libri` non e' in whitelist, `vault` e' sovereign-only.
4. **Tetto WIP.** Al massimo 3 worktree agente attivi per volta nel perimetro
   (Osmani: WIP 3-5, scelto il minimo). Il parallelismo oltre e' fuori scope,
   come nella spec 1B.

### Candidato e riserva

Orca (`stablyai/orca`, MIT, Windows) primario. Vibe Kanban riserva, solo se Orca
fallisce la regola 3: e' locale ma orfano.

### Spike (mezza giornata, macchina di Eduardo, a carico del tetto 10%)

| # | Controllo | Esito atteso | Se fallisce |
|---|---|---|---|
| 1 | Rete del solo albero di processi di Orca, figli-agente esclusi (Sysmon evento 3 filtrato sull'immagine di Orca), mobile e remoto spenti, sessione sull'hub; piu' snapshot-diff di `~/.gitconfig`, `~/.claude`, `~/.codex` e hook prima e dopo | zero connessioni fuori da una allowlist dichiarata prima (github.com); diff di configurazione vuoto | spike chiuso, Orca fuori |
| 2 | Gate `1A-CODEX-BWRAP` e smoke bug/clean 1A rilanciati in un terminale Orca | stessi verdi del rapporto versionato `docs/superpowers/reports/2026-10-28-board-link-1a-goal-conclusivo.md` | Orca non e' esecutore ammesso per Codex |
| 3 | `orca worktree create ... --json` -> `output` della riga Lavori via `board_write.py work`; script worktree-vs-Lavori della regola 1 | Board resta SoT, schema invariato, script verde | aggancio sbagliato, non si forza |
| 4 | Rilettura degli incidenti hub del 2026-08-20 e 2026-08-22 | erano collisioni di working tree condiviso | il worktree per task non e' la cura; torna l'opzione D |

Accettazione: un agente prende un id della coda, lavora nel worktree creato da
Orca e consegna un diff; il coordinatore lo verifica e apre la PR; Eduardo non
tocca un file Markdown a mano. Kimi resta coordinatore in Kimi Work, fuori da
Orca: un cambiamento per volta.

### Criterio di uscita (kill criterion), quattro settimane dallo spike

Misura la causa, non la pausa della 1B:

- **uso**: almeno 5 task della coda chiusi con worktree Orca e riga Lavori
  collegata (N chiusi via Orca / N chiusi totali, riportato);
- **collisioni**: zero, con definizione meccanica: un commit con trailer
  `Coding-Agent: X` che tocca un path sotto un lease attivo di una sessione Y
  diversa, lease ricavato dalla storia git di `AGENTI_BOARD.md`. Lo script
  nasce nello spike con un selftest che inietta una collisione finta: senza
  selftest il "zero" non vale;
- **tocchi manuali**: zero modifiche a `AGENTI_BOARD.md` e `CODA_LAVORI.md`
  fuori dal writer, misurate sui commit senza trailer `Coding-Agent`.

Se uno dei tre fallisce, Orca esce e la 1B riprende. La quota di commit
meta-lavoro (hub + pathmaster + Taverna, regex a confine di parola, SHA
fissato) si riporta come contesto, non come criterio.

### Stati

`Proposed` fino a spike concluso. Se passa: `Accepted (early, n=1,
ratification check <data spike + 30gg>)` secondo ADR-0010; solo allora la riga
in ORCHESTRATION.md sez 8 e l'emendamento della spec 1B. Se fallisce: nota di
chiusura sotto Status, `Deprecated`.

### Cosa NON decide questo ADR

- Non sposta `CODA_LAVORI.md` in GitHub Issues: decisione separata, ADR
  proprio, solo se lo spike passa.
- Non sposta Kimi dentro Orca.
- Non tocca Board desktop e widget.
- Non estende il perimetro oltre hub e Taverna.

## Consequences

- **Spec Board-LINK** (`2026-10-27-board-agent-link-design.md`): emendamento
  esplicito, dopo le quattro settimane superate, in tre punti: "senza
  orchestratore persistente" diventa "senza orchestratore che possieda lo
  stato dei task" (Orca e' un'app persistente senza stato autoritativo);
  "parallelismo fuori scope" diventa "parallelismo con tetto WIP 3"; "gli
  agenti non fanno commit" resta. La 1B perde solo la creazione del worktree
  e il lancio del processo; confinamento, canary, idempotenza, reconcile e
  verifica restano.
- **ORCHESTRATION.md sez 8**: una riga "Cockpit di worktree: ammessi alle
  quattro regole di ADR-0045", solo al passaggio ad Accepted.
- **Costo di uscita dichiarato**: restano worktree e branch su disco (da
  rimuovere con `git worktree remove`), la configurazione di Orca, e il tempo
  dello spike. Non resta nessuno stato da migrare: e' questo che la regola 1
  compra, non un'uscita "gratis".
- **Rischio accettato**: churn di Orca; mitigato dalla versione bloccata.
- **Rischio non mitigato**: doc Orca non lette dalla sessione cloud. Il
  controllo 1 e' l'unica difesa; senza di esso lo spike non parte.
- **Precondizione della priorita' 3 della coda**: misurata il 2026-11-02 con
  `gh api search/issues`: Taverna #572 mergiata alle 13:11Z, 0 PR aperte su
  Taverna, pathmaster-dd e hub (oltre a #31). I checkout principali su `main`
  non sono misurabili dal cloud: restano a Eduardo prima dello spike.

## More Information

- Nota di ricerca con grilling, fatti e comandi:
  `docs/research/worktree-cockpit-anti-scope-2026-11-02.md`.
- Rapporto hub, confronto funzione per funzione:
  `pathfinder-hub/sessione-2026-07-16/rapporti/2026-11-02-prova-idea-orca-vibe-kanban-base-board.md`
  (PR hub #31).
- ADR-0036 e appendice `docs/superpowers/specs/2026-05-29-orchestration-doctrine-design.md`.
- Design Board v2: `pathfinder-hub/proposte/2026-10-26-board-agenti-v2-design.md`;
  survey: `sessione-2026-07-16/rapporti/2026-10-26-survey-coordinamento-agenti.md`.
- Spec Board-LINK: `pathfinder-hub/docs/superpowers/specs/2026-10-27-board-agent-link-design.md`.
- Harsh review pre-merge 2026-11-02: 6 P1, 8 P2, 3 P3; tutti i P1 e i P2
  incorporati; verdetto iniziale "da riscrivere", riscritto.
- Repo esterni: https://github.com/stablyai/orca, https://github.com/BloopAI/vibe-kanban.
