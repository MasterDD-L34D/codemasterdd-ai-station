"""OD-053 FE3 T1 smoke: explicit ChatAnthropic + tiny task verify."""
import os
import sys
import time
from pathlib import Path


def load_keys_env(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def main() -> int:
    keys_path = Path(r"C:\Users\VGit\.config\api-keys\keys.env")
    keys = load_keys_env(keys_path)
    api_key = keys.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("FAIL: ANTHROPIC_API_KEY missing in keys.env", file=sys.stderr)
        return 2
    os.environ["ANTHROPIC_API_KEY"] = api_key

    # P0-3 enforcement: scrub other provider keys to prevent silent fallback
    for sus in ("OPENAI_API_KEY", "GROQ_API_KEY", "CEREBRAS_API_KEY",
                "GEMINI_API_KEY", "GOOGLE_GENERATIVE_AI_API_KEY"):
        os.environ.pop(sus, None)

    print(f"[FE3-T1] ANTHROPIC_API_KEY set (len={len(api_key)}), other provider keys scrubbed")

    from browser_use import Agent, ChatAnthropic
    print(f"[FE3-T1] browser-use import OK")

    llm = ChatAnthropic(model="claude-sonnet-4-5")
    print(f"[FE3-T1] ChatAnthropic explicit constructor OK")

    agent = Agent(
        task="Open http://localhost:5174 and report the exact text of the first H1 or main heading on the page. After reporting, stop.",
        llm=llm,
    )
    print(f"[FE3-T1] Agent constructed")

    import asyncio
    start = time.time()
    try:
        history = asyncio.run(agent.run(max_steps=5))
    except Exception as e:
        print(f"FAIL: agent.run raised {type(e).__name__}: {e}", file=sys.stderr)
        return 3
    elapsed = time.time() - start

    print(f"\n[FE3-T1] elapsed={elapsed:.1f}s")
    try:
        result = history.final_result() if hasattr(history, "final_result") else str(history)
        print(f"[FE3-T1] result: {result!r}")
    except Exception:
        print(f"[FE3-T1] history (raw): {history}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
