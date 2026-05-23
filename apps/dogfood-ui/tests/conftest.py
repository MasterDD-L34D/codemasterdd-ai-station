"""Shared pytest fixtures for dogfood-ui tests.

Each test gets an isolated SQLite DB in a tmp_path so tests don't see each
other's entries. The app factory is re-imported under a monkeypatched DB_PATH
so we don't touch the developer's real data/dogfood.sqlite.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


@pytest.fixture
def app_factory(tmp_path, monkeypatch):
    """Returns a callable that builds a fresh app bound to a tmp SQLite DB.

    Caller can pass env vars (LANGFUSE_PROJECT_ID etc.) before building. All
    Langfuse/Dafne/LiteLLM env vars are cleared first so the test environment
    never inherits a developer's exported config (e.g. a real
    LANGFUSE_PROJECT_ID flipping URL rendering to project-scoped mode).
    """
    HERMETIC_VARS = (
        "LANGFUSE_HOST", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY",
        "LANGFUSE_PROJECT_ID", "DAFNE_HOST", "LITELLM_ENDPOINT",
        "TAVILY_API_KEY", "TAVILY_ENDPOINT", "OPENCODE_CONFIG_PATH",
        "API_KEYS_FILE",
        "FLASK_SECRET", "API_SECRET",
    )

    def _build(**env: str):
        for var in HERMETIC_VARS:
            monkeypatch.delenv(var, raising=False)

        # Ensure a secret key is present for testing if not explicitly provided
        if "FLASK_SECRET" not in env:
            monkeypatch.setenv("FLASK_SECRET", "test-secret-key")
        if "API_SECRET" not in env:
            monkeypatch.setenv("API_SECRET", "test-api-secret")

        for k, v in env.items():
            monkeypatch.setenv(k, v)
        # Reload the module so module-level config picks up monkeypatched env.
        import app as app_mod
        importlib.reload(app_mod)
        monkeypatch.setattr(app_mod, "DB_PATH", tmp_path / "dogfood.sqlite")
        flask_app = app_mod.create_app()
        flask_app.config["TESTING"] = True
        return flask_app, app_mod

    return _build


@pytest.fixture
def client(app_factory):
    flask_app, _ = app_factory(
        LANGFUSE_HOST="http://lf.example.com",
        LANGFUSE_PUBLIC_KEY="pk-test",
        LANGFUSE_SECRET_KEY="sk-test",
    )
    return flask_app.test_client()


@pytest.fixture
def client_with_project(app_factory):
    flask_app, _ = app_factory(
        LANGFUSE_HOST="http://lf.example.com",
        LANGFUSE_PUBLIC_KEY="pk-test",
        LANGFUSE_SECRET_KEY="sk-test",
        LANGFUSE_PROJECT_ID="proj-abc",
    )
    return flask_app.test_client()
