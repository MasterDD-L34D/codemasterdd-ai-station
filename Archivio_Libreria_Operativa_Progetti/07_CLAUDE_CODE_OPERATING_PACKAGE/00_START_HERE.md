# Pacchetto Operativo per Claude Code

Questo pacchetto serve a trasformare il progetto in un ambiente **davvero operabile da Claude Code**.

Non è una raccolta di prompt generici.
È un sistema di regole, limiti, protocolli e file canonici che permette a Claude Code di:

- leggere l'archivio e il repo con priorità corrette
- capire cosa può decidere da solo e cosa no
- scrivere nei file giusti invece di disperdere il lavoro in chat
- eseguire refactor e sprint con un perimetro sicuro
- aggiornare la memoria del progetto a fine sessione

## Obiettivo del pacchetto

Portare il progetto da:

- repo leggibile solo da umani
- decisioni disperse
- sessioni AI scollegate
- refactor senza guardrail

A:

- repo + archivio machine-operable
- memoria persistente
- autonomia operativa con binari chiari
- sprint piccoli e verificabili
- continuità tra sessioni Claude Code

## File inclusi

- `CLAUDE_OPERATING_RULES.md`
- `TASK_EXECUTION_PROTOCOL.md`
- `SAFE_CHANGES_ONLY.md`
- `CHANGE_BUDGET.md`
- `CLAUDE_CODE_MASTER_ORCHESTRATOR.prompt.md`
- `SPRINT_00_BOOTSTRAP.md`
- `OPEN_DECISIONS.template.md`
- `REPO_AUTONOMY_READINESS_CHECKLIST.md`

## Ordine corretto di uso

1. Leggi `CLAUDE_OPERATING_RULES.md`
2. Leggi `TASK_EXECUTION_PROTOCOL.md`
3. Leggi `SAFE_CHANGES_ONLY.md`
4. Leggi `CHANGE_BUDGET.md`
5. Compila o aggiorna `OPEN_DECISIONS.md` se serve partendo dal template
6. Usa `CLAUDE_CODE_MASTER_ORCHESTRATOR.prompt.md` come prompt di avvio
7. Parti con `SPRINT_00_BOOTSTRAP.md` se il repo non è ancora pronto per autonomia vera

## Regola chiave

Claude Code non deve essere “lasciato libero”.
Deve essere **reso autonomo dentro un sistema**.

La formula corretta è:

**massima autonomia operativa, minima libertà distruttiva**
