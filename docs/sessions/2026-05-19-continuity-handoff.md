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

## PENDING GOVERNANCE — Cross-machine parity audit (2026-05-19, Eduardo-confirmed)

Owner override: AA01 + runtime NON sono "correttamente fuori-parity"
(mio conflation error, ritirato). 2 conflation: (a) AA01 scope-separato
≠ non-versionato; (b) runtime transiente ≠ recipe-provisioning. Audit
ground-truth Lenovo↔Ryzen (read-only SSH) → gap:

**🔴 CRITICO**: Ryzen **global git-hooks ASSENTI** (`git config --global
core.hooksPath` UNSET + repo-local commit-msg assente). Ogni commit da
Ryzen (Eduardo/Codex/Aider/Jules/Claude) **bypassa ADR-0011 (Conventional
+trailer cross-agent) + ADR-0008/0020 (silent-corruption/silent-fail
pre-commit)**. Governance hole attivo finché Eduardo lavora da Ryzen.

| Gap | Ryzen | Sev | Fix |
|---|---|---|---|
| global git-hooks commit-msg/pre-commit | ASSENTE | 🔴 | set core.hooksPath + deploy hook scripts repo-canonical |
| `~/.local/bin` wrappers | ASSENTE | 🟠 | `scripts/setup/install-wrappers.ps1` su Ryzen |
| `~/.aider.conf.yml` | ASSENTE | 🟠 | deploy conf |
| AA01 + lessons (`~/aa01`,`/c/dev/AA01`) | ASSENTE | 🟠 | AA01 → repo git PRIVATO proprio (scope-separato MA versionato), clone Ryzen; learnings viaggiano con esso |
| `.claude/settings.json` + global CLAUDE.md | esiste, content-parity NON verificata | 🟠 | `deploy_claude_global.ps1` parity (anti-pattern #9) |
| Ollama Ryzen | ROTTO (init fail/timeout) | 🟠 | fix runtime separato (tier-1/2 local morto Ryzen) |
| Runtime recipe (Godot pin/.dqlaunch/ScheduledTask/deploy-quick) | ad-hoc Ryzen, non-repo | 🟠 | infra-as-code `codemasterdd/scripts/ryzen/` + `bootstrap-ryzen.ps1` idempotente; transiente-live resta local rigenerabile |

**Reverse-gap (Ryzen-only → Lenovo manca)**: Vault-ops Python tooling;
repo `claude-supermemory-local`,`_workspace`. Lenovo-only: AA01,
Game-aa01-cap14b/15b,Gpt. → repo-set reconcile.

**Correttamente NON-parity**: keys.env *value* (procedura=code, valore=
manuale-secure per-machine); runtime live-state (PID/URL ephemeral,
rigenerabile da recipe); junk Lenovo `/c/dev/null`,`null'` (=cleanup).
**Già OK Ryzen**: `.config/api-keys`✓ `aider-privacy-whitelist.txt`✓
`.claude/commit-guard.js`✓ `skills/continuous-learning-v2`✓.

**Governance change richiesto**: la regola "AA01 NON-git" (global
CLAUDE.md + memory `project_aa01_studio`) = decisione documentata →
override owner-mandato 2026-05-19, va in DECISIONS_LOG/ADR.

### Next-session task (Eduardo-confirmed scope)
1. ADR "cross-machine parity model" (AA01→git-privato · runtime→infra-as-code · git-hooks-parity CRITICO · wrappers/aider.conf/settings parity · ollama-fix · vault-ops reverse · repo-set reconcile · junk cleanup) + DECISIONS_LOG entry override AA01-non-git.
2. `bootstrap-ryzen.ps1` idempotente (anti-pattern #9: test -Apply sandbox PRIMA del live, verify artefatto non solo log).
3. Priority order: 🔴 git-hooks Ryzen FIRST (governance hole attivo).

## 🔴🔴 #0 BLOCKER (2026-05-19) — Ryzen git-auth GitHub ROTTO

Ground-truth: Ryzen `git fetch/pull/push origin` FALLISCE →
`fatal: Unable to persist credentials with the 'wincredman' credential
store` + `bash: /dev/tty: No such device` + `exit 1`. Git Credential
Manager Ryzen non autentica (non-interactive + store rotto). Conseguenza:
- Ryzen `origin/main` CONGELATO a `212be6c` (ultimo fetch ok, pre-#177).
- Ryzen ha doc continuity VECCHIO (#175, senza §parity-scope) → "non lo
  trovo aggiornato" spiegato.
- Ryzen NON pusha → reorg/commit fatti da Ryzen NON arrivano a GitHub
  via questo path (rischio lavoro Ryzen isolato/perso).
- Precede ogni altro gap parity: senza git-auth Ryzen non sincronizza
  nulla. **Priority #0, prima di git-hooks**.

Stato 3-way 2026-05-19: GitHub origin/main `058bfa8` (canonical, doc
parity-scope ✓) · Lenovo `058bfa8` ALIGNED ✓ · Ryzen `212be6c` STUCK.

### Fix (Eduardo, Ryzen interattivo — auth=owner-action, NON Claude)
Opzione consigliata (gh ecosystem):
```
gh auth login           # su Ryzen, interattivo, scegli GitHub.com + HTTPS
gh auth setup-git       # gh diventa credential helper, bypassa wincredman rotto
cd C:\dev\codemasterdd-ai-station && git pull --ff-only origin main
```
Alternative: `git config --global credential.helper store` + 1 auth
interattiva · oppure remote→SSH (`git remote set-url origin
git@github.com:MasterDD-L34D/codemasterdd-ai-station.git` + chiave SSH
Ryzen→GitHub registrata). Verifica reorg-commit Ryzen non-pushati PRIMA
(git log origin/main..HEAD su ogni repo Ryzen) per non perderli.

---

## EVENING UPDATE 2026-05-19 — OD-050 CHAIN CLOSED end-to-end

Sessione Ryzen 2026-05-19 evening: catena OD-050 chiusa+live-verified
entrambi PC. Aggiornamento PENDING table sopra (lines 22-31):

### Done in questa serata
- **OD-049 §4.5** (21-script Vault-ops consolidation) MERGED (vault main).
- **tdd-guard C-raffinato shipped 2-PC**:
  - codemasterdd `#180` MERGED (L1/L2: per-repo `.claude/settings.json`
    hook + path-role template `scripts/hooks/tddguard-instructions.template.md`
    + idempotent seeder `tddguard-seed-instructions.ps1`)
  - vault `#131` MERGED (L3 canonical 3b: plugin tdd-guard@tdd-guard=false
    user-global + W-2 observe.sh `pre`/`post` arg + L43/L44/L46 coherence
    + deploy.ps1 documenting comment, NO logic-change canonical-driven)
  - vault `#130` MERGED (OD-050 doc, status RESOLVED-PENDING-LIVE-VERIFY)
  - codemasterdd `#181` MERGED (runbook tddguard-task5-cross-pc-verify)
  - codemasterdd `#182`+`#183` MERGED (helper `task5-deploy-verify.ps1`
    — flagged known-fragile, see lesson sotto)
- **Task-5 cross-PC** DONE 2026-05-19 22:48-22:51:
  - Ryzen `-Apply` -> tdd-guard@tdd-guard True->False (direct file-read
    verified, mtime match)
  - Lenovo (via SSH) re-deploy POST `git pull` 7fb5ded82 -> True->False
    (findstr-verified). Sequence-bug fixed (1st run: `|tail` cmd-incompat
    silently failed git-pull -> deploy ran on STALE canonical).
  - **STATIC PARITY 2-PC**: tdd-guard=false both Ryzen+Lenovo.
  - **LIVE TRIGGER Ryzen** (22:51, fresh Claude Code Desktop on
    `C:\dev\vault`, edit `hot.md`): PASS no-block ("OD050 LIVE PASS,
    nessun blocco"). Falsifies original bug empirically. Probe reverted.
  - Lenovo live = trust-by-parity (script-identical + static-false +
    canonical precedent `hook_userprofile_fix`).
- **OD-050 STATUS** `RESOLVED-PENDING-LIVE-VERIFY` -> `RESOLVED` (vault
  PR `#132` PENDING-MERGE Eduardo-sovereign; canonical L46 anti-rot
  pending->DONE evidence; OD-050 §5 fully rewritten end-to-end).
- **vault-sync** 47-behind -> 0 (4 tracked-dirty other-session preserved
  via mirato stash-restore: pathfinder-tune.json blob + 3 gitlink-ptr
  cosmetic, zero-loss).
- **Cross-repo audit** prunato ~281 branch stale merged-verified
  (Game/Godot/vault, Game-DB clean).
- **#284 verification addendum** appended (Protocol-1 ground-truth:
  4/5 claims verified, claim-2 "zero-theme" corrected to "non-bible-token
  conformant", +1 NEW bug-finding main_scene-committed-PhoneComposerBoot
  bug build_web.sh main-mode would export wrong scene). #284 stays
  DRAFT (gate-1 ultrareview Eduardo, post-approval umbrella).

### PENDING ORA (post-this-session)
| Item | Owner | Stato |
|---|---|---|
| Merge vault `#132` (OD-050 RESOLVED close) | Eduardo (sovereign) | vault main = canonical RESOLVED post-merge |
| `/ultrareview` PR `#284` (gate-1 Godot remediation chain) | Eduardo | catena separata, no-rush, post-approval umbrella |
| Cleanup Ryzen scheduled-task (handoff §39 above: `Unregister evo-deploy-quick/evo-godot-install` + kill node/cloudflared/bash + rm `.dq*/.sync*/.ci2*` Desktop) | Eduardo | optional post-playtest |
| Helper `task5-deploy-verify.ps1` deprecate/fix | Claude (follow-up, low-pri) | known-fragile flagged; runbook #181 = via affidabile |
| `~/aa01-vs-C:/dev/AA01` aa01 dup resolution (handoff §PENDING line) | Eduardo | OD-047 follow-up |

### Lessons encoded (oltre quelle handoff §60-64)
- **Over-engineering automation** quando il manuale-robusto basta = anti-pattern. Helper task5 #182/#183 fragile (4 fail-iter: em-dash mojibake + nested-quoting probe + SSH-cmd-incompat `|tail` + deploy-unicode-misread). Robust path = direct findstr/file-read + runbook. Lesson: automate solo se non-fragile; "1-command" che richiede 4 fix > "5-step manuali robusti".
- **Sequence-dependency cross-PC**: `git pull` PRIMA di `deploy -Apply`, altrimenti deploy gira su canonical-stale. `|tail` cmd-incompat ha mascherato il fail (esempio currency-gate handoff §61).
- **AI-conflict resolution via ground-truth**: 2 sessioni Claude in disaccordo (Lenovo "63 dirty = reorg loss-risk" vs Ryzen "engine .uid churn") -> ground-truth diretto sul PC dove i file SONO = autoritativo (L-034 segnale-indipendente).
- **Encoding-policy violation self-caught**: em-dash in .ps1 -> PS5.1 mojibake parse-break. CLAUDE.md ASCII-first encoding-policy esiste per QUESTO (cross-tool Windows). Ho violato la mia stessa policy, corretto.

### Cross-link aggiornato per vault handoff
```
[ai-station-cross-ref 2026-05-19 evening] OD-050 catena CHIUSA
end-to-end: tdd-guard plugin=false 2-PC + live-verified Ryzen
(no-block .md edit, falsifica bug originale). vault PR #132 = close
pending-Eduardo-merge sovereign. Per ripresa qualsiasi sessione futura:
git -C C:\dev\codemasterdd-ai-station pull + leggi
docs/sessions/2026-05-19-continuity-handoff.md (questo, §EVENING UPDATE).
Godot #284 DRAFT separato gate-1-ultrareview-Eduardo quando vuoi.
```
