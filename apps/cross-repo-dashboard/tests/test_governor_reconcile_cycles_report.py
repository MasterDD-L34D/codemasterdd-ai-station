"""TDD tests for the EXTERNAL clean-cycle report (spec sec 7.1; actor-criteria sec 4/6).

Anti-self-licking: the clean-cycle COUNT lives OUTSIDE the actor, read-only, advisory, NEVER a
gate input. A clean R1 cycle = a reconcile PR (a) MERGED BY A HUMAN, (b) not reverted within 7
days, (c) no same-line follow-up within 7 days. Pure predicate; network/gh NEVER hit.
"""


def test_clean_cycle_requires_human_merge_no_revert_no_followup():
    from governor.reconcile_cycles_report import is_clean_cycle
    base = {"merged": True, "merged_by_human": True, "reverted_within_7d": False,
            "same_line_followup_within_7d": False}
    assert is_clean_cycle(base) is True
    assert is_clean_cycle(dict(base, merged_by_human=False)) is False   # hub-merged != clean
    assert is_clean_cycle(dict(base, merged=False)) is False            # open != clean
    assert is_clean_cycle(dict(base, reverted_within_7d=True)) is False
    assert is_clean_cycle(dict(base, same_line_followup_within_7d=True)) is False


def test_summarize_counts_clean_cycles_readonly():
    from governor.reconcile_cycles_report import summarize
    prs = [
        {"id": "status-multi-repo", "merged": True, "merged_by_human": True,
         "reverted_within_7d": False, "same_line_followup_within_7d": False},
        {"id": "vault-lint-status", "merged": True, "merged_by_human": False,
         "reverted_within_7d": False, "same_line_followup_within_7d": False},
    ]
    rep = summarize(prs)
    assert rep["clean_cycles"] == 1
    assert rep["total"] == 2
    assert rep["clean_ids"] == ["status-multi-repo"]
    assert rep["advisory"] is True       # marker: NEVER a gate input


def test_actor_module_does_not_import_cycles_report():
    """Structural anti-self-licking: the actor must NOT IMPORT the accounting module (the
    actor's output can never feed its own promotion gate). The actor MAY mention the module by
    name in its docstring (documentation) -- only an import is the regression."""
    import inspect
    from governor import reconcile
    src = inspect.getsource(reconcile)
    assert "import reconcile_cycles_report" not in src
    assert "from governor.reconcile_cycles_report import" not in src
