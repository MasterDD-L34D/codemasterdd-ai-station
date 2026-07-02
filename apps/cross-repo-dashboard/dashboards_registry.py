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
        "name": "Tufte sparkline telemetry (RITIRATA)",
        "area": "Game", "kind": "generator", "status": "stale",
        # Ponytail audit 2026-07-02: legge logs/telemetry_*.jsonl con eventi
        # 'session_complete' -- stream MAI popolato e schema mai emesso dal
        # backend (session logs reali = array JSON con session_end/win).
        # Dashboard costruita contro una spec, mai contro dati. Regen rimosso.
        # L'intento (trend nel tempo) e' coperto da sessions_by_day/outcome_by_day
        # nella AI-Playtest dashboard.
        "desc": "RITIRATA: leggeva uno stream telemetry mai esistito (schema drift). "
                "Trend temporali -> AI-Playtest dashboard.",
        "open": GAME + r"\tools\py\sparkline_dashboard.py",
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
        "id": "ermes-report",
        "name": "ERMES eco-pressure report",
        "area": "Game", "kind": "generator", "status": "regenerable",
        "desc": "Report statico multi-bioma dal boot ERMES: bande diegetiche, bias "
                "encounter/mutazione, rischi estinzione. Sostituisce il workbench "
                "Streamlit FASE-1 (morto). Salvage 2026-07-02.",
        "open": GAME + r"\logs\reports\ermes_report.html",
        "regen": {
            "cwd": GAME,
            "steps": [["py", "tools/py/build_ermes_report.py"]],
            "timeout": 120,
        },
    },
    {
        "id": "hud-canary-report",
        "name": "HUD canary alerts report",
        "area": "Game", "kind": "generator", "status": "regenerable",
        "desc": "KPI pipeline HUD Smart Alerts (ack rate vs 80%, filter ratio, trend "
                "per sessione) dai log playtest reali. Soglie importate dal QA gate. "
                "Salvage 2026-07-02.",
        "open": GAME + r"\logs\qa\hud_canary_report.html",
        "regen": {
            "cwd": GAME,
            "steps": [["py", "tools/feedback/build_hud_canary_report.py"]],
            "timeout": 120,
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
    # v1 entry (map-elites-hc06-overnight, trial_dir ...-overnight-20260702)
    # retired 2026-07-02: run interrupted 25/50, negative result (Game
    # docs/research/2026-07-02-map-elites-hc06-overnight-negative-result.md).
    # v2 below uses the PINNED label the launch will pass via --label
    # (Game PR #3181); the card reads "absent" until the run starts.
    {
        "id": "map-elites-hc06-v2",
        "name": "MAP-Elites v2 hardcore_06 (WR x turns QD archive)",
        "trial_dir": GAME + r"\docs\playtest\map-elites-hardcore_06-v2-run",
        "total_iter": 50,
        "n_per_trial": 40,
        "freshness_stall_min": 30,
    },
    # edm follow-up run (Game PR #3183: knob-space SoT-full, WR floor 15%).
    # Run COMPLETE 2026-07-02 (50/50 iter); card kept to consult the archive.
    {
        "id": "map-elites-hc06-v2-edm",
        "name": "MAP-Elites v2 hardcore_06 edm-run (enemy_damage knob)",
        "trial_dir": GAME + r"\docs\playtest\map-elites-hardcore_06-v2-edm-run",
        "total_iter": 50,
        "n_per_trial": 40,
        "freshness_stall_min": 30,
    },
]
