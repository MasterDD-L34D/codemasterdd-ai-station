"""Fleet-wide dashboard catalog (data-only registry).

Curated from the 2026-07-02 six-area inventory sweep (hub / Game tools /
Game served / swarm / Godot+DB / loose artifacts). Consumed by the
/cross-repo/dashboards route and by /api/regen-dashboard.

SECURITY CONTRACT: `regen.steps` are FIXED argv lists (no shell, no user
input ever interpolated). /api/regen-dashboard accepts only a registry id
and executes these exact argv lists -- adding an entry here is the only
way to make something runnable from the UI (reviewed like code, because
it is code).

Status semantics: live = serving/refreshing now | regenerable = script
reproduces it on demand | stale = outdated snapshot kept for history |
one-shot = point-in-time artifact, arc closed.
"""
from __future__ import annotations

from typing import Any

GAME = r"C:\dev\Game"
HUB = r"C:\dev\codemasterdd-ai-station"

DASHBOARDS: list[dict[str, Any]] = [
    # ------------------------------------------------------------- hub
    {
        "id": "cross-repo-index",
        "name": "Cross-repo fleet dashboard",
        "area": "hub", "kind": "served", "status": "live",
        "desc": "Questa piattaforma: repo cards, healthcheck, governor, ADR countdown.",
        "open": "http://127.0.0.1:8081/cross-repo/",
    },
    {
        "id": "governor-pane",
        "name": "Governor R0 signal pane",
        "area": "hub", "kind": "served", "status": "live",
        "desc": "Segnali consolidati read-only (vault eng-graph, evo digest, sot-drift).",
        "open": "http://127.0.0.1:8081/cross-repo/governor",
    },
    {
        "id": "governance-lint",
        "name": "Governance lint report",
        "area": "hub", "kind": "generator", "status": "regenerable",
        "desc": "Drift detection: COMPACT_CONTEXT vs origin, PR claims, journal staleness.",
        "open": HUB + r"\logs",
        "regen": {
            "cwd": HUB,
            "steps": [["powershell", "-NoProfile", "-File", "scripts/governance-lint.ps1"]],
            "timeout": 120,
            # linter semantics: rc=1 = "findings found" (report written anyway)
            "ok_exit_codes": [0, 1],
        },
    },
    {
        "id": "chatgpt-recovery-dash",
        "name": "ChatGPT recovery progress",
        "area": "hub", "kind": "generator", "status": "one-shot",
        "desc": "Arco recovery chiuso: generatore markdown di avanzamento export.",
        "open": HUB + r"\chatgpt-recovery\pipeline\live-dashboard.py",
    },
    # ------------------------------------------------------------ game
    {
        "id": "playtest-dashboard",
        "name": "AI-Playtest dashboard (Chart.js)",
        "area": "Game", "kind": "generator", "status": "regenerable",
        "desc": "KPI batch-sim: outcomes, WR per scenario vs banda 30-50%, damage per "
                "specie/job, funnel per turno. Post-F2/F3: timeout e scenario_id reali.",
        "open": GAME + r"\logs\reports\evo_playtest_dashboard.html",
        "regen": {
            "cwd": GAME,
            "steps": [
                ["py", "tools/py/aggregate_session_logs.py"],
                ["py", "tools/py/build_playtest_dashboard.py"],
            ],
            "timeout": 600,
        },
    },
    {
        "id": "sparkline-dashboard",
        "name": "Tufte sparkline telemetry",
        "area": "Game", "kind": "generator", "status": "regenerable",
        "desc": "Small-multiples: win-rate, durata sessioni, kill, skip-rate, funnel tutorial.",
        "open": GAME + r"\out\sparkline_dashboard.html",
        "regen": {
            "cwd": GAME,
            "steps": [["py", "tools/py/sparkline_dashboard.py"]],
            "timeout": 300,
        },
    },
    {
        "id": "trait-completion",
        "name": "Trait completion KPI (markdown)",
        "area": "Game", "kind": "generator", "status": "regenerable",
        "desc": "Copertura metadati trait: species_affinity, biome_tags, completion_flags.",
        "open": GAME + r"\reports\trait_progress.md",
        "regen": {
            "cwd": GAME,
            "steps": [["py", "tools/py/trait_completion_dashboard.py"]],
            "timeout": 300,
        },
    },
    {
        "id": "mission-console",
        "name": "Mission Console (Vue SPA)",
        "area": "Game", "kind": "served", "status": "live",
        "desc": "Console operativa: flow validation, telemetria, proxy API verso :3334.",
        "open": "http://127.0.0.1:5555/",
        "launch_hint": "node scripts/serve-mission-console.mjs (da C:\\dev\\Game)",
    },
    {
        "id": "game-docs-hub",
        "name": "Game docs hub (landing)",
        "area": "Game", "kind": "static", "status": "live",
        "desc": "Landing Game che linka console, generator ecosistema, report pack.",
        "open": GAME + r"\docs\index.html",
    },
    {
        "id": "pack-generator",
        "name": "Ecosystem pack generator UI",
        "area": "Game", "kind": "static", "status": "live",
        "desc": "Generazione procedurale missioni/biomi/encounter con filtri e export dossier.",
        "open": GAME + r"\docs\evo-tactics-pack\generator.html",
    },
    {
        "id": "pack-reports",
        "name": "Ecosystem pack reports",
        "area": "Game", "kind": "static", "status": "regenerable",
        "desc": "Overview meta-ecosistema + dettaglio biomi + species index.",
        "open": GAME + r"\docs\evo-tactics-pack\reports\index.html",
    },
    {
        "id": "pack-catalog",
        "name": "Pack catalog explorer",
        "area": "Game", "kind": "static", "status": "live",
        "desc": "Browser interattivo biomi/specie/ecosistemi.",
        "open": GAME + r"\docs\evo-tactics-pack\catalog.html",
    },
    {
        "id": "pack-validation",
        "name": "Pack validation report",
        "area": "Game", "kind": "static", "status": "regenerable",
        "desc": "Schema compliance + integrita' referenziale ultimo run.",
        "open": GAME + r"\packs\evo_tactics_pack\out\validation\last_report.html",
    },
    {
        "id": "showcase-dossier",
        "name": "Showcase dossier",
        "area": "Game", "kind": "static", "status": "regenerable",
        "desc": "Press-kit: pitch ecosistema + specie chiave + preview meccaniche.",
        "open": GAME + r"\docs\presentations\showcase\evo-tactics-showcase-dossier.html",
    },
    {
        "id": "session-reports-2025",
        "name": "Playtest session reports 2025",
        "area": "Game", "kind": "static", "status": "stale",
        "desc": "Report sessioni 2025-10/11: storici, superati dal batch-sim corrente.",
        "open": GAME + r"\docs\reports\incoming\latest\report.html",
    },
    # ----------------------------------------------------------- other
    {
        "id": "swarm-observability",
        "name": "Swarm observability (Alpine+ECharts)",
        "area": "Dafne swarm", "kind": "served", "status": "live",
        "desc": "Fasi #93-#102 complete: stato agenti, cicli, KPI, telemetria JSONL.",
        "open": "http://127.0.0.1:5000/",
        "launch_hint": "START-SWARM.ps1 (sovereign-only)",
    },
    {
        "id": "gdb-dashboard",
        "name": "Game-Database CMS dashboard",
        "area": "Game-Database", "kind": "served", "status": "live",
        "desc": "Admin taxonomy React+MUI: record KPI, entita', qualita'.",
        "open": "http://127.0.0.1:3333/api/dashboard",
        "launch_hint": "npm start (server :3333) + app dashboard Vite",
    },
    {
        "id": "vault-reconciliation-map",
        "name": "Reconciliation master map",
        "area": "vault", "kind": "static", "status": "live",
        "desc": "Matrice 31 game-inspiration -> DF levels, pillar, milestone.",
        "open": r"C:\dev\vault\Spaces\Dev\Evo-Tactics\core\reconciliation-master-map.html",
    },
]

# Overnight/long-running batch runs surfaced in the "run attive" section.
# freshness_stall_min: newest file older than this -> STALLED badge.
RUN_MONITORS: list[dict[str, Any]] = [
    {
        "id": "map-elites-hc06-overnight",
        "name": "MAP-Elites hardcore_06 overnight (QD archive)",
        "trial_dir": GAME + r"\docs\playtest\map-elites-hardcore_06-overnight-20260702",
        "total_iter": 50,
        "n_per_trial": 40,
        "monitor_html": GAME + r"\logs\map_elites_monitor.html",
        "freshness_stall_min": 90,
    },
]
