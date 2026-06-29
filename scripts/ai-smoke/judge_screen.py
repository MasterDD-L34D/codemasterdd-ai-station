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
    """Pull the first VALID JSON array out of a free-form model response.

    A greedy `\\[.*\\]` match grabs from the first '[' to the last ']', so a reply
    with bracketed prose around the verdict (e.g. "Assessment [draft] ... [..] ...
    note [end]") yields invalid JSON and json.loads returns None even though a
    real array is present. Instead, scan each '[' as a candidate start, do a
    string-aware balanced-bracket walk to its matching ']', and return the first
    candidate that parses to a list. Robust to fenced/prefaced/trailing text.
    """
    if not text:
        return None
    for start, ch in enumerate(text):
        if ch != "[":
            continue
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(text)):
            c = text[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    candidate = text[start:i + 1]
                    try:
                        parsed = json.loads(candidate)
                    except json.JSONDecodeError:
                        break  # this '[' is not a valid array start -- try the next
                    if isinstance(parsed, list):
                        return parsed
                    break  # parsed but not a list -- try the next '['
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
            "the Ferrospora biopunk skin is used -- teal spore-glow (#3acde5) is the PRIMARY accent over a living-void ground, with painted/organic frames (chitin, carved bone, mycelium veins); a parchment-only gold-bordered fantasy panel is a FAIL (gold/bronze is the SECONDARY accent, not the primary)",
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
            "the Ferrospora biopunk skin is used -- teal spore-glow (#3acde5) is the PRIMARY accent over a living-void ground, with painted/organic frames (chitin, carved bone, mycelium veins); a parchment-only gold-bordered fantasy panel is a FAIL (gold/bronze is the SECONDARY accent, not the primary)",
            "no missing-glyph boxes (tofu squares) anywhere in the text",
        ],
    },
    "world_seed_reveal": {
        "title": "Screen 3 - World Seed Reveal (TV host view)",
        "purpose": "ERMES + companion become felt, not explained",
        "items": [
            "a primary-biome panel is a dominant element (large, left/center)",
            "world pressure is shown as a diegetic word + meter/bar (e.g. 'bassa'/'unstable'), NOT a raw decimal like 0.52",
            "a companion panel is present (the Custode named/appearing -- the reveal makes the companion felt, so a populated/named panel is correct here, NOT a defect)",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "the Ferrospora biopunk skin is used -- teal spore-glow (#3acde5) is the PRIMARY accent over a living-void ground, with painted/organic frames (chitin, carved bone, mycelium veins); a parchment-only gold-bordered fantasy panel is a FAIL (gold/bronze is the SECONDARY accent, not the primary)",
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
            "the Ferrospora biopunk skin is used -- teal spore-glow (#3acde5) is the PRIMARY accent over a living-void ground, with painted/organic frames (chitin, carved bone, mycelium veins); a parchment-only gold-bordered fantasy panel is a FAIL (gold/bronze is the SECONDARY accent, not the primary)",
            "no missing-glyph boxes (tofu) AND no raw debug keys (e.g. missing_world.biome_id) leaking to the UI",
        ],
    },
    "scenario_brief": {
        "title": "Screen 5 - Scenario Brief (TV host view)",
        "purpose": "the mission becomes concrete; commit to combat",
        "items": [
            "the scenario title + a short brief/description is the dominant central element",
            "a biome + pressure readout is shown (e.g. 'Bioma: ... -- pressione ...')",
            "a start-combat call-to-action is present (e.g. 'Inizia combattimento')",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "the Ferrospora biopunk skin is used -- teal spore-glow (#3acde5) is the PRIMARY accent over a living-void ground, with painted/organic frames (chitin, carved bone, mycelium veins); a parchment-only gold-bordered fantasy panel is a FAIL (gold/bronze is the SECONDARY accent, not the primary)",
            "no missing-glyph boxes (tofu squares) anywhere in the text",
        ],
    },
    "combat": {
        "title": "Screen 6 - Combat (TV host view)",
        "purpose": "tactical clarity",
        # Combat board + chrome fill the screen -> no clean corner void to sample;
        # the corner-sample false-FAILs, so item 4 is vision-judged (qualitative)
        # not the deterministic corner check. run() honors bg_mode.
        "bg_mode": "vision",
        "items": [
            "a tactical board with unit sprites is the central element",
            "an objective + round/season/phase readout is shown (top bar)",
            "an icon action dock is present along the bottom",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "a selected-unit info panel is present (left edge)",
            "no missing-glyph boxes (tofu), no overlapping/garbled status text, no missing-texture (magenta/checkerboard) tiles",
        ],
    },
    "debrief": {
        "title": "Screen 7 - Debrief (TV host view)",
        "purpose": "the run is remembered; outcome + chronicle",
        "items": [
            "an outcome + run readout is shown (e.g. esito, turni totali, MVP)",
            "a lineage / bond readout is present (e.g. 'Legame: ...' or a lineage summary)",
            "a chronicle/Cronaca section is present (per-encounter or full-story log)",
            "background is a dark living void (near-black, subtle), NOT flat mid-gray default",
            "the Ferrospora biopunk skin is used -- teal spore-glow (#3acde5) is the PRIMARY accent over a living-void ground, with painted/organic frames (chitin, carved bone, mycelium veins); a parchment-only gold-bordered fantasy panel is a FAIL (gold/bronze is the SECONDARY accent, not the primary)",
            "no missing-glyph boxes (tofu squares) anywhere in the text",
        ],
    },
}

# Screens whose item 5 is the panel-theme/accent line: the accent COLOR is gated
# deterministically (teal-presence) in run(), because the vision model
# hallucinates color (same lesson as the item-4 dark-bg check). Combat is absent
# (its item 5 is the selected-unit info panel, not a theme line).
for _accent_screen in ("lobby", "form_pulse", "world_seed_reveal",
                       "world_setup", "scenario_brief", "debrief"):
    SPECS[_accent_screen]["accent_item"] = 5


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


def _classify_teal_pixel(rgb):
    """True iff the pixel reads as Ferrospora spore-glow teal (~#3acde5). The
    PRIMARY accent gate -- deliberately excludes gold/bronze (#eedbae, secondary),
    the near-black void, and mycelium purple (#cd52d2, secondary) so a parchment
    gold-only screen scores ~0 teal. Cyan region: low red, high green+blue."""
    r, g, b = rgb[0], rgb[1], rgb[2]
    return (r < 120 and g > 110 and b > 130
            and (g - r) >= 40 and (b - r) >= 50 and (b - g) >= -50)


def _is_teal_accent(fraction, min_fraction=0.005):
    """Deterministic accent verdict: True iff a meaningful fraction of the screen
    is teal. Color is measurable -> not left to the vision model (which
    hallucinates color). A parchment-only screen lands ~0 -> FAIL."""
    return fraction >= min_fraction


def _merge_verdicts(vision, det):
    """Combined judge: deterministic results WIN for measurable items (vision
    hallucinates color/px); vision kept for qualitative items. `det` maps
    item -> {verdict, reason}. Each merged row is tagged with its source."""
    merged = []
    seen = set()
    for v in vision:
        item = v.get("item")
        seen.add(item)
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
    # Deterministic-only safety net: if the vision response is SHORTER than the
    # deterministic item indices (an incomplete Gemma reply that drops e.g. item 4),
    # still emit that deterministic verdict -- the measurable FAIL/PASS override must
    # never vanish just because the reply was incomplete. This covers the omit /
    # short-array case ONLY. A REORDERED reply is already safe upstream and NOT via
    # this loop: run() renumbers vision positionally (i+1) and `det` overrides by
    # slot, so a measurable item's override survives reordering regardless.
    for item in sorted(k for k in det if k not in seen):
        d = det[item]
        merged.append({
            "item": item,
            "verdict": d["verdict"],
            "reason": d["reason"],
            "source": "deterministic",
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


def sample_accent(image_path, max_dim=256, border_frac=0.2):
    """Scan only the CHROME BAND -- the outer frame of the screenshot (panel
    borders, top/side bars, frame edges) -- and return the fraction of teal-glow
    pixels there. The central content rectangle (the dominant gameplay element)
    is EXCLUDED so teal *content* (e.g. a teal 5-axis radar or chart) cannot mask
    parchment/gold *chrome*: item 5 gates the panel skin, not gameplay graphics.
    Downscaled, nearest = no color blending. ~0 on a parchment/gold screen,
    non-trivial when a teal Ferrospora frame/accent is present.

    border_frac is the band thickness as a fraction of each dimension; the
    excluded centre is [border_frac, 1-border_frac] on both axes (default 0.2 ->
    outer 20% frame sampled, central 60% x 60% content ignored)."""
    from PIL import Image

    im = Image.open(image_path).convert("RGB")
    im.thumbnail((max_dim, max_dim), Image.NEAREST)
    w, h = im.size
    raw = im.tobytes()  # flat RGB bytes -- stable, avoids deprecated getdata()
    if w == 0 or h == 0:
        return 0.0
    x0, x1 = w * border_frac, w * (1.0 - border_frac)
    y0, y1 = h * border_frac, h * (1.0 - border_frac)
    band = 0
    teal = 0
    for i in range(len(raw) // 3):
        x = i % w
        y = i // w
        if x0 <= x < x1 and y0 <= y < y1:
            continue  # central content region -- not chrome, skip
        band += 1
        if _classify_teal_pixel((raw[3 * i], raw[3 * i + 1], raw[3 * i + 2])):
            teal += 1
    if band == 0:
        return 0.0
    return teal / band


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
        accent_sampler=None, host="localhost:11434", model="gemma4:latest"):
    """End-to-end combined judge: deterministic bg (sampler -> _is_dark_bg) +
    deterministic accent (accent_sampler -> _is_teal_accent) + vision
    (vision_post -> _extract_json) merged (deterministic wins for the measurable
    color items). sampler/accent_sampler/vision_post are injectable for testing."""
    bg = sampler(image_path)
    bg_dark = _is_dark_bg(bg, det_threshold)
    # Per-screen bg mode: default = deterministic corner-sample wins for item 4
    # (vision hallucinates color). "vision" = the screen has no clean corner void
    # (e.g. combat board+chrome fill it) -> item 4 falls back to the vision verdict.
    if SPECS.get(screen, {}).get("bg_mode") == "vision":
        det = {}
    else:
        det = {4: {"verdict": "PASS" if bg_dark else "FAIL",
                   "reason": "bg pixel mean ~%s -> %s" % (bg[0], "dark" if bg_dark else "NOT dark (gray)")}}
    # Deterministic primary-accent gate: on the screens whose item 5 is the
    # panel-theme line, the teal-presence fraction WINS over the vision verdict
    # (the vision model false-PASSes parchment as "teal/biopunk"). Color = measured.
    accent_idx = SPECS.get(screen, {}).get("accent_item")
    if accent_idx and accent_sampler is not None:
        frac = accent_sampler(image_path)
        has_teal = _is_teal_accent(frac)
        det[accent_idx] = {
            "verdict": "PASS" if has_teal else "FAIL",
            "reason": "teal accent fraction ~%.4f -> %s" % (
                frac, "teal present" if has_teal else "no teal (parchment/gold only)"),
        }
    vraw = _extract_json(vision_post(image_path, screen, host, model)) or []
    vision = [{"item": i + 1, "verdict": str(v.get("verdict", "")).upper(), "reason": v.get("reason", "")}
              for i, v in enumerate(vraw)]
    return _merge_verdicts(vision, det)


def main(argv=None, run_fn=run, sampler=sample_bg, vision_post=_vision_post,
         accent_sampler=sample_accent, out=print):
    """CLI wrapper -- the un-landed glue making the judge invokable end-to-end.
    Wires the real sampler + Ollama transport into run(); exits non-zero iff any
    item FAILs (autonomous-smoke gate). All collaborators injectable for tests."""
    import argparse

    ap = argparse.ArgumentParser(description="AI-driven Godot-v2 screen smoke judge")
    ap.add_argument("--image", required=True, help="screenshot PNG to judge")
    ap.add_argument("--screen", default="lobby", help="SPECS screen key")
    ap.add_argument("--host", default="localhost:11434", help="Ollama host:port (override for cross-machine)")
    ap.add_argument("--model", default="gemma4:latest", help="vision model tag")
    ap.add_argument("--threshold", type=int, default=40, help="dark-bg brightness cutoff")
    a = ap.parse_args(argv)
    merged = run_fn(a.image, a.screen, a.threshold, sampler=sampler,
                    vision_post=vision_post, accent_sampler=accent_sampler,
                    host=a.host, model=a.model)
    out(json.dumps(merged, indent=2))
    return 1 if any(m.get("verdict") == "FAIL" for m in merged) else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
