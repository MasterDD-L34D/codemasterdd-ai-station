#!/bin/bash
# sdmg-gate: SDMG Protocol 7 manual invocation gate
# Reference: L-2026-05-033 (self-designed-method-external-falsification-before-integration)
# Anti-pattern catalogue #8 (META-RULE 2026-05-17 OD-046)
# Cognitive protocol family: ADR-0026 Protocol 7
#
# Usage:
#   sdmg-gate.sh <decision-id> <class>
#     class = install | method | architectural | tool-adopt | abandon | other
#
# Prints SDMG Protocol 7 checklist, prompts interactively, logs JSONL.
# Manual invocation only. NO auto-detection (heuristic-as-decider forbidden per
# Protocol 7 step 6 + harsh-reviewer P1.2 2026-05-20 HSGF rejection finding).
#
# 2-week empirical test period from first invocation. Quarterly review.

set -e

if [ "$#" -lt 2 ]; then
    cat <<'USAGE'
Usage: sdmg-gate.sh <decision-id> <class>
  decision-id: slug identifier (e.g., "plugin-install-autoresearch")
  class:       install | method | architectural | tool-adopt | abandon | other

Reference: docs/patterns/self-designed-method-governance.md
Lesson:    L-2026-05-033 (vault learnings + global CLAUDE.md Anti-Pattern #8)
USAGE
    exit 1
fi

DECISION_ID="$1"
CLASS="$2"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LOG_DIR="$REPO_ROOT/logs"
LOG_FILE="$LOG_DIR/sdmg-invocations-$(date +%Y-%m).jsonl"
mkdir -p "$LOG_DIR"

cat <<'CHECKLIST'

=== SDMG Protocol 7 invocation gate ===
Reference: L-2026-05-033 + ADR-0026 Protocol 7 + Anti-Pattern Catalogue #8

(1) Design = hypothesis (NOT decision yet)
(2) Test empirical read-only (necessary NOT sufficient)
(3) External falsification BEFORE integration:
    - harsh-reviewer subagent OR Archon CALIBRATE (P3) OR ground-truth API
    - Pre-commit: "if rejects, adopt non-defend"
(4) Anti-accretion check:
    - Nth amendment on base with unresolved defect = STOP, fix base first
(5) Narrow adoption:
    - Read-only flag, action stays human/specialist
(6) Tuning-before-execute:
    - Decider = specialist/ground-truth, NEVER heuristic
(7) Post-exec validation:
    - Outcome measured vs hypothesis

Answer each prompt empirically. If any answer NOT empirical-y -> reconsider.

CHECKLIST

read -p "Falsifying experiment defined? (y/n): " EXP_DEFINED
read -p "Falsifying experiment EXECUTED pre-commit? (y/n): " EXP_EXECUTED
read -p "External arbiter invoked? (harsh-reviewer | archon | ground-truth | none): " ARBITER
read -p "Arbiter verdict (CONFIRM | REJECT | CONDITIONAL | n/a): " ARB_VERDICT
read -p "Narrow-adoption applied? (read-only | flag | scoped | NO): " NARROW
read -p "Anti-accretion check passed? (y/n): " ANTI_ACC
read -p "Decision verdict (ADOPT | DEFER | PIVOT | REJECT | RESERVE): " VERDICT
read -p "Confidence 0.0-1.0: " CONFIDENCE
read -p "Notes (one line): " NOTES

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TRACE=$(python -c "import uuid; print(uuid.uuid4())" 2>/dev/null || echo "no-trace")
PC="${COMPUTERNAME:-unknown}"
USER_ID="${USERNAME:-${USER:-unknown}}"

# Build JSON entry via python with env-var passthrough (JSON-safe escape automatic)
ENTRY=$(TS="$TS" TRACE="$TRACE" PC="$PC" USER_ID="$USER_ID" DECISION_ID="$DECISION_ID" \
    CLASS="$CLASS" EXP_DEFINED="$EXP_DEFINED" EXP_EXECUTED="$EXP_EXECUTED" \
    ARBITER="$ARBITER" ARB_VERDICT="$ARB_VERDICT" NARROW="$NARROW" \
    ANTI_ACC="$ANTI_ACC" VERDICT="$VERDICT" CONFIDENCE="$CONFIDENCE" NOTES="$NOTES" \
    python -c '
import json, os
fields = ("TS","TRACE","PC","USER_ID","DECISION_ID","CLASS","EXP_DEFINED",
         "EXP_EXECUTED","ARBITER","ARB_VERDICT","NARROW","ANTI_ACC",
         "VERDICT","CONFIDENCE","NOTES")
e = {k: os.environ.get(k,"") for k in fields}
out = {
    "ts": e["TS"], "trace_id": e["TRACE"], "pc": e["PC"], "user": e["USER_ID"],
    "decision_id": e["DECISION_ID"], "class": e["CLASS"],
    "experiment_defined": e["EXP_DEFINED"], "experiment_executed": e["EXP_EXECUTED"],
    "arbiter": e["ARBITER"], "arbiter_verdict": e["ARB_VERDICT"],
    "narrow_adoption": e["NARROW"], "anti_accretion_check": e["ANTI_ACC"],
    "verdict": e["VERDICT"], "confidence": e["CONFIDENCE"], "notes": e["NOTES"],
}
print(json.dumps(out))
')

echo "$ENTRY" >> "$LOG_FILE"

cat <<DONE

=== Logged ===
File:    $LOG_FILE
Trace:   $TRACE
Decision: $DECISION_ID ($CLASS) -> $VERDICT
DONE

if [ "$VERDICT" = "ADOPT" ] && [ "$EXP_EXECUTED" != "y" ]; then
    echo "WARNING: ADOPT verdict without executed falsifying experiment."
    echo "         Per L-2026-05-033, this violates SDMG step (3)."
    echo "         Reconsider: run experiment OR downgrade verdict to DEFER/RESERVE."
    exit 2
fi

if [ "$ARBITER" = "none" ] && [ "$CLASS" = "method" ]; then
    echo "WARNING: self-designed method class without external arbiter."
    echo "         Per L-2026-05-033, methods auto-violate Protocol 7 step (3)."
    echo "         Reconsider: invoke harsh-reviewer OR downgrade to DEFER."
    exit 2
fi

exit 0
