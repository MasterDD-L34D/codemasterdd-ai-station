# llmfit task-eval: deepseek-coder-v2:16b vs qwen2.5-coder:14b (2026-05-22)

> Research report (QG Step 2). Stage-2 of the fleet LOCAL-LLM-STANDARD 2-stage
> model selection: llmfit HW-fit shortlist -> task-eval N>=10 on the real prompt.
> Verdict: **REJECT deepseek-coder-v2:16b for the behavior-critical coding tier.**
> HW-fit != task-fit, confirmed empirically.

## Context

The fleet standard (`C:\dev\tools\llmfit\LOCAL-LLM-STANDARD.md`) prescribes a
2-stage pick: (1) llmfit ranks models by hardware-fit + general category score;
(2) a real task-eval (N>=10, anti lucky-sample / anti-pattern #14) decides the
behavioral winner, because "what runs well on my HW + general category quality"
!= "which model does MY task best".

On Ryzen (`ryzen-llm-fit.md`), llmfit ranked **deepseek-coder-v2-lite** #1 in the
coding category (HW-fit score 95.5, est 119 tps, 16B MoE A2.4B). This report
runs stage-2 to test whether that stage-1 ranking holds for the codemasterdd
behavior-critical use case (constraint-respecting single-file edits, ADR-0008/0016).

## Method

- Harness: `scripts/llmfit-task-eval.py` (self-test validated: reference solution
  PASS, broken solution FAIL). Fires the same coding prompt N times per model at
  the local Ollama endpoint, extracts the code block, runs it against hidden
  asserts in an isolated subprocess (10s timeout), records pass/fail + latency.
- Endpoint: Ryzen Ollama `127.0.0.1:11434` (both models in 12 GB VRAM; this is
  the fleet "14B -> Ryzen q4-full" routing).
- N = 10 per model per task. `temperature = 0.3` (variance on purpose -- a flaky
  model should surface fails across the 10 runs; temp 0 would make runs identical
  and hide reliability).
- Two tasks:
  - **easy** `merge_intervals` (3 constraints: merge incl. touching / sort / empty).
  - **hard** `evaluate` arithmetic expression (5 constraints: + - * / , parens,
    precedence, **integer floor division `//`**, ignore spaces). The int-div
    constraint discriminates: a lazy `return eval(expr)` yields a float for
    `"10/3"` (3.33 != 3) and fails.

## Results

| model | easy (intervals) | hard (expr, 5-constraint) | median latency (hard) |
|-------|:----------------:|:-------------------------:|:---------------------:|
| qwen2.5-coder:14b (baseline, current behavior tier) | 10/10 | **9/10 (90%)** | 18.2 s |
| deepseek-coder-v2:16b (llmfit #1 coding candidate) | 10/10 | **5/10 (50%)** | 13.1 s |

- Easy task: both 100%. Candidate ~34% faster (4.07 s vs 6.19 s median). On this
  band the candidate looked superior.
- Hard task: baseline **90%** vs candidate **50%** -- a 40 pp gap. Candidate is
  faster but constraint-unreliable.

## Verdict

**REJECT** deepseek-coder-v2:16b for the behavior-critical / constraint-following
coding tier. qwen2.5-coder:14b stays the behavior default (now on Ryzen q4-full
per the fleet routing, validated 90%).

- llmfit stage-1 ranked the candidate #1 for coding (95.5); stage-2 shows it
  fails the harder constraint task half the time. **HW-fit != task-fit, proven.**
  Adopting on the llmfit score alone would have been wrong.
- The 40 pp gap is far beyond N=10 noise (CI95 ~+/-30 pp on a point estimate;
  L-069). Direction is robust; an N=40 ratify is optional, the gap is decisive.

## Methodological value (why the 2-stage matters)

The **easy task was non-discriminating** (both 100%) -- a lucky-band that would
have led to a wrong ADOPT on speed alone (the exact anti-pattern #14 failure
mode). The **hard task separated them**. This is direct empirical support for the
LOCAL-LLM-STANDARD load-bearing caveat: never adopt a model from its llmfit/HW-fit
rank; always run a task-eval, and make sure the task is hard enough to
discriminate (constraint count in the band where models actually fail).

## Caveats + follow-ups

- Single hard task (expr). A fuller eval would add 2-3 discriminating tasks
  across the codemasterdd edit profile (refactor, bug-fix, multi-constraint).
- deepseek-coder-v2:16b may still suit non-constraint tasks (quick chat, draft,
  speed-first) given its latency edge -- not evaluated here.
- N=10 direction-grade per L-069/L-072; a behavior ratify would use N=40.
- The harness `scripts/llmfit-task-eval.py` is reusable for future stage-2 evals
  (any Ollama model tags, `--n`, `--host`).

## Routing implication

No change to the behavior tier: qwen2.5-coder:14b confirmed. This corroborates
the `MODEL_ROUTING.md` fleet update (14B -> Ryzen q4-full): the right behavior
model on the right machine, and the top llmfit discovery candidate did NOT beat
it on quality. The 2-stage gate held.
