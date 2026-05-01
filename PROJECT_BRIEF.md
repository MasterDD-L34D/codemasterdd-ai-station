# PROJECT_BRIEF

## Identita

- Nome: CodeMasterDD AI Station.
- Tipo: governance repo + workstation AI documentation + infrastructure scaffold.
- Stato: structural recovery dopo transplant su macchina diversa.
- Owner: Eduardo Scarpelli.
- Branch recovery: `codex/structural-reset`.

## Problema attuale

Il repo e' stato trasportato fuori dalla macchina originale. Molti documenti
radice continuavano a descrivere:

- path locali non presenti;
- repo esterni non verificabili;
- runtime services non attivi qui;
- log e DB gitignored non trasportati;
- snapshot HEAD e percentuali di fase divergenti.

Il rischio principale non e' perdita di codice, ma perdita di orientamento:
troppi file si presentavano come "live" mentre erano storici.

## Decisione di recovery

Questo repo torna a governare solo se stesso.

I progetti esterni sono stati riclassificati come dormienti:

- Evo-Tactics / Game
- Synesthesia
- Dafne swarm / evo-swarm
- AA01

La loro storia resta nel repo, ma nessuna azione su di loro e' corrente finche
non passa il gate in `EXTERNAL_REPOS.md`.

## Scope attivo

- Bonifica governance root-level.
- ADR index completo e coerente.
- Roadmap strutturale.
- Backlog solo per task verificabili in questa copia.
- Policy su artefatti runtime mancanti.
- Separazione tra storia e piano.
- Mappa strutturale machine-readable in `config/system-map.yaml`.
- Diagnostica locale con `scripts/recovery-status.ps1` e `scripts/check-all.ps1`.
- Dashboard `/recovery` nello scaffold `apps/dogfood-ui`.

## Fuori scope

- Fix Game.
- Privacy validation Synesthesia.
- Avvio o riparazione Dafne.
- Review AA01.
- Ricostruzione manuale dei log dogfood mancanti.
- Rebuild dello stack solo per far combaciare vecchie dashboard.

## Criteri di successo

La recovery e' riuscita quando:

1. una nuova sessione capisce in meno di 5 minuti cosa e' attivo;
2. nessun file radice rimanda a repo fantasma come se fossero live;
3. ADR e backlog sono coerenti con i file realmente presenti;
4. i runtime artifacts assenti sono dichiarati assenti;
5. il prossimo sprint e' `SPRINT_02.md`, non vecchi dogfood task;
6. Dafne e gli altri repo esterni sono opt-in, non dipendenze implicite.

## Prossimo passo

Verificare e pubblicare il branch `codex/structural-reset`, poi ricollegarlo
dal `main` del PC corretto seguendo `docs/recovery/pre-merge-checklist.md`.
