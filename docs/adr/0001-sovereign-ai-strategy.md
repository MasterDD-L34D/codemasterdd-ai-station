# ADR 0001 — Sovereign AI Strategy

> *TL;DR: post Claude Max (scadenza 19/05/2026), transizione a stack sovereign Ollama+Claude Code senza OAuth con fallback OpenRouter pay-per-use, target €60-180/anno invece di €2400. Trade-off: minor capability frontier, validazione empirica richiesta in Fase 6.*

> ⚠️ **AMENDMENT 2026-05-18 (pivot accettato da Eduardo)**: il target sovereign-$0-50/anno e' **ufficialmente RITIRATO**. ADR-0015 amendment 15/05 lo aveva dichiarato "VIOLATED by realism"; **ADR-0030 (Hybrid A1, Accepted 2026-05-18) lo supersede**: nuovo modello = Pro $20/mo + Meridian + OpenCode + Gemini-CLI-free + OpenRouter-overflow, target realistico **$240-600/anno**. La filosofia sovereign-first (locale-prioritario, no-lock-in, multi-provider) RESTA valida come *principio*; il *numero* $0-50 e' morto. Vedi ADR-0030 + DECISIONS_LOG Decisione 009.

**Status**: Accepted (target $0-50/anno superseded-by-ADR-0030 2026-05-18; filosofia sovereign-first invariata)
**Data**: 2026-04-20
**Decisore**: Eduardo Scarpelli
**Tipo decisione**: strategica (lungo termine, budget, filosofia)

## Contesto

### Situazione iniziale (aprile 2026)

Dopo il trauma Victus del 17 aprile 2026 (perdita PC per bug BitLocker +
OneDrive), ho acquistato Lenovo desktop come sostituzione.
Questa workstation (ribattezzata CodeMasterDD) diventa la mia piattaforma
dev primaria.

**Hardware disponibile**:
- CPU Intel Core Ultra 7 255HX (24 core Arrow Lake HX)
- GPU NVIDIA RTX 5060 8GB VRAM (Blackwell)
- 16GB DDR5
- 1TB SSD

**Sottoscrizioni attive**:
- Claude Max: €200/mese (attivo da marzo 2026, scade 19/05/2026)

**Progetti reali in sviluppo**:
- Evo-Tactics (co-op tactical game d20, Node+Python monorepo)
- Synesthesia (web app esame UniUPO, Express+EJS+SQLite)
- App per artisti (early stage, da definire stack)

**Workload**: 8-10 ore/giorno di dev su progetti reali.

### Il problema

**Claude Max** costa €200/mese = €2400/anno.
Con workload pesante, c'è rischio di saturare rate limit
(15-35 ore/settimana Opus 4.7 garantite, heavy users reportano
esaurimento in 3-5h di lavoro attivo).

**Visto il costo elevato e rischio rate limit, la sostenibilità a lungo
termine è incerta**.

### Filosofia personale

Aldilà del costo, ho una **filosofia di fondo** che vale di più:

**"Voglio che il mio stack dev sia mio"**. Non a noleggio mensile. Non
vincolato a terzi che possono cambiare prezzi, policy, o shut down.

**Parole chiave**:
- **Sovereignty**: controllo totale di dati + strumenti
- **Ownership**: hardware + software locali che posseggo
- **Predictability**: costi prevedibili, zero sorprese
- **Resilience**: funzionamento anche senza internet

## Decisione

Adotto una **strategia sovereign AI graduale** in 3 fasi.

### Fase 1: Setup intensivo (aprile-metà maggio 2026)

**Durata**: ~30 giorni con Claude Max attivo
**Obiettivo**: **learning + building infrastructure per la transizione**

**Attività**:
- Usare Claude Code + Opus 4.7 intensivamente per capire cosa è imprescindibile
- Setup parallelo Ollama locale (Qwen 2.5 Coder 7B come primo modello)
- Per ogni task fatto su Opus: valutare "questo lo farebbe anche Qwen 7B?"
- Costruire infrastructure riutilizzabile: CLAUDE.md ottimi, subagents, scripts
- Misurare gap qualitativo Opus vs Qwen su task reali
- Documentare workflow, decisioni, ricerche

**Outcome atteso**: skill profondi Claude Code + infrastructure tested + clarity
su quali task richiedono cloud e quali vanno bene locali.

### Fase 2: Transizione (metà maggio - giugno 2026)

**Durata**: ~30 giorni
**Obiettivo**: **scollegare dipendenza Claude Max, consolidare locale**

**Attività**:
- Rinuncia rinnovo Claude Max il 19/05/2026
- Setup account OpenRouter con $10-20 credito iniziale (per fallback
  pay-per-use su task critici)
- Spostare 90% workflow su Ollama locale + Claude Code (anche senza Max,
  Claude Code funziona con API keys)
- Configurare VS Code + estensione Cline (agent AI locale, free, BYOK)
- Se emergono gap di qualità → usare OpenRouter per task specifici

**Outcome atteso**: stack dev 100% funzionale senza subscription ricorrenti.

### Fase 3: Sovereign steady state (da giugno 2026)

**Durata**: indefinita
**Obiettivo**: **operatività autonoma low-cost ad alta qualità**

**Stack target**:
- **Primary inference**: Ollama locale (Qwen 2.5 Coder 7B + Qwen 3 8B + eventuali modelli futuri)
- **Fallback cloud**: OpenRouter pay-per-use ($5-20/mese in media)
- **Editor**: VS Code + Cline (agent locale)
- **Terminale**: Claude Code (senza Max, pay-per-use o community models)
- **MCP servers**: solo quelli essenziali (GitHub, Context7 probabile)

**Budget atteso**: **€0 fisso + €5-20/mese variabile = €60-240/anno**

### Estensioni future OPZIONALI (non dependency)

**Mac mini M4 Pro 48GB** (~€2500-3000): se/quando budget permette.
Permetterebbe di girare modelli 30B+ (DeepSeek-Coder-V2, Qwen 3 32B)
con unified memory. **Ma NON è dependency del piano**: Lenovo funziona
pienamente da solo.

## Consequenze

### Positive attese

**Budget**:
- Da €2400/anno (Claude Max continuo) a €60-240/anno
- **Risparmio stimato 3 anni: ~€4000-7000**
- Mac mini eventuale ammortizzato in 12-18 mesi

**Controllo**:
- Dati sensibili (code, progetti, thinking) non passano da server esterni
- Zero dipendenza da "cambi di policy" Anthropic
- Funziona offline (aereo, internet down, travel)

**Skill**:
- Competenza profonda su LLM locali, Ollama, quantizzazione
- Prompt engineering trasferibile tra modelli
- Subagents ottimizzati

**Resilienza**:
- No vendor lock-in
- No surprise pricing
- No service discontinuity risk

### Negative attese

**Qualità**:
- Qwen 7B locale < Opus 4.7 su task complessi (architettura, debug
  difficili, reasoning lungo)
- **Mitigazione**: OpenRouter per task critici, Qwen 7B per routine

**Setup effort**:
- Più setup iniziale (Ollama config, env vars, benchmark, workflow)
- Più manutenzione (update modelli, cleanup storage)

**Hardware dependency**:
- Se Lenovo si rompe → no AI finché non ripristino
- **Mitigazione**: backup cloud (OpenRouter come emergency)

### Risk mitigation

**Rischio 1**: Qwen 7B qualità insufficiente su task critici
**Mitigation**: OpenRouter backup + Mac mini upgrade se budget permette

**Rischio 2**: Lenovo fail/furto
**Mitigation**: repo su GitHub + dotfiles repo + setup script idempotente
per ricreare ambiente rapidamente

**Rischio 3**: Ecosistema Ollama va stale (modelli open source rallentano)
**Mitigation**: Hugging Face ha sempre alternative, switch modello è 1 comando

**Rischio 4**: Mi abituo a Opus 4.7 e non tollero downgrade
**Mitigation**: durante Fase 1 forzare me stesso a usare Qwen 7B 50%+ del tempo,
per abituarmi gradualmente

## Alternative considerate

### Alternative 1: Claude Max continuo

**Descrizione**: mantenere Claude Max attivo indefinitamente (€200/mese).

**Pro**:
- Opus 4.7 è modello di frontier quality (migliore attualmente disponibile)
- Zero setup aggiuntivo
- 1M context window

**Contro**:
- €2400/anno fisso
- Rate limit per heavy users
- Dipendenza Anthropic

**Perché scartata**: costo + filosofia sovereign + rischio continuità servizio.

### Alternative 2: Claude Pro + OpenRouter fallback

**Descrizione**: Claude Pro $20/mese + OpenRouter pay-per-use.

**Pro**:
- Basso costo fisso (€240/anno)
- Accesso a Sonnet 4.6 (quasi Opus quality)
- Meno setup di Ollama

**Contro**:
- Ancora subscription fisso
- Rate limit anche su Pro
- Dati comunque su cloud

**Perché scartata**: filosofia sovereign, ma **mantenuta come fallback Plan B**
se Fase 3 dimostra qualità locale insufficiente.

### Alternative 3: Z.ai GLM-4.7 subscription

**Descrizione**: subscription alternativa a Anthropic ($10/mese).

**Pro**:
- Molto più economica di Anthropic
- Modello cinese performante

**Contro**:
- Ancora subscription
- Dati su server cinesi (implicazioni privacy)
- Ecosistema meno maturo

**Perché scartata**: violava stessa filosofia sovereign. Inoltre io non
l'avevo mai autorizzata — era una raccomandazione di Claude che ho poi
fermato quando realizzata l'incongruenza.

### Alternative 4: API only (no subscription)

**Descrizione**: solo API key Anthropic, pay-per-token.

**Pro**:
- Nessuna subscription
- Pago solo quello che uso

**Contro**:
- Costo variabile imprevedibile
- Per workload pesante potrebbe costare più di Claude Max
- Ancora dipendenza cloud totale

**Perché scartata**: costo imprevedibile + nessuna sovereign component.

### Alternative 5: Full cloud multi-provider

**Descrizione**: abbonamenti multipli (OpenAI + Anthropic + Google).

**Pro**:
- Flessibilità massima su modello migliore per task
- Ridondanza

**Contro**:
- Costi esplosivi ($60-200/mese combinati)
- Vendor sprawl
- Zero sovereign

**Perché scartata**: violazione completa filosofia sovereign.

### Alternative 6: Mac mini subito + scrapping Lenovo

**Descrizione**: vendere Lenovo, comprare Mac mini M4 Pro 48GB come dev primary.

**Pro**:
- Hardware ottimizzato per AI (unified memory)
- macOS preferito da molti dev

**Contro**:
- Costo immediato €2500-3000
- Perdita di hardware nuovo (Lenovo)
- Mac non nativo per alcuni ecosistemi (Windows-specific tool)

**Perché scartata**: Lenovo è già valido. Mac mini è upgrade futuro,
non sostituzione. **Mac mini ≠ dependency**.

## Piano implementativo

> **Nota storica (2026-05-24)**: questo piano e' stato scritto il 20 aprile 2026.
> Le milestone 1-4 sono state parzialmente eseguite e poi **sostituite da decisioni successive**:
> vedi ADR-0014 (timeline compression), ADR-0023 (strategic tier post-Max),
> ADR-0029 (OpenRouter declined), ADR-0030 (Hybrid A1 orchestration).
> Le voci qui sotto sono mantenute come documento storico, non come piano attivo.

### Milestone 0 (19-20 aprile 2026) — DONE ✅
- [x] Setup Lenovo security (BitLocker off, OneDrive off, bloatware)
- [x] Install Git + Claude Code + dev stack
- [x] Ollama + Qwen 2.5 Coder 7B installato (benchmark 93 tok/s)
- [x] Repo GitHub `codemasterdd-ai-station` (infrastructure-as-code)

### Milestone 1 (settimana 21-27 aprile) — SUPERSEDED
- [~] Migrare Evo-Tactics + Synesthesia dal Ryzen al Lenovo → **non eseguito**: Synesthesia intenzionalmente sospesa fino ago 2026 (AGENTS.md), Evo-Tactics rimasto su repo esterno `MasterDD-L34D/Game`
- [~] Verificare che test passino (710+ test Evo) → **non pertinente** senza migrazione
- [x] Prime comparazioni Opus 4.7 vs Qwen 7B su task reali → **fatto** (documentato in docs/research/)
- [x] Documentare gap quality → **fatto** (ADR-0016, ADR-0028)

### Milestone 2 (settimana 28 aprile - 4 maggio) — SUPERSEDED
- [x] Install VS Code → **fatto**
- [~] Configurare Cline con Ollama locale → **non adottato**: stack evoluto verso OpenCode (ADR-0022, ADR-0030)
- [x] Workflow parallelo: Opus per task critici, Qwen per routine → **fatto**, ma con Claude Code + OpenCode anziche' Cline
- [~] Eventuale install nvm-windows se Evo-Tactics ha conflitti Node 22/24 → **deferito** (YAGNI, mai servito)

### Milestone 3 (settimana 5-11 maggio) — SUPERSEDED
- [x] Rush finale Claude Max: task piu' complessi da salvare memoria → **fatto**
- [~] Prep OpenRouter account ($10-20 credito) → **valutato e rifiutato**: ADR-0029 sceglie sovereign-first BYOK
- [~] Subagent critical ready (rules-engineer Evo, passport-auth Synesthesia) → **parziale**: Jules PR governance (ADR-0032/0033/0034) ma non come subagent dedicati

### Milestone 4 (19-25 maggio) — DONE (parziale)
- [x] Rinuncia rinnovo Claude Max → **fatto**: Claude Max scaduto, non rinnovato
- [~] Switch workflow primario a Ollama + Cline → **fatto parziale**: Ollama usato (qwen3-coder:30b), ma con OpenCode, non Cline
- [x] Claude Code in modalita' pay-per-use (API key) → **fatto**
- [~] Test completo: workflow dev sul Lenovo senza Max → **in corso**: smoke test integrati (10/10), ma tuning continuo

### Milestone 5 (da giugno) — STEADY STATE (futuro)
- [ ] Validazione continua: e' sostenibile?
- [ ] Se qualita' insufficiente: Plan B (Claude Pro $20/mese)
- [ ] Se qualita' ok: mantieni, valuta Mac mini futuro

## Metriche di successo

**Fase 1 success**:
- Setup Lenovo stable + documented
- Qwen 7B benchmark ≥ 50 tok/s → **superato**, 93 tok/s
- Workflow Claude Code maturo
- 4+ commit su repo infrastructure

**Fase 2 success**:
- Zero subscription AI ricorrente
- Workflow dev funzionante su Lenovo da solo
- OpenRouter credit usage < $20/mese in media
- Evo-Tactics + Synesthesia development continuo

**Fase 3 long-term success**:
- Costo totale anno < €300
- Zero perdite di produttività post-migration
- Skill LLM locali consolidati
- Mac mini quando/se budget permette, non prima

## Meta-learning / riflessioni personali

### Perché questa decisione è importante per me

Non è (solo) per il risparmio €. È per **controllo** e **chiarezza mentale**.

Ogni tool/servizio a subscription mensile è una **cognitive load**:
- "Sto usando abbastanza per giustificare il costo?"
- "Dovrei cancellare?"
- "Che succede se aumentano il prezzo?"
- "E se il servizio sparisce?"

**Sovereign stack rimuove tutto questo**. Pago una volta (hardware),
uso finché voglio, nessuno può toglierlo.

### Il collegamento con il trauma Victus

Non è coincidenza che questa decisione segua il disastro Victus:
- BitLocker + Microsoft Account = fragile
- OneDrive sync obbligato = fragile
- Subscription AI = fragile

**Ho sofferto per la fragilità. Ora progetto per la resilienza**.

### L'equilibrio tra idealismo e pragmatismo

**Idealismo puro**: 100% locale, zero cloud, sovereign assoluto.
**Pragmatismo**: alcuni task locali non li farei con qualità accettabile.

**Equilibrio**: **sovereign di default, cloud solo quando necessario**.
OpenRouter è scelto **esplicitamente** (non auto) per task specifici.
È differenza qualitativa: scelgo io cosa mandare, non c'è auto-upload
opaco di dati.

### Perché NON rimandare

Ogni mese che passa con subscription continua è:
- Denaro speso non recuperabile
- Dipendenza che si rafforza
- Procrastinazione del piano

**Il momento giusto per iniziare sovereign è stato 1 anno fa.
Il secondo momento migliore è oggi.**

### Cosa NON comprare

Per ora NON compro:
- nvm-windows (YAGNI, solo se conflitti reali emergono)
- Mac mini (non necessario finché Lenovo basta)
- Subscription backup (ho già GitHub + Syncthing plan)
- Modelli locali oltre Qwen 7B (aggiungo quando servono)

**Keep it minimal until proven insufficient**.

## Revisione

**Prossima revisione pianificata**: 20 maggio 2026 (fine Claude Max).
**Trigger revisione straordinaria**: se qualità workflow scende
significativamente post-transizione.

## Appendice: situazione di partenza dettagliata

### Hardware Lenovo desktop ("CodeMasterDD")
- CPU: Intel Core Ultra 7 255HX (24 core Arrow Lake HX, 2.40 GHz base)
- GPU: NVIDIA RTX 5060 8GB VRAM (Blackwell sm_120)
- RAM: 16GB DDR5 5600 MT/s
- Storage: SSD 1TB Micron NVMe
- OS: Windows 11 Home 25H2 (build 26200)

### Software baseline (19-20 aprile 2026)
- Git 2.53.0
- Claude Code 2.1.114
- NVIDIA Driver 595.79 + CUDA 13.2
- GitHub CLI 2.90.0
- Node.js 24.15.0 + npm 11.12.1
- Python 3.12.10 + pip 25.0.1
- VS Code 1.116.0
- Ollama 0.21.0 + Qwen 2.5 Coder 7B (Q4_K_M, 4.7GB)

### Repository GitHub
- `MasterDD-L34D/codemasterdd-ai-station` (private, infrastructure-as-code)
- `MasterDD-L34D/Game` (Evo-Tactics, public)
- `MasterDD-L34D/synesthesia` (Synesthesia, public)
- Altri 6 repo pubblici side-project

### Budget storico AI subscriptions
- Claude Pro $20/mese da ottobre 2025 a febbraio 2026 (5 mesi × $20 = $100)
- ChatGPT Plus $20/mese sporadico (~3 mesi totali = $60)
- Claude Max $200/mese da marzo 2026 (1 mese pagato = $200)
- **Totale speso AI subscriptions 2025-2026**: ~$360

### Target budget post-transizione
- Costi fissi: $0/mese
- Costi variabili: $5-20/mese (OpenRouter)
- **Annuale**: $60-240
- **Risparmio su Claude Max continuo**: $2160+/anno
