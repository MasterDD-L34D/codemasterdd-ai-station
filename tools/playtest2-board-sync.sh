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
# docs/governance/EXECUTION-BOARD.md, between the AUTO-SYNC markers. The
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
# OD-044 deep-metrics: Game's ai-sim-nightly baseline-update PR now ALSO
# commits a small board-consumable digest of the analyzer metrics.json to
# this stable public path (same auto-PR, same idempotency guard). It is
# raw-fetchable with no cross-repo auth, exactly like pillar-baseline.json.
# Honest residual closer: if Game has not produced/committed it yet
# (bootstrap, 404), this script falls back to the verdict-only block —
# the per-pillar line is simply omitted, never fabricated, never crashes.
DIGEST_PATH="tools/sim/playtest2-latest.json"
WORKFLOW_FILE="ai-sim-nightly.yml"
BOARD="docs/governance/EXECUTION-BOARD.md"

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

# --- 2b. Fetch Game's committed deep-metrics digest (raw, no auth) --------
# OD-044 residual closer. Optional + graceful: a 404 (Game has not yet
# committed the digest — bootstrap, or older Game main) or any parse
# failure leaves $pillar_line empty, so the block degrades cleanly to the
# pre-existing verdict-only behavior. NEVER fabricated, NEVER crashes.
DIGEST_RAW_URL="https://raw.githubusercontent.com/${GAME_OWNER}/${GAME_REPO}/${GAME_REF}/${DIGEST_PATH}"
digest_json="$(curl -fsSL --max-time 25 "$DIGEST_RAW_URL" 2>/dev/null || true)"
pillar_line=""
if [ -n "$digest_json" ] && echo "$digest_json" | python3 -c 'import sys,json; json.load(sys.stdin)' 2>/dev/null; then
  pillar_line="$(echo "$digest_json" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    def g(path, default="n/a"):
        cur = d
        for k in path.split("."):
            if not isinstance(cur, dict) or k not in cur or cur[k] is None:
                return default
            cur = cur[k]
        return cur
    def n(path, suffix=""):
        v = g(path)
        if isinstance(v, float):
            v = round(v, 1)
        return "n/a" if v == "n/a" else "{}{}".format(v, suffix)
    parts = [
        "P3 **{}** (promos {})".format(g("pillars.p3.verdict"), n("pillars.p3.key_metric")),
        "P4 **{}**".format(g("pillars.p4.verdict")),
        "P6 **{}** (rewind {})".format(g("pillars.p6.verdict"), n("pillars.p6.rewind_pct", "%")),
        "OD-024 firing {}".format(n("pillars.od024.firing_pct", "%")),
        "OD-026 skiv {} / biome-focus {}".format(n("pillars.od026.skiv_pulse"), n("pillars.od026.biome_focus")),
        "perf p95 {} ({})".format(n("pillars.performance.p95_ms", "ms"), g("pillars.performance.verdict")),
    ]
    ss = g("sample_size")
    rid = g("run_id")
    print("Deep per-pillar (Game `{}` @ `main`, sample {}, run {}): ".format("tools/sim/playtest2-latest.json", ss, rid) + " · ".join(parts))
except Exception:
    print("")
' 2>/dev/null || echo "")"
  if [ -n "$pillar_line" ]; then
    log "deep-metrics digest fetched: $pillar_line"
  else
    log "deep-metrics digest present but unparseable — verdict-only fallback"
  fi
else
  log "deep-metrics digest unreachable/404 (Game not yet committed it) — verdict-only fallback (honest, no-op)"
fi

TODAY="$(date -u +%Y-%m-%d)"
run_link="${run_url:-https://github.com/${GAME_OWNER}/${GAME_REPO}/actions/workflows/${WORKFLOW_FILE}}"

# Deep-metrics sentence: present only when the digest was fetched + parsed.
# Honest fallback line otherwise so the board is explicit about the gap.
if [ -n "$pillar_line" ]; then
  pillar_md=" ${pillar_line}."
else
  pillar_md=" Deep per-pillar metrics: _not yet published by Game (digest absent / bootstrap) — verdict-only above is authoritative._"
fi

# --- 3. Build the auto-sync snapshot block -------------------------------
read -r -d '' BLOCK <<EOF || true
$BEGIN
**Auto-sync (OD-044, last refresh ${TODAY} UTC)** — source: Game \`${BASELINE_PATH}\` @ \`${GAME_REF}\` (raw-fetch, OD-042-A pattern). Pillar verdict: **${verdict}** · baseline samples: **${samples}** · baseline updated_at: \`${updated_at}\`. Latest \`ai-sim-nightly\` run: **${run_status}** (${run_date}) → [run log](${run_link}).${pillar_md} _Auto-refreshed signal only; human prose below is authoritative for context._
$END
EOF

if [ ! -f "$BOARD" ]; then log "board missing: $BOARD"; exit 0; fi

# --- 4. Patch: inject or replace block immediately after the row ----------
# Pass block + markers via the ENVIRONMENT (not source interpolation) so
# UTF-8 content (·, →, accented prose) never corrupts the inline python
# source bytes. The heredoc body is fully static + quoted.
P2SYNC_BOARD="$BOARD" P2SYNC_BEGIN="$BEGIN" P2SYNC_END="$END" P2SYNC_BLOCK="$BLOCK" \
python3 - <<'PYEOF'
# -*- coding: utf-8 -*-
import io, os, re, sys
board_path = os.environ["P2SYNC_BOARD"]
begin = os.environ["P2SYNC_BEGIN"]
end   = os.environ["P2SYNC_END"]
block = os.environ["P2SYNC_BLOCK"]

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
