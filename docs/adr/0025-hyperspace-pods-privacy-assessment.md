# ADR-0025 -- Hyperspace Pods privacy assessment (NO-GO empirico)

> *TL;DR: Hyperspace Pods (P2P AI Compute Clusters via libp2p) **NO-GO definitivo** per stack sovereign codemasterdd. Verdict basato su empirical trial 30s daemon `v5.73.8` (AA01 task aa01-001 decisions D-017 + D-018) condotto **2026-05-10 sera / 2026-05-11 mattina** (sessione precedente). 3 finding architetturali non-config-fixable: (1) auto-update FORCED 680 MB on startup, NO opt-out; (2) **local Ollama models auto-esposti** alla network 2M+ peer **senza consenso** (`Loading ollama:qwen2.5-coder:7b: 0%` visible nei log daemon startup); (3) pulse round voting ATTIVO con isolation flags `--no-agent --no-research --no-causes --no-api --profile relay`. Empirical pktmon capture (120149 pkt outbound in 3 min): **30+ destinazioni IP TUTTE PUBBLICHE** (DigitalOcean bootstrap pool + GitHub Releases CDN + Cloudflare + GCP + Contabo VPS + CherryServers), **zero traffic LAN despite `--pod eduardo-trial-1node`**. Pivot decisione: **llama.cpp RPC** primary candidate (sovereign-pure, LAN-only by design, MIT open source) + **llama-server REST API** single-node Lenovo viable (76 tok/s Qwen 7B Q4 CUDA, D-019/D-022).*

- **Status**: **Accepted** (2026-05-12 auto-ratified) -- soft-default ratification anticipata via Eduardo authorization "fai tutti i residual possibili in auto" 12/5 sera
- **Data**: 2026-05-11 (originale) / 2026-05-12 (ratification)
- **Decisore**: Eduardo Scarpelli
- **Deciders**: solo-dev
- **Supersedes**: nessuno (Hyperspace era REFERENCE-only)
- **Related**: AA01 task `2026-05-aa01-001-2026-05-10-fleet-discovery-pod-design` decisions D-001 to D-022

## Ratification note (2026-05-12 sera auto)

Auto-ratified Proposed -> Accepted via Eduardo authorization "fai tutti i residual possibili in auto" 12/5 sera. Empirical support cumulative:
- D-017 99% confidence empirical 30s daemon trial (2026-05-11 mattina)
- pktmon evidence 120149 pkt outbound 3 min, 30+ destinazioni IP TUTTE PUBBLICHE
- 3 finding architetturali non-config-fixable verified empirico
- L-2026-05-002 Hyperspace audit cycle lesson promoted (3 anti-pattern + 4 pattern positive)
- aa01-003 web-only audit REJECT archived (duplicate cycle confermato)
- AMEND ADR documentato (process honesty note)
- Cross-session value: lesson L-002 cumulative methodology framework

Reversibility: Eduardo puo' revert via amend ADR (Status -> Proposed) se discovery future change verdict. Pivot llama.cpp single-node Lenovo PASS confermato D-019/D-022, multi-node SPRINT_03+.

## Process honesty note

Questo ADR è stato inizialmente scritto **2026-05-11 notte** in AA01 task aa01-003 con verdict **CONDITIONAL GO** basato su autoresearch web-only multi-source (6 fonti). **AMEND post discovery** (2026-05-11 notte+1): refresh-verify state interno mancato → task aa01-001 fleet-discovery aveva già completato audit empirico 30s daemon trial con verdict opposto NO-GO definitivo (D-017, 99% confidence). Mio audit web-only ha DUPLICATO 4-5h di lavoro empirico + reached verdict ERRATO (CONDITIONAL GO) perché empirical trial 30s ha rivelato 3 finding architetturali che documentazione pubblica + autoresearch web NON espongono.

Lesson L-2026-05-002 (in promotion da DRAFT aa01-001 fleet-discovery): empirical trial breve > documentation cycles per architectural decisions, anti-pattern "documentation ground truth assumption". Memory `feedback_governance_refresh_verify` violata in mia sessione 2026-05-11: pre-edit refresh state INTERNO mancato.

## Context and Problem Statement

Memory `reference_hyperspace_pods.md` (added 2026-05-10) REFERENCE-only fase 1 con audit privacy P2P required PRE-install. Hyperspace Pods strategic candidate per scenario distributed inference codemasterdd (Mac mini extension alternative, device pooling family).

Hardware compat OK (RTX 5060 8GB qualifies VRAM minimum 4GB + Ryzen 4070 SUPER 12GB compatible).

Audit trail completo:
1. **2026-05-10 sera**: AA01 task aa01-001 fleet-discovery startato + audit Phase 4 originale web-only → verdict CONDITIONAL GO (DRAFT/02)
2. **2026-05-10 sera**: D-007 NO-GO premature post one-shot README re-audit
3. **2026-05-10 sera**: D-009 CONDITIONAL GO RESTORED post Eduardo pushback + autoresearch multi-source
4. **2026-05-11 mattina**: D-011 pivot exo (basato su Archon 7-step + multi-source autoresearch); Hyperspace ABANDON
5. **2026-05-11 mattina**: D-013 abandonment exo (Windows non supportato falsified) + pivot Ollama+SSH
6. **2026-05-11 mattina**: D-015 RE-FRAME goal + Hyperspace v5.x re-evaluation (Archon 7-step) → CONDITIONAL GO restored Phase 6-sextus
7. **2026-05-11 mattina**: **D-017 empirical trial 30s daemon Hyperspace v5.73.8 → NO-GO DEFINITIVO 99% confidence**
8. **2026-05-11 mattina**: D-018 pivot llama.cpp RPC primary candidate
9. **2026-05-11 mattina**: D-019 Phase 6-septies llama.cpp PASS Lenovo standalone (Qwen 7B Q4 CUDA, 76 tok/s tg32, ~5060 sm_120)
10. **2026-05-11 mattina**: D-020/D-021 Phase 7-septies BLOCKED (DESKTOP AVG quarantine + rpc-server silent-exit Windows bug)
11. **2026-05-11 mattina**: D-022 Option D llama-server REST API smoke PASS Lenovo (0.34s latency 50-token chat completion)

22 decisions documentate in `aa01/workspace/2026-05-aa01-001-2026-05-10-fleet-discovery-pod-design/decisions.md`.

## Decision

**NO-GO Hyperspace adoption per use case sovereign codemasterdd.**

Tutti i 3 finding architetturali emersi durante empirical trial 30s daemon Hyperspace v5.73.8 (D-017) sono **architetturali, non config-fixable**:

### Finding empirico 1 -- Auto-update FORCED at startup, NO opt-out

- Daemon scarica v5.73.8 → v5.73.9 (680 MB) IMMEDIATAMENTE su startup
- Anche con manual zip install user-dir + service NON registrato
- Updater logic dentro al binary, NON solo timer Linux/macOS files
- Mitigation tentata pre-install (manual zip extract) NON sufficiente
- Bug osservato: "[UPDATE] Wrote v5.73.9 but launcher on disk still reports vunknown. Auto-update paused for 0h to avoid restart loop." -- "0h" suggerisce bug stato

**Implication**: sovereign principle "audit-then-replay" violato architettura -- binary cambia post-install senza consenso utente. Reproducibilita' build impossibile.

### Finding empirico 2 -- Local Ollama models auto-esposti SENZA CONSENSO (privacy violation severa)

- Log daemon startup: "Loading ollama:qwen2.5-coder:7b: 0%"
- Daemon ha scoperto Ollama locale Lenovo + sta caricando IL Qwen 7B locale per esporlo come inference resource alla network 2M+ peer
- Documentation feature ("Discovers and uses locally installed Ollama models out of the box") era opt-in implicito MA empirical e' **opt-out only** (richiede uninstall Ollama o disable Hyperspace)
- **Implicazione PRIVACY GRAVE**: sovereign-only stack codemasterdd Lenovo (Aider + OpenCode + Ollama 8 modelli) sarebbe esposto al network al primo daemon start
- Behavior NON documented in changelog / README / Twitter announcement

### Finding empirico 3 -- Pulse round voting ATTIVO despite isolation flags

- Log: "[NETWORK] -> Elected for pulse round"
- Pulse rounds = network consensus voting (parte sistema economic incentive USDC)
- Flags `--no-agent --no-research --no-causes --no-api --profile relay` NON disabilitano pulse participation
- Conferma: even minimal-relay node partecipa al consenso economic-incentive network-wide
- "1-node Pod" framing marketing != architectural isolation reale

### Pktmon capture analysis (D-018, 120149 pkt 3 min)

Empirical network monitoring durante 3-min daemon run con `--pod eduardo-trial-1node --no-agent --no-research --no-causes --no-api --profile relay --mode chill --headless`:

- **120149 pkt outbound** in 3 min
- **30+ destinazioni IP uniche, TUTTE PUBBLICHE** (zero traffic LAN 192.168.1.0/24 fleet)
- Provider mappati: DigitalOcean (5+ IPs Hyperspace bootstrap pool), GitHub Releases CDN (auto-update download), Cloudflare (assets hyperspace.sh), Google Cloud, Contabo VPS, CherryServers VPS
- Top destinations: 138.197.168.9 (DO, 26460 pkt), 64.225.82.25 (DO, 25065 pkt), 185.199.110.133 (cdn-185-199-110-133.github.com, 14112 pkt)
- **Implicazione**: `--pod <name>` flag NON isola routing-level. Daemon partecipa al global P2P regardless.

### Aggravanti accessori

- AVM Windows non in release matrix (404)
- Chain blockchain Windows non disponibile (404)
- AES-GCM JS fallback (no Rust addon Windows secondary)
- Pod scope `--pod eduardo-trial-1node` NON ha prevented network connection
- Capture pktmon riempito da auto-update download 680 MB vs inference traffic

## Path forward: llama.cpp RPC primary candidate

Decision D-018 + empirical validation D-019/D-022:

### Razionale llama.cpp RPC

- **License**: MIT (open source, audit-then-replay possibile)
- **Windows binary native**: ggml-org/llama.cpp Releases CUDA 13.1 builds
- **LAN-only by design**: security warning explicit "Never run on open networks"
- **Pure sovereign**: no bootstrap, no telemetry, no auto-update, no economic system
- **Heterogeneous CUDA**: 5060 sm_120 + 4070S sm_89 + 2070S sm_75 + 1050Ti sm_61 supportato via tensor-split
- **GGUF compat**: Ollama models reusable (no duplicate download)

### Validation empirica (D-019/D-022)

**Single-node Lenovo PASS** (Phase 6-septies):
- llama.cpp Windows CUDA work confirmed: RTX 5060 sm_120 detected, ggml-cuda.dll loaded
- Performance baseline Qwen 7B Q4: pp16 931 tok/s + tg32 **76 tok/s** CUDA Lenovo
- Performance vs Ollama: 76 vs 114 tok/s = -33% slowdown (Ollama piu' veloce single-node, llama.cpp unlocks distributed via RPC)
- llama-server REST API Option D PASS: 0.34s latency 50-token chat completion (OpenAI-compatible `POST /v1/chat/completions`)

**Multi-node Phase 7-septies BLOCKED tonight** (D-020/D-021):
- DESKTOP-B9L203E: AVG Antivirus quarantine 41 file post-extract (1 sopravvive: `libomp140.x86_64.dll` MS-signed). Eduardo manual UI AV exclusion needed
- DESKTOP-B9L203E driver 536.99 -> max CUDA 12.2 (incompat llama.cpp CUDA 12.4 + 13.1, needs driver update >=545)
- LAPTOP-D73A8DIE went to sleep durante test
- rpc-server CPU-only Windows: silent-exit 10s no error message (b9097 build bug hypothesis)

### Trade-off llama.cpp RPC accettato

- **POC stage**: fragile, manual config (vs Ollama auto-discovery)
- **Manual peer discovery**: no auto-discovery, comma-separated addresses
- Mitigation: Phase 6-septies + 7-septies trial empirical incremental

## Options considered

### Opzione A -- NO-GO Hyperspace + pivot llama.cpp RPC (scelta)

Validato empirically via aa01-001 22 decisions audit cycle.

**Pro**:
- Sovereign principle preserved (LAN-only + open source MIT + audit-then-replay possibile)
- Empirical validation done (D-019 single-node PASS Lenovo)
- llama-server REST API fallback ready (D-022 Option D)
- Cleanup post-trial preserved per future audit reference

**Contro**:
- Phase 7-septies multi-node BLOCKED tonight (AVG + driver + rpc-server bug)
- POC stage fragility accepted as trade-off

### Opzione B -- CONDITIONAL GO Hyperspace 5 gate (mio ADR-0025 original)

5 hard gates per Phase 2 trial isolated.

**Pro**: web-research-based + multi-source synthesis
**Contro**: empirical trial 30s ha rivelato 3 finding architetturali NON detectable da web-only. Gate 1 (Pod mode only) **architetturalmente non raggiungibile** (D-017 empirical proof).

**Verdict**: scartata post discovery aa01-001 D-017.

### Opzione C -- GO clean

Install + use default.

**Verdict**: scartata immediate -- 3 finding empirici (auto-update FORCED + Ollama auto-expose + pulse voting) violano sovereign principle architetturalmente.

## Consequences

### Positive
- Sovereign-first principle preserved
- llama.cpp RPC single-node Lenovo validato empirico
- llama-server REST API pattern viable per future LAN cross-node routing (HTTP REST piu' debuggable di Ollama-CLI dispatch)
- 22 decisions documented = audit trail completo per future reference
- Lesson L-2026-05-002 cattura 3 anti-pattern + 4 pattern positive

### Negative
- Hyperspace abandoned (capability distributed inference Pod-private NOT available come pure sovereign)
- Phase 7-septies multi-node BLOCKED (DESKTOP AV + driver update + rpc-server Windows bug)
- Pivot path llama.cpp RPC = POC stage fragility accepted

### Mitigations
- llama-server REST API fallback (D-022) per single-node Lenovo deployment immediate
- Defer Phase 7-septies multi-node a SPRINT_03+ trigger:
  - Source-build llama.cpp Windows + verify rpc-server bug fix
  - Mac mini scenario (Apple Silicon + MLX path)
  - vLLM + Ray cluster con WSL2 + GPU passthrough
  - Petals private swarm (P2P pattern simile Hyperspace ma open-source)

## Cleanup post-trial (done 2026-05-11 mattina)

- `Remove-Item -Recurse $env:USERPROFILE\.hyperspace` (Lenovo)
- Capture pktmon 262 MB logs preserved per future audit reference
- Lesson L-2026-05-002 amplified con 3 anti-pattern + 4 pattern positive

## Related

- **AA01 task** `2026-05-aa01-001-2026-05-10-fleet-discovery-pod-design` -- 22 decisions audit trail completo
- **Lesson L-2026-05-002** (in promotion da DRAFT/07 → learnings/) -- Hyperspace audit cycle 3 anti-pattern + 4 pattern positive
- **Memory** `reference_hyperspace_pods.md` -- status update "ABANDONED post-trial" + reference L-2026-05-002
- **Plan** `docs/archive/plans/integration-aa01-vault-hyperspace-2026-05.md` Obiettivo 3 (Hyperspace audit -- NO-GO outcome formalized)
- **ADR-0009** Upgrade strategy (Mac mini scenario alternative -- riformulato post-Hyperspace abandonment)
- **ADR-0023** Strategic tier post-Max (Phase 1 multi-source synthesis Tier 0)
- **Feedback** `autoresearch_default` -- methodology enforced ma INSUFFICIENT senza empirical trial per architectural decisions
- **Feedback** `governance_refresh_verify` -- pattern violato in mia sessione 2026-05-11 (refresh state INTERNO mancato)

## Notes

### Ratification

Status **Proposed**. Eduardo decide accept/reject/modify. Verdict NO-GO supportato empirico in aa01-001 D-017 99% confidence.

### Lesson methodology (L-2026-05-002)

3 anti-pattern documentati:
1. **One-shot README audit**: produce verdict confidente ma sbagliato
2. **Marketing != implementation**: Twitter announcement framing != architectural primitives
3. **Documentation ground truth assumption**: 4 cicli audit documentale missed quello che 30s empirical trial ha rivelato direttamente

4 pattern positive:
1. **Autoresearch obbligatorio per audit** (memory `feedback_autoresearch_default.md` 8-step checklist)
2. **Empirical trial breve per architectural decisions** (30s daemon trial > 4 cicli audit documentale)
3. **Archon 7-step First Principles per high-stakes** (RESTATE + CHALLENGE + RED-TEAM + CALIBRATE)
4. **Falsifying experiment economic check pre-commit** (~30s WebFetch verify top-1 assumption prima di formalizzare decision con confidence elevata)

### Reactivation triggers (per riconsiderazione futura)

- Hyperspace release con architectural redesign (opt-out auto-update + opt-out Ollama expose + opt-out pulse voting tutti enforceable via config flags persistenti)
- 3rd-party security audit indipendente che documenta isolation reale Pod mode
- Source full open-source (no private monorepo)
- Empirical re-trial 30s capture con verdict different finding

Senza questi trigger, status **ABANDONED** definitivo.

### Non-negotiable

- NO install Hyperspace finché trigger reactivation soddisfatto
- llama.cpp RPC POC stage fragility accettata come trade-off sovereign
- Pivot path Phase 7-septies deferred SPRINT_03+ trigger (Mac mini scenario o major workflow change >32 GB models)
