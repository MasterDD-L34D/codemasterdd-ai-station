# COMPACT_CONTEXT

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/COMPACT_CONTEXT.md`.
>
> Aggiornare in rituale chiusura sessione (CLAUDE_OPERATING_RULES.md #9).

## Progetto
- **Nome**: CodeMasterDD AI Station
- **Versione del compact**: v3 (post-sprint01 T1+T2 execution)
- **Data ultimo aggiornamento**: 2026-04-23 22:30

## Stato attuale
- Barra globale **88%** invariata. Fase 6 al **40%** (8/20 dogfood + quality bench v1+v2 done).
- HEAD `e687b42`, origin/main aligned, working tree clean.
- **Commit sessione 2026-04-23 sera**: `4f5227c` (governance framework) → `e7a4ed0` (JOURNAL framework) → `f80ab3c` (retry logic quality-bench rescue) → `2dccec7` (apostrofo fix Aider auto) → `e687b42` (findings consolidation). **5 commit**, pushed.
- Fase 6 dataset attuale: 5 cosmetic full + 1 cosmetic partial + 1 behavior success + 1 behavior **REJECT**. Fail rate 12.5% (vs 30% threshold ADR-0014). Zero silent-corruption working-tree cumulative.
- Framework operativo `Archivio_Libreria_Operativa_Progetti/` integrato come governance layer.

## Obiettivo di questa fase
- **Fase 6 (compressa, ~4 settimane)**: chiudere 4 criteri ADR-0014 entro **~2026-05-20**.
- **Sprint 01 target**: dataset 8 → ≥12 dogfood (di cui ≥3 behavior-critical) + validare cp1252 + review settimana 2.

## Cosa è già stato fatto

### Pre-sessione corrente
- Hardware setup + hardening + migrazione progetti (Fase 1-5 closed).
- Stack AI tier-routing 4 tier + privacy policy per-repo.
- 14 ADR, 4 guard rail commit cross-agent, tracking `ccusage` + dogfood log.
- Quality bench framework (75 test, 100% pass@1 discriminant-limited).
- 11 file governance root-level + 4 aggiuntivi compilati seguendo schema archivio.
- Framework `Archivio_Libreria_Operativa_Progetti/` importato e integrato.

### Sessione 2026-04-23 sera (governance + sprint01 T1/T2)
- **Normalizzazione governance**: 11 file schema archivio, 3 Decisioni non-ADR registrate (001/002/003).
- **T1 behavior-critical cloud REJECT**: Groq 70B ha prodotto 5 constraint violations su retry logic `Invoke-Model`, inclusa 1 BLOCKING (return-value divergence tra branch). **Rescue manuale** Claude Code con helper `Invoke-ModelRequest` — commit `f80ab3c`, syntax validated.
- **T2 cosmetic local partial**: Qwen 7B ha fixato apostrofo elisione in `bench-ollama.ps1` (✅) ma skippato condensazione NOTES (❌). Auto-commit retry ADR-0011 validato (hook block → Aider self-retry → pass 2nd-try) — commit `2dccec7`.
- **OD-006 proposta**: constraint-count come seconda dimensione routing (≥5 constraint strict → manual Claude Code preferito).
- **Consolidamento findings** in `JOURNAL`, `OPEN_DECISIONS`, `MODEL_ROUTING`, `BACKLOG` — commit `e687b42`.

## Decisioni prese

### ADR strategici (14, indice in DECISIONS_LOG)
- **ADR-0008** Hub pattern tier routing (cosmetic/behavior/escalation)
- **ADR-0011** Commit governance cross-agent
- **ADR-0012** RAM 64GB upgrade, qwen3:30b tier 2 stabile
- **ADR-0013** Tier 3 cloud free providers — Groq/Cerebras primary
- **ADR-0014** Fase 6 compressa a ~4 settimane

### Decisioni non-ADR (operative minori, in DECISIONS_LOG)
- **001** Adozione schema framework archivio per governance files
- **002** `FIRST_PRINCIPLES_GAME_CHECKLIST` N/A per questo repo (non game)
- **003** Regole 07_OPERATING_PACKAGE non clonate al root (pointer + adozione)

## Vincoli hard
- RTX 5060 8 GB VRAM → ctx tuning obbligato modelli >7B.
- Windows cp1252 bug Aider → fix deployato ma **validazione empirica pending** (5 dogfood consecutivi senza retry loop naturale).
- **Deadline fissa 2026-05-19** (Claude Max expiration). Target Fase 6 closure 2026-05-20.
- Privacy per-repo rigorosa (Synesthesia mixed, cliente sovereign-only).
- No `--force` su main, no `--no-verify`, Conventional Commits enforced.

## Problemi aperti

- **P1** Dogfood behavior-critical n=2 (1 success + 1 REJECT). Target ≥5.
- **P2** Fix cp1252 validation empirica ancora pending (5 dogfood senza trigger retry loop).
- **P3** Privacy validation reale 1/3.
- **P6** Qwen 7B commit-prompt 0% compliance (ma auto-retry post-hook-block **funziona** empirically — nuovo dato positivo dogfood #8).
- **P7 (nuovo)** — Cloud 70B degrada a 20% compliance su behavior-critical con ≥5 strict semantic constraint (dogfood #7). Implicazione: ridimensionamento shift cloud-first di ADR-0013.

Dettaglio e next actions in `BACKLOG.md` (H1-H6) + `OPEN_DECISIONS.md` (OD-001 to OD-006).

## File / output importanti
- Governance root-level (11): `PROJECT_BRIEF`, `COMPACT_CONTEXT` (questo), `DECISIONS_LOG`, `BACKLOG`, `OPEN_DECISIONS`, `ROADMAP`, `SPRINT_01`, `MASTER_PROMPT`, `REFERENCE_INDEX`, `PROMPT_LIBRARY`, `MODEL_ROUTING`
- Convenzioni Claude Code: `CLAUDE.md` (progetto) + `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/*` (meta-rules adottate)
- Diario cronologico: `JOURNAL.md` (3 nuovi entries sessione 2026-04-23)
- Decision history: `docs/adr/` (14 file)
- Operational log: `logs/aider-delegation-2026-04.md` (8 dogfood entries + breakdown per classe)
- Framework archivio: `Archivio_Libreria_Operativa_Progetti/` (130 file multi-progetto)

## Prossimi 3 passi
1. **H1** — Aggiungere ≥3 dogfood behavior-critical aggiuntivi (attuale n=2). Preferito mix Groq 70B + locale 14B Q2 per bilanciare dataset. Candidati reali emergenti dal lavoro quotidiano (NON bench artificiali).
2. **H6** — Validare empiricamente OD-006 con n≥3 dogfood di constraint-count variabile (1, 3, 5+). Se pattern confermato → ADR-0016 seconda dimensione routing.
3. **Review settimana 2** (~2026-05-07) — sessione ~30min: count dataset + fail rate + cost proiezione + ETA chiusura Fase 6. Decisione on-track / mid-course / extension early-warning.

## Next session restart: cosa leggere per ripartire

Ordine raccomandato:
1. `CLAUDE.md` — convenzioni progetto
2. Questo file (`COMPACT_CONTEXT.md`) — snapshot stato corrente
3. `Archivio_.../07_CLAUDE_CODE_OPERATING_PACKAGE/CLAUDE_OPERATING_RULES.md` — regole meta-operative
4. `BACKLOG.md` + `OPEN_DECISIONS.md` — cosa è aperto
5. `SPRINT_01.md` — sprint attivo + task candidates
6. ADR rilevanti solo se task tocca topic noto

Memory auto-caricata via `~/.claude/projects/.../memory/MEMORY.md`.
