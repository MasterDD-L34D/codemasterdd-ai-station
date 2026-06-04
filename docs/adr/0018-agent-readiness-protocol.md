# ADR-0018 — Agent readiness protocol (smoke test + ricerca + tuning)

> *TL;DR: Sessione 2026-04-24 ha creato 13 nuovi agent in `.claude/agents/` portando totale a 18. Solo 3 invocati live end-to-end prima del commit. Harsh review + Eduardo hanno identificato che "inventario agent" ≠ "agent ready": scrivere system prompt non valida funzionamento. Nuovo protocollo: **ogni agent richiede 3 gate prima di stato `ready`** — (1) smoke test live con prompt reale, (2) ricerca fonti validate (licenze/attribuzione confermate, nessun pattern inventato), (3) tuning basato sui findings. Agent esistenti retroattivamente riclassificati `draft` fino a passaggio gate. Applicazione forward: pre-commit check sulla creazione di nuovo agent file in `.claude/agents/`.*

- **Status**: **Accepted** (2026-04-24 — dichiarato da Eduardo durante sessione live)
- **Data**: 2026-04-24
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev

## Context and Problem Statement

### Situazione 2026-04-24 post auto-mode session

Session ha prodotto:
- 13 nuovi agent `.md` in `.claude/agents/` (game, dafne, quality, security, db, meta)
- SOURCES.md con attribuzione archivio + TikTok + research esterna
- README.md con tabella invocation pattern

**Verifica effettiva**: solo 3/18 agent invocati live durante sessione:
1. `swarm-cycle-analyzer` — Dafne live snapshot analysis (pattern detection funzionante)
2. `delegation-classifier` — classificazione task real docker-compose fix (ADR-0016 aware confermato)
3. `harsh-reviewer` — critical review del lavoro notturno (output solido 3 blocking + 5 significant)

**15 agent non invocati** = stato `inventory speculativo`:
- game-balance-auditor, game-systems-designer, game-design-validator, lore-consistency-checker (scope Evo-Tactics, 0 task reali durante auto-mode)
- dafne-proposal-triager (scope Dafne, 0 proposte review richieste)
- privacy-policy-enforcer, a11y-wcag-reviewer (Synesthesia dormant → 0 trigger reali)
- owasp-security-auditor, database-schema-designer, compact-conversation (cross-cutting, no task trigger)
- agents originali (dogfood-analyst, bench-reporter, cost-monitor, repo-health-auditor, adr-drafter) invocati indirettamente ma non in questa sessione

### Diagnosi (da harsh-reviewer review 2026-04-24 mattina)

> **"Dei 18 agent, quanti hai invocato in 8h di auto-mode? Se <5, gli altri 13 sono inventory speculativo."**

Pattern identificato: scrivere system prompt dettagliato ≠ validare comportamento real. Gap tipici di agent non testati:
- Path file hardcoded inesistenti nel repo target
- Tool calls che presumono API endpoint non deployed
- Scope creep vs trigger reali (agent fa cose generiche quando serve specifico)
- Guardrail "Cosa NON fare" irrealistici o troppo restrittivi
- Fonti citate in `SOURCES.md` non tutte licensa-verificate (Donchitos example dal harsh review)

### Problema

Senza protocollo, risk continuo di:
- Invocare agent → output inutile → recovery manuale → credit loss
- Invocare agent critico (security, balance) con false-positive → decisione errata
- Attribution claims non verificate → problemi licensing se repo diventa pubblico

## Decision

### Adottare "Agent Readiness Protocol" 3-gate

Ogni nuovo agent file `.claude/agents/<name>.md` deve passare **tutti e 3** i gate prima di essere dichiarato `ready` in README.md:

#### Gate 1 — Smoke test live (required)

Invocazione reale dell'agent via `Agent` tool con:
- **prompt rappresentativo**: no hello-world, caso d'uso primario documentato nel frontmatter `description`
- **data source reale**: se agent deve leggere `C:/dev/Game/data/`, test su data effettivi
- **verifica output**:
  - format conforme al sistema prompt output template
  - contenuto plausibile (no hallucinated file paths, no phantom references)
  - runtime accettabile (haiku <20s, sonnet <60s, opus <120s per task tipico)

Criterio PASS: **1+ invocazione produces output usable senza correzione manuale**.

Documenta smoke test in commit message o `docs/superpowers/tests/<agent>.md` (1 riga OK: "YYYY-MM-DD: smoke test PASS, prompt=... output=...").

#### Gate 2 — Ricerca validation (required)

Review `SOURCES.md` entry per l'agent:
- **Licenza fonti**: verificare che ogni repo/skill/framework citato sia MIT/Apache/CC0/BSD-3 o equivalente permissive. Flag esplicito se ELv2, AGPL, GPL, CC BY-NC-ND.
- **Pattern validity**: se pattern deriva da archivio/TikTok, confermare il pattern esiste nella fonte citata (no invention).
- **Framework actual**: se cita framework/tool, verificare attivo 2025-2026 (not abandoned).
- **Findings update**: se research outdated (>3 mesi), refresh prima di dichiarare ready.

Criterio PASS: **attribuzione confermata, zero fonti flagged problematic**.

#### Gate 3 — Tuning iterativo (required)

Dopo smoke test, applicare minimo una iterazione di refinement basata sui findings:
- **Prompt adjustments**: sezioni riduntanti rimosse, nuovi edge case documentati
- **Scope narrowing**: se agent fa cose out-of-scope durante smoke test, aggiungere guardrail
- **Model tier review**: se haiku-assigned agent non basta (es. reasoning esteso), promoverlo; se opus-assigned è overkill, retrocederlo
- **Integration check**: se agent deve orchestrare con altri agent/tool, documentare flow handoff in README matrix

Criterio PASS: **agent rilasciato con almeno 1 commit di tuning post-smoke-test**.

### Applicazione retroattiva (agent pre-2026-04-24)

I 18 agent esistenti sono **riclassificati `draft`** nel README fino a passaggio gate. Priorità:

**Tier 1 — P0 (da validare entro 2 settimane)**:
Agent critici per Fase 6 + Fase 7 transition.
- `owasp-security-auditor` (security critical)
- `privacy-policy-enforcer` (pre-delegation gate)
- `harsh-reviewer` ✅ GATE 1 PASS (sessione 2026-04-24 mattina)
- `delegation-classifier` ✅ GATE 1 PASS
- `swarm-cycle-analyzer` ✅ GATE 1 PASS

**Tier 2 — P1 (validare opportunistic, entro 4 settimane)**:
- `game-balance-auditor`, `game-systems-designer`, `game-design-validator` (trigger = Eduardo apre Game repo)
- `dafne-proposal-triager` (trigger = Dafne propone nuovi agent)
- `database-schema-designer` (trigger = schema work Synesthesia/Game)
- `compact-conversation` (trigger = fine sessione lunga)
- `lore-consistency-checker` (trigger = swarm → Game integration)

**Tier 3 — P2 (validare solo a trigger reale)**:
- `a11y-wcag-reviewer` (Synesthesia dormant fino agosto)
- agents originali Fase 6 (dogfood-analyst, bench-reporter, cost-monitor, repo-health-auditor, adr-drafter) — invocati storicamente ma serve passaggio formal gate per consistency

### Applicazione forward

Ogni volta che si crea un nuovo agent `.md`:

1. **Commit iniziale**: agent file con frontmatter e body, status `draft` in README
2. **Commit gate 1**: smoke test log + finding (anche "output correct" brevissimo)
3. **Commit gate 2**: SOURCES.md entry validata, licenze confermate
4. **Commit gate 3**: tuning iteration, README status → `ready`

Ogni commit può contenere refinements multipli — il separation serve solo per audit trail.

**Anti-pattern**: creare 5+ agent in un solo commit senza passare gate per nessuno. Il pattern 2026-04-24 (13 agent in 1 commit) è **no-go forward**.

## Options considered

### Opzione A — 3-gate readiness protocol (scelta)

Formalizza quello che un agent maturo richiede realistically + applica anche retroattivamente.

**Pro**:
- Riduce false-positive quando agent invocato
- Allinea credito development con invocation history reale
- Attribution onestà (licensing audit)
- Retrofix senza deletion massive (tutti gli agent restano, solo stato diverso)

**Contro**:
- 15 agent da validare = ~4-8h cumulative di smoke test iniziali
- Richiede discipline forward (no shortcut)

### Opzione B — Delete non-invoked agent, ri-creare on-demand

Rimuovere i 15 agent non invocati, riscrivere quando serve.

**Pro**: inventory matches reality 1:1
**Contro**: perdita asset (lavoro 4h per i 13 nuovi), pattern "scrivere agent" richiede di nuovo stesso tempo ogni volta

**Verdict**: troppo aggressivo. Opzione A è più graduale.

### Opzione C — Status quo (no policy)

Accetta che agent sono "documentazione executable" senza obbligo test.

**Pro**: nessun overhead
**Contro**: ignora problema identificato, rischio continuo false-confidence

**Verdict**: scartata — contraddice direttiva esplicita Eduardo.

## Consequences

### Positive

- **Agent trust matrix** chiara: `ready` vs `draft` visibile in README
- **Ordered invocation**: quando serve agent per task, priorità a `ready`. Se solo `draft` disponibile per quella categoria → validation prima di invoke critica OR fallback a Claude Code direct
- **Licensing compliance**: Gate 2 audit previene contaminazione se repo diventa pubblico
- **Sessione auto-mode forward**: no più produzione massive agent senza validation

### Negative

- **Time overhead**: 4-8h di smoke test validation per backlog esistente
- **Decision friction**: se serve agent nuovo urgente durante session → non può essere ready subito (almeno 3 commit)

### Mitigations

- **Gate 1 smoke test template**: documentato in `.claude/agents/SMOKE_TEST_TEMPLATE.md` per ridurre setup time ogni agent
- **Gate 2 license quick-check**: grep awk su SOURCES.md per flag AGPL/NC licenses rapidi
- **Forward exemption**: agent di emergency (es. incident response) possono skip gate 3 tuning se gate 1+2 PASS e uso 1-shot documentato → status `draft-emergency` temporary

## Related

- **ADR-0010** — MADR format + skill install policy (questo ADR estende): preview + ADR per skill now + readiness gate per agent
- **ADR-0017** — UI + observability stack (scope agent dogfood-ui orchestration)
- **Harsh review 2026-04-24**: primary trigger per questa policy

## Notes

### Ratification

Status **Accepted** immediato (2026-04-24) perché:
1. Eduardo ha dichiarato policy esplicitamente in sessione live
2. No controversial trade-off — tutti gli argomenti contro sono risolvibili con discipline
3. Impact è migliorativo + non-destructive (agent esistenti restano, solo status diverso)

### Metriche success post-adozione

A review settimana 4 (~2026-05-17), verificare:
- N agent passati da `draft` → `ready`: target ≥5 (priorità P0)
- N agent rimossi: preferibilmente 0 (retrofit > deletion)
- N invocazioni nuovi agent: tracked in `logs/aider-delegation-*.md` o simili
- Qualsiasi invocazione agent che produce output unusable → tracked in `OPEN_DECISIONS` come OD nuovo

### Template smoke test

Creato `.claude/agents/SMOKE_TEST_TEMPLATE.md` con:
- Prompt prescriptive per ogni tipo agent (analyzer / reviewer / classifier / designer)
- Output validation checklist (format, content plausibility, runtime)
- Tuning iteration pattern

### Non-negotiable

- No agent nuovo go `ready` senza smoke test documented
- No `SOURCES.md` claim senza license verification
- No agent senza iteration di tuning post-test
