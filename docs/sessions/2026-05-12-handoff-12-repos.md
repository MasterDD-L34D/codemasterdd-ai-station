# HANDOFF — Sessione 2026-05-12 sera (cloud sandbox -> PC fisico)

> **NON un to-do passivo**. Vedi sezione "Step 0 -- Metodologia obbligatoria pickup" prima di toccare qualsiasi file.
> Trigger origin: screenshot OCR `TOP CLAUDE CODE REPOSITORIES` (12 repo) inviato da Eduardo.
> Output principali: `docs/reference/subagents-skills-candidates.md` esteso, `docs/aa01-handoff/` (4 scaffold), BACKLOG M11-M14, PR #57 draft.

---

## Step 0 -- Metodologia obbligatoria pickup (NO acceptance cieca)

Sessione futura (Claude Code sul PC fisico Lenovo Windows o nuova sessione cloud) **NON deve** trattare questo handoff come istruzione da eseguire passo-passo. Deve applicare i 4 cognitive workflow protocols (CLAUDE.md sezione "Cognitive workflow protocols", ADR-0026):

### Protocol 1 -- Refresh-verify state interno (OBBLIGATORIO PRIMA di toccare file)

```bash
cd C:\dev\codemasterdd-ai-station
git fetch origin && git status              # verify branch + sync
git log --oneline origin/main..HEAD         # cosa c'e' di nuovo dal mio side
gh pr view 57                               # stato PR (merged? open? new comments?)

# Verifica file citati nel handoff esistano effettivamente
ls docs/reference/subagents-skills-candidates.md
ls docs/aa01-handoff/
cat BACKLOG.md | grep -A2 "M11\|M12\|M13\|M14"

# Verifica state AA01 (dovresti farlo TU Eduardo se sub-agent NON puo' accedere)
cd C:\Users\edusc\aa01
bash scripts/status.sh                      # AA01 workspace state
ls inbox/                                   # gia' paste-d scaffold? quanti?
ls active/                                  # task gia' promoted?
```

**Anti-pattern critico**: ereditare narrative da questo handoff senza re-verify. Caso studio: lesson L-2026-05-002 (mio errore 2026-05-11 ADR-0025 amend, accetto narrative COMPACT senza verify).

**Trigger reverify aggiuntivo**: se PR #57 ha review comments / CI fails / merge conflict -> stop, leggi context completo prima di action.

### Protocol 2 -- Autoresearch multi-source (per re-validate decisioni preliminari)

Le **decisioni preliminari** in `subagents-skills-candidates.md` (INSTALL/BOOKMARK/SKIP/AUDIT-ONLY/DORMANT) sono **TENTATIVE**, non binding. Per ogni task M11-M14 prima di SHIP:

1. Re-verify stars repo live (`gh api repos/<owner>/<repo> --jq .stargazers_count`) -- OCR drift gia' osservato 9x su `obra/superpowers`
2. Re-verify last commit < 90gg (manutenuto?)
3. Re-verify license (Apache/MIT/BSD acceptable)
4. Re-leggi README repo per use case attuale (potrebbe essere cambiato da quando handoff fu scritto)
5. Cross-check vs nostri 18 sub-agent + skills installati (`ls ~/.claude/skills/` + `ls .claude/agents/`)

**Weighting**: internal > external, empirical > documentation, recent > old.

**Anti-pattern**: one-shot "il handoff dice INSTALL #4 claude-mem -> proceed" senza autoresearch. Decisione era tentative basata su README scan veloce.

### Protocol 3 -- Archon 7-step (high-stakes / irreversibile)

**Trigger Archon**:
- Task M12 install `claude-mem` -> hook SessionStart + Stop wire-up modifica permanente `~/.claude/settings.json`. Interaction con H12 hooks codemasterdd attivi (commit `bc2d3...`). Architectural lock-in -> applica RESTATE + ENUMERATE + DECOMPOSE + CHALLENGE + RECONSTRUCT + RED-TEAM + CALIBRATE prima di committare config prod.
- Scelta esclusiva claude-mem vs `affaan-m/everything-claude-code` Memory Persistence -> exclusion irreversibile (uno bloccca l'altro per evitare doppio store / drift sync). Archon obbligatorio.
- Task M11 install ufficiale `anthropics/skills` selettivo -> verifica che skill scelte non collidano con built-in Claude Code skills nominate uguale.

**Falsifying experiment** (CALIBRATE pre-commit, ~5min):
- claude-mem: prima di hook prod, dry-run isolato in scratch repo: 1 sessione test capture + restore. Se restore non riesce -> DON'T commit prod config.
- skills install: prima `mv ~/.claude/skills/<skill> ~/.claude/skills/.test-<skill>` rename test, sessione smoke 5min, poi rename back se OK.

**NO Archon per**: bookmark Task D (low-stakes reversibile), refresh stars table (no architectural impact).

### Protocol 4 -- AA01 workspace audit trail (workflow standard)

Per ogni task M11-M14 esecuzione SHIP:
1. **NON** procedere senza prima `bash scripts/classify.sh inbox/<file>` + `bash scripts/promote.sh inbox/<file> research-long`
2. DRAFT contiene autoresearch (Protocol 2 output) + Archon decision se applicabile
3. PROPOSED gate: decisioni finali (INSTALL/BOOKMARK/SKIP/AUDIT-ONLY) firmate con rationale aggiornato
4. SHIP gate: install/bookmark eseguito + verify smoke + JOURNAL entry codemasterdd
5. **Lesson obbligatoria** `learnings/L-2026-05-NNN-<slug>.md` -- NO archive `--status=SHIP` senza lesson
6. Update master table `subagents-skills-candidates.md` con stato finale (INSTALLED/BOOKMARKED/SKIPPED/DORMANT)

**Anti-pattern**: F2 cimitero (archive senza lesson), F3 confused re-opening, F4 inbox-zero theater (auto-promote senza confirm scope).

### Quando fare back-engineering

Trigger di back-engineering (re-decostruire decisioni handoff):

| Trigger | Action |
|---------|--------|
| Decisione preliminare nel handoff non chiara o "perche'?" | Risali al commit `d820d9f` + leggi rationale in `subagents-skills-candidates.md` sezione Wave 2026-05-12. Se ancora non chiaro -> Protocol 3 Archon. |
| Decisione preliminare contraddice altro ADR / lesson recente | Re-prioritizza ADR/lesson recente. Handoff e' snapshot 12/5 sera -- altre evidence successive vincono. |
| Star count o stato repo cambiato significativamente vs handoff | Re-trigger autoresearch Protocol 2 + aggiorna decisione preliminare. |
| 2 task M11-M14 hanno overlap che il handoff non risolve | Decostruisci scope, eventualmente split o merge task. NON forzare separazione artificiale. |
| Tu (sub-agent / Claude Code session) non puoi accedere a path `C:/Users/edusc/...` o `C:/dev/...` | Stop. Comunica a Eduardo che e' Eduardo direct execution, NON sub-agent automatable. NO finta esecuzione. |

---

## Stato repo (snapshot al commit `d820d9f`)

- Branch: `claude/read-image-generate-list-iJwhs`
- Commit: `d820d9f docs(reference): wave 2026-05-12 batch eval 12 top claude code repos`
- PR draft: **https://github.com/MasterDD-L34D/codemasterdd-ai-station/pull/57**
- Status: 1 ahead di main, 0 review/CI pending

**Verify questo snapshot ancora valido** (Protocol 1 sopra) prima di assumere correttezza.

## Cosa e' stato prodotto in sessione cloud 12/5 sera

### 1. Reference esteso
`docs/reference/subagents-skills-candidates.md` -- sezione nuova "Wave 2026-05-12 batch evaluation":
- OCR drift table (importante: `obra/superpowers` reale ~16.6k NON 148k OCR; `awesome-claude-code-subagents` reale ~8.1k NON 17.1k)
- 9 nuovi repo categorizzati + refresh 3 gia coperti (#1, #6, #11)
- Tabella riepilogo 12-row con decisioni preliminari INSTALL/BOOKMARK/SKIP/AUDIT-ONLY

**Caveat back-engineering**: decisioni preliminari = output di analisi 12/5 sera basata su README scan + GitHub stats live quel giorno. NON sono binding. Re-verify con Protocol 2 prima di SHIP ognuna.

### 2. 4 scaffold AA01 paste-ready
`docs/aa01-handoff/`:
- `2026-05-12-A-skills-resources.md` -- skills (#1 refresh, #3, #5, #10), 4-6h
- `2026-05-12-B-subagent-memory-resources.md` -- claude-mem INSTALL + VoltAgent refresh, 2-3h
- `2026-05-12-C-dev-tools-resources.md` -- repomix INSTALL + gsd BOOKMARK, 2h
- `2026-05-12-D-guides-awesome-design-resources.md` -- bookmark-heavy, 1-2h
- `README.md` -- workflow handoff documentato

### 3. BACKLOG + JOURNAL
- `BACKLOG.md` -- M11/M12/M13/M14 (uno per task AA01)
- `JOURNAL.md` -- entry sessione `2026-05-12 (sera)` con discovery OCR drift + boundary preserved

## Esecuzione (Eduardo direct sul PC) -- DOPO Protocol 1+2

### Step 1 -- AA01 paste (5-10 min, post Protocol 1 verify scaffold ancora aderente)

```bash
cd C:/Users/edusc/aa01

# Esempio Task A
cp /c/dev/codemasterdd-ai-station/docs/aa01-handoff/2026-05-12-A-skills-resources.md inbox/
bash scripts/classify.sh inbox/2026-05-12-A-skills-resources.md
bash scripts/promote.sh inbox/2026-05-12-A-skills-resources.md research-long
# Ripeti per B, C, D oppure solo i task che vuoi attivare ora
```

### Step 2 -- decidi priorita esecuzione (NON binding la mia raccomandazione)

Mia raccomandazione 12/5 sera (basata su utility immediata + effort low-first):
1. **M13 Task C** -- repomix install (utility cross-repo immediata, lowest risk). Effort 2h.
2. **M12 Task B** -- claude-mem first se context drift e' problema sentito ora (Archon Protocol 3 obbligatorio). Effort 2-3h.
3. **M11 Task A** -- skills foundational (deeper audit, post-Max sovereign rilevante). Effort 4-6h.
4. **M14 Task D** -- bookmark + lesson cross-pattern (lightweight, opportunistico). Effort 1-2h.

**Back-engineering trigger**: se sentito tu altro priority (es. SPRINT_02 imminente 20/5 = priority skills foundational FIRST), prevale. Handoff e' opinion, non decision.

### Step 3 -- merge PR #57

Quando ok review (e quando almeno 1 task M11-M14 e' SHIP per validare scaffold workflow end-to-end):
```powershell
gh pr ready 57   # promuovi da draft a ready
gh pr merge 57 --squash
```

Oppure lascia draft fino a outcome chiaro -- nessuna urgenza merge.

### Step 4 -- post-SHIP per ogni M11-M14

- Lesson `learnings/L-2026-05-NNN-<slug>.md` AA01 (Protocol 4 obbligatoria)
- JOURNAL entry codemasterdd con outcome (skills installati, subagent cherry-pick, ecc)
- Update `docs/reference/subagents-skills-candidates.md` tabella riepilogo con stato finale (INSTALLED / BOOKMARKED / SKIPPED)
- Vault Card Eduardo direct (per Task D guides + design)

## Discovery importanti (verify ancora rilevanti)

1. **OCR star count strutturalmente inaffidabili** (font monospace troncato): drift fino a 9x. Sempre verifica live GitHub.
2. **ADR-0027 NON necessario** in 12/5 sera analysis: policy install gia in ADR-0010 + file reference esistente. **Re-evaluate** se M12 claude-mem hook wire-up scopre architectural impact non previsto -> potrebbe servire ADR-0027 dedicato Memory + Hook coordination.
3. **3/12 repo gia coperti Apr 22** in `subagents-skills-candidates.md` (#1 affaan-m, #6 hesreallyhim, #11 VoltAgent subagents). Refresh stars + nuove decisioni inline.
4. **Boundary preserved**: AA01 e vault-shared NON-toccati direttamente. Pattern adottato: scaffold codemasterdd -> Eduardo paste manuale -> AA01 lifecycle Eduardo direct.

## Caveat / blockers potenziali

- **claude-mem (M12) install method da verify**: README repo per command esatto. Ipotesi handoff `npm install -g @thedotmack/claude-mem` ma NON validata empiricamente.
- **claude-mem vs everything-claude-code Memory**: scelta esclusiva (no doppio store). Recommended handoff: claude-mem standalone -- ma autoresearch fresh potrebbe rivelare alternative migliori (es. memory in `obra/superpowers` se overlap audit Task A discover capability).
- **claude-mem hook + H12 SessionStart hook codemasterdd**: dry run obbligatorio. Possibile ADR-0027 trigger se interaction non-trivial. Archon Protocol 3 obbligatorio.
- **Privacy guard rail**: tutti 12 repo pubblici, cloud OK. NON applicare wave su repo Synesthesia / cliente future senza re-evaluation.

## Reference path (verify exist al pickup)

- PR: https://github.com/MasterDD-L34D/codemasterdd-ai-station/pull/57
- Master table: `docs/reference/subagents-skills-candidates.md` sezione Wave 2026-05-12
- Scaffold dir: `docs/aa01-handoff/`
- BACKLOG: `BACKLOG.md` sezione "Task derivati da OCR screenshot wave 2026-05-12"
- JOURNAL: `JOURNAL.md` entry `2026-05-12 (sera)`
- ADR cognitive workflow: `docs/adr/0026-cognitive-workflow-protocols.md`
- AA01 path Eduardo: `C:/Users/edusc/aa01/`

## Anti-pattern critici (NO violare in pickup)

1. **Acceptance passiva del handoff** (skip Protocol 1 refresh-verify) -> caso studio L-2026-05-002 ripetuto.
2. **Bulk install tutti i repo** ciecamente -> cherry-pick discipline obbligatoria.
3. **Doppia memory system** (claude-mem + Memory Persistence di #1 entrambi) -> SPOF sync irreversibile.
4. **Vault Card creation da Claude Code session** -> boundary sibling-peer violato.
5. **Skip OCR validation** per future screenshot -> sempre verifica stars live.
6. **Aggiornare PR #57 prima di SHIP almeno 1 task** -> snapshot stabile preserva audit trail.
7. **Skip lesson AA01** post-SHIP -> F2 cimitero anti-pattern.
8. **Skip Archon Protocol 3** su install architectural irreversibile (claude-mem hook config) -> rischio rompere H12 SessionStart attivo.
9. **Trust handoff narrative** se contraddetto da fresh evidence -> recent + empirical wins.
10. **Eseguire fingendo accesso** a path `C:/...` da sub-agent / cloud sandbox Linux -> stop, comunica a Eduardo, NO finta esecuzione.

## Calendarizzati invariati

- 2026-05-19 Claude Max expiration (7gg residui al 12/5 sera)
- 2026-05-20+ SPRINT_02 Fase 8 sovereign
- 2026-06-07 ratification ADR-0021
- 2026-06-09 ratification ADR-0022

## Combined methodology checklist (lesson L-2026-05-002 + L-2026-05-003 + ADR-0026)

```
[Pickup handoff this file]
  -> Protocol 1 Refresh-verify state interno (OBBLIGATORIO -- skip = anti-pattern)
  -> Protocol 4 AA01 workspace audit trail start (classify + promote scaffold)
  -> Protocol 2 Autoresearch multi-source (re-validate decisioni preliminari)
  -> [Decision high-stakes irreversibile? es. claude-mem hook prod config]
        |- SI -> Protocol 3 Archon 7-step + CALIBRATE falsifying experiment
        |- NO -> empirical trial breve per architectural validation (es. dry-run scratch)
  -> Output: SHIP M11-M14 + lesson AA01 + JOURNAL entry codemasterdd + update master table
```

**Reference completo**: ADR-0026 + lesson L-2026-05-002 (anti-pattern) + lesson L-2026-05-003 (cross-repo pattern adoption).
