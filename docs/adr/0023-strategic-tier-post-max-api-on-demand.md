# ADR-0023 — Strategic tier post-Max: Claude API on-demand con budget cap

> *TL;DR: post-19/05/2026 Claude Max OAuth scade. Strategic tier (multi-file refactor / debug architetturale / ADR draft / synthesis cross-source) e' NON-delegabile (ADR-0008). Senza Pro $240/anno acquisito (Scenario A full-sovereign confermato in ADR-0015), strategic tier necessita fallback formalizzato. Decisione: **Claude API pay-per-use on-demand con budget cap mensile $10-20** tracciato in ccusage. Quando emerge task strategic complesso (multi-file ≥3 OR constraint ≥5 OR debug architetturale), Eduardo autorizza spend per quella sessione esplicitamente, poi torna sovereign. Trigger reactivation Pro condizionale: se utilizzo medio API >$20/mese per 2 mesi consecutivi -> ratification ADR-0023 addendum revisita Scenario A vs B (Pro $240/anno = $20/mese effective, costo orario uguale ma flat-rate predicibile).*

- **Status**: **SUPERSEDED-by-ADR-0030 2026-05-18**. Premessa "Senza Pro $240/anno acquisito (Scenario A)" e' **factualmente morta**: ADR-0030 (Hybrid A1, Accepted 2026-05-18) ha acquisito Pro $20/mo. Lo strategic-tier-fallback non e' piu' "Claude API on-demand senza Pro" ma e' coperto dalla Pro subscription Hybrid A1. Questo ADR resta come reasoning storico; routing strategic -> vedi ADR-0030. (era: Proposed 2026-05-09, premise-falsificata caught retrospective B1 2026-05-18.)
- **Data**: 2026-05-09 (originale) / 2026-05-12 sera (empirical refresh)
- **Decisore**: Eduardo Scarpelli
- **Tipo decisione**: budget + workflow tier 0 strategic post-19/05 expiration

## Empirical refresh 2026-05-12 sera (re-eval calendarizzati Eduardo "procedi con metodo")

Evidence empirical raccolta cluster session 12/5 sera (5 PR codemasterdd + 4 vault commits) ha **rafforzato** il razionale ADR-0023 H7:

### Evidence 1 -- Claude Code usage intensivo pre-Max (49 PR/6gg)

Cumulative 2026-05-07 -> 2026-05-12 = **49 PR codemasterdd 7-12/5** + 4 vault commits via Claude Code Max. Media ~8 PR/gg con quality high (governance + research + bundles + lessons + ratification). Empirical = **Claude Code session quality e velocita' sono daily-driver core**, NON luxury.

### Evidence 2 -- Lessons cumulative high-leverage requirono Claude Code

12 lessons (L-001 + L-002..L-012) cumulative methodology framework. Specifically:
- **L-006 Karpathy autoresearch + Archon CALIBRATE methodology** -> synthesis cross-source emerged via Claude Code session 12/5 pomeriggio
- **L-008 plugin install Archon + falsifying experiment** -> Protocol 3 Archon application richiede Claude Code reasoning quality
- **L-009 Archon DEFER -> PIVOT pattern** -> high-stakes decision pattern via Claude Code reflexive
- **L-010 Reflexive methodology audit** -> Bundle 2 B4 ADR-0026 effectiveness audit (cite count + density gerarchia + 3 caso studi)
- **L-012 Vault sibling-peer write boundary override** -> Eduardo authorization pattern + sistema classifier final authority

Tutti pattern high-stakes emerged via Claude Code quality reasoning, NON tier sovereign (Aider single-file + OpenCode multi-step tool calls). Empirical = **post-Max friction concreta** se NO tier 0 strategic on-demand.

### Evidence 3 -- Plugin ecosystem MAJOR upgrade (NEW dimension)

3 plugins (compass + superpowers v5.1.0 + claude-mem v13.2.0) installati 12/5 = NEW operational layer:
- Skill auto-trigger (superpowers 14 skills) functioning ANCHE post-Max (plugin scope independent da Max subscription)
- claude-mem 6 hook lifecycle persistent cross-session ANCHE post-Max
- compass project-direction tracking ANCHE post-Max

Plugin ecosystem ATTENUA friction Claude Code post-Max ma NON elimina need per tier 0 strategic. Synergy: plugins layer continuativo + Claude API on-demand budget cap $10-20 = balance ottimale.

### Conclusion empirical refresh

ADR-0023 H7 setup **RAFFORZATO 2026-05-12 sera**. Empirical evidence:
- Usage intensivo Claude Code pre-Max = 49 PR/6gg
- 12 lessons cumulative pattern high-leverage = need tier 0 strategic
- Plugin ecosystem NEW operational layer attenua ma NON elimina need

**Action H7**: invariato (Eduardo-direct ~5min Anthropic Console pre-19/05). Trigger reactivation Pro $240/anno mantained: utilizzo >$20/mese 2 mesi consecutivi -> addendum revisita Scenario A vs B.

**Ratification check date**: ADR-0023 entro 2026-06-08 (30gg post Proposed 2026-05-09). Empirical refresh oggi (3gg post Proposed) supporta ratification anticipata SE Eduardo decide -- soft-default Accepted con empirical evidence Bundle 4 cluster questa sessione.

## Context and Problem Statement

Harsh review flow chart 2026-05-09 (`docs/reviews/flow-chart-harsh-review-2026-05-09.md`) ha identificato **vulnerabilita' BLOCKING V1**: tier 0 strategic post-19/05 e' un buco nero non risolto.

### Stato corrente (pre-19/05)

- **Strategic tier** (ADR-0008): multi-file refactor / debug architetturale / ADR draft / synthesis cross-source = NON-delegabile a Aider/OpenCode/Ollama. Validato empirically 2026-04-21 (test ADR-0009 generation): delega 7B produce quality D+, rewrite completo richiesto, hub overhead +25-40% token vs direct Claude.
- **Constraint count >=5 strict** (ADR-0016 Proposed): cloud 70B degrada ~20% compliance. Pattern attuale: ritorno a Claude direct per quei task.
- **Claude Max OAuth attivo** fino 2026-05-19 (hard date). Tutti i task strategic vengono fatti da Claude Code Opus 4.7 senza budget concern marginale.

### Gap post-19/05

ADR-0015 ha confermato **Scenario A full-sovereign $0-50/anno**:
- Claude Pro $240/anno NOT acquisito
- Pro declassato (quality parity 70B cloud / 14B Q2 locale)
- Fase 8 sovereign steady state da 2026-05-20+

Ma Scenario A **NON copre esplicitamente strategic tier**. Implicito: "Eduardo lo fa a mano". Realta':
- Multi-file refactor 5+ file con cross-reference: tempo Eduardo 4-8h, vs Claude direct 30-60min
- Debug architetturale: richiede synthesis cross-codebase + reasoning cumulative
- ADR draft con MADR format + 4 opzioni considerate + decision rationale: ~2h Eduardo + iterazione, vs Claude direct 20-30min con superior quality
- OpenCode 30B su multi-file complesso NON validato (ADR-0022 dataset n=2 single-file dogfood)

**Risk concreto**: senza fallback strategic, Eduardo si trova post-19/05 con choices sub-ottimali:
1. Lo fa a mano in 4-8h (perdita produttivita' 80%)
2. Tenta OpenCode multi-file (fallisce per gap empirici)
3. Differisce / accumula debito (anti-pattern)
4. Riacquista Pro reactive in panico (ADR-0015 invalidato)

## Decision Drivers

- **Sovereign principle ADR-0001**: zero subscription ricorrenti. API on-demand mantiene principle (paghi solo quando usi).
- **Quality preservation**: strategic tier richiede frontier reasoning. Claude API Opus 4.7 / Sonnet 4.6 mantiene parity con sessioni Max attuali.
- **Cost predictability**: budget cap $10-20/mese e' 1/12 a 1/24 di Claude Pro $240/anno = costo orario equivalente ma scalato a effective usage.
- **Trigger reactivation Pro chiaro**: se utilizzo >$20/mese 2 mesi consecutivi -> revisita Scenario A vs B con dati reali. Anti-panic decision.
- **ccusage tracking esistente**: tooling Claude Code gia' traccia consumption. Nessun setup aggiuntivo.

## Considered Options

### Opzione A (chosen) -- Claude API pay-per-use on-demand con budget cap

Setup:
- API key Claude Console (`ANTHROPIC_API_KEY` in `~/.config/api-keys/keys.env`, ACL-hardened gia' applicata da setup precedente)
- Budget cap mensile $10-20 (soft-cap auto-monitor, no hard enforcement)
- Trigger spend autorizzato:
  - Multi-file refactor >=3 file con cross-reference
  - Debug architetturale (root cause analysis su sistema complesso)
  - ADR draft strategico (MADR format + 4 opzioni + rationale)
  - Synthesis cross-source (research + ADR + code)
  - Constraint >=5 strict in singolo task
- Workflow: Eduardo lancia `claude --print "<task>" --model claude-opus-4-7` o sessione interactive `claude` quando needed. Token consumed tracked in ccusage.

**Pro**:
- Scenario A full-sovereign principle preservato (zero subscription)
- Quality strategic tier mantenuta
- Costo flessibile (paghi quanto usi, $0 se non usi quel mese)
- Trigger reactivation Pro chiaro (no panic decision)

**Contro**:
- Cognitive overhead "vale la spend?" per ogni task strategic
- Cost variance imprevedibile mese-per-mese (vs flat $20/mese Pro)
- Dependency API key disponibile (single-point-of-failure secondary)

**Costo stimato**: $5-15/mese in working assumption (1-3 task strategic complessi/mese a $1-5 ciascuno).

### Opzione B -- Claude Pro $240/anno acquisito

**Pro**: flat rate, predictability, no decision overhead, Claude Code OAuth continua daily
**Contro**: Scenario A full-sovereign INVALIDATO. ADR-0015 amendment necessario. $240/anno = $20/mese fixed. Anti-pattern "pay-just-in-case" se utilizzo medio < $20/mese.

### Opzione C -- Strategic tier "lo fa a mano Eduardo"

**Pro**: $0/anno, full sovereign integral
**Contro**: perdita produttivita' 4-8x su task strategic. Backlog accumula. Anti-pattern documentato 2026-04-21.

### Opzione D -- Differisco / dico no

**Pro**: zero spend
**Contro**: debito tecnico cresce. Anti-lean. Solo per task low-priority differibili.

## Decision Outcome

**Scelto Opzione A**: Claude API pay-per-use on-demand con budget cap mensile $10-20.

### Configurazione applicata

1. **API key setup** (gia' presente in `~/.config/api-keys/keys.env` come `ANTHROPIC_API_KEY` -- verificare presenza, eventualmente generare via Console)
2. **Budget cap soft**: monitor mensile via `ccusage` cumulative end-of-month. Threshold:
   - $0-10 OK silente
   - $10-15 awareness (verifica trend)
   - $15-20 alert (riconsidera frequenza task delegati)
   - $20+ trigger reactivation Pro ratification (vedi sezione Follow-up)
3. **Trigger spend autorizzato**: esplicita per task. Eduardo dichiara in chat "questo e' strategic, autorizzo Claude API". Pattern check-in volontario.
4. **Tracking**: entry in `logs/claude-api-spend-YYYY-MM.md` per ogni sessione. Schema:
   ```
   | Data | Task | Token sent/recv | Cost USD | Outcome |
   ```
5. **Fallback se API down**: rivedere budget cap, considerare deferral task O reactive Pro purchase.

### Workflow integration con tier routing esistente

Decision tree updated (CLAUDE.md "Priorita' modelli AI" + MODEL_ROUTING):

```
Task strategic complesso (multi-file >=3 / constraint >=5 / debug arch / ADR draft)?
├─ SI -> Claude API on-demand (Opzione A questo ADR)
│        ├─ Cost stimato accettabile? (mental check vs budget mensile rimanente)
│        │   ├─ SI -> esegui sessione Claude (sonnet o opus a discrezione)
│        │   └─ NO -> defer / OpenCode 30B con expectation lower quality / manual
│        └─ Tracking ccusage + entry log
└─ NO -> tier 1-3 esistenti (Aider/OpenCode/Ollama)
```

## Consequences

### Positive

- Strategic tier coperto post-19/05 senza compromettere Scenario A full-sovereign
- Cost predictability via cap mensile + ccusage monitoring
- Trigger reactivation Pro chiaro (no panic decision in Q3 2026)
- Scenario A integral: subscription ricorrenti = $0, API consumption = pay-per-use

### Negative

- Cognitive overhead per task: "vale spend?" decision check
- Variance mensile imprevedibile (vs Pro flat)
- API key dependency (mitigato: backup automation deferred SPRINT_02)
- Risk underestimation cost: se utilizzo cresce gradualmente senza accorgermene -> trigger reactivation tardivo

### Neutral

- ADR-0015 NON viene emendato (Scenario A confermato; questo ADR estende, non sostituisce)
- ccusage tooling gia' presente, no setup aggiuntivo

## Follow-up

- [ ] Verifica `ANTHROPIC_API_KEY` presente in `~/.config/api-keys/keys.env`. Se assente, generare via Anthropic Console.
- [ ] Creare `logs/claude-api-spend-2026-05.md` (gitignored) con header schema entry tracking
- [ ] CLAUDE.md "Priorita' modelli AI" sezione: aggiungere tier 0 strategic post-Max con riferimento ADR-0023
- [ ] MODEL_ROUTING.md: aggiornare "Decisione finale attuale" sezione "post 19/05" con strategic tier on-demand
- [ ] Trigger reactivation Pro: se cumulative ccusage >$20 in mese N AND mese N+1 -> ratification ADR-0023 addendum revisita Scenario B
- [ ] Trigger Accepted (status flip Proposed -> Accepted): n>=2 task strategic completati post-19/05 con cost <$20/mese OR documentazione 1 task con cost >$10 ma rationale forte (es. ADR-0024 draft).
- [ ] Backup automation API keys (deferred SPRINT_02): script PowerShell daily rotation backup.

## Addendum 2026-05-18 — Premessa-drift deadline + Max ri-acquistato

**Fatto**: la deadline Max reale era **~17/05/2026** (non 19/20 come da TL;DR + roadmap CLAUDE.md). Eduardo ha **ri-acquistato Claude Max per +1 mese (~17/05 → ~17/06/2026)**.

**Impatto decisione**:
- La premessa "post-19/05 Claude Max OAuth scade" di questo ADR e' **temporaneamente differita**, NON annullata. Strategic-tier-fallback resta valido come piano; il trigger si sposta a **~17/06/2026**.
- ADR-0023 resta **Proposed** (non flip): non c'e' ancora periodo post-Max reale su cui raccogliere n>=2 dogfood strategic-tier. Il mese Max aggiuntivo = finestra per **validazione empirica sovereign-tier** (provare il fallback davvero, non teorizzare) → a ~17/06 la budget-decision avra' dati reali invece di stima.
- Trigger reactivation Pro / Accepted invariati come *logica*; le *date* shiftano +1 mese.

**Classe-errore**: stesso pattern drift doc-vs-reality cacciato nella sessione 2026-05-18 (Triangle/Sentience premise falsificate via ground-truth). Qui il doc strategico *fondante* (roadmap CLAUDE.md + TL;DR questo ADR) aveva deadline-fantasma. Lezione: anche le date strategiche vanno re-verify, non ereditate.

**Azioni derivate** (questa sessione): CLAUDE.md roadmap §AGGIORNAMENTO 2026-05-18 + "Priorita' modelli AI" date corrette; DECISIONS_LOG pointer; STATUS_MULTI_REPO §DF gia' nota verdetto C/C indipendente. Sovereign scope **INVARIATO** (long-term), solo cronometro rilassato.

## Riferimenti

- ADR-0001 -- Sovereign AI strategy: `0001-sovereign-ai-strategy.md`
- ADR-0008 -- Aider whole format silent-corruption + tier routing: `0008-aider-whole-format-silent-corruption.md` (strategic NON delegabile)
- ADR-0015 -- Fase 7 budget decision full-sovereign: `0015-fase7-budget-decision-full-sovereign.md` (Scenario A confermato)
- ADR-0016 -- Constraint-count routing dimension: `0016-constraint-count-routing-dimension.md` (Proposed, 5+ strict trigger)
- ADR-0022 -- OpenCode tool-use model routing: `0022-opencode-tooluse-model-routing.md` (Accepted con n=3 dogfood single-file)
- Harsh review: `docs/reviews/flow-chart-harsh-review-2026-05-09.md` (V1 BLOCKING resolution)
- Decisione 007 in `DECISIONS_LOG.md` (Eduardo risposte 6 questions, scelta 1A)
- ccusage docs: `https://github.com/anthropics/claude-code` (tooling integrato)
