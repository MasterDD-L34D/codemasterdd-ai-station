#!/usr/bin/env python3
"""llmfit 2-stage stage-2: task-eval N-sample on a real coding prompt.

The fleet LOCAL-LLM-STANDARD prescribes: llmfit shortlist (HW-fit) -> task-eval
N>=10 on the real prompt (anti lucky-sample, anti-pattern #14). This is the
stage-2 harness: fires the SAME coding task N times at each candidate model
(local Ollama endpoint), extracts the code, runs it against hidden asserts in an
isolated subprocess, reports pass-rate + median latency.

Task = merge_intervals (3 constraints: merge incl. touching / sort / empty) --
the 2-3 constraint band where models actually differ (ADR-0016).

Usage:
    python scripts/llmfit-task-eval.py --selftest
    python scripts/llmfit-task-eval.py [--n 10] [--host URL] model_a model_b ...
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
import time
import urllib.request

PROMPT = (
    "Write a single Python function `merge_intervals(intervals)`.\n"
    "Requirements:\n"
    "1. Merge all overlapping intervals; touching intervals (e.g. [1,2] and "
    "[2,3]) also merge into [1,3].\n"
    "2. The input list may be unsorted; the output MUST be sorted by start "
    "ascending.\n"
    "3. Empty input returns [].\n"
    "Each interval is a [start, end] list with start <= end.\n"
    "Return ONLY the function in a python code block, no explanation."
)

TESTS = [
    ([], []),
    ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
    ([[1, 4], [4, 5]], [[1, 5]]),
    ([[5, 6], [1, 3]], [[1, 3], [5, 6]]),
    ([[1, 10], [2, 3], [4, 5]], [[1, 10]]),
    ([[1, 2]], [[1, 2]]),
]

_REFERENCE = (
    "def merge_intervals(intervals):\n"
    "    if not intervals:\n"
    "        return []\n"
    "    s = sorted([list(x) for x in intervals], key=lambda x: x[0])\n"
    "    out = [s[0]]\n"
    "    for a, b in s[1:]:\n"
    "        if a <= out[-1][1]:\n"
    "            out[-1][1] = max(out[-1][1], b)\n"
    "        else:\n"
    "            out.append([a, b])\n"
    "    return out\n"
)


def extract_code(text: str) -> str:
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return m.group(1) if m else text


def run_test(code: str) -> bool:
    harness = (
        code
        + "\n\n_T = " + json.dumps(TESTS) + "\n"
        + "for _in, _exp in _T:\n"
        + "    _r = merge_intervals([list(x) for x in _in])\n"
        + "    _rn = [list(x) for x in _r]\n"
        + "    _en = [list(x) for x in _exp]\n"
        + "    assert _rn == _en, (_in, _rn, _en)\n"
        + "print('PASS')\n"
    )
    try:
        p = subprocess.run(
            [sys.executable, "-c", harness],
            capture_output=True, text=True, timeout=10,
        )
        return p.returncode == 0 and "PASS" in p.stdout
    except Exception:
        return False


def call_ollama(host: str, model: str, prompt: str):
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": 0.3, "num_ctx": 8192},
    }).encode("utf-8")
    t0 = time.time()
    req = urllib.request.Request(
        host, data=body, headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8"))
    return d.get("response", ""), (time.time() - t0) * 1000.0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("models", nargs="*")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--host", default="http://127.0.0.1:11434/api/generate")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        ok_ref = run_test(_REFERENCE)
        ok_broken = run_test("def merge_intervals(intervals):\n    return intervals\n")
        print(f"selftest reference -> {'PASS' if ok_ref else 'FAIL'} (expect PASS)")
        print(f"selftest broken    -> {'PASS' if ok_broken else 'FAIL'} (expect FAIL)")
        return 0 if (ok_ref and not ok_broken) else 1

    if not args.models:
        ap.error("provide model tags or --selftest")

    results = {}
    for model in args.models:
        passes, lats = 0, []
        for i in range(args.n):
            try:
                resp, lat = call_ollama(args.host, model, PROMPT)
                ok = run_test(extract_code(resp))
            except Exception as exc:
                ok, lat = False, 0.0
                print(f"  {model} run{i+1}: ERROR {exc}", flush=True)
            passes += int(ok)
            lats.append(lat)
            print(f"  {model} run{i+1}: {'PASS' if ok else 'FAIL'} {lat:.0f}ms", flush=True)
        med = statistics.median(lats) if lats else 0.0
        results[model] = (passes, args.n, med)
        print(f"=== {model}: {passes}/{args.n} pass | median {med:.0f}ms ===", flush=True)

    print("\n## Summary (task-eval stage-2)")
    for model, (p, n, med) in results.items():
        print(f"- {model}: {p}/{n} ({100*p/n:.0f}%) pass | {med:.0f}ms median")
    return 0


if __name__ == "__main__":
    sys.exit(main())
