# MODEL_ROUTING

Post-transplant routing policy.

## Status

Recovery mode.

The old routing matrix depended on original-machine facts: installed Ollama
models, Aider wrappers, API keys, dogfood logs, and runtime services. Those are
not verified in this checkout.

## Current routing rule

For this branch:

```text
structural docs -> current agent
external repo work -> dormant until reactivated
runtime claims -> verify locally first
model/client claims -> verify locally first
```

## Original principle to preserve

From the OpenCode/Ollama material and later Aider work:

```text
few tools
few models
clear roles
local first
cloud only when useful
document evidence
```

This principle remains active. Specific model choices are dormant until checked
on the correct PC.

## Client roles

| Client/tool | Recovery status | Intended role |
|-------------|-----------------|---------------|
| Codex | active in this checkout | Structural recovery and repo editing. |
| Claude Code | historical/compatible | Original orchestration client; verify on correct PC. |
| Aider | historical primary execution client | Re-enable only if wrappers/models exist. |
| OpenCode | architectural option | Portability bridge and possible secondary client; not active dependency. |
| Ollama | local runtime candidate | Verify installed models before using. |
| LiteLLM/Langfuse/promptfoo | scaffold/dormant | Observability/eval stack; restore only intentionally. |
| Cloud providers | dormant | Requires keys, budget policy, and privacy check. |

## Reactivation checks

Before using any client/model stack:

1. Verify binary exists.
2. Verify config path exists.
3. Verify model/API key exists.
4. Verify target repo is active.
5. Verify privacy scope.
6. Run a small smoke test.
7. Record the result in current docs.

## OpenCode position

OpenCode should be remembered as:

- an evaluated client;
- a bridge to Ollama;
- a client that can consume repo-native instruction files;
- a reason to keep `CLAUDE.md` clean and portable.

OpenCode should not be treated as:

- installed;
- preferred over Aider;
- required for recovery;
- proof that any model/runtime exists locally.

## Aider position

Aider was historically preferred on the original Lenovo because it fit:

- Windows-native workflow;
- Git-native diff review;
- ADR-0008 safety lessons;
- local/cloud wrapper routing.

In this checkout, Aider is dormant until wrappers and models are verified.

## Current active tasks

Use the current agent directly for:

- recovery docs;
- root governance;
- instruction-file cleanup;
- branch reconnection playbooks;
- static code review of files in this repo.

Do not delegate to external tools for this recovery pass unless explicitly
requested.

## Future routing reconstruction

On the correct PC, rebuild routing in this order:

1. Verify local hardware and Ollama.
2. Verify installed models.
3. Verify Aider wrappers.
4. Verify OpenCode if installed or desired.
5. Verify LiteLLM/Langfuse/promptfoo if needed.
6. Verify runtime evidence logs/DB.
7. Update this file with fresh facts.

Until then, this file is a recovery-safe policy, not a performance matrix.
