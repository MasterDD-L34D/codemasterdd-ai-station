# Client runtime matrix

## Purpose

Clarify which clients and runtimes are active, dormant, or candidates after
structural recovery.

## Matrix

| Client/runtime | Current status | Original role | Reactivation check |
|----------------|----------------|---------------|--------------------|
| Codex | active here | Recovery/editor in transplanted checkout | Already active in this session. |
| Claude Code | historical compatible | Original orchestration client during subscription period | Verify installed/authenticated on correct PC. |
| Aider | dormant historical primary | Git-native diff execution client | Verify binary, wrappers, local models, and hooks. |
| OpenCode | candidate/bridge | Evaluated client, Ollama bridge, instruction-file portability | Verify install/config; test reading repo instructions. |
| Ollama | dormant local runtime | Local model server | Verify service, installed models, GPU config. |
| LiteLLM | scaffold/dormant | Unified model proxy and virtual key budget layer | Verify Docker/config/env and endpoint. |
| Langfuse | scaffold/dormant | Observability/tracing | Verify Docker/config/env and endpoint. |
| promptfoo | scaffold/dormant | Evaluation runner | Verify install and result path. |
| dogfood-ui | scaffold/dormant | Local dashboard for dogfood evidence | Verify DB/runtime and decide Dafne panel status. |
| Dafne API | dormant external | Swarm status/proposal integration | Reactivate Dafne workspace first. |

## Current default

Use Codex directly for recovery work.

Do not use Aider, OpenCode, Ollama, or cloud wrappers from this checkout unless
the user explicitly asks and local availability is verified.

## OpenCode note

OpenCode matters because it supports the original architecture goal:

```text
repo-native instruction files
  -> portable agent client
  -> local/cloud model routing
```

That does not mean OpenCode is installed or preferred here. It means the
instruction surface should stay clean enough that OpenCode could consume it on
the correct PC.
