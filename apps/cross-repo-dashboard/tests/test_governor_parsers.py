import json
from pathlib import Path

_FIX = Path(__file__).resolve().parent / "fixtures"

def test_parse_game_governance_drift():
    from governor.parsers import parse_game_governance_drift
    raw = json.loads((_FIX / "governance_drift_report.json").read_text(encoding="utf-8"))
    sig = parse_game_governance_drift(raw)
    assert sig.source == "game-governance-drift"
    assert sig.kind == "drift"
    assert sig.severity == "warning"          # 0 errors, 297 warnings
    assert sig.counts == {"total": 297, "errors": 0, "warnings": 297}
    assert sig.produced_at == "2026-05-25T07:19:51+00:00"
    assert "297" in sig.summary
    assert sig.payload_hash != ""

def test_parse_game_governance_drift_errors_make_error_severity():
    from governor.parsers import parse_game_governance_drift
    sig = parse_game_governance_drift(
        {"generated_at": "2026-01-01T00:00:00+00:00",
         "summary": {"total": 3, "errors": 3, "warnings": 0}, "issues": []})
    assert sig.severity == "error"

def test_parse_game_governance_drift_handles_missing_summary():
    from governor.parsers import parse_game_governance_drift
    sig = parse_game_governance_drift({})
    assert sig.severity == "ok"
    assert sig.counts == {"total": 0, "errors": 0, "warnings": 0}

def test_parse_evo_swarm_digest():
    from governor.parsers import parse_evo_swarm_digest
    md = (_FIX / "evo_swarm_digest.md").read_text(encoding="utf-8")
    ref = "https://raw.githubusercontent.com/MasterDD-L34D/evo-swarm/main/docs/exports/EXPORT-FOR-GAME-REPO-2026-05-27.md"
    sig = parse_evo_swarm_digest(md, ref)
    assert sig.source == "evo-swarm-digest"
    assert sig.kind == "digest"
    assert sig.counts.get("cycles") == 7
    assert sig.counts.get("coverage_gaps") == 3
    assert sig.produced_at == "2026-05-27"
    assert sig.severity in {"info", "ok"}
    assert sig.ref == ref
    assert sig.payload_hash != ""

def test_parse_evo_swarm_digest_missing_numbers_safe():
    from governor.parsers import parse_evo_swarm_digest
    sig = parse_evo_swarm_digest("# Evo-Swarm -> Game Repo Digest -- 2026-06-01\nno numbers here", "r")
    assert sig.counts.get("cycles") == 0
    assert sig.counts.get("coverage_gaps") == 0
    assert sig.produced_at == "2026-06-01"

def test_parse_sot_drift_issues_open():
    import json
    from pathlib import Path
    from governor.parsers import parse_sot_drift_issues
    fix = Path(__file__).resolve().parent / "fixtures" / "sot_drift_issues.json"
    issues = json.loads(fix.read_text(encoding="utf-8"))
    sig = parse_sot_drift_issues(issues, "ref-url")
    assert sig.source == "game-sot-drift"
    assert sig.kind == "sot-drift"
    assert sig.severity == "warning"
    assert sig.counts == {"open": 1}
    assert sig.produced_at == "2026-06-01T20:51:08Z"
    assert sig.ref == "ref-url"
    assert sig.payload_hash != ""

def test_parse_sot_drift_issues_empty_is_ok():
    from governor.parsers import parse_sot_drift_issues
    sig = parse_sot_drift_issues([], "ref")
    assert sig.severity == "ok"
    assert sig.counts == {"open": 0}
    assert sig.produced_at is None
