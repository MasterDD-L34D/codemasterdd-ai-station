---
title: evo-swarm asymmetric redundancy checker -- design (lever 2 of 3)
status: rejected (SDMG falsification 2026-06-20) -- pending rework decision
date: 2026-06-20
owner: Eduardo
author: claude-opus-4-8 (hub, supervised)
scope: evo-swarm (Dafne) verification upgrade -- lever 2 of 3 (asymmetric redundancy checker)
supersedes: none
related:
  - docs/superpowers/specs/2026-06-18-evo-swarm-entity-grounding-gate-design.md (lever 1, landed #124/#125/#126)
  - evo-swarm DECISIONS_LOG Decisione 012 (lever-1 ratify + lever-2 open)
  - docs/adr/0036-unified-orchestration-doctrine.md (fleet-tools cross_check, Decision 5)
  - Game OPEN_DECISIONS OD-022 (swarm canonical validator gate, GATE_THRESHOLD=0.30)
  - evo-swarm camel-agents/dafne_similarity.py (H5 semantic-duplicate gate -- SHADOW-DUPLICATE)
  - evo-swarm scripts/verify-swarm-claims.py (lever-1 verifier + load_canonical_index)
  - Game docs/museum/cards/evo-swarm-run-5-discarded-claims.md (labeled corpus)
  - Game docs/appendici/ALIENA_documento_integrato.md (assi I/E/L embedding fields)
  - last30days research 2026-06-20 (LLM-as-judge reliability, self-preference bias, dedup pitfalls)
  - cross-repo recon 2026-06-20 (5 aree: swarm/Game/codemasterdd/sibling/aa01)
  - L-2026-05-033 (SDMG), L-2026-05-034 (circular validation trap), L-2026-05-035 (currency gate), L-2026-06-041 (negative control)
---

# evo-swarm asymmetric redundancy checker -- design (lever 2 of 3)

## 1. Contesto e problema

Lever-1 (entity-grounding pre-emit gate, landed #124/#125/#126) ferma le allucinazioni di
ESISTENZA: entita inventate, valori canonical sbagliati, category-confusion (parts vs trait).
La recon del corpus run-5 (8 hallucinated + 2 redundant, museum card M-2026-05-08-001) mostra che
TUTTI i 10 scarti erano fallimenti di fatto-canonical -- ma 3 casi (#8 "nuovo stress framework"
quando esiste gia `biomes.yaml > hazard.stress_modifiers`; #9/#10 reinvent-wheel di pattern
gia live) NON sono coperti puliti dall'existence-check di lever-1. Quella e' la classe
**reinvent-wheel / redundancy semantica**: una proposta ben-formata e canonical-consistente che
DUPLICA un pattern/trait/framework gia esistente, sotto un nome o una locazione diversa.

L'existence-check non la prende perche la proposta non e' "inesistente" -- e' "gia esistente
altrove". Serve un giudizio di SIMILARITA semantica vs il canon, non un lookup binario. E qui
scatta il rischio confirmation-bias: se il giudice e' della stessa famiglia-modello del
generatore (entrambi Ollama-local), condivide i blind-spot. La research last30days 2026-06-20
quantifica il problema: i judge LLM premiano la propria famiglia +10-25% (self-preference bias),
nessun judge e' affidabile in modo uniforme (>50% errore su bias-benchmark hard). La doctrine
ADR-0036 Decision 5 nomina la cura: un giudice di **famiglia-modello diversa** (anti-monoculture)
via il tool gia ratificato `cross_check`.

**Recon-gap evitato (lezione lever-1).** La recon cross-repo (2026-06-20) ha trovato che il
retriever/similarity che lo spec avrebbe potuto "costruire da zero" ESISTE GIA: `dafne_similarity.py`
(gate H5: embedding nomic-embed-text + Jaccard fallback, `check_semantic_duplicate`, soglie 0.75
embed / 0.15 Jaccard, gia hard-gate in `dafne._execute_create_agent:517` per dedup AGENT).
Lever-2 NON ricostruisce un similarity engine -- riusa le funzioni pure di dafne_similarity e il
loader canon di lever-1. Vedi sez. 4.6 (shadow-duplicate).

## 2. Goal e non-goals

**Goal.** Dare allo swarm un segnale ADVISORY di redundancy semantica: per ogni artifact che ha
passato lever-1, stimare quanto duplica un pattern canonical gia esistente, usando un giudice di
famiglia-modello diversa dai generatori (anti-monoculture), e fornire il segnale a Dafne perche
lo pesi nella sua valutazione di qualita -- senza auto-reject.

**Non-goals (espliciti, OUT da questo spec):**
- Hard-gate / auto-reject. Lever-2 e' ADVISORY (vedi D2). La redundancy e' un giudizio, non
  ground-truth; SDMG + research dicono di non hard-gate un giudizio.
- Generic value-judgment (balance / plausibilita / tono). NON evidenziato dal corpus run-5 =
  scope speculativo, scartato (D1).
- Sostituire o estendere il gate H5 dafne_similarity (agent-dedup). Lever-2 e' ortogonale, a uno
  stadio diverso (sez. 4.6).
- Lever-3 (constrained schema-output Ollama `format`). Follow-up spec separato.
- Riattivare lo swarm. Resta PARKED; lever-2 e' validato OFFLINE su corpus.
- Full entity-extraction su prosa (gia residuo noto di lever-1).

## 3. Decisioni ratificate

| # | Decisione | Razionale |
|---|-----------|-----------|
| D1 | Scope = redundancy semantica (reinvent-wheel), NON generic value-judgment | Unica classe del corpus run-5 non coperta pulita da lever-1 (#8/#9/#10). Data-grounded, falsificabile. Il value-judgment ampio non ha evidenza (lezione recon-gap). |
| D2 | Verdict = ADVISORY (redundancy_ratio a Dafne), NON hard-gate | La redundancy e' un giudizio semi-soggettivo, non ground-truth (D4 lever-1). Research: nessun judge affidabile uniforme; non hard-gate un giudizio. Rispetta il ruolo coordinatore di Dafne. |
| D3 | Architettura = retrieve-then-judge, swarm-local | Retriever (cheap, locale) restringe i candidati; judge (different-family) decide solo sullo shortlist -> minimizza costo cloud e taglia i false-positive (multi-stage, research dedup). |
| D4 | Judge = famiglia-modello DIVERSA dai generatori Ollama (cross_check Gemini primary, Groq fallback) | Anti-monoculture (ADR-0036 D5, L-034 circular-validation-trap). Self-preference bias +10-25% se stessa famiglia. Gemini (Google) e Groq (Meta-LLaMA) = signal indipendente dal qwen/mistral Ollama. |
| D5 | Build-on-existing: riusa dafne_similarity (funzioni pure) + load_canonical_index (lever-1) + dafne_groq (judge fallback) + cross_check MCP-contract | Anti-shadow-duplicate (agent-scanner, recon-before-build). NESSUN nuovo similarity engine, NESSUN nuovo canon loader, NESSUN nuovo llm_call MCP (gia SDMG-rejected). |
| D6 | Rule-of-Two = drop documentato + at-call key | Lever-2 tiene 3/3 capability [untrusted input, secret access, state-change]. Mitigazione: key lette at-call da keys.env (pattern dafne_groq, mai hardcoded/persistite/loggate), egress = testo game-design non-secret. Drop documentato qui (vedi 5.5). |

## 4. Architettura

### 4.1 Locus

Il gate gira swarm-local, nello stesso punto di lever-1: dopo che l'artifact e' prodotto e ha
passato `entity_grounding_gate`, PRE-score in `swarm_loop._run`. A differenza di lever-1 NON
hard-rejecta: calcola un segnale e lo allega. Sovereignty (D2 lever-1): retriever + judge dentro
`camel-agents/`, nessun coupling runtime Game-side.

### 4.2 Componente: retriever (build-on-existing)

Single-purpose. Input: artifact (assi A.L.I.E.N.A. estratti) + corpus canon. Output: top-K
candidati canonical simili.

- Corpus = `load_canonical_index()` (lever-1, verify-swarm-claims.py) + indice delle proposte
  storiche (dafne-proposals.json active + rejected). NESSUN rebuild del loader.
- **Fast-path Tier-1 fuzzy** (`_normalize_for_match` / Levenshtein di verify-swarm-claims) PRIMA
  dell'embedding: un match ovvio per nome non spende una chiamata embedding/cloud.
- **Embedda SOLO assi I/E/L** (A.L.I.E.N.A.: I=morfologia, E=ecologia, L=pressioni evolutive --
  ALIENA_documento_integrato). Skip A/N/A2 (narrativi: il lore originale non e' un asse di
  duplicazione) e i field-name (Tier-3 stopwords). Questo e' cio che rende il segnale "redundancy
  di sostanza" e non "redundancy di prosa".
- kNN cosine via Ollama `nomic-embed-text` (stesso modello di H5 = efficienza, gia pullato).
  **top-K=5** (research: top-1->top-3 alza i FP; K basso + judge stage-2 che filtra).
- Indice persistito (.pkl/.json) con invalidation su change game-repo o proposals.json
  (currency gate L-035: pin versione embed-model + snapshot canon; stale-embed + fresh-canon = FP
  silenziosi).
- Fallback: nomic-embed unavailable -> funzioni pure Jaccard/cosine di dafne_similarity con
  confidence ridotta (circuit-breaker, loud WARNING).

### 4.3 Componente: judge (different-family, ladder)

Single-purpose. Input: artifact + i top-K candidati. Output: verdetto redundancy strutturato.

- Ladder con label provider su ogni step:
  1. primary: `cross_check(model='gemini-2.5-flash', prompt=construct_redundancy_prompt(...))`
     -- contratto fleet-tools (gemini* -> Gemini, else Groq). GEMINI_API_KEY confermata presente
     in keys.env (recon 2026-06-20).
  2. fallback: `dafne_groq.call_groq_api(system, user)` (llama-3.3-70b, gia nativo nello swarm).
  3. tertiary: Ollama-local `qwen3:8b` (loud, confidence ridotta -- viola anti-monoculture, solo
     come degradazione last-resort, mai default).
- Prompt: NON embedda l'istruzione-modello (il routing e' per prefix del param `model`). Rubrica
  esplicita: `NOVEL=0.0 / MOSTLY_NOVEL=0.33 / SIMILAR=0.67 / DUPLICATE=1.0`. Istruzione chiave:
  "lore originale da solo NON redime una duplicazione morfologica/ecologica (assi I/E/L)".
- Anti-sycophancy (research: position/verbosity/self-pref bias): randomizza l'ordine
  artifact-vs-candidati; giudica sul merito, mai sull'autorita dell'agent-autore.

### 4.4 Verdict e output (advisory)

Dict advisory, mai dentro proposal.json:
```json
{
  "redundancy_ratio": 0.0,
  "top_k_similar": [{"id": "...", "sim_score": 0.0, "differing_axes": ["E"]}],
  "judge_verdict": "NOVEL|MOSTLY_NOVEL|SIMILAR|DUPLICATE",
  "reasoning": "...",
  "judge_model": "gemini-2.5-flash",
  "confidence": 0.0
}
```
- Allegato come `co02_semantic_redundancy` (parallelo a `co02_validation` / lever-1
  `hallucination_ratio`). Backward-compat: chiave assente = non-ancora-scored.
- NO auto-reject. Dafne lo legge in `assess()` / `intervene()`, lo surface in `focus_directive`,
  flag se `redundancy_ratio >= 0.7`. Override sempre possibile (ruolo coordinatore).
- Score integration (DECISIONS_LOG 008): `final_score = base * (1 - hallucination_ratio*0.5) *
  (1 - redundancy_ratio*0.3)`. **Coefficienti TBD** -- da tunare su 223 artifact storici (Quality
  Gate, vedi 9). Soglia OD-022 `GATE_THRESHOLD=0.30` (ratio-gate, advisory) e soglia-flag UI 0.7
  sono cose diverse: la prima e' il segnale di REJECT-suggestion, la seconda l'alert a Dafne.

### 4.5 Data flow

```
artifact (ha passato entity_grounding_gate)
  -> extract assi I/E/L
  -> retriever: fuzzy fast-path -> nomic-embed kNN (top-K=5) su canon+proposals
       -> top_k_similar[]
  -> judge ladder (gemini -> groq -> ollama): redundancy verdict su artifact vs top_k
       -> {ratio, verdict, reasoning, judge_model, confidence}
  -> allega co02_semantic_redundancy -> telemetry/artifact (NON proposal.json)
  -> Dafne assess: pesa ratio, flag se >=0.7, override possibile (NO auto-reject)
```

### 4.6 SHADOW-DUPLICATE: dafne_similarity (load-bearing)

`camel-agents/dafne_similarity.py` E' GIA un gate semantic-duplicate completo (H5): embedding
nomic-embed + Jaccard, `check_semantic_duplicate`, hard-gate auto-reject in
`dafne._execute_create_agent:517` (soglie 0.75 embed / 0.15 Jaccard).

- **Rischio**: ricreare un retriever/similarity = shadow-duplicate (viola agent-scanner / OD-007 /
  recon-before-build).
- **Risoluzione**: lever-2 e' ORTOGONALE, non sostitutivo. H5 = hard-block agent-dedup
  pre-propose (dominio: proposte di nuovi AGENT vs agents_index). Lever-2 = advisory su redundancy
  di CONTENUTO-DESIGN (specie/trait/biome/framework) vs canon Game. Stadi e domini diversi,
  coesistono. Lever-2 riusa le funzioni PURE (cosine/jaccard/tokenize) come fallback, ma il judge
  DEVE essere different-family. NON estendere il hard-gate H5.
- **Azione (refactor pre-crescita)**: estrarre `camel-agents/similarity_common.py` (stopwords +
  tokenize) condiviso da dafne_similarity / agent-similarity-gate / lever-2 retriever, PRIMA di
  aggiungere codice. (Anche valutare `tools/py/lib/canonical_loader.py` per dedup loader
  cross-repo: swarm_canonical_validator.py + check-canon-consistency.cjs + verify-swarm-claims --
  enhancement, non MVP.)

## 5. Error handling e edge case

### 5.1 Fail-open-but-loud (raffinamento lever-1 sez.11)

Lever-2 e' advisory: un giudice mancante costa un SEGNALE, non un loop fermo.
- embed-model down -> Jaccard fallback (confidence ridotta) o `{ratio: null, reason:
  'embedding_model_unavailable'}`; artifact passa.
- judge timeout (30s) -> next judge nel ladder; se tutti falliscono -> `{ratio: 0, judge_timeout:
  true}` loggato; artifact passa.
- kNN corpus vuoto (first run) -> pass silenzioso.
- kNN malformed -> log WARNING, candidate-list vuota -> pass.
- Mai silent-fail, mai false-VERIFIED, mai halt dello swarm.

### 5.2 Currency gate (L-2026-05-035)

Pin/timestamp su versione `nomic-embed-text` + snapshot canon. Indice embedding invalidato su
change game-repo o proposals.json. Stale-embed + fresh-canon = false-positive silenziosi -> il
pin li rende visibili.

### 5.3 Threading

Retriever read-only su proposals/index: rispetta `PROPOSALS_LOCK` / `AGENTS_INDEX_LOCK` (dafne.py).
Judge output non-mutating.

### 5.4 OD-007 / Source Authority alignment

Lever-2 DEVE leggere la stessa sorgente canon di lever-1. La recon ha trovato la Source Authority
Map A2 documentata: biome PRIMARY = `packs/evo_tactics_pack/data/biomes.yaml`, species =
`data/core/species/species_catalog.json` (v0.4.3+). Lever-1 attualmente legge `data/core/biomes*`
(divergenza OD-007). Implementazione lever-2 e' BLOCCATA su OD-007 finche la SoT biome non e'
riconciliata (non bloccante per il design; vedi 9).

### 5.5 Rule-of-Two -- drop documentato (D6)

Lever-2 tiene 3/3 capability: untrusted-input (testo proposta agent), secret-access (API key
judge), state-change (ratio entra nello score). Lo swarm e' un runtime Python detached, NON un
client MCP, e gia tiene GROQ_API_KEY (Dafne active). Mitigazione adottata (NON full
session-isolation MCP, impossibile dato l'arch detached):
- key lette at-call da `~/.config/api-keys/keys.env` (pattern dafne_groq: `os.environ` al momento
  della chiamata, redatte nei log, mai hardcoded, mai persistite negli artifact).
- egress consapevole: il testo delle proposte (game-design content) va a Gemini/Groq. Non sono
  secret; rischio-egress basso. Documentato qui.
- Drop esplicito della mitigazione full-isolation, accettato (D6) con queste compensazioni.

## 6. SDMG falsification plan (load-bearing)

Metodo self-designed = IPOTESI finche non falsificato esternamente (L-2026-05-033, ADR-0026
Protocol 7). Lever-2 NON e' trusted -- e lo swarm NON e' riattivato -- finche questo non passa.

**6.1 Labeled corpus (esiste).** Stesso run-5 corpus (museum card).
- REDUNDANT (deve flaggare ratio alto): #8 stress-framework, #9 schema-location, #10 stress-system.
- NOVEL (deve NON flaggare): trio OD-012 known-good (magnetic_rift_resonance ecc.) + proposte
  genuinamente nuove. Distinto da lever-1: un artifact puo essere VERIFIED (lever-1) ma REDUNDANT
  (lever-2).

**6.2 Metriche.** Confusion matrix redundancy distinta da lever-1: recall sui 3 redundant,
precision sui known-novel (zero false-flag). N=3 redundant = SOLO direction-probe. Ratify a
**N>=40** casi sintetici (N-sample: N=10 non ratifica una metrica). La research conferma: 100
esempi = statisticamente affidabile, 500+ per slice.

**6.3 Negative-control (L-2026-06-041, anti-vacuous-test).** Inietta un known-duplicate noto ->
assert flag (ratio alto), E un known-novel -> assert pass. Prova che il gate advisory non e' un
no-op silenzioso (fail-open puo degenerare in flag-nothing).

**6.4 External falsification (mandatory pre-wire).** harsh-reviewer different-model (ortogonale
all'autore del design) rivede il design + i risultati corpus PRIMA del wiring live; blocca merge
fino ad ACCEPT. Dogfood: far girare il giudizio redundancy anche via `cross_check` per una
second-opinion non-Claude sul design stesso.

## 7. Testing

- Modulo isolato `camel-agents/semantic_redundancy_gate.py` + CLI
  `scripts/verify-semantic-redundancy.py <artifact.json> --game-repo PATH` (mirror dell'interface
  verify-swarm-claims). API pubblica `check_semantic_redundancy(artifact, corpus_embeddings,
  judge_callable)` (judge injectabile = testabile con mock).
- Unit: retriever kNN (mock embedding/vettori stub), fuzzy fast-path, judge ladder routing
  (mock Gemini/Groq/Ollama, no-key), fail-open ladder, currency-invalidation.
- Pattern test come `test_dafne_similarity.py`: unit mock + integration live separata.
- Edge: corpus vuoto/all-rejected, Ollama down, Groq 403, Gemini timeout, JSON malformato,
  atomic-write non corrompe proposals/index.
- Corpus + negative-control (6.1-6.3) come test ripetibile.
- TDD: test prima del modulo (Definition of Done repo).

## 8. Rollout (parked-safe)

1. Refactor: estrarre `similarity_common.py` (4.6) -- PRIMA del nuovo codice.
2. Implementa retriever + judge + gate (dietro lo stato PARKED).
3. SDMG falsification (sez. 6) OFFLINE su corpus -- nessun swarm run.
4. harsh-reviewer external falsification; fix findings.
5. Land via branch + PR su evo-swarm; merge = Eduardo. DECISIONS_LOG entry su ratify.
6. Quality Gate: tuning coefficienti score su 223 artifact storici (metrica delta before/after).
7. Attivo per il PROSSIMO swarm run (quando Eduardo riattiva) -- non triggera riattivazione.

Reversibilita: advisory + env-flag; disabilitarlo non cambia il comportamento di accept (il
coefficiente redundancy_ratio degrada a 1.0 = no-op). Nessun canon mutato; read-only sul SoT.

## 9. Open questions / follow-up

1. **OD-007 SoT biome (BLOCCANTE impl, non design)**: riconciliare la sorgente biome (lever-1
   legge data/core; Source Authority Map A2 dice packs/ primary). Lever-2 deve leggere la stessa
   di lever-1.
2. **Coefficienti score** (`0.5` halluc / `0.3` redund): TBD, tuning empirico su 223 artifact
   (Quality Gate step 3). `GATE_THRESHOLD=0.30` (OD-022) vs flag 0.7 = due cose diverse.
3. **Biome/asse field-name discovery**: step-1 impl DEVE dumpare i field reali live (es.
   `biome_affinity`, body_plan, trait_refs) -- non assumere il naming.
4. **harsh-reviewer pre-wire**: confermare chi/quale modello fa la falsificazione ortogonale
   (non l'autore). Candidati: harsh-reviewer (codemasterdd/.claude/agents) + cross_check dogfood
   + aa01 critic-redteam.
5. **codemasterdd ADR**: differito (DECISIONS_LOG 012). Un ADR unico full-arc (lever 1-2-3 +
   recon-gap lesson + OD-007 finding) dopo che lever-2 produce dati.
6. **Lever-3** (constrained schema-output Ollama `format`): follow-up spec; rende i
   canonical_refs strutturalmente obbligatori (chiude il residuo undeclared-in-prose).

## 10. Riferimenti

- evo-swarm: scripts/verify-swarm-claims.py (load_canonical_index, lever-1), camel-agents/
  dafne_similarity.py (H5 shadow-duplicate), dafne_groq.py (judge fallback), orchestrator.py +
  swarm_loop.py (locus), agent-similarity-gate.py (tokenize da estrarre)
- codemasterdd: apps/fleet-tools-mcp/server.mjs (cross_check), docs/adr/0036 (Decision 5),
  docs/adr/0026 (SDMG Protocol 7), docs/governance/actor-activation-criteria.md (Rule-of-Two,
  different-family judge gate item)
- Game: docs/museum/cards/evo-swarm-run-5-discarded-claims.md (corpus), docs/appendici/
  ALIENA_documento_integrato.md (assi I/E/L), OPEN_DECISIONS OD-022, tools/py/
  swarm_canonical_validator.py (dataclass skeleton), scripts/check-canon-consistency.cjs
- lessons: L-2026-05-033 (SDMG), L-2026-05-034 (circular validation trap), L-2026-05-035
  (currency gate), L-2026-06-041 (negative control)
- research: last30days 2026-06-20 (LLM-as-judge self-preference bias +10-25%, no judge uniforme,
  retrieve-then-judge multi-stage, embedding dedup FP/threshold pitfalls)
- recon: cross-repo synthesis 2026-06-20 (5 aree, 484k tok, shadow-duplicate finding)

## 11. Falsification outcome (SDMG, 2026-06-20) -- VERDETTO REJECT

Panel adversariale a 3 lenti (feasibility / metodologia / sicurezza), verificato su codice
reale. Verdetto: **REJECT**. Per SDMG i finding si adottano, non si difendono. 10 P1
ship-blocking; i 4 temi:

1. **Meccanismo sbagliato per il target (P1-A/B/C, P1-G).** I casi run-5 #8/#9/#10 sono
   redundancy STRUTTURALE di schema biome (`hazard.stress_modifiers` + `stresswave`), sull'asse
   A-Ambiente -- la spec ha droppato A confondendo A-Ambiente con A-Ancoraggio narrativo, e ha
   puntato l'embedding sugli assi SPECIE I/E/L. Inoltre: `load_canonical_index` harvesta solo
   IDs/names (0 match su hazard.stress_modifiers -> niente da recuperare); gli artifact reali
   sono prosa non strutturata (nessun asse da estrarre). E "different-family" (LLM su prosa LLM)
   non da' indipendenza di MECCANISMO (L-034) -- serve un asse non-LLM strutturale come segnale
   primario, judge LLM demoto a secondario.
2. **Judge irraggiungibile + safety falsa (P1-D, P1-J).** `cross_check` e' MCP-only, non
   invocabile dal runtime Python detached -> la ladder collassa a Groq (anti-monoculture
   fallisce). L'unico path Gemini in-swarm mette la key in URL (viola D6). La R2-mitigation
   "key at-call mai persistita" e' falsa (`dafne_groq` legge os.environ; START-SWARM carica tutti
   gli 11 secret nell'env detached); una spec non puo' auto-concedersi il drop R2 (serve ADR).
3. **Validazione impossibile come scoped (P1-F/H/I, P3).** Corpus positivo = N=1 (3 istanze
   quasi-identiche, #8 mislabeled HALLUCINATED). 223 artifact storici tutti rejected -> zero
   positivi novel-and-good per calibrare precision/score. La formula score attribuita a
   DECISIONS_LOG 008 NON esiste (grep). Advisory + fail-open + override = metrica live
   infalsificabile (no-op e gate-funzionante indistinguibili).
4. **OD-007 = blocker di correttezza (P1-E), non differibile.** Lo swarm legge un corpus biome
   corrotto (40 ids incluso il sentinel 'aliases', vs 27 pack reali) -> flag DUPLICATE contro
   ~13 phantom + miss dei duplicati pack-only reali.

Cosa regge: locus + primitive judge-ladder esistono; recon build-on-existing onesto (cosine/
jaccard/tokenize riusabili); OD-007 reale; GEMINI key presente. Postura advisory sana come
intento (il difetto e' la non-falsificabilita', non la prudenza).

Conseguenza: lo spec NON procede a writing-plans. Decisione di rework/park aperta (vedi PR
codemasterdd#400 + sessione 2026-06-20).
