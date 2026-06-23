# Spec — Context-Files Governance Reorg (CLAUDE.md + rules + reference)

> **Status (2026-06-23):** shipped -- Fasi 1-6 complete 2026-06-03

- **Status**: PROPOSED (brainstorming-approved 2026-06-03, design shape + global example approved by Eduardo)
- **Author**: Claude Opus 4.8 (1M) hub session
- **Date**: 2026-06-03
- **Scope owner**: codemasterdd-ai-station (policy hub) + user-global `~/.claude/`
- **Cognitive protocols applied**: P6 brainstorming (this flow) ; research = web-scan mirato (official Anthropic docs + AGENTS.md standard + expert consensus). harsh-reviewer invoked? pending (P5, post-spec). 

## TL;DR

I file di contesto (CLAUDE.md global + project) sforano 2-3x il limite ufficiale (<200 righe)
e caricano ~25k token OGNI sessione, causando il failure-pattern documentato da Anthropic
("over-specified CLAUDE.md -> Claude ignora meta delle regole"). Riorganizzo con approccio
**index + moduli on-demand**: CLAUDE.md slim = solo regole sempre-attive come comandi diretti;
il detail topic-specifico si sposta in `.claude/rules/` (path-scoped), reference doc, skill,
e authority file gia esistenti -- caricamento on-demand, **niente contenuto perso**, solo rilocato.
Target: ~25k -> ~6-8k token sempre-caricati. Programma multi-fase; Fase 1 (questo spec) =
global + project CLAUDE.md + rules + reference. Repo esterni in fasi successive, via branch+PR.

## Problema (quantificato)

| File | Attuale | Limite ufficiale | Sforamento |
|---|---|---|---|
| `~/.claude/CLAUDE.md` (global) | 435 righe / ~6.8k tok | <200 righe / <5k tok | 2.2x |
| `codemasterdd/CLAUDE.md` (project) | 569 righe / ~15.9k tok | <200 righe / <5k tok | 2.8x |
| **Sempre caricato/sessione** | **~25k tok** (+ MEMORY.md ~2.5k) | -- | massiccio |

Root cause del bloat: contenuto che NON deve caricare ogni sessione vive inline --
catalogo 19 anti-pattern (sono learnings), tabelle hardware/bench, dettaglio fleet-SSH,
7 protocolli cognitivi full, blocchi per-repo full, routing tables. Tutto questo ha gia
una home autoritativa (learnings dir, ADR, runbook, STATUS_MULTI_REPO, MODEL_ROUTING).

## Standard researched (la rubrica riusabile)

Fonti: Anthropic [memory](https://code.claude.com/docs/en/memory) + [best-practices](https://code.claude.com/docs/en/best-practices),
standard [AGENTS.md](https://agents.md/) (Linux Foundation), consenso esperti 2026.

Regole load-bearing (rubrica di audit per OGNI context file):

1. **Size <200 righe/file.** Oltre -> adherence cala, regole importanti si perdono nel rumore.
   Target aggressivo: <5k token.
2. **CLAUDE.md carica SEMPRE INTERO** (no cap). MEMORY.md invece e cappato a 200 righe / 25KB
   (primo che scatta); resto on-demand.
3. **`@import` NON salva token** -- i file importati caricano interi al launch. E solo
   organizzazione, NON riduzione contesto. Quindi: la vittoria e spostare FUORI dal
   sempre-caricato, non splittare in import.
4. **Cosa salva contesto davvero**:
   - **Skills** (`.claude/skills/`) -- workflow rilevanti-a-volte, load on-demand/on-invoke.
   - **`.claude/rules/` path-scoped** (`paths:` frontmatter) -- caricano solo quando Claude
     tocca file matchanti.
   - **docs/reference** referenziati per prosa (Claude legge on-demand).
   - `.claude/rules/` SENZA `paths:` carica ogni sessione (= stesso costo di CLAUDE.md):
     usarlo solo per modularita, non per risparmio.
5. **Comandi diretti verificabili** ("usa 2-space", non "formatta bene"). `IMPORTANT`/`YOU MUST`
   per adherence su regole critiche.
6. **Niente contraddizioni** -- regole in conflitto -> Claude sceglie a caso. Pruna conflitti.
7. **HTML comment `<!-- -->`** strippati pre-inject -> note manutentore a costo zero token.
8. **Includi**: comandi non-inferibili, code-style che differisce dai default, test runner,
   repo-etiquette (branch/PR), decisioni architetturali specifiche, env-quirk, gotcha non-ovvi.
   **Escludi**: cio che Claude inferisce dal codice, convenzioni standard, API-doc dettagliata
   (linka), info che cambia spesso, spiegazioni lunghe, descrizioni file-by-file, ovvieta.
9. **AGENTS.md**: Claude NON lo auto-legge. Coesistenza: `@AGENTS.md` import in CLAUDE.md,
   o symlink (Windows: usa l'import). 28+ tool leggono AGENTS.md (Codex/Jules/Cursor/Aider).
10. **Treat like code**: review quando qualcosa va storto, pruna regolarmente, testa osservando
    se il comportamento cambia davvero.

## Metodologia (procedura safe-slim, applicabile a ogni target)

Per ogni context file da snellire:

1. **Audit** vs rubrica: marca ogni sezione come {sempre-attiva | on-demand | morta/duplicata | stale}.
2. **Verify-no-loss PRIMA di tagliare**: per ogni sezione "on-demand", conferma che il contenuto
   esista gia in una home autoritativa; se NO -> crea reference doc con copia 1:1 PRIMA del taglio.
   (Tagliare senza preservare = anti-pattern data-loss.)
3. **Riloca**: sposta on-demand -> skill / rules path-scoped / reference / authority file.
4. **Riscrivi slim**: regole sempre-attive come comandi diretti; pointer per-prosa al detail.
5. **Measure**: before/after righe + token-est. Verifica <200 righe.
6. **Behavior-check**: la sessione successiva trova ancora il contenuto rilocato quando serve?
   (test: chiedere a Claude di applicare una regola rilocata -> deve sapere dove guardare).

## Programma (fasi)

- **Fase 1 (questo spec)**: `~/.claude/CLAUDE.md` + `codemasterdd/CLAUDE.md` + creazione
  `~/.claude/rules/` + `~/.claude/reference/`. ROI massimo (fixa il tax ~25k/sessione).
- **Fase 2**: root governance files codemasterdd (COMPACT_CONTEXT 46KB, STATUS_MULTI_REPO 63KB,
  BACKLOG 34KB, MODEL_ROUTING 24KB, OPEN_DECISIONS 25KB, DECISIONS_LOG 27KB). On-demand
  (non auto-load) -> urgenza minore, ma audit + slim/archive. JOURNAL escluso (append-only).
- **Fase 3**: memory (skill `consolidate-memory`: merge dup, fix stale, pruna MEMORY.md index)
  + agents (skill `agent-scanner`: overlap/stale audit su 18 def in `.claude/agents/`).
- **Fase 4+**: rollout per-repo (Game, Game-Godot-v2, Game-Database, Synesthesia, Dafne, vault),
  uno spec/PR per repo, boundary-aware (sotto).

Ogni fase = ciclo proprio (spec/plan/exec). Questo spec consegna Fase 1 concreta + rubrica
riusabile per le fasi 2-4.

## Fase 1 -- design concreto

### 1a. Global CLAUDE.md (APPROVATO)

Da 435 -> ~72 righe (-76%). Contenuto verbatim approvato in brainstorming 2026-06-03.
Sezioni tenute inline (sempre-attive): Fleet (2 machine + identity-check + SSH gotcha),
LLM routing (rapido + authority link + caveat 2-stage), Quality Gate 3-step, Commit
attribution ADR-0011, Agent-scanner rule, Background task, Lessons (index + 5 guardrail).

Rilocazioni:

| Tagliato | Vive ora in | Caricamento |
|---|---|---|
| 19 anti-pattern full | NEW `~/.claude/reference/anti-patterns.md` (copia 1:1) + `~/aa01/learnings/L-*` (37) | on-demand |
| llmfit prosa + auto-refresh | `C:\dev\tools\llmfit\LOCAL-LLM-STANDARD.md` + `*-fit.json` (gia SoT) | on-demand |
| SSH matrix + IP-history | `docs/runbook/ssh-inbound-fleet-setup.md` (gia SoT) | on-demand |
| PC-identity tabella 4-PC + refs | compresso (2 machine + check-cmd); full -> runbook | -- |
| Agent-scanner sources/locations | skill `agent-scanner` SKILL.md (gia esiste) | on-invoke |

Nota: `~/.claude/reference/anti-patterns.md` e OBBLIGATORIO -- gli anti-pattern #1-#7
(subprocess/stdout/filename/PDF/checkpoint/atomize/force-push) NON hanno L-ref nei learnings,
quindi senza il reference doc andrebbero persi. Verificato: 37 L-*.md esistono ma coprono ~#8-#19.

### 1b. Project CLAUDE.md (target structure)

Da 569 -> ~150 righe. Sezioni e disposizione:

INLINE (sempre-attive, comandi diretti):
- Ruolo workstation (3 righe) + pivot Hybrid A1 (1 riga + link ADR-0030).
- Stack essenziale (5 righe: Git/Claude Code/Node/Python/Ollama/Aider/OpenCode) + link
  `docs/reference/stack-installed.md` per la lista esaustiva.
- Capacita AI locali (summary 3 righe + link ADR-0012 + `docs/research/bench-*` per le tabelle).
- Tier routing (decision-summary ~8 righe) + link `MODEL_ROUTING.md` + ADR-0008/0016/0022.
- Wrapper CLI delegazione (lista nomi 1-riga ciascuno) + link sezione dettaglio.
- Privacy guard rail (regola + whitelist repo) -- load-bearing, tenuto.
- 7 protocolli cognitivi = **7 trigger 1-riga ciascuno** + link ADR-0026 (full detail).
- Convenzioni operative (git/encoding/lingua/file-mod) -- tenuto compresso.
- Repo monitorati = **1-riga/repo** (nome + path + status 1-frase) + link `STATUS_MULTI_REPO.md`.
- Aggiornamento JOURNAL (comando journal-land 2 righe).
- Ordine lettura nuove sessioni (lista) + governance meta (3 righe + link Archivio).

RILOCATO:
| Tagliato | Vive ora in | Note |
|---|---|---|
| Hardware tables full | `docs/reference/hardware-and-models.md` (NEW) + ADR-0012 | summary resta inline |
| Bench tables (isolato/mixed/swap) | `docs/research/bench-*.md` (gia esistono) | linkati |
| Stack installato esaustivo | `docs/reference/stack-installed.md` (NEW) | essenziali restano inline |
| Modelli Ollama full list | `docs/reference/hardware-and-models.md` (NEW) | `ollama list` per verify |
| Per-repo blocchi full | `STATUS_MULTI_REPO.md` (gia esiste) | 1-riga/repo resta |
| Tier routing tabelle full | `MODEL_ROUTING.md` (gia esiste) + ADR | decision-summary resta |
| Protocolli cognitivi full | `docs/adr/0026-*.md` (gia esiste) | 7 trigger 1-riga restano |

### 1c. File nuovi da creare

1. `~/.claude/reference/anti-patterns.md` -- catalogo 19 completo (copia 1:1 dal global attuale).
2. `~/.claude/rules/encoding.md` -- policy ASCII-first, path-scoped:
   `paths: ["**/*.md","**/*.ps1","**/*.sh","**/*.py","**/*.js","**/*.json","**/*.{yaml,yml}"]`.
   Carica solo quando Claude edita questi file. Hook pre-commit resta hard-enforcement.
3. `docs/reference/stack-installed.md` -- lista stack esaustiva (da project CLAUDE.md).
4. `docs/reference/hardware-and-models.md` -- hardware tables + modelli Ollama (da project CLAUDE.md).

NON creo separate `commit-governance` rule: la policy ADR-0011 e gia compressa inline nel
global slim (4 righe) + i due hook la enforce-ano. I commit non sono path-triggered, quindi
un rule path-scoped non scatterebbe -- inline+hook e la scelta corretta.

## Verifica (no-loss + behavior)

- **No-loss diff**: per ogni sezione tagliata, `grep` del contenuto chiave nella nuova home
  PRIMA di salvare lo slim. Checklist in PR description.
- **Line/token count**: `(Get-Content f).Count` su entrambi i CLAUDE.md -> conferma <200.
- **Behavior smoke** (QG Step-1): in sessione nuova, chiedere a Claude (a) "qual e la policy
  encoding?" (b) "dove sono gli anti-pattern?" (c) "regola force-push main?" -> deve rispondere
  correttamente usando i pointer (verifica che i link funzionino come on-demand recall).
- **Rules load**: `/memory` mostra `encoding.md` come loaded quando si apre un `.md`/`.ps1`.

## Rollback

Tutti i file sotto git (codemasterdd) o backuppabili (`~/.claude/` non-git -> copia `.bak`
pre-edit). Rollback = `git checkout`/restore `.bak`. Lo slim e additivo-sicuro: i reference
doc/rules nuovi non rompono nulla se i CLAUDE.md vecchi restano; il taglio e l'ultimo step,
reversibile.

## Rollout repo (Fasi 4+) -- boundary rules

Lo standard si applica ai repo esterni MA con vincoli (CLAUDE.md codemasterdd + memory
`feedback_external_repo_action_boundary`):

- **Mai overwrite diretto, mai push-main.** Ogni repo: audit -> slim -> **branch+PR, merge Eduardo**.
- **Game / Game-Godot-v2 / Game-Database**: codemasterdd "monitora solo / NON sovrascrive"
  -> auth esplicita Eduardo per-PR. Gia hanno AGENTS.md (multi-client) -> applico pattern
  `@AGENTS.md` import + slim. Public + cloud-OK.
- **Synesthesia**: mixed privacy (controllers/routes/middlewares sovereign) -> no cloud-delega,
  edit local/Claude Code only.
- **vault**: branch+PR OK, **MAI merge, MAI direct-main** (policy Eduardo, merge-gate = oversight).
- Ogni repo = spec + PR proprio. Triage delivery in chat per repo esterni.

## Out of scope (questo spec)

- Memory consolidation + agents audit (Fase 3, ciclo separato -- scelta Eduardo).
- Root governance files slim (Fase 2).
- Repo esterni (Fasi 4+).
- JOURNAL.md (append-only by design, non si snellisce).
- Modifiche a hooks / settings.json (separato; `update-config` skill se servira).

## Decisioni risolte (2026-06-03, Eduardo)

- **R1**: reference doc nuovi -> **nuova dir `docs/reference/`**. `REFERENCE_INDEX.md` resta
  indice-di-indici e li linka.
- **R2**: commit Fase 1 (parte git) -> **branch `claude/context-files-reorg-2026-06-03`
  (worktree-isolato) + PR + auto-merge autorizzato** dopo verifica verde (no-loss + line-count
  + behavior smoke).
- **R3**: esecuzione -> **piano scritto prima** (writing-plans) con checkpoint di review.
- **R4** (split deploy): parte non-git (`~/.claude/` global + reference + rules) = edit Lenovo
  diretto + backup `.bak`; **deploy-parita su Ryzen = follow-up flaggato**, non auto in questa sessione.
  Identita confermata: PC=CODEMASTERDD / edusc = Lenovo canonical.
