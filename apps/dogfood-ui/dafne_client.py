"""Dafne swarm client — proxy verso API locale :5000."""
from __future__ import annotations

from typing import Any

import requests


class DafneClient:
    """Client minimal per Dafne swarm API (evo-swarm repo).

    Endpoint attesi (vedi camel-agents/api_server.py):
      GET /api/status                 — agents list, artifact count, ollama online
      GET /api/swarm/status           — cycle count, current agent, error state
      GET /api/stats                  — per-agent rolling window + levels
      GET /api/dafne/status           — dafne intervention history + drift
      GET /api/dafne/proposals        — proposals pending/approved/rejected
    """

    def __init__(
        self,
        host: str = "http://localhost:5000",
        timeout: float = 5.0,
        ping_timeout: float = 2.0,
    ) -> None:
        """
        timeout: per operazioni full-snapshot (swarm può essere mid-cycle con LLM busy → alza a 5s)
        ping_timeout: per liveness check rapido (aggressive OK perché /api/status è O(1))
        """
        self.host = host.rstrip("/")
        self.timeout = timeout
        self.ping_timeout = ping_timeout
        self.last_error: str | None = None

    # -----------------------------------------------------------------------
    # Core fetchers (return None on failure = server down / endpoint 404)
    # -----------------------------------------------------------------------

    def ping(self) -> bool:
        try:
            r = requests.get(f"{self.host}/api/status", timeout=self.ping_timeout)
            return r.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False

    def _get(self, path: str) -> dict[str, Any] | None:
        try:
            r = requests.get(f"{self.host}{path}", timeout=self.timeout)
            if r.status_code == 200:
                return r.json()
            return None
        except (requests.ConnectionError, requests.Timeout, ValueError):
            return None

    def status(self) -> dict[str, Any] | None:
        """GET /api/status -- agents list + artifact count + ollama online flag."""
        return self._get("/api/status")

    def swarm_status(self) -> dict[str, Any] | None:
        """GET /api/swarm/status -- cycle count + current agent + error state."""
        return self._get("/api/swarm/status")

    def stats(self) -> dict[str, Any] | None:
        """GET /api/stats -- per-agent rolling window + levels."""
        return self._get("/api/stats")

    def dafne_status(self) -> dict[str, Any] | None:
        """GET /api/dafne/status -- intervention history + drift state."""
        return self._get("/api/dafne/status")

    def proposals(self) -> dict[str, Any] | None:
        """GET /api/dafne/proposals -- pending + approved + rejected list."""
        return self._get("/api/dafne/proposals")

    # -----------------------------------------------------------------------
    # High-level rollup per dashboard
    # -----------------------------------------------------------------------

    def _build_kpis(self, status: dict[str, Any], swarm: dict[str, Any]) -> dict[str, Any]:
        return {
            "cycles_total": swarm.get("cycle_count", 0),
            "cycles_ok": swarm.get("cycles_ok", 0),
            "cycles_rejected": swarm.get("cycles_rejected", 0),
            "current_agent": swarm.get("current_agent"),
            "next_specialist": swarm.get("specialist_next"),
            "swarm_status": swarm.get("status"),
            "ollama_online": status.get("ollama_online", False),
            "artifacts_count": status.get("artifacts_count", 0),
            "agents_count": len(status.get("agents_available", [])),
            "last_error": swarm.get("last_error"),
        }

    def _build_intervention(self, dafne: dict[str, Any]) -> dict[str, Any]:
        return {
            "count": dafne.get("intervention_count", 0),
            "active": dafne.get("intervention_active", False),
            "last_at": dafne.get("last_intervention_at"),
            "last_focus": dafne.get("last_focus_directive"),
            "last_assessment": dafne.get("last_assessment"),
            "drifting": (dafne.get("flint") or {}).get("is_drifting", False),
            "gameplay_ratio": (dafne.get("flint") or {}).get("gameplay_ratio"),
        }

    def _build_stats_levels(self, agents: dict[str, Any]) -> dict[str, list[str]]:
        by_level: dict[str, list[str]] = {"Maestro": [], "Specialista": [], "Esperto": [], "Apprendista": []}
        for name, info in agents.items():
            lvl_name = info.get("level_name", "Apprendista")
            by_level.setdefault(lvl_name, []).append(name)
        return by_level

    def _build_stats_agents_detail(self, agents: dict[str, Any]) -> list[dict[str, Any]]:
        details = [
            {
                "name": name,
                "level": info.get("level_name"),
                "cycles": info.get("total_cycles", 0),
                "accept_rate": info.get("accept_rate"),
                "avg_score": info.get("avg_score"),
                "rejected": info.get("rejected", 0),
                "security_alerts": info.get("security_alerts", 0),
            }
            for name, info in agents.items()
        ]
        details.sort(key=lambda a: a.get("cycles", 0), reverse=True)
        return details

    def _build_proposals_summary(self, proposals: dict[str, Any]) -> dict[str, Any]:
        return {
            "total": len(proposals.get("all", [])) if proposals.get("all") else 0,
            "pending": sum(1 for p in (proposals.get("all") or []) if p.get("status") == "pending"),
            "approved": sum(1 for p in (proposals.get("all") or []) if p.get("status") == "approved"),
            "rejected": sum(1 for p in (proposals.get("all") or []) if p.get("status") == "rejected"),
        }

    def full_snapshot(self) -> dict[str, Any]:
        """Aggrega tutti gli endpoint in un singolo dict dashboard-friendly.

        Degrada gracefully: campi None se endpoint unreachable.
        """
        status = self.status()
        swarm = self.swarm_status()
        stats = self.stats()
        dafne = self.dafne_status()
        proposals = self.proposals()

        rollup: dict[str, Any] = {
            "reachable": status is not None,
            "host": self.host,
            "status": status,
            "swarm": swarm,
            "dafne": dafne,
        }

        # Derive compact KPIs
        if status and swarm:
            rollup["kpi"] = self._build_kpis(status, swarm)

        if dafne:
            rollup["intervention"] = self._build_intervention(dafne)

        if stats:
            agents = stats.get("agents") or {}
            rollup["levels"] = self._build_stats_levels(agents)
            rollup["agents_detail"] = self._build_stats_agents_detail(agents)

        if proposals and isinstance(proposals, dict):
            rollup["proposals_summary"] = self._build_proposals_summary(proposals)

        return rollup
