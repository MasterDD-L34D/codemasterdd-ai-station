#!/bin/bash
# aider-log — append delegation entry to logs/aider-delegation-YYYY-MM.md
# Usage:
#   aider ... 2>&1 | aider-log --task "JSDoc on demo.js" --class cosmetic --stack 7B-whole
# Parses "Tokens:" line + "Commit HASH" + outcome heuristics from stdin,
# appends row to current-month log file in current git repo root.

# Exit codes:
# 0 = success (entry logged)
# 1 = error (missing required argument, not in a git repo, or invalid input)

set -u

TASK=""
CLASS=""
STACK=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --task) TASK="$2"; shift 2 ;;
        --class) CLASS="$2"; shift 2 ;;
        --stack) STACK="$2"; shift 2 ;;
        -h|--help)
            cat <<USAGE
Usage: aider ... 2>&1 | aider-log --task "..." --class <C> --stack <S>

  --task <desc>     short one-line task description
  --class <C>       cosmetic | behavior | strategic
  --stack <S>       7B-whole | 14B-diff | claude | other

Appends entry to <repo-root>/logs/aider-delegation-YYYY-MM.md, creating
the file with header if it doesn't exist.
USAGE
            exit 0
            ;;
        *) echo "error: unknown arg '$1' (try --help)" >&2; exit 1 ;;
    esac
done

[ -z "$TASK" ]  && { echo "error: --task required" >&2;  exit 1; }
[ -z "$CLASS" ] && { echo "error: --class required" >&2; exit 1; }
[ -z "$STACK" ] && { echo "error: --stack required" >&2; exit 1; }

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "error: not in a git repo" >&2
    exit 1
}

INPUT=$(cat)

# parse Tokens line (supports "1.1k sent" and "3100 sent")
TOKENS_LINE=$(echo "$INPUT" | grep -E "Tokens:.+sent.+received" | tail -1)
if [ -n "$TOKENS_LINE" ]; then
    TOKENS_SENT=$(echo "$TOKENS_LINE" | sed -E 's/.*Tokens: ([^ ]+) sent.*/\1/')
    TOKENS_RECV=$(echo "$TOKENS_LINE" | sed -E 's/.*sent, ([^ ]+) received.*/\1/')
else
    TOKENS_SENT="-"
    TOKENS_RECV="-"
fi

# parse last commit hash Aider printed
COMMIT_HASH=$(echo "$INPUT" | grep -oE "Commit [a-f0-9]{7,}" | tail -1 | awk '{print $2}')
[ -z "$COMMIT_HASH" ] && COMMIT_HASH="-"

# outcome heuristic
if echo "$INPUT" | grep -q "silent-corruption detected"; then
    OUTCOME="hook-block"
elif echo "$INPUT" | grep -qE "Only [0-9]+ reflections allowed"; then
    OUTCOME="safe-fail"
elif echo "$INPUT" | grep -q "Applied edit to"; then
    OUTCOME="success"
elif echo "$INPUT" | grep -qE "llama runner.+terminated"; then
    OUTCOME="error"
else
    OUTCOME="unknown"
fi

# retry count (reflection retry attempts)
RETRY=$(echo "$INPUT" | awk '/Retrying in/ { c++ } END { print c+0 }')

NOW=$(date +%Y-%m-%d\ %H:%M)
YM=$(date +%Y-%m)
LOG_FILE="$REPO_ROOT/logs/aider-delegation-$YM.md"

if [ ! -f "$LOG_FILE" ]; then
    mkdir -p "$(dirname "$LOG_FILE")"
    cat > "$LOG_FILE" <<HEADER
# Aider delegation log — $YM

Generated via \`aider-log\`. See template: \`docs/patterns/aider-delegation-log-template.md\`

| Data/ora | Task | Classe | Stack | Esito | Retry | Tokens s/r | Durata | Commit/note |
|----------|------|--------|-------|-------|-------|------------|--------|-------------|
HEADER
fi

printf "| %s | %s | %s | %s | %s | %s | %s/%s | — | \`%s\` |\n" \
    "$NOW" "$TASK" "$CLASS" "$STACK" "$OUTCOME" "$RETRY" "$TOKENS_SENT" "$TOKENS_RECV" "$COMMIT_HASH" \
    >> "$LOG_FILE"

echo "logged: $OUTCOME, tokens $TOKENS_SENT/$TOKENS_RECV, commit $COMMIT_HASH"
echo "       → $LOG_FILE"
