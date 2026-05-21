#!/usr/bin/env python3
"""whisper-transcribe -- sovereign local audio transcription (faster-whisper).

Stack tool added 2026-05-21. GPU (CUDA via nvidia-* wheels) with CPU fallback.
Handles the Windows nvidia-wheel DLL-dir setup automatically.

Usage:
  python whisper_transcribe.py <file.wav|dir> [--model large-v3] [--lang it] [--device auto]
Writes a .txt sidecar next to each audio file (or to --out dir).
"""
from __future__ import annotations
import argparse, glob, os, site, sysconfig, sys, time
from pathlib import Path


def _enable_cuda_dlls():
    bases = [sysconfig.get_paths()["purelib"], site.getusersitepackages(), *site.getsitepackages()]
    for base in bases:
        for d in glob.glob(os.path.join(base, "nvidia", "*", "bin")):
            try:
                os.add_dll_directory(d)
            except Exception:
                pass
            os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="audio file or directory")
    p.add_argument("--model", default="large-v3")
    p.add_argument("--lang", default=None, help="force language (e.g. it); default=auto-detect")
    p.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    p.add_argument("--glob", default="*.wav", help="pattern when path is a dir")
    p.add_argument("--out", default=None, help="output dir (default: alongside source)")
    args = p.parse_args()

    _enable_cuda_dlls()
    from faster_whisper import WhisperModel

    src = Path(args.path)
    files = sorted(src.glob("**/" + args.glob)) if src.is_dir() else [src]
    if not files:
        print("no audio files found", file=sys.stderr); return 1

    order = [("cuda", "float16"), ("cpu", "int8")] if args.device == "auto" else \
            [(args.device, "float16" if args.device == "cuda" else "int8")]
    model = None
    for dev, ct in order:
        try:
            model = WhisperModel(args.model, device=dev, compute_type=ct)
            print(f"[whisper] model={args.model} device={dev}", flush=True)
            break
        except Exception as e:
            print(f"[whisper] {dev} unavailable: {str(e)[:80]}", flush=True)
    if model is None:
        print("no usable device", file=sys.stderr); return 1

    outdir = Path(args.out) if args.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)
    for i, f in enumerate(files, 1):
        t0 = time.time()
        segs, info = model.transcribe(str(f), language=args.lang)
        txt = "".join(s.text for s in segs).strip()
        dst = (outdir / (f.stem + ".txt")) if outdir else f.with_suffix(".txt")
        dst.write_text(txt, encoding="utf-8")
        print(f"  {i}/{len(files)} [{info.language}] {time.time()-t0:.1f}s -> {dst.name}", flush=True)
    print(f"[whisper] DONE {len(files)} files", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
