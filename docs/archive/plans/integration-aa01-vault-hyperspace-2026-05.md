# Integration Roadmap: AA01 + Vault + Hyperspace (May 2026)

> Plan doc per next 2-3 sessioni Claude Code (target completion entro fine SPRINT_02 ~19/06/2026).
>
> **Status**: Proposed 2026-05-11 (sessione closure ritual). Eduardo-approved chat-only, formalizzato qui per stable reference.
>
> **Scope**: 3 obiettivi sequenziati per integrare AA01 come hub orchestrante, controllo/uso read-only Vault sibling-peer, e Hyperspace Pods Phase 1 privacy audit.

---

## Context strategico

**Window operativa**:
- 2026-05-11 (oggi): plan formalizzato, 8gg residui pre-Claude Max
- 2026-05-19: Claude Max expiration
- 2026-05-20 -> ~2026-06-19: SPRINT_02 (sovereign validation, T2/T5/T7 restanti)
- Questo plan: integration roadmap parallela a SPRINT_02 task ufficiali

**Dipendenze sequence**:
```
Obiettivo 1 (AA01 inbox capture) ──┬──> Obiettivo 2 (Vault read-only)
                                   │
                                   └──> Obiettivo 3 (Hyperspace Phase 1)
                                          ^ DEPENDS on Vault lessons (stack overlap Ollama LAN)
```

---

## Obiettivo 1 -- AA01 hub orchestrante (non solo silent driver)

### Stato attuale (2026-05-11)
- AA01 v1.0.0 in `C:/Users/edusc/aa01/` (separato da codemasterdd, NON git)
- Counter task: 1 SHIP (`aa01-001` two-repos-analysis via PR #39) + 1 in progress (`aa01-002` fleet-discovery-pod-design via PR #40, Phase 1+2 done)
- OD-007 capability registry **deferred Three Strikes** (counter 1 completed + 1 in progress, trigger NON attivato perche' nessuna frizione tool selection osservata)
- Pattern usage: reactive a richieste Eduardo, NON proactive lifecycle

### Action concrete next session
1. **Inbox capture proattivo** (zero-friction, no frontmatter):
   - `C:/Users/edusc/aa01/inbox/2026-05-aa01-003-vault-integration-readonly.md`
   - `C:/Users/edusc/aa01/inbox/2026-05-aa01-004-hyperspace-phase-1-privacy-audit.md`
2. **Classify Stage 1 regex** entrambi (`bash scripts/classify.sh inbox/<file>`)
3. **Promote 1 dei 2** a workspace con preset esplicito:
   - Vault: `research-long` (60d timeout, capability adoption study)
   - Hyperspace: `research-long` (60d timeout, deep privacy audit)
4. Iniziare DRAFT in `workspace/<task-id>/DRAFT/` per il task promoted

### Counter Three Strikes implication
- Pre-azione: 1 SHIP + 1 in progress = 2 task
- Post-azione: 2 SHIP candidates + 1 in progress = 3 task (se aa01-003 promoted) o 2 + 2 in progress (se entrambi promoted)
- **Trigger reactivation OD-007 SE**: in aa01-003 o aa01-004 emerge frizione concreta "quale agent uso per Phase X" / "scelgo sempre lo stesso perche' l'unico che ricordo"

### Output atteso
- 2 inbox file capture
- 1-2 workspace task in DRAFT
- Memory `project_aa01_studio.md` aggiornata con counter + task list

### Tempo stimato
30-45 min. NO write su codemasterdd repo, solo `C:/Users/edusc/aa01/`.

---

## Obiettivo 2 -- Vault control & uso (read-only sibling-peer)

### Stato attuale (2026-05-11)
- vault-shared sibling-peer in `C:/dev/vault-shared/` (clonato 2026-05-10)
- 7/7 production agents milestone (2026-05-10): Quality Gate workflow smoke -> draft -> production 3-gate
- LLM routing matrix v1.0 (commit reference path stabile, NO hash citato per drift risk)
- Stack overlap codemasterdd: Ollama LAN + Qwen + deepseek-r1 + Claude variants
- Privacy validato spot-check (sovereign-only: UniUPO + GDR + GPT-Prompts + Dev notes)
- Boundary: NO write-path codemasterdd-side, Eduardo media bidirezionale

### Action concrete next session (AA01 task aa01-003)
1. **Read-only deep dive Phase 1** (workspace/aa01-003/DRAFT/):
   - Leggere `C:/dev/vault-shared/llm-routing.json` completo
   - Leggere docs Quality Gate workflow (smoke/draft/production gate criteria)
   - Leggere 7 production agent prompts (file paths TBD durante session)
   - Identificare metodologia "split metrics + keep_alive + retries + output validation"
2. **Identify 2-3 pattern adottabili** in codemasterdd:
   - Pattern A: methodology MODEL_ROUTING addendum (split metrics)
   - Pattern B: 1 agent prompt adatto a codemasterdd context (es. quality-gate-style)
   - Pattern C: TBR durante research
3. **Decide adopt/skip per pattern** con rationale documented:
   - Cherry-pick policy: pull-when-needed, audit-then-replay, attribution header, NO bulk import
   - Se adopt: identifica file target codemasterdd-side + PR scope
4. **Output**: `docs/research/vault-patterns-adoption-2026-05-NN.md` con tabella decision matrix
5. **Eventuale addendum MODEL_ROUTING.md** in PR separato post-research (NON in stesso commit, mantenere atomic)

### Constraint hard
- **NO clone agent files** da vault → codemasterdd (cherry-pick = read concept, replay implementation se serve)
- **NO write su vault-shared** (boundary memory `project_vault_shared.md`)
- **NO referenziare commit hash vault** in codemasterdd governance (drift risk repo Eduardo-driven, methodology TBR audit)

### Output atteso
- 1 research doc in `docs/research/` con findings + adopt/skip decisions
- Eventuale 1-2 patch PR su MODEL_ROUTING + 1 agent prompt (separate, opzionali)
- Memory `project_vault_shared.md` aggiornata con adoption findings

### Tempo stimato
1-2h. Output = 1 research doc + eventuali patch atomici.

---

## Obiettivo 3 -- Hyperspace Pods Phase 1 privacy audit (NO install)

### Stato attuale (2026-05-11)
- REFERENCE_INDEX EXT-03 + memory `reference_hyperspace_pods.md`
- 4-fase roadmap (research -> audit privacy -> small pod test -> fleet integration)
- Hardware compat OK (RTX 5060 + RTX 4070 SUPER post PR #40 fleet discovery)
- **Privacy AUDIT REQUIRED PRE-install** (hard gate)
- Trigger: Mac mini extension / VRAM 8GB constraint / device pooling family-friends

### Action concrete next session (AA01 task aa01-004, **DOPO** aa01-003 Vault)
1. **Phase 1 privacy audit deep**, 5 ambiti:
   1. **P2P data flow**: cosa transita su libp2p mesh, encryption end-to-end (Noise vs custom?), metadata exposure
   2. **Pod trust model**: chi puo' joinare pod, kick semantics, blacklist, ban revoke, reputation system
   3. **GossipSub messages**: telemetry leak (modelli usati, prompt count, perf metrics)? Channel topics noti?
   4. **Thor backend**: source-available vs Pi MIT FOSS — cosa e' effettivamente reproducible vs closed
   5. **LAN model sharing**: modelli condivisi = leak weights/prompts cross-device? Quale isolation guarantee?
2. **Multi-source synthesis** (feedback `autoresearch_default` 10/5):
   - 3-5 fonti indipendenti (GitHub repo + docs + community discussion + third-party security review se esiste)
   - NO one-shot README "best match"
   - Parallel research embedded come PR #39 pattern
3. **Output**: `docs/adr/0025-hyperspace-pods-privacy-assessment.md` **Proposed** con:
   - 5 findings per ambito
   - **Decision**: GO / NO-GO / CONDITIONAL GO
   - Conditional gate criteri se applicable (es. "GO se Thor backend FOSS verificato + GossipSub e2e encryption")
   - Phase 2 trigger spec (cosa richiede prima di install)

### Constraint hard
- **NO install Hyperspace tools** in questa session (audit-only)
- **NO connect a public mesh** se anche solo per test
- **Privacy gate decision** Eduardo-final (ADR Proposed → Eduardo accept/reject)
- **Multi-source NON one-shot**: feedback `autoresearch_default` enforce

### Output atteso
- 1 ADR-0025 Proposed (deep multi-source synthesis)
- Decision tree Phase 2 trigger
- Memory `reference_hyperspace_pods.md` aggiornata con audit findings

### Tempo stimato
2-3h. Output = 1 ADR + decision tree.

### Risk flag Claude Max window
- Multi-source synthesis = capability strategic (Tier 0 ADR-0023). Idealmente entro 19/05 con Max attivo
- Se deferred post-Max: usare strategic tier on-demand budget cap ($10-20/mese)
- Decision: NON deferred a budget-paid se possibile completare entro 19/05

---

## Sequenza consigliata (calendario)

### Next session #N+1 (lean, ~1.5h)
- Obiettivo 1 (45min): AA01 inbox capture 2 task + classify + promote 1 (Vault aa01-003 primo)
- Obiettivo 2 Phase 0 (45min): Vault read-only deep dive parziale, draft initial findings

### Session #N+2 (~2h)
- Obiettivo 2 completion: research doc + decision adopt/skip pattern + eventuali PR atomiche

### Session #N+3 (~3h, target entro 19/05)
- Obiettivo 3: Hyperspace Phase 1 privacy audit + ADR-0025 Proposed

### Dipendenza esplicita
Hyperspace audit DEPENDS on Vault integration completion (Vault stack overlap include Ollama LAN — pattern simile a quello che Hyperspace abilita su P2P). Lessons da Vault read-only adoption informano Hyperspace privacy gate.

---

## Definition of done

- [ ] 2 AA01 task formali in workspace o archived SHIP (aa01-003 + aa01-004)
- [ ] 1 research doc Vault patterns adoption con decision matrix
- [ ] 1 ADR-0025 Hyperspace privacy assessment Proposed (Eduardo decide accept/reject)
- [ ] Eventuali patch atomiche MODEL_ROUTING / agent prompts post Vault research (opzionali)
- [ ] Memory updates: project_aa01_studio + project_vault_shared + reference_hyperspace_pods
- [ ] OD-007 counter re-evaluated (Three Strikes trigger check post 2 task in piu')

---

## Trigger fallimento / pivot

- **Vault read-only ostacolo**: se Eduardo non disponibile per chiarire pattern ambigui → skip + memory note "Vault Phase 1 incomplete, fonti TBR"
- **Hyperspace audit NO-GO finale**: documenta motivo in ADR-0025 + memory aggiornata + sostituisce con scenario Mac mini standalone (ADR future)
- **Hyperspace audit CONDITIONAL GO**: Phase 2 trigger criteri esplicit + Eduardo decide se procedere
- **Three Strikes OD-007 trigger DA aa01-003/004**: se frizione tool selection emerge → riapri OD-007 + valuta capability registry MVP

---

## Note operative

- AA01 capability registry feature (OD-007) **DEFERRED** -- non implementare durante questo roadmap (Three Strikes governance)
- Repo write boundary respect: codemasterdd OK (own repo), vault-shared NO write, hyperspace NO install
- Privacy guard rail H8 ADR-0023: vault NOT whitelisted → aider-* wrapper auto-abort se delegation tentata (atteso, validato 10/5)
- Stop hook H12 (fix in v18 PR #41): SessionStart prossima dovrebbe creare marker `.claude/.session-start-head` -- verifica empirica next session
