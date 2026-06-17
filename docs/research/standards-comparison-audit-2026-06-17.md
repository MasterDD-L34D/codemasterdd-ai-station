# Standards Comparison Audit -- repo vs novita ultimi 30 giorni (2026-06-17)

> Ricerca multi-source fan-out (6 assi paralleli, recency mid-May -> mid-June 2026)
> che confronta contenuti e METODI di questo repo + fleet con lo stato dell'arte.
> Metodologia: ADR-0026 Protocol 2 (autoresearch multi-source, mai one-shot). Ogni
> claim ha fonte datata; i caveat di verifica sono in fondo. ASCII-first (ADR-0021).

## Metodologia

- **Refresh-verify** (Protocol 1): inventario metodi repo da `CLAUDE.md`, `ORCHESTRATION.md`,
  `MODEL_ROUTING.md`, `docs/reference/hardware-and-models.md`, `docs/reference/stack-installed.md`.
- **Fan-out**: 6 agenti research paralleli (1 per asse-metodo), recency 30gg, verdetto
  per-finding (OUTDATED / BORDERLINE / STILL-FINE / ALIGNED / AHEAD / MISSING).
- **Caveat trasversale**: diverse fonti primarie (OWASP genai, Anthropic engineering,
  alcuni vendor blog, Medium) hanno restituito 403 a WebFetch; quei punti poggiano su
  summary di ricerca / aggregatori secondari -- flaggati come tali. La "finestra 30gg"
  e' rispettata dove possibile; alcune release-chiave (Qwen 3.6, OWASP Agentic Top 10)
  sono di aprile/dicembre 2025 ma sono il contesto competitivo corrente -- datate inline.

## TL;DR -- verdetto globale

I **metodi** (la dottrina) sono allineati-o-avanti rispetto al consenso 2026.
Le **versioni concrete** (tool + modelli + label di standard) sono indietro di una
generazione. Nessun cambio di architettura richiesto; serve un **version-refresh** +
3 gap di security/governance da chiudere. Due item hanno urgenza con scadenza.

| Asse | Dottrina/metodo | Versioni/contenuti | Verdetto sintetico |
|------|-----------------|--------------------|--------------------|
| Orchestration | ALIGNED / AHEAD | n/a | mantenere; 1 upgrade opzionale (agent-as-judge) |
| Modelli locali | metodo llmfit AHEAD | OUTDATED (1 gen) | version-refresh: Ollama + Qwen 3.6 / IQ-quants |
| Tool agentici | pattern on-trend | OUTDATED + 1 break | aggiorna Claude Code; fix aider-gemini PRIMA del 18/06 |
| MCP | scoping CORRECT | CURRENT | watch RC 2026-07-28; pin server github |
| Security | posture buona | 3 GAP nuovi | Rule-of-Two, tool-output-untrusted, label OWASP |
| Governance/ADR | AHEAD su ADR | 1 GAP convergente | single-source CLAUDE.md/AGENTS.md |

## Azioni prioritizzate

### P0 -- urgente (scadenza imminente)
1. **`aider-gemini` si rompe il 2026-06-18.** Google ritira Gemini CLI per utenti
   free/Pro/Ultra il 18/06 (folding in Antigravity CLI, annuncio I/O 2026 ~19/05). Il
   wrapper sopravvive SOLO con una API key Gemini paid. Decidere oggi: (a) puntare il
   wrapper su key paid, oppure (b) ritirarlo e spostare quel ruolo su Groq/Cerebras.
   Fonte: Google Developers Blog (ritiro 18/06/2026); The Register (20/05/2026).
2. **Patch hygiene Claude Code GitHub Action.** Se si usa `claude-code-action` /
   `@anthropic-ai/claude-code`, verificare versioni patchate (action v1.0.94 / CLI
   >=2.1.128): prompt-injection da issue/PR untrusted leggeva `/proc/self/environ` e
   leakava `ANTHROPIC_API_KEY` (reported 29/04, patched 05/05; Microsoft Security 05/06/2026).

### P1 -- alto valore, basso rischio
3. **Aggiornare Claude Code 2.1.116 -> 2.1.179** (~63 versioni). Sblocca primitive che
   oggi sono hand-rolled nel repo: worktree nativi (EnterWorktree), subagent annidati
   (5 livelli, 2.1.172), Dynamic Workflows (orchestrazione 10s-100s background agent),
   hook Stop/SubagentStop con `additionalContext` (utile per il verification-gate),
   `fallbackModel` chain (utile per budget post-Max), permessi fine-grained `Tool(param:value)`.
   Default ora Opus 4.8 (la routing "Opus per tutto" regge, solo su default piu' forte).
   Fonte: changelog ufficiale code.claude.com (2.1.154 28/05 -> 2.1.179 16/06/2026).
4. **Aggiornare Ollama 0.21.0 -> 0.30.8** (~9 minor). Sblocca QAT weights (meno memoria),
   speculative decoding (MTP), offload GGUF/llama.cpp migliorato. Fonte: GitHub releases
   (0.30.0 13/05 -> 0.30.8 12/06/2026).
5. **Security GAP -- "Agents Rule of Two" (Microsoft, 05/06/2026).** Un workflow agent
   non deve avere contemporaneamente: (1) input untrusted + (2) accesso a secret + (3)
   tool state-changing/exfil. Una sessione Claude Code che legge PR-content untrusted E
   tiene le key E puo' merge viola tutti e tre -- rilevante per l'autonomy ladder R2.
   Azione: documentare il vincolo in `ORCHESTRATION.md` sec 5 (irreducible residue) e/o
   un mini-ADR. Si lega all'attuale gate ma lo rende esplicito sul triade.

### P2 -- da valutare (eval prima di adottare)
6. **Modelli: version-refresh (famiglia Qwen confermata leader locale).**
   - behavior-slot (oggi `qwen2.5-coder:14b-q2_K`): candidato **Qwen 3.6-27B** (77.2%
     SWE-bench Verified) in Q2/Q3 sul Ryzen 12GB -- stessa giocata "Q2 su VRAM-bound",
     modello piu' forte. Simon Willison: 25.6 tok/s @ 65K ctx (22/04/2026).
   - escalation-slot (oggi `qwen3-coder:30b` MoE): candidato **Qwen3-Coder-Next** (80B/3B
     MoE, 58.7% SWE-bench, 256K ctx) -- stessa architettura expert-offload, drop-in da
     valutare via llmfit + task-eval N>=10.
   - **Quant: testare IQ-quants (IQ3/IQ2 i-quants) al posto di Q2_K** -- il finding
     storico "Q2_K > Q3" va ri-validato contro IQ-series (codebook non-lineari, miglior
     qualita' a parita' di VRAM). Eventuale backend alternativo: `ik_llama.cpp`.
   - Caveat: i bench di MiniMax M3 (01/06) e Kimi K2.7-Code (12/06) sono self-reported e
     comunque NON fleet-relevant (datacenter-scale). Il metodo llmfit+task-eval resta la
     gate giusta proprio perche' i bench nuovi non sono verificati da terzi.
7. **Security GAP -- output di tool come input untrusted (non solo descrizioni/PR).**
   Agentjacking (CSA, 12/06/2026): instructions iniettate in eventi Sentry recuperati via
   MCP -> Claude Code/Cursor/Codex eseguono comandi con i privilegi del dev. Il concern-set
   attuale copre tool-description + PR-content ma non i tool-OUTPUT poisoned ne' il
   supply-chain dei server MCP. Trattare `tavily_search` / `cross_check` output e ogni
   server MCP terzo come supply-chain untrusted (pin + review, no auto-update).
8. **Security label -- aggiornare `owasp-security-auditor`.** Citare **OWASP Top 10 for
   Agentic Applications 2026 (ASI01-ASI10)** (pub. Dic 2025, struttura nuova vs "Agentic
   Skills Top 10"), aggiungendo check ASI06 memory/context poisoning e ASI09 human-agent
   trust exploitation (oggi non nei concern). LLM Top 10 v2026: nomi categorie invariati,
   il riferimento "2025" e' funzionalmente current.
9. **Governance GAP -- single-source CLAUDE.md / AGENTS.md.** AGENTS.md e' ora standard
   convergente sotto Linux Foundation AAIF (letto nativamente da Codex/Cursor/Windsurf/
   Gemini CLI/Copilot); Claude Code NON lo legge ancora nativamente a mid-giugno (issue
   #31005). Il repo gia' tiene entrambi (ADR-0021) ed entrambi human-written (evita
   l'anti-pattern instruction-file LLM-generated). Best-practice emergente: UN canonico,
   l'altro stub/pointer per evitare drift fra due file mantenuti a mano. Azione: nota/ADR
   che fissa quale e' canonico.

### P3 -- watch-list (non adottare ora; coerente con anti-scope ADR-0036)
- **A2A (agent-to-agent)**: standard inter-agent settling sotto Linux Foundation (MCP per
  tool, A2A per agent). Risolve un problema che il setup single-workstation non ha;
  adottarlo ora violerebbe l'anti-scope corretto. Re-valutare solo se uno spoke diventa
  un agente autonomo separatamente hostato.
- **MCP spec RC 2026-07-28** (drop 21/05): stateless core, MCP Apps, Tasks, deprecazione
  `sampling`/`roots`/`logging`. Non tocca un server tool-only come fleet-tools. Conferma
  che `cross_check`-as-tool (NON come MCP `sampling`) era la scelta giusta. Re-check al GA.
- **Agent-as-judge**: il frontiere del verification-gate sposta il judge da "legge il diff"
  a "ESEGUE i test/triage" + pre-layer deterministico + pairwise both-orderings. Upgrade
  opzionale del gate gia' esistente (harsh-reviewer + cross_check cross-family).
- **Spec-Driven Development tooling** (GitHub Spec Kit v0.8.7 07/05; OpenSpec): il repo gia'
  fa specs-first (`docs/superpowers/specs`); opzionale adottare il concetto "constitution"
  (mappa su invarianti CLAUDE.md). Nessuna urgenza.
- **NIST CAISI AI Agent Standards**: control-set non ancora GA (Interoperability Profile
  atteso Q4 2026). Nulla di bindabile oggi. EU AI Act / ISO 42001: solo dev non-deployer
  e' fuori-scope sostanziale; non over-investire.
- **Aider in decelerazione**: 0.86.2 fermo dal 12/02/2026 (~4 mesi). Fork community
  **Aider-CE** ("now official"). 0.86.2 funziona ed e' sovereign-local -> STILL-FINE breve
  termine, ma pianificare: migrare a Aider-CE OPPURE consolidare sovereign-local su
  **OpenCode** (sano, v1.17.7 14/06/2026). Non aggiungere nuova infra Aider-dependent senza
  rivedere questo.

## Dettaglio per asse

### 1. Orchestration -- ALIGNED / AHEAD
Il consenso 2026 si e' indurito su "single-agent-hub by default; multi-agent solo se il
lavoro decompone in sub-task paralleli con context indipendente" -- esattamente l'hub-and-
spoke con subagent isolati + return distillato. Il judge cross-family anti-monoculture e'
ora best-practice NOMINATA (rimedio documentato a self-preference bias / preference leakage).
L'autonomy "human-on-the-loop al merge, auto-merge cauto" e' il default 2026; la ladder
R0->R1->R2 earned e' piu' conservativa. Anti-scope (no LangGraph/CrewAI/AutoGen/LiteLLM per
solo-dev) e' ECHEGGIATO dai vendor stessi. Unico upgrade: agent-as-judge (vedi P3).

### 2. Modelli locali -- metodo AHEAD, versioni OUTDATED
Vedi P2 #6. La famiglia (Qwen Coder) resta la scelta giusta; le versioni specifiche sono
una generazione indietro. Il metodo llmfit (HW-fit shortlist -> task-eval N>=10) e' piu'
necessario che mai dato che i bench dei modelli nuovi sono self-reported.

### 3. Tool agentici -- pattern on-trend, versioni OUTDATED + 1 break
Vedi P0 #1, P0 #2, P1 #3. OpenCode v1.17.7 sano e in crescita (allineato alla scelta repo);
superpowers/claude-mem fine, solo update versioni. Pattern repo (hub + verification-gate +
subagent + worktree) on-trend; upgrade = judge che ESEGUE + worktree/workflow nativi Claude
Code invece di glue custom.

### 4. MCP -- scoping corretto, setup current
Vedi P3. Il rifiuto del completion-routing-MCP (LiteLLM-redux) resta ben allineato: la
convergenza A2A/ACP riguarda agent-interop, non completion-routing -- nessuno standard
emerso giustifica retroattivamente il routing-MCP declinato. Threat dominante = tool-poisoning
da server terzi (VIPER-MCP, 05/2026: 39.884 repo scansionati, 106 zero-day, 67 CVE); il
setup hand-registered in `.mcp.json` ha rischio registry-poisoning quasi-nullo (vantaggio
strutturale). Azione: pin/verify provenienza del server `github`.

### 5. Security -- posture buona, 3 gap nuovi
Vedi P1 #5, P2 #7, P2 #8. Gia' current: storage key file-based ACL'd (migliore di env-inject
CI per l'attacco `/proc/self/environ`), commit-guard + secret-scanning, privacy whitelist,
human-merge boundary su repo esterni. Gap nuovo non coperto: exfil runtime di key via agent
prompt-injected (non via commit) -> Rule-of-Two e' il controllo. Direzione industria: da
env-var plaintext verso short-lived/OIDC + rotation discipline.

### 6. Governance/ADR -- AHEAD su ADR, 1 gap convergente
Vedi P2 #9. Il setup 39-ADR MADR + decisions log + provenance (JOURNAL `CodingAgent`,
trailer commit, `logs/aider-delegation-*`) e' piu' rigoroso della media. Watch-item: ADR
enforceable / "ADR-as-pre-generation-check" (Mneme-style) potra' bolt-on su harsh-reviewer
+ ASCII-guard hook, ma nulla lo forza ora. AI-Act/ISO 42001 fuori-scope per solo-dev.

## Caveat di verifica (onesta)
- ~12+ fonti primarie 403 a WebFetch (OWASP genai, Anthropic engineering, Snyk, alcuni
  vendor): i relativi specifici (wording ASI esatto, percentuali Snyk, alcuni numeri di
  versione Ollama May) poggiano su aggregatori secondari, corroborati ma non verificati
  verbatim. Verificare i numeri SEP MCP e i nomi categorie OWASP sul primario prima di
  citarli in un ADR.
- Claim "Qwen3.6-35B su 6GB VRAM ~30 tps": NON verificato (Medium 403). Trattare come ipotesi.
- Bench MiniMax M3 / Kimi K2.7: self-reported, non re-run da terzi a mid-giugno.
- GitHub MCP scoped al solo repo target -> non e' stato possibile pull diretto delle release
  notes upstream Ollama/llama.cpp (usato GitHub releases public via web).

## Fonti principali
Orchestration: Augment Code (single vs multi-agent 2026); Anthropic effective-context-
engineering; arXiv Agent-as-a-Judge (2601.05111, 08/01/2026); DeepResearch Ninja framework
comparison (05/2026); Zylos A2A/MCP (16/05/2026).
Modelli: DeepLearning.AI The Batch (Kimi/Qwen/DeepSeek); MarkTechPost MiniMax M3 (01/06);
Nerova Kimi K2.7 (12/06); GitHub Ollama releases (0.30.x); Simon Willison Qwen3.6-27B (22/04);
ik_llama.cpp; arXiv llama.cpp quant eval (2601.14277).
Tool: code.claude.com changelog; PyPI aider-chat 0.86.2; OpenCode changelog v1.17.7 (14/06);
Google Developers Blog (Gemini CLI retire 18/06); The Register (20/05).
MCP: blog.modelcontextprotocol.io RC (21/05); arXiv VIPER-MCP (2605.21392); MDPI tool-poisoning
(05/05); Tenable CVE-2025-54136.
Security: OWASP Agentic Top 10 2026 (genai.owasp.org); Microsoft Security CI/CD agentic
(05/06); CSA Agentjacking (12/06); Snyk ToxicSkills (02/2026); Help Net Security Claude
security plugin (27/05).
Governance: MarkTechPost Spec Kit (08/05); Codex KB agent-instruction-files (27/05); GitHub
issue #31005; MADR repo; SureCloud EU AI Act (06/2026).
