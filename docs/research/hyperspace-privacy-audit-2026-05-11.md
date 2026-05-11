# Hyperspace Pods privacy audit research (2026-05-10/11 empirical)

<!--
AMEND post discovery 2026-05-11 notte+1: research originale (web-only, autoresearch 6 fonti)
era CONDITIONAL GO. Refresh-verify mancato ha duplicato lavoro empirico di aa01-001 fleet-discovery
(D-017 30s daemon trial NO-GO definitivo 99% confidence + D-018 pktmon capture).
Questo doc AMEND consolida empirical findings (primary) + web research (secondary corroborate).
Verdict NO-GO empirico definitivo.
Lesson L-2026-05-002 (in promotion da DRAFT aa01-001 /07-lesson-draft.md).
-->

> **Scope**: Hyperspace Pods privacy audit COMPLETO -- web research (autoresearch 6 fonti, 2026-05-11 sera) + empirical trial 30s daemon v5.73.8 + pktmon capture 120149 pkt (aa01-001 D-017/D-018, 2026-05-10 sera / 2026-05-11 mattina).
>
> **Status**: Research complete. Verdict ADR-0025: **NO-GO empirico definitivo**.

---

## TL;DR

Empirical trial 30s daemon Hyperspace v5.73.8 ha rivelato 3 finding architetturali (NON config-fixable) che invalidano sovereign principle:
1. **Auto-update FORCED** 680 MB on startup, no opt-out
2. **Local Ollama models auto-esposti** alla network 2M+ peer SENZA CONSENSO
3. **Pulse round voting ATTIVO** despite isolation flags `--no-agent --no-research --no-causes --no-api --profile relay`

Pktmon capture 3 min: **120149 pkt outbound, 30+ destinazioni IP TUTTE PUBBLICHE, zero LAN traffic** (DigitalOcean bootstrap pool + GitHub CDN + Cloudflare + GCP + Contabo).

**Verdict ADR-0025: NO-GO** + pivot llama.cpp RPC primary (D-018, sovereign-pure LAN-only MIT) + llama-server REST API single-node Lenovo (D-022 PASS 76 tok/s).

---

## 1. Process honesty (transparency)

Questo research doc è stato inizialmente scritto **2026-05-11 sera** in AA01 task aa01-003 hyperspace-phase-1-privacy-au con verdict **CONDITIONAL GO** basato su autoresearch web-only multi-source (6 fonti).

**AMEND post discovery** (2026-05-11 notte+1):
- Refresh-verify state interno mancato: task aa01-001 fleet-discovery aveva già completato audit empirico 30s daemon trial con verdict opposto NO-GO definitivo (D-017, 99% confidence)
- Mio audit web-only ha duplicato 4-5h di lavoro empirico precedente
- Reached verdict ERRATO (CONDITIONAL GO) perché empirical trial 30s ha rivelato 3 finding architetturali che documentazione pubblica + autoresearch web NON espongono

Memory `feedback_governance_refresh_verify` violata. Lesson L-2026-05-002 (in promotion): empirical trial breve > documentation cycles per architectural decisions.

Questo doc AMEND consolida:
- **Empirical findings primary** (aa01-001 D-017 + D-018) -- verdict NO-GO empirico
- **Web research secondary** (aa01-003 my session) -- corroborate quando overlap, irrelevant quando contraddetto empirico

---

## 2. Empirical findings (primary -- aa01-001 D-017)

### 2.1 Setup empirico

- **Date**: 2026-05-10 sera (Phase 6-sextus falsifying experiment) → 2026-05-11 mattina (D-017 formalize)
- **Environment**: Lenovo CodeMasterDD (RTX 5060 sm_120 8GB)
- **Version**: Hyperspace v5.73.8 manual zip install (no service, no systemd, user-dir extract)
- **Trial flags**: `--pod eduardo-trial-1node --no-agent --no-research --no-causes --no-api --profile relay --mode chill --headless`
- **Duration**: 3 min daemon run
- **Monitoring**: pktmon capture parallel + observation log behavior

### 2.2 Finding empirico 1 -- Auto-update FORCED at startup, NO opt-out

- Daemon scarica v5.73.8 → v5.73.9 (**680 MB**) IMMEDIATAMENTE su startup
- Anche con manual zip install user-dir + service NON registrato
- Updater logic dentro al binary, NON solo timer files Linux/macOS
- Mitigation tentata pre-install (manual zip extract, no service) NON sufficiente
- Bug osservato: `[UPDATE] Wrote v5.73.9 but launcher on disk still reports vunknown. Auto-update paused for 0h to avoid restart loop.` -- "0h" suggerisce bug stato

**Implication sovereign**: principle "audit-then-replay" violato architetturalmente. Binary cambia post-install senza consenso utente. Reproducibilità build impossibile.

### 2.3 Finding empirico 2 -- Local Ollama models auto-esposti SENZA CONSENSO (privacy severa)

Log daemon startup esplicito:
```
Loading ollama:qwen2.5-coder:7b: 0%
```

- Daemon ha scoperto Ollama locale Lenovo (gestito da codemasterdd stack)
- Sta caricando IL Qwen 7B locale per esporlo come inference resource alla network 2M+ peer
- Documentation feature ("Discovers and uses locally installed Ollama models out of the box") era opt-in implicito MA empirical è **opt-out only** (richiede uninstall Ollama o disable Hyperspace)
- Behavior NON documented in changelog / README / Twitter announcement / autoresearch web

**Implicazione PRIVACY GRAVE**: stack sovereign-only codemasterdd Lenovo (Aider + OpenCode + Ollama 8 modelli installati) sarebbe esposto alla network 2M+ peer al primo daemon start.

**Architectural mismatch sovereign**: feature behavior auto-expose è inverse opt-in semantic da framing marketing "private compute cluster".

### 2.4 Finding empirico 3 -- Pulse round voting ATTIVO despite isolation flags

Log daemon: `[NETWORK] -> Elected for pulse round`

- Pulse rounds = network consensus voting (parte sistema economic incentive USDC)
- Flags `--no-agent --no-research --no-causes --no-api --profile relay` NON disabilitano pulse participation
- Conferma: even minimal-relay node partecipa al consenso economic-incentive network-wide
- "1-node Pod" framing marketing != architectural isolation reale

---

## 3. Pktmon capture analysis (primary -- aa01-001 D-018)

### 3.1 Capture setup

- **Duration**: 3 min daemon run
- **Capture mode**: pktmon outbound only, etl2txt + PowerShell regex extraction
- **Resolution**: Resolve-DnsName reverse PTR + traffic categorization

### 3.2 Findings empirical

- **120149 pkt outbound** in 3 min daemon run
- **30+ destinazioni IP uniche, TUTTE PUBBLICHE**
- **Zero traffic LAN** 192.168.1.0/24 fleet despite `--pod eduardo-trial-1node` flag

### 3.3 Provider mappati

- **DigitalOcean** (5+ IPs Hyperspace bootstrap pool)
- **GitHub Releases CDN** (auto-update download)
- **Cloudflare** (assets hyperspace.sh)
- **Google Cloud**
- **Contabo VPS**
- **CherryServers VPS**

### 3.4 Top destinations

| IP | PTR | Pkt count |
|---|---|---|
| 138.197.168.9 | DigitalOcean | 26460 |
| 64.225.82.25 | DigitalOcean | 25065 |
| 185.199.110.133 | cdn-185-199-110-133.github.com | 14112 |

### 3.5 Critical implication

`--pod <name>` flag **NON isola routing-level**. Daemon partecipa al global P2P regardless del Pod scope.

Marketing layer "Private AI Compute Clusters" (hyperspace.sh) != architectural layer (daemon connette global P2P 2M+ nodes, Pod è overlay Raft consensus su rete globale economic-incentive).

---

## 4. Web research findings (secondary -- my session aa01-003)

### 4.1 Methodology

6 fonti parallel (autoresearch_default enforce):
1. github.com/hyperspaceai/aios-cli README
2. github.com/hyperspaceai/agi README
3. docs.hyperspace.computer (404 durante audit)
4. libp2p Noise spec
5. libp2p GossipSub v1.1 spec
6. WebSearch hyperspace.sh privacy audit 2026
+ Phase 1.2: changelog.hyper.space + hyper.space root

### 4.2 Findings web (corroborate empirici quando overlap)

**Source private monorepo** (CORROBORATE empirico):
- aios-cli README esplicit: "release-only repository... source code lives in a private monorepo"
- License MIT dichiarata MA source NOT public
- Memory `reference_hyperspace_pods.md` riga 13 claim "CLI + network + SDK open source" inaccurate

**5 GossipSub topic noti**:
- `research/rounds`, `search/experiments`, `finance/experiments`, `cause/skills`, `cause/inspiration`
- ~5min GitHub archival default mode = data persistence PUBLIC
- Topic discovery via Peer Exchange v1.1

**6 bootstrap nodes hyperspaceai-controlled**:
- US East / EU West / Asia Pacific / US West / South America / Oceania
- SPOF dependency initial

**libp2p Noise XX encryption**: e2e + forward secrecy + ephemeral keys (standard mature)

**AVM (Agent Virtual Machine) v5.40.11**: supply-chain protection + sandboxed + neurosymbolic gates

### 4.3 Findings web NON detectable empirico

- Source private monorepo (META-level, audit-then-replay impossibile)
- Bootstrap nodes locations (META-level, no SPOF mitigation visible)
- License terms (META-level)
- Spec libp2p sotto-strato (META-level)

### 4.4 Limitations web research

Empirical trial 30s ha rivelato 3 finding NON identificabili da web research:
- Finding 1 auto-update FORCED (web suggests opt-in implicit, empirical opt-out only)
- Finding 2 Ollama auto-expose (NON documented anywhere)
- Finding 3 pulse voting despite flags (NON documented)

Plus pktmon capture findings (zero LAN traffic, 30+ public destinations) NON web-derivable.

**Web research conclusione errata** (mio CONDITIONAL GO 5 gate): empirical trial necessario per architectural decisions di questa natura.

---

## 5. Cross-source synthesis

### 5.1 Empirical vs web findings

| Aspetto | Web research (my session) | Empirical (aa01-001) | Consistency |
|---------|---------------------------|----------------------|-------------|
| Encryption | Noise XX libp2p standard | Confirmed wire-level | Consistent |
| Pod private mode | AES-256-GCM + Raft capsules | Empirical: daemon connects 13+ public peer despite `--pod` | **Web overstated** |
| Telemetry | 5 GossipSub topic + ~5min GitHub | Empirical: pulse round voting forced | **Web understated** |
| Auto-update | Generic "auto-update" mentioned | Empirical: 680 MB FORCED, no opt-out architectural | **Web understated** |
| Local model exposure | Not addressed | Empirical: Ollama auto-expose visible startup log | **Web missed** |
| Source availability | Private monorepo | Confirmed (web detected this) | Consistent |
| Bootstrap nodes | 6 nodes hyperspaceai | Capture confirmed DO IPs in top destinations | Consistent |

### 5.2 Verdict consolidation

**Web research-only verdict** (mio aa01-003 CONDITIONAL GO con 5 gate): basato su trust-but-verify model con Phase 2 trial empirical proposed → ERRATO

**Empirical-driven verdict** (aa01-001 D-017 NO-GO 99% confidence): basato su 30s daemon trial + pktmon capture → CORRETTO

**Conclusione**: web research-only insufficient per architectural privacy decisions con marketing layer / docs gap. Empirical trial obbligatorio (lesson L-2026-05-002 pattern positive 2).

---

## 6. Path forward: llama.cpp RPC + REST API

### 6.1 D-018 pivot llama.cpp RPC primary

**Razionale**:
- License MIT (audit-then-replay possibile)
- Windows binary native (ggml-org/llama.cpp Releases CUDA)
- LAN-only by design (security warning explicit "Never run on open networks")
- Pure sovereign: no bootstrap, no telemetry, no auto-update, no economic system
- Heterogeneous CUDA support
- GGUF compat (Ollama models reusable)

### 6.2 D-019 Phase 6-septies single-node Lenovo PASS

- RTX 5060 sm_120 CUDA confirmed
- Qwen 7B Q4: pp16 931 tok/s + tg32 **76 tok/s**
- Performance vs Ollama: -33% (Ollama 114 tok/s) ma llama.cpp unlocks distributed
- cudart runtime separate (~383 MB) gotcha documented

### 6.3 D-020/D-021 Phase 7-septies multi-node BLOCKED tonight

- DESKTOP-B9L203E: AVG Antivirus quarantine 41 file post-extract
- Driver 536.99 max CUDA 12.2 (need >=545 per CUDA 12.4/13.1)
- LAPTOP-D73A8DIE sleep
- rpc-server CPU-only Windows: silent-exit 10s no error (b9097 build bug hypothesis)

### 6.4 D-022 Phase 7-septies Option D REST API PASS Lenovo

- llama-server v9097 Windows CUDA: starts cleanly
- REST API OpenAI-compatible `POST /v1/chat/completions`
- Latency: 0.34s end-to-end 50-token chat completion
- Pattern viable alternative a Ollama runtime per Lenovo deployment

### 6.5 Defer multi-node SPRINT_03+ trigger

- Source-build llama.cpp Windows + verify rpc-server bug fix
- Mac mini scenario (Apple Silicon + MLX path)
- vLLM + Ray cluster con WSL2 + GPU passthrough
- Petals private swarm (P2P open-source pattern simile Hyperspace)

---

## 7. Lesson L-2026-05-002 (in promotion)

### 3 anti-pattern documentati (aa01-001 DRAFT/07-lesson-draft.md)

1. **One-shot README audit** -- produce verdict confidente ma sbagliato (caso study: aios-cli README v2-era ferma mentre binary v5.73.8 70+ versioni avanti)
2. **Marketing != implementation** -- Twitter announcement + hyperspace.sh framing "Private AI Compute Clusters" != architectural layer (overlay Raft su global P2P 2M+ economic-incentive)
3. **Documentation ground truth assumption** -- 4 cicli audit documentale missed quello che 30s empirical trial ha rivelato direttamente

### 4 pattern positive

1. **Autoresearch obbligatorio per audit** (memory `feedback_autoresearch_default.md` 8-step checklist) -- NECESSARY ma INSUFFICIENT senza empirical
2. **Empirical trial breve per architectural decisions** (30s daemon > 4 cicli audit documentale)
3. **Archon 7-step First Principles per high-stakes** (RESTATE + CHALLENGE + RED-TEAM + CALIBRATE)
4. **Falsifying experiment economic check pre-commit** (~30s WebFetch verify top-1 assumption prima di formalizzare decision con confidence elevata)

### Counter-examples (NON applicare lesson)

- Tool source open + LICENSE chiaro + active maintainer + small codebase (< 5k LOC) → README empirical sufficiente
- Patch fix routine, no architectural impact → Archon over-engineered
- Decisione gia' chiara + mantenuta → non ri-validare for sake of it

---

## 8. Constraint compliance verified

- [x] NO install Hyperspace post-trial cleanup (Remove-Item `~/.hyperspace` Lenovo, 2026-05-11 mattina)
- [x] Empirical evidence preserved (262 MB pktmon capture logs `/hyperspace-trial/`)
- [x] Cleanup post-trial NON destructive (reversibile, no service registered Windows)
- [x] AA01 governance audit trail (22 decisions D-001 to D-022 in aa01-001)

---

## 9. Provenance

- AA01 task primary: `2026-05-aa01-001-2026-05-10-fleet-discovery-pod-design` (22 decisions D-001 to D-022)
- AA01 task duplicate (REJECT): `2026-05-aa01-003-2026-05-11-hyperspace-phase-1-privacy-au` (my session, web-only)
- DRAFT integrali primary: `C:/Users/edusc/aa01/workspace/2026-05-aa01-001-2026-05-10-fleet-discovery-pod-design/DRAFT/01-07-*.md`
- Lesson L-2026-05-002: in promotion da DRAFT/07-lesson-draft.md → learnings/L-2026-05-002-hyperspace-audit-cycle.md
- ADR-0025 `docs/adr/0025-hyperspace-pods-privacy-assessment.md` (formalized decision NO-GO)
- Plan integration `docs/plans/integration-aa01-vault-hyperspace-2026-05.md` Obiettivo 3 (DONE empirical via aa01-001)
- Session: 2026-05-10/11 (aa01-001 empirical) + 2026-05-11 (aa01-003 web-only duplicate + AMEND)

## 10. Related

- [ADR-0025](../adr/0025-hyperspace-pods-privacy-assessment.md) -- decision NO-GO formalized
- Memory `reference_hyperspace_pods.md` -- status update "ABANDONED post-trial"
- Lesson L-2026-05-002 (in promotion) -- Hyperspace audit cycle methodology
- Feedback `autoresearch_default` -- methodology enforced ma INSUFFICIENT senza empirical
- Feedback `governance_refresh_verify` -- pattern violato in mia sessione 2026-05-11 (refresh state INTERNO mancato)
- ADR-0023 Strategic tier post-Max (Phase 1 multi-source synthesis Tier 0)
- ADR-0009 Upgrade strategy (Mac mini scenario alternative riformulato post-Hyperspace)
