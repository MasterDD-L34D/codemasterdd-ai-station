"""Reproducible Ollama timing bench (METODO-SELEZIONE-LLM v4, step 7).

Per arm: cold runs (model unloaded before each) + warm runs in ABBA blocks
(A x n, B x n, B x n, A x n), each block preceded by one discarded warmup.
ABBA instead of ABAB because OLLAMA_MAX_LOADED_MODELS=1: alternating per
request would force a reload every time and no run would ever be warm.

Per request: TTFT (first streamed token, incl. thinking), end-to-end,
decode tok/s (eval_count/eval_duration), prompt tok/s, load_duration,
min RAM free, max commit, max VRAM used, CPU/GPU split from /api/ps.

Known limit (review PR582 P1-1, fix pending): resume skips a block's warmup if it
was already recorded, so a block interrupted mid-way restarts cold and its first
"warm" run includes a model load. After an interruption, use a fresh --out DIR
(or drop that block's rows from raw.jsonl); check warm load_s ~ 0 in raw.jsonl.

Usage:
  py scripts/bench-v4/bench_v4_timing.py --models A B --cold 3 --warm 5 --out DIR
  py scripts/bench-v4/bench_v4_timing.py --models A B --cold 1 --warm 1 --out DIR  (mini-sample)
"""
import argparse
import ctypes
import json
import statistics
import subprocess
import sys
import threading
import time
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path

HOST = "http://127.0.0.1:11434"
PROMPT = (
    "Write a Python implementation of a doubly-linked list class named DoublyLinkedList.\n"
    "Include these methods: insert_head(value), insert_tail(value), delete_by_value(value),\n"
    "find_by_value(value) returning the node or None, and __str__ for readable string\n"
    "representation. Add a docstring to each method explaining its purpose, parameters,\n"
    "and return value. Use type hints."
)  # same prompt as scripts/bench-ollama.ps1 -> comparable with Apr/May 2026 numbers


def make_prompt():
    """PROMPT with a per-run nonce prefix: defeats Ollama prefix (KV) cache, so warm
    TTFT/prompt tok/s measure real prefill instead of a cache hit (review PR582 P1-2)."""
    return f"[run {uuid.uuid4().hex}]\n" + PROMPT


class MemStatus(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


def ram_free_gb():
    m = MemStatus()
    m.dwLength = ctypes.sizeof(MemStatus)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2**30, (m.ullTotalPageFile - m.ullAvailPageFile) / 2**30


def vram_used_mib():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=5).stdout
        return int(out.strip().splitlines()[0])
    except Exception:
        return None


class Sampler(threading.Thread):
    """1 Hz sampler of RAM free, commit, VRAM used while a request runs."""

    def __init__(self):
        super().__init__(daemon=True)
        self.stop = threading.Event()
        self.samples = []

    def run(self):
        while not self.stop.is_set():
            free, commit = ram_free_gb()
            self.samples.append((free, commit, vram_used_mib()))
            self.stop.wait(1.0)

    def summary(self):
        if not self.samples:
            return {}
        vr = [s[2] for s in self.samples if s[2] is not None]
        return {"ram_free_min_gb": round(min(s[0] for s in self.samples), 2),
                "commit_max_gb": round(max(s[1] for s in self.samples), 2),
                "vram_max_mib": max(vr) if vr else None}


def post(path, body, timeout=900):
    req = urllib.request.Request(HOST + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=timeout)


def unload_all():
    with urllib.request.urlopen(HOST + "/api/ps", timeout=30) as r:
        for m in json.load(r).get("models", []):
            post("/api/generate", {"model": m["name"], "keep_alive": 0}).read()
    time.sleep(2)


def ps_split(model):
    with urllib.request.urlopen(HOST + "/api/ps", timeout=30) as r:
        for m in json.load(r).get("models", []):
            if m["name"].split(":")[0] == model.split(":")[0]:
                size, vram = m.get("size", 0), m.get("size_vram", 0)
                return {"size_gb": round(size / 2**30, 2), "gpu_pct": round(100 * vram / size) if size else None}
    return {}


def one_request(model, args, phase):
    body = {"model": model, "prompt": make_prompt(), "stream": True,
            "options": {"num_ctx": args.ctx, "num_predict": args.predict, "temperature": 0, "seed": 42}}
    s = Sampler()
    s.start()
    t0 = time.perf_counter()
    ttft, ttfa, final, thinking_chars, resp_chars, err = None, None, None, 0, 0, None
    resp_parts = []
    try:
        with post("/api/generate", body) as r:
            for line in r:
                ev = json.loads(line)
                if "error" in ev:
                    err = ev["error"]
                    break
                th, rs = ev.get("thinking") or "", ev.get("response") or ""
                if ttft is None and (th or rs):
                    ttft = time.perf_counter() - t0
                if ttfa is None and rs.strip():  # first answer token, after any thinking
                    ttfa = time.perf_counter() - t0
                thinking_chars += len(th)
                resp_chars += len(rs)
                resp_parts.append(rs)
                if ev.get("done"):
                    final = ev
    except Exception as e:  # recorded, not swallowed: run counts as error in summary
        err = repr(e)
    e2e = time.perf_counter() - t0
    s.stop.set()
    s.join()
    rec = {"ts": datetime.now().isoformat(timespec="seconds"), "model": model, "phase": phase,
           "ttft_s": round(ttft, 3) if ttft else None, "ttfa_s": round(ttfa, 2) if ttfa else None, "e2e_s": round(e2e, 2), "error": err,
           "thinking_chars": thinking_chars, "response_chars": resp_chars,
           "response": "".join(resp_parts), **s.summary()}
    if final:
        ed, pd = final.get("eval_duration", 0), final.get("prompt_eval_duration", 0)
        rec.update({"eval_count": final.get("eval_count"),
                    "decode_tps": round(final["eval_count"] / (ed / 1e9), 2) if ed else None,
                    "prompt_tps": round(final["prompt_eval_count"] / (pd / 1e9), 2) if pd else None,
                    "load_s": round(final.get("load_duration", 0) / 1e9, 2),
                    "done_reason": final.get("done_reason")})
        rec.update(ps_split(model))
    return rec


def med_range(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return "n/a"
    return f"{statistics.median(xs):g} [{min(xs):g}-{max(xs):g}] n={len(xs)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs=2, required=True, help="arm A and arm B")
    ap.add_argument("--cold", type=int, default=3)
    ap.add_argument("--warm", type=int, default=5, help="runs per ABBA block (2 blocks per arm)")
    ap.add_argument("--ctx", type=int, default=8192)
    ap.add_argument("--predict", type=int, default=300)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    raw = out / "raw.jsonl"
    done = set()
    if raw.exists():  # idempotent resume: skip (phase, model, idx) already recorded
        for ln in raw.read_text(encoding="utf-8").splitlines():
            r = json.loads(ln)
            done.add((r["phase"], r["model"], r["idx"]))
    a, b = args.models

    def run(model, phase, idx, unload):
        if (phase, model, idx) in done:
            return
        if unload:
            unload_all()
        rec = one_request(model, args, phase)
        rec["idx"] = idx
        with raw.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        print(f"[{rec['ts']}] {phase:5} {model:32} #{idx} ttft={rec['ttft_s']} e2e={rec['e2e_s']} "
              f"tps={rec.get('decode_tps')} load={rec.get('load_s')} gpu%={rec.get('gpu_pct')} err={rec['error']}",
              flush=True)

    # cold: alternated A,B,A,B... each preceded by full unload (symmetric)
    for i in range(args.cold):
        for m in (a, b):
            run(m, "cold", i, unload=True)
    # warm ABBA: block = 1 discarded warmup + n measured
    for blk, m in enumerate((a, b, b, a)):
        run(m, "wup", blk, unload=False)
        for i in range(args.warm):
            run(m, "warm", blk * 100 + i, unload=False)

    rows = [json.loads(x) for x in raw.read_text(encoding="utf-8").splitlines()]
    lines = [f"# Bench v4 timing -- {datetime.now():%Y-%m-%d %H:%M}", "",
             f"Prompt: DoublyLinkedList (as bench-ollama.ps1), num_ctx={args.ctx}, num_predict={args.predict}, "
             f"T=0 seed=42. Cold={args.cold}/arm, warm={2 * args.warm}/arm in ABBA blocks. Values: median [min-max] n.", ""]
    for m in (a, b):
        for ph in ("cold", "warm"):
            rs = [r for r in rows if r["model"] == m and r["phase"] == ph]
            ok = [r for r in rs if not r["error"]]
            lines += [f"## {m} -- {ph}",
                      f"- errors: {len(rs) - len(ok)}/{len(rs)}",
                      f"- decode tok/s: {med_range([r.get('decode_tps') for r in ok])}",
                      f"- TTFT s: {med_range([r.get('ttft_s') for r in ok])}",
                      f"- time to first answer token s: {med_range([r.get('ttfa_s') for r in ok])}",
                      f"- response chars: {med_range([r.get('response_chars') for r in ok])}",
                      f"- done_reason: {sorted({str(r.get('done_reason')) for r in ok})}",
                      f"- end-to-end s: {med_range([r.get('e2e_s') for r in ok])}",
                      f"- load s: {med_range([r.get('load_s') for r in ok])}",
                      f"- prompt tok/s: {med_range([r.get('prompt_tps') for r in ok])}",
                      f"- eval_count: {med_range([r.get('eval_count') for r in ok])}",
                      f"- thinking chars: {med_range([r.get('thinking_chars') for r in ok])}",
                      f"- RAM free min GB: {med_range([r.get('ram_free_min_gb') for r in ok])}",
                      f"- VRAM max MiB: {med_range([r.get('vram_max_mib') for r in ok])}",
                      f"- size GB / GPU%: {med_range([r.get('size_gb') for r in ok])} / {med_range([r.get('gpu_pct') for r in ok])}",
                      ""]
    (out / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
