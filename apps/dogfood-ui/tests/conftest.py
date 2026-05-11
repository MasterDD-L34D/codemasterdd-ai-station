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

    Caller can pass env vars (LANGFUSE_PROJECT_ID etc.) before building.
    """
    def _build(**env: str):
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
