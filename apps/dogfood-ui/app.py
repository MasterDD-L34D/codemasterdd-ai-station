"""
CodeMasterDD AI Station — Dogfood UI (ADR-0017)

Mini-app Flask per tracciare dogfood Fase 6 + correlazione con bench results.
Legge/scrive da SQLite locale (source-of-truth) + optional sync con Langfuse.

Start:  python app.py
Debug:  FLASK_DEBUG=1 python app.py
Port:   8080 (cambia via PORT env var)
"""
from __future__ import annotations

import os
import csv
import io
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, Response

from db import Database
from langfuse_client import LangfuseClient
from dafne_client import DafneClient
from stats import aggregate_stats, aggregate_by_day, build_sparkline_svg, parse_promptfoo_results

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

APP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = APP_ROOT.parent.parent
DB_PATH = APP_ROOT / "data" / "dogfood.sqlite"
PROMPTFOO_LATEST = REPO_ROOT / "scripts" / "quality-bench" / "results" / "promptfoo-latest.json"

LITELLM_ENDPOINT = os.environ.get("LITELLM_ENDPOINT", "http://localhost:4000")
LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST", "http://localhost:3000")
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")
LANGFUSE_PROJECT_ID = os.environ.get("LANGFUSE_PROJECT_ID", "")
DAFNE_HOST = os.environ.get("DAFNE_HOST", "http://localhost:5000")

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")

    flask_secret = os.environ.get("FLASK_SECRET")
    if not flask_secret:
        raise RuntimeError("FLASK_SECRET environment variable is not set")
    app.secret_key = flask_secret

    db = Database(DB_PATH)
    db.init_schema()
    lf = LangfuseClient(
        host=LANGFUSE_HOST,
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
    )
    dafne = DafneClient(host=DAFNE_HOST)

    host = LANGFUSE_HOST.rstrip("/")

    def langfuse_trace_url(trace_id: str) -> str:
        if LANGFUSE_PROJECT_ID:
            return f"{host}/project/{LANGFUSE_PROJECT_ID}/traces/{trace_id}"
        return f"{host}/trace/{trace_id}"

    @app.context_processor
    def inject_langfuse_ctx() -> dict[str, Any]:
        return {
            "langfuse_host": host,
            "langfuse_project_id": LANGFUSE_PROJECT_ID,
            "langfuse_trace_url": langfuse_trace_url,
            "langfuse_configured": bool(LANGFUSE_PUBLIC_KEY),
        }

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

    @app.route("/entries/export.csv", methods=["GET"])
    def export_entries_csv():
        entries = db.list_entries(limit=10000)
        return _csv_response(entries, filename_prefix="dogfood-entries")

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
                "langfuse_trace_id": request.form.get("langfuse_trace_id", "").strip(),
                "note": request.form.get("note", "").strip(),
            }
            errors = validate_entry(payload)
            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template("new_entry.html", form=payload)
            pulled = enrich_from_langfuse(payload, lf)
            entry_id = db.insert_entry(payload)
            if pulled:
                flash(f"Entry #{entry_id} saved. Auto-filled from Langfuse: {', '.join(pulled)}.", "success")
            else:
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
        entries = db.list_entries()
        stats = aggregate_stats(entries)
        daily = aggregate_by_day(entries)
        sparkline_count = build_sparkline_svg(
            [d["count"] for d in daily],
            label="Entries per day",
            stroke="#3b82f6", fill="#3b82f650",
        )
        sparkline_cost = build_sparkline_svg(
            [d["cost_usd"] for d in daily],
            label="Cost USD per day",
            stroke="#10b981", fill="#10b98150",
        )
        return render_template(
            "stats.html",
            stats=stats,
            daily=daily,
            sparkline_count=sparkline_count,
            sparkline_cost=sparkline_cost,
        )

    @app.route("/bench")
    def bench_view():
        bench = None
        if PROMPTFOO_LATEST.exists():
            try:
                bench = parse_promptfoo_results(PROMPTFOO_LATEST)
            except (json.JSONDecodeError, KeyError) as exc:
                flash(f"Promptfoo results malformed: {exc}", "error")
        return render_template("bench.html", bench=bench, path=str(PROMPTFOO_LATEST))

    @app.route("/dafne")
    def dafne_view():
        snapshot = dafne.full_snapshot()
        return render_template("dafne.html", snapshot=snapshot, host=DAFNE_HOST)

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
            pulled = enrich_from_langfuse(payload, lf)
            entry_id = db.insert_entry(payload)
            return jsonify({
                "id": entry_id,
                "status": "created",
                "langfuse_autofilled": pulled,
            }), 201
        entries = db.list_entries(limit=int(request.args.get("limit", 100)))
        return jsonify([entry_to_dict(e) for e in entries])

    @app.route("/api/stats")
    def api_stats():
        return jsonify(aggregate_stats(db.list_entries()))

    # Health cache TTL 30s -- root cause fix /api/health 4s latency
    # (dafne.ping + lf.ping each ~2s timeout when services DOWN)
    # 2026-05-14 sera-tardi-ultra-2 per Eduardo "dogfood-ui slow latency"
    _health_cache: dict[str, Any] = {"data": None, "ts": 0.0}
    _HEALTH_TTL_SEC = 30.0

    @app.route("/api/health")
    def api_health():
        import time
        now = time.time()
        cached = _health_cache.get("data")
        if cached and (now - _health_cache["ts"]) < _HEALTH_TTL_SEC:
            cached_with_meta = dict(cached)
            cached_with_meta["cache_age_sec"] = round(now - _health_cache["ts"], 1)
            return jsonify(cached_with_meta)
        data = {
            "status": "ok",
            "app": "dogfood-ui",
            "version": "0.2.1",
            "db": db.health(),
            "langfuse": {
                "configured": bool(LANGFUSE_PUBLIC_KEY),
                "reachable": lf.ping() if LANGFUSE_PUBLIC_KEY else None,
            },
            "litellm_endpoint": LITELLM_ENDPOINT,
            "dafne": {
                "host": DAFNE_HOST,
                "reachable": dafne.ping(),
            },
            "promptfoo_results_available": PROMPTFOO_LATEST.exists(),
            "cache_age_sec": 0,
        }
        _health_cache["data"] = data
        _health_cache["ts"] = now
        return jsonify(data)

    @app.route("/api/dafne/snapshot")
    def api_dafne_snapshot():
        """Proxy snapshot aggregato da Dafne :5000."""
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


def enrich_from_langfuse(payload: dict[str, Any], lf: LangfuseClient) -> list[str]:
    """Best-effort auto-pull of tokens/cost/latency from Langfuse.

    Only fills payload fields that are zero/missing - never overrides explicit
    user-supplied values. Returns the list of field names that were auto-filled
    (empty if no trace_id, Langfuse unreachable, or trace had no usable data).
    """
    trace_id = (payload.get("langfuse_trace_id") or "").strip()
    if not trace_id:
        return []
    metadata = lf.fetch_metadata(trace_id)
    if not metadata:
        return []
    filled: list[str] = []
    for key in ("tokens_sent", "tokens_received", "cost_usd", "latency_ms"):
        if key in metadata and not payload.get(key):
            payload[key] = metadata[key]
            filled.append(key)
    return filled


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


CSV_COLUMNS = [
    "id", "created_at", "task_description", "classe", "stack",
    "constraint_count", "outcome", "retry_count",
    "tokens_sent", "tokens_received", "cost_usd", "latency_ms",
    "commit_hash", "note", "langfuse_trace_id",
]


def _csv_response(entries: list[sqlite3.Row], filename_prefix: str) -> Response:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for row in entries:
        d = dict(row)
        d.setdefault("latency_ms", 0)
        writer.writerow({k: d.get(k, "") for k in CSV_COLUMNS})
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{filename_prefix}-{stamp}.csv"
    return Response(
        buf.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app = create_app()
    app.run(host="127.0.0.1", port=port, debug=debug)
