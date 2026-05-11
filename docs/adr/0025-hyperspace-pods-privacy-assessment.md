# ADR-0025 -- Hyperspace Pods privacy assessment (Phase 1 audit)

> *TL;DR: Phase 1 privacy audit deep su Hyperspace Pods (P2P AI Compute Clusters via libp2p) completata 2026-05-11 con multi-source synthesis (6 fonti, AA01 task aa01-003). Findings: encryption strong (Noise XX libp2p), Pod private mode con AES-256-GCM capsules + Raft consensus, **MA**: source aios-cli **private monorepo** (memory `reference_hyperspace_pods.md` aveva claim inaccurate "open source", fixed in questa session), bootstrap nodes 6/6 hyperspaceai-controlled, 5 GossipSub topic broadcast experiment results network-wide + ~5min GitHub archival default mode, telemetry opt-out NOT documented esplicito. **Verdict: CONDITIONAL GO** con 5 hard gates obbligatori prima di Phase 2 trial. NO install fino a trigger reale (Mac mini scenario / VRAM 8GB constraint / device pooling family/friends).*

- **Status**: **Proposed** (2026-05-11)
- **Data**: 2026-05-11
- **Decisore**: Eduardo Scarpelli (final accept/reject)
- **Deciders**: solo-dev

## Context and Problem Statement

Memory `reference_hyperspace_pods.md` (added 2026-05-10) REFERENCE-only fase 1 con audit privacy P2P required PRE-install. Hyperspace Pods strategic candidate per scenario distributed inference codemasterdd (Mac mini extension alternative, device pooling family).

Hardware compat OK (RTX 5060 8GB qualifies VRAM minimum 4GB + Ryzen 4070 SUPER 12GB compatible).

Audit Phase 1 trigger: Eduardo "auto modo con archon aa01 e autoresearch come core per le decisioni" (sessione 2026-05-11). Plan integration `docs/plans/integration-aa01-vault-hyperspace-2026-05.md` Obiettivo 3 prevedeva:
- 5 ambiti privacy audit (P2P data flow / Pod trust model / GossipSub messages / Thor backend / LAN model sharing)
- Multi-source synthesis enforce (memory `feedback_autoresearch_default.md` 8-step checklist)
- Output ADR Proposed con verdict GO / NO-GO / CONDITIONAL GO + decision tree Phase 2 trigger

Audit eseguito via AA01 task `2026-05-aa01-003-2026-05-11-hyperspace-phase-1-privacy-au` con 6 fonti parallel:
1. hyperspaceai/aios-cli README (GitHub)
2. hyperspaceai/agi README (GitHub)
3. hyperspace.computer docs (URL 404, captured come finding)
4. libp2p Noise spec
5. libp2p GossipSub v1.1 spec
6. WebSearch "hyperspace.sh privacy security audit 2026"
+ Phase 1.2: changelog.hyper.space + hyper.space root

Audit log integrale: `C:/Users/edusc/aa01/workspace/2026-05-aa01-003-*/DRAFT/01-five-ambiti-synthesis.md` + `DRAFT/02-adr-scaffold-and-trigger.md`.

## Decision

**CONDITIONAL GO** -- 5 hard gates obbligatori prima di Phase 2 trial.

### Findings per 5 ambiti

#### Ambito 1 -- P2P data flow + encryption

**Findings**:
- Encryption channel libp2p Noise XX (ChaChaPoly + SHA256 + Curve25519) -- e2e strong, forward secrecy
- 2 data flow modes: `--local` (NO network) vs `--p2p` (network inference, routing to "best peer")
- Metadata leak unavoidable: connection timing + message size + handshake patterns visible to network observer

**Verdict ambito**: encryption strong, MA `--p2p` mode routing logic + Pod isolation enforcement NON dettagliato fonti pubbliche.

#### Ambito 2 -- Pod trust model

**Findings**:
- Pod = private AI clusters, members install CLI + form mesh + pool compute
- AES-256-GCM encrypted capsules portable + self-hosting via Docker
- Membership control mechanism NOT detailed in fonti pubbliche (chi invita / kicker / ban / reputation Pod-internal TBD)

**Verdict ambito**: capability OK in principio, granularity controls UNKNOWN.

#### Ambito 3 -- GossipSub messages telemetry

**Findings critici**:
- **5 GossipSub topic NOTI default mode** broadcasted network-wide: `research/rounds`, `search/experiments`, `finance/experiments`, `cause/skills`, `cause/inspiration`
- Performance metrics + model results flowing through ~1s latency + ~2min CRDT consensus + **~5min GitHub archival** (data persistence PUBLIC default)
- GossipSub spec esplicit: "specification doesn't address privacy properties" -- topic subscriptions + content visible within mesh topology
- Opt-out flags NOT clearly specified

**Verdict ambito**: major concern per default mode. Pod private mode forse isola, MA confirm trial.

#### Ambito 4 -- Thor backend FOSS vs source-available

**Finding critico**:
- aios-cli repo esplicit: "**This is a release-only repository... source code lives in a private monorepo**"
- License MIT dichiarata MA source NOT public
- **Contradice memory `reference_hyperspace_pods.md` riga 13** -- accuracy fix immediato
- NextronSystems Thor (WebSearch result) != Hyperspace Thor (omonima cybersecurity scanner)
- Hyperspace Thor = TurboQuant data-oblivious vector quantization (KV cache + vector search)
- 6 bootstrap nodes hyperspaceai-controlled geographically distributed (US East/EU West/Asia Pacific/US West/South America/Oceania) -- SPOF dependency initial
- AVM (Agent Virtual Machine, v5.40.11 April 2026) = security layer con "supply-chain protection + sandboxed installations + behavioral scanning + neurosymbolic gates rules first block always wins"

**Verdict ambito**: source private = MAJOR concern sovereign-first. Bootstrap controlled = limited decentralization. AVM security layer good in principio MA source FOSS portion TBD.

#### Ambito 5 -- LAN model sharing isolation

**Findings**:
- Native GPU inference (CUDA/Metal via node-llama-cpp)
- Models: Qwen, GLM-5, GGUF formats
- "One member downloads model, rest pull from LAN ~1Gbps" claim
- Transport protocols + checksum verify + format detail NOT documented
- Pod isolation via AES-256-GCM capsules -- in-Pod sharing OK
- Cross-Pod / public mesh sharing isolation UNKNOWN

**Verdict ambito**: in-Pod sharing capability OK, cross-Pod isolation TBD trial.

### Cross-ambito condensato

**Pattern emerged**:
1. Sovereign-first principle stress: source private + bootstrap controlled + GitHub archival public mode default = trust transitive su organization
2. Pod mode private = isolation key (AES-256-GCM capsules + Raft consensus + Docker self-hosting) -- capability strong, enforcement detail TBD
3. Telemetry default-on con 5 topic publici = primary privacy concern per default mode
4. Local-first claims valid in `--local` mode, `--p2p` mode increase exposure
5. Audit reproducibility limited: docs 404 + source private = gap insanabile fonti pubbliche

### 5 hard gates (CONDITIONAL GO criteria)

#### Gate 1 -- Pod mode only

Operazione exclusively via Pod privato creation. NON join default mesh con 5 topic GossipSub publici.

**Verificable**: Pod creation CLI flow + Wireshark/tcpdump network egress monitoring durante trial 1-node Lenovo (24h baseline).

#### Gate 2 -- Telemetry empirical opt-out

Test trial 1-node, identificare mandatory telemetry vs opt-out flags. "Cost receipts on every request" semantica -- locale vs server-side?

**Verificable**: trial 1-node + network egress monitoring 24h continuous + scan opzioni CLI/config.

#### Gate 3 -- Source verifiable portion

aios-cli source NOT pubblico. Verificare:
- Thor self-hosting Docker image pubblico esiste?
- Quale subset funzionalita' e' reproducible build via FOSS?
- AVM source FOSS?

**Verificable**: search hyperspaceai org repos public + DockerHub registry + license analysis ogni componente disponibile.

#### Gate 4 -- Trust model Pod live verification

Documenta admin/kick/ban capability durante trial 2-node:
- Chi invita
- Chi puo' kicker / ban revoke
- Chi vede encrypted capsule key

**Verificable**: trial 2-node (Lenovo + 1 device test) + admin operations test scenarios.

#### Gate 5 -- Bootstrap SPOF acceptable

6 bootstrap nodes hyperspaceai-controlled. Test cached peer list ricovery + Pod mesh sopravvive bootstrap down.

**Verificable**: trial con bootstrap nodes blocked (firewall rule) + observe se Pod private continua funzionare.

## Options considered

### Opzione A -- CONDITIONAL GO (scelta)

5 hard gates + Phase 2 trial isolated 1-node prima multi-node adoption.

**Pro**:
- Allow exploration use case Mac mini extension / device pooling
- Preserve sovereign-first via Pod private mode validation empirico
- Reactivation criteria clear per pivot a NO-GO se trial fail

**Contro**:
- Trial setup overhead (1-2 sessioni Phase 2 + 24h+ observation periodo)
- Source private restrictive per pure sovereign audit purist position

### Opzione B -- NO-GO

Adoption Hyperspace NON allowed. Continue scenario Mac mini standalone (ADR-0009 / 0024 derivati).

**Pro**: Sovereign-first principle strict respect, NO black-box dependency
**Contro**: Loss of distributed inference capability potential, Mac mini scenario solitario more expensive ($1500+ vs $0 infrastruttura compagni)

**Verdict**: scartata -- gates Phase 2 trial mitigano gran parte concerns. NO-GO premature senza empirical trial.

### Opzione C -- GO clean (install + use default)

Adoption immediate without restrictions.

**Pro**: zero overhead
**Contro**: violates sovereign-first principle (source private + telemetry default-on + bootstrap SPOF), high privacy risk default mesh participation

**Verdict**: scartata -- audit findings revelano risks NON acceptable senza gates.

## Consequences

### Positive (se Phase 2 trial PASS tutti 5 gates)
- Distributed inference capability validated per Mac mini scenario / device pooling family
- AES-256-GCM encrypted capsules + Raft consensus = Pod isolation strong validated empirico
- Multi-device heterogeneous sharding (MLX Apple Silicon + CUDA Lenovo) = future-proof
- Foundation per ADR derivati (ADR-0009 / 0024 addendum Mac mini scenario riformulato)

### Negative
- Source aios-cli private monorepo = NO ispezione codice gestione weights/queries direct (license MIT trust transitive)
- Bootstrap nodes 6/6 hyperspaceai-controlled = limited decentralization (mitigation: cached peer list)
- Audit reproducibility limited fonti pubbliche

### Mitigations
- Trial Phase 2 = empirical validation prima multi-node
- Memory `reference_hyperspace_pods.md` accuracy fix immediate (questa session)
- Reactivation criteria per pivot NO-GO se gates 1-5 fail

## Phase 2 trigger (decision tree)

```
Trigger Eduardo (Mac mini scenario / VRAM 8GB constraint / family pooling)
  |
  ├── Gate 1 verifiable -> Pod mode private creation possible?
  |     ├── NO -> NO-GO (FAIL)
  |     └── YES -> proceed Gate 2
  |
  ├── Gate 2 trial 1-node -> 24h observation OK telemetry?
  |     ├── Mandatory telemetry detected -> NO-GO (FAIL)
  |     └── Opt-out validated -> proceed Gate 3
  |
  ├── Gate 3 verify -> Thor Docker + AVM source FOSS portion?
  |     ├── NO ALL black-box -> NO-GO (FAIL)
  |     └── Partial verifiable -> proceed Gate 4
  |
  ├── Gate 4 trial 2-node -> admin/kick/ban OK?
  |     ├── Trust model insufficient -> NO-GO (FAIL)
  |     └── Verified -> proceed Gate 5
  |
  ├── Gate 5 -> bootstrap SPOF acceptable?
  |     ├── Cached peer list NON funziona -> NO-GO (FAIL)
  |     └── Mesh sopravvive bootstrap down -> Phase 3 GO
  |
  Phase 3: ADR scaffold integration + MODEL_ROUTING addendum
```

## Phase 2 trial setup (futuro, se trigger reale)

1. **Setup environment**: Lenovo CodeMasterDD primario test machine. Network monitoring Wireshark/tcpdump (capture egress 24h).
2. **Install**: `hyperspace` CLI Lenovo only (1-node, NO multi-node initially)
3. **Pod creation**: private Pod via CLI invite-link or local-only mode
4. **Observation 24h**: log all egress destinations + payload (size + frequency)
5. **Source audit**: scan hyperspaceai org repos public + DockerHub + license analysis
6. **Documenta finding**: `docs/research/hyperspace-trial-phase-2-<date>.md` separate
7. **Decision Eduardo**: continue Phase 3 multi-node o stop Phase 2

## Related

- **Memory** `reference_hyperspace_pods.md` -- accuracy fix immediato (sezione License/source + Thor backend + 5 GossipSub topics + bootstrap SPOF + 5 gate)
- **Plan** `docs/plans/integration-aa01-vault-hyperspace-2026-05.md` Obiettivo 3 (completion via questo ADR)
- **AA01 task** `2026-05-aa01-003-2026-05-11-hyperspace-phase-1-privacy-au` -- audit log completo
- **Research doc** `docs/research/hyperspace-privacy-audit-2026-05-11.md` -- volumetric synthesis 5 ambiti + cross-source
- **ADR-0009** Upgrade strategy (Mac mini scenario alternative)
- **ADR-0023** Strategic tier post-Max (Phase 1 multi-source synthesis = Tier 0 capability)
- **ADR-0024** Vue3 archive / Godot canonical timeline (parallel-run Game pivot context)
- **Feedback** `autoresearch_default` -- methodology enforced

## Notes

### Ratification

Status **Proposed** (NOT Accepted). Eduardo decide accept/reject/modify durante review PR.

### Source quality limitations (transparency)

- `hyperspace.computer` docs URL 404 (official docs unavailable durante audit 2026-05-11)
- aios-cli source private (NO direct code audit)
- 3rd-party security audit independent NOT found via WebSearch
- Findings basati su README + community + libp2p protocol spec + changelog vendor
- Source reliability score: 6 fonti indipendenti, 1 MAJOR finding cross-source (private monorepo), 0 audit terzo

### Reactivation triggers (per pivot a NO-GO post-trial)

- Pod mode forza join default mesh first (Gate 1 fail)
- Mandatory telemetry NON disabilitabile (Gate 2 fail)
- All components black-box closed source (Gate 3 fail)
- No Pod admin / kick / ban capability (Gate 4 fail)
- Bootstrap mandatory dependency con NO recovery (Gate 5 fail)
- Trial mostra prompt/weight leak network-wide (any Gate fail)

### Non-negotiable

- NO install Phase 1 (audit-only completato 2026-05-11)
- NO join public mesh prima Pod private trial validato
- Phase 2 trial separate scope (NON in codemasterdd repo, output research doc destination)
- Eduardo final accept/reject prima Phase 2 trigger

### Sourcing methodology validation

Memory `feedback_autoresearch_default.md` 8-step checklist:
1. ✅ Multi-source > 1 (6 fonti indipendenti)
2. ✅ Parallel research (batch fetch synthesis)
3. ✅ Synthesis NOT one-shot (cross-ambito + contradictions)
4. ✅ Finding cross-source emerged (source private monorepo)
5. ✅ Gap identified (docs 404 + 3rd-party audit absent)
6. ✅ Cost-benefit verdict cross-source (CONDITIONAL GO con 5 gate)
7. ✅ Attribution memory/plan/AA01 preserved
8. ✅ Audit log AA01 DRAFT 01 + 02 + decisions.md (D-001 to D-005)
