#!/bin/bash
# Smoke test for sdmg-gate.sh
# Verifies: script runs, log file written, JSON valid, exit codes correct

set -e

SCRIPT="$(git rev-parse --show-toplevel)/scripts/sdmg/sdmg-gate.sh"
LOG_FILE="$(git rev-parse --show-toplevel)/logs/sdmg-invocations-$(date +%Y-%m).jsonl"

PASS=0
FAIL=0

assert_eq() {
    local label="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "  PASS: $label"
        PASS=$((PASS+1))
    else
        echo "  FAIL: $label (expected: $expected, actual: $actual)"
        FAIL=$((FAIL+1))
    fi
}

assert_nonempty() {
    local label="$1" actual="$2"
    if [ -n "$actual" ]; then
        echo "  PASS: $label (got: $actual)"
        PASS=$((PASS+1))
    else
        echo "  FAIL: $label (empty)"
        FAIL=$((FAIL+1))
    fi
}

# Setup: clean log file for fresh test
rm -f "$LOG_FILE"

# Test 1: script exists + executable
echo "Test 1: script exists + executable"
assert_eq "script file exists" "1" "$([ -f "$SCRIPT" ] && echo 1 || echo 0)"
assert_eq "script executable" "1" "$([ -x "$SCRIPT" ] && echo 1 || echo 0)"

# Test 2: usage exit code on missing args
echo "Test 2: usage on missing args"
set +e
bash "$SCRIPT" >/dev/null 2>&1
EXIT_NOARGS=$?
set -e
assert_eq "exit 1 on missing args" "1" "$EXIT_NOARGS"

# Test 3: full invocation with valid input, DEFER verdict (no warning trigger)
echo "Test 3: full invocation DEFER"
INPUT=$(printf "y\ny\nharsh-reviewer\nCONFIRM\nread-only\ny\nDEFER\n0.5\ntest-note-smoke\n")
set +e
echo "$INPUT" | bash "$SCRIPT" smoke-test-001 install >/tmp/sdmg-out 2>&1
EXIT_OK=$?
set -e
assert_eq "exit 0 on full valid DEFER" "0" "$EXIT_OK"
assert_eq "log file written" "1" "$([ -f "$LOG_FILE" ] && echo 1 || echo 0)"

# Test 4: JSON validity
echo "Test 4: JSON valid"
LAST_LINE=$(tail -n 1 "$LOG_FILE")
JSON_VALID=$(python -c "import json,sys; json.loads(sys.argv[1]); print(1)" "$LAST_LINE" 2>/dev/null || echo 0)
assert_eq "last log line valid JSON" "1" "$JSON_VALID"

# Test 5: JSON content fields present
echo "Test 5: JSON content"
DEC_ID=$(python -c "import json,sys; print(json.loads(sys.argv[1])['decision_id'])" "$LAST_LINE" 2>/dev/null)
assert_eq "decision_id matches" "smoke-test-001" "$DEC_ID"
CLASS_VAL=$(python -c "import json,sys; print(json.loads(sys.argv[1])['class'])" "$LAST_LINE" 2>/dev/null)
assert_eq "class matches" "install" "$CLASS_VAL"
VERD=$(python -c "import json,sys; print(json.loads(sys.argv[1])['verdict'])" "$LAST_LINE" 2>/dev/null)
assert_eq "verdict matches" "DEFER" "$VERD"

# Test 6: ADOPT without executed experiment -> warning + exit 2
echo "Test 6: ADOPT no experiment guard"
INPUT2=$(printf "y\nn\nnone\nn/a\nNO\ny\nADOPT\n0.9\nshould-warn\n")
set +e
echo "$INPUT2" | bash "$SCRIPT" smoke-test-002 install >/tmp/sdmg-out2 2>&1
EXIT_WARN=$?
set -e
assert_eq "exit 2 on ADOPT without experiment" "2" "$EXIT_WARN"

# Test 7: self-designed method without arbiter -> warning + exit 2
echo "Test 7: method without arbiter guard"
INPUT3=$(printf "y\ny\nnone\nn/a\nread-only\ny\nADOPT\n0.7\nmethod-no-arbiter\n")
set +e
echo "$INPUT3" | bash "$SCRIPT" smoke-test-003 method >/tmp/sdmg-out3 2>&1
EXIT_METH=$?
set -e
assert_eq "exit 2 on method class without arbiter" "2" "$EXIT_METH"

# Summary
echo ""
echo "=== Summary: $PASS PASS, $FAIL FAIL ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
