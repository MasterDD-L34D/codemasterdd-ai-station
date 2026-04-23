# PROJECT_BRIEF

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/PROJECT_BRIEF.md`.

## Identità del progetto
- **Nome progetto**: CodeMasterDD AI Station (repo: `codemasterdd-ai-station`)
- **Tipo di progetto**: infrastructure-as-code personale + registry decisionale di transizione strategica AI (NON un prodotto, NON una libreria, NON codice di progetti reali — quelli vivono in `Evo-Tactics` e `Synesthesia` separati)
- **Stato attuale**: barra globale 88%, Fase 6 (empirical tracking compressa) al 30%, HEAD `a23b533` working tree clean
- **Owner / team**: solo-dev — Eduardo Scarpelli (`eduscarpelli@gmail.com`), GitHub `@MasterDD-L34D`

## Scopo
- **Problema che risolve**: sostituire Claude Max (€200/mese, scade 2026-05-19) con stack AI agentic sovereign a costo ~zero ($0-50/anno), senza perdita materiale di produttività
- **Perché esiste**: (1) filosofia sovereign post-trauma Victus — controllo totale + resilienza offline + zero vendor lock-in; (2) pragmatica economica — $2400/anno vs target sub-$60; (3) registrare decisioni in ADR navigabili per future sessioni (umane o agenti)
- **Risultato concreto atteso**: operatività quotidiana dev post-19/05 senza subscription AI fisse, con evidenza empirica che locale+cloud-free coprono ≥95% workflow

## Pubblico / destinatario
- **Utenti principali**: Eduardo stesso (single-user workstation)
- **Utenti secondari**: future sessioni Claude Code / Aider / eventuali subagent che lavorano su questo repo o sui progetti dipendenti
- **Contesto d'uso**: daily driver dev, 8-10 ore/giorno, workflow Evo-Tactics + Synesthesia + possibili nuovi progetti — ambiente Windows 11 + bash + cmd.exe

## Obiettivo core
- **Job-to-be-done principale**: garantire che al 20/05/2026 esista un *tier-routing documentato, validato empiricamente, stabile* capace di gestire tutti i workflow dev che oggi passano da Claude Max
- **Unità minima che deve funzionare bene**: delega Aider 1-file cosmetic + 1-file behavior-critical (local + cloud) senza silent-corruption e con commit message conformi a policy
- **Cosa NON è importante ora**:
  - Perfezione architetturale ADR retroattiva (ADR-0010 skip MADR retrofit)
  - Subagent ecosystem esteso (catalogo dormiente è ok)
  - Mac mini M4 Pro upgrade (Lenovo basta)
  - Quality-ceiling capability-max (ADR-0015 risolve dopo Fase 6)

## Vincoli

### Vincoli tecnici hard
- RTX 5060 **8 GB VRAM** → tutti i modelli >7-8B dense hanno CPU spill → ctx tuning obbligatorio
- 64 GB RAM → cap modelli ~60 GB loaded (gpt-oss:120b locale NON viable)
- Windows 11 cp1252 console → bug Unicode Aider retry loop (fix preventivo deployato 2026-04-23, validation pending)
- Ollama 0.21.0 non supporta KV cache q4_0 su Blackwell (CUDA error) → q8_0 obbligato
- Privacy: repo cliente MAI cloud; Synesthesia mixed (sovereign per auth, cloud OK per views)

### Vincoli di team / tempo / budget
- **Team**: 1 persona (single-dev, zero delega umana)
- **Tempo**: hard deadline **2026-05-19** (Claude Max expiration). Fase 6 closure target 2026-05-20.
- **Budget target post-Max**: $0-50/anno (free tier Groq+Cerebras + eventuali OpenAI overflow <$20/mese)
- **Budget attuale**: Claude Max €200 già pagato mese corrente; $0.0089 cumulativo dogfood cloud finora

### Vincoli di scope
- NO codice progetti reali in questo repo (scope-creep vietato)
- NO refactor di ADR 0001-0009 a MADR (ROI basso, scelta ADR-0010)
- NO nuovi tool/wrapper speculativi (YAGNI, ADR-0005)
- NO scadenze clienti esterne (è progetto personale)

## Materiali esistenti
- **Repo**: GitHub `MasterDD-L34D/codemasterdd-ai-station` (private), origin/main aligned
- **Documentazione**: `docs/adr/` (14 ADR), `docs/patterns/`, `docs/research/`, `docs/lessons-learned/`, `docs/sessions/`
- **Fonti / reference**:
  - `Archivio_Libreria_Operativa_Progetti/` — framework operativo universale multi-progetto (appena importato 2026-04-23)
  - `final-research-and-snippets-2026-04-21-v3.md` — source material esterno triato
  - `JOURNAL.md` — diario cronologico sessioni significative
- **Asset**: 6 wrapper Aider in `~/.local/bin/`, 4 API keys in `~/.config/api-keys/keys.env`, hook git globali in `~/.local/share/git-hooks/`
- **Conversazioni importanti**: sessione maratona 2026-04-22/23 (14 commit, 3 ADR strategici ratificati) documentata in JOURNAL + memory `project_session_resumption.md`

## Problemi attuali
- **P1** — Dogfood behavior-critical n=1 → statisticamente non significativo per chiusura Fase 6 (target ≥5)
- **P2** — Fix cp1252 deployato ma non validato empiricamente su retry loop reale
- **P3** — Privacy validation reale = 1 sessione su target ≥3 (criterio 3 ADR-0014)
- **P4** — Memoria `project_session_resumption.md` cita HEAD `24d3965` vs reale `a23b533` (drift)
- **P5** — Aggregati mensili `logs/aider-delegation-2026-04.md` da popolare fine mese
- **P6** — Qwen 7B commit-prompt non-compliance (0/6 dogfood), workaround manual-fallback attivo ma non a regime

## Metriche di successo

### Criteri chiusura Fase 6 (tutti-4 AND, da ADR-0014)
1. **Quality bench** ≥10 problemi × ≥5 modelli → ✅ **fatto** (75 test, 100% pass@1, discriminant-limited ma sufficiente per parity)
2. **Reliability dogfood**: n≥20, fail rate <30%, **zero silent-corruption** (attuale: 6/20, 100% success, 0 corruption)
3. **Privacy validation**: ≥3 sessioni reali classificazione repo enforced senza violation (attuale: 1)
4. **Cost tracking**: <$20/mese extrapolato (attuale: ~$0.01 cloud + Max pre-paid)

### Metriche di sostenibilità Fase 8 (post ADR-0015)
- Spesa cumulativa 30 giorni post-Max < $4/mese
- Zero incidenti silent-corruption su workflow reali
- ≥1 revisione qualitativa senza gap materiali a 30 giorni

## Prossimo passo singolo più utile
Eseguire **dogfood behavior-critical cloud #2** (T1 di `SPRINT_01.md`): refactor retry logic su `scripts/quality-bench/run-bench.ps1` via `aider-groq`. Leverage alto perché (a) sblocca P1, (b) valida indirettamente fix cp1252 P2 se entra in retry, (c) produce 1/5 del criterio 2 ADR-0014. Esecuzione <1h.
