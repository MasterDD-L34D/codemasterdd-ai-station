# Hyperspace Pods privacy audit research (2026-05-11)

<!--
Multi-source synthesis ai01 task aa01-003. Memory `feedback_autoresearch_default.md` 8/8 step compliant.
6 fonti parallel: hyperspaceai/aios-cli + agi + hyperspace.computer (404) + libp2p Noise + libp2p GossipSub v1.1 + WebSearch.
+ Phase 1.2 changelog.hyper.space + hyper.space root.
Audit log integrale: C:/Users/edusc/aa01/workspace/2026-05-aa01-003-2026-05-11-hyperspace-phase-1-privacy-au/DRAFT/01-02-*.md
-->

> **Scope**: Phase 1 privacy audit deep su Hyperspace Pods (P2P AI Compute Clusters via libp2p) via multi-source synthesis (autoresearch_default enforce). Output complementare a ADR-0025 Proposed (questo doc = research volumetric, ADR = decision formalized).
>
> **Status**: Research complete 2026-05-11. Phase 2 trial trigger-deferred (Mac mini scenario / VRAM 8GB constraint / device pooling family).

---

## TL;DR

5 ambiti privacy audit synthesized via 6 fonti parallel:
- **Encryption strong** (Noise XX libp2p e2e + AES-256-GCM Pod capsules)
- **MA**: source aios-cli **private monorepo** (memory accuracy fix), bootstrap 6/6 hyperspaceai-controlled, 5 GossipSub topic broadcast network-wide default mode, telemetry opt-out NOT documented
- **Verdict ADR-0025**: CONDITIONAL GO con 5 hard gates obbligatori prima Phase 2 trial
- **NO install** fino a trigger Eduardo (Mac mini / VRAM 8GB / device pooling)

---

## 1. Methodology

### Multi-source synthesis (memory feedback_autoresearch_default enforce)

6 fonti parallel fetch + cross-ambito synthesis:

| Source | Type | Reliability | Status |
|--------|------|-------------|--------|
| github.com/hyperspaceai/aios-cli README | Primary org repo | HIGH | Accessible -- finding **source private monorepo** |
| github.com/hyperspaceai/agi README | Primary org repo | HIGH | Accessible -- finding 5 GossipSub topics + AES-256-GCM |
| docs.hyperspace.computer | Official docs | UNAVAILABLE | 404 durante audit 2026-05-11 |
| libp2p Noise spec | Standards | HIGH | Accessible -- e2e encryption confirmed |
| libp2p GossipSub v1.1 spec | Standards | HIGH | Accessible -- "doesn't address privacy" |
| WebSearch hyperspace.sh privacy audit | Aggregated | MEDIUM | NO 3rd-party audit found |
| changelog.hyper.space (Phase 1.2) | Vendor | MEDIUM | v5.40.11 + AVM + Pod features |
| hyper.space root (Phase 1.2) | Marketing | LOW | login wall, limited info |

**Source diversity score**: 8 fonti totali, 1 MAJOR finding cross-source (source private), 0 audit terzo indipendente.

### 8-step autoresearch checklist compliance

1. ✅ Multi-source > 1
2. ✅ Parallel fetch (batch synthesis)
3. ✅ Synthesis NOT one-shot README
4. ✅ Finding cross-source emerged (private monorepo finding)
5. ✅ Gap identified transparently (docs 404 + audit terzo absent)
6. ✅ Cost-benefit verdict (CONDITIONAL GO con 5 gate)
7. ✅ Attribution memory/plan preserved
8. ✅ Audit log AA01 (DRAFT 01-02 + decisions.md D-001 to D-005)

---

## 2. Ambito 1 -- P2P data flow + encryption

### Findings

**Encryption channel libp2p Noise XX**:
- Cipher: ChaChaPoly
- Hash: SHA256
- DH: Curve25519
- Protocol name: `Noise_XX_25519_ChaChaPoly_SHA256`
- Mutual authentication: static key signature + ephemeral per session
- Forward secrecy via ephemeral DH
- Max message length: 65535 bytes per frame

**Data flow modes**:
- `hyperspace infer --local` = local-only (NO network call)
- `hyperspace infer --p2p` = network inference, routing to "best peer" (logic unclear)

**Metadata leak** (libp2p Noise limitations transparent):
- Connection initiation timing visible to network observer
- Message size (2-byte length prefix) visible
- Handshake patterns reveal peer presence
- Traffic analysis remains possible post-handshake
- Peer ID exposure via libp2p identity layer

### Verdict ambito

Encryption strong + standards-based (libp2p Noise XX mature spec). `--p2p` mode routing logic + Pod isolation enforcement NON dettagliato fonti pubbliche. Metadata leak unavoidable (network observer traffic analysis possible).

---

## 3. Ambito 2 -- Pod trust model

### Findings

**Pod semantics**:
- "Pods" = private AI clusters
- Members install CLI + form mesh + pool compute
- Encrypted state via **AES-256-GCM** as portable capsules
- Self-hosting via Docker supported
- Raft consensus per Pod (`pod-raft clock drift fix` da changelog)
- Auto-rejoin mechanism (peer drops + reconnect transparent)
- Heterogeneous engine sharding: MLX (Apple Silicon) + CUDA (NVIDIA) in one ring

**Membership control**:
- Mechanism NOT detailed in fonti pubbliche
- "Small groups share machines" descritto (implicit trust)
- Chi invita / kicker / ban revoke / reputation Pod-internal -- TBD

**Trust assumptions**:
- Implicit trust intra-Pod members
- Peer scoring GossipSub v1.1 (network-wide anti-sybil) NOT Pod-internal scoring

### Verdict ambito

Capability strong in principio (AES-256-GCM + Raft + Docker self-hosting + heterogeneous sharding). Granularity controls + admin operations UNKNOWN da fonti pubbliche. Gate 4 trial 2-node necessario.

---

## 4. Ambito 3 -- GossipSub messages telemetry

### Findings critici

**5 GossipSub topics NOTI** (da hyperspaceai/agi README):
1. `research/rounds` -- research experiments results
2. `search/experiments` -- search experiments
3. `finance/experiments` -- finance experiments (financial transactions?)
4. `cause/skills` -- agent skills broadcasted
5. `cause/inspiration` -- agent inspiration broadcasted

**Propagation model GossipSub v1.1**:
- Hybrid mesh + gossip flooding
- Publishers "flood publishing" to peers exceeding score thresholds
- 0.25 of eligible nodes gossip factor + D_lazy minimum

**Privacy properties**:
- GossipSub spec **esplicit**: "specification doesn't address privacy properties"
- Topic subscriptions + message content visible within mesh topology to connected peers
- Topic discovery via Peer Exchange (PX) -- peer learns topic membership via mesh participation

**Persistence**:
- ~1s latency before CRDT consensus
- ~2 min CRDT consensus
- **~5 min GitHub archival** -- agent results PERSIST on PUBLIC GitHub repos default mode

**Anti-abuse mechanisms** (NOT privacy):
- Peer scoring: 7 weighted parameters (time-in-mesh, deliveries, invalid msg, IP colocation)
- D_out outbound connection quotas counter sybil
- Anti-spam: GRAFT/IWANT/IHAVE limits

### Verdict ambito

**Major concern default mode**: 5 topic publici + GitHub archival ~5min = data persistence PUBLIC. Pod private mode forse isola, MA confirm trial (Gate 1). Opt-out path NOT documented -- Gate 2 empirical validation.

---

## 5. Ambito 4 -- Thor backend FOSS vs source-available

### Finding critico (cross-source contradiction)

**Memory `reference_hyperspace_pods.md` riga 13** (added 2026-05-10):
> "License: Pi component MIT. CLI + network + SDK open source. Web app + Thor backend source-available (cloning + self-hosting capable)."

**aios-cli README reality** (verified 2026-05-11):
> "This is a release-only repository. Binary releases are published here for direct download and auto-update. The source code lives in a private monorepo."

**Quindi**:
- CLI source = PRIVATE monorepo (NOT open source)
- License MIT dichiarata (full terms NOT in excerpt)
- Binary releases public + auto-update
- "open source" claim memory **NON ACCURATE** -- accuracy fix in questa session

### Thor backend reality

- NextronSystems "Thor" (WebSearch) = cybersecurity scanner, **NON Hyperspace**
- Hyperspace Thor = TurboQuant data-oblivious vector quantization (KV cache + vector search)
- "No traditional Thor backend exists" (agi README): system uses 6 bootstrap nodes per initial connectivity only
- Agents run autonomously, results persist GitHub + hourly JSON snapshots (NOT persistent server)

### Bootstrap nodes

- 6 nodes hyperspaceai-controlled geographically distributed: US East / EU West / Asia Pacific / US West / South America / Oceania
- Necessari per peer discovery initial
- SPOF: se tutti down -> network bootstrap fails
- Centralized control point: hyperspaceai org

### AVM (Agent Virtual Machine, v5.40.11 April 2026)

- Core security layer
- Supply-chain protection
- Sandboxed installations
- Behavioral scanning
- "Neurosymbolic gates: rules first, ML advisory: ML can restrict, ML cannot relax, block always wins"
- Source FOSS portion? changelog NOT specifica

### Verdict ambito

**Source private monorepo** = MAJOR concern sovereign-first. Bootstrap controlled = limited decentralization. AVM security layer claim solid in principio MA source verifiable portion TBD (Gate 3).

---

## 6. Ambito 5 -- LAN model sharing isolation

### Findings

**Model sharing capabilities**:
- Native GPU inference via node-llama-cpp (CUDA/Metal)
- Models supported: Qwen, GLM-5, GGUF formats
- Commands: `hyperspace models pull`, `hyperspace models add`
- Transport protocols + checksum verify + format details NOT documented

**LAN propagation claim**:
- "One member downloads model, rest pull from LAN ~1Gbps (no re-download per peer)"
- Encrypted via Noise inter-peer transport

**Isolation guarantees**:
- Model weights distribution = standard file sharing on mesh
- Pod isolation -> AES-256-GCM encrypted capsules
- LAN sharing inter-Pod vs intra-Pod: granularity NOT clear

**Risk profile**:
- Model weights leak IN-Pod = OK (implicit member trust)
- Model weights leak OUT-Pod = depends on public publish semantics
- Prompt leak via inference logging: NOT documented (TurboQuant data-oblivious claim could mitigate, audit independent NOT found)

### Verdict ambito

In-Pod sharing OK. Cross-Pod / public mesh isolation UNKNOWN. Prompt isolation claim NOT independently verified. Gate 1 + Gate 4 trial confirm.

---

## 7. Cross-ambito synthesis

### Pattern emerged

1. **Sovereign-first principle stress test**:
   - Source private monorepo + bootstrap controlled + GitHub archival public default = trust transitive su hyperspaceai organization
   - NON pure sovereign, MA capability strong se Pod private mode isolato

2. **Pod mode private = isolation key**:
   - AES-256-GCM capsules + Raft consensus + Docker self-hosting + heterogeneous sharding
   - Capability strong, enforcement detail TBD live verification

3. **Telemetry default-on con 5 topic publici** = privacy concern primary per default `--p2p` mode

4. **Local-first claims valid** in `--local` mode, `--p2p` mode increase exposure

5. **Audit reproducibility limited fonti pubbliche**:
   - docs 404
   - source private
   - 3rd-party audit absent
   - Trust transitive necessario per parts non auditable

### Memory accuracy corrections needed

| Memory section | Issue | Fix |
|----------------|-------|-----|
| Riga 13 License | "CLI + network + SDK open source" inaccurate | Replace: "CLI: release-only binary, source private monorepo, MIT license dichiarata. SDK + network code: TBD verifiable" |
| Riga 14 Thor backend | "source-available" vague | Replace: "Thor backend = TurboQuant data-oblivious vector quantization, source-availability TBD" |
| Riga 60-67 5 questions | Open questions originali | Replace con 5 hard gates ADR-0025 |
| Add section | -- | "5 GossipSub topic noti default mode + ~5min GitHub archival risk" |
| Add section | -- | "6 bootstrap nodes hyperspaceai-controlled SPOF" |
| Add section | -- | "ADR-0025 Proposed CONDITIONAL GO link" |

---

## 8. Verdict + Phase 2 trigger

### Verdict formalized in ADR-0025: CONDITIONAL GO

5 hard gates obbligatori prima Phase 2 trial:
1. Pod mode only (NO default `--p2p` public mesh)
2. Telemetry empirical opt-out (trial 24h observation)
3. Source verifiable portion (Thor Docker + AVM FOSS check)
4. Trust model Pod live verification (trial 2-node)
5. Bootstrap SPOF acceptable (cached peer list recovery)

### Phase 2 trigger criteria

Trigger Eduardo:
- Mac mini scenario decisione (ADR-0009 / 0024 derivati)
- VRAM 8GB constraint sentito (modelli 30B+ frequente)
- Device pooling family/friends emerge interesse
- Sub-agent codemasterdd hot ricorrente needs distributed inference

### Reactivation criteria per pivot a NO-GO post-trial

- Pod mode forza join default mesh first (Gate 1 fail)
- Mandatory telemetry NON disabilitabile (Gate 2 fail)
- All components black-box closed source (Gate 3 fail)
- No Pod admin / kick / ban capability (Gate 4 fail)
- Bootstrap mandatory dependency con NO recovery (Gate 5 fail)
- Trial mostra prompt/weight leak network-wide (any Gate fail)

---

## 9. Provenance

- AA01 workspace task: `2026-05-aa01-003-2026-05-11-hyperspace-phase-1-privacy-au`
- DRAFT integrali: `C:/Users/edusc/aa01/workspace/2026-05-aa01-003-*/DRAFT/01-02-*.md`
- Decision audit log: `C:/Users/edusc/aa01/workspace/2026-05-aa01-003-*/decisions.md` (D-001 to D-005)
- Plan integration: `docs/plans/integration-aa01-vault-hyperspace-2026-05.md` Obiettivo 3 (completion)
- Session: 2026-05-11, 8gg residui pre-Claude Max 19/05
- Tier strategic: Claude Max attivo (multi-source synthesis 5 ambiti = Tier 0 ADR-0023 applicable, fatto entro window)

## 10. Related

- [ADR-0025](../adr/0025-hyperspace-pods-privacy-assessment.md) Proposed -- decision formalized + 5 gate
- Memory `reference_hyperspace_pods.md` -- accuracy fix immediato in questa session
- Plan `docs/plans/integration-aa01-vault-hyperspace-2026-05.md` Obiettivo 3 (DONE)
- AA01 task aa01-003 (audit log integrale)
- Feedback `autoresearch_default` -- methodology enforced
- ADR-0009 / 0024 -- Mac mini scenario contesto Phase 2 trigger
