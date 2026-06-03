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


def test_parse_evo_swarm_digest_emdash_header_date():
    # Real exports separate the date with an em-dash (U+2014), not "--". The date
    # regex must still extract it (else evo produced_at = None, no date in the pane).
    from governor.parsers import parse_evo_swarm_digest
    em = chr(0x2014)  # em-dash, kept out of source bytes (ASCII-guard clean)
    md = f"# Evo-Swarm {em} Game Repo Digest {em} 2026-05-27\n\n**Cicli inclusi**: 0 entry\n"
    sig = parse_evo_swarm_digest(md, "r")
    assert sig.produced_at == "2026-05-27"

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


def test_parse_vault_report_gap():
    from pathlib import Path
    from governor.parsers import parse_vault_report
    md = (Path(__file__).resolve().parent / "fixtures" / "vault_gap.md").read_text(encoding="utf-8")
    sig = parse_vault_report(md, source="vault-gap", kind="gap", ref="ref")
    assert sig.source == "vault-gap"
    assert sig.kind == "gap"
    assert sig.produced_at == "2026-06-01"
    # findings present (G4=1, G3=4, dup=1 -> nonzero) -> warning
    assert sig.severity == "warning"
    assert "finding" in sig.summary.lower() or any(v > 0 for v in sig.counts.values())
    assert sig.payload_hash != ""


def test_parse_vault_report_empty_is_ok():
    from governor.parsers import parse_vault_report
    sig = parse_vault_report("", source="vault-coherence", kind="coherence", ref="r")
    assert sig.severity == "ok"
    assert sig.counts["findings"] == 0


def test_parse_vault_report_counts_only_summary_section():
    # Real reports bold the corpus size ("Scanned **2249** md") OUTSIDE the Summary;
    # findings must count ONLY the Summary-section metrics, not corpus/other numbers.
    from governor.parsers import parse_vault_report
    md = (
        "# Gap-scan report 2026-06-01\n\n"
        "Scanned **2249** md.\n\n"
        "## Summary\n\n"
        "- G4 orphan: **1**\n"
        "- G3 stale: **4**\n\n"
        "## G4 orphan (1)\n- detail **9**\n"
    )
    sig = parse_vault_report(md, source="vault-gap", kind="gap", ref="r")
    assert sig.counts["findings"] == 5   # 1 + 4 (Summary only); NOT 2249 or 9
    assert sig.counts["metrics"] == 2


def test_parse_vault_report_date_anchored_to_title():
    # A stray ISO date in body text before the title must NOT win: the report
    # date comes from the heading line (else wrong produced_at -> wrong hash ->
    # spurious "new" signal churn in the advisory pane every ingest run).
    from governor.parsers import parse_vault_report
    md = (
        "context mentions 2025-01-01 in passing\n\n"
        "# Gap-scan report 2026-06-01\n\n"
        "## Summary\n\n"
        "- G4 orphan: **1**\n"
    )
    sig = parse_vault_report(md, source="vault-gap", kind="gap", ref="r")
    assert sig.produced_at == "2026-06-01"


def test_parse_vault_report_coherence_block_zero_warn_is_warning():
    # Coherence reports have NO `## Summary`; "BLOCK" appears in policy prose, but
    # the STRUCTURED verdict is e.g. `BLOCK: 0  WARN: 1  INFO: 6`. Must NOT be a
    # false "error" (BLOCK:0), but must NOT be green "ok" either when WARN>0 --
    # that would hide a surfaced vault signal (Codex P2). -> warning.
    from governor.parsers import parse_vault_report
    md = (
        "# Coherence pass -- 2026-06-01\n\n"
        "Apri PR SOLO se >=1 BLOCK. WARN o BLOCK -> review.\n\n"
        "## Disposition\n\nVerdict: BLOCK: 0  WARN: 1  INFO: 6\n"
    )
    sig = parse_vault_report(md, source="vault-coherence", kind="coherence", ref="r")
    assert sig.severity == "warning"    # BLOCK:0 but WARN:1 -> warning (not error, not ok)
    assert sig.counts["block"] == 0
    assert sig.counts["warn"] == 1
    assert sig.produced_at == "2026-06-01"


def _eng_graph_moc_fixture() -> str:
    """Inline fixture for eng-graph MOC tests.

    Uses chr(0x2014) for em-dash so source bytes stay ASCII-guard clean.
    """
    em = chr(0x2014)
    return (
        "---\n"
        "created: 2026-05-20\n"
        "last_verified: 2026-05-31\n"
        "---\n"
        "\n"
        "# Engineering MOC\n"
        "\n"
        "<!-- eng-graph:auto -->\n"
        "## Repo (bridge)\n"
        f"- [[codemasterdd-overview]] {em} repo `codemasterdd`\n"
        f"- [[evo-swarm-overview]] {em} repo `evo-swarm`\n"
        f"- [[game-overview]] {em} repo `game`\n"
        f"- [[game-database-overview]] {em} repo `game-database`\n"
        f"- [[game-godot-v2-overview]] {em} repo `game-godot-v2`\n"
        "<!-- /eng-graph:auto -->\n"
    )


def test_parse_eng_graph_moc_happy_path():
    from governor.parsers import parse_eng_graph_moc
    md = _eng_graph_moc_fixture()
    ref = "https://api.github.com/repos/MasterDD-L34D/vault/contents/Atlas/engineering-moc.md"
    sig = parse_eng_graph_moc(md, ref)
    assert sig.source == "vault-eng-graph"
    assert sig.kind == "eng-graph"
    assert sig.severity == "info"
    assert sig.produced_at == "2026-05-31"
    assert sig.counts["repos"] == 5
    assert "5" in sig.summary
    assert "2026-05-31" in sig.summary
    assert sig.ref == ref
    assert sig.payload_hash != ""


def test_parse_eng_graph_moc_falls_back_to_created_date():
    from governor.parsers import parse_eng_graph_moc
    em = chr(0x2014)
    md = (
        "---\n"
        "created: 2026-05-01\n"
        "---\n"
        "\n"
        "<!-- eng-graph:auto -->\n"
        f"- [[x]] {em} repo `alpha`\n"
        "<!-- /eng-graph:auto -->\n"
    )
    sig = parse_eng_graph_moc(md, "r")
    assert sig.produced_at == "2026-05-01"
    assert sig.counts["repos"] == 1


def test_parse_eng_graph_moc_no_region_returns_zero_repos():
    from governor.parsers import parse_eng_graph_moc
    md = "---\nlast_verified: 2026-05-31\n---\n\n# Eng MOC\n\nNo auto region here.\n"
    sig = parse_eng_graph_moc(md, "r")
    assert sig.counts["repos"] == 0
    assert sig.severity == "info"
    assert sig.produced_at == "2026-05-31"


def test_parse_eng_graph_moc_empty_input():
    from governor.parsers import parse_eng_graph_moc
    sig = parse_eng_graph_moc("", "r")
    assert sig.counts["repos"] == 0
    assert sig.produced_at is None
    assert "(undated)" in sig.summary
    assert sig.severity == "info"


def test_parse_eng_graph_moc_hash_stable():
    # Same inputs -> same hash (no time-dependent component).
    from governor.parsers import parse_eng_graph_moc
    em = chr(0x2014)
    md = (
        "---\nlast_verified: 2026-05-31\n---\n"
        "<!-- eng-graph:auto -->\n"
        f"- [[x]] {em} repo `game`\n"
        "<!-- /eng-graph:auto -->\n"
    )
    sig1 = parse_eng_graph_moc(md, "r")
    sig2 = parse_eng_graph_moc(md, "r")
    assert sig1.payload_hash == sig2.payload_hash


def _jules_digest_fixture(awaiting=2, verdicts=(
    "ACTIONABLE (linked PR CLOSED unmerged -> NOT shipped)",
    "ARCHIVE (shipped: linked PR merged)",
)):
    lines = [
        "# Jules daily digest 2026-06-03 (ADR-0034 Option D, READ-ONLY, heuristic v4.1: PR-state+files)",
        "> Signal = Jules session -> linked GitHub PR -> {merge-state, changed files}.",
        "",
        f"Awaiting sessions: {awaiting}",
        "",
    ]
    for i, v in enumerate(verdicts):
        lines.append(f"- `sess{i}` [MasterDD-L34D/Game] **{v}** -- some task  | ev")
    return "\n".join(lines) + "\n"


def test_parse_jules_digest_actionable_is_warning():
    from governor.parsers import parse_jules_digest
    sig = parse_jules_digest(_jules_digest_fixture(), "ref-url")
    assert sig.source == "jules-digest"
    assert sig.kind == "jules-digest"
    assert sig.severity == "warning"          # 1 actionable
    assert sig.counts["awaiting"] == 2
    assert sig.counts["actionable"] == 1
    assert sig.counts["archive"] == 1
    assert sig.produced_at == "2026-06-03"
    assert sig.ref == "ref-url"
    assert sig.payload_hash != ""


def test_parse_jules_digest_zero_awaiting_is_ok():
    from governor.parsers import parse_jules_digest
    md = "# Jules daily digest 2026-06-03 (...)\n\nAwaiting sessions: 0\n"
    sig = parse_jules_digest(md, "r")
    assert sig.severity == "ok"
    assert sig.counts["awaiting"] == 0
    assert sig.counts["actionable"] == 0
    assert sig.produced_at == "2026-06-03"


def test_parse_jules_digest_archive_only_is_info():
    from governor.parsers import parse_jules_digest
    md = _jules_digest_fixture(awaiting=1, verdicts=("ARCHIVE (shipped: linked PR merged)",))
    sig = parse_jules_digest(md, "r")
    assert sig.severity == "info"             # awaiting>0 but no actionable
    assert sig.counts["actionable"] == 0
    assert sig.counts["archive"] == 1


def test_parse_jules_digest_ambiguous_defer_dont_escalate():
    # The digest is conservative-AMBIGUOUS; only ACTIONABLE escalates to warning.
    from governor.parsers import parse_jules_digest
    md = _jules_digest_fixture(awaiting=2, verdicts=(
        "AMBIGUOUS (PR state unknown)", "DEFER (freeze-path; no PR)"))
    sig = parse_jules_digest(md, "r")
    assert sig.severity == "info"
    assert sig.counts["ambiguous"] == 1
    assert sig.counts["defer"] == 1


def test_parse_jules_digest_error_digest_is_error():
    from governor.parsers import parse_jules_digest
    md = ("# Jules daily digest 2026-06-03 -- ERROR\n\n"
          "> Sessions API fetch FAILED (timeout). NOT empty-set; re-run / check JULES_API_KEY.\n")
    sig = parse_jules_digest(md, "r")
    assert sig.severity == "error"
    assert sig.produced_at == "2026-06-03"


def test_parse_jules_digest_hash_folds_severity():
    # actionable (warning) vs none (ok) on the same date -> distinct hash (escalation = a new row)
    from governor.parsers import parse_jules_digest
    warn = parse_jules_digest(_jules_digest_fixture(awaiting=1, verdicts=("ACTIONABLE (x)",)), "r")
    ok = parse_jules_digest("# Jules daily digest 2026-06-03\n\nAwaiting sessions: 0\n", "r")
    assert warn.payload_hash != ok.payload_hash


def test_parse_jules_digest_empty_safe():
    from governor.parsers import parse_jules_digest
    sig = parse_jules_digest("", "r")
    assert sig.counts["awaiting"] == 0
    assert sig.produced_at is None
    assert sig.severity == "ok"


def test_parse_jules_digest_real_format_snapshot():
    # Guards the jules-daily-digest.ps1 <-> parser-regex contract (anti-pattern #10
    # cross-file drift). The fixture mirrors the SCRIPT's exact session-line format AND
    # its legend prose (bare ARCHIVE/ACTIONABLE words without `**`) -- those must NOT be
    # counted. If a future script reword breaks the format, this test goes red instead of
    # the signal silently zeroing.
    from governor.parsers import parse_jules_digest
    sig = parse_jules_digest((_FIX / "jules_digest_sample.md").read_text(encoding="utf-8"), "ref")
    assert sig.counts == {
        "awaiting": 4, "actionable": 1, "defer": 1, "ambiguous": 1, "archive": 1, "in_progress": 0,
    }
    assert sig.severity == "warning"      # 1 actionable; legend prose did NOT inflate the count
    assert sig.produced_at == "2026-05-18"
