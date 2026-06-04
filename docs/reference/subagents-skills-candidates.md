# Subagent + Skill candidates — preview-worthy (2026-04-22, est. 2026-05-12)

Catalogo curato post-rivalutazione approfondita del materiale research 2026-04-21. **NON sono installati**. Reference per futuro: se emerge use case reale, passare per `gh skill preview` (ADR-0010) o manual copy in `.claude/agents/` del repo target, audit markdown content prima.

**Estensione 2026-05-12**: 9 repo aggiuntivi triagati post-screenshot OCR di Eduardo (sezione "Wave 2026-05-12 batch evaluation" in fondo). Total catalogo ora: **12 external resources** indicizzati, di cui 3 nella sezione originale + 9 nella wave 2026-05-12. Workflow di adozione: 4 scaffold AA01 **superseded+archiviati 2026-05-17** in `docs/archive/aa01-handoff/archive/` (vedi "Re-decisione 2026-05-17" in fondo — adoption via loop studio→conferma→tuning→apply).

## Subagent Claude Code — da `VoltAgent/awesome-claude-code-subagents` (17.9k⭐)

Subagent sono markdown statici con frontmatter `name/description/tools/model`. Supply chain risk = prompt injection nel system prompt, non RCE. Audit file-by-file prima di installare.

| Subagent | Path | Valore per lo stack | Install via |
|----------|------|---------------------|-------------|
| **code-reviewer** | `04-quality-security/code-reviewer.md` | Review post-Aider su behavior-critical edit; complementa guard rail pre-commit ADR-0008 | Manual copy in `.claude/agents/` repo target |
| **test-automator** | `04-quality-security/test-automator.md` | Scale-up test authoring su Evo-Tactics (710 test) e Synesthesia | Idem |
| **dependency-manager** | `06-developer-experience/dependency-manager.md` | Migrazione Node 22→24 + Python 3.10→3.12 check per Evo-Tactics | Idem |
| **debugger** | `04-quality-security/debugger.md` | Triage errori prima di escalation a Qwen 30B o Claude Pro (riduce costo tier) | Idem |

**Invocazione pattern** (dopo install): `> Use the code-reviewer subagent to review the last commit`

**Skip bulk plugin install** (`voltagent-qa-sec` porta 16 agent, ~60% off-topic). Cherry-pick file singoli.

## Skill — da `alirezarezvani/claude-skills` (12.2k⭐, Aider-compat)

235 skill totali, signal/noise ~40% pertinente per engineering stack vanilla. Autore 1-person project. License MIT.

**⚠️ Finding 2026-04-22**: repo **NON ha struttura `gh skill`-compatibile** standard (`skills/*/SKILL.md`). `gh skill preview` restituisce "no skills found, may be curated list". **Adozione richiede manual clone + run install script** (`./scripts/install.sh --tool claude-code`) che genera structure compatibile. Overhead significativo vs `gh skill install` diretto.

| Skill | Path | Valore | Priorità |
|-------|------|--------|----------|
| **skill-security-auditor** | `engineering/skill-security-auditor/` | **Meta-skill: operazionalizza ADR-0010 `gh skill preview`-before-install**. Scansiona skill per command injection / prompt injection | 🔴 Alta — coerente con security policy |
| **monorepo-navigator** | `engineering/monorepo-navigator/` | Match diretto Evo-Tactics (Node+Python mono, workspaces pnpm/npm) | 🟡 Media — dopo migrazione progetti |
| **dependency-auditor** | `engineering/dependency-auditor/` | Unified `npm audit` + `pip-audit` + license compliance | 🟡 Media — su 22 vuln Evo-Tactics upstream |
| **pr-review-expert** | `engineering/pr-review-expert/` | Blast-radius + coverage delta | ⚪ Bassa — complementa code-reviewer subagent |
| **tech-debt-tracker** | `engineering/tech-debt-tracker/` | Scanner + dashboard debito tecnico | ⚪ Bassa — nice-to-have |

**Caveat Aider conversione**: `./scripts/install.sh --tool aider` produce `CONVENTIONS.md` (rules-flat), **non** SKILL.md nativo. Per workflow hub-delegation (3-tier routing) è lossy. Skill restano utili sia via Claude Code (primary) sia standalone (script Python stdlib).

## Tool — da `affaan-m/everything-claude-code` (140k⭐)

Hackathon-winner, v1.10.0 aprile 2026. Già estratto: AgentShield (commit `be315c9`).

| Tool | Valore | Rischio |
|------|--------|---------|
| **Instincts** (`/instinct-import`) | Estrae pattern da sessioni con confidence scoring → **formalizza ADR empirici** (tipo 0007/0008) in regole auto-richiamate | Basso — autore nativo, bug #148 chiuso |
| **Memory Persistence hooks** | SessionStart/Stop hooks + SQLite state store v1.9 → **automatizza JOURNAL** a fine sessione | Basso — 997 test passing, hook profiles opt-in |
| **Model routing** (`/model-route`, `/harness-audit`) | Codifica dichiarativa tier 7B/14B/30B (ADR-0009) invece di decision-tree mentale | Medio — richiede wiring custom a Ollama |

**Install strategy**: clone repo, `./install.sh typescript` con profile `minimal`, cherry-pick `hooks/` + `instincts/`. **NO** marketplace plugin install.

## Reference esterni — da `hesreallyhim/awesome-claude-code` curator (40k⭐)

Progetti production-ready linkati dalla curator list. Non dal repo stesso.

| Repo | Valore | Quando attivare |
|------|--------|-----------------|
| **[nizos/tdd-guard](https://github.com/nizos/tdd-guard)** | Hook blocca file-ops che violano TDD → estende guard rail globale con layer "behavior-critical edit senza test modificato = block" | Post-migrazione Evo-Tactics (usa test heavy) |
| **[zippoxer/recall](https://github.com/zippoxer/recall)** | Full-text search + resume sessioni Claude Code → context recovery across sessions | Qualunque momento, basso costo setup |
| **[hagan/claudia-statusline](https://github.com/hagan/claudia-statusline)** | Rust + SQLite persistent stats + context progress bar | **Post-19/05/2026** (monitorare consumo Claude Pro / switch a Ollama tier) |

## Hook candidate salvato localmente — `commit-guard.js`

Script 41 righe JS standalone (zero dep) estratto da `rohitg00/awesome-claude-code-toolkit/hooks/scripts/commit-guard.js`. Salvato in `scripts/hooks/commit-guard.js` del repo come asset riutilizzabile.

**Cosa fa**: hook PreToolUse Claude Code — intercetta `git commit -m "..."` eseguito da Claude durante una sessione e valida Conventional Commits (type(scope): description, ≤72 chars, no trailing period, lowercase first word).

**Complementare al guard rail globale**: il guard rail git in `~/.local/share/git-hooks/pre-commit` blocca silent-corruption (ADR-0008) a livello git. commit-guard.js blocca commit malformati a livello Claude Code PreToolUse **prima** che il git commit sia eseguito. Catena difesa:
1. Claude Code: `commit-guard.js` valida messaggio (PreToolUse hook)
2. git nativo: guard rail globale valida contenuto (pre-commit hook)
3. Husky repo-locale (se presente): validazioni policy repo (es. branch block `main`)

**Install quando utile**: aggiungere a `.claude/settings.local.json`:
```json
"hooks": {
  "PreToolUse": [
    { "matcher": "Bash", "hooks": [
      { "type": "command", "command": "node scripts/hooks/commit-guard.js" }
    ]}
  ]
}
```

**Non installato now**: script presente nel repo, hook config NON attivata. Attivare se in sessione Claude Code emergono commit message malformati auto-generati da Aider (pattern già osservato in behavior-critical routing).

## Tool rimandati a trigger specifici

| Tool | Trigger attivazione |
|------|---------------------|
| `GateGuard` (pip install gateguard-ai) | Quando claim "+2.25 quality" viene replicato indipendentemente |
| `Agno framework full` | Quando parte use case "DM AI Evo-Tactics campaign state" (memory semantica + multi-agent) |
| `rohitg00/awesome-claude-code-toolkit` MCP configs | Quando emerge use case MCP reale (K8s, AWS, Figma non previsti ora) |
| `LambdaTest/agent-skills` pytest/mocha | Se adotto skill framework nel workflow (non urgente, test già funzionano senza) |

## Policy install (ricordo da ADR-0010)

1. `gh skill preview <repo> <skill>` → leggi SKILL.md
2. Assess content/author/license/last-commit
3. Match con use case reale (non speculativo)
4. Install via `gh skill install` + 1 riga JOURNAL
5. Se impatto architetturale (hooks, MCP, runtime): ADR dedicato

---

## Wave 2026-05-12 — batch evaluation 9 external resources

**Trigger**: Eduardo screenshot OCR `TOP CLAUDE CODE REPOSITORIES` 12 repo. Verifica MCP/WebSearch identità + stars reali (vs OCR drift). 3 repo (#1, #6, #11) già coperti nella sezione originale sopra — refresh stars+notes inline. 9 repo nuovi triagati qui.

### OCR audit drift (importante per priorità)

| Repo | OCR stars | Stars reali | Drift |
|------|-----------|-------------|-------|
| obra/superpowers | 148k | **~16.6k** | **OCR inflato 9x** — non e' "top tier" come l'OCR suggeriva |
| VoltAgent/awesome-claude-code-subagents | 17.1k | **~8.1-8.5k** | **OCR inflato 2x** — refresh da 17.9k linea 5 del file |
| thedotmack/claude-mem | 49.6k | ~70-75k | OCR -34% sotto |
| forrestchang/andrej-karpathy-skills | 19.3k | ~117-123k | OCR -84% sotto |
| VoltAgent/awesome-design-md | 45.5k | ~74-75k | OCR -39% sotto |

OCR font monospace ha distrorto cifre. Validazione via star-history + GitHub-live 2026-05-12.

### ⚠️ Audit correction 2026-05-12 tardo (PR audit gh API live)

**Tabella OCR drift sopra contiene 3 errori MAJOR** scoperti via `gh api repos/<owner>/<repo>` live 2026-05-12 tardo (post PR #57 merge):

| Repo | PR #57 claim | gh API REAL | Errore PR #57 |
|------|--------------|-------------|---------------|
| **obra/superpowers** | "~16.6k OCR inflato 9x" | **186639 stars MIT 2026-05-12** | **11x SOTTO real** — direction errata: OCR (148k) era PIU' VICINO real (186k) di PR #57 (16.6k). |
| **VoltAgent/awesome-claude-code-subagents** | "~8.1-8.5k OCR inflato 2x" | **19575 stars MIT 2026-04-20** | **2.4x SOTTO** — OCR (17.1k) era effettivamente corretto. Pattern era CRESCITA (+9% Apr 22 -> 12/5) NON drift. |
| **dair-ai/Prompt-Engineering-Guide** | "~58.2k" | **74448 stars MIT 2026-03-11** | -22% off. |

**Root cause**: PR #57 ha usato source secondaria (probabilmente WebSearch cached o star-history page) invece di `gh api repos/<owner>/<repo>` live. Karpathy autoresearch weighting "empirical > documentation" violato.

**License gaps undisclosed PR #57**:
- #5 forrestchang/andrej-karpathy-skills: gh API `license: ?` unknown -> automatic AUDIT-ONLY gate
- #10 anthropics/skills: gh API `license: ?` unknown -> per-skill license verify obbligatoria
- #6 hesreallyhim/awesome-claude-code: `NOASSERTION` non standard -> BOOKMARK con caveat

**Lesson L-2026-05-007** (AA01 learnings/) formalizza pattern "gh API live mandatory PRIMA di stars-based decision".

### Re-decisione preliminare corretta (post audit gh API)

| # | Repo | PR #57 decisione | Re-decisione (gh API corretto) |
|---|------|------------------|---------------------------------|
| #3 obra/superpowers | DORMANT "non top-tier" | **ELEVATE -> INSTALL CANDIDATE high-priority** (REAL 186k MIT = top tier) **→ INSTALLED 2026-05-12 v5.1.0 (Archon CALIBRATE + falsifying experiment 5/5 PASS)** |
| #11 VoltAgent subagents | REFRESH (rationale "OCR drift") | REFRESH (rationale: **crescita +9% Apr 22 -> 12/5**, NO drift) |
| #5 forrestchang | AUDIT-ONLY | AUDIT-ONLY **+ license check obbligatoria PRE-cherry-pick** |
| #10 anthropics/skills | INSTALL selective | INSTALL **GATED** per-skill license verification |
| #6 hesreallyhim | BOOKMARK refresh | BOOKMARK **+ NOASSERTION license caveat** |
| #4 thedotmack/claude-mem | INSTALL (preferito vs #1 Memory subset) | **DEFER post-Archon CALIBRATE 2026-05-12**: 3 blocker -- (a) Bun runtime MISSING (require pre-install separate), (b) H12 hook collision risk (claude-mem 6 hooks lifecycle vs codemasterdd `.claude/settings.json` SessionStart+Stop hooks, dry-run obbligatorio), (c) privacy concern `@anthropic-ai/claude-agent-sdk` dependency = cloud calls Anthropic API per ogni session compression (NON pure local come scaffold claim) |

### gh API live verified (12 repo, 2026-05-12 tardo)

| # | Repo | Stars REAL | License | Last push |
|---|------|------------|---------|-----------|
| 1 | affaan-m/everything-claude-code | 179572 | MIT | 2026-05-12 |
| 2 | shanraisshan/claude-code-best-practice | 52418 | MIT | 2026-05-11 |
| 3 | obra/superpowers | **186639** | MIT | 2026-05-12 |
| 4 | thedotmack/claude-mem | 74880 | Apache-2.0 | 2026-05-11 |
| 5 | forrestchang/andrej-karpathy-skills | 125338 | **?** | 2026-04-20 |
| 6 | hesreallyhim/awesome-claude-code | 43395 | **NOASSERTION** | 2026-04-27 |
| 7 | yamadashy/repomix | 24609 | MIT | 2026-05-11 |
| 8 | gsd-build/get-shit-done | 61572 | MIT | 2026-05-12 |
| 9 | dair-ai/Prompt-Engineering-Guide | **74448** | MIT | 2026-03-11 |
| 10 | anthropics/skills | 132353 | **?** | 2026-05-09 |
| 11 | VoltAgent/awesome-claude-code-subagents | **19575** | MIT | 2026-04-20 |
| 12 | VoltAgent/awesome-design-md | 75778 | MIT | 2026-05-11 |

### Wave 2026-05-12 — categoria A: skills-collection (#3, #5, #10) — refresh #1

`anthropics/skills` ufficiale è **upstream marketplace skills**. Gli altri 3 sono catalog terzi. Cherry-pick = audit individual skill files, NO bulk install.

| Repo | Stars | Path install previsto | Skill candidati high-priority | Audit gate |
|------|-------|----------------------|-------------------------------|------------|
| **anthropics/skills** | ~132k | `~/.claude/skills/<skill>/SKILL.md` | TBD (catalog official ampio, depth-first read README poi cherry-pick) | License Apache/MIT confermare per-skill, autore ufficiale |
| **obra/superpowers** | ~16.6k | `~/.claude/skills/<skill>/` | TBD ("agentic skills framework + software dev methodology"), valutare overlap con `affaan-m/everything-claude-code` Instincts | Author single-maintainer (Jesse Vincent obra), license MIT presumibile — verify |
| **forrestchang/andrej-karpathy-skills** | ~117-123k | NON skills dir — un singolo `CLAUDE.md` derivativo | Audit del CLAUDE.md singolo: confronto vs nostro CLAUDE.md sezione "Cognitive workflow protocols" + "Trigger delega" | Derivative observation Karpathy public talks — citation chain |
| **affaan-m/everything-claude-code** (refresh) | ~163-180k (era 140k Apr 22) | `~/.claude/skills/` + `hooks/` + `instincts/` | **Instincts** + **Memory Persistence hooks** + **Model routing** (già scoperti, vedi sezione "Tool" sopra). Refresh post-19/05 sovereign | Già `be315c9` commit estratto AgentShield. ADR-0023 trigger se Memory Persistence integra `claude-mem` (item #4) |

**Decisione preliminare** (pre-AA01 task A):
- Tier 1 install: `anthropics/skills` selective (1-2 skill match Synesthesia o Game) + `forrestchang/andrej-karpathy-skills` audit-only (no install, lessons learned)
- Tier 2 DORMANT: `obra/superpowers` overlap analysis vs everything-claude-code prima di install
- Refresh #1 in pipeline (sezione "Tool" sopra) — non re-installare ma promuovere Memory Persistence se claude-mem `BOOKMARK`

### Wave 2026-05-12 — categoria B: subagent + memory (#4) — refresh #11

| Repo | Stars | Path install previsto | Use case | Audit gate |
|------|-------|----------------------|----------|------------|
| **thedotmack/claude-mem** | ~70-75k | `~/.local/bin/claude-mem` CLI + SessionStart/Stop hooks in `~/.claude/settings.json` | **Persistente context across session**: cattura + comprime + reinjetta history. Match diretto a problema JOURNAL/COMPACT drift già documentato in lesson L-2026-05-002 | Security: SQLite locale (no network), license MIT confermare. Overlap con `affaan-m/everything-claude-code` Memory Persistence (item #1) — **scelta UNICO sistema**, no doppia memory |
| **VoltAgent/awesome-claude-code-subagents** (refresh) | ~8.1-8.5k (era 17.9k Apr 22 — OCR drift) | Manual copy in `.claude/agents/` codemasterdd | 4 candidati già identificati (code-reviewer, test-automator, dependency-manager, debugger). Refresh: re-audit eventuale crescita catalogo dopo 20gg | Cherry-pick file singoli — già policy attiva |

**Decisione preliminare** (pre-AA01 task B):
- **claude-mem vs everything-claude-code Memory**: scelta esclusiva. claude-mem più dedicato e battle-tested (70k+ stars vs sub-feature di everything-claude-code). Lean A: install `claude-mem` standalone, escludere Memory Persistence di `affaan-m` per evitare doppio store + drift sync.
- Refresh subagent VoltAgent: re-check catalogo per nuovi agent post-Apr 22 (es. GitHub-PR-watcher, ADR-drafter equivalenti — vediamo se collidono con i nostri 18 sub-agent o complementano).

### Wave 2026-05-12 — categoria C: dev-tool (#7, #8)

| Repo | Stars | Path install | Use case | Audit gate |
|------|-------|-------------|----------|------------|
| **yamadashy/repomix** | ~24.6k | `npm install -g repomix` → `~/.npm-global/bin/repomix` (o `~/.local/bin/repomix-pack` wrapper) | **AI-ingestible pack**: comprime repo in singolo file per upload context window. Use case: handoff cross-session quando AA01 master task + 12 sub-entries supera context (esempio: pack `vault-shared/` knowledge in 1 file per session start). Complementare a context compression. | Open-source MIT confermare. Network: solo file I/O locale, no upload. Già provato da community Eduardo? Da verificare in vault-shared cards |
| **gsd-build/get-shit-done** | ~57.5k | Clone read-only (evaluate-only) | "Meta-prompting + context-engineering + spec-driven dev system by TACHES". **Overlap potenziale con AA01 workflow**: preset spec → DRAFT → PROPOSED → SHIP è simile a get-shit-done flow? Audit per cherry-pick pattern, NON sostituire AA01 (Eduardo personal discipline) | Security low (è metodologia + prompt library, no eseguibile critico) |

**Decisione preliminare** (pre-AA01 task C):
- `repomix`: probabile INSTALL diretto (caso d'uso chiaro context-pack handoff)
- `get-shit-done`: BOOKMARK + audit comparativo vs AA01 preset (lesson cross-pattern, niente install — AA01 è già self-governed disciplina personale)

### Wave 2026-05-12 — categoria D: guide-docs + awesome-list + design-resource (#2, #9, #12) — refresh #6

| Repo | Stars | Pattern adozione | Use case | Note |
|------|-------|------------------|----------|------|
| **shanraisshan/claude-code-best-practice** | ~48.8k | Vault Card sovereign (Eduardo media) | Tips/pattern coding agentico — match cross-pattern review vs nostri ADR (0007, 0008, 0016, 0022, 0026). Cherry-pick lessons | NO write-path codemasterdd. Eduardo personal review |
| **dair-ai/Prompt-Engineering-Guide** | ~58.2k | Vault Atlas reference + link in `REFERENCE_INDEX.md` | Guide canonico prompt eng + RAG + agents. Lookup-only, non eseguibile | Manutenuto, multi-author, MIT. Citation chain academic |
| **VoltAgent/awesome-design-md** | ~74-75k | `C:\dev\awesome-design-md-ref\` clone read-only (NON in `~/.claude/`) | DESIGN.md collection da brand systems. **Use case Synesthesia UI**: scaffolding DESIGN.md per views/ (a11y WCAG 2.2 AA gia requirement progetto). Eventuale use anche Game-Godot-v2 visual style | Apache 2.0 presumibile, verify. Read-only reference |
| **hesreallyhim/awesome-claude-code** (refresh) | ~41.6k (era 40k) | Già in sezione "Reference esterni" sopra (line 48-56). Refresh: re-scan curator list per nuovi entry post-Apr 22 | Meta-source navigator | Già usata per individuare tdd-guard, recall, claudia-statusline. Re-audit 6/12 |

**Decisione preliminare** (pre-AA01 task D):
- Tutti BOOKMARK (no install eseguibile)
- Vault Card creation: Eduardo direct (codemasterdd NON scrive su vault-shared — boundary sibling-peer documentato in CLAUDE.md)
- `awesome-design-md` clone in `C:\dev\` se Synesthesia attiva (M5 BACKLOG trigger) o Godot v2 UX phase

### Riepilogo decisioni preliminari (output 4 task AA01)

| # | Repo | Categoria | Decisione preliminare | Path |
|---|------|-----------|----------------------|------|
| 1 | affaan-m/everything-claude-code | skills | **DEFER 2026-05-12** (Memory subset esclusa post claude-mem v13.2.0 INSTALLED. Skill catalog 100+ ha HIGH OVERLAP con superpowers v5.1.0 INSTALLED. Post 1-week monitor superpowers behavior + cherry-pick selective gap-only). | DEFER post-monitor superpowers usage |
| 2 | shanraisshan/claude-code-best-practice | guide | BOOKMARK | vault Card Eduardo |
| 3 | obra/superpowers | skills | **INSTALLED 2026-05-12** (post Archon CALIBRATE + falsifying experiment 5/5 PASS) | `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/` |
| 4 | thedotmack/claude-mem | memory | **INSTALLED 2026-05-12** v13.2.0 (post Archon CALIBRATE PIVOT: 3 blocker auto-resolved -- Bun installed v1.3.13 + hook collision empirical NO conflict (plugin vs project scope separato) + privacy SAME-TIER come Claude Code attuale, NO new exposure) | `~/.claude/plugins/cache/thedotmack/claude-mem/13.2.0/` |
| 5 | forrestchang/andrej-karpathy-skills | skills | **AUDIT-ONLY CONFERMATO 2026-05-12** -- LICENSE file MISSING (gh API verified), default copyright = NO right to clone/install. Lesson via README/CLAUDE.md read inspirational only. | NO install (license blocker) |
| 6 | hesreallyhim/awesome-claude-code | awesome | REFRESH (re-scan curator) | vault Atlas index |
| 7 | yamadashy/repomix | tool | INSTALL | `npm install -g` |
| 8 | gsd-build/get-shit-done | tool | BOOKMARK (no install, audit vs AA01) | vault Card |
| 9 | dair-ai/Prompt-Engineering-Guide | guide | BOOKMARK | vault Atlas + `REFERENCE_INDEX.md` |
| 10 | anthropics/skills | skills | **MARKETPLACE REGISTERED 2026-05-12** as `anthropic-agent-skills`. **NO additional per-skill install required**: skill bundle disponibili nativamente in session via `anthropic-skills:*` namespace (algorithmic-art, brand-guidelines, canvas-design, claude-api, doc-coauthoring, docx, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, webapp-testing, xlsx). Marketplace expose **2 BUNDLE plugins NON per-skill**: `document-skills` (xlsx+docx+pptx+pdf) + `example-skills` (collection ~13 skills). Install bundle plugin = duplicate skill già accessible session = skip default. | Bundle install solo se sandbox/CI senza native skills bundle accessible |
| 11 | VoltAgent/awesome-claude-code-subagents | subagents | **ADOPT-custom 2026-05-17**: REFRESH-re-audit confermò 0 agent generici valgono cherry-pick (tutti redundant vs ~23 nostri / no use-case). MA gap ENGINE-layer Godot reale → creato custom `godot-engine-specialist` (1-file structural seed da VoltAgent `game-developer` MIT injection-clean + specializzazione Godot-4.x originale) | `.claude/agents/godot-engine-specialist.md` |
| 12 | VoltAgent/awesome-design-md | design | BOOKMARK (clone read-only se trigger) | `C:\dev\` clone su trigger |

### Re-decisione 2026-05-17 (loop studio→conferma→tuning→apply, Eduardo-confermato)

| # | Aggiornamento vs final-table |
|---|---|
| 1 | DEFER → **ADOPT scoped**: cherry-pick SOLO `continuous-learning-v2/Instincts` (MIT, gap pattern-mining no-overlap), gated default-OFF, vendored `vault Vault-ops-remote/claude-global/skills/`. Time-gate droppato. |
| 3 | INSTALLED-canon ma **ASSENTE Ryzen** (regola-0) → azione user-CLI `/plugin install superpowers@claude-plugins-official` |
| 4 | DISABLED → **trigger fired**: upstream #19012 CLOSED. Re-eval re-enable pending (verifica fix-in-versione + smoke, NON auto-flip) |
| 6 | REFRESH → studio: parry (Windows-NO=bloccante) + Rulesync (merge-semantics non verif) = **STUDY-MORE parked-with-trigger**; ClaudeCTX=SKIP (overwrite regressione). Cross-PC resta bespoke (§7: no re-architettura non giustificata). |
| 7 | INSTALL → **DONE** repomix v1.14.0 (`npm i -g`, Ryzen 2026-05-17 verificato) |
| 11 | REFRESH → **ADOPT-custom** `godot-engine-specialist` (vedi sopra) |

**Wave-12 scaffold AA01 (A/B/C/D)**: superseded+**ARCHIVED 2026-05-17** → `docs/archive/aa01-handoff/archive/`. Meccanismo adoption corretto = loop studio→conferma→tuning→apply (NON rituale-paste AA01).

**Tracking BACKLOG**: M11-M14 **CHIUSI** (Wave-12 resolved, scaffold archiviati 2026-05-17).
