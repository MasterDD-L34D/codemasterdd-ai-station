# Cockpit di worktree e anti-scope orchestratori -- grilling e fatti (2026-11-02)

> **Scope**: input per ADR-0045, che emenda ADR-0036 decisione 6. Raccoglie le
> risposte del grilling con Eduardo, i fatti misurati con comando e SHA, le
> decisioni delegate, le correzioni del harsh-reviewer e le affermazioni da
> falsificare nello spike. Non e' una decisione: la decisione sta nell'ADR.
>
> **Status**: grilling completato (due giri, frontiera vuota); harsh review
> eseguita e incorporata; spike NON eseguito.
>
> **Protocolli**: refresh-verify (ADR-0026 P1) su ADR-0036, appendice ricerca
> della dottrina, ORCHESTRATION.md sez 8, CODA_LAVORI.md e AGENTI_BOARD.md
> dell'hub; autoresearch (P2) con fonti primarie GitHub; grilling Pocock (skill
> `grilling`, due giri); brainstorming a quattro opzioni (P6) nell'ADR;
> harsh-reviewer pre-merge (P5) sull'ADR.
>
> **Rapporto gemello nell'hub**: `pathfinder-hub` ->
> `sessione-2026-07-16/rapporti/2026-11-02-prova-idea-orca-vibe-kanban-base-board.md`
> (PR hub #31): confronto funzione per funzione fra Board agenti v2 e i candidati.

## 1. Domanda

Eduardo ha proposto di usare un cockpit esistente (Orca, Vibe Kanban) come base
della Board agentica fra i repo. L'anti-scope di ADR-0036 decisione 6 e
ORCHESTRATION.md sez 8 vieta "heavy orchestration framework". Eduardo non e' sicuro
di quella scelta e ha chiesto di rivalutarla con un grilling e delle ricerche.

## 2. Cosa vieta davvero l'anti-scope, riletto alle fonti

Due divieti distinti, con due prove distinte:

| Divieto | Prova citata | Dove |
|---|---|---|
| Framework multi-agente (LangGraph, CrewAI, AutoGen, claude-flow) | multi-agente "POOR fit for shared-context / interdependent work like most coding" | `docs/superpowers/specs/2026-05-29-orchestration-doctrine-design.md` righe 26-28 (Anthropic) |
| Gateway e proxy LLM (LiteLLM, Bifrost, Langfuse) | overhead di amministrazione per un solo-dev | OD-009 |

La stessa appendice, righe 196-198, cita Osmani: "WIP 3-5; kill stuck-3-iter;
worktrees; one-file-one-owner". Le fonti di ADR-0036 quindi **raccomandano** i
worktree con un tetto WIP e un file per owner, e vietano il coordinamento fra
LLM dentro un runtime. Un cockpit di worktree sta dalla parte raccomandata.

**Correzione dopo harsh review.** La prima stesura di questa nota diceva che
"nessuna fonte riguarda un'app che crea worktree" e l'ADR diceva che la
categoria "non esisteva" nel maggio 2026. Entrambe false: Osmani parla di
worktree e `stablyai/orca` e' nato il 2026-03-17, Vibe Kanban nel giugno 2025.
ADR-0036 non li considera perche' guardava un'altra classe di strumenti, non
perche' mancassero. Il controllo 5 dello spike della prima stesura
("le fonti non coprono i cockpit") e' gia' falsificato ed e' stato tolto.

## 3. Fatti misurati

Rimisurati il 2026-11-02. Hub a `origin/main` = `0ef8b48`; branch di lavoro
`6231c2a`. Comandi accanto, come richiede il criterio F1.

| Fatto | Valore | Comando |
|---|---|---|
| Commit hub negli ultimi 30 giorni | 178 | `git log --since=2026-10-03 --format=%s \| wc -l` |
| Commit con board, coda o handoff nel messaggio, confine di parola | 60 (34%) | `git log --since=2026-10-03 --format=%s \| grep -icE '\b(board\|coda\|handoff)\b'` (stesso valore senza confine) |
| File toccati in area board/coda/handoff vs resto | 280 vs 763 (27%) | `git log --since=2026-10-03 --format=%h --name-only \| awk '/AGENTI_BOARD\|CODA_LAVORI\|board\|HANDOFF\|handoff\|proposte\/2026-10-2\|rapporti\/2026-10-2[67]/{m++;next}{o++}END{print m,o}'` |
| Tetto meta-lavoro deciso da Eduardo (CODA_LAVORI, priorita' 5, 2026-11-02) | ~10% del tempo agenti | lettura |
| PR aperte hub | solo #31 (questo lavoro); #16 e #23 non piu' aperte | `list_pull_requests` (GitHub MCP) |
| PR aperte pathmaster-dd | 0 | idem |
| Taverna: PR aperte e #572 | 0 aperte; #572 mergiata 2026-11-02 13:11Z | `gh api -X GET search/issues -f q='repo:MasterDD-L34D/Master-DD-Taverna is:pr is:open'` |
| Checkout principali su `main` | **non misurabili dal cloud**: restano a Eduardo | -- |
| `stablyai/orca` | MIT, TypeScript/Electron, 113.223 stelle, 7.161 fork, 7.904 issue aperte, push 2026-11-02, nato 2026-03-17 | `gh api -X GET search/repositories -f q='repo:stablyai/orca'` |
| `BloopAI/vibe-kanban` | Apache-2.0, Rust, 28.562 stelle, push 2026-10-29; azienda chiusa 2026-04-10, codice community, solo locale | idem + README |
| `orca-cli/orca` | 4 stelle, 5 commit, fermo da 2026-05-08 | idem |
| `saltbo/agent-kanban` | 495 stelle, licenza non dichiarata | idem |
| Kimi Code CLI | esiste (`MoonshotAI/kimi-code`), installer Windows | ricerca web |
| Whitelist privacy (CLAUDE.md AI Station) | codemasterdd, Game, Game-Godot-v2; `pathfinder-hub` e `repo-libri` assenti; `vault` sovereign-only | lettura |
| `tmp/board-link/` nell'hub | in `.gitignore` riga 46: non e' evidenza versionata; quella versionata e' `docs/superpowers/reports/2026-10-28-board-link-1a-goal-conclusivo.md` | `grep -n tmp .gitignore` |

Avvertenze sulla quota di commit: e' un proxy del tempo, non il tempo; la
finestra contiene il picco di costruzione della Board v2 (26-27 ottobre); i
commit "coda" li impone la regola 2 di `CODA_LAVORI.md`; una regex a
sottostringa conterebbe anche "dashboard". Per questo nell'ADR la quota e'
contesto, non criterio di uscita.

Le 113.223 stelle in sette mesi sono il dato restituito dall'API oggi; da
ricontrollare dalla macchina locale con `gh api repos/stablyai/orca` prima
dello spike.

Due siti non raggiungibili dalla sessione cloud: `onorca.dev` (doc Orca) e
`vibekanban.com`. Restano NON verificati: esistenza di una board kanban in Orca,
dove tiene i dati, cosa esce dalla macchina per companion mobile e runtime remoto.

## 4. Grilling -- risposte di Eduardo e paternita' delle scelte

Primo giro 8 domande, secondo giro 6. Colonna "Chi ha deciso" per non spacciare
un consiglio accettato per una richiesta.

| # | Domanda | Risposta di Eduardo | Esito | Chi ha deciso |
|---|---|---|---|---|
| Q1 | Dolore primario: meta-lavoro, visibilita', parallelismo, telefono | "tutti, visto che la board non funziona ancora" | Criterio di spike in Q9 | Eduardo |
| Q2 | Cosa sostituisce Orca | "penso che (c) possa essere un improve" = anche la coda | Vedi Q10: coda NON migra adesso | Eduardo, poi consiglio accettato |
| Q3 | Chi usa Orca | (c) sia Eduardo sia gli agenti via CLI | Spike: agenti via CLI; Kimi fuori (Q11) | Eduardo |
| Q4 | Dove sta la verita' | "decidi tu" | **Markdown in Git**; Orca solo riferimento in riga | autore |
| Q5 | Perimetro privacy | hub + cloud-ok + repo-libri + vault; Synesthesia fuori | ADR limitato a hub + Taverna (Taverna aggiunta da Eduardo alla ratifica del 2026-11-02); estensioni con emendamento e controllo 1 ripetuto (harsh review P2.13) | Eduardo l'intento e Taverna; autore la gradualita' |
| Q6 | Forma della rivalutazione | "decidi tu" | **Emendamento per categoria**, non revoca | autore |
| Q7 | Budget e precedenza | "decidi tu" | Mezza giornata a carico del 10%; #16, #23 e Taverna #572 chiuse | autore |
| Q8 | Destinazione | "decidi tu" | ADR-0045 + questa nota; spec Board-LINK dopo le 4 settimane | autore |
| Q9 | Cosa vuol dire "la Board funziona" | accettato il consiglio | un agente prende un id coda, lavora in worktree, consegna un diff; il coordinatore verifica e apre la PR; Eduardo non tocca Markdown a mano | autore, accettato |
| Q10 | Coda in GitHub Issues? | accettato il consiglio | **No, non adesso**: decisione separata con ADR proprio dopo lo spike | autore, accettato |
| Q11 | Kimi dentro o fuori Orca | accettato | Fuori nello spike: un cambiamento per volta | autore, accettato |
| Q12 | Condizione su vault | accettato | Entra solo con emendamento, controllo 1 ripetuto, agenti del suo routing | autore, accettato |
| Q13 | Cosa resta di Board-LINK 1B | accettato | Resta tutto tranne creazione worktree e lancio processo; emendamento in tre punti dopo le 4 settimane | autore, accettato |
| Q14 | Criterio di uscita | accettato la prima versione (quota commit 15%) | **sostituito** dopo harsh review P1.2: uso, collisioni meccaniche, tocchi manuali. Ri-ratificato da Eduardo il 2026-11-02 | autore; Eduardo ha riletto |
| -- | Riserva | decisa | Vibe Kanban solo se Orca fallisce la regola 3 | autore |

Dolori di Q1 che l'ADR **non** affronta: il telefono (regola 3 lo esclude), la
coda (Q10). Il parallelismo e' ammesso con tetto WIP 3.

## 5. Harsh review 2026-11-02 -- cosa ha cambiato

Verdetto iniziale: "da riscrivere". Sei P1, otto P2, tre P3. Tutti verificati
alle fonti prima di incorporarli; nessuno scartato.

| Rilievo | Verifica | Effetto nell'ADR |
|---|---|---|
| P1.1 categoria "nuova" e fonti "che non la coprono": false | appendice dottrina righe 26-28 e 196-198 lette | premesse riscritte; controllo 5 tolto; regola 4 WIP |
| P1.2 kill criterion scollegato, aggirabile, passa per costruzione | regex a confine di parola da' lo stesso 60; finestra col picco v2 | criterio sostituito: uso, collisioni meccaniche con selftest, tocchi manuali |
| P1.3 contraddice la spec 1B in tre punti | spec righe 11, 186, 281 lette | emendamento esplicito dichiarato; "agenti non committano" conservato; accettazione riscritta |
| P1.4 controllo privacy indecidibile | ragionamento accettato | rete del solo albero Orca via Sysmon evento 3, allowlist, snapshot-diff config |
| P1.5 supply chain non dichiarata | ragionamento accettato | versione bloccata, auto-update off, terminali senza keys.env |
| P1.6 regole prima della falsificazione | Follow-up vs Consequences contraddittori | stati ADR-0010: Proposed -> Accepted (early, n=1) |
| P2.7 manca l'opzione semplice | `.claude/worktrees/` in CLAUDE.md hub; Agentlocks nel design v2 | opzione D aggiunta con overlap OD-007 |
| P2.8 regole 1 e 2 solo dichiarate | -- | script worktree-vs-Lavori; esercizio di uscita; dispatcher nominato |
| P2.9 uscita "gratis" aspirazionale | -- | costo di uscita dichiarato |
| P2.10 appartenenza non meccanica | ADR-0036 opzione B respinge "dispatch service" | checklist di appartenenza a quattro punti |
| P2.11 meta-lavoro non a budget; PR ferme non tutte misurate | Taverna misurata via search API | dichiarato a carico del 10%; Taverna #572 mergiata, 0 PR aperte |
| P2.12 numeri senza SHA | -- | SHA e comandi completi in sez 3 |
| P2.13 perimetro privacy prematuro | repo-libri non in whitelist; vault sovereign-only | ADR limitato a hub + Taverna (pubblico) |
| P2.14 paternita' non dichiarata | -- | colonna "Chi ha deciso"; paragrafo Provenienza nell'ADR |
| P3.15 Archon non motivato | -- | motivato: reversibile, gated; scatta oltre l'hub |
| P3.16 formato MADR | ADR-0010 sezioni minime lette | TL;DR in corsivo, Decisore, More Information; nota Amended-by in ADR-0036 |
| P3.17 `tmp/board-link` non versionato | `.gitignore` riga 46 | evidenza versionata citata |

## 6. Affermazioni da falsificare nello spike

Da passare come claim da smontare, non come premesse (criterio F3).

1. "Con mobile e remoto spenti, l'albero di processi di Orca, figli esclusi,
   non apre connessioni fuori dalla allowlist e non scrive nelle cartelle di
   configurazione." Misura: Sysmon evento 3 filtrato sull'immagine di Orca;
   snapshot-diff di `~/.gitconfig`, `~/.claude`, `~/.codex`, hook. Allowlist
   scritta prima di accendere Orca.
2. "Il gate `1A-CODEX-BWRAP` da' lo stesso esito dentro un terminale Orca."
   Confronto col rapporto versionato del 2026-10-28.
3. "Da `orca worktree create ... --json` si scrivono worktree, branch e agente
   in `output` della riga Lavori senza toccare lo schema, e lo script
   worktree-vs-Lavori e' verde."
4. "Gli incidenti del 2026-08-20 e 2026-08-22 erano collisioni di working tree
   condiviso." Se no, il worktree per task non e' la cura e torna l'opzione D.
5. "Un terminale Orca non eredita `keys.env`."

Gotcha gia' noti da mettere nel piano: tdd-guard legge `test.json` dal checkout
principale (`-o tdd_guard_project_root=...`); i worktree non hanno `.venv`.

## 7. Cosa questa nota non fa

- Non installa niente e non decide: la decisione e' ADR-0045, da ratificare.
- Non aggiorna `AGENTI_BOARD.md`: la presenza si registra dalla macchina locale.
- Non apre GitHub Issues e non tocca `CODA_LAVORI.md`.
- Non ha letto le doc di Orca: host non raggiungibile.
