# ADR-0021 — Multi-client instruction files (AGENTS.md per Codex + CLAUDE.md autoritativo)

> *TL;DR: la review del branch `codex/structural-reset` (rejected 2026-05-07) ha esposto un pattern Codex Cloud sandbox che confonde "non vedo i path Windows assoluti" con "i path non esistono / il repo è transplanted". Si introduce `AGENTS.md` come instruction file Codex-specifico con anti-confusion preamble. `CLAUDE.md` resta unica fonte autoritativa progetto-specifica; `AGENTS.md` è breve e rimanda. Adottato anche encoding policy ASCII-first per nuovi doc per ridurre mojibake cross-tool.*

- **Status**: Accepted
- **Data**: 2026-05-07
- **Decisore**: Eduardo Scarpelli
- **Tipo decisione**: meta-operativa (instruction surface)

## Context and Problem Statement

Il 1° maggio 2026 Codex (operando da Codex Cloud, sandbox web senza accesso al filesystem locale Windows) ha pushato il branch `codex/structural-reset` con 6 commit, 43 file modificati (+3690/-2186), e una premessa centrale: *"this checkout was transplanted away from the original workstation, all external paths are missing"*.

La review sistematica eseguita il 2026-05-07 sul **PC corretto** (CodeMasterDD) ha verificato empiricamente che **tutti i 9 path** che Codex marcava "missing" esistono fisicamente:

- `C:\dev\Game`, `C:\dev\synesthesia`, `C:\Users\edusc\Dafne\workspace\swarm`, `C:\Users\edusc\aa01`
- `C:\Users\edusc\.local\bin` (7/7 wrapper aider-* installati)
- `C:\Users\edusc\.config\api-keys\keys.env`
- `~/.aider.conf.yml`
- `logs/aider-delegation-2026-04.md`, `apps/dogfood-ui/data/dogfood.sqlite`, `scripts/quality-bench/results/`

Il branch è stato **rejected** in toto perché il framing "structural recovery / quarantine external repos" cancellava la governance reale (CLAUDE.md -312, MODEL_ROUTING.md -359, STATUS_MULTI_REPO.md -247) sostituendola con stato "dormant" basato su falsa premessa. Tuttavia la review ha esposto un **bisogno reale** di copertura cross-client:

1. **Codex Cloud sandbox non ha filesystem locale**: il pattern OpenCode/Cursor/Codex usa `AGENTS.md` come convenzione standard di entry-point (vedi `https://agents.md/`). Senza un AGENTS.md anti-confusion, agent operanti in sandbox potrebbero ripetere lo stesso errore.
2. **CLAUDE.md è ottimizzato per Claude Code** (stack tier routing dettagliato, hardware specs, sezione "Progetti monitorati" con path Windows). Per Codex/OpenCode/altri client web-based serve una versione operativa più asciutta.
3. **Encoding mojibake**: file legacy (`Ã`, `â€”`) sono presenti in alcuni doc. Riscritture Codex/Aider su file mojibake amplificano artifact. Serve policy ASCII-first per nuovi doc senza riscrittura globale cieca (consistente con principio Codex `encoding-policy.md` che era unico cherry-pick valido).

## Decision Drivers

- **Anti-confusion ricorrenza**: prevenire un secondo `codex/structural-reset` quando Codex (o altri agent sandbox-confined) opera in futuro
- **Convenzione agents.md**: standard cross-tool emergente, supportato da OpenCode, Cursor, Codex, Aider context loading
- **CLAUDE.md autoritativo**: nessuna duplicazione di stato; CLAUDE.md resta fonte progetto-specifica unica
- **YAGNI minimalism (ADR-0005)**: AGENTS.md ≤ 80 righe, no clone CLAUDE.md
- **Coabitazione preserva ADR-0010**: `CLAUDE.md` autoritativo per decisioni progetto; AGENTS.md è layer compatibilità, non override

## Considered Options

### Opzione A — Solo CLAUDE.md, niente AGENTS.md (status quo)

**Pro**: zero file nuovi, single source of truth.
**Contro**: Codex Cloud non sempre legge CLAUDE.md correttamente (path Windows assoluti `C:\...` lo confondono); pattern `codex/structural-reset` ricorrente. Convenzione `agents.md` sempre più diffusa, perdere allineamento è friction.

### Opzione B (chosen) — `AGENTS.md` minimale + `CLAUDE.md` autoritativo

`AGENTS.md` (≤ 80 righe) come entry-point Codex/OpenCode/altri agent web-based, con:
- preamble anti-confusion sui path Windows assoluti
- pointer obbligatorio a CLAUDE.md per dettaglio operativo
- repo state minimo (Fase 6 attivo, branch convention, encoding policy)
- esplicito "non quarantinare external repos senza chiedere"

CLAUDE.md resta autoritativo. AGENTS.md non duplica info, rimanda.

**Pro**:
- Risolve confusion sandbox empirica (Codex Cloud)
- Allineato a convenzione cross-tool
- Costo low: 1 file, ~70 righe, no maintenance overhead se CLAUDE.md cambia (AGENTS.md ha solo pointer)

**Contro**:
- Due file da tenere coerenti (mitigato: AGENTS.md si limita a pointer, non duplica)
- Coabitazione con regole 07_CLAUDE_CODE_OPERATING_PACKAGE da chiarire (mitigato: AGENTS.md scope = preamble Codex, non override regole meta)

### Opzione C — Riscrivere CLAUDE.md per essere multi-client friendly

**Pro**: single file.
**Contro**: perderemmo dettaglio Claude Code-specific (stack tier routing, hardware, ADR pointers); peggiora esperienza Claude Code per coprire un edge case Codex Cloud. Anti-pattern.

### Opzione D — Solo encoding policy, no AGENTS.md

**Pro**: zero ridondanza file.
**Contro**: lascia il pattern confusion sandbox irrisolto. La policy encoding affronta solo 1/2 problemi.

## Decision Outcome

**Scelto Opzione B**: introduzione `AGENTS.md` minimale + adozione encoding policy ASCII-first per nuovi doc.

### AGENTS.md (root-level, tracked)

Contenuto:
- 1 paragrafo preamble: "questo è il PC corretto, path Windows assoluti `C:\...` sono attesi e validi; se non li vedi, sei in sandbox; non concludere 'missing/transplanted', chiedi"
- Lista 4 progetti esterni (Game/Synesthesia/Dafne/AA01) come ATTIVI, non dormant
- Pointer a CLAUDE.md come autoritativo
- Branch convention `codex/...` ok ma review obbligatoria contro CLAUDE.md prima di merge
- Encoding policy: nuovi doc ASCII-first; legacy mojibake frozen (no global rewrite)

### Encoding policy (CLAUDE.md "Convenzioni operative" → nuova subsection)

- Nuovi file `.md` creati da agent (Codex, Aider, Claude Code) → ASCII puro per content principale
- Caratteri non-ASCII consentiti: emoji status (⚠️ ✅ 🔴), simboli matematici (≥, ≤, →) se semanticamente rilevanti
- Em-dash `—`, middot `·`, smart quotes `' '` `" "`: **evitare** in nuovi doc (sostituire con `--`, `|`, `'`, `"`)
- File legacy con mojibake (`Ã`, `â€”`, ecc.): frozen — non riscrivere blind. Fix mirato solo se file diventa attivamente confusing per task corrente.

### Coabitazione 3 file

```
AGENTS.md       — preamble Codex + altri agent web-based (≤ 80 righe)
                  scope: anti-confusion sandbox, path map, pointer
CLAUDE.md       — autoritativo progetto (stack, tier, hardware, convenzioni)
                  scope: tutto il dettaglio operativo Claude Code-centric
07_OPERATING/   — regole meta-universali (CLAUDE_OPERATING_RULES + TASK_EXEC + ...)
                  scope: pattern operativi cross-progetto
```

In caso conflitto: CLAUDE.md > AGENTS.md su decisioni progetto; AGENTS.md > CLAUDE.md su preamble sandbox-awareness; 07 > tutto su pattern Claude Code generici.

## Consequences

### Positive

- Codex (e altri agent web sandbox) ricevono preamble esplicito → riduzione rischio ricorrenza pattern `structural-reset`
- Allineamento convenzione cross-tool `agents.md`
- Encoding policy ASCII-first mitiga drift mojibake senza riscritture cieche (anti-pattern visto in Codex branch)
- `CLAUDE.md` resta lean per Claude Code, non polluted da preamble multi-client

### Negative

- Un file in più da curare (AGENTS.md)
- Drift risk se CLAUDE.md cambia path/scope e AGENTS.md pointer obsoleto (mitigato: AGENTS.md ha solo pointer, no duplicate state)

### Neutral

- Branch `codex/structural-reset` rimane reference storica come case-study sandbox-confusion (non mergeato, possibile delete remote dopo close)
- Concept `config/machine-profile.example.yaml` (multi-PC portability template) **deferred** — riprendere se/quando entra Mac mini come secondo device (vedi CLAUDE.md "Estensioni future")

## Follow-up

- [x] Scrivere `AGENTS.md` (root-level, ≤ 80 righe)
- [x] Aggiungere subsection "Encoding e charset" in CLAUDE.md "Convenzioni operative"
- [x] Aggiungere pointer ad AGENTS.md in CLAUDE.md "Ordine di lettura raccomandato"
- [x] ADR-0021 scritto
- [ ] Chiudere branch `codex/structural-reset` su origin (delete remote ref) dopo merge ADR-0021
- [ ] Decidere se aggiungere check pre-commit ASCII-only su nuovi `.md` (deferred, gather data primo)
- [ ] Future: se entra Mac mini come device secondario → riconsiderare `config/machine-profile.example.yaml` template (concept Codex valido in scenario multi-PC)

## Riferimenti

- Branch rejected: `codex/structural-reset` (HEAD `4b7c84a`, 2026-05-01, rejected 2026-05-07)
- ADR-0010 — MADR format adoption + skill policy: `0010-madr-format-adoption-and-skill-policy.md`
- ADR-0011 — cross-agent commit governance: `0011-cross-agent-commit-governance.md`
- Convenzione `agents.md`: https://agents.md/
- Pattern OpenCode instruction file portability: vedi `docs/recovery/original-system-intent.md` del branch rejected (sezione "OpenCode's intended role" — cherry-pick conceptuale, file non importato)
