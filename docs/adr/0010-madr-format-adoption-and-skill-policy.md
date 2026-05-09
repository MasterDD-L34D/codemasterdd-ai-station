# ADR-0010 — Adozione MADR format da 0010+ e skill install policy via `gh skill preview`

> *TL;DR: da ADR-0010 in poi uso formato MADR bare-minimal (Considered Options + Pros/Cons sistematici); i 9 ADR esistenti restano in formato custom. Per skill Claude Code introduco policy "preview-before-install" via `gh skill preview`, nessuna installazione blind.*

- **Status**: Accepted
- **Data**: 2026-04-22
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

## Context and Problem Statement

La rivalutazione approfondita del materiale research `final-research-and-snippets-2026-04-21-v3.md` (sessione claude.ai web 2026-04-21) ha identificato due decisioni meta-architetturali pending:

1. **Format ADR**: i 9 ADR esistenti usano formato custom (Status/Data/Decisore + Contesto + Decisione + Conseguenze + Follow-up). Funziona, ma manca struttura sistematica per confronto alternative — spesso il confronto avviene narrativamente nel "Contesto".

2. **Skill install policy**: il tool `gh skill` (rilasciato 16/04/2026, compat gh 2.90.0+) permette install skill da GitHub con semantica package-manager. Il repo sorgente ha identificato skill potenzialmente utili (es. LambdaTest pytest-skill/mocha-skill per test workflow, eventuali future). Manca policy ufficiale: preview? install diretto? ADR per ogni skill?

## Decision Drivers

- Allineamento con stile ADR-backed (evidence + rationale documentati)
- Tool ecosystem concreto per MADR: `adr-kit` (CI validation), VSCode ADR Manager, template markdownlint config ufficiale
- Sovereign / supply-chain safety: skill install blind = supply-chain risk
- YAGNI minimalism (ADR-0005): nessun formalismo senza ROI chiaro
- 9 ADR esistenti: sunk-cost, retrofit non giustificato

## Considered Options

### Opzione A — Mantenere formato custom a vita
**Pro**: consistenza retroattiva, zero migrazione.  
**Contro**: Considered Options e Pros/Cons restano informali; nessun tool ecosystem.

### Opzione B — Migrare tutti 9 ADR esistenti a MADR
**Pro**: consistenza completa.  
**Contro**: effort ~2h per 9 file già funzionanti = sunk-cost pour. Rischio introdurre errori.

### Opzione C (chosen) — Adottare MADR da ADR-0010+, no retrofit
**Pro**: 
- Considered Options sistematico obbligatorio da 0010 in avanti (cattura comparison che fai già informalmente)
- Tool ecosystem oggettivo (`adr-kit` per CI validation, VSCode ADR Manager linting)
- Nessun costo migrazione — gli ADR esistenti restano validi
- Template [bare-minimal](https://github.com/adr/madr/blob/main/template/adr-template-bare-minimal.md) evita overhead RACI

**Contro**:
- Formato dual (custom 0001-0009 + MADR 0010+) = leggera inconsistenza storica
- MADR v4.0.0 ha 8 sezioni full; uso bare-minimal per evitare bloat su ADR semplici

### Per skill install policy — 3 opzioni

1. **Install-blind** (`gh skill install X`): zero friction, alto supply-chain risk
2. **Preview-before-install** (`gh skill preview X`, valutazione manuale, poi install): bilanciamento safety/velocità
3. **ADR-dedicato per ogni skill**: max safety, alto friction

**Scelto Opzione 2**: preview obbligatoria prima di `install`. Nessun ADR dedicato per singola skill salvo scenari di impatto architetturale (es. skill che modifica hooks o MCP server).

## Decision Outcome

### Format ADR
**Adottato MADR bare-minimal da ADR-0010+**. Template reference: [adr-template-bare-minimal.md](https://github.com/adr/madr/blob/main/template/adr-template-bare-minimal.md).

Sezioni minime:
- `# ADR-NNNN — Title`
- `> *TL;DR: 1-liner in italics*`
- Header `Status / Data / Decisore`
- `## Context and Problem Statement`
- `## Decision Drivers` (optional)
- `## Considered Options` (con Pro/Contro per ciascuna)
- `## Decision Outcome`
- `## Consequences`
- `## More Information` (links, refs)

TL;DR 1-liner retroattivo **verrà aggiunto ai 9 ADR esistenti** (add-only, zero logic change) per uniformità reader-quick-glance.

### Status workflow + early-acceptance flag (addendum 2026-05-09)

Trigger addendum: harsh review 2026-05-09 ha identificato V3 SIGNIFICANT (sample size empirici sotto threshold per claim "Accepted"). Eduardo scelta 3B (Decisione 007 in DECISIONS_LOG): early-acceptance flag esplicito.

**Stati ADR validi**:
- `Proposed` — decisione formulata, validation in corso, NON applicata operativamente
- `Accepted` — decisione validated empirically con sample sufficient (n>=10 OR contrarian event handled), applicata operativamente
- **`Accepted (early, n=N, ratification check YYYY-MM-DD)`** — decisione applicata operativamente MA validation con sample piccolo (n<10). Ratification check obbligatorio entro 30gg con dati addizionali. Format: `n=N` indica sample dimension al momento Accepted, `ratification check YYYY-MM-DD` e' deadline per re-evaluation
- `Superseded by ADR-NNNN` — decisione sostituita da ADR successivo
- `Deprecated` — decisione non piu' valida ma preserve per audit trail

**Trigger early-acceptance**:
- Sample size n<10 al momento decisione
- Validation qualitativa (es. 5/5 criteri PASS ma criteri sono soft)
- Pattern empirico osservato in n=1 ricognizione passiva

**Ratification check process**:
- Data deadline: 30gg da Accepted (early)
- Output: una di queste 3 azioni
  1. Status flip a `Accepted` (validation cumulativa raggiunto n>=10 + zero contrarian)
  2. ADR addendum con findings empirici + status flip o `Superseded`
  3. Status flip a `Deprecated` se contrarian event emerso

**ADR retroactive flag** (applicati 2026-05-09):
- ADR-0017 -- Accepted 2026-05-07 con 5/5 criteri qualitativi -> NO flag (criteri concreti, non early)
- ADR-0021 -- Accepted 2026-05-07 con n=1 ricognizione (Game-Godot-v2 governance autosufficiente) -> flag `Accepted (early, n=1, ratification check 2026-06-07)`
- ADR-0022 -- Accepted 2026-05-09 con n=3 dogfood (1 smoke + 2 edit reali) -> flag `Accepted (early, n=3, ratification check 2026-06-09)`

### Skill install policy
```
Nuova skill candidate → gh skill preview <repo> <skill>
  → Read SKILL.md + assess content/author/license
  → Match con use case reale (non speculativo)
  → Se OK: gh skill install + 1 riga in JOURNAL (non ADR)
  → Se impatto architetturale (hooks, MCP, runtime): ADR dedicato
```

Nessuna skill installata come side effect di curiosity.

## Consequences

### Positive
- Considered Options documentate strutturalmente → zero rischio "dimenticare un'alternativa scartata"
- `adr-kit` CI validation futuro possibile (hook pre-commit già compatibile)
- Pattern skill sicuro per `gh skill` ecosystem growing
- TL;DR retroattivo migliora readability di ADR lunghi (ADR-0007/0008/0009 sono >300 righe ciascuno)

### Negative
- Dual format (custom 0001-0009 / MADR 0010+) — mitigato da TL;DR uniforme
- MADR bare-minimal ha 6 sezioni vs 4 custom: +50% righe header per ADR brevi (accettabile)

### Neutral
- Skill policy "preview-before-install" è default sano; nessun cambio nello stato attuale (0 skill installate)

## More Information

- [MADR template bare-minimal](https://github.com/adr/madr/blob/main/template/adr-template-bare-minimal.md) (v4.0.0, 17/09/2024)
- [MADR primer (Olaf Zimmermann, 2022)](https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html)
- [adr-kit CLI + CI validation](https://github.com/kschlt/adr-kit)
- [VSCode ADR Manager extension](https://marketplace.visualstudio.com/items?itemName=StevenChen.vscode-adr-manager)
- [gh skill release changelog](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)
- Rivalutazione research: `JOURNAL.md` entry 2026-04-22 Parte 3
- Y-Statement skip rationale: [Zimmermann 2022 primer](https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html) (Y-Statement → "got deviated into MADR sections")
