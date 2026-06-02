#!/usr/bin/env python3
"""AI-driven smoke -- sovereign vision-judge (no Claude in loop).

Productionized "judge" layer of the Godot-v2 First-Playable AI-driven smoke.
Incremental TDD build (tdd-guard): start with the JSON extractor the RED test
needs; integration (Ollama call, CLI) added in later cycles.
"""
import base64
import json
import re
import urllib.request


def _extract_json(text):
    """Pull the first JSON array out of a free-form model response."""
    m = re.search(r"\[.*\]", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


SPECS = {
    "lobby": {
        "title": "Screen 1 - Lobby (TV host view)",
        "purpose": "we are together; world not born yet",
        "items": [
            "room code is the dominant central element (large, centered)",
            "a player-slots area is present (panel listing companions in the room)",
            "a companion seed placeholder is shown, dormant/asleep/unknown",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "panels use a warm parchment/bronze theme with gold borders (not flat default UI)",
            "no missing-glyph boxes (tofu squares) anywhere in the text",
        ],
    },
    "form_pulse": {
        "title": "Screen 2 - Shared Form Pulse (TV host view)",
        "purpose": "player choices create party identity",
        "items": [
            "a 5-axis party radar (pentagon shape) is the dominant central element",
            "the 5 axes use creature-verb labels (Simbiosi/Predazione, Esplorativo/Cauto, Agile/Robusto, Solitario/Sciame, Memoria/Istinto), NOT numeric or MBTI psychology jargon",
            "a per-axis party imprint readout (bars or aggregate) is shown below the radar",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "panels use a warm parchment/bronze theme with gold borders (not flat default UI)",
            "no missing-glyph boxes (tofu squares) anywhere in the text",
        ],
    },
    "world_seed_reveal": {
        "title": "Screen 3 - World Seed Reveal (TV host view)",
        "purpose": "ERMES + companion become felt, not explained",
        "items": [
            "a primary-biome panel is a dominant element (large, left/center)",
            "world pressure is shown as a diegetic word + meter/bar (e.g. 'bassa'/'unstable'), NOT a raw decimal like 0.52",
            "a companion panel is present with a dormant/unnamed seed placeholder",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "panels use a warm parchment/bronze theme with gold borders (not flat default UI)",
            "no missing-glyph boxes (tofu squares) anywhere in the text",
        ],
    },
    "world_setup": {
        "title": "Screen 4 - World Setup Vote (TV host view)",
        "purpose": "first shared decision",
        "items": [
            "a world-condition package panel is shown (biome, pressure, hazards, scenario)",
            "a vote tally / readiness readout is present (e.g. 'Voti: N')",
            "a companion comment panel is present",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "panels use a warm parchment/bronze theme with gold borders (not flat default UI)",
            "no missing-glyph boxes (tofu) AND no raw debug keys (e.g. missing_world.biome_id) leaking to the UI",
        ],
    },
    "combat": {
        "title": "Screen 6 - Combat (TV host view)",
        "purpose": "tactical clarity",
        "items": [
            "a tactical board with unit sprites is the central element",
            "an objective + round/season/phase readout is shown (top bar)",
            "an icon action dock is present along the bottom",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "a selected-unit info panel is present (left edge)",
            "no missing-glyph boxes (tofu), no overlapping/garbled status text, no missing-texture (magenta/checkerboard) tiles",
        ],
    },
}


def _prompt(screen):
    s = SPECS[screen]
    lines = [
        "You are a strict UI QA judge for a co-op tactics game (TV+phones, Jackbox-style).",
        "Judge the attached screenshot against the spec. For EACH item return a verdict",
        "PASS, CONDITIONAL or FAIL with a one-line reason from what you SEE.",
        "Do NOT measure pixels or exact colors -- judge qualitative conformance only.",
        "SCREEN: %s" % s["title"],
        "PURPOSE: %s" % s["purpose"],
        "ITEMS:",
    ]
    for i, it in enumerate(s["items"], 1):
        lines.append("  %d. %s" % (i, it))
    lines.append("Respond ONLY with a JSON array of objects {item, verdict, reason}.")
    return "\n".join(lines)


def _is_dark_bg(rgbs, threshold=40):
    """Deterministic measurable check -- vision-LLM hallucinates color, so the
    bg-darkness verdict is computed from sampled pixel RGB, not model-judged.
    True iff mean brightness of all sampled points is below threshold (dark)."""
    if not rgbs:
        return False
    mean = sum(sum(c) / 3.0 for c in rgbs) / len(rgbs)
    return mean < threshold


def _merge_verdicts(vision, det):
    """Combined judge: deterministic results WIN for measurable items (vision
    hallucinates color/px); vision kept for qualitative items. `det` maps
    item -> {verdict, reason}. Each merged row is tagged with its source."""
    merged = []
    for v in vision:
        item = v.get("item")
        if item in det:
            d = det[item]
            merged.append({
                "item": item,
                "verdict": d["verdict"],
                "reason": d["reason"],
                "source": "deterministic",
            })
        else:
            merged.append({
                "item": item,
                "verdict": v.get("verdict"),
                "reason": v.get("reason", ""),
                "source": "vision",
            })
    return merged


def sample_bg(image_path, inset=40):
    """Sample background RGB at the 4 corners (inset from edges) -- the empty
    area around the panels. PIL-based deterministic IO for the measurable layer."""
    from PIL import Image

    im = Image.open(image_path).convert("RGB")
    w, h = im.size
    pts = [(inset, inset), (w - inset, inset), (inset, h - inset), (w - inset, h - inset)]
    return [im.getpixel(p) for p in pts]


def build_judge_payload(image_b64, screen, model="gemma4:latest"):
    """Pure Ollama /api/generate request body for the vision judge."""
    return {
        "model": model,
        "prompt": _prompt(screen),
        "images": [image_b64],
        "stream": False,
        "options": {"temperature": 0.1},
    }


def _vision_post(image_path, screen, host, model="gemma4:latest",
                 urlopen=urllib.request.urlopen):
    """Real Ollama transport for run()'s vision channel: image -> b64 ->
    POST http://<host>/api/generate -> the model 'response' text. urlopen is
    injectable so the transport contract is unit-tested without real network."""
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    payload = build_judge_payload(b64, screen, model)
    req = urllib.request.Request(
        "http://%s/api/generate" % host,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
    return data["response"]


def run(image_path, screen, det_threshold, sampler, vision_post,
        host="192.168.1.10:11434", model="gemma4:latest"):
    """End-to-end combined judge: deterministic bg (sampler -> _is_dark_bg) +
    vision (vision_post -> _extract_json) merged (deterministic wins for the
    measurable bg item). sampler + vision_post are injectable for testing."""
    bg = sampler(image_path)
    bg_dark = _is_dark_bg(bg, det_threshold)
    det = {4: {"verdict": "PASS" if bg_dark else "FAIL",
               "reason": "bg pixel mean ~%s -> %s" % (bg[0], "dark" if bg_dark else "NOT dark (gray)")}}
    vraw = _extract_json(vision_post(image_path, screen, host, model)) or []
    vision = [{"item": i + 1, "verdict": str(v.get("verdict", "")).upper(), "reason": v.get("reason", "")}
              for i, v in enumerate(vraw)]
    return _merge_verdicts(vision, det)


def main(argv=None, run_fn=run, sampler=sample_bg, vision_post=_vision_post,
         out=print):
    """CLI wrapper -- the un-landed glue making the judge invokable end-to-end.
    Wires the real sampler + Ollama transport into run(); exits non-zero iff any
    item FAILs (autonomous-smoke gate). All collaborators injectable for tests."""
    import argparse

    ap = argparse.ArgumentParser(description="AI-driven Godot-v2 screen smoke judge")
    ap.add_argument("--image", required=True, help="screenshot PNG to judge")
    ap.add_argument("--screen", default="lobby", help="SPECS screen key")
    ap.add_argument("--host", default="192.168.1.10:11434", help="Ollama host:port")
    ap.add_argument("--model", default="gemma4:latest", help="vision model tag")
    ap.add_argument("--threshold", type=int, default=40, help="dark-bg brightness cutoff")
    a = ap.parse_args(argv)
    merged = run_fn(a.image, a.screen, a.threshold, sampler=sampler,
                    vision_post=vision_post, host=a.host, model=a.model)
    out(json.dumps(merged, indent=2))
    return 1 if any(m.get("verdict") == "FAIL" for m in merged) else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
