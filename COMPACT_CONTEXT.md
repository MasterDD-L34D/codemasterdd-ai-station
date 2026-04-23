# COMPACT_CONTEXT

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/COMPACT_CONTEXT.md`.
>
> Aggiornare in rituale chiusura sessione (CLAUDE_OPERATING_RULES.md #9).

## Progetto
- **Nome**: CodeMasterDD AI Station
- **Versione del compact**: v2 (post-integrazione Archivio framework)
- **Data ultimo aggiornamento**: 2026-04-23

## Stato attuale
- Barra globale **88%** (fasi-based). Fase 6 al 30% (6/20 dogfood + quality bench v1+v2 done).
- HEAD `a23b533`, origin/main aligned, working tree clean.
- 3 ADR strategici ratificati 2026-04-23: **0012** (RAM 64GB) + **0013** (cloud tier 3) + **0014** (Fase 6 compression).
- 6 wrapper Aider operativi + 4 API keys cloud (Groq/Cerebras/Gemini/OpenAI) + 5 modelli Ollama attivi.
- Framework operativo `Archivio_Libreria_Operativa_Progetti/` integrato come governance layer (2026-04-23 sera).

## Obiettivo di questa fase
- **Fase 6 (compressa, ~4 settimane)**: chiudere i 4 criteri ADR-0014 entro **~2026-05-20** per ratificare ADR-0015 Budget decision.
- **Target sprint corrente**: portare dataset dogfood da 6 → ≥12 (di cui ≥3 behavior-critical) + validare empiricamente fix cp1252 + cost snapshot mid-sprint.

## Cosa è già stato fatto
- Hardware setup + hardening + migrazione progetti (Fase 1-5 closed).
- Stack AI tier-routing 4 tier (cosmetic/behavior/escalation/reasoning) + privacy policy per-repo.
- 14 ADR in `docs/adr/`, 4 guard rail commit cross-agent, tracking `ccusage` + dogfood log.
- Quality bench framework riusabile (`scripts/quality-bench/`) + 75 test eseguiti.
- 6 dogfood registrati (5 cosmetic + 1 behavior), 100% success, 0 silent-corruption.
- Normalizzazione project files: 7 file governance root-level + 4 aggiuntivi (MASTER_PROMPT, REFERENCE_INDEX, PROMPT_LIBRARY, MODEL_ROUTING) compilati 2026-04-23.

## Decisioni prese
- **ADR-0001** Sovereign strategy + target budget $0-50/anno (revisionato da $60-240 via 0013).
- **ADR-0008** Hub pattern tier routing: cosmetic 7B whole, behavior 14B Q2 diff no-auto-commits, escalation 30B MoE.
- **ADR-0011** Commit governance cross-agent: `commit-msg` globale + `--git-commit-verify` + `--commit-prompt English` nei wrapper.
- **ADR-0012** RAM 64GB upgrade, qwen3:30b promosso tier 2 stabile, 32B dense scartato.
- **ADR-0013** 4 API keys cloud free/paid, storage `~/.config/api-keys/keys.env` ACL-hardened, routing Groq/Cerebras primario.
- **ADR-0014** Fase 6 timeline compressa 3 mesi → ~4 settimane, chiusura target ~20/05.
- **Adozione framework archivio** (2026-04-23 sera): schema bootstrap-kit + regole 07_OPERATING_PACKAGE come meta-governance non-distruttiva (CLAUDE.md resta autoritativo progetto-specifico).

## Vincoli hard
- RTX 5060 8 GB VRAM → tuning ctx obbligatorio modelli >7B.
- Windows cp1252 console bug Aider → fix `chcp 65001 + PYTHONIOENCODING=utf-8` nei wrapper (validazione empirica pending).
- **Deadline fissa 2026-05-19** (Claude Max expiration). Target Fase 6 closure 2026-05-20.
- Privacy per-repo rigorosa (Synesthesia mixed, repo cliente sovereign-only).
- No `--force` su main, no `--no-verify`, Conventional Commits enforced cross-agent.

## Problemi aperti
- **P1** Dogfood behavior-critical n=1 (target ≥5).
- **P2** Fix cp1252 validation empirica pending.
- **P3** Privacy validation reale 1/3.
- **P4** Memory drift HEAD.
- **P5** Aggregati mensili log da popolare.
- **P6** Qwen 7B commit-prompt 0% compliance.

Dettaglio e next actions in `BACKLOG.md` + `OPEN_DECISIONS.md`.

## File / output importanti
- Governance root-level: `PROJECT_BRIEF.md`, `COMPACT_CONTEXT.md`, `DECISIONS_LOG.md`, `BACKLOG.md`, `OPEN_DECISIONS.md`, `ROADMAP.md`, `SPRINT_01.md`, `MASTER_PROMPT.md`, `REFERENCE_INDEX.md`, `PROMPT_LIBRARY.md`, `MODEL_ROUTING.md`
- Convenzioni Claude Code: `CLAUDE.md` (progetto) + `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/*` (meta-rules adottate)
- Diario cronologico: `JOURNAL.md`
- Decision history: `docs/adr/` (14 file)
- Operational log: `logs/aider-delegation-2026-04.md`
- Framework archivio: `Archivio_Libreria_Operativa_Progetti/` (reference multi-progetto)

## Prossimi 3 passi
1. **Commit** 11 file governance nuovi/aggiornati + entry JOURNAL 2026-04-23 con rationale integrazione framework archivio.
2. **Dogfood behavior-critical cloud #2** (T1 SPRINT_01): `aider-groq scripts/quality-bench/run-bench.ps1` per retry logic 429/5xx. Validazione simultanea fix cp1252 se emerge retry.
3. **Refresh memory** `project_session_resumption.md` con HEAD attuale + pointer a `COMPACT_CONTEXT.md` (evita duplicazione contenuti).
