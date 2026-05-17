# Studio: modello operativo Claude <-> Jules (ricostruzione empirica)

**Data**: 2026-05-17
**Tipo**: research / doctrine (alimenta ADR-0032)
**Origine**: direttiva Eduardo -- "raramente Jules lavora inutilmente; spesso sbaglia ma produce SEMPRE qualcosa a cui devi saper dare spiegazione, reagire e rispondere. Serve uno studio approfondito."
**Metodo**: P2 autoresearch (evidenza empirica sessione 2026-05-16/17) + P4 AA01 audit trail + sintesi strategica (non delegabile)

## 0. Tesi centrale

Il fallimento ricorrente NON e' di Jules ("non ha lavorato") ma **mio**: giudico
Jules al **layer sbagliato**. Leggo la *PR di superficie* (commit/diff) e ne
deduco "vuoto / sprecato / da chiudere". Ma la PR e' una **proiezione lossy**
della sessione Jules. La verita' di terra e' la **sessione** (state +
`agentMessaged` + `gitPatch` artifacts), non la PR.

Corollario operativo (regola d'oro): **mai concludere "wasted / empty / close"
dalla sola PR.** Prima ground-truth della sessione Jules. Estende L-025
(API-ground-truth) specificamente al caso Jules: *session > PR*.

Evidenza che ha forzato la tesi (caso gitpatch, 2026-05-17): triage subagent
+ mia sintesi -> "8 PR vuote, lavoro sprecato, CLOSE". Ground-truth sessioni
-> **4/8 avevano lavoro reale intrappolato** (`gitPatch` in-sessione, PR a
diff-zero per sandbox-stale). Chiuderle = distruggere fix reali. La mia
conclusione era falsa-negativa al 50%.

## 1. Tassonomia degli stati di output Jules (osservati empiricamente)

| # | Stato | Sintomo PR | Realta' sessione | Reazione corretta |
|---|-------|-----------|------------------|-------------------|
| S1 | PR-faithful | diff pulito, CI verde | lavoro = PR | triage -> MERGE-OK set (Eduardo-explicit) |
| S2 | Scope-creep | diff + dep-bump/artifact | lavoro reale offuscato | sendMessage "ri-sottometti pulito" -- NON close (#2305/2294 dep; #2320/2313/2292/2291/2288 artifact) |
| S3 | Sandbox-stale / push-lost | diff VUOTO, ma "COMPLETED, success" | `gitPatch` reale in-sessione, mai arrivato al branch | ground-truth artifacts; sendMessage re-push; o estrai patch + sovereign-apply (#125; #2321/2317/2314/2310) |
| S4 | Genuinely empty | diff vuoto | 0 patch anche in-sessione | CLOSE-safe (raro, vero spreco) (#2319/2315/2309/2303) |
| S5 | Premise-false | "remove unused X" | X e' in uso (dict-value/template) | sendMessage con grep evidence -> Jules scope-adjusta (L-030) |
| S6 | Behavior-under-cosmetic | titolo "code health" | cambia logica/balance/API | leggi diff reale, audit specialist; NON il titolo |
| S7 | Duplicate/triplicate | N PR stesso fn | varianti dello stesso lavoro | pick cleanest, close rest (Eduardo-explicit) |

Distribuzione misurata (Game, 32 PR, 2026-05-17): S1 ~0%, S2 ~22%, S3+S4
~41% (di cui meta' S3 salvabile, meta' S4 vero spreco), S5/S6/S7 il resto.
**Implicazione**: "Jules lavora a vuoto" e' vero solo per S4 (~12%). Il
resto e' lavoro reale in uno stato che io devo *interpretare*, non scartare.

## 2. Perche' le mie conclusioni sbagliano (bias sistematico)

1. **Surface-reading bias**: `gh pr diff` vuoto -> "niente". Falso per S3
   (lavoro in `gitPatch` di sessione). Fix: per ogni PR Jules "vuota o
   sospetta", interrogare SEMPRE `GET /v1alpha/sessions/<id>/activities`
   e cercare `artifacts[].changeSet.gitPatch.unidiffPatch`.
2. **Trust-the-claim bias**: Jules dice "I successfully modified..." ->
   assumo fatto. Falso per S3 (claim COMPLETED + PR vuota). Fix: il claim
   Jules e' un'ipotesi, non un fatto -- ground-truth PR vs claim (L-029).
3. **Triage-as-verdict bias**: il subagent triage e' read-only e legge
   superficie; il suo "CLOSE" e' un'ipotesi di lavoro, non una decisione.
   Caso 2312/2307: triage "pick one" -> game-balance-auditor "entrambi in
   sequenza" (specialist > triage shallow). Fix: triage filtra, lo
   specialist/ground-truth decide.
4. **Title bias** (S6): gia' codificato in jules-pr-triager, ma vale anche
   per me: il titolo cosmetico non e' la natura del diff.

## 3. Dottrina di reazione: i 3 obblighi per OGNI PR Jules

Eduardo: "...a cui devi saper dare **spiegazione, reagire e rispondere**."
Formalizzato come tre obblighi non saltabili:

- **(E) Explanation**: classificare lo stato (S1..S7) con evidenza
  ground-truth (session state + artifacts + diff reale). Mai "vuoto" senza
  aver letto la sessione.
- **(R1) Reaction**: l'azione Model-3 corretta per quello stato (tabella
  S1..S7). Default per S2/S3/S5 = sendMessage correttivo, NON close.
- **(R2) Response a Jules**: chiudere il loop -- comunicare a Jules il
  ground-truth (es. "tua PR e' vuota nonostante 'completed', re-push").
  **Errore cardinale: il close silenzioso.** Chiudere senza spiegare a
  Jules ne' verificare la sessione e' il singolo anti-pattern peggiore
  (distrugge lavoro S3 + non da' feedback correttivo -> Jules ripete).

## 4. Pattern sandbox-stale (S3) -- approfondimento

Pattern dominante e piu' insidioso (n>=5 osservati: #125 codemasterdd +
2321/2317/2314/2310 Game). Meccanica: il sandbox Jules non riesce a
`git pull` origin/main aggiornato -> opera su base stale -> il commit
risulta no-op contro la base sbagliata, oppure il push non materializza il
diff sul branch remoto. Jules dichiara COMPLETED in buona fede (nel suo
sandbox il lavoro c'e'). Sintomo esterno: PR diff vuoto + sessione con
`gitPatch` reale + claim success.

Detection deterministica: `state==COMPLETED` AND `gh pr diff` vuoto AND
`sum(len(gitPatch.unidiffPatch))>0` nelle activities -> S3 confermato.

Remediation (in ordine di preferenza):
1. sendMessage re-push (Jules re-sync + push) -- piu' economico, validato.
2. Se Jules non recupera in 1 ciclo: estrarre il `gitPatch` dalle
   activities e applicarlo sovereign su branch (Model-3 fix tier).
3. Solo se 0 patch in-sessione (degrada a S4): CLOSE-safe.

## 5. Modello operativo corretto (sintesi)

```
PR Jules -> [E] ground-truth sessione (state+activities+gitPatch) + diff reale
         -> classifica S1..S7
         -> [R1] azione per-stato:
              S1 -> MERGE-OK set (Eduardo-explicit)
              S2 -> sendMessage "resubmit clean"
              S3 -> sendMessage re-push | sovereign-extract-patch
              S4 -> CLOSE-set (Eduardo-explicit) -- UNICO close legittimo
              S5 -> sendMessage + grep evidence (L-030)
              S6 -> specialist audit (game-balance-auditor/harsh-reviewer)
              S7 -> pick cleanest, close-rest set (Eduardo-explicit)
         -> [R2] response a Jules (loop chiuso, mai close silenzioso)
         -> merge/close = SEMPRE Eduardo-explicit per-batch (ADR-0032)
```

Invariante: il gate merge/close resta Eduardo-only. Cambia il *resto*:
non sono un gatekeeper-che-scarta, sono un interprete-che-reagisce.

## 6. Proposte di emendamento ADR-0032

1. **A1 -- Ground-truth obbligatorio pre-verdetto**: nessun verdetto
   CLOSE/empty su PR Jules senza interrogazione `GET sessions/<id>/
   activities` (anti-bias S3). Aggiungere allo step "Ground-truth verify".
2. **A2 -- Tassonomia S1..S7** come riferimento canonico nel workflow
   Model-3 (sostituisce la dicotomia implicita "buono/spreco").
3. **A3 -- Errore cardinale "close silenzioso"**: esplicitare che ogni
   close e' preceduto da response-a-Jules + ground-truth sessione.
4. **A4 -- jules-pr-triager**: aggiungere allo step 3 dell'agent il check
   `gitPatch in-session` per le PR a diff-zero (oggi le marcherebbe CLOSE
   -- falso-negativo S3 dimostrato).

## 7. Lezione AA01 (da promuovere)

`L-2026-05-031`: *Jules session-state e' ground-truth, la PR e' proiezione
lossy. Tassonomia 7-stati. Errore cardinale = close silenzioso. n>=5
sandbox-stale (S3) recuperati via re-push/sovereign-extract.* Famiglia
L-025/L-029/L-030.

## 8. Limiti / aperti

- Distribuzione S1..S7 misurata su 1 batch (Game 32 PR) -- ricalibrare a
  n>=2 batch.
- Throttle Jules (jules.google + GitHub-App) resta leva Eduardo org-level,
  fuori scope: lo studio riduce il *danno* del volume, non il volume.
- S3 root-cause (sandbox sync Jules-side) non e' fixabile lato nostro --
  solo rilevabile + remediabile post-hoc.
