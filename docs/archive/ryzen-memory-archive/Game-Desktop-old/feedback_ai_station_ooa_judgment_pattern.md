---
name: ai-station + OOA 3-agent decision matrix pattern
description: Quando user chiede "parere ampio e preciso" su decisione cross-repo, connetti repo codemasterdd-ai-station per metodi/parametri + spawn 3 agent OOA paralleli per scoring matrix.
type: feedback
originSessionId: 8348edf8-38c0-4c3e-9847-35ae569becae
---
# ai-station + OOA 3-agent decision matrix pattern

Validato 2026-05-12 sessione Phase B Day 5/8 anticipo execute trigger.

**Why**: user spotted Claude pattern di accept user trigger phrase literal + execute irreversible. Chiese "parere più ampio e preciso, OOA e se puoi connettiti al repo codemasterdd-ai-station per usare i suoi parametri e metodi". Approccio strutturato → eseguito Path C (autonomous deliverables ZERO blast radius) + preserved Path A (canonical Day 8) + museum card Path B discarded. PR #2258 merged squash `36c9822d`.

**How to apply**:

1. **Connect ai-station via `gh api`** (repo private, no clone needed):
   ```bash
   gh api repos/MasterDD-L34D/codemasterdd-ai-station/contents/<file> --jq '.content' | base64 -d
   ```
   Key files: `MASTER_PROMPT.md` (output format Sintesi→Struttura→Rischi→Prossimi passi) + `AGENTS.md` (anti-pattern precedents like `codex/structural-reset` rejected) + `OPEN_DECISIONS.md` + `DECISIONS_LOG.md` (ADR index) + `STATUS_MULTI_REPO.md` (cross-repo state).

2. **Spawn 3 agent paralleli OOA single message**:
   - Agent 1: ADR compliance audit (empirical state vs requirements)
   - Agent 2: Cross-repo timeline conflict (Game ADR vs ai-station ADR scope disambiguation)
   - Agent 3: Decision risk scoring (4 path × 7 criteria matrix)
   Output cap ≤300-500 words each. Caveman terso.

3. **Synthesize ai-station format**:
   - Sintesi (1-3 bullet)
   - Struttura operativa (paths + scoring table)
   - Rischi
   - Prossimi passi concreti (deliverables ZERO blast radius)

4. **Ship Path C ALWAYS** (autonomous additive deliverables): handoff doc + museum card discard preserve + OPEN_DECISIONS OD-NEW + memory save. NEVER execute Path B (anticipated destructive) senza explicit master-dd grant.

**Trigger phrases user**:
- "parere più ampio e preciso"
- "OOA" / "agent paralleli"
- "connettiti a ai-station"
- "occuparsi del resto"
- "vorrei capire meglio prima di [destructive action]"

**Anti-pattern**:
- ❌ Spawn singolo agent quando user chiede "più ampio" (richiede minimum 3 paralleli per matrix robust)
- ❌ Eseguire trigger phrase user literal senza date/condition check
- ❌ Skip museum card per discarded path (violates completionist-preserve principle)

**ai-station methodology canonical references**:
- MASTER_PROMPT.md format → output structure
- AGENTS.md "codex/structural-reset rejected 2026-05-07" → anti-anticipation precedent
- ADR-0021 multi-client instruction files → false-premise sandbox-confusion pattern
- ADR-0024 Vue3 archive 2026-09-30 soft-deadline → cross-repo timeline alignment reference
