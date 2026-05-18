# ADR-0034 — Jules autonomous-managed model (owner mandate, supersede ADR-0033)

> *TL;DR: Eduardo (master-dd, sole decider) ha dato mandato durevole esplicito
> 2026-05-18: Claude gestisce L'INTERO processo Jules in autonomia su TUTTI i
> repo (own + esterni) — triage + risposta (write/correzione/invio) + gestione
> sezione "suggestions" per-repo (apply-full / modify-slightly / reject + iter)
> + orchestrazione del cap **15 sessioni attive concorrenti sfruttato al
> massimo**. Eduardo interviene SOLO su orchestratore finale + contenuti
> finali. Questo SUPERSEDE ADR-0033 (2) "esterni read-only / Eduardo-explicit".
> Status: **Proposed** — go-live GATED su (a) falsificazione esterna
> harsh-reviewer sopravvissuta (SDMG/Protocol-7, obbligatoria dato che il
> precedente self-designed Jules-active ADR-0032 si e' AUTO-DISTRUTTO) +
> (b) Eduardo permission-rule che sblocca il classifier auto-mode.*

- **Status**: **Option A REJECTED-redux 2026-05-18 da arbitro esterno harsh-reviewer (conf 84%); Option D adottata-come-raccomandazione, pending Eduardo accept + permission-rule.** SDMG/Protocol-7 pre-commit ("se rigetta adotto non difendo") onorato — Option A NON difesa.
- **Data**: 2026-05-18
- **Decisore**: Eduardo Scarpelli (mandato durevole esplicito)
- **Supersedes**: ADR-0033 decision (2) (esterni read-only / zero sendMessage / Eduardo-explicit). ADR-0033 (1) throttle + (3) own-repo-active RESTANO validi e incorporati.

## Context

ADR-0033 (Accepted 2026-05-17) limitava Jules su repo esterni a triage
read-only, zero corrective sendMessage, close/merge Eduardo-explicit —
nato da evidenza di danno: ADR-0032 self-designed-active si AUTO-DISTRUSSE
(ledger: 69% CLOSE falso-positivo, 2 backfire #2294/#2313 = corrective
message → esplosione scope 1→14/19 file, 0 merge utili attribuibili).

2026-05-18 Eduardo ha dato **mandato owner durevole esplicito** (3x
ribadito): vuole l'INTERO controllo Jules autonomo lato Claude; il suo
intervento e' SOLO orchestratore finale + contenuti finali. Il mandato
cambia *chi decide* (owner override legittimo) — NON elimina il fatto che
il metodo ha tasso d'errore alto dimostrato. Per SDMG/Protocol-7:
autonomizzare un metodo self-designed high-error richiede falsificazione
esterna pre-go-live, "se l'arbitro rigetta adotto non difendo".

Evidenza fresca a supporto del valore (audit CLI 8/8 2026-05-18):
7/8 sessioni Game "Awaiting" = rework su codice gia'-shippato → il loop
autonomo + throttle taglierebbe rumore reale; ground-truth-gate funziona
(8/8 verificate vs 5+inferenza del browser-scrape).

## External falsification outcome (2026-05-18, harsh-reviewer SDMG arbiter)

**Verdetto: REJECT-redux, confidence 84%.** Pre-commit SDMG onorato: Option A
NON difesa, rigetto adottato.

Findings P0 (ground-truthed, validi):
- **R3 = il messaggio A5 fallito ri-emesso**: lo scope-explosion #2294/#2313
  era comportamento generativo di Jules, NON funzione della precisione del
  nostro prompt. Un template "scoped" non puo' impedire a un agent terzo
  incontrollabile di esplodere lo scope. R3 wishful.
- **R1 valida solo la meta' sicura**: ground-truth-gate provato su
  *detection statica* (8/8), NON sul *corrective generativo* (il vettore
  reale del 69%-FP + backfire). Claim "gia' validato empiricamente"
  fuorviante → ritirato.
- **R4 = il gate no-incident gia' fallito, ricalibrato**: scatta dopo 2
  backfire = blast-radius storico INTERO (il totale storico era esattamente
  2). Non previene, registra a danno avvenuto.
- **R2-as-decider = l'euristico 69%-FP che SDMG vieta** (decider deve essere
  ground-truth/specialista, MAI euristico self-designed).
- Anti-accretion: ADR-0032→0033→0034 = l'accretion che L-2026-05-033
  proibiva; base-defect (azione generativa autonoma esterna vs agent
  incontrollabile) non risolto, ri-avvolto in 7 promesse. 0 upside esterno
  mai dimostrato (ADR-0033: 0 merge utili da active-mode).

→ **Option A = ADR-0032-redux. RIGETTATA.** (Sezione "Decision (proposed)"
sotto = storica, NON adottata.)

## Decision (ADOTTATA: Option D — draft-batch, execute-only-non-generative)

Soddisfa l'intento owner (Eduardo operativamente fuori dal loop) SENZA
autonomia di corrective-send su agent non-falsificabile:

1. **Claude full-auto triage + ground-truth** (R1 read-path, provato 8/8)
   su own + esterni. R7 audit-trail. R5 throttle-primario (ADR-0033(1)).
2. **Auto-esegue SOLO non-generativo verificabile-safe**: archive-gia-
   shippato (ground-truth-confermato), flag, log. Zero mutazione live-agent.
3. **Generativo/corrective** (respond/correct/send a sessioni Jules vive +
   suggestions apply/modify) → Claude **drafta l'INTERO batch come 1
   artefatto** con ground-truth-evidenza + scope-lock per-item.
4. **Eduardo: unica interazione loop = 1 batch approve/reject** (NON triage
   per-sessione, NON per-item). Operativamente fuori dal loop = intento
   mandato soddisfatto. Lui resta decider non-euristico sul path generativo
   (dove SDMG lo richiede), a costo ~1 approve/ciclo ≪ rischio auto-distruz.
5. **own-repo codemasterdd**: active-mode pieno preservato (ADR-0033(3),
   unico dominio con evidenza positiva).
6. **15-cap**: ceiling per il triage read-path, NON target da imbottire
   (R5; risolve la contraddizione P1 exploit-max vs anti-noise — il
   batch-approve di Eduardo e' il vero throttle del path generativo).

### Falsifying experiment pre-go-live (proposto dall'arbitro)
Dry-run: Claude drafta ogni corrective su prossimo cluster Game "open"
SENZA inviare (artefatto). Eduardo+ground-truth post-hoc: % che (a)
targetta sessione davvero-open-sana + (b) scoped tale che reviewer onesto
predice no-scope-explosion. **Se <90% entrambi → Option D stessa va
ri-tarata prima di go-live.** Costo ~0, dirimente.

## Decision (proposed) [STORICA — Option A, REJECTED-redux, NON adottata]

**Claude gestisce il ciclo Jules completo in autonomia**, sotto rail hard
anti-backfire NON negoziabili. Scope = own (codemasterdd) + esterni
(Game/Godot-v2/Game-Database).

### Scope autonomo
1. **Triage** ogni sessione (list+pull via CLI; metodo runbook
   `jules-session-triage-via-cli.md`).
2. **Rispondere** alle azioni Jules: write + correzione + invio risposta.
3. **Suggestions per-repo**: monitorare la sezione, decidere apply-in-toto /
   modify-slightly / reject, iterare il processo.
4. **Orchestrazione cap**: max **15 sessioni attive concorrenti**, sfruttato
   al massimo (ceiling da riempire con lavoro ad-alto-ROI, NON da imbottire
   di rumore — vedi rail R5).
5. Eduardo residuo: SOLO orchestratore finale + contenuti finali.

### Rail HARD anti-backfire (violazione = STOP)

- **R1 Ground-truth-gate**: PRIMA di ogni azione su una sessione, `gh api`
  verify del diff/premessa vs `origin/main`. Nessuna azione su non-verificato.
  Premessa falsa → archive + flag, mai "continue".
- **R2 Verdict-logic**: gia'-shippato→archive · genuinamente-open+sano→
  risposta scoped · sensitive-path/freeze-attivo→risposta-deferral · ambiguo
  →STOP escalate Eduardo. (tassonomia S1-S7 ADR-0033 incorporata.)
- **R3 Response-template scoped**: ogni risposta a Jules DEVE includere:
  scope-lock esplicito (solo X), behavior-preserving, ZERO altri file, no
  API/contract change, follow existing pattern, "se ambiguita'/ripple
  cross-file → STOP request review, NON espandere scope". (contro #2294/#2313.)
- **R4 No-corrective-loop / kill-switch**: se post-risposta una sessione
  esplode scope (file-count jump) → STOP, NON inviare ulteriore corrective
  (e' il vettore backfire), archive + flag Eduardo. **2 backfire in finestra
  → auto-revert ad ADR-0033 read-only + escalate**.
- **R5 Anti-noise cap**: il 15-cap e' ceiling, riempito SOLO con sessioni
  ad-ROI-verificato (ground-truth pre-spawn). MAI spawnare per riempire (il
  41%-rumore ADR-0033 e' il fallimento causale). Throttle org-level
  (ADR-0033 (1)) resta leva primaria complementare.
- **R6 Suggestions-gate**: ogni suggestion applicata = ground-truth-gated +
  scoped come R3. modify-slightly documentato (diff intent). reject con motivo.
- **R7 Audit-trail**: ogni azione autonoma loggata (sessione-id, verdetto,
  ground-truth-evidenza, azione, esito) — `logs/jules-autonomous-YYYY-MM.md`.

## Go-live gate (NON attivo finche':)

1. **harsh-reviewer** falsifica questo ADR (SDMG external arbiter,
   obbligatorio dato auto-distruzione ADR-0032). "Se rigetta → adotto, non
   difendo." Verdetto + confidence pre-committato.
2. **Eduardo permission-rule** che autorizza il classifier auto-mode a
   permettere Jules external-write *policy-authorized* (non agent-inferred).
   Senza, il harness ri-blocca (denial 2026-05-18 documentato).
3. Post-(1)+(2): Status → Accepted, loop autonomo attivo.

## Options considered

- **A (proposed)**: full-autonomous con rail hard + falsificazione pre-go-live.
- **B**: own-repo-active only (ADR-0033 status quo) — rifiutato da owner mandate.
- **C**: full-autonomous SENZA falsificazione (improvvisare ora) — rifiutato:
  e' esattamente ADR-0032 redux (self-designed high-error non falsificato →
  auto-distruzione). Il harness lo blocca giustamente.

## Consequences

- (+) Eduardo libero da loop Jules (suo intento), focus su orchestratore/contenuti.
- (+) Rail R1-R7 + falsificazione = autonomia affidabile, non ADR-0032-redux.
- (+) ground-truth-gate gia' validato empiricamente (8/8 2026-05-18).
- (-) Superficie azione esterna ampia → R4 kill-switch obbligatorio.
- (-) Go-live non immediato (gate falsificazione + permission-rule) — costo
  accettato per non ripetere l'auto-distruzione.

## Decision needed (master-dd, post harsh-reviewer)

1. Accetti i rail R1-R7 come vincolanti (non negoziabili in autonomia)?
2. Aggiungi la permission-rule che sblocca external-write policy-authorized?
3. harsh-reviewer verdict integrato (P0 fix obbligatori prima di Accepted).

Rif: ADR-0033 (ledger + S1-S7 + throttle), runbook
`jules-session-triage-via-cli.md`, DECISIONS_LOG Decisione 010,
audit 8/8 2026-05-18 (STATUS_MULTI_REPO).
