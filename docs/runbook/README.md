# runbook/

Playbook operativi: setup, deploy, recovery, troubleshooting. Include la matrice
di routing key/task (ex `operations/`, flattened 2026-06-04).

## File principali

- `ssh-inbound-fleet-setup.md` -- SoT setup SSH inbound fleet (Ryzen <-> Lenovo)
- `post-max-cutover.md` -- cutover Claude Max -> Hybrid A1 (~17/06), tier-0 overflow + spend log + rollback
- `key-and-task-routing-matrix.md` -- inventario chiavi + 3-tier tool ecosystem + dispatch matrix (ex `operations/`)
- `godot-v2-first-playable-golive.md` -- go-live First Playable Godot
- `playtest2-board-sync.md` -- sync execution board
- `jules-session-triage-via-cli.md`, `jules-suggestions-snapshot.md` -- triage Jules
- `skiv-monitor-blocked-pr-fix.md`, `mirror-external-drive.md`, `adr-0017-hot-restart.md`, `adr-status-check.md`, `tddguard-task5-cross-pc-verify.md`
