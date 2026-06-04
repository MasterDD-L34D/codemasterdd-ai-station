---
name: feedback-n-sample-authority
description: N=10 batch insufficient per pillar upgrade — always N=40 ratify se CI95 spans band ceiling. Evidence cluster 2026-05-20.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f821c00b-6bc9-4eec-bacc-b012fef82617
---

# N-sample authority rule (calibration batch)

**Rule**: never claim pillar status upgrade (🟡→🟢, 🟢 candidato→🟢 confirmed) from N=10 batch alone if CI95 WR spans band ceiling.

**Why**: 2026-05-20 session evidence cluster — verdict flip 3 volte stessa sessione:

1. hardcore_07 N=10 WR 40% in-band → N=40 WR 60% OOB-high (+20pp delta, N=10 false signal)
2. hardcore_06 boss HP 30 N=10 WR 10% → boss HP 26 N=10 WR 0% (knob improved but result degraded, N=10 noise floor)
3. Cross-iter chain N=10 each = compounding noise not signal

N=10 CI95 = ±30pp on WR 40-60% range. Band ceiling-touch insufficient power.

**How to apply**:

- N=10 = direction probe (in-band? OOB?)
- N=40 = authoritative band placement (CI95 ±15pp)
- Pillar upgrade gate: ONLY post N=40 ratify
- N=10 chain (iter1, iter2, iter3 N=10 each) = anti-pattern; one N=40 > three N=10
- Knob exploration: 1 N=10 to confirm direction, then commit to N=40 verify

**Exception when N=10 OK**:

- Direction probe (knob has ANY effect?)
- Pre-batch instrumentation smoke (telemetry fields populated?)
- Cross-scenario sanity (both scenarios not catastrophic before committing N=40 to one)
- Bug detection (failures > 0 = stop, infrastructure broken)

**Tool**: [[calibrate-drift-verify-wrapper]] tools/py/calibrate_drift_verify.py auto-escalates N=10 → N=40 if direction promising

**Refs**:
- Museum [[calibration-n-sample-authority-2026-05-20]]
- Anti-pattern catalogue CLAUDE.md #10
- Evidence playtest docs/playtest/2026-05-20-hardcore-*.json (6 batch reports)
