"""Real-Jinja render test for the /governor pane template (cr_governor.html).

Closes the gap left by the route test in test_governor_ingest.py, which MOCKS
render_template -- so the actual Jinja template is never exercised and a template
typo (a misspelled variable, a broken loop) would NOT fail CI. This test renders
the REAL template via standalone jinja2 using the route's context shape, proving
the pane renders every signal row + the load-bearing acted-on count + the
advisory list.

Standalone jinja2 (not a Flask test client): the suite mocks flask (conftest
_DEPS_TO_MOCK) but jinja2 is real and unmocked. The template's only Flask
dependency is url_for(), stubbed here. The per-app suite is invoker-run (the CI
pytest job is scoped to scripts/tests + chatgpt-recovery), so the local jinja2
install is the verification surface.
"""
from __future__ import annotations

from pathlib import Path

import pytest

# The dashboard suite is hermetic: conftest treats web deps as absent (it mocks
# flask rather than installing it). jinja2 is in the same web-dep class and is NOT
# guaranteed present, so a top-level `import jinja2` would error collection of the
# whole per-app suite in a jinja2-absent env (confirmed by Codex running it ->
# ModuleNotFoundError). importorskip skips THIS module cleanly when jinja2 is
# absent and runs it fully on the invoker machine (where jinja2 is installed) --
# the real-render verification surface. Mocking jinja2 is rejected: a real-render
# test needs the real engine.
jinja2 = pytest.importorskip("jinja2")

_TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

# R0 signal sources the governor ingests (one row each in the pane).
_SOURCES = [
    "game-governance-drift",
    "game-sot-drift",
    "evo-swarm-digest",
    "vault-gap",
    "vault-coherence",
    "vault-eng-graph",
]


def _signal(source: str, severity: str = "warning") -> dict:
    """A signal dict matching store.latest_per_source() output (template keys)."""
    return {
        "source": source,
        "kind": "drift",
        "severity": severity,
        # Decoupled from `source` on purpose: if the summary embedded the source
        # token, a broken `{{ s.source }}` cell would still satisfy `source in html`
        # via the summary cell (a masked assertion -- caught during teeth-proofing).
        "summary": "drift summary",
        "produced_at": "2026-06-02",
        "fetched_at": "2026-06-02T10:00:00Z",
    }


def _render(signals: list, acted_count: int, advisory: list) -> str:
    """Render cr_governor.html with the real template + a url_for stub."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(_TEMPLATES)),
        autoescape=True,
    )
    env.globals["url_for"] = lambda *a, **k: "style.css"
    return env.get_template("cr_governor.html").render(
        signals=signals, acted_count=acted_count, advisory=advisory
    )


def test_pane_renders_every_seeded_signal_source() -> None:
    """Loop integrity + multiplicity: all seven seeded sources appear in the HTML."""
    html = _render([_signal(s) for s in _SOURCES], acted_count=0, advisory=[])
    for source in _SOURCES:
        assert source in html, f"signal source {source!r} missing from rendered pane"


def test_pane_renders_acted_on_count() -> None:
    """The load-bearing off-ramp gate metric renders as its exact number.

    Asserts the precise `<strong>N</strong>` fragment: a broken {{ acted_count }}
    would render an empty <strong></strong> and fail this (built-in teeth).
    """
    html = _render([_signal(_SOURCES[0])], acted_count=3, advisory=[])
    assert "<strong>3</strong>" in html, "acted-on count not rendered as its number"


def test_pane_renders_advisory_entries() -> None:
    """The advisory list (auto-observed, NOT a gate input) renders its entries."""
    advisory = [
        {
            "observed_at": "2026-06-02T10:00:00Z",
            "source": "vault-gap",
            "event": "gap-detected",
            "detail": "3 gaps",
        }
    ]
    html = _render([_signal(_SOURCES[0])], acted_count=0, advisory=advisory)
    assert "gap-detected" in html, "advisory event not rendered"
    assert "3 gaps" in html, "advisory detail not rendered"
