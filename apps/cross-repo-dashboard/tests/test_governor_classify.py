"""TDD tests for governor.classify -- one test at a time (tdd-guard)."""


def test_classify_error_severity_escalates():
    from governor.classify import classify
    sig = {"source": "s1", "severity": "error", "summary": "boom"}
    result = classify(sig, prior_severity=None)
    assert result["action"] == "escalate"
    assert result["rank"] == 3
    assert "error" in result["reason"]


def test_classify_worsened_delta_escalates():
    from governor.classify import classify
    # ok -> warning = worsened
    sig = {"source": "s1", "severity": "warning", "summary": "some warnings"}
    result = classify(sig, prior_severity="ok")
    assert result["action"] == "escalate"
    assert result["rank"] == 2
    assert "worsened" in result["reason"]
    assert "ok" in result["reason"]
    assert "warning" in result["reason"]


def test_classify_steady_warning_reports():
    from governor.classify import classify
    # warning -> warning = steady -> report
    sig = {"source": "s1", "severity": "warning", "summary": "still warning"}
    result = classify(sig, prior_severity="warning")
    assert result["action"] == "report"
    assert result["rank"] == 2


def test_classify_ok_no_prior_reports():
    from governor.classify import classify
    # ok with no prior = first signal, no escalation
    sig = {"source": "s1", "severity": "ok", "summary": "all good"}
    result = classify(sig, prior_severity=None)
    assert result["action"] == "report"
    assert result["rank"] == 0


# ---------------------------------------------------------------------------
# P2.2: unknown severity rank default must be -1 (not 0) for both current and prior
# ---------------------------------------------------------------------------

def test_classify_unknown_severity_no_prior_reports():
    """P2.2: unknown severity with no prior -> report (rank -1, not 0).

    Using rank=0 for an unknown current severity silently ranks it as "ok",
    which hides the unknown signal. Default must be -1.
    """
    from governor.classify import classify
    sig = {"source": "s1", "severity": "bogus", "summary": "unknown severity"}
    result = classify(sig, prior_severity=None)
    assert result["action"] == "report"
    assert result["rank"] == -1, (
        "unknown severity rank must default to -1, not 0 (0 would silently rank as 'ok')"
    )
