#!/usr/bin/env bash
# playtest2-board-sync.sh — OD-044 cross-repo board auto-sync.
#
# Mirrors the OD-042-A proven pattern: consumer raw-fetches the producer's
# git-committed file (NO cross-repo auth needed for a public repo). Game's
# `ai-sim-nightly.yml` Envelope-B commits `tools/sim/pillar-baseline.json`
# (verdict / samples / updated_at) to Game/main via its own baseline-update
# PR. codemasterdd cannot read Game's workflow ARTIFACT (auth-gated), but
# CAN read that committed JSON + the public Actions run conclusion.
#
# This script refreshes ONLY the auto-syncable signal block inside the
# `| **playtest#2 automation (OD-044)** |` row of
# docs/cross-repo/EXECUTION-BOARD.md, between the AUTO-SYNC markers. The
# human-authored prose of the row is never touched.
#
# Contract:
#   exit 0 + writes file  -> row changed, caller should open a PR
#   exit 0 + no file diff  -> already current OR data unreachable (no-op,
#                             NEVER spam a PR, NEVER crash the schedule)
# Defensive by design: any network / parse failure degrades to a no-op.
set -uo pipefail

GAME_OWNER="MasterDD-L34D"
GAME_REPO="Game"
GAME_REF="main"
BASELINE_PATH="tools/sim/pillar-baseline.json"
WORKFLOW_FILE="ai-sim-nightly.yml"
BOARD="docs/cross-repo/EXECUTION-BOARD.md"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT" || { echo "[sync] cannot cd repo root"; exit 0; }

BEGIN="<!-- AUTO-SYNC:playtest2 BEGIN -->"
END="<!-- AUTO-SYNC:playtest2 END -->"

log() { echo "[sync] $*"; }

# --- 1. Fetch Game's committed pillar baseline (raw, no auth) -------------
RAW_URL="https://raw.githubusercontent.com/${GAME_OWNER}/${GAME_REPO}/${GAME_REF}/${BASELINE_PATH}"
baseline_json="$(curl -fsSL --max-time 25 "$RAW_URL" 2>/dev/null || true)"

verdict="unknown"; samples="?"; updated_at="?"
if [ -n "$baseline_json" ] && echo "$baseline_json" | python3 -c 'import sys,json; json.load(sys.stdin)' 2>/dev/null; then
  verdict="$(echo "$baseline_json"   | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("verdict") if d.get("verdict") not in (None,"") else "bootstrap")' 2>/dev/null || echo unknown)"
  samples="$(echo "$baseline_json"   | python3 -c 'import sys,json; print(json.load(sys.stdin).get("samples","?"))' 2>/dev/null || echo '?')"
  updated_at="$(echo "$baseline_json" | python3 -c 'import sys,json; v=json.load(sys.stdin).get("updated_at"); print(v if v else "n/a")' 2>/dev/null || echo '?')"
  log "baseline fetched: verdict=$verdict samples=$samples updated_at=$updated_at"
else
  log "baseline unreachable/invalid (repo private, 404, or network) — degrading to no-op"
  exit 0
fi

# --- 2. Latest ai-sim-nightly run conclusion (public REST, no PAT) --------
API="https://api.github.com/repos/${GAME_OWNER}/${GAME_REPO}/actions/workflows/${WORKFLOW_FILE}/runs?per_page=1"
runs_json="$(curl -fsSL --max-time 25 -H 'Accept: application/vnd.github+json' "$API" 2>/dev/null || true)"
run_status="unknown"; run_date="?"; run_url=""
if [ -n "$runs_json" ]; then
  run_status="$(echo "$runs_json" | python3 -c 'import sys,json
try:
  r=json.load(sys.stdin)["workflow_runs"][0]
  print(r.get("conclusion") or r.get("status") or "unknown")
except Exception: print("unknown")' 2>/dev/null || echo unknown)"
  run_date="$(echo "$runs_json" | python3 -c 'import sys,json
try: print(json.load(sys.stdin)["workflow_runs"][0].get("run_started_at","?")[:10])
except Exception: print("?")' 2>/dev/null || echo '?')"
  run_url="$(echo "$runs_json" | python3 -c 'import sys,json
try: print(json.load(sys.stdin)["workflow_runs"][0].get("html_url",""))
except Exception: print("")' 2>/dev/null || echo '')"
fi
log "nightly run: status=$run_status date=$run_date"

TODAY="$(date -u +%Y-%m-%d)"
run_link="${run_url:-https://github.com/${GAME_OWNER}/${GAME_REPO}/actions/workflows/${WORKFLOW_FILE}}"

# --- 3. Build the auto-sync snapshot block -------------------------------
read -r -d '' BLOCK <<EOF || true
$BEGIN
**Auto-sync (OD-044, last refresh ${TODAY} UTC)** — source: Game \`${BASELINE_PATH}\` @ \`${GAME_REF}\` (raw-fetch, OD-042-A pattern). Pillar verdict: **${verdict}** · baseline samples: **${samples}** · baseline updated_at: \`${updated_at}\`. Latest \`ai-sim-nightly\` run: **${run_status}** (${run_date}) → [run log](${run_link}). _Auto-refreshed signal only; human prose below is authoritative for context._
$END
EOF

if [ ! -f "$BOARD" ]; then log "board missing: $BOARD"; exit 0; fi

# --- 4. Patch: inject or replace block immediately after the row ----------
python3 - "$BOARD" "$BEGIN" "$END" <<'PYEOF' > /tmp/.p2sync_block.txt
import sys
# block content arrives on stdin via env; we just stage markers here.
PYEOF

python3 - "$BOARD" <<PYEOF
import io, re, sys
board_path = "$BOARD"
begin = """$BEGIN"""
end   = """$END"""
block = """$BLOCK"""

with io.open(board_path, "r", encoding="utf-8") as f:
    text = f.read()

orig = text
row_marker = "| **playtest#2 automation (OD-044)** |"

if begin in text and end in text:
    # idempotent replace of existing block
    text = re.sub(re.escape(begin) + r".*?" + re.escape(end),
                  block.strip(), text, count=1, flags=re.DOTALL)
elif row_marker in text:
    # first-time injection: place block on its own line right after the
    # table row that contains the OD-044 marker.
    lines = text.split("\n")
    out = []
    injected = False
    for i, ln in enumerate(lines):
        out.append(ln)
        if not injected and row_marker in ln:
            out.append("")
            out.append(block.strip())
            injected = True
    text = "\n".join(out)
else:
    print("[sync] OD-044 row marker not found — no-op", file=sys.stderr)
    sys.exit(0)

if text == orig:
    print("[sync] board already current — no-op (no PR)", file=sys.stderr)
    sys.exit(0)

with io.open(board_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("[sync] board patched — change present", file=sys.stderr)
PYEOF

# --- 5. Report change state via git (idempotency / no-spam gate) ---------
if git diff --quiet -- "$BOARD" 2>/dev/null; then
  log "no net change to $BOARD — idempotent no-op, no PR"
  exit 0
fi

log "CHANGED: $BOARD updated — caller should open a PR"
exit 0
