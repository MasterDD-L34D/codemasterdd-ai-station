# PROJECT_BRIEF

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/PROJECT_BRIEF.md`.

## Identità del progetto
- **Nome progetto**: CodeMasterDD AI Station (repo: `codemasterdd-ai-station`)
- **Tipo di progetto**: infrastructure-as-code personale + registry decisionale di transizione strategica AI (NON un prodotto, NON una libreria, NON codice di progetti reali — quelli vivono in `Evo-Tactics` e `Synesthesia` separati)
- **Stato attuale**: barra globale 88%, Fase 6 (empirical tracking compressa) al 55% (11/20 dogfood), HEAD `cb2e506` working tree clean, review settimana 2 anticipata ✅ on-track
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
- **Budget attuale**: Claude Max €200 già pagato mese corrente; $0.0148 cumulativo dogfood cloud (0.07% di budget $20/mese) — invariato post dogfood #8-#11 (tutti local)

### Vincoli di scope
- NO codice progetti reali in questo repo (scope-creep vietato)
- NO refactor di ADR 0001-0009 a MADR (ROI basso, scelta ADR-0010)
- NO nuovi tool/wrapper speculativi (YAGNI, ADR-0005)
- NO scadenze clienti esterne (è progetto personale)

## Materiali esistenti
- **Repo**: GitHub `MasterDD-L34D/codemasterdd-ai-station` (private), origin/main aligned
- **Documentazione**: `docs/adr/` (16 ADR, ultimo ADR-0016 Proposed), `docs/patterns/`, `docs/research/`, `docs/lessons-learned/`, `docs/sessions/`
- **Fonti / reference**:
  - `Archivio_Libreria_Operativa_Progetti/` — framework operativo universale multi-progetto (appena importato 2026-04-23)
  - `final-research-and-snippets-2026-04-21-v3.md` — source material esterno triato
  - `JOURNAL.md` — diario cronologico sessioni significative
- **Asset**: 6 wrapper Aider in `~/.local/bin/`, 4 API keys in `~/.config/api-keys/keys.env`, hook git globali in `~/.local/share/git-hooks/`
- **Conversazioni importanti**: sessione maratona 2026-04-22/23 (14 commit, 3 ADR strategici ratificati) documentata in JOURNAL + memory `project_session_resumption.md`

## Problemi attuali
- **P1** — Dogfood behavior-critical n=4 (3 success + 1 REJECT) → gap 1 verso target ≥5
- **P2** — Fix cp1252 deployato ma non validato empiricamente su retry loop reale (8 dogfood consecutivi senza trigger, soglia pazienza n=15)
- **P3** — Privacy validation reale = 1 sessione su target ≥3 (criterio 3 ADR-0014)
- **P6** — Qwen 7B commit-prompt 0% compliance, ma auto-retry post-hook-block validato empirically n=2 (#8 + #11)
- **P7** — Cloud 70B degrada a ~20% compliance su behavior-critical con ≥5 strict constraint (dogfood #7 REJECT). **Driver ADR-0016** (Proposed 2026-04-24, chiude OD-006).

## Metriche di successo

### Criteri chiusura Fase 6 (tutti-4 AND, da ADR-0014) — review sett.2 anticipata 2026-04-24

1. **Quality bench** ≥10 problemi × ≥5 modelli → ✅ **PASS** (75 test, 100% pass@1, discriminant-limited ma sufficiente per parity)
2. **Reliability dogfood**: n≥20, fail rate <30%, **zero silent-corruption** → 🟡 **on-track** (11/20 al 55%, fail rate 9.1%, 0 silent-corruption working-tree)
3. **Privacy validation**: ≥3 sessioni reali classificazione repo enforced → 🟡 **on-track** (1/3, gap attende task Synesthesia reale)
4. **Cost tracking**: <$20/mese extrapolato → ✅ **PASS** ($0.0148 cloud = 0.07% budget)

### Metriche di sostenibilità Fase 8 (post ADR-0015)
- Spesa cumulativa 30 giorni post-Max < $4/mese
- Zero incidenti silent-corruption su workflow reali
- ≥1 revisione qualitativa senza gap materiali a 30 giorni

## Prossimo passo singolo più utile
**Attendere task emergente** per M5 Synesthesia privacy validation (criterio 3 ADR-0014, ancora 1/3). Sprint 01 obiettivi già superati early (11/12 dogfood, 4/3 behavior-critical); forzare ulteriori dogfood artificiali contraddice anti-pattern "non forzare". Pre-closure check formale previsto settimana 4 (~2026-05-17) + preparazione ADR-0015 skeleton. H1 residuo (+1 behavior-critical) e H2 (+3 cosmetic) restano opportunistici su task naturali.
