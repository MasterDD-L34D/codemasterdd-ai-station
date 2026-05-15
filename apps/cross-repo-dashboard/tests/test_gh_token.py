from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest

# We import app after mocks are in place (handled by conftest.py's clear_cache fixture)
# But _get_gh_token is called at module level in app.py when GH_TOKEN is initialized.
# We will test the function directly.

def test_get_gh_token_success():
    """Test happy path where gh auth token returns a token."""
    from app import _get_gh_token, _NO_WINDOW_FLAG

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = b"gho_testtoken123\n"

    with patch("subprocess.run", return_value=mock_result) as mock_run:
        token = _get_gh_token()

        assert token == "gho_testtoken123"
        mock_run.assert_called_once_with(
            ["gh", "auth", "token"],
            capture_output=True, text=False, timeout=10, check=False, shell=False,
            creationflags=_NO_WINDOW_FLAG,
        )

def test_get_gh_token_non_zero_exit():
    """Test when gh auth token returns a non-zero exit code."""
    from app import _get_gh_token

    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = b""

    with patch("subprocess.run", return_value=mock_result):
        token = _get_gh_token()
        assert token == ""

def test_get_gh_token_empty_stdout():
    """Test when gh auth token returns zero exit code but empty stdout."""
    from app import _get_gh_token

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = b""

    with patch("subprocess.run", return_value=mock_result):
        token = _get_gh_token()
        assert token == ""

def test_get_gh_token_exception():
    """Test when subprocess.run raises an exception (e.g., gh not found)."""
    from app import _get_gh_token

    with patch("subprocess.run", side_effect=FileNotFoundError("No such file or directory: 'gh'")):
        token = _get_gh_token()
        assert token == ""
