# ADR-0012 — Upgrade RAM 16→64 GB: impatto su tier routing e config Ollama

> *TL;DR: upgrade hardware 2×32GB DDR5-5600 dual channel effettuato 2026-04-22 rimuove il collo di bottiglia RAM da tier 2 (qwen3-coder:30b "RAM tight"), apre finestra praticabilità per modelli 30B+ dense, e rende rivalutabile `OLLAMA_CONTEXT_LENGTH=8192` (ADR-0004). Decisione: aggiornare CLAUDE.md + promuovere qwen3:30b a tier 2 stabile ora; rivalidare `num_ctx` default e pullare candidati 30B+ solo dopo bench empirico (task separato, non retroattivo su numeri già misurati).*

- **Status**: Accepted
- **Data**: 2026-04-22
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

## Context and Problem Statement

Il 2026-04-22 è stato effettuato upgrade hardware non pianificato in roadmap ADR-0009:

- **Prima**: 16 GB DDR5 (1 modulo)
- **Ora**: 64 GB DDR5-5600 (2×32 GB Micron CT32G56C46S5.C16D, dual channel ChannelA-DIMM1 + ChannelB-DIMM1)

Misura empirica post-upgrade (idle desktop + Claude Code + VSCode aperti):

```
Total: 63.37 GB | Used: 8.99 GB | Free: 54.38 GB
```

L'upgrade tocca **direttamente** due ADR già Accepted:

1. **ADR-0004 "Ollama config per RTX 5060 Blackwell"** documenta 16GB DDR5 come vincolo host. `OLLAMA_CONTEXT_LENGTH=8192` (ridotto da 16384 il 2026-04-20) è stato scelto per liberare KV cache da CPU spill su 14B Q2 con RAM stretta. Razionale originale: decaduto.
2. **ADR-0009 "Strategia evoluzione stack AI locale"** addendum 2026-04-21 promuove `qwen3-coder:30b` (Q4_K_M, 18 GB) a tier 2 escalation ma annota esplicitamente "RAM tight (1.3 GB free)". Con 54 GB liberi il vincolo è rimosso.

Serve un ADR che:
- Documenti lo stato hardware attuale e la sua data (l'hardware è "definitivo" in CLAUDE.md ma si è mosso)
- Dica cosa cambia *subito* senza bench (decisioni a rischio zero)
- Separi ciò che richiede bench empirico (decisioni con rischio regressione)
- Non invalidi dati già misurati (i tok/s sono empirici e restano validi; solo le *condizioni al contorno* cambiano)

## Decision Drivers

- **Fedeltà al dato empirico**: i numeri in CLAUDE.md (Qwen 14B Q2 18.7 tok/s, qwen3:30b 23.3 tok/s @ ctx 8192) restano validi — misurati, non predetti. L'upgrade RAM non li sposta al rialzo *automaticamente*: apre solo finestra rebench.
- **YAGNI (ADR-0005)**: non modificare env var globali finché non esiste dato che confermi miglioramento. La fascia 14B Q2 + ctx 8192 è la base testata di Fase 6 (n=3 dogfood + dati pre-upgrade).
- **ADR-0009 governance trigger**: questo upgrade materializza *parzialmente* il trigger T2 "hardware RAM" senza attraversare il decision framework formale. Va documentato retroattivamente senza pretendere che lo fosse.
- **Sovereign post 19/05/2026**: più RAM = tier 2 locale più solido = pressione economica ridotta su Claude Pro fallback. Impatto sulla budget decision Fase 7 non quantificabile ora ma positivo in direzione "sovereign sostenibile".

## Considered Options

### Opzione A — Ignorare l'upgrade nei documenti, usare la RAM extra opportunisticamente

**Pro**: zero effort documentale; gli ADR esistenti restano puri.

**Contro**: futuro-me legge CLAUDE.md "16GB DDR5" + ADR-0009 "qwen3:30b RAM tight" e ragiona su vincoli falsi. I dogfood Fase 6 successivi a oggi avverranno in condizioni diverse dai pre-upgrade senza tracciabilità del perché.

### Opzione B — Aggiornare CLAUDE.md + ADR-0012 + rebench tutto subito

Prima di concludere la sessione: pullare Qwen 32B Q4, rebench 14B Q2 @ ctx 16384, rebench qwen3:30b con RAM libera, ripubblicare tabella.

**Pro**: CLAUDE.md + ADR-0012 consolidati con numeri freschi in un colpo solo.

**Contro**: bench rigoroso costa 1-2h e richiede prompt standardizzato (ADR-0007 usa DoublyLinkedList Python) + condizioni controllate (nessun altro processo). Farlo "di corsa" introduce rumore nei dati. Fase 6 sta raccogliendo n=3 dogfood reali — meglio non inquinare con cambi infrastruttura mid-stream.

### Opzione C (chosen) — Aggiornare docs + promuovere qwen3:30b a tier 2 stabile ORA; bench come task separato

Oggi:
- CLAUDE.md: hardware section 16→64 GB + nota su `OLLAMA_CONTEXT_LENGTH` da rivalidare + promozione qwen3:30b
- ADR-0012: questo documento
- JOURNAL entry + memory update

Deferred (task esplicito, non in questa sessione):
- Bench 14B Q2 @ ctx 16384 vs 8192 su prompt standard ADR-0007
- Bench qwen3:30b con RAM libera (conferma tok/s ±)
- Pull + bench candidati 30B+ dense (Qwen 2.5 Coder 32B Q4, Codestral 22B, DeepSeek Coder V2 33B) — se e solo se emerge esigenza concreta

**Pro**: decisioni a rischio zero prese subito (promozione tier, rimozione vincolo falso); decisioni che richiedono misura trattate come tali; Fase 6 non viene inquinata.

**Contro**: CLAUDE.md resta per un periodo con una nota "rivalidare bench empirico" — forma di debito documentale esplicito, accettabile.

## Decision Outcome

**Scelta Opzione C**.

### Cambiamenti immediati (questo ADR)

1. **CLAUDE.md Hardware section**: `16GB DDR5` → `64GB DDR5-5600 (2×32GB Micron CT32G56C46S5.C16D, dual channel)` con riferimento a questo ADR e data upgrade.
2. **CLAUDE.md Capacità AI**: nota esplicita "post 2026-04-22 modelli 30B+ non più RAM-bound" sotto la tabella tok/s, senza toccare i numeri misurati.
3. **CLAUDE.md env vars**: nota in-line su `OLLAMA_CONTEXT_LENGTH=8192` che il razionale originale è decaduto, rivalidazione richiesta.
4. **CLAUDE.md modelli installati `qwen3-coder:30b`**: rimossa nota "RAM tight (1.3 GB free)", promosso da tier 2 borderline a tier 2 stabile.

### NON cambiati (deliberatamente)

- `OLLAMA_CONTEXT_LENGTH` env var User scope → resta `8192` fino a bench
- Wrapper `aider-cosmetic.cmd` / `aider-refactor.cmd` → invariati
- Tier routing CLAUDE.md sezione "Priorità modelli AI" → invariato (Qwen 7B cosmetic / 14B Q2 behavior / qwen3:30b escalation) — la decision matrix usa **speed + faithfulness**, non RAM headroom
- ADR-0004 / ADR-0007 / ADR-0008 / ADR-0009 → **non modificati nel corpo**, questo ADR li supersede sui soli punti RAM-bound
- `docs/adr/0009-upgrade-strategy.md` **trigger T2 hardware** resta formalmente non-triggerato (questo upgrade era opportunistic, non guidato dai trigger espliciti)

### Bench deferred (task separato)

Task singolo con prompt standard ADR-0007 (DoublyLinkedList Python) + condizioni controllate:

1. **14B Q2_K @ ctx 8192 vs 16384 vs 32768** → misurare tok/s delta. Se ctx 16384 resta ≥90% di 8192: promuovere a default env var. Se regressione >10%: mantenere 8192 e documentare che il collo è VRAM/KV compute, non RAM.
2. **qwen3-coder:30b @ ctx 8192 ripetuto** → conferma tok/s ~23.3 con RAM abbondante (sanity check: il numero pre-upgrade era con swap a rischio).
3. **qwen3-coder:30b @ ctx 16384 / 32768** → test escalation context per task multi-file.
4. **(Opzionale)** Qwen 2.5 Coder 32B Q4_K_M pull + bench — candidato sweet-spot se tok/s ≥15 e faithfulness ≥14B Q2.

Bench rimandato esplicitamente: evita di inquinare Fase 6 con cambio baseline infrastruttura mid-stream. Quando eseguito, genera entry dedicata in ADR-0007 o nuovo ADR specifico.

### Impatto su Fase 6 in corso

- I dogfood n=3 già raccolti (JSDoc commit-guard, comment-based help ps1, aider-log exit codes) restano validi **as-is**: task cosmetic 7B-whole, RAM non era mai il collo per loro.
- I prossimi dogfood behavior-critical (14B Q2) continueranno con ctx 8192 default finché non c'è bench.
- La **baseline economica** ($118.76 / 3 giorni pay-per-use) resta quella di riferimento per Fase 7 budget decision.

### Impatto su Fase 7 budget decision

L'upgrade rafforza lo scenario **sovereign** in modo qualitativo: tier 2 locale più solido = meno deleghe che cadono in pay-per-use escalation. **Non quantificabile ora** — dipende da Fase 6 fail rate empirico. Questo ADR registra la direzione, non muove la decisione.

## Consequences

**Positive**:
- Vincolo falso ("RAM tight") eliminato dalla knowledge base operativa
- Finestra praticabilità per modelli 30B+ aperta (rebench decides)
- Pressione su `OLLAMA_CONTEXT_LENGTH` reversibile con dato

**Negative / debito**:
- Debito documentale esplicito: "rivalidare bench empirico" in CLAUDE.md resta finché task bench non eseguito
- Due cose da ricordare per future me: (a) qwen3:30b "RAM tight" non è più vero, (b) `num_ctx 8192` è legacy config da 16GB RAM

**Neutral**:
- La tabella tok/s in CLAUDE.md resta invariata — dati empirici pre-upgrade sono validi, upgrade non li invalida (apre rebench, non lo forza)

## Follow-up

- [ ] Aggiornare CLAUDE.md (fatto in questa sessione)
- [ ] Entry JOURNAL.md 2026-04-22 (fatto in questa sessione)
- [ ] Update memory `project_sovereign_evaluation.md` (rimuovere blocker RAM-tight dal ragionamento budget)
- [ ] **Task deferred**: bench empirico 14B Q2 + qwen3:30b @ ctx variabili, in sessione dedicata
- [ ] **Task opzionale**: valutare pull Qwen 2.5 Coder 32B Q4_K_M come candidato tier 2 dense (~19-20 GB)
- [ ] Quando bench eseguito e decisioni prese: questo ADR passa a "Superseded by ADR-0013" (se emerge nuovo ADR su default `num_ctx`) o viene esteso con Addendum.

## Riferimenti

- **ADR-0004** `0004-ollama-rtx5060-config.md`: config Ollama originale — razionale `num_ctx=8192` da questo ADR parzialmente superato.
- **ADR-0007** `0007-aider-qwen-quantization-findings.md`: dati tok/s Qwen 14B Q2 misurati con 16GB. Prompt standard DoublyLinkedList Python da riusare per rebench.
- **ADR-0009** `0009-upgrade-strategy.md`: framework trigger hardware. Trigger T2 RAM formalmente non-triggerato (upgrade opportunistic). Addendum 2026-04-21 su qwen3:30b "RAM tight" superato da questo ADR.
- **CLAUDE.md**: sezioni Hardware, Capacità AI, Stack installato modelli locali — aggiornate stessa data.

---

## Addendum 2026-04-22 sera — Bench empirico completato

Bench eseguito stessa serata dell'upgrade (8 run totali), log completo: `docs/research/bench-post-ram-upgrade-2026-04-22.md`.

### Sintesi risultati

**14B Q2_K dense** (tier 1 behavior default):
- ctx 8192: 25.39 tok/s (sanity PASS vs baseline 25.54)
- ctx 16384: 17.28 tok/s (-7.7% vs baseline 18.72 — possibile drift Ollama 0.21 o rumore; tracciare in uso reale)
- ctx 32768: 11.62 tok/s (nuovo dato)
- → **Nessun beneficio RAM**: collo è VRAM+compute, non RAM budget.

**qwen3-coder:30b MoE** (tier 2 escalation):
- ctx 8192: 30.67 tok/s (**+31.6%** vs baseline 23.3 pre-upgrade)
- ctx 16384: 30.65 tok/s (zero penalty vs 8192)
- ctx 32768: 29.78 tok/s (-3% rumore)
- → **Beneficio RAM massiccio**: rimuovere "RAM tight 1.3 GB free" libera workload CPU-spilled. MoE ctx-insensitive: ctx doppio gratis.

**qwen2.5-coder:32b dense** (bench 7 + 7b, candidato tier 2 valutato):
- ctx 8192: 3.65 tok/s
- ctx 16384: 3.52 tok/s
- → **8.4× più lento di qwen3:30b MoE a size pari**. CPU-bound massiccio (73% CPU, 32B attivi full-weight ogni token). **Scartato** come tier routing.

### Decisioni finalizzate (post-bench)

1. **`OLLAMA_CONTEXT_LENGTH=8192` RESTA default globale** (coerente con 14B Q2 tier 1). Il razionale ADR-0004 era decaduto *come giustificazione RAM* ma la scelta resta ottima *come coerenza tier 1 speed*.
2. **qwen3:30b tier 2 promosso a ctx 16384** per task multi-file (override `options.num_ctx=16384` via API) — zero penalty tok/s, raddoppia effective context. Da integrare in `aider-refactor.cmd` come variante o flag opzionale.
3. **qwen2.5-coder:32b dense scartato** come candidato tier routing. Resta scaricato per reference/comparison, ma non va in CLAUDE.md tier table.
4. **Hub pattern ADR-0008 invariato**: la decision matrix (cosmetic 7B / behavior 14B Q2 / escalation qwen3:30b) è **rafforzata** dal bench, non modificata. L'unico cambio è ctx default per tier 2 escalation (8192 → 16384) via override per-request, non env var globale.

### Regressione 14B Q2 ctx 16384 (-7.7%) — tracking

17.28 tok/s vs 18.72 baseline ADR-0007. Cause possibili da indagare se si ripresenta in uso reale:
- Ollama 0.21.0 vs versione al tempo di ADR-0007 (2026-04-20 — verificare changelog)
- Driver NVIDIA 595.79 stability
- Thermal throttling (bench sera, 32B appena scaricato, possibile heat leftover)
- Rumore statistico n=1

**Non è blocker** perché il default operativo 14B Q2 resta ctx 8192. Se il `num_ctx: 16384` override per-request viene usato raramente, il dato è informativo ma non critico.

### Impact Fase 7 budget decision

Il bench **rafforza scenario sovereign**:
- Tier 2 qwen3:30b post-upgrade = 30 tok/s cross-ctx → può coprire task multi-file che pre-upgrade sarebbe stato marginale
- Tier 1 14B Q2 invariato a 25 tok/s (sweet spot validato)
- Capability tier 3 rimane Claude Pro fallback per debug strategico multi-turn

Baseline economica $118.76/3g pay-per-use → pressure di downgrade a Pro resta valida ma **meno drammatica** se Fase 6 confermerà che il 90% dei task è tier 1-2 locale.

### ADR status

Da "Accepted" a **"Accepted + Validated"**: la decisione di promuovere qwen3:30b a tier 2 stabile ha dato empirico (+31.6% speed post-upgrade). La decisione di tenere `OLLAMA_CONTEXT_LENGTH=8192` default ha dato empirico (nessun beneficio RAM su 14B Q2).

Superseding tracking: questo ADR **supersede** punti specifici di ADR-0004 (razionale RAM su num_ctx 8192) e di ADR-0009 addendum 2026-04-21 (qwen3:30b "RAM tight"). ADR-0007 resta intatto (i suoi numeri 14B Q2 sono confermati).
