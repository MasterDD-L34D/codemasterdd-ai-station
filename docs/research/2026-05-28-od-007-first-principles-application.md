# OD-007 -- First-principles application + verdict (2026-05-28)

> **Trigger**: Eduardo, "facciamo OD-007 con metodo" + "e' il momento giusto per usare la checklist appena creata?"
> **Method**: `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` (root, creato stamane chiudendo OD-005). Dogfood + validation del metodo.
> **Scope**: applicate solo 5 sezioni (1, 3, 4, 7, 9 + gate 10) -- quelle rilevanti per una decisione build-vs-skip su una singola feature. Sezioni 2/5/6/8 skip (over-engineer per feature-decision).

## Ground-truth raccolto (currency-gate interno)

| Fatto | Fonte | Implicazione |
|-------|-------|--------------|
| ARCHON v2 ha gia' design + skill per "Agent Scanner" | `C:/Users/edusc/aa01/research/07-subagents-and-registry/README.md` + `archon/skills/agent-scanner/SKILL.md` + `archon/templates/agent_registry.yaml` | La feature **esiste**, non e' "missing" |
| Decisione D-007 ARCHON: "Agent Scanner con soglia overlap 70" | `aa01/research/07-subagents-and-registry/README.md` link decision-log | Design ratificato (non solo proposto) |
| Skill ha 4 trigger mandatori | SKILL.md: BOOTSTRAP / TEAM_FORMATION / DELTA / ON_DEMAND | Operativa, invocabile |
| Anti-pattern listato esplicitamente: "Shadow duplication -- creare planner-v2 quando planner funziona" | research README + Ibrahim 2026 "Build on existing work. Never recreate." | Costruire OD-007 = violazione self-aware |
| AA01 `AGENTS.md` NON contiene riferimenti a "scanner" / "D-007" / "Strato 11" | grep AGENTS.md = 0 hit | Gap reale = discovery, NON feature |

## Sezione 1 -- Verita fondamentali (di AA01)

1. "Build on existing work. Never recreate." (cardine ARCHON, Ibrahim 2026; Microsoft Multi-Agent Ref Arch: monitor overlap to prevent redundancy)
2. AA01 = personal cognitive studio per task >=30min cross-session value (workflow inbox -> workspace -> archive -> lesson)
3. Disciplina > feature (Three Strikes: feature emerge solo dopo 3 frizione reali, non da idea-disgiunta-da-evidenza)

Verifica assiomi: ognuna ancorata in materiale tracciabile (1 = fonte esterna citata in research README; 2 = `aa01/AGENTS.md` "CHI SEI"; 3 = AA01 AGENTS.md "CONVENTIONS").

## Sezione 3 -- Test di cancellazione su "build OD-007 capability registry"

Domanda: se NON costruisco una nuova capability registry (verdict skip), quale verita fondamentale violo? Quale workflow si ferma?

Risposta: **nulla si rompe**.
- Verita 1 ("build on existing") -- se COSTRUISCO, la violo. Skip e' verita-coerente.
- Verita 2 (cognitive studio inbox->lesson) -- registry indipendente da questo flow.
- Verita 3 (disciplina > feature) -- Three Strikes mai attivato (18+ task AA01 zero learning friction-related). Skip e' disciplina-coerente.

| Asset proposto | Verita servita | Se NON lo costruisco si rompe? | Categoria | Azione |
|---|---|---|---|---|
| Nuova capability scan AA01 (OD-007 original framing) | Nessuna (esiste gia' ARCHON Agent Scanner) | No | Cerimoniale / shadow-duplicate | **TAGLIA proposta originale** |
| ARCHON Agent Scanner esistente | Verita 1 esplicitamente | Si (workflow ARCHON D-007 si ferma) | Core ARCHON | **TIENI** (gia' built) |
| Link in AA01 AGENTS.md drill-down -> Agent Scanner | Verita 1 + discovery | Si (scanner resta forgotten in drill-down profondo) | Supporto utile | **CONSIDERA** (1-2 righe, Eduardo-direct AA01-side) |

## Sezione 4 -- Triade fondamentale AA01

1. **mission**: personal cognitive studio Eduardo per task >=30min cross-session value (lesson + archon protocol)
2. **scope**: lifecycle task (inbox -> workspace -> archive -> lesson promote); decision logging (D-NNN ARCHON); skill registry interno
3. **constraint dominante**: "build on existing work, never recreate" + Three Strikes + lesson-after-ship obbligatoria

OD-007 (proposta originale "costruisci nuova registry") **violerebbe il constraint dominante**. La triade e' stabile, OD-007 era una frizione mal-formulata.

## Sezione 7 -- Rational Design

Comportamento desiderato (framing originale OD-007 2026-05-11):
- "Agent-in-sessione sceglie tool corretto senza bias 'chi-ho-piu-memoria-recente-vince'"

Comportamento attuale indesiderato (framing originale):
- "Scelgo agent arbitrario / duplico harsh-reviewer perche' lo sapevo io"

Comportamento attuale REALE (post-evidence 2026-05-28):
- L'Agent Scanner skill ESISTE e ha trigger mandatorio BOOTSTRAP, MA non viene invocata perche' AA01 `AGENTS.md` (entry-point primario) non la cita nel drill-down section. Frizione = "discovery gap", non "feature missing".

Implicazione: **costruire registry parallela non risolve il discovery gap, lo peggiora** (raddoppia la surface da scoprire). Fix che risolve davvero il comportamento desiderato:

1. 1-2 righe in `aa01/AGENTS.md` sezione DRILL-DOWN -> link `archon/skills/agent-scanner/SKILL.md`
2. Invocazione esplicita al BOOTSTRAP di una nuova AA01 task (gia' richiesta dal SKILL stesso, basta renderla visible dall'entry-point)

## Sezione 9 -- Decisione finale

- **Strategia scelta**: **STRONG-SKIP del build OD-007 (proposta originale "costruisci nuova registry")** + **ADOPT existing ARCHON Agent Scanner**.
- **Primo step utile** (opzionale, AA01-side Eduardo-direct -- NON codemasterdd action): aggiungi 1-2 righe in `aa01/AGENTS.md` DRILL-DOWN che linkano `archon/skills/agent-scanner/SKILL.md` come "tool-selection registry". Validation = la prima AA01 task successiva invoca scanner al BOOTSTRAP senza che Eduardo debba ricordarselo.
- **NON toccare**: ARCHON internals (scope AA01 self-governed, fuori dominio codemasterdd). Skill registry yaml e' di pertinenza ARCHON D-007.

## Sezione 10 -- Gate finale

- [x] So cosa deve fare davvero AA01 (personal cognitive studio, non tool-builder)
- [x] So cosa deve fare davvero il workflow (build on existing + Three Strikes)
- [x] So cosa deve fare davvero la triade (mission + scope + constraint dominante)
- [x] Sto evitando complessita senza valore (no shadow-duplicate planner-v2)
- [x] Il primo step e' leggibile e motivato (verifica discovery gap, non build feature)

**Verdetto: STRONG-SKIP RATIFIED**. OD-007 in `OPEN_DECISIONS.md` chiuso come **CLOSED-DUPLICATE-CONFIRMED** (la feature esiste in ARCHON). Fix discovery proposto AA01-direct, non codemasterdd action.

## Meta -- validation del metodo (FIRST_PRINCIPLES_INFRA_CHECKLIST)

- **Tempo applicazione**: ~5 minuti su una decisione che era aperta da 17 giorni.
- **Sezioni usate** (5/10): 1, 3, 4, 7, 9 + gate 10. Le altre (2/5/6/8) erano over-engineer per una single feature-decision.
- **Output**: verdetto chiaro + rationale tracciabile + step concreto.
- **Lezione meta**: la checklist e' molto stringente sul test di cancellazione (sezione 3) -- non basta dire "no friction", devo dire "se NON lo costruisco quale verita violo / quale workflow si ferma". Filtraggio piu' affilato del semplice usage-count.
- **Lezione meta-2**: la sezione 7 (rational design "comportamento attuale REALE vs supposto") ha riformulato OD-007 da "feature missing" a "discovery gap" -- diagnosi totalmente diversa con stesso prompt. Questo da sola giustifica la checklist.
