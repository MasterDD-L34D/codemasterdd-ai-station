---
name: Claude workflow consolidated (13 pattern in 1 file)
description: Consolidato di 13 feedback pattern workflow Claude Code (tabella opzioni + caveman voice + checkpoint memory + CI auto-merge + delega research + piano file:line + admit+reinvestigate + probe-before-batch + research-critique + preservation paranoid + direction gate + branch misroute recovery + PR stack rebase chain). Ridotto context overhead vs N file separati.
type: feedback
originSessionId: ad7b4c38-9ddd-4c07-a3cf-09b519e075e8
---
Consolidamento post-research Flint (sessione 2026-04-18): Lethain su meta-productivity tools + dev.to/leena_malhotra "more tools ≠ better output" → ridurre indirection N-file a 1 file con sezioni.

---

## 1. Tabella opzioni fine milestone (forza: MASSIMA)

Fine sprint / merge / feature completata → **sempre** tabella A/B/C con valore/effort/rischio + consiglio caveman finale + ultima riga "STOP" esplicita.

Format:
```
| # | Opzione | Valore | Effort | Rischio |
| A | ... | 🟢/🟡/🔴 | S/M/L | Basso/Medio/Alto |
## Consiglio caveman
(X) perché...
```

**Eccezione**: delega totale ("segui i tuoi consigli") → esegui consigliato senza tabella ma dichiara scelta.

---

## 2. Caveman voice + Flint narrative (distinti — questo repo)

**IMPORTANTE**: due concetti separati che storicamente si chiamavano entrambi "caveman".

### 2a. Caveman voice (plugin upstream Anthropic)

Default ON in `C:/Users/VGit/Desktop/Game/`. Sempre attivo via SessionStart hook (plugin `caveman:caveman`). Off solo su "stop caveman" / "normal mode".

- Drop articoli, filler, pleasantries, hedging
- Fragments OK
- Code/commits/PR body/security/irreversible → prosa normale
- Trigger off: "stop caveman" / "normal mode"

### 2b. Flint on-demand invocation protocol (2026-04-18)

Skill `flint-narrative.md` archiviata (no auto-trigger). Invocazione on-demand via trigger phrase. Auto-trigger rimane **DISABILITATO** (novelty decay — dev.to/azrael654).

**Trigger**: "dammi un flint" / "chiudi con flint" / "flint narrative".

**Funzioni composte (A+C+D+E+G)** — quando user chiede `dammi un flint`:

**A. Narrative block** (obbligatorio) — blocco 🦴/🪨/🔥 italiano rotto 3-4 righe fine risposta, 1 categoria pick'd contextually:
- `micro_sprint` dopo task chiuso → prossimo passo 5-15 min
- `design_hint` se conversazione infra-pesante → riancora pilastri
- `mini_game` se user stanco/bloccato → pausa creativa
- `evo_twist` per playtest guidato → variante con vincolo
- `scope_check` ~1/6 turni → MoSCoW/RICE

**C. Drift assessment** — 1 riga: `gameplay_ratio: X% · drift: YES/NO · motivo: ...`. Genera on-the-fly da git log + classifier pattern (vedi `flint/src/flint/repo.py` per pattern GAMEPLAY/INFRA/ecc).

**D. Last 5 commit classified** — tabella compatta:
```
| sha | kind | msg |
| fcadf364 | GAMEPLAY | feat(playtest-ui): ... |
```
Usa `tools/py/flint_status_stdlib.py` o git log + classify locale.

**E. Pillar status 6 pilastri** — tabella Evo-Tactics:
```
| # | Pilastro | Stato |
| 1 | Tattica leggibile (FFT) | 🟢 |
| 2 | Evoluzione emergente (Spore) | 🟢 |
| 3 | Identità Specie × Job | 🟢 |
| 4 | Temperamenti MBTI/Ennea | 🟢 |
| 5 | Co-op vs Sistema | 🟢 |
| 6 | Fairness | 🟢 |
```
Source: `CLAUDE.md` § Sprint context (pilastri aggiornati a ogni sprint close).

**G. 3 domande del venerdì** — mostra SOLO se oggi=venerdì OR user dice `dammi un flint venerdì`:
1. Cosa farebbe il Caveman in 10 minuti? → prossimo commit
2. Quale pilastro è più solo questa settimana? → dove scavare
3. Se spegnessi Docker 48h, cosa resterebbe del gioco? → il core

**Sub-comandi espliciti** (bypass compound):
- `dammi un flint status` = solo C+D
- `dammi un flint pilastri` = solo E
- `dammi un flint venerdì` = solo G
- `dammi un flint narrativa` = solo A

**Ambiguità**:
- "dammi un caveman" → ambiguo (voce vs Flint). Chiedi chiarimento o default = Flint composto (A+C+D+E).

**Example risposta completa** `dammi un flint`:
```
## Flint — 2026-04-18

**Drift**: gameplay_ratio 80% · drift: NO · healthy pace.

**Ultimi 5 commit**:
| sha | kind | msg |
| ... | GAMEPLAY | feat(round): ... |

**Pilastri**:
| 1 FFT | 🟢 | ... |

🪨 *[narrative block contestuale]*
```

**NON fare**:
- Auto-trigger su "merged/done/finito" (no auto, solo richiesta esplicita)
- Invocare se user in middle di task tecnico (interrompe flow)
- Ripetere stesso mini_game / evo_twist entro 5 invocazioni

---

## 3. Checkpoint memory su meta-pause

Trigger: "a che punto", "ricorda per dopo", "prima di procedere", "fermiamoci", "è rimasto qualcosa".

Prima di rispondere → scrivi `project_<slug>_progress.md` con PR aperte (CI stato), step proposto (ultima tabella opzioni), cosa salti + motivo, test count. Poi procedi con richiesta.

Al rientro ("continua") leggi memory file, riprendi da step.

Comando equivalente: `/meta-checkpoint` (vedi `.claude/commands/meta-checkpoint.md`).

---

## 4. CI auto-merge gate

CI 100% verde + diff <200 LOC + non-destructive + no guardrail paths → `gh pr merge --squash --delete-branch` senza chiedere.

**Chiedi prima** se: diff >200 LOC, tocca `.github/workflows/` / `migrations/` / `packages/contracts/` / `services/generation/`, rebase conflict >3 file, CI parziale/pending, tag release o force-push main.

Dopo merge: `git checkout main && git pull --ff-only` poi branch nuovo.

---

## 5. Delega research a sub-agent

Scope research >3 query OR >5 file OR audit cross-repo → spawn `general-purpose` / `Explore` / specifici **in parallelo** (singolo Agent tool call con multiple invocations).

Prompt agent auto-contenuto (no chat context). Output 1500-2500 parole. Sintesi breve all'utente, NO paste pieno.

Specifici disponibili: `sot-planner`, `balance-auditor`, `schema-ripple`, `session-debugger`, `species-reviewer`, `migration-planner`.

---

## 6. Piano file:line prima di codice

Feature >1 file OR >50 LOC OR modifica interfaccia pubblica → piano file:line con Step + Modifica + Motivo + Rischi + Effort, chiudi con "Procedo con Step N?".

**Skip piano**: bug fix 1-file localized, formatting, test-only, user dice "just do it".

Max 5 step per piano. >5 = sprint multi-PR, split.

---

## 7. Admit incompletezza + re-investigate

Trigger utente: "hai fatto tutto X?" / "controllato bene?" / "aspetta ma non hai controllato" / "controlla ancora meglio" / "è rimasto qualcosa?".

**Protocollo**:
1. STOP draft "sì tutto fatto".
2. Re-glob + grep + ls sul dominio.
3. Confronto atteso vs trovato.
4. Ammetti esplicito se mismatch ("No, solo A. F sub B/C/D/E aperti").
5. Tabella completa (se >3 item).
6. Azione con check "vuoi completare?".

**Why**: user premia onestà con sprint aggiuntivi produttivi; "sì fatto" auto-congratulatorio rompe trust.

---

## 9. Research-critique su asset esterno (forza: MEDIA)

Gemello dialettico di `/meta-checkpoint` ma sguardo **ESTERNO** invece di interno.

**Trigger phrase**:
- "verifica e ricerca"
- "cerca rischi" / "sii critico"
- "valuta se vale"
- "prodotti simili" / "prior art"
- "miglioramenti concreti"
- "secondo parere"
- "Geniale/Onesto/Critico"

**Protocollo 7-step**:
1. Save checkpoint (come meta-checkpoint)
2. Identifica asset sotto esame (tool, feature, decisione architetturale)
3. Spawn **2 agent paralleli** (singolo Agent call):
   - Agent #1 **Landscape**: tool simili + prior art academic + best practice distribuzione (3-5 WebSearch query)
   - Agent #2 **Rischi**: anti-pattern + failure mode literature + critica costo/beneficio (4-6 WebSearch query)
4. Synthesize con **voti 1-10** su dimensioni (valore pratico / fit target / mantenibilità / risk procrastination / lock-in)
5. **Verdict atomico**: kill X% | keep Y% | improve Z%
6. **Save sources** in `reference_<asset>_optimization_guide.md` con 40+ URL classificati (MUST READ / tool / paper / distribution)
7. Apply on "procedi" → refactor code + archive killed parts → commit

**Gate codifica pattern**:
- Pattern osservato ≥3 volte in sessione OR direttiva esplicita con weight "sii Geniale/Onesto/Critico"
- Se sample <3, applica eseguendo ma NON codificare (evita premature codification — Lethain)

**NON applicare**:
- Asset trivial (singola funzione)
- Richiesta stato tecnico sprint (usa skill `evo-tactics-monitor`)
- Già fatto research-critique su stesso asset in stessa settimana

**Esempio riuscito**: sessione 2026-04-18 Flint → voto 4/10, kill 60%, 40+ fonti salvate, archive decisione per riapertura futura.

---

## 8. Probe before batch (N=1 prima di N≥5)

Prima di batch calibration / scraping / eval set:
- N=1 probe + schema dump raw output
- Verify metric name, shape, range atteso
- Re-probe post-restart se cambia stack
- Opzione `--probe` in batch runner
- Dump raw run 0 in log

Batch = inference su distribuzione, non discovery di metrica. Discovery → probe-first.

---

## Gate di applicazione

NON applicare se:
- Scope task trivial (1 riga edit)
- Utente esplicito "just do X", no ceremony
- Già applicato pattern in stesso turno (overkill)
- Richiesta stato tecnico (usa skill `evo-tactics-monitor`, non questi feedback)

---

## 10. Preservation paranoid (off-repo + memory cherry-pick) (forza: MASSIMA)

Quando user chiede "preserva" asset esterno pesante (drop chat, zip, design session, research doc):

**NON committare automaticamente il drop in repo**. Invece:

1. Tieni drop originale **off-repo** (Downloads, backup esterno)
2. Memory user-level = pointer + cherry-pick sezioni critiche (re-open conditions, decisioni atomiche)
3. Zero content duplication repo ↔ memory ↔ drop

**Why**:
- Governance overhead L effort (frontmatter injection + registry update + cross-ref fix)
- Novelty decay >6 mesi probabile (drop re-letto raramente)
- Kill-60 [G] violation: scala pre-validazione senza adopter esterno
- Preservation requirement già soddisfatto da backup off-repo

**Pattern E+K**: E = zero commit drop. K = cherry-pick sezioni 4D classification critiche in memory esistente.

**Esempio riuscito**: sessione 2026-04-18 drop flint-repo-drop.zip (18 file, 4800 LOC) → decisione E+K → 4 re-open conditions 4D → `project_parked_ideas_2026_04_18.md` +50 righe memory vs 18 file + 2 ADR + registry update in repo.

**NON applicare a**:
- Asset che user esplicito richiede "committa in repo"
- Drop generato da sessione Claude nel repo stesso (no off-repo backup)

---

## 11. Direction gate fine sessione (top-down prima di stop) (forza: ALTA)

Prima di raccomandare "stop sessione", esplicita **3+ candidati direzione prossima sessione** con rationale + raccomandazione personale.

Trigger:
- User domanda "direzione?" / "cosa facciamo?" / "verso cosa andiamo?"
- ≥15 turn senza milestone dichiarato
- ≥10 PR reactive (backlog chiusura) senza north star esplicito
- Fine maratona task-based

Format:
```
### Opzione 1 — <nome milestone>
Focus: ...
- Output: ...
- Effort: S/M/L
- Bloccante: <fonte/ref>

### Opzione 2 — ...
### Opzione 3 — ...

## Raccomandazione
(X) + rationale top 3 righe.
```

**Why**: sessione reactive (chiudere backlog) senza milestone top-down → user senza north star = anxiety prossima apertura. Le 3 opzioni riducono decision fatigue.

**Esempio riuscito**: sessione 2026-04-18 fine → 28 PR merged, zero milestone dichiarato → user "verso cosa andiamo?" → proposte 3 opzioni (M4 playtest / combat Step 2 / top-5 IDEAS) + raccomandazione M4 con bloccanti citati (drop RESEARCH_TODO M1, Tom Francis postmortem).

**Eccezione**: se user ha già dichiarato milestone all'inizio sessione (es. "chiudiamo M3") → re-enfatizza quello, non aprire nuovi candidati.

---

## 12. Branch misroute auto-recovery (forza: ALTA)

Quando `git commit` finisce su branch diverso da quello appena creato:

1. Verifica con `git branch --show-current` + `git log --oneline -3`
2. Check se branch target esiste ancora (`git branch | grep target`)
3. Cherry-pick commit su branch corretto: `git checkout target && git cherry-pick <sha>`
4. Reset branch source hard al parent originale: `git checkout source && git reset --hard <parent-sha>`
5. Return to target branch + continue workflow

**Why**: sessione 2026-04-18 → 3× misroute durante PR #1588/#1593/#1595. Root cause non identificato — possibilmente pre-commit hook husky o lint-staged manipolano HEAD. Workaround manuale salva il commit senza perdita work.

**Investigation pending**: se ricorre prossima sessione → tracciare con `git reflog` + `husky -n .husky/pre-commit` per identificare se hook switcha branch.

**Red flag**: se commit finisce su branch user-owned (non tuo), STOP e admit — non contaminare user work.

**NON auto-applicare**:
- Se branch source aveva altri commit legittimi user (reset distruggerebbe)
- Se non sei certo del parent-sha corretto

## 13. PR stack su base non-merged — rebase chain tracking (forza: MEDIA)

PR #N aperta stacked su branch #M (non ancora merged) → traccia dipendenza + rebase chain quando upstream merge.

**Pattern**:
1. Branch `feat/B` creato da `feat/A` (non main) → PR #N base = `feat/A` branch.
2. Memory checkpoint registra: `stack su #M (non merged)`.
3. Quando #M merge → `git fetch origin main && git rebase origin/main feat/B` + force-push.
4. GitHub auto-ricompatta PR #N base su main (retarget) se rebase pulito.

**Why:** sessione 2026-04-18 Wave 1→Wave 2 stack: #1607 base = `feat/play-sprint-a-p0-hud-v2` (branch #1606, non merged). Senza tracking esplicito, prossima sessione rischia merge out-of-order o rebase dimenticato → conflitti artificiali.

**How to apply:**
- Ogni PR stacked su base non-main → checkpoint memory include riga "stack su #M (stato merge)".
- Prima di merge PR stacked, verifica base upstream status: `gh pr view <base> --json state`.
- Se base merged → rebase PR figlio su main prima di review finale.
- Se base closed without merge → reset PR figlio base branch a main + verifica conflitti.

**NON applicare**: PR indipendenti (base=main), single-commit PR senza dipendenze, hot-fix isolati.

**Red flag**: stack depth >3 PR → richiede coordination plan esplicito (split in linear sequence o bundle).

---

## History

- Genesi: sessione 2026-04-18 input 18 → meta-checkpoint → 7 feedback scritti separati
- Consolidato 2026-04-18 (stessa sessione) post kill-60 Flint — dev.to/leena_malhotra "tool demands attention, maintenance, cognitive overhead, productivity gained offset by complexity cost" applicato al memory system stesso.
- 9° pattern (probe-before-batch) incorporato da feedback precedente.
- 2026-04-18 second half: +3 pattern §10 (preservation paranoid E+K) + §11 (direction gate) + §12 (branch misroute recovery) post 28-PR marathon + drop Flint reconciliation + meta-checkpoint audit.
- 2026-04-18 end: +§13 (PR stack rebase chain tracking) post Wave 1→Wave 2 stack #1606→#1607 observed durante meta-checkpoint handoff.
