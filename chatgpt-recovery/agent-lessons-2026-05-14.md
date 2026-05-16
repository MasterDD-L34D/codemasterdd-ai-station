# Agent Lessons -- ChatGPT Recovery Operation 2026-05-14

Captured during real-task invocation of 3+ untested specialized agents on the chatgpt-recovery pipeline. Use for future agent-selection decisions + Protocol 5 (harsh-reviewer cluster scrutiny) calibration.

---

## Methodology

3 agent lanciati in parallelo su scope reale:
- `harsh-reviewer` (quality review)
- `owasp-security-auditor` (security review)
- `adr-drafter` (governance ADR creation)

Brief prompts: ~400-600 parole ognuno, con scope esplicito + file paths + threat model + format atteso (sotto N parole, severity-ranked, cita file:line).

Costo: ~$0.30-0.50/agent stimato (~85K token harsh, ~70K owasp, ~70K adr) — tutti sotto cap $20/mese ADR-0023.

---

## Agent 1: `harsh-reviewer`

### Output quality: 🟢 ECCELLENTE

**Findings real**:
- 4 P0 reali identificati (atomize.py hardcoded threshold, role filter, classify threshold, orchestrator blocking Read-Host)
- 11 P1 (multi-root mapping, Ollama timeout, race condition)
- 9 P2 maintainability
- **Cita file:line precisi** (es. `atomize.py:135-137`, `classify.py:467-469`)
- Domande pertinenti a Eduardo (3) per priority decision
- TLDR + "net verdict" + "top 3 next actions" finale

**Cosa ha catturato che NON avrei trovato da solo**:
- `atomize.py:135` hardcoded 40 char threshold redundante con args.min_msg_length (race con orchestrator setting 50)
- `atomize.py:259` role filter logica `not in (...) AND not (X AND not Y)` cognitively impenetrabile (mentre funziona oggi, prossimo refactor lo rompe)
- Multi-root mapping su branched conversations (real risk ChatGPT data)
- BERTopic + zero-vec contamination da Ollama embed failure

**Anti-pattern catturato in me**:
- LLM prompt bias: avevo messo "evo-tactics-balance" come esempio nel prompt LLM labeling → modello copiava letterale (Topic 2 hallucinazione `evo-tactics-discussion` su keywords non-correlati)

### Bias osservato

NESSUN flattery. Identifica "cosa funziona (no flattery)" come sezione separata limited a 4 punti specifici. Tono diretto ("REWORK" come verdict). Apprezzato.

### Quando rilanciarlo

- Cluster >=3 PR same day (Protocol 5 trigger) ✓
- Pre-merge ADR-class implementation
- Pipeline complessa pre-run su dati reali ✓ ← USECASE OGGI
- Cattura race condition + edge case su 5 file in parallelo

### Limitazioni

- Non corre code (no test execution)
- Non legge files concorrenti (race condition derived from prompt context, not observation)
- Suggerisce "Fix direction:" ma non scrive il diff

---

## Agent 2: `owasp-security-auditor`

### Output quality: 🟢 ECCELLENTE

**Findings real**:
- 2 P0 reali (bearer in jsonl transcript — verified via grep, bearer in %TEMP% no auto-expiry)
- 4 P1 (JWT verify warning doc, argv exposure CWE-214, account-id confusion, Playwright auth-state durability)
- 3 P2 (TLS pin, silent error swallow, URL bearer leak verified OK)
- OWASP refs precisi: A02 Cryptographic Failures, A04 Insecure Design, A07 Auth Failures, A09 Logging
- CWE references (CWE-200, CWE-214, CWE-538, CWE-347, CWE-613, CWE-863, CWE-778)

**Cosa ha catturato che NON avrei trovato da solo**:
- Bearer JWT è davvero finito nel session.jsonl transcript (verificato real-time durante review) — threat documentato ma non da me intercettato pre-emergence
- Playwright auth-state durability ortogonale a bearer 10gg lifetime (session cookie ~30gg, different decay)
- Account-id confusion su multi-workspace user (Eduardo ha 1 team + 2 free) come authorization risk

**Bias osservato**:
- Confirmato bias: "architettura solida... gestibili pre-merge" framing initial = un po' di soft opening, MA poi cita issue P0 reali (bearer in trascript = vera P0).
- Severity ranking corretto. No false positives su nostri privacy guard rail (riconosce sovereign-only design come baseline OK).

### Quando rilanciarlo

- Endpoint auth handling (Flask Dafne, Express Synesthesia)
- Secret/token management
- API scraping con session token ✓ ← USECASE OGGI
- Wrapper cloud delegation (Groq/Cerebras with API keys)

### Limitazioni

- Non corre security scan tooling (semgrep, bandit)
- Non testa attacchi reali (penetration test would be next step)
- Threat model deriva dal prompt + context, non da analisi dinamica

### Synergy con harsh-reviewer

Complementari. Harsh-reviewer ha trovato `auto-audit.py:362` JWT sub potentially None → TypeError. OWASP-auditor ha trovato JWT signature non verificata (CWE-347 doc concern). Stesso file, angoli diversi.

---

## Agent 3: `adr-drafter`

### Output quality: 🟢 BUONO

**Output prodotto**:
- File ADR-0030: `docs/adr/0030-chatgpt-recovery-classification-pipeline.md` (Status: Proposed)
- 5 opzioni comparate (A brianjlacy chosen, B pionxzh, C ocombe, D SaaS, E native, F Nexus conseguente)
- Implementation plan 7 step + bearer storage policy esplicita
- 4 mitigations operative (422 bug, BERTopic calibrazione, bearer scaduto mid-export, rollback staging)
- Cross-LLM applicability section per riusabilità futura
- **Updated DECISIONS_LOG retroattivamente**: ha aggiunto righe tabella ADR-0025..0029 mancanti (governance hygiene fix bonus!)
- Updated COMPACT_CONTEXT con counter 24→30

**Cosa ha catturato che NON avrei fatto altrettanto bene**:
- Ratification trigger ESPLICITO ("bulk export run PASS senza errori >5% + classify smoke PASS n=20 plausible clusters")
- Cross-LLM applicability future-proof section
- Governance hygiene bonus: ratecover righe ADR mancanti in DECISIONS_LOG (le 5 righe ADR-0025..0029 esistenti come file ma NON in indice — drift fix)

### Bias osservato

- Output marketing-friendly ("Tutto fatto", "Status: Proposed → trigger esplicito"), MA contenuto solido.
- Format MADR canonical rispettato (verificato leggendo 2 ADR esistenti per match style).

### Quando rilanciarlo

- Nuova decisione architetturale irreversibile/costoso reverse
- Tool selection con multi-option trade-off ✓ ← USECASE OGGI
- Pivot strategico
- Pre-implementation per scope >50 LOC con sub-decisions

### Limitazioni

- Output NON include diagrammi (Mermaid/PlantUML) — solo testo + tabelle
- Non automaticamente accepted (richiede Eduardo ratification step)

---

---

## Agent 4: `privacy-policy-enforcer`

### Output quality: 🟡 MISTO — buone idee + HALLUCINATION P0

**Findings real**:
- PII tag schema proposal solida (frontmatter `pii_tags` + `canonical_audience` flag) — implementabile
- Stratification by sensitivity recommendation (HIGH/MEDIUM/LOW per categoria data) — concettualmente corretta
- Cleanup policy intermediate files — corretta

**HALLUCINATION P0 critica**:
> "**P0 — JWT bearer token in export**: session jsonl contiene JWT per API calls — visible plaintext in export"

Falso. Verificato empirically:
```bash
grep -l "eyJhbGciOi" C:/dev/chatgpt-full-export-2026-05-14/json/ → 0 match
find ... -name "*.json" -exec grep -l "Bearer eyJ" {} \; → 0 match
```

Bearer JWT è SOLO nel mio Claude Code session.jsonl (`C:/Users/edusc/.claude/projects/.../*.jsonl`). I file ChatGPT export `/backend-api/conversation/{id}` response body NON contengono il bearer (è in request header, non response). Agent ha conflated `session.jsonl` (Claude Code transcript) con `conversation JSON files` (ChatGPT export output). False high-confidence claim → proposed script `strip-jwt-from-chatgpt-export.py` è UNNECESSARY.

**Altro mismatch strutturale**:
- Proposed vault structure: `Spaces/hobbies/gdr/`, `Sources/academic/uniupo/`, `Sources/dev/evo-tactics/_design-public/`
- Reality: vault già ha `Spaces/Dev/Evo-Tactics`, `Spaces/GDR/HaoJin`, `Spaces/UniUPO`, `Spaces/GPT-Prompts` (mapped in cross-reference-map.yaml)
- Agent ha proposto NEW structure ignoring existing — overlap-confusion risk

### Bias osservato

- High confidence framing su P0 false positive (no "verify" qualifier)
- Tendenza a proporre NEW infrastructure invece di reconcile con existing
- Buon framework di sensitivity classification ma applicazione poco verificata

### Quando rilanciarlo (lessons learned)

✅ Use when:
- PII classification task (output framework solido)
- Pre-cloud-delegation privacy check (overlap con privacy-guard rail scripts)
- Sensitivity-stratification design su nuovo subsystem

❌ Skip when:
- Existing vault structure to honor (agent proposes NEW)
- Critical assertion → ALWAYS verify empirically before action (hallucination risk)

### Counter-measure pattern

Per agent output con confident claims: regex/grep verification PRE-action su qualunque path/file mentioned. Costo verifica ~10 sec, salva ore di fix di artefatti hallucinated.

---

---

## Agent 5: `Explore`

### Output quality: 🟢 ECCELLENTE

**Findings real**:
- Naming convention vault: kebab-case + collection-prefix + section-slug (con esempi)
- YAML frontmatter standard: 4 field universali (100%) + 5 common (80-100%) + 6 metadata (60-95%)
- Tag taxonomy: `[card, {collection}, raw-collection, section-atomize, {lang}]` baseline
- Wikilink format: `[[../../Sources/raw/{source-path}|{filename}]]` con relative path completo
- MOC convention: `{collection-name}-moc.md` in Atlas/ con frontmatter type:moc + fixed sections
- Atomize.py config implications table (immediatamente actionable)

**Cosa ha catturato che NON avrei intuito da solo**:
- `source_sha256: hex_8` content fingerprint (data integrity check)
- `char_count` metric per Card
- `last_verified` field (audit trail freshness)
- Sezione "ATOMIZE.PY CONFIG IMPLICATIONS" mappa diretto requirements → implementation

### Quando rilanciarlo

- Convention scan su codebase esistente prima di scrivere nuovo content
- Pattern detection across files (frontmatter, wikilinks, MOC)
- Open-ended search >3 queries

### Limitazioni

- Read-only (non scrive update files)
- Output testuale solo, no code-gen direct

---

## Agent 6: `Plan`

### Output quality: 🟢 ECCELLENTE

**Findings real**:
- 8 fasi sequenced con dep graph + estimated time + owner (auto/Ed/mixed)
- Decision points espliciti (6 punti dove Eduardo must intervene)
- Edge case handling (Ollama OOM, qwen hallucinates Italian, multi-root branches)
- Sampling formula stratificata: `sample_size = max(5, ceil(sqrt(topic_doc_count)))` invece di review tutti
- "Done" criteria misurabile (7 condizioni AND)
- Rollback path per ogni stage critico (snapshot vault HEAD pre-stage)
- Cross-LLM reuse pattern (Phase 8 future-proof)

**Cosa ha catturato che NON avrei intuito**:
- **Snapshot vault HEAD pre-staging** come rollback anchor (`git rev-parse HEAD > _meta/pre-stage-vault-head.txt`) — io non avrei pensato a versionare lo stato prima
- **Copy NOT move** da staging a canonical (mantiene audit trail per 30gg)
- **Stratified sampling formula** sqrt-based con confidence-level 95% CI ±5% MoE — analiticamente fondato
- 2 nuovi script da scrivere: `pipeline/sample-cards.py` + `pipeline/promote-cards.py`
- Atlas MOC dedicato: `chatgpt-recovery-2026-05-14-moc.md`
- Git tag `chatgpt-import-2026-05-14` per identificare snapshot import

### Bias osservato

- Time estimates aggressive (90-180m per Eduardo review di 120-180 Cards — realistic? Eduardo's attention budget?)
- Output verbosity ALTA — Plan agent tende a expand. Buono per pianificazione completa, ma TLDR mancante (devo estrarre io)

### Quando rilanciarlo

- Multi-step implementation con >5 phases
- Tradeoff analysis con multiple decision points
- Pre-implementation orchestrator design
- Rollback strategy formalization

### Limitazioni

- Read-only (non scrive script proposti)
- No dry-run validation di assumptions
- Time estimates can be optimistic (must validate empirically)

---

## Lessons consolidate

1. **Agent specialization paga**: prompt brevi (~400-600 parole) con scope + file paths + format → output high-signal. Agent generic-purpose avrebbe richiesto più hand-holding.

2. **Parallel invocation reliable**: 3 agent in parallelo via `run_in_background: true`. Timing: harsh ~112s, owasp ~94s, adr ~178s. Tutti completati senza conflict (read-only su file diversi).

3. **Severity ranking + cita file:line OBBLIGATORIO** in prompt: senza, output è descriptive ma non actionable. Con, posso direct-fix.

4. **Findings da chiedere ESPLICITAMENTE altrimenti agent default-skip**:
   - "Cosa funziona (no flattery)" → bilancia il negative-only bias
   - "Domande per Eduardo" → forza decision points
   - "Top N next actions" → ranking utile per execution

5. **Bias positivo evidente**: tutti e 3 i miei agent-prompt erano abbastanza ricchi di context per ridurre framing ambiguity. Se prompt avesse mancato threat model OWASP, severity ranking sarebbe stato ad-hoc.

6. **Synergy multi-agent**:
   - harsh-reviewer catches IMPLEMENTATION bugs (logic, performance, race)
   - owasp-security-auditor catches THREAT MODEL gaps (token flow, transcript leak)
   - adr-drafter catches GOVERNANCE drift (missing ADR rows in DECISIONS_LOG)
   - Non-overlapping → ROI alto per parallel run

7. **Costo modesto**: ~$1.50 totale per le 3 review (cap $20/mese tier 0 ADR-0023). Soglia P5 Protocol 5 trigger (~$0.30-0.50/invocazione, sotto cap) → invocabile su routine basis senza burden.

---

## Comparative table for future agent picks

| Need | Agent | Trigger |
|---|---|---|
| Pre-merge code review (logic + race + performance) | `harsh-reviewer` | Cluster PR same day, complex pipeline pre-run |
| Auth/token/session security review | `owasp-security-auditor` | Endpoint auth, API scraping, secret handling |
| Architectural decision capture | `adr-drafter` | Tool selection, pivot, irreversible commitment |
| Codebase exploration broad | `Explore` | Open-ended search >3 queries |
| Implementation strategy planning | `Plan` | Multi-step task before touch code |
| Privacy classification | `privacy-policy-enforcer` | Pre-cloud-delegation, mixed-privacy repo |
| Fase 6-7 dogfood pattern analysis | `dogfood-analyst` | Multi-task aggregate review |
| Cross-repo health audit | `repo-health-auditor` | Periodic ecosystem refresh |
| Game balance d20 stats | `game-balance-auditor` | Evo-Tactics balance run |
| Dafne swarm cycles | `swarm-cycle-analyzer` | Deep cycle pattern analysis |
| Vault lore consistency | `lore-consistency-checker` | Cross-reference biome/species/trait narratives |
| Database schema | `database-schema-designer` | Synesthesia/Game schema review |

---

## Tracking entry per BACKLOG/lessons promotion

Questo file → eventualmente promossa in `aa01/learnings/L-2026-05-NNN-multi-agent-parallel-on-recovery.md` se cross-session value emerges. Per ora resta locale al recovery workspace.

Trigger Protocol 5 measurement (ADR-0026 amendment L-016): aggiungo "Cognitive protocols applied: harsh-reviewer Y, owasp Y, adr-drafter Y" al PR finale di chatgpt-recovery (se mergerà in main).
