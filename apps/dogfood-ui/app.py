"""
CodeMasterDD AI Station - Dogfood UI (ADR-0017)

Mini-app Flask per tracciare dogfood Fase 6 + correlazione con bench results.
Legge/scrive da SQLite locale (source-of-truth) + optional sync con Langfuse.

Start:  python app.py
Debug:  FLASK_DEBUG=1 python app.py
Port:   8080 (cambia via PORT env var)
"""
from __future__ import annotations

import os
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

from db import Database
from langfuse_client import LangfuseClient
from dafne_client import DafneClient
from stats import aggregate_stats, parse_promptfoo_results

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

APP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = APP_ROOT.parent.parent
DB_PATH = APP_ROOT / "data" / "dogfood.sqlite"
PROMPTFOO_LATEST = (
    REPO_ROOT / "scripts" / "quality-bench" / "results" / "promptfoo-latest.json"
)

LITELLM_ENDPOINT = os.environ.get("LITELLM_ENDPOINT", "http://localhost:4000")
LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST", "http://localhost:3000")
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")
DAFNE_HOST = os.environ.get("DAFNE_HOST", "http://localhost:5000")
DAFNE_ENABLED = os.environ.get("DAFNE_ENABLED", "0").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = os.environ.get("FLASK_SECRET", "dev-only-not-for-prod-codemasterdd")

    db = Database(DB_PATH)
    db.init_schema()
    lf = LangfuseClient(
        host=LANGFUSE_HOST,
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
    )
    dafne = DafneClient(host=DAFNE_HOST) if DAFNE_ENABLED else None

    # -----------------------------------------------------------------------
    # Routes
    # -----------------------------------------------------------------------

    @app.route("/")
    def index():
        entries = db.list_entries(limit=50)
        stats = aggregate_stats(db.list_entries())
        return render_template(
            "index.html",
            entries=entries,
            stats=stats,
            langfuse_configured=bool(LANGFUSE_PUBLIC_KEY),
        )

    @app.route("/entries", methods=["GET"])
    def list_entries():
        entries = db.list_entries(limit=500)
        return render_template("entries.html", entries=entries)

    @app.route("/entries/new", methods=["GET", "POST"])
    def new_entry():
        if request.method == "POST":
            payload = {
                "task_description": request.form.get("task_description", "").strip(),
                "classe": request.form.get("classe", "").strip(),
                "stack": request.form.get("stack", "").strip(),
                "constraint_count": int(request.form.get("constraint_count", 0) or 0),
                "outcome": request.form.get("outcome", "").strip(),
                "retry_count": int(request.form.get("retry_count", 0) or 0),
                "tokens_sent": int(request.form.get("tokens_sent", 0) or 0),
                "tokens_received": int(request.form.get("tokens_received", 0) or 0),
                "cost_usd": float(request.form.get("cost_usd", 0) or 0),
                "commit_hash": request.form.get("commit_hash", "").strip(),
                "note": request.form.get("note", "").strip(),
            }
            errors = validate_entry(payload)
            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template("new_entry.html", form=payload)
            entry_id = db.insert_entry(payload)
            flash(f"Entry #{entry_id} saved.", "success")
            return redirect(url_for("list_entries"))
        return render_template("new_entry.html", form={})

    @app.route("/entries/<int:entry_id>/delete", methods=["POST"])
    def delete_entry(entry_id: int):
        db.delete_entry(entry_id)
        flash(f"Entry #{entry_id} deleted.", "success")
        return redirect(url_for("list_entries"))

    @app.route("/stats")
    def stats_view():
        stats = aggregate_stats(db.list_entries())
        return render_template("stats.html", stats=stats)

    @app.route("/bench")
    def bench_view():
        bench = None
        if PROMPTFOO_LATEST.exists():
            try:
                bench = parse_promptfoo_results(PROMPTFOO_LATEST)
            except (json.JSONDecodeError, KeyError) as exc:
                flash(f"Promptfoo results malformed: {exc}", "error")
        return render_template("bench.html", bench=bench, path=str(PROMPTFOO_LATEST))

    @app.route("/recovery")
    def recovery_view():
        snapshot = recovery_snapshot(db=db, dafne_enabled=DAFNE_ENABLED)
        return render_template("recovery.html", snapshot=snapshot)

    @app.route("/dafne")
    def dafne_view():
        if not DAFNE_ENABLED or dafne is None:
            return render_template(
                "dafne.html",
                disabled=True,
                snapshot={"reachable": False},
                host=DAFNE_HOST,
            )
        snapshot = dafne.full_snapshot()
        return render_template(
            "dafne.html",
            disabled=False,
            snapshot=snapshot,
            host=DAFNE_HOST,
        )

    # -----------------------------------------------------------------------
    # JSON API (for external tools / scripts / future CLI integration)
    # -----------------------------------------------------------------------

    @app.route("/api/entries", methods=["GET", "POST"])
    def api_entries():
        if request.method == "POST":
            payload = request.get_json(silent=True) or {}
            errors = validate_entry(payload)
            if errors:
                return jsonify({"errors": errors}), 400
            entry_id = db.insert_entry(payload)
            return jsonify({"id": entry_id, "status": "created"}), 201
        entries = db.list_entries(limit=int(request.args.get("limit", 100)))
        return jsonify([entry_to_dict(e) for e in entries])

    @app.route("/api/stats")
    def api_stats():
        return jsonify(aggregate_stats(db.list_entries()))

    @app.route("/api/health")
    def api_health():
        return jsonify({
            "status": "ok",
            "app": "dogfood-ui",
            "version": "0.2.0",
            "db": db.health(),
            "langfuse": {
                "configured": bool(LANGFUSE_PUBLIC_KEY),
                "reachable": lf.ping() if LANGFUSE_PUBLIC_KEY else None,
            },
            "litellm_endpoint": LITELLM_ENDPOINT,
            "dafne": {
                "enabled": DAFNE_ENABLED,
                "host": DAFNE_HOST,
                "reachable": dafne.ping() if DAFNE_ENABLED and dafne is not None else None,
            },
            "promptfoo_results_available": PROMPTFOO_LATEST.exists(),
        })

    @app.route("/api/dafne/snapshot")
    def api_dafne_snapshot():
        """Proxy snapshot aggregato da Dafne :5000."""
        if not DAFNE_ENABLED or dafne is None:
            return jsonify({
                "reachable": False,
                "enabled": False,
                "message": "Dafne integration disabled. Set DAFNE_ENABLED=1 to enable.",
            })
        return jsonify(dafne.full_snapshot())

    return app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_CLASSES = {"cosmetic", "behavior", "strategic"}
VALID_OUTCOMES = {"success", "partial", "reject", "safe-fail", "hook-block", "error"}
VALID_STACKS = {
    "7B-local-whole",
    "14B-Q2-local-diff",
    "30B-MoE-local-diff",
    "R1-8B-local",
    "gemma4-multimodal-local",
    "groq-70b-cloud",
    "cerebras-8b-cloud",
    "gemini-flash-cloud",
    "openai-4o-mini-cloud",
    "claude-code-direct",
    "other",
}


def validate_entry(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not payload.get("task_description"):
        errors.append("task_description required")
    if payload.get("classe") not in VALID_CLASSES:
        errors.append(f"classe must be one of {sorted(VALID_CLASSES)}")
    if payload.get("stack") not in VALID_STACKS:
        errors.append(f"stack must be one of {sorted(VALID_STACKS)}")
    if payload.get("outcome") not in VALID_OUTCOMES:
        errors.append(f"outcome must be one of {sorted(VALID_OUTCOMES)}")
    return errors


def entry_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)


def recovery_snapshot(db: Database, dafne_enabled: bool) -> dict[str, Any]:
    """Return recovery status from files present in this checkout."""
    docs = {
        "PROJECT_STATE.yaml": REPO_ROOT / "PROJECT_STATE.yaml",
        "EXTERNAL_REPOS.md": REPO_ROOT / "EXTERNAL_REPOS.md",
        "SPRINT_02.md": REPO_ROOT / "SPRINT_02.md",
        "transplant audit": (
            REPO_ROOT / "docs" / "recovery" / "2026-04-30-transplant-audit.md"
        ),
        "active boundary": (
            REPO_ROOT / "docs" / "recovery" / "active-vs-historical-boundary.md"
        ),
        "pre-merge checklist": REPO_ROOT / "docs" / "recovery" / "pre-merge-checklist.md",
    }
    runtime = {
        "dogfood log": REPO_ROOT / "logs" / "aider-delegation-2026-04.md",
        "dogfood sqlite": DB_PATH,
        "promptfoo results": REPO_ROOT / "scripts" / "quality-bench" / "results",
    }
    external = {
        "Game": Path("C:/dev/Game"),
        "Synesthesia": Path("C:/dev/synesthesia"),
        "Dafne swarm": Path("C:/Users/edusc/Dafne/workspace/swarm"),
        "AA01": Path("C:/Users/edusc/aa01"),
    }
    db_health = db.health()
    return {
        "mode": "structural_recovery",
        "repo_root": str(REPO_ROOT),
        "docs": [
            {"name": name, "exists": path.exists(), "path": str(path)}
            for name, path in docs.items()
        ],
        "runtime": [
            {"name": name, "exists": path.exists(), "path": str(path)}
            for name, path in runtime.items()
        ],
        "external": [
            {"name": name, "exists": path.exists(), "path": str(path)}
            for name, path in external.items()
        ],
        "db": db_health,
        "dafne_enabled": dafne_enabled,
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app = create_app()
    app.run(host="127.0.0.1", port=port, debug=debug)
