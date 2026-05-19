# Runbook — Task-5: tdd-guard cross-PC deploy + live-verify (OD-050 close)

- Owner: Eduardo (operational; rug-pull + fresh-session + 2-PC = non
  delegabile a una sessione Claude in-corso)
- Gate: OD-050 §5 `RESOLVED-PENDING-LIVE-VERIFY` → `RESOLVED` SOLO se questo
  runbook passa verde su **ENTRAMBI** i PC. Anti-Pattern#9: validare LIVE,
  non assumere.
- Prereq merged: codemasterdd PR#180, vault PR#131 (canonical 3b) +#130.
- Ref: OD-050, spec/plan `codemasterdd/docs/superpowers/{specs,plans}/
  2026-05-19-tddguard-pathscoped*`.

## Cosa cambia (atteso)

canonical-3b: plugin `tdd-guard@tdd-guard=false` user-global → la sua
`hooks.json` (`npx tdd-guard@latest` su Write|Edit|MultiEdit|TodoWrite)
NON auto-fira più ovunque. Enforcement = SOLO repo ON-set che hanno il
hook nel proprio `.claude/settings.json` tracked (codemasterdd PR#180;
Game/Godot/Item-gen quando aggiunti — fuori scope Task-5, separate).

## Procedura — PER OGNI PC (Ryzen `Vgit` + Lenovo `edusc`/.10)

Da sessione **fresca, cwd-neutro** (NON dentro vault):

```
git -C C:\dev\vault pull --ff-only origin main      # Ryzen gia' fatto (sync 47->0); Lenovo DA FARE
<vault-ops>\scripts\deploy_claude_global.ps1        # DRY-RUN prima: leggi changes
<vault-ops>\scripts\deploy_claude_global.ps1 -Apply # poi APPLY
```
- DRY-RUN deve elencare: `enabledPlugins.tdd-guard@tdd-guard true->false`
  (o `null->false` se settings.json assente). Se NON lo elenca → STOP,
  canonical non pullato / path errato.
- `-Apply` scrive `~/.claude/settings.json`. **Riavvia/usa sessione nuova**
  (hook/settings caricano a session-start).

## LIVE-VERIFY MATRIX (sessione FRESCA post-Apply, per PC)

Trigger reale (Write/Edit), osserva block vs no-block:

| # | Repo / file | Azione | ATTESO |
|---|---|---|---|
| 1 | vault (qualsiasi `.md` o `Vault-ops-remote/scripts/*.py`) | Edit 1-riga | **NO block** (inerte) |
| 2 | synesthesia o altro non-ON-set, `.py` | Edit | **NO block** |
| 3 | codemasterdd `scripts/**` ops `.py` o `docs/*.md` | Edit | **NO block** (L2 path-scope PASS) |
| 4 | codemasterdd behavior-code allowlist (`apps/**/src`, `scripts/lib/**`) senza test | Write logica | **BLOCK** "write test first" |
| 5 | Game behavior-code senza test (se hook gia' aggiunto la' — altrimenti skip) | Edit | BLOCK / N-A |

PASS = righe 1-3 NO-block + riga-4 BLOCK su ENTRAMBI i PC.
- Se riga 1/2/3 BLOCCA → 3b NON effettivo (plugin ancora attivo / settings
  non scritto / sessione non-fresca). Diagnostica: `~/.claude/settings.json`
  `enabledPlugins.tdd-guard@tdd-guard` deve essere `false`.
- Se riga 4 NON blocca → o codemasterdd hook non deployato (PR#180 nel
  repo? `.claude/settings.json` ha PreToolUse npx tdd-guard?) o path fuori
  allowlist L2 (vedi `scripts/hooks/tddguard-instructions.template.md`).
- L2 seed: `.claude/tdd-guard/data/instructions.md` deve esistere
  (SessionStart seeder l'ha copiato da template). Se assente → seeder non
  girato (controlla SessionStart `tddguard-seed-instructions.ps1`).

## Idempotenza (Anti-Pattern#9 sub)

2a `-Apply` consecutivo = no-op (DRY-RUN "GIA = canonico"). Re-run
matrix invariata. Verifica.

## Esito

- VERDE entrambi PC → OD-050 §5 `RESOLVED-PENDING-LIVE-VERIFY` → `RESOLVED`
  + anti-rot canonical L46 "Live-verify ... pending" → "DONE 2026-XX".
  Commit doc su vault feature-branch → PR (Eduardo-merge sovereign).
- ROSSO → NON chiudere OD-050. systematic-debugging Phase-1 (no assume).
  Rollback: `git revert` del commit canonical-3b in vault → ripristina
  plugin=true (1-revert reversibile, harsh-review verificato).

## Cleanup correlato (handoff §39, post-playtest, opzionale)

`Unregister-ScheduledTask evo-deploy-quick,evo-godot-install`; kill
node/cloudflared/bash residui Ryzen; rm `.dq*`/`.sync*`/`.ci2*`/
`godot-install.ps1`/`.godot-install.log` Ryzen Desktop (artefatti temp).
