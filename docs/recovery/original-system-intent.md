# Original system intent

## Purpose

This document reconstructs how the repository was originally supposed to work
before the transplant.

It is not a live operating plan for this checkout. It is a map for the correct
PC to reconnect the structural recovery branch to the original system.

## Core idea

The original project was not just a documentation repo and not just an OpenCode
experiment.

It was meant to become a sovereign AI development station:

- local-first;
- cloud-second;
- low fixed cost;
- privacy-aware;
- model-routed;
- documented through ADR;
- portable across agent clients through repo-native instruction files.

The healthy shape was:

```text
human intent
  -> repo governance
  -> model/tool routing
  -> local or cloud execution
  -> evidence/logging
  -> ADR/backlog/compact update
```

## Original layers

### Layer 1 - Workstation substrate

The Lenovo workstation was the physical substrate:

- Windows 11;
- Git/GitHub CLI;
- Node/Python;
- NVIDIA/CUDA;
- Ollama;
- local models;
- Aider wrappers;
- optional cloud API keys;
- global git hooks.

This layer is machine-specific and must be verified on any new machine.

### Layer 2 - Repo governance

This repo was the memory and policy layer:

- `CLAUDE.md` for operating rules;
- root governance files for brief, roadmap, backlog, context, routing;
- ADR for decisions;
- `JOURNAL.md` for chronological session history;
- `docs/patterns/` for repeatable workflows;
- `docs/research/` for tool/model research;
- `logs/` for runtime dogfood evidence.

This layer is the part that should remain portable.

### Layer 3 - Client/runtime layer

The original system considered multiple clients:

- Claude Code as frontier orchestration during Claude Max;
- Aider as Git-native execution client;
- OpenCode as evaluated alternative/portability candidate;
- Ollama as local model runtime;
- LiteLLM/Langfuse/promptfoo as observability/evaluation stack;
- direct cloud providers as fallback.

The important design was client interchangeability, not loyalty to one client.

### Layer 4 - Model routing

The routing principle from the OpenCode/Ollama material was:

```text
few models
clear roles
local first
cloud when needed
document the routing
```

The later Aider work refined this into:

- cosmetic tasks -> small fast local model;
- behavior-critical single-file work -> stronger local model with diff review;
- difficult or time-sensitive work -> cloud/free-tier or frontier model;
- strict multi-constraint work -> manual/frontier path, not blind delegation.

### Layer 5 - Evidence loop

The system was supposed to learn from use:

- dogfood logs;
- cost snapshots;
- quality bench outputs;
- commit hooks;
- rejected delegations;
- ADR updates;
- sprint reviews.

After transplant, this layer is the most damaged because much of it was
gitignored runtime state.

## OpenCode's intended role

OpenCode appears in the archive as a workflow candidate built around:

1. install OpenCode;
2. connect to Ollama;
3. choose a small set of local models;
4. add API/cloud fallback only when useful;
5. avoid model sprawl.

The extracted principle is stronger than the specific model names from the
screens.

Original OpenCode value:

- a possible local/cloud coding client;
- a way to connect agent workflow to Ollama;
- a portability bridge because OpenCode could read repo-native instruction
  files such as `CLAUDE.md` or `AGENTS.md`;
- a conceptual confirmation of local-first/cloud-second routing.

OpenCode was not the final chosen operational client in the later docs. Aider
won for the original Lenovo context because:

- it was Windows-native;
- it matched the diff-first review loop;
- it fit ADR-0008 safety lessons;
- it had working wrappers and dogfood evidence.

Therefore OpenCode should be preserved as:

- an architectural option;
- a portability bridge;
- a re-evaluation candidate;
- not an active dependency.

## What "the system" was supposed to be

The original system was a small sovereign AI operating system for Eduardo's dev
work:

```text
Instruction surface:
  CLAUDE.md / AGENTS.md / governance root docs

Decision memory:
  ADR + DECISIONS_LOG + JOURNAL

Task intake:
  user request -> classify task -> choose client/model

Execution:
  direct agent / Aider / local Ollama / cloud fallback

Safety:
  git hooks + diff review + no silent corruption + privacy gates

Observability:
  dogfood logs + promptfoo + Langfuse/LiteLLM + cost monitor

Closure:
  commit + journal + compact context + backlog update
```

The mistake that grew later was that this system started governing external
projects from inside the policy repo. That made sense on the original PC while
all paths existed, but it became fragile after transplant.

## What must be preserved

Preserve:

- local-first/cloud-second principle;
- few-model routing;
- ADR-backed decisions;
- diff/safety review loop;
- runtime evidence as explicit artifacts;
- client portability through clean instruction files;
- external repo registry with activation gates.

Do not preserve as active without verification:

- old path assumptions;
- old runtime status;
- old dogfood counts without logs/DB;
- old service health;
- old cross-repo next actions;
- old model ranking from screenshots as universal truth.

## Reconnection hypothesis

When this branch is opened on the correct PC, the right workflow is:

1. keep the structural reset;
2. verify the original machine layer;
3. restore or regenerate runtime evidence;
4. decide whether Aider remains primary;
5. evaluate whether OpenCode is useful as a secondary client;
6. reactivate external repos one by one, not as a bundle.

## Open questions for the correct PC

- Is OpenCode installed or still only an archived plan?
- Is Aider still the primary execution client?
- Are the global git hooks still installed?
- Do the dogfood logs and SQLite DB exist on the original machine?
- Should `AGENTS.md` become the primary portable instruction file for Codex,
  with `CLAUDE.md` retained for Claude/OpenCode compatibility?
- Should LiteLLM/Langfuse remain active, or become optional scaffold?
