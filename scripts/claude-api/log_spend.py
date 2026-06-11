"""Append a Claude API spend entry to logs/claude-api-spend-YYYY-MM.md (ADR-0023).

Minimal per-call tracking for the post-Max tier-0 strategic path: date, task,
model, tokens, estimated cost, outcome. Creates the monthly file from template
on first use, recomputes the monthly cumulative, and prints budget-cap status
($10/$15/$20 soft thresholds per ADR-0023; overflow slice of ADR-0030 Hybrid A1).

Usage:
  py scripts/claude-api/log_spend.py --task "ADR draft X" --model claude-haiku-4-5 \
      --tokens-in 20 --tokens-out 10 [--cost-usd 0.0001] [--outcome OK]

Cost: pass --cost-usd explicitly, or omit it and let the script estimate from
the embedded pricing table (USD per MTok, cached 2026-06-11 from claude-api skill).
No secrets are read or written by this script.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# USD per 1M tokens (input, output) -- cached 2026-06-11
PRICING = {
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-opus-4-6": (5.00, 25.00),
    "claude-opus-4-7": (5.00, 25.00),
    "claude-opus-4-8": (5.00, 25.00),
}

TEMPLATE = """# Claude API spend log -- {month_label}

Tracking spend per-call tier-0 strategic (ADR-0023, overflow slice di ADR-0030 Hybrid A1).
File generato/aggiornato da `scripts/claude-api/log_spend.py`.

## Schema entry

| Data/ora | Task | Model | Token sent | Token recv | Cost USD | Outcome |
|----------|------|-------|------------|------------|----------|---------|

## Entry

| Data/ora | Task | Model | Token sent | Token recv | Cost USD | Outcome |
|----------|------|-------|------------|------------|----------|---------|

## Aggregati mensili

- **Cumulative cost mese**: $0.0000
- **Budget cap soft mensile**: $10-20 (ADR-0023)
- **Threshold**: $0-10 OK / $10-15 awareness / $15-20 alert / $20+ trigger reactivation Pro (ADR-0023 addendum)

## Riferimenti

- docs/adr/0023-strategic-tier-post-max-api-on-demand.md
- docs/adr/0030-post-max-orchestration-hybrid-a1.md (Hybrid A1: Pro primary, API on-demand = overflow)
- docs/runbook/post-max-cutover.md
"""


def estimate_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    rate_in, rate_out = PRICING[model]
    return (tokens_in * rate_in + tokens_out * rate_out) / 1_000_000


def parse_entries_total(text: str) -> float:
    total = 0.0
    entry_section = text.split("## Entry", 1)[1].split("## Aggregati", 1)[0]
    for match in re.finditer(r"\|\s*\$([0-9]+\.[0-9]+)\s*\|", entry_section):
        total += float(match.group(1))
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="short task description")
    parser.add_argument("--model", required=True, help="model id, e.g. claude-haiku-4-5")
    parser.add_argument("--tokens-in", type=int, required=True)
    parser.add_argument("--tokens-out", type=int, required=True)
    parser.add_argument("--cost-usd", type=float, default=None,
                        help="actual cost; omitted -> estimated from pricing table")
    parser.add_argument("--outcome", default="OK")
    parser.add_argument("--log-dir", default=None,
                        help="override log directory (default: <repo>/logs)")
    parser.add_argument("--date", default=None,
                        help="override timestamp, ISO format (default: now)")
    args = parser.parse_args()

    when = datetime.fromisoformat(args.date) if args.date else datetime.now()

    cost = args.cost_usd
    if cost is None:
        if args.model not in PRICING:
            print(
                f"ERROR: model '{args.model}' not in pricing table; pass --cost-usd explicitly.",
                file=sys.stderr,
            )
            return 2
        cost = estimate_cost(args.model, args.tokens_in, args.tokens_out)

    log_dir = Path(args.log_dir) if args.log_dir else Path(__file__).resolve().parents[2] / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"claude-api-spend-{when:%Y-%m}.md"

    if not log_file.is_file():
        log_file.write_text(TEMPLATE.format(month_label=f"{when:%Y-%m}"), encoding="utf-8")

    text = log_file.read_text(encoding="utf-8")

    task = args.task.replace("|", "/")
    row = (
        f"| {when:%Y-%m-%d %H:%M} | {task} | {args.model} "
        f"| {args.tokens_in} | {args.tokens_out} | ${cost:.4f} | {args.outcome} |\n"
    )

    entry_head, rest = text.split("## Entry", 1)
    entry_body, aggregates = rest.split("## Aggregati", 1)
    entry_body = entry_body.rstrip("\n") + "\n" + row + "\n"
    text = entry_head + "## Entry" + entry_body + "## Aggregati" + aggregates

    total = parse_entries_total(text)
    text = re.sub(
        r"\*\*Cumulative cost mese\*\*: \$[0-9.]+",
        f"**Cumulative cost mese**: ${total:.4f}",
        text,
    )

    if not text.isascii():
        print("ERROR: refusing to write non-ASCII log content (ADR-0021).", file=sys.stderr)
        return 3

    log_file.write_text(text, encoding="utf-8")

    print(f"Logged ${cost:.4f} ({args.model}, {args.tokens_in}in/{args.tokens_out}out) -> {log_file}")
    print(f"Month-to-date total: ${total:.4f} (soft cap $10-20, ADR-0023)")
    if total >= 20:
        print("THRESHOLD $20+: trigger reactivation Pro ratification (ADR-0023 addendum).")
    elif total >= 15:
        print("THRESHOLD $15-20: alert -- riconsidera frequenza task delegati.")
    elif total >= 10:
        print("THRESHOLD $10-15: awareness -- verifica trend.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
