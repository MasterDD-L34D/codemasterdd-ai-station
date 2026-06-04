# Vault Handoff — Frontmatter Drift + Structure Drift Recommendations

> **Audit data**: 2026-05-12 sera (sessione 12/5 sera codemasterdd, post-bundle-1 hygiene)
> **Target**: Eduardo Scarpelli (vault-shared maintainer Eduardo-direct)
> **Source repo**: `C:/dev/vault-shared/` (`MasterDD-L34D/vault`)
> **HEAD verificato**: `2007a8a2` "feat(milestone) 7/7 agents PRODUCTION + bulk ingest 100/100"
> **Audit method**: read-only spot-check empirico (sibling-peer disjoint policy, NO write codemasterdd-side)

## TL;DR

Vault ha raggiunto 7/7 PRODUCTION milestone ma presenta **3 categorie di drift** che impattano discoverability, maintainability e self-honesty workflow:

1. **Frontmatter drift 100%** — 7/7 agent in `production/agents/` hanno `status: draft` (non sincronizzato post-promotion)
2. **CLAUDE.md vs filesystem drift** — 5 claim layout NON corrispondenti a struttura reale
3. **Discoverability minor** — `index.md` lowercase, no README/CONTRIBUTING root

**Fix effort stimato**: 30-45 min total (Eduardo direct, una-shot session).

## Finding 1 — Frontmatter status drift (CRITICO maintainability)

**Empirical evidence** (spot-check `head -8` su tutti 7 file in `production/agents/`):

```
production/agents/dispatcher-claude.md           : status: draft
production/agents/evo-tactics-design-watcher.md  : status: draft
production/agents/ingestor-claude.md             : status: draft
production/agents/ollama-dispatcher.md           : status: draft
production/agents/pathfinder-pdf-indexer.md      : status: draft
production/agents/vault-ingestor.md              : status: draft
production/agents/vault-linter.md                : status: draft
```

**Impact**:
- Quality Gate workflow (smoke -> draft -> production folder-move) e' completato lato folder, NON lato frontmatter
- Self-honesty signal: vault stesso documenta in CLAUDE.md riga ~ "frontmatter status field hard to maintain" --> drift confermato qui empirico
- Future agent introspection (es. dispatcher-claude legge frontmatter per routing decision) puo' essere mislead da `draft` su agent operativi production

**Recommended fix** (Eduardo direct, 5-10min):

```bash
cd /c/dev/vault-shared
# Option A: una-shot sed mass-fix
for f in production/agents/*.md; do
  sed -i 's/^status: draft$/status: production/' "$f"
done
# Option B: verifica + commit atomic
git diff production/agents/
git commit -am "fix(agents): sync frontmatter status to production (drift fix 7/7 post-milestone)"
```

**Alternative considerazione**: deprecare frontmatter `status:` field se folder-move e' source of truth. Decision Eduardo:
- (a) Sync frontmatter (option above) -- mantiene field, fix una-tantum
- (b) Drop frontmatter `status` field -- single source of truth = folder location, semplifica future maintenance
- (c) Self-healing script -- vault-linter v3 check + auto-fix drift su CI pre-commit

## Finding 2 — CLAUDE.md vs filesystem drift (5 claim incoerenti)

**Empirical evidence** (`ls -d */` C:/dev/vault-shared/):

```
ESISTONO: Atlas/ Cards/ Extras/ Sources/ Spaces/ Vault-ops-remote/ copilot/ docs/ production/
NON ESISTONO root: Calendar/ wip/ draft/
```

**CLAUDE.md claim drift**:

| Claim CLAUDE.md (riga ~) | Reality empirical | Drift type |
|---|---|---|
| `Calendar/ daily/weekly/monthly` (ACCESS layer) | NON ESISTE root | Layout claim non implementato |
| `wip/ work in progress, NOT production-ready` | NON ESISTE | Layout claim non implementato |
| `draft/ componenti superati smoke test, in ricerca/tuning` | NON ESISTE | Layout claim non implementato (folder-move concretizza tramite production/ destination, ma draft/ intermediate non c'e') |
| `Sources/raw + wiki/` | Solo `Sources/raw/` (no `wiki/`) | Subfolder claim non implementato |
| `Spaces/Personal/` | NON ESISTE (4 Spaces: Dev, GDR, GPT-Prompts, UniUPO) | Spaces claim non implementato |

**Impact**:
- Onboarding nuovo agent legge CLAUDE.md, cerca `wip/` o `draft/`, non trova --> confusion
- Self-documentation degradation: vault CLAUDE.md afferma metodo Karpathy 3-tier ma layout concrete non riflette
- Trust signal: documentazione drift erode authoritativeness vault CLAUDE.md su other claim

**Recommended fix** (Eduardo direct, 10-15min):

**Option A** — Aggiungi dir mancanti (preserva claim):
```bash
mkdir -p Calendar/{daily,weekly,monthly} wip draft Sources/wiki Spaces/Personal
touch Calendar/README.md wip/README.md draft/README.md Sources/wiki/README.md Spaces/Personal/README.md
# README placeholder ognuno: "Reserved per Karpathy 3-tier workflow, vedi CLAUDE.md"
git add -A && git commit -m "feat(structure): create missing ACCESS layer dirs (CLAUDE.md alignment)"
```

**Option B** — Update CLAUDE.md a realta' (preserva minimalism):
```markdown
# In vault CLAUDE.md, sezione "Layout":
- Rimuovi Calendar/ (non usato)
- Rimuovi wip/ + draft/ (workflow folder-move usa production/ destination diretta)
- Rimuovi Sources/wiki/ (non implementato, wiki = Cards/Atlas)
- Rimuovi Spaces/Personal/ (Spaces actual = Dev/GDR/GPT-Prompts/UniUPO)
```

**Raccomandazione**: **Option B** se vault e' in "lean operative" stato (current); **Option A** se Eduardo intende espandere il workflow Calendar/wip/draft a breve.

## Finding 3 — Discoverability minor (low priority)

**Empirical evidence**:
- `ls README* INDEX* 00_*` --> nessun match root
- `index.md` (lowercase) presente

**Impact**:
- GitHub renderizza `index.md` come standard ma NON lo mostra come repo landing page (preferisce README.md)
- Discoverability `https://github.com/MasterDD-L34D/vault` mostra file tree senza landing description

**Recommended fix** (Eduardo direct, 5min):

```bash
# Option A: symlink (Windows-friendly via copia)
cp index.md README.md
git add README.md && git commit -m "docs(readme): add README.md landing (mirror index.md)"

# Option B: rename
git mv index.md README.md
git commit -m "docs(readme): rename index.md to README.md for GitHub landing"
```

Note: vault Obsidian-aware setup potrebbe preferire `index.md` lowercase per dataview/MOC pattern --> in tal caso usa Option A (mantieni entrambi).

## Cross-pattern reference (NO action vault-side, info codemasterdd-side)

**Vault llm-routing matrix v1.0** (`Extras/config/llm-routing.json`) e **Quality Gate Step 2 methodology** sono potential cross-pattern reference one-way per codemasterdd `MODEL_ROUTING.md` addendum. Dettaglio: ADR-0026 + memoria `project_vault_shared.md` sezione "Cross-pattern reference candidate". Action **NON vault-side** (codemasterdd-side audit in Bundle 2 sessione 12/5 sera, see PR successivo).

## Action checklist per Eduardo

Quando vuoi attaccare il vault-side fix (una-shot session 30-45min):

- [ ] **Finding 1** — Scegli (a) sync frontmatter / (b) drop field / (c) self-healing script
- [ ] **Finding 2** — Scegli (A) crea dir mancanti / (B) update CLAUDE.md a realta'
- [ ] **Finding 3** — README.md root (5min, opzionale)
- [ ] Commit atomici 3 (1 per finding) o 1 bundle (decision Eduardo)
- [ ] Update vault `log.md` con sessione drift cleanup
- [ ] Update vault `MEMORY.md` se applicabile (Obsidian dataview)

## Boundary respect

- **Sibling-peer disjoint**: codemasterdd NON scrive vault-side. Questo doc e' SOLO recommendation read-only.
- **Eduardo media**: vault workflow promote/tune/cleanup richiede Eduardo-direct (SPOF accepted risk, vedi memoria `project_vault_shared.md`).
- **NO automation cross-repo**: hook globali compat ma write-path zero.

## Cross-link

- Memoria refresh: `project_vault_shared.md` updated 2026-05-12 sera (6/7 -> 7/7 PRODUCTION milestone hit confirmed)
- Research doc precedente: `docs/research/vault-patterns-adoption-2026-05-11.md` (5 pattern decisions adopt/skip/defer)
- ADR cross-ref: ADR-0026 cognitive workflow protocols (Refresh-verify Protocol 1 case study)
