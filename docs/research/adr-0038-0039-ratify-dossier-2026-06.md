# Dossier di ratifica -- ADR-0038 (doctrine carve-out completion) + ADR-0039 (R1 open-PR reconcile rung)

Data: 2026-06-11. Autore: hub (Claude Code, `claude-fable-5`). Decisore: Eduardo (la
decisione di flip Proposed->Accepted NON e' presa qui -- questo e' il dossier istruttorio,
task in-sprint ratificato da Eduardo 2026-06-11).

Metodo (protocolli ADR-0026): (1) evidence check ground-truth al 2026-06-11 su ogni
claim/premessa (git log, gh pr/api, filesystem, test run); (2) falsificazione esterna SDMG
Protocol 7 via subagent `harsh-reviewer` (run 2026-06-11, fresh, sul testo merged su main);
(3) probe empirica eseguita sul finding P1 (output incluso). Entrambe le ADR toccano
`docs/adr/**` = doctrine = il PR di questo dossier NON viene self-merged dal hub.

---

## Raccomandazioni (executive)

| ADR | Raccomandazione | Sintesi |
|-----|-----------------|---------|
| 0038 | **ACCEPT con 4 amendment** (2 applicabili al merge, 1 testuale proposto, 1 follow-up same-PR) | Il core "tightens, grants nothing" regge clause-by-clause. Amendment: header stale (FIXED in questo PR), re-founding del rationale GOALS.md/G1-G4 (proposto, sostanza), nota prospettica `~/.claude/agents/**` (proposto), sync actor-criteria sec 7 (follow-up obbligatorio alla ratifica). |
| 0039 | **ACCEPT con amendment P1 sul claim clock-free** + 3 annotazioni R2 | Il safety-claim che conta (no-merge, 3-lock) regge sotto attacco + test reali. MA il claim "clock-free" e' FALSIFICATO per la gamba codemasterdd (probe empirica confermata): la severity eng-graph e' time-derived a monte del render. Amendment necessario prima che i cycle del STATUS leg contino per R2. Header stale FIXED in questo PR. |

Nessuna delle due e' REJECT o STAY-PROPOSED: 0038 e' sana-con-pulizia; 0039 spedisce codice
sicuro (apre PR, mai merge -- verificato) ma porta un invariante falsificabile (clock-free)
provatamente rotto per una delle due gambe. E' un amendment, non una rejection, perche' la
proprieta' di sicurezza vera (no merge) regge: il leak tocca la QUALITA' DELL'EVIDENZA R2,
non la safety.

---

## ADR-0038 -- Doctrine carve-out completion

### Evidence check (claim -> ground-truth 2026-06-11 -> verdetto)

| Claim/premessa | Ground-truth 2026-06-11 | Verdetto |
|---|---|---|
| ADR-0037 Accepted (base da emendare); dec.2 = enumerazione chiusa 6-item | `docs/adr/0037` Status Accepted 2026-06-03, dec.2 elenca esattamente i 6 item | REGGE |
| I file nominati nel carve-out esistono | 6 root rule-files presenti; `docs/governance/**` (8 file incl. `EXECUTION-BOARD.md` + `actor-activation-criteria.md`); `.claude/agents/harsh-reviewer.md`; `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/SAFE_CHANGES_ONLY.md`; `~/.config/aider-privacy-whitelist.txt`; tutti i NON-doctrine operational nominati | REGGE |
| Subpath globali `~/.claude/` | 7/8 esistono; `~/.claude/agents/` NON esiste su disco (glob prospettico, fail-closed innocuo per un classifier path-based) | REGGE con nota (P2-2 review) |
| Falsificazione SDMG fatta | Sezione Falsification documenta run 2026-06-03, verdict SURVIVE-WITH-CHANGES, adottato pre-PR; PR #286 merged 2026-06-03 | REGGE -- ma l'header diceva ancora "Pending (a) SDMG falsification": STALE, fixato in questo PR |
| Il carve-out e' gia' load-bearing de-facto | `governor/reconcile.py:is_doctrine()` implementa il set statico ADR-0038 ed e' in produzione dal merge di #295 (ADR-0039 la usa come authority); docstring rescoped P1.1 verificato nel codice | REGGE -- argomento PRO ratifica: il codice shipped la consuma gia' |
| DECISIONS_LOG riga 0038 | Presente (riga 48, via PR #303) | REGGE |
| "GOALS.md = the autonomy doctrine itself (G1/G4)" | G1/G4 vivono in `docs/superpowers/jules/2026-06-03-jules-autonomy-gaps.md`; root `GOALS.md` e' un direction file (D-row); il D2 row conferma 0036/0037 | NON REGGE come formulato (vedi P2-3) -- la conclusione (GOALS.md = doctrine) resta difendibile su altra base |

### Harsh-review (SDMG, 2026-06-11) -- findings

- **P2-1 (header-vs-body)**: header "Pending: (a) SDMG falsification" ma il body la
  documenta DONE 2026-06-03. Attivamente falso; resta pending solo il ratify+merge di
  Eduardo. -> **FIXED in questo PR** (fix fattuale, il body lo documentava gia').
- **P2-2 (claim-vs-disk)**: `~/.claude/agents/**` citato come glob coperto e l'esempio
  bandiera (charter del falsificatore) vi si appoggia, ma il path globale non esiste su
  disco (il vivo e' il repo-level `.claude/agents/`). Mai dichiarato prospettico. ->
  amendment testuale proposto (sotto).
- **P2-3 (autorita' mal-attribuita -- il finding sostanziale)**: il rationale P0.2
  ("GOALS.md G1/G4 ARE the merge-autonomy doctrine") poggia su un'identita' file/contenuto
  falsa; e contemporaneamente la Falsification (riga 103) classifica NON-doctrine proprio
  il file jules che G1/G4 li contiene davvero ("goals = inputs"). L'ADR sostiene A e
  non-A su dove vive la dottrina. La conclusione (root `GOALS.md` = doctrine) resta
  giusta su base diversa: e' un root rule/direction-file sotto cui il hub opera (test del
  Principle). -> amendment di re-founding proposto (sostanza: decisione Eduardo).
- **P3-1 (chiarezza)**: il CATCH-ALL content-based e' presentato in lista accanto ai glob
  eseguibili senza il caveat "human-enforced, non classifier-enforced" che ADR-0039 dec.2
  esplicita. Un lettore di 0038 da sola puo' credere che il classifier valuti il contenuto.
  -> annotazione proposta.

### Contraddizioni vs autorita' Accepted

- vs ADR-0037 dec.2: NESSUNA -- relazione di amendment pulita e dichiarata.
- vs `actor-activation-criteria.md` sec 7: **drift vivo al momento della ratifica** -- sec 7
  enumera ancora la VECCHIA lista 6-item di 0037 (righe ~150-153). Alla ratifica di 0038 i
  due file di governance divergono su cosa e' "doctrine". -> follow-up OBBLIGATORIO:
  aggiornare sec 7 nello stesso PR di ratifica (actor-criteria e' essa stessa doctrine =
  Eduardo-merge, quindi puo' viaggiare nello stesso merge di ratifica).

### Rischio non dichiarato (per il verbale, non blocca)

Il CATCH-ALL e' inapplicabile dall'unico consumer automatico esistente (il rung 0039 non
puo' valutare contenuti): il buco "file di governance a path imprevisto" e' chiuso SOLO dal
checkpoint umano per-reconciler. Un FUTURO write-path autonomo diverso dal rung non eredita
ne' il guard `__post_init__` ne' il checkpoint -> riaprirebbe il buco. Amendment proposto:
una riga in 0038 che obbliga ogni nuovo write-path autonomo a re-implementare entrambi.

### Amendment proposti (testo, decisione Eduardo)

1. **(P2-3, sostanza)** In TL;DR e Context P0.2: sostituire l'attribuzione "GOALS.md (the
   autonomy doctrine itself, G1/G4)" con "GOALS.md (root direction/rule file the hub
   operates under; the G1/G4 autonomy goals live in docs/superpowers/jules/
   2026-06-03-jules-autonomy-gaps.md, deliberately NON-doctrine as inputs)". Nessun file
   cambia classificazione: si corregge solo il PERCHE'.
2. **(P2-2)** Nella lista subpath globali: aggiungere "(`~/.claude/agents/**` is
   prospective -- not on disk today; the live agents dir is the repo-level
   `.claude/agents/**`, e.g. harsh-reviewer.md)".
3. **(P3-1)** Al CATCH-ALL: aggiungere "(human-review-enforced; no path-classifier can
   evaluate content -- see ADR-0039 dec.2)".
4. **(rischio)** Aggiungere al Principle: "any NEW autonomous write-path (beyond the 0039
   rung) must re-implement both the construction-time doctrine gate and the human
   classification checkpoint".
5. **(follow-up same-PR di ratifica)** Sync `actor-activation-criteria.md` sec 7 alla
   lista 0038 (glob + named + catch-all pointer).

---

## ADR-0039 -- R1 open-PR reconcile rung

### Evidence check (claim -> ground-truth 2026-06-11 -> verdetto)

| Claim/premessa | Ground-truth 2026-06-11 | Verdetto |
|---|---|---|
| Rung BUILT, spec v4 #292 + plan esistono | `docs/superpowers/specs/2026-06-03-governor-r1-open-pr-rung-design.md` + plan presenti; codice merged via PR #295 (2026-06-03) | REGGE |
| Codice + test dedicati | `governor/reconcile.py`, `reconcile_cycles_report.py`, 6 test file dedicati; run mirato 2026-06-11: **40 passed** (no_merge + doctrine + cycles_report + actor) | REGGE (verde oggi) |
| Negative test sul builder REALE (dec.4a, P1.3) | `test_governor_reconcile_no_merge.py` guida il REALE `_real_open_or_update_pr` (create + reuse path, transport registrato, no network), asserisce nessuna route `/merge` + pin `real_gh_api().keys() == {get_file, open_or_update_pr}` | REGGE |
| Branch protection UNAVAILABLE (dec.4) | RE-VERIFICATO 2026-06-11: `gh api .../branches/main/protection` -> HTTP 403 "Upgrade to Pro" | REGGE |
| settings.json ceiling invariato (dec.4c/6) | Nessuna allow-rule di merge; ceiling `git push origin claude/*` | REGGE |
| Token fail-closed (dec.6) | `GOVERNOR_RECONCILE_TOKEN` mintato da Eduardo 2026-06-03 (JOURNAL: PAT fine-grained contents+PR write, codemasterdd+vault only); write actor senza token = no-op fail-closed (test); env-only (P2.1 adottato) | REGGE |
| Doctrine gate (dec.2) | `is_doctrine` fail-closed a costruzione + re-check runtime; docstring rescoped a "write-refusal superset" (P1.1) verificata nel codice | REGGE |
| Anti-self-licking (dec.7) | `reconcile_cycles_report.py` = libreria pura ADVISORY (marker `advisory: True`), nessun entrypoint CLI, l'actor non la importa (pin CI) | REGGE |
| Vault leg clock-free (dec.5) | `parse_vault_report` senza `now`, hash su contenuto -- confermato anche dalla review | REGGE |
| `tools/playtest2-board-sync.sh` (References) | Esiste | REGGE |
| actor-criteria activation note (References) | Update 2026-06-03 presente in coda a actor-criteria | REGGE |
| 3a falsificazione SDMG sul BUILT code | Body la documenta DONE 2026-06-03 (SURVIVE-WITH-CHANGES, no P0) -- header diceva ancora "Pending (a)": STALE, fixato in questo PR | REGGE (header fix) |
| **Claim "clock-free ... NEVER because the calendar advanced" (dec.1/TL;DR)** | **FALSIFICATO per la gamba codemasterdd** -- vedi P1-1 sotto, probe empirica | **NON REGGE per 1 di 2 gambe** |

### Stato R1 de-facto (e' operativo?)

SI -- attivato e usato una volta, con esito pulito:

- 2026-06-03: token mintato (Eduardo); **primo run reale** apre esattamente 2 reconcile
  PR: codemasterdd **#296** (region GOVERNOR-SYNC in `STATUS_MULTI_REPO.md`) + vault
  **#252** (`Atlas/lint-status.md`, file nuovo). Trailer ADR-0011 corretti, solo i file
  target (JOURNAL 2026-06-03).
- Entrambi MERGED 2026-06-03 19:34/19:35 dall'account MasterDD-L34D. Attribuzione umana
  corroborata (non provata macchinalmente): vault e' Eduardo-only-merge per regola
  standing, il JOURNAL assegnava "rivedere+mergiare" a Eduardo, merge a 1 minuto di
  distanza nella stessa sessione. NB review: non esiste segnale nativo git/gh che
  distingua "Eduardo alla tastiera" da "sessione hub con auth ambient dello stesso
  account" -- vedi annotazione R2 (c).
- **Finestre 7-day chiuse 2026-06-10 pulite**: nessun revert; nessun same-line follow-up
  (PR #318 del 06-10 ha toccato `STATUS_MULTI_REPO.md` ma FUORI dalla region; il file
  vault non ha commit successivi al merge). -> **clean-R1-PR-cycles = 2 (1+1 su 2 repo)**
  al 2026-06-11. Gate R2: >=4 su >=2 repo su >=2 settimane -> 2/4 cycle, 2/2 repo,
  ~1.2/2 settimane.
- Caveat sull'evidenza banked: entrambi i cycle sono **bootstrap-class** (il primo run ha
  CREATO la region/il file). La review distingue: create-PR != steady-state-drift-PR come
  classe di evidenza (vedi annotazione R2 (d)).
- Dal 2026-06-03 nessun re-run (nessun log, nessun nuovo PR): il silenzio attuale =
  **no-run, non no-drift** (cadenza manuale `python -m governor.reconcile`, no cron per
  anti-scope dec.8). Per far maturare l'earn servono run manuali periodici -- oppure il
  non-run prolungato va letto onestamente come segnale off-ramp "classe non necessaria".

### P1-1 -- clock-leak nella gamba codemasterdd (finding headline, CONFERMATO)

**Claim attaccato**: dec.1 clausola 2 + TL;DR -- "no wall-clock ... the signal STATE
changes only when the report CONTENT changes, NEVER because the calendar advanced".

**Meccanismo**: il claim vale per il RENDER (nessun param `now` -- vero) e per la gamba
vault (parser clock-free -- vero). Ma il render della gamba STATUS riproduce
`store.latest_per_source()` per TUTTE le sorgenti, inclusa `vault-eng-graph`, la cui
severity e' time-derived A MONTE: `ingest.py:158` (`now = now or date.today()`) ->
`ingest.py:137` -> `parse_eng_graph_moc(now=now)` -> `parsers.py:163-175` (info ->
warning oltre `STALE_WARN_DAYS`, -> error oltre `STALE_ERROR_DAYS`), severity inclusa nel
`payload_hash` -> riga DISTINTA nello store -> region diversa -> drift -> PR.

**Probe empirica (2026-06-11, store sqlite temporaneo, contenuto sorgente
byte-identico, cambia solo `now`)**:

```
now=2026-06-10 severity=info hash=06ebbb2bd685
now=2026-07-20 severity=warning hash=5c8ee1a438b9
payload_hash differs: True
rendered region differs: True
REGION ROW A: | vault-eng-graph | info | eng-graph MOC: 2 repos indexed, last_verified 2026-06-01 | ...
REGION ROW B: | vault-eng-graph | warning | eng-graph MOC: 2 repos indexed, last_verified 2026-06-01 | ...
VERDICT: P1-1 CONFIRMED (calendar-only diff)
```

**Impatto**: (a) l'invariante headline e' falso per 1 gamba su 2 -- la gamba STATUS puo'
aprire un PR il cui unico diff e' una cella severity flippata dal calendario, la STESSA
classe del band di staleness eng-graph KILLED che 0039 cita come cio' che ha evitato;
(b) e' anche un buco di gameability: i clean-cycle del STATUS leg possono essere
"calendar-manufactured" aspettando le soglie -- l'esternalita' dec.7 separa il verdetto
del classifier dalla promozione, ma NON separa il drift calendar-driven dal conteggio.
(c) NON e' un buco di SAFETY: il no-merge 3-lock regge; tocca la qualita' dell'evidenza.

**Fix direction (decisione Eduardo, amendment)**: (a) il reconciler STATUS renderizza
solo campi clock-free (esclude la severity per le sorgenti staleness-class), oppure
(b) si emenda dec.1 clausola 2 da "il RENDER non usa wall-clock" a "lo STATO renderizzato
e' funzione pura di contenuto non time-derived" e si prova eng-graph fuori -- col costo
onesto che la gamba STATUS puo' restare vuota finche' non drifta un segnale clock-free.
**Fino alla risoluzione: i PR-cycle della gamba codemasterdd non dovrebbero contare verso
R2** (i 2 cycle gia' banked restano validi come bootstrap-class: il diff di #296 era la
creazione della region, non un flip di staleness).

### Altri findings review

- **P2-1 (header-vs-body)**: come 0038 -- header "Pending (a) 3rd SDMG falsification" ma
  body la documenta DONE. -> **FIXED in questo PR**.
- **P2-2 (produced_at renderizzato)**: per sorgenti con `produced_at` derivato da "max di
  N" (sot-drift, jules-digest) il timestamp renderizzato si muove all'arrivo di item nuovi
  anche a severity stabile -- churn benigno (il contenuto E' cambiato davvero) ma APRE un
  PR. -> 1 riga proposta in Consequences: "produced_at-only diffs will open PRs".
- **P3-1 (splice marker-integrity)**: idempotenza garantita finche' i marker sopravvivono;
  se un umano cancella marker+anchor il fallback appende un SECONDO blocco. Precondizione
  da annotare o skip+warn. Rischio basso (marker committati).
- **P3-2 (human-merge-only non-enforced)**: dec.3 e' un invariante di prosa, non un gate
  runtime -- una sessione umana con gh auth proprio non e' vincolata da settings.json.
  Accettabile nell'earn window PERCHE' il conteggio e' esterno e post-hoc; da pesare
  nell'ADR R2 (gia' richiesto da dec.4). Nessun fix richiesto a 0039.

### Contraddizioni vs autorita' Accepted

- vs ADR-0036 (auto-merge rung Deferred): NESSUNA -- 0039 resta a R1, R2 deferito (dec.8).
- vs actor-criteria sec 6 (clean cycle): coerente; ma vedi annotazione (c) sotto su
  `merged_by_human`.
- INTERNA: dec.1 "clock-free" vs catena eng-graph = P1-1 (sopra).

### Annotazioni per il futuro ADR R2 (da verbalizzare ratificando 0039)

a. "Human-merge-only" e' disciplina operatore + audit git post-hoc, non enforcement by
   construction (niente branch protection: 403 re-verificato 2026-06-11).
b. Il campo `merged_by_human` di `reconcile_cycles_report.is_clean_cycle` e' popolato
   dall'ESTERNO: nessun segnale nativo distingue il merge di Eduardo da un merge della
   stessa-account-auth. Il conteggio R2 vale quanto chi lo popola.
c. P1-1: finche' il clock-leak non e' chiuso, i cycle della gamba STATUS sono
   calendar-manufacturable -> non contarli (i 2 banked sono bootstrap-class, non
   staleness-flip).
d. Create-if-absent PR (bootstrap) e steady-state-drift PR sono classi di evidenza
   diverse: R2 ha bisogno della seconda. Suggerito amendment a dec.7/dec.8: "create-PRs
   and steady-state drift PRs are different evidence classes; R2 needs the latter".

---

## Fix fattuali applicati in questo PR (refusi/stale-ref -- nessun cambio di sostanza)

1. `docs/adr/0038-...md` header: "Pending (a) SDMG falsification" -> falsification done
   2026-06-03 (il body la documentava gia'); pending = solo Eduardo ratify+merge.
2. `docs/adr/0039-...md` header: idem per la 3a falsificazione sul BUILT code.

Tutto il resto (re-founding GOALS.md, nota prospettica, catch-all caveat, fix direction
P1-1, sync actor-criteria sec 7, annotazioni R2) = **amendment proposti**: cambi di
sostanza, decisione di Eduardo.

Convenzione suggerita (cross-cutting, dalla review): quando una falsificazione completa,
aggiornare la riga "Pending" dell'header NELLO STESSO commit del body -- uccide l'intera
classe di drift header-vs-body (n=2 in questa serie).

## Cosa resta a Eduardo

1. Decidere i 2 flip Proposed->Accepted (con o senza gli amendment proposti) e fare il
   merge dei rispettivi cambi (doctrine = Eduardo-only).
2. Se ratifica 0038: includere il sync di actor-criteria sec 7 nello stesso PR.
3. Se ratifica 0039: decidere la fix-direction P1-1 (a o b) e se verbalizzare le
   annotazioni R2 (a-d) nell'ADR o nel file actor-criteria.
4. Decidere la cadenza dei run manuali del rung (o accettare il silenzio come off-ramp).

## Riferimenti

- ADR-0036 (spine Accepted), ADR-0037 (Accepted), ADR-0038/0039 (Proposed, oggetto).
- PR: #286 (0038), #292 (spec v4), #295 (0039+code), #296/#252 (primi reconcile PR),
  #303 (DECISIONS_LOG rows), #318 (refresh 06-10, fuori region).
- `docs/governance/actor-activation-criteria.md` (sec 6 clean cycle + activation note
  2026-06-03; sec 7 DA SINCRONIZZARE alla ratifica di 0038).
- Harsh-review SDMG 2026-06-11 (subagent run, findings integrati sopra); probe P1-1
  eseguita 2026-06-11 (script temporaneo, store sqlite temp, rimosso dopo l'esecuzione).
- JOURNAL.md 2026-06-03 (attivazione rung + token) / 2026-06-10 (PR #318).
