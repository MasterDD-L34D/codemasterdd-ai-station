#!/usr/bin/env python3
"""AI-driven smoke -- sovereign vision-judge (no Claude in loop).

Productionized "judge" layer of the Godot-v2 First-Playable AI-driven smoke.
Incremental TDD build (tdd-guard): start with the JSON extractor the RED test
needs; integration (Ollama call, CLI) added in later cycles.
"""
import json
import re


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
