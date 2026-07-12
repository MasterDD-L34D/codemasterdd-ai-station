# Agentic OS Console -- design spec (2026-07-12)

> Status: MVP IMPLEMENTED (2026-07-13). Scope Option A: 5 azioni tier-0 + 1 tier-1
> (`create-draft-pr` via wrapper reale); `jules-dispatch`/`aider-delegate` -> v2
> (sec 5 + sec 10). Home `/os`, `/api/run-action`, param->argv, test verdi.
> Authority chain: ADR-0044 (Agentic OS = composition) -> AGENTIC_OS.md (the map) ->
> this spec (the "front door" app). ASCII-first (ADR-0021). Local single-user.
> Approccio approvato: estendere `apps/cross-repo-dashboard` (NON nuova app).

## 1. Problem / intent

"Agentic OS" oggi = una MAPPA (AGENTIC_OS.md) + pezzi sparsi (Claude Code, subagent,
skill, hook, memoria, cron). Eduardo vuole "una struttura tipo app per avviarla e
usarla davvero": un unico posto che (a) MOSTRA lo stato dell'OS e (b) LANCIA azioni
fleet con un click. Deciso (AskUserQuestion 2026-07-12): pannello di CONTROLLO con
azioni tool-deterministiche + muta-reversibili; NO spawn di agenti Claude headless.

Vincolo doctrine: il pannello e' un **front-end umano** a tool GIA' gated -- il click
di Eduardo E' l'autorizzazione umana, NON una nuova autonomia (l'autonomia =
agente-agisce-da-solo resta governor-gated, ADR-0036/0037). Irreversibile/outward
(merge-main-doctrine, force-push, comms) restano fuori dal pannello.

## 2. Reuse baseline (cosa esiste GIA', non ricreare)

`apps/cross-repo-dashboard/` (Flask, `127.0.0.1:8081`) ha gia':
- `app.py` -- blueprint, route `/` (index), `/api/state`, `/api/regen-dashboard`,
  `/api/open-dashboard`.
- `dashboards_registry.py` -- catalogo ~15 pannelli (fleet, governor R0, playtest,
  trait-completion, ERMES, HUD canary, Mission Console...).
- **Contratto sicurezza `/api/regen-dashboard`** (da specchiare 1:1): optional
  `API_SECRET` bearer (constant-time `hmac.compare_digest`); unico input client =
  registry `id` (dict lookup, ZERO interpolazione); `steps` = argv-list code-reviewed
  eseguite `shell=False` + timeout + `ok_exit_codes`; `regen` argv NON raggiunge mai il
  template (`e.pop("regen")`).
- Launcher gia' presenti: `start-dashboard.cmd`, `tray.pyw` (system tray),
  `install-shortcut.ps1`, `governor/` + `governor.db`.
- Test: `apps/cross-repo-dashboard/tests/` + `scripts/tests/test_dashboards_registry.py`.

## 3. Architettura (delta minimo)

Nuovi artefatti (specchiano i pattern esistenti):
- **`actions_registry.py`** -- catalogo azioni tiered (schema in sec 4). Specchia
  `dashboards_registry.py`.
- **Route `/os`** (nuova home, diventa il default) -- render `os_console.html`.
- **`/api/run-action`** (POST) -- specchia `/api/regen-dashboard`: bearer auth, input =
  solo action `id`, esegue argv fissi tier-gated, ritorna output tail. Gli argv NON
  raggiungono il template.
- **`templates/os_console.html`** -- home OS.
- Launcher: voce in `.claude/launch.json` + `/os` come route di default; tray/shortcut
  gia' funzionanti puntano alla home.

Nessun nuovo processo, nessun framework, nessun gateway (ADR-0036 sec 8).

## 4. Action registry -- schema

Ogni azione = dict literal (mai costruito da input client):

```python
{
  "id": "fleet-verify",                  # unico; unico input dal client
  "label": "Fleet-verify (audit flotta)",
  "tier": 0,                              # 0 read/report | 1 muta-reversibile | 2 escluso
  "area": "hub",                          # raggruppamento UI
  "desc": "Audit game-family cross-machine (read-mostly).",
  "steps": [ ["powershell","-File","scripts/fleet/...ps1"] ],  # argv-list, shell=False
  "cwd": "<repo-root>",
  "timeout": 600,
  "ok_exit_codes": [0],
  # tier-1 SOLO:
  "wrapper": "draft-pr",                  # OBBLIGATORIO se tier==1: nome del gate
  "wrapper_path": "scripts/fleet/draft-pr.ps1",  # OBBLIGATORIO se tier==1: deve risolvere a un file
  # param opzionale: mappa una CHOICE whitelisted a un flag CLI fisso ->
  # l'endpoint appende [flag, value] allo step lato server (value solo da choices):
  "params": [ {"name":"repo","flag":"--repo","choices":["MasterDD-L34D/Game",...]} ],
}
```

Regole di integrita' (enforced dai test, sec 7):
- `tier in {0,1,2}`; `id` unico.
- tier 0/1 -> `steps` presente e non-vuoto; tier 2 -> NESSUN `steps` eseguibile.
- tier 1 -> `wrapper` presente E `wrapper_path` che RISOLVE a un file reale nel repo
  (un'etichetta senza script dietro = comando nudo mascherato da gated; il test lo blocca).
  Inoltre tier-1 richiede `API_SECRET` settato sul server (muta -> auth obbligatoria).
- ogni elemento di ogni `steps` argv e' una stringa literal; nessun placeholder viene
  interpolato dall'`id` o da input client. I `params` mappano una scelta da whitelist a un
  `flag` CLI fisso (dropdown, non testo); l'endpoint appende `[flag, value]` con value SOLO
  da `choices`. Un'azione con `params` ha esattamente UNO step (append target univoco).

## 5. Azioni MVP

**Tier-0 (read/report, un click):**
- `fleet-verify` -- audit flotta.
- `morning-brief` -- rigenera il brief R0.
- `fleet-pr-status` -- `gh pr list` sui repo monitorati (read).
- `bench-report` -- report bench da risultati esistenti.
- `governance-lint` -- lint governance (gia' regenerable nel dashboards_registry).

**Tier-1 (muta-reversibile, click = autorizzazione, via wrapper) -- 1 azione nell'MVP:**
- `create-draft-pr` -- apre un draft-PR per il branch `claude/*` corrente via il
  wrapper REALE fail-closed `scripts/fleet/draft-pr.ps1` (aborta se non su un
  branch `claude/*` o se non pushato; `gh pr create --draft` con `--head` pinnato
  al branch risolto -- nessun input client raggiunge l'argv). Reversibile (draft).
- `jules-dispatch` + `aider-delegate` -- **NON nell'MVP** (v2): richiedono un flusso
  d'input (repo + task-file per Jules; file-target + tier per Aider) che il pannello
  non ha ancora. Riammessi solo quando il flusso e il wrapper file-backed esistono.
  Vedi sec 10 (out-of-scope).

**Tier-2 (esclusi dal pannello):** merge-main/doctrine, force-push, comms esterne. Non
hanno bottone. Se mai richiesti in futuro: conferma digitata + classifier backstop, via
una spec dedicata + earn-path.

## 6. Data flow

**Home load (`GET /os`):**
1. parse tabella 7-layer da `AGENTIC_OS.md` (repo root) -> righe layer + link authority.
2. leggi ultimo `logs/morning-brief/<oggi>.md` (se assente: nota "non ancora generato").
3. `gh pr list` cross-repo (cached ~60s, degrade-non-fatal come morning-brief).
4. stato scheduled-task (`morning-brief`, `jules-daily-digest`).
5. render azioni da `actions_registry` (senza argv nel template).

**Run action (`POST /api/run-action {id}`):**
1. bearer auth se `API_SECRET` set.
2. lookup `id` in ACTIONS (ignoto -> 400).
3. tier 2 -> 403 (non eseguibile dal pannello).
4. tier 1 -> verifica `wrapper` presente; costruisci argv da `steps` + `params`
   (posizioni fisse, valori solo da whitelist).
5. `subprocess.run(argv, shell=False, timeout, cwd)`; ritorna tail stdout/stderr +
   `ok` per `ok_exit_codes`.

## 7. Error handling

- Auth fallita -> 401. Id ignoto -> 400. Tier-2 -> 403. Param fuori whitelist -> 400
  (mai passato ad argv). Timeout -> 500 + tail parziale. rc non in `ok_exit_codes` ->
  500 + tail. gh/tool non disponibile -> degrade nel payload (non crash), come
  morning-brief.
- La UI mostra sempre l'output tail; nessun errore silenzioso (ADR-0020).

## 8. Testing (specchia test_dashboards_registry.py)

- **schema integrity**: id unici; tier valido; tier-1 ha wrapper; tier-2 senza steps
  eseguibili.
- **no-injection (load-bearing)**: ogni argv e' lista di stringhe literal; nessun `id`/
  param interpolato in una stringa comando; i `params` mappano solo a scelte whitelist.
  Negative control: un id con caratteri shell (`; rm -rf`) -> 400 lookup-miss, MAI
  eseguito (L-041 must-block case).
- **tier enforcement**: POST tier-2 id -> 403; POST tier-1 senza wrapper nel registry ->
  fallisce il test di schema.
- **route smoke**: Flask test client su `/os` (200) e `/api/run-action` (id noto tier-0
  mockato -> 200; id ignoto -> 400).
- **param whitelist**: param fuori lista -> 400, non raggiunge subprocess (negative
  control).

Test in `apps/cross-repo-dashboard/tests/` + estensione `scripts/tests/`.

## 9. Launcher

- `.claude/launch.json` con una config `agentic-os-console` (runtimeExecutable = il
  comando che `start-dashboard.cmd` usa; port 8081).
- `/os` diventa la route di default (o l'index linka la home OS in cima).
- `tray.pyw` + `install-shortcut.ps1` gia' aprono il browser sul dashboard -> puntano a
  `/os`. "Aprire l'app" = 1 click sull'icona tray/shortcut.

## 10. MVP scope / out-of-scope

**In (MVP):** home `/os` (7 layer + brief + azioni), tier-0 completo (5 azioni,
`fleet-pr-status` con param `repo` funzionante), 1 azione tier-1 (`create-draft-pr`
via wrapper reale branch-guarded), launcher wiring, test (incl. happy-path exec +
tier-1-auth negative control).

**Out (later, spec propria / v2):**
- `jules-dispatch` (serve flusso input repo + task-file, wrapper scoped) e
  `aider-delegate` (serve file-target + tier, wrapper privacy-guarded file-backed):
  spostati a v2 -- l'MVP non ha il flusso d'input e non wireremo un placeholder morto.
- tier-2 qualsiasi; spawn agenti Claude headless (`claude -p`); azioni
  autonome/schedulate dal pannello (= act-layer governor-gated); auth multi-utente /
  esposizione non-locale; storicizzazione run in governor.db.

## 11. Decisioni (risolte -- Eduardo 2026-07-12, spec approvata)

- Q1 RESOLVED: home `/os` = route DEFAULT; `/` (fleet-dash attuale) resta raggiungibile
  (link in cima alla home OS).
- Q2 RESOLVED: `create-draft-pr` -- titolo da whitelist di prefissi conventional-commit
  (feat/fix/chore/docs/refactor/test) + campo desc controllato; NO free-text nel comando.
- Q3 RESOLVED: `aider-delegate` -- dropdown file solo da repo privacy-whitelisted
  (codemasterdd / Game / Game-Godot-v2); repo sovereign-only esclusi.
