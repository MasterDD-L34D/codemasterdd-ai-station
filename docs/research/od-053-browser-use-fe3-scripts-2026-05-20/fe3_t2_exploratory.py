"""OD-053 FE3 T2: real-surface exploratory bug-find on Game-Database React."""
import os
import sys
import time
from pathlib import Path


def load_keys_env(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def main() -> int:
    keys = load_keys_env(Path(r"C:\Users\VGit\.config\api-keys\keys.env"))
    api_key = keys.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("FAIL: no ANTHROPIC_API_KEY", file=sys.stderr)
        return 2

    os.environ["ANTHROPIC_API_KEY"] = api_key
    for sus in ("OPENAI_API_KEY", "GROQ_API_KEY", "CEREBRAS_API_KEY",
                "GEMINI_API_KEY", "GOOGLE_GENERATIVE_AI_API_KEY"):
        os.environ.pop(sus, None)

    print(f"[FE3-T2] ANTHROPIC_API_KEY set, other provider keys scrubbed")

    from browser_use import Agent, ChatAnthropic

    llm = ChatAnthropic(model="claude-sonnet-4-5")

    # Real-surface exploratory task. Game-Database React dashboard.
    # Goal: find anomalies (visual / behavior / data quality issues).
    # Eduardo will manually triage signal:noise post-run.
    task = (
        "Explore the dashboard at http://localhost:5174 systematically. "
        "Visit the main page, click navigation links, examine tables and "
        "widgets. Look for visual anomalies (broken layouts, overlapping "
        "elements, missing icons), behavior anomalies (broken links, "
        "console errors, failed API calls), data quality issues (empty "
        "tables that should have data, inconsistent labels, mixed "
        "languages where it should be one), or accessibility problems. "
        "Report 3-5 specific findings with selectors or visual descriptions. "
        "If you find no anomalies after exploring 3-4 pages, report 'no "
        "anomalies found' with a summary of what you inspected. Budget hard "
        "stop: 25 steps maximum."
    )

    agent = Agent(task=task, llm=llm)
    print(f"[FE3-T2] Agent constructed, max_steps=25 budget cap")

    import asyncio
    start = time.time()
    try:
        history = asyncio.run(agent.run(max_steps=25))
    except Exception as e:
        print(f"FAIL: agent.run raised {type(e).__name__}: {e}", file=sys.stderr)
        return 3
    elapsed = time.time() - start

    print(f"\n[FE3-T2] elapsed={elapsed:.1f}s")
    try:
        result = history.final_result() if hasattr(history, "final_result") else str(history)
        print(f"\n[FE3-T2] FINAL REPORT:\n{result}\n")
    except Exception as e:
        print(f"[FE3-T2] history (raw): {history}")

    # Try to extract steps count + token usage if available
    try:
        if hasattr(history, "history"):
            print(f"[FE3-T2] steps executed: {len(history.history)}")
        if hasattr(history, "total_tokens"):
            print(f"[FE3-T2] total_tokens: {history.total_tokens}")
        if hasattr(history, "usage"):
            print(f"[FE3-T2] usage: {history.usage}")
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
