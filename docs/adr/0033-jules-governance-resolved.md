# ADR-0033 -- Jules governance: own-repo active / external read-only-with-ground-truth / throttle primary

> *TL;DR: Supersede ADR-0032. Risoluzione dopo Archon 7-step (verdetto interno c' 75%) + arbitro esterno indipendente harsh-reviewer (verdetto b-with-teeth 82%, ground-truth-verified, ha falsificato c'). Decisione: **(1)** leva PRIMARIA = throttle Jules org-level (Eduardo, jules.google) -- previene il 41% rumore alla fonte a costo ~0; **(2)** repo ESTERNI (Game/Godot-v2/Game-Database): SOLO triage read-only, con la dottrina ground-truth S1-S7 + no-silent-close incorporata nella VERDICT-LOGIC del triager (non come azioni attive Claude); ZERO corrective sendMessage / sovereign-fix Claude su Jules-session esterne; merge/close = Eduardo-explicit; **(3)** Model-3 ATTIVO pieno (corrective sendMessage + sovereign-fix) SOLO su repo proprio codemasterdd. La tassonomia S1-S7, i 3-obblighi (E/R1/R2), no-silent-close, lesson L-031 sopravvivono qui. Status Accepted (la decisione e' essa stessa l'esito del metodo, non pending un altro ciclo).*

- **Status**: **Accepted** (2026-05-17)
- **Data**: 2026-05-17
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)
- **Supersedes**: ADR-0032 (mai ratificato; esecuzione ne ha dimostrato l'insicurezza su repo esterni)

## Context

ADR-0032 ("Model-3 attivo": Claude triage + corrective sendMessage a sessioni Jules + sovereign-fix + batch per Eduardo) e' stato costruito e applicato a `MasterDD-L34D/Game` (esterno) in sessione 2026-05-16/17. L'esecuzione ha prodotto evidenza falsificante. Metodo di risoluzione (Protocol 3 + Protocol 5, "metodi vincenti reiterati"):

- **Archon v2 7-step** (interno): verdetto (c') split-per-failure-mode, confidence 75%.
- **Arbitro esterno harsh-reviewer** (indipendente, adversarial, ground-truth-verified): verdetto **(b)-with-teeth**, confidence **82%**, ha smontato (c'):
  - mis-attribuzione F4: merge Jules attribuibili a Model-3-active = **0** (#2307=duplicate-resolution, #2297/#2287 non via active).
  - #2325 = self-inflicted-cleanup (typo nostro), non throughput Jules.
  - dottrina ground-truth **disaccoppiabile** dalla write-authority -> incorporabile in triager read-only, stesso valore, zero superficie destabilizzante.
  - gate "no-incident" gia' fallito (backfire #2294/#2313 = incidente del ciclo).

Per CALIBRATE Archon (esperimento falsificante pre-committato: "se l'arbitro converge su (b) repo-split, (c') e' sospetto") + disciplina di sessione (arbitro esterno > giudizio interno; conclusioni Claude ~biased, dimostrato 5x questa sessione) -> adottato il verdetto esterno.

### Fatti ground-truthed (ledger)

| Fatto | Valore |
|-------|--------|
| Triage CLOSE falso-positivo | 69% (9/13) |
| Self-revision verdetto stesso item | 3-4x |
| Corrective sendMessage inviati | ~15 |
| Backfire (esplosione 1->14/19 file, innescata DAL corrective) | 2 (#2294/#2313) |
| Merge Jules CODE attribuibili a Model-3-active | **0** |
| Rumore Jules (no-op + artifact) | 41% del volume |
| Blocker sistemico (registry placeholder 1-riga) | gating intera coda, 0 relazione con qualita' Jules |
| Throttle org-level: costo / effetto | ~0 / previene il 41% alla fonte |

## Decision

**(1) Leva PRIMARIA -- throttle Jules org-level (Eduardo, jules.google + GitHub-App)**. Cap concurrency/rate su `MasterDD-L34D/Game`. Riduce il VOLUME (la variabile causale del problema), non il danno. ~0 costo. Rende ~70% della macchina ADR-0032 non necessaria. ADR-0033 e' esplicitamente subordinato: ogni processing-machinery e' giustificata solo sul residuo post-throttle.

**(2) Repo ESTERNI monitorati (Game, Game-Godot-v2, Game-Database)**: SOLO triage read-only.
- La dottrina ground-truth (tassonomia **S1-S7**, **no-silent-close**, mandatory `GET /v1alpha/sessions/<id>/activities` + check `gitPatch` pre-verdetto CLOSE) e' incorporata nella **verdict-logic del `jules-pr-triager`** -> produce una *tabella verdetti migliore per Eduardo*.
- **VIETATO** su sessioni Jules di repo esterni: corrective sendMessage Claude, sovereign-fix Claude, commenti PR Claude. (Il canale corrective e' il destabilizzatore provato -- F: backfire innescato DAL corrective.)
- merge/close = **Eduardo-explicit** (invariato). Claude prepara set + comandi; Eduardo esegue (o relaunch Jules pulito per S2/S3).

**(3) Repo PROPRIO `codemasterdd-ai-station`**: Model-3 attivo pieno consentito (corrective + sovereign-fix), dove ha funzionato (cluster 15/16) con full-context e basso S2. Questo NON e' survivorship-bias-license: e' il solo dominio dove l'evidenza e' positiva.

### Cosa sopravvive da ADR-0032 / studio (il vero yield)

Tassonomia S1-S7, 3-obblighi (E)splicazione/(R1)eazione/(R2)esponse, no-silent-close, lesson **L-2026-05-031** (session-state > PR proiezione lossy). Migrano nella verdict-logic del triager (esterni) e nel Model-3 attivo (codemasterdd).

## Consequences

**Positive**: elimina il vettore backfire su repo esterni; mantiene il valore (ground-truth doctrine) senza la superficie d'azione; throttle attacca la causa-radice; un solo modello coerente cross-sessione.

**Negative / accettati**: su repo esterni Eduardo riprende l'azione manuale (merge/close/relaunch) -- ma il triager ground-truthed gli da' una tabella decisionale di qualita' superiore al Model-B originale; nessuna autonomia-write Claude esterna (by design, e' il punto).

**Reconciliation immediata** (questo ADR):
- `.claude/agents/jules-pr-triager.md` -> hardened: S1-S7 + no-silent-close nella verdict-logic; rimosso il framing "sessione opera Model-3" per repo ESTERNI (Model-3 attivo = solo codemasterdd).
- memory `feedback_external_repo_action_boundary` -> emendamento ADR-0032 (active su Jules-PR esterni) **revocato**; esterni = triage read-only + ground-truth; Model-3 attivo = solo repo proprio.
- Loop corrective attivo su Game: **STOP** (nessun nuovo sendMessage a sessioni Jules Game). B2 (merge batch B esplicitamente autorizzato + CI-gated) completa come azione one-time gia' autorizzata; nessun nuovo ciclo attivo Game.

**Azione #1 per Eduardo**: settare il throttle Jules a jules.google OGGI (org-level, fuori scope Claude). E' la leva di massima leva, costo ~0.

## Riferimenti

- ADR-0032 (superseded), `docs/research/jules-operating-model-study-2026-05-17.md`
- Archon v2 7-step (Protocol 3) + harsh-reviewer arbitro esterno (Protocol 5) -- metodo di risoluzione
- L-2026-05-031, L-025/L-029/L-030, ADR-0026 (cognitive protocols)
