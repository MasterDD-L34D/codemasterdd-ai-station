# Session continuity handoff — 2026-05-18/19

> **Scopo**: preservare lo stato di QUESTA sessione attraverso (a) chat
> close/compact, (b) la **reorg parallela Ryzen/vault** che Eduardo sta
> facendo (sposta file Lenovo+Ryzen + cambia doc — handoff dentro vault).
> Paste-ready per ripresa nuova sessione. **La reorg deve consultare
> questo doc** prima di spostare i path elencati in §Reorg-collision.

## Arco sessione
Jules autonomous (ADR-0034 Option D) → R3-bis → G2 Combat Freeze → pivot
DF/playtest → Godot-v2 deploy Ryzen → design-conformance audit. Tema
ricorrente corretto: **stale-first adoption + hollow-success su metriche-
proxy** (Eduardo l'ha flaggato ripetutamente → currency-gate encoded).

## DONE / merged (in git, reorg-safe se `git mv`)
- **codemasterdd**: PR #167 (adr-status-check runbook) · #168 (jules-cli-triage runbook) · #169 (ADR-0034 Accepted Option D) · #170 CLOSED-superseded · #171 (JULES-CAPABILITIES-MASTER, P0-3 fixed) · #172 (jules-daily-digest v4.1 + scheduler) · #173 (R3-bis no-message-on-moot) · #174 (ciclo-1 defer resolved). MERGED main.
- **Game**: #2326 (DF rescue) · #2330 (umbrella ADR DF-levels) · #2332 (playbook addendum hybrid) · #2333 (G2 Combat Freeze CLOSED, combat-only scope, gate-doc drift fixed) — MERGED. #2331 CLOSED anti-dup.
- **Jules ciclo-1**: 8/8 sessioni gestite (6 ARCHIVE + 2 DEFER→archive Eduardo-decision), AWAITING residue=0.
- **settings.json** `~/.claude/settings.json`: autoMode.allow ridotto a `["$defaults"]` (P0-3, standing Jules entries rimosse) — NON in repo, Lenovo-local.
- **Godot 4.6.2-stable** installato Ryzen (vedi §Ryzen-runtime).

## PENDING (owner)
| Item | Owner | Stato |
|---|---|---|
| `/ultrareview` su gap-report | Eduardo | **DEFERRED** — vive su PR-draft #284 Game-Godot-v2 |
| Integrare findings ultrareview (P0 fix) | Claude | post-ultrareview |
| Approvare remediation-spec | Eduardo | post-ultrareview |
| P0-3 TV web export | Claude | post-approval (Godot installato Ryzen, eseguibile E2E) |
| Remediation P0/P1/P2 Godot-v2 | Claude | post-approval (umbrella: no code prima) |
| Step-3 P5 playtest umano | Eduardo | dopo client conforme |
| Vault handoff cross-link a questo doc | Eduardo (vault sibling, merge suo) | testo fornito sotto |

## Ryzen runtime state (192.168.1.11 Vgit, REORG-FRAGILE)
- **Godot**: `C:\Users\VGit\AppData\Local\Godot\Godot_v4.6.2-stable_win64.exe` (172MB GUI) + `_console.exe` (wrapper). Export templates `%APPDATA%\Godot\export_templates\4.6.2.stable\` (8 web tpl).
- **Scheduled Tasks** (PERSISTENTI, da cleanup a fine): `evo-deploy-quick` (git-bash → `.dqlaunch.sh`), `evo-godot-install` (one-shot, done — rimovibile).
- `C:\Users\VGit\Desktop\Game-Godot-v2\.dqlaunch.sh` (launcher: prisma generate + GODOT_BIN + deploy-quick.sh, NO SKIP_REBUILD).
- `C:\Users\VGit\Desktop\Game` synced detached `0f8a572a`; deps installati `npm ci --ignore-scripts` + `prisma generate --schema=apps/backend/prisma/schema.prisma`.
- Tunnel Quick = **ephemeral** (URL cambia ogni restart task; non stabile). Named tunnel `evo-tactics-demo`/`eduscarpelli.dev` = NON provisionato (setup-once mai completato).
- **Cleanup a fine playtest**: `Unregister-ScheduledTask evo-deploy-quick,evo-godot-install`; kill node/cloudflared/bash residui; `.dqlaunch.sh`/`.dq*`/`.sync*`/`.ci2*`/`godot-install.ps1`/`.godot-install.log` su Ryzen Desktop = artefatti temporanei rimovibili.

## Reorg-collision — file QUESTA sessione (la reorg NON deve clobberare silenziosamente)
NUOVI (questa sessione):
- `codemasterdd/scripts/jules-daily-digest.ps1` (v4.1, scheduled 8am) — se reorg sposta scripts/, aggiornare Windows ScheduledTask `jules-daily-digest` path.
- `codemasterdd/scripts/godot-install-ryzen.ps1`
- `codemasterdd/docs/jules/JULES-CAPABILITIES-MASTER.md`
- `codemasterdd/docs/jules-batch/2026-05-18-*.md` (digest + batch-01-CORRECTED)
- `codemasterdd/docs/runbook/jules-session-triage-via-cli.md`, `adr-status-check.md`
- `codemasterdd/docs/adr/0034-*.md` (+ R3-bis addendum)
- `codemasterdd/docs/sessions/2026-05-19-continuity-handoff.md` (questo)
- `Game-Godot-v2/docs/godot-v2/design-conformance-gap-2026-05-19.md` (PR #284 DRAFT — **non orfanare; rilocare con intento se reorg tocca docs/godot-v2/**)
- `Game-Godot-v2/docs/combat/combat-canon.md` (migration banner aggiunto #2333)
- `Game/docs/planning/EVO_FINAL_DESIGN_MILESTONES_AND_GATES.md` (G2 CLOSED)
- AA01 (NON git, Lenovo `~/aa01/learnings/`): L-2026-05-031, -034, -035
- Memory (NON git, Lenovo `~/.claude/.../memory/`): `feedback_currency_gate.md`, `reference_jules_workflow.md` + MEMORY.md index

PATH-DEPENDENT (citati cross-doc — se rinomini, aggiorna riferimenti):
- gap-report cita: `Game-Godot-v2/docs/godot-v2/visual-screen-bible.md` + `visual-design-research.md`; `Game/docs/planning/2026-04-26-coop-mvp-spec.md`; `Game/docs/adr/ADR-2026-04-20-m11-jackbox-phase-a.md`; `Game/docs/PLAYER-VISION.md`; `codemasterdd/docs/EVO_TACTICS_DESIGN_DIGEST.md` §12.
- ScheduledTask `jules-daily-digest` → `C:\dev\codemasterdd-ai-station\scripts\jules-daily-digest.ps1` (hard path, rompe se repo spostato).

## Lessons encoded (durevoli, fuori repo → reorg-safe)
- **Currency-gate** (memory `feedback_currency_gate.md` + L-035): pre-action git-recency + front-matter status/superseded + sibling-newer + cited-path-exists + verdetto 1-riga. Root: "tiri fuori soluzioni vecchie".
- **R3-bis** (L-031 + ADR-0034 addendum): moot/shipped → archive-only, MAI sendMessage (risveglia sessione = backfire).
- **L-034**: segnale-indipendente > euristica self-designed; validazione circolare = nessuna.
- Hollow-success anti-pattern: NON dichiarare "valido" su HTTP-200/file-serve; serve validazione funzionale/visiva (ground-truth Playwright per UI).

## Next gates (ordine)
1. Eduardo `/ultrareview` su PR #284 (quando può) → falsificazione esterna gap-report.
2. Claude integra P0 findings → spec riconciliata.
3. Eduardo approva remediation → SOLO ALLORA code.
4. Claude P0-3 (TV export) E2E + verifica visiva Playwright.
5. Remediation P1/P2; poi Step-3 P5 playtest umano.

## Cross-link per vault handoff (Eduardo incolla vault-side)
```
[ai-station-cross-ref 2026-05-19] La sessione Claude 2026-05-18/19 ha
artefatti vivi: codemasterdd PR #167-174 merged, Game #2330/2332/2333
merged, Game-Godot-v2 PR #284 DRAFT (design-conformance gap, pending
/ultrareview — NON mergere, NON orfanare). Stato runtime Ryzen +
reorg-collision file list: codemasterdd/docs/sessions/2026-05-19-
continuity-handoff.md. La reorg DEVE consultare quel doc §Reorg-collision
prima di spostare gli script/doc elencati (ScheduledTask path-dependent).
```
