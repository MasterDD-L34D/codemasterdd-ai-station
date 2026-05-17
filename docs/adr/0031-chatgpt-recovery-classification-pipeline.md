# ADR-0031 -- ChatGPT Business workspace recovery + classification pipeline

> *TL;DR: Esportare l'intero workspace ChatGPT Business "Area di lavoro di Master DD" (12 progetti, ~3500 conversazioni, 83 memory items, custom instructions) non e' possibile via native OpenAI export (Business/Team plans GDPR-blocked). Tool selezionato per bulk export: `brianjlacy/export-chatgpt` MIT (last push 2026-04-24), unico candidato con Projects folder traversal verificato empiricamente. Classificazione offline 100% sovereign: BERTopic + nomic-embed-text (Ollama) + Qwen 14B Q2 LLM labeling. Output staging in vault Sources/raw/ con promozione Eduardo-direct (sibling-peer NO-WRITE default codemasterdd). Decisione presa 2026-05-14, ratification trigger: bulk export run PASS + classify.py smoke.*

- **Status**: **Proposed** (2026-05-14 pre-execution)
- **Data**: 2026-05-14
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev (single-user workstation)

## Context and Problem Statement

Eduardo ha accumulato >3 anni di conversazioni in ChatGPT Business workspace "Area di lavoro di Master DD": 12 progetti, ~3500 conversazioni totali (numero audit UI, campo `total` endpoint sidebar restituiva conteggi errati), 83 memory items gestiti OpenAI, custom instructions attive. Con l'avvicinarsi della transizione sovereign (ADR-0015 Accepted, Claude Max expiration ~20/05/2026), recuperare e classificare questa knowledge base e' un task one-shot time-bounded.

### Situazione attuale

- Nessuna copia locale del corpus ChatGPT. Knowledge dispersa in OpenAI cloud.
- Native OpenAI "Data Export" (Settings > Data Controls) **NON disponibile per Business/Team plans** (GDPR thread community.openai.com). Solo Personal plans hanno accesso al ZIP nativo.
- Bearer JWT ChatGPT e' long-lived (~10 giorni, caso particolare vs consumer ~1h) -- finestra operativa ampia per bulk export.
- Vault Obsidian (origin Ryzen `C:/Users/VGit/Vault/`, clone Lenovo `C:/dev/vault-shared/`) ha struttura ACCESS (Atlas/Cards/Sources/Spaces) e 7 agent production. Destinazione naturale per atomizzazione.

### Input / trigger

Transizione sovereign pre-20/05: closing the loop su workspace cloud ChatGPT prima di ridurre abbonamento. Task one-shot non-ripetibile (finestra bearer + timing). Scope piu' grande del previsto: audit endpoint sidebar ha restituito conteggi `total` errati -- workspace e' piu' grande. Necessita' di pipeline classificazione offline per rendere utile il corpus estratto.

## Options

### Opzione A -- brianjlacy/export-chatgpt + BERTopic sovereign (SCELTA) ✅

Tool: `https://github.com/brianjlacy/export-chatgpt` (MIT, last push 2026-04-24, 36 stars).

Audit code completato pre-decisione:
- Project folder traversal verificato: endpoint `snorlax/sidebar` + per-project cursor paginato
- Business workspace explicit support documentato nel README
- Resumable progress via `.export-progress.json`
- Retry exhaustivo su 422 HTTP (multi-part file_id -- known bug non-fatal, non blocca export testo)

Memory items e Custom Instructions: direct API (`/backend-api/memories` + `/backend-api/user_system_messages`), NOT tramite MemPort (eliminata dipendenza aggiuntiva, scoperta durante audit-script pre-decisione).

Classificazione pipeline:
- **BERTopic** (Python, MIT) per clustering semantico automatico
- **nomic-embed-text** via Ollama locale per embeddings (100% sovereign, nessun dato verso cloud)
- **Qwen 14B Q2_K** via Aider/Ollama per LLM labeling dei topic cluster (tier 2 ADR-0008 sweet spot)

Staging: `Sources/raw/chatgpt-export-2026-05-14/_processed/Cards/` -- NOT diretto in `Spaces/<canonical>/`. Eduardo media promozione vault-direct (codemasterdd sibling-peer NO-WRITE).

**Pro**:
- 100% sovereign eccetto sorgente dati OpenAI backend (necessaria per origine)
- Projects traversal verificato empiricamente (non doc-only)
- Resumable -- bearer 10gg, export interrompibile
- BERTopic + nomic = classificazione offline zero-cloud
- MIT license su tutti i componenti
- Memory items + Custom Instructions via API direct -- no tool aggiuntivo

**Contro**:
- 36 stars (low community) -- bus-factor del maintainer elevato
- Known bug HTTP 422 multi-part file_id: non blocca export testo ma alcuni allegati multi-part potrebbero mancare
- 1 known contributor attivo -- no community bug triage attivo
- BERTopic richiede calibrazione manuale n_topics (hyperparameter sensibile)

**Cost**: ~30-60 min export (stima 3500 conv * rate API) + ~2h pipeline classify + ~1-3h vault integration manuale

### Opzione B -- pionxzh/chatgpt-exporter (SCARTATA)

Chrome extension MIT, UI-driven, molto diffusa (>5000 stars).

**Pro**: alta community, interfaccia visuale familiare

**Contro**: audit terminologia durante autoresearch wave 4 ha rivelato ambiguita' "Projects" -- chatgpt-exporter usa "Projects" per riferirsi a conversazioni organizzate per tag/folder UI-side, NON ai Business Team Projects (folder server-side con endpoint `snorlax/sidebar` dedicato). Support Business workspace project traversal NON verificabile da documentazione pubblica.

**Verdict**: scartata. Rischio export parziale silenzioso (nessuna garanzia Projects folder traversal Business).

### Opzione C -- ocombe gist (SCARTATA)

Script gist di ocombe, esplicitamente documentato per Business+SSO.

**Pro**: Business+SSO explicit support menzionato

**Contro**: project folder traversal NON documentato. Gist = manutenzione zero, no issue tracking, no version. Dipendenza fragile per un task one-shot critico.

**Verdict**: scartata. Gap documentazione project traversal non accettabile.

### Opzione D -- ChatGPT Toolbox / MemPort commercial (SCARTATE)

Soluzioni SaaS closed-source (ChatGPT Toolbox) o Chrome extension closed-source (MemPort per export bulk).

**Contro**: violano sovereign-first (ADR-0001 + ADR-0013). Source data ChatGPT (3500 conv) passa attraverso SaaS terzo.

**Verdict**: scartate immediate per sovereign-first. MemPort mantenuto SOLO per fallback memory items se API direct (`/backend-api/memories`) fallisce (uso minimo, browser-local, dati non trasmessi a server MemPort in questo caso d'uso).

### Opzione E -- Native OpenAI Data Export (SCARTATA)

Via Settings > Data Controls > Export data.

**Contro**: **NON disponibile per Business/Team plans** (verificato GDPR thread community.openai.com). 7-day SLA anche se disponibile -- fuori finestra 20/05. Non percorribile.

**Verdict**: scartata per blocco tecnico piano Business.

### Opzione F -- Nexus AI Chat Importer (SCARTATA)

Tool che importa dall'export ZIP nativo OpenAI.

**Contro**: richiede ZIP nativo come input (Opzione E). Se E non e' disponibile, F non e' percorribile.

**Verdict**: scartata per dependency su Opzione E.

### Custom GPTs: Opzione B Playwright gap-filler (DEFERRED)

Eduardo ha 0 Custom GPTs owned nel workspace (verificato durante audit). Script `chatgpt-recovery/scripts/scrape-custom-gpts.js` rimane scaffolded come gap-filler per future run o altri workspace.

## Decision

**Opzione A -- brianjlacy/export-chatgpt + BERTopic + nomic + Qwen 14B Q2 sovereign pipeline**.

Rationale:
1. **Unico tool con Projects traversal Business verificato** (empirico, non doc-only) tra i candidati valutati
2. **Sovereign compliance**: classificazione 100% locale preserva ADR-0001 + privacy corpus personale (GDR campagne, UniUPO notes, dev notes Evo-Tactics in vault)
3. **Staging decoupled**: vault staging `Sources/raw/` senza promozione automatica e' pattern vault-ops esistente (vault sibling-peer boundary CLAUDE.md preservato)
4. **Custom GPTs 0 owned**: Opzione B Playwright non necessaria per questa run

### Implementation plan

- **Step 1** [pre-execution] -- Pre-flight audit UI `chatgpt-recovery/01-PREFLIGHT-AUDIT.md` (conteggi, bearer token, struttura progetti) -- 10 min
- **Step 2** [export] -- Run brianjlacy bulk export secondo runbook `chatgpt-recovery/02-bulk-export-runbook.md`. Output locale `exports/` worktree o path temp. -- 30-90 min
- **Step 3** [memory + instructions] -- API direct `/backend-api/memories` + `/backend-api/user_system_messages` + bearer `%TEMP%\chatgpt-bearer.env` (ACL edusc+SYSTEM, no inheritance, delete post-pipeline) -- 15 min
- **Step 4** [staging] -- Copy `exports/` -> `C:/dev/vault-shared/Sources/raw/chatgpt-export-2026-05-14/` (Lenovo clone) -- 5 min
- **Step 5** [classification] -- `pipeline/classify.py` BERTopic + nomic-embed-text + Qwen 14B Q2 labeling -- 30-90 min (dipende da n=3500)
- **Step 6** [atomize] -- `pipeline/atomize.py` per-conversation -> Cards candidati -- 30-60 min
- **Step 7** [vault integration] -- Eduardo-direct: promozione Cards -> `vault/Spaces/<canonical>/` + MOC update -- 1-3h stima

Bearer storage policy: `%TEMP%\chatgpt-bearer.env`, NTFS ACL `CODEMASTERDD\edusc:(F)` + `NT AUTHORITY\SYSTEM:(F)`, inheritance disabilitata. Deletion obbligatoria post-pipeline (in runbook Step 3 teardown).

Cross-reference map `chatgpt-recovery/vault-cross-reference-map.yaml` mappa 12 progetti ChatGPT a vault Spaces esistenti (Dev/Evo-Tactics, GDR/HaoJin, ecc.).

### Consequences

#### Positive

- Corpus 3500+ conversazioni recuperato e classificato prima della transizione sovereign 20/05
- Knowledge base ChatGPT integrata in vault Obsidian strutturato (ACCESS: Atlas/Cards/Sources)
- Pipeline riusabile per futuri export (template ready, requirements.txt versionato)
- Memory items 83 + custom instructions capturati come markdown atomici

#### Negative

- brianjlacy bus-factor elevato (1 maintainer, 36 stars): se tool cessa maintenance, re-engineering necessario per future run
- HTTP 422 bug multi-part: alcuni allegati (images/files multi-part) potrebbero mancare senza errore visibile -- workaround: audit `export-progress.json` post-run
- BERTopic hyperparameter n_topics: calibrazione manuale richiesta per qualita' clustering (overhead +30-60 min prima run)
- Corpus potenzialmente grande (stima 200-500MB JSON) -- disk usage temporaneo Lenovo SSD

#### Neutral

- Custom GPTs: 0 owned -> Opzione B Playwright deferred senza impatto
- Staging vault `Sources/raw/` non e' promozione automatica -- Eduardo decision point post-pipeline (conforme sibling-peer boundary)

### Mitigations

- **Bug 422 file_id**: post-export, verificare `export-progress.json` per record con `error: 422`. Se >5% conversazioni affette, manual fetch targettato per quelle specifiche. Bug documentato come non-fatal per export testo.
- **BERTopic clustering povero**: fallback manual tagging top-20 clusters per nome se LLM labeling produce topic generici. Qwen 14B Q2 re-run con prompt piu' specifico.
- **Bearer scaduto mid-export**: export e' resumable via `.export-progress.json`. Refresh bearer + re-run riprende da ultimo checkpoint.
- **Rollback**: nessun write su vault-shared durante pipeline. Staging e' copia non-destructive. Eduardo decide se promuovere post-review. Se pipeline fallisce, staging delete + retry.

## Related

- **ADR-0001** -- Sovereign AI strategy (foundation: classificazione 100% locale)
- **ADR-0015** -- Fase 7 budget decision full-sovereign (trigger timing: transizione 20/05)
- **ADR-0028** -- Tier promotion quality gate methodology (vault Quality Gate 3-step, pipeline output dovra' rispettare standard)
- **vault-cross-reference-map** -- `chatgpt-recovery/vault-cross-reference-map.yaml` (mapping 12 progetti ChatGPT -> vault Spaces)
- **Memory** `project_vault_shared.md` -- sibling-peer boundary NO-WRITE codemasterdd (staging-only pattern)
- `chatgpt-recovery/01-PREFLIGHT-AUDIT.md` -- pre-flight checklist
- `chatgpt-recovery/02-bulk-export-runbook.md` -- runbook operativo
- `chatgpt-recovery/pipeline/classify.py` -- BERTopic + nomic + Qwen 14B Q2 pipeline
- community.openai.com GDPR thread (Business export blocco verificato -- Opzione E scartata)

## Notes

- **Timing**: finestra bearer ~10 giorni da oggi 2026-05-14. Export deve completarsi entro ~24/05 (post Max expiration). Non critico per Max, critico per motivazione one-shot.
- **Ratification trigger**: ADR Proposed -> Accepted dopo (1) brianjlacy bulk export run PASS (export-progress.json senza errori >5%) E (2) classify.py smoke PASS su campione n=20 conversazioni con topic clusters plausibili.
- **Trigger review futuro**: se ChatGPT Business abilita native export ZIP (GDPR compliance upgrade) -> Opzione F (Nexus) diventa primary, questo ADR Superseded. Se brianjlacy repo archived -> re-audit tool alternatives (ocombe gist come prima alternativa).
- **Cross-LLM applicability**: pipeline BERTopic + nomic + Qwen locale e' generica per qualsiasi corpus chat JSON (Gemini takeout, Claude export, Perplexity history). Documentare come pattern riusabile in `docs/patterns/` post-run se risultato positivo.
