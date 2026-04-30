# dogfood-ui

Recovery status: scaffold/dormant.

The source code is present, but runtime state is absent in this transplanted
checkout.

Missing current runtime evidence:

- `apps/dogfood-ui/data/dogfood.sqlite`
- old migrated dogfood entries
- verified LiteLLM endpoint
- verified Langfuse endpoint
- verified Dafne endpoint

## Current rule

Treat this app as code scaffold until local runtime evidence is restored.

The Dafne panel depends on `http://localhost:5000`, which is not available
unless the external Dafne workspace is reactivated through `../../EXTERNAL_REPOS.md`.

## What remains useful

- Flask app structure.
- SQLite schema code in `db.py`.
- Stats helpers in `stats.py`.
- Templates and static assets as UI reference.

## What is not currently guaranteed

- Any old dogfood count.
- Any old cost aggregate.
- Any old promptfoo correlation.
- Any old Langfuse trace.
- Any old Dafne live status.

## Reactivation checklist

1. Decide whether `dogfood-ui` is still needed.
2. Restore or recreate `apps/dogfood-ui/data/dogfood.sqlite`.
3. Restore runtime logs or accept a fresh empty database.
4. Start the Flask app from this checkout.
5. Verify `/api/health`.
6. Keep Dafne integration disabled or explicitly reactivate Dafne first.
