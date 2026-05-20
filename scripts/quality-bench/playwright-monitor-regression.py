"""OD-051 FE1 — Tiered T1+T2+T3 Playwright-direct regression on dogfood-ui /monitor.

Usage:
    # Pre-req: Flask dogfood-ui running on the port reported below.
    python scripts/quality-bench/playwright-monitor-regression.py

Tiered gates (independent verdicts per harsh-review P0.2):
    T1: Playwright executability  (covered by import + version + binary path)
    T2: Headless render /monitor  (5 objective asserts)
    T3: Interactive nav-click flow (4 objective asserts)

Exits 0 if all asserts pass. Non-zero exit indicates which tier+assert failed.

OD-051 reference: vault docs/decisions/OD-051-browser-agentic-loop-sdmg-gate-2026-05-20.md
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("DOGFOOD_UI_BASE", "http://localhost:8080")
SCREENSHOT_DIR = Path(__file__).parent / "results"
SCREENSHOT_DIR.mkdir(exist_ok=True)
SCREENSHOT_PATH = SCREENSHOT_DIR / "screenshot-fe1-t2.png"


def assert_eq(name: str, actual, expected) -> None:
    if actual != expected:
        print(f"FAIL {name}: expected={expected!r} actual={actual!r}", file=sys.stderr)
        sys.exit(2)
    print(f"PASS {name}: {actual!r}")


def assert_contains(name: str, haystack: str, needle: str) -> None:
    if needle not in haystack:
        print(f"FAIL {name}: needle={needle!r} not in haystack[:200]={haystack[:200]!r}", file=sys.stderr)
        sys.exit(2)
    print(f"PASS {name}: contains {needle!r}")


def assert_ge(name: str, actual: int, threshold: int) -> None:
    if actual < threshold:
        print(f"FAIL {name}: actual={actual} < threshold={threshold}", file=sys.stderr)
        sys.exit(2)
    print(f"PASS {name}: {actual} >= {threshold}")


def main() -> int:
    print(f"[FE1] BASE_URL={BASE_URL}")
    print(f"[FE1] SCREENSHOT={SCREENSHOT_PATH}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # ===== T2: Headless render /monitor =====
        print("\n=== T2: Headless render /monitor ===")
        response = page.goto(f"{BASE_URL}/monitor")
        assert_eq("T2.1 HTTP status", response.status if response else None, 200)
        assert_eq("T2.2 final URL", page.url.rstrip("/"), f"{BASE_URL}/monitor")

        h1_text = page.locator("h1").first.text_content()
        assert_contains("T2.3 h1 contains expected", h1_text or "", "Cross-repo drift monitor")

        tr_count = page.locator("table.data-table tbody tr").count()
        assert_ge("T2.4 tbody tr count >= 1", tr_count, 1)

        refresh_content = page.locator("meta[http-equiv='refresh']").get_attribute("content")
        if not refresh_content or not refresh_content.startswith("120"):
            print(f"FAIL T2.5 refresh meta: content={refresh_content!r}", file=sys.stderr)
            sys.exit(2)
        print(f"PASS T2.5 refresh meta: {refresh_content!r}")

        page.screenshot(path=str(SCREENSHOT_PATH))
        size = SCREENSHOT_PATH.stat().st_size
        assert_ge("T2.6 screenshot size > 5KB", size, 5000)

        # ===== T3: Interactive click flow =====
        print("\n=== T3: Interactive click flow ===")
        response_stats = page.goto(f"{BASE_URL}/stats")
        assert_eq("T3.1 /stats HTTP status", response_stats.status if response_stats else None, 200)

        nav_link = page.locator("a[href='/monitor']").first
        nav_link.click()
        print("PASS T3.2 nav click executed")

        page.wait_for_url("**/monitor", timeout=5000)
        assert_contains("T3.3 URL transitions to /monitor", page.url, "/monitor")

        tr_count_post_click = page.locator("table.data-table tbody tr").count()
        assert_ge("T3.4 tbody tr count post-click >= 1", tr_count_post_click, 1)

        browser.close()

    print("\n=== ALL TIERS PASS ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
