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

### Parallel-session log 2026-05-20
- `[parallel-A6 OWNING Game Vue3 branch claude/parallel-game-a6-frontend-2026-05-20 start 2026-05-20T01:33Z]` (Lenovo, scope: A6 starter_bioma frontend label gap ~30 LOC; backend chain ✅ già shipped; no-touch Godot v2 / vault / codemasterdd governance)
- `[parallel-A6 DONE PR https://github.com/MasterDD-L34D/Game/pull/2334 finish 2026-05-20T01:40Z]` (4 file edit +129/-21, 36/36 test verde, Prettier verde, live probe backend OK; A6 BACKLOG row 🟡 PARTIAL → ✅ DONE pending master-dd merge)
- `[parallel-COOP-TESTS DONE PR https://github.com/MasterDD-L34D/Game/pull/2335 finish 2026-05-20T01:55Z]` (branch claude/parallel-coop-test-coverage-2026-05-20, test-only +49 LOC, 5 nuovi test phase-skip + startRun negative, 46/46 verde; BACKLOG "Test coverage gaps coop" 2/3 entry chiuse + 1 stale closed)
- `[parallel-CASCADE-3-AGENT DONE PR Game #2336 (auto-bundled coop disconnect race + computeRoleGap tests + W8O-2 fix) MERGED + Game #2337 (P1 orch.hostId stale gate fix + 5 tests) + Game #2338 (listBiomeRoleDemands + GET /api/coop/role-demands + 7 tests) finish 2026-05-20T02:06Z]` (multi-agent dispatch via superpowers:dispatching-parallel-agents: coop-phase-validator + repo-archaeologist + Explore → synthesis 3 PR cascade; #2337 + #2338 open ready master-dd review; museum card coop-ws-test-infra-patterns shipped score 5/5)

---

## LESSONS-ENCODED 2026-05-19/20 — durable rules from multi-arc session

> Pattern: rule + concrete-evidence + mitigation. Promotable a aa01
> `learnings/L-2026-05-NNN-<slug>.md` Lenovo quando convenient.
> Anti-Pattern-Catalogue candidates per global CLAUDE.md (Eduardo gate).

### L-DRAFT-A: Jules-class silent-drop di fix sostantivi (regression-class)

**Pattern.** Bot-orchestrator-PRs (Jules, similar) che dichiarano scope ristretto
("ack task complete", "no changes necessary", "align docs registry") possono
**rewrite-completi** del file toccato anche se l'effective-diff è minimo,
**droppando linee sostantive landed in PR precedenti** se non protette da test
in CI-watchlist. Evidence 2026-05-19/20: PR #2321 (W8O-2 race-fix, mio,
TDD-validated) + suo regression test droppati da Jules PR #2327 "rewrite ability
panel condition" landed 8h dopo. Race-bug "barra si e buggata" rientrato silent.
Diagnosi solo post-empirical sospetto + ground-truth-check (system-reminder
inadeguato a flaggare regressioni-pattern).

**Mitigation.** (i) Test-regression aggiunto co-fix in PR substantive (gia
pratica TDD); (ii) CI-watchlist file-x-test-essenziali: regression-test must
pass su CI obbligatorio = bot-rewrite che lo droppa = CI red; (iii) post-merge
auto-check pattern: dopo Jules-class merge che tocca file con regression-test
recente, smoke-test re-run automatico (cron periodic monitor catches now).

**Anti-Pattern# candidate**: "Bot-rewrite-drop su fix-recenti non-CI-guarded".

### L-DRAFT-B: Helper-over-engineering — automate-only-if-non-fragile

**Pattern.** Quando il manuale-robusto (file-read + findstr + runbook) e
deterministico, costruire un helper-script che introduce nested-quoting
(probe inline) + SSH-cross-shell-cmd + cross-tool-unicode = MORE failure-surface
than the task it automates. Evidence: `task5-deploy-verify.ps1` PR#182/#183
quattro iterazioni-fail (em-dash mojibake, nested $probe quoting PS5.1,
SSH-cmd-incompat `|tail`, deploy-unicode-misread). Deprecato PR#185, runbook
#181 + check-diretti = path affidabile.

**Mitigation.** Quando proponi "automatizziamo": prima quantifica fragilita
(quoting-layers nested-count, cross-shell hops, unicode-touch). Se >2 cose
fragili: NO automatizzare, scrivi runbook + check-diretti SEMPLICI. Rule:
"automate solo se non-fragile; 1-comando-che-richiede-4-fix > 5-step-manuali-robusti".

**Anti-Pattern# candidate**: "Helper-tool che introduce piu failure-surface
del task originale".

### L-DRAFT-C: Encoding-policy self-violation (em-dash + PS5.1)

**Pattern.** CLAUDE.md gia esige ASCII-first body prose (anti-pattern cross-tool
Windows shell). Auto-violato in PR#182: em-dash `—` in Say-strings di .ps1 ->
Bash-cat-heredoc UTF-8 write -> PS5.1 ANSI-read -> mojibake `â€"` ->
ParserError -> task-blocked. Fix-#183 ASCII-only.

**Mitigation.** Pre-commit hook (gia idea ADR-0021 encoding policy): grep
non-ASCII su nuovi .ps1/.sh/.bat/.cmd files in tracked-staged paths.
Block-commit se non-ASCII rilevato senza esplicita override-marker
(`# encoding-non-ascii-ok: <reason>`).

**Anti-Pattern# candidate**: "Encoding-policy compliance richiede enforcement
non-solo-doc".

### L-DRAFT-D: Sequence-dependency cross-PC + cmd-incompat silent-fail

**Pattern.** Task-5 1st-Lenovo-run: `git pull | tail -2` su SSH-cmd (Windows
default shell). `tail` non esiste in cmd -> intera chain `&&`-collapsed
silent-fail nella parte git-pull -> deploy gira su canonical-STALE -> result
sbagliato. Silent perche `tail` errored MA `&&` short-circuit non chiamato
(la pipe `|` parsing diverge cross-shell).

**Mitigation.** SSH-cross-shell scripts: (i) NO unix-tool pipes su Windows-cmd
SSH (`tail`/`head`/`grep` etc); (ii) usare powershell-native equivalenti
(`Select-Object -Last`/`-First`); (iii) sequenza-dependent operations =
verifica-step-completion esplicita (exit-code check), no implicit-pipe-chain;
(iv) DRY-RUN su SSH-target separato prima di -Apply per validare
shell-portability.

**Anti-Pattern# candidate**: "SSH-cmd-cross-shell tool incompat silent-collapse".

### L-DRAFT-E: AI-conflict resolution via ground-truth (L-034 reinforcement)

**Pattern.** 2+ sessioni AI in disaccordo su stesso oggetto (es. "63 file
Game-Godot-v2 reorg loss-risk" Lenovo vs "engine .uid churn" Ryzen).
**Nessuna delle 2 si fida cieca dell'altra**. Risoluzione = ground-truth
diretto sul PC dove i file SONO = autoritativo. Lenovo session stessa flaggava
"behind=0 NON affidabile dal mio lato, fetch SSH silent-fail" = onesta
sui propri limiti, escalava a Ryzen. Pattern proven working.

**Mitigation.** (i) Mai trustare cross-PC remote-state senza ground-truth-local;
(ii) ogni session deve essere honest sui propri limiti (ref-stale-claim,
SSH-fetch-fail, ecc); (iii) coordinator-session ha l'autorita di ground-truth
sul PC dove gira; (iv) handoff-doc serve come tie-breaker per AI-conflict
(=SoT condiviso, no he-said-she-said).

**Anti-Pattern# reinforcement**: L-034 esistente. Aggiungere clausola
"cross-session AI-conflict -> ground-truth-local arbiter".

---

## NEXT-PROMOTION

Quando convenient (Lenovo accesso), promuovi 5 lessons -> aa01
`learnings/L-2026-05-NNN-*.md` (slug: jules-silent-drop, helper-over-engineering,
encoding-policy-enforcement, ssh-cmd-cross-shell, ai-conflict-ground-truth).
Anti-Pattern-Catalogue update global CLAUDE.md (Eduardo gate, sovereign).

## LESSONS-PROMOTED 2026-05-20 (D-sequence closure)

L-DRAFT-A..E promossi a canonical vault learnings + Anti-Pattern Catalogue
globale aggiornato (Ryzen-side deploy done, Lenovo deploy deferred next-session):

- **L-2026-05-034** jules-silent-drop -> Anti-Pattern #10 (bot-rewrite-drop su fix-recenti non-CI-guarded)
- **L-2026-05-035** helper-over-engineering -> Anti-Pattern #11 (helper-tool che introduce piu failure-surface del task originale)
- **L-2026-05-036** encoding-policy-enforcement -> Anti-Pattern #12 (encoding-policy compliance richiede enforcement non-solo-doc)
- **L-2026-05-037** ssh-cmd-cross-shell -> Anti-Pattern #13 (SSH-cmd cross-shell tool incompat silent-collapse)
- **L-2026-05-038** ai-conflict-ground-truth -> reinforcement L-025 famiglia (no new entry catalogue)

**Vault PR refs**:
- PR #139 (5 L-NNN promotion) MERGED 2026-05-20T18:35:04Z, squash commit `fcb5b26ef`
- PR #140 (Anti-Pattern #10-#13 canonical CLAUDE.md) MERGED 2026-05-20T18:53:41Z, squash commit `316bf8c32`

**Deploy status fleet**:
- Ryzen `~/.claude/CLAUDE.md` propagated 2026-05-20 via `deploy_claude_global.ps1 -Apply` (CLAUDE.md identical canonical, #10-#13 visible)
- Lenovo `~/.claude/CLAUDE.md` PENDING (next Lenovo session: `git pull vault` + `deploy_claude_global.ps1 -Apply`)
- Side-finding: script exit 1 su supermemory marketplace add (preexisting canonical drift, separato dal PR #140, da triagare)

**Codex P2 review addressed** (PR #139): L-036 hook example `grep -P` -> `perl -ne` (portable BSD/macOS) + glob extended (ps1|sh|bat|cmd|py|js|json|ya?ml) per coverage-align con doc policy.

**Coordinator-lane cleanup**: venv `C:/Users/VGit/AppData/Local/Temp/browser-use-fe3-venv` (264MB) deleted; 2 .py scripts archiviati `codemasterdd/docs/research/od-053-browser-use-fe3-scripts-2026-05-20/`. Cron `cross-repo-drift-monitor` Option-A leave-running (4 iter all-OK, watchdog mode).
- `[parallel-#2 MERGED PR-δ #122 squash 91d5007 finish 2026-05-20T17:15:12Z]` (Fase 1 PR 4/5 done; 4 commits +548/-0 in 9 file; GET /api/audit + composite migration + 12 test + research; full suite 153→165 verde; CI 8/8 pass incl. schema-doc-check 5s; next PR-ε import validator STRICT)
- `[parallel-#2 DONE FIX-#123 https://github.com/MasterDD-L34D/Game-Database/pull/124 finish 2026-05-20T17:22Z]` (a11y MUI TablePagination i18n fix; aria-label English defaults overridden con t() helper italiano; 4 file +84/-4; +3 test PaginationBar.test.tsx + 1 update DataTable.test.tsx; chiude #123 OD-053 browser-use finding; CI pending)
- `[parallel-#2 MERGED FIX-#123 PR #124 squash be15c7f finish 2026-05-20T17:24:26Z]` (a11y fix MUI TablePagination i18n; +84/-4 in 4 file; +3 PaginationBar.test.tsx + 1 DataTable.test.tsx update; CI 4/4 verde; issue #123 auto-CLOSED)
- `[parallel-#2 OWNING Game-Database branch claude/parallel-gamedb-pr-epsilon-import-validator-2026-05-20 start 2026-05-20T17:31Z]` (Ryzen, scope: PR-ε Fase 1 5/5 import-taxonomy.js --validate-only flag + STRICT default tiered errori+schema_validation per Q4 resolved + fix stdout JSON pollution bug)
- `[parallel-#2 DONE PR-ε https://github.com/MasterDD-L34D/Game-Database/pull/125 finish 2026-05-20T17:34Z]` (import validator Fase 1 PR 5/5 — FASE 1 COMPLETE: --validate-only flag + STRICT tiered exit code Q4 + computeExitCode pure function + stdout JSON pollution fix; 3 commit +297/-11; +16 test; full suite 165→181 verde; CI pending)
- `[parallel-#2 MERGED PR-ε #125 squash e1454c2 finish 2026-05-20T17:38:15Z]` (FASE 1 COMPLETE — 5/5 PR all merged; --validate-only flag + STRICT tiered + computeExitCode pure + stdout JSON pollution fix; 3 commits +300/-11 in 4 file; CI 6/6 verde; full suite 165→181 verde)
- `[parallel-#2 MERGED PR #118 spec roadmap squash 9f01b4e finish 2026-05-20T17:42:31Z]` (spec + plan PR-α + 4Q autoresearch all su main; followup PR #126 status DRAFT→EXECUTED con merge SHAs)
- `[parallel-#2 MERGED PR #126 spec-executed squash eb3f890 finish 2026-05-20T17:44:27Z]` (docs-only +19/-1: spec status DRAFT→EXECUTED + Fase 1 PR table SHAs; no-CI docs-only; sessione parallel-#2 = TOTAL CLOSED, Fase 1 complete, 0 issue 0 PR open)
- `[parallel-#2 OWNING Game-Database branch claude/parallel-gamedb-fase2-audit-history-ui-2026-05-20 start 2026-05-20T18:25Z]` (Ryzen, scope: Fase 2 1/N audit history UI panel — consume /api/audit endpoint PR-δ, AuditHistoryPanel component su 4 entity detail pages, i18n strings, smoke tests)
- `[parallel-#2 DONE FASE2-1 https://github.com/MasterDD-L34D/Game-Database/pull/127 finish 2026-05-20T18:30Z]` (Fase 2 1/N audit history UI: AuditHistoryPanel su 4 entity detail pages, lib/audit.ts client, 11 i18n key audit.json, +6 vitest; consume PR-δ endpoint; +1 file passing +6 test vs baseline dashboard; CI pending)
- `[parallel-#2 MERGED FASE2-1 #127 squash f986922 finish 2026-05-20T18:32:32Z]` (Fase 2 1/N audit history UI done; 9 file +397/-1; AuditHistoryPanel su 4 detail page + lib/audit.ts + 11 i18n key + 6 vitest; CI 4/4 verde)
- `[parallel-#2 DONE CODEX-FOLLOWUP https://github.com/MasterDD-L34D/Game-Database/pull/128 finish 2026-05-20T18:40Z]` (5 Codex review comments unaddressed in PR #118/#122/#125/#127 → consolidated fix: P1 process.exitCode + arg parser --flag=value form, P2 audit empty-string validation, audit-UI useInfiniteQuery append, spec PR-ε mode consistency + new pre-merge protocol section; backend 181→193 verde; CI pending)
- `[parallel-#2 MERGED CODEX-FOLLOWUP #128 squash 0df1a41 finish 2026-05-20T18:42:57Z]` (5 Codex findings fixed + nuovo pre-merge protocol section spec; 7 file +226/-27; backend 181→193 verde; CI 6/6 + 0 Codex comment passed via new protocol — protocol now ACTIVE for all future PRs)
- `[parallel-#2 MERGED PROTOCOL-PERSIST #129 squash c056528 finish 2026-05-20T18:46:16Z]` (CLAUDE.md + AGENTS.md ora documentano pre-merge gh-api comments-check protocol mandatory; durability cross-session, sessione futura su questo repo legge la rule da onboarding docs immediati; +49/-2; new protocol passed first-check on this PR — 0 CI no path-filter + 0 Codex no source change)
- `[parallel-#2 OWNING Game-Database branch claude/parallel-gamedb-fase2-audit-revert-2026-05-20 start 2026-05-20T18:48Z]` (Ryzen, scope: Fase 2 2/N audit revert endpoint POST /api/audit/:logId/revert per DELETE actions, requireTaxonomyWrite gated, v1 resurrect tombstoned entity, UPDATE-revert deferred per spec note)
- `[parallel-#2 DONE FASE2-2 https://github.com/MasterDD-L34D/Game-Database/pull/130 finish 2026-05-20T18:52Z]` (Fase 2 2/N audit revert endpoint: POST /api/audit/:logId/revert DELETE-only v1, 5 master entity whitelist + scalar field projection, requireTaxonomyWrite gated; +8 test 16→24 audit.test.js; full backend 193→201 verde; CI pending — pre-merge protocol active gh-api check before squash)
- `[parallel-#2 MERGED FASE2-2 #130 squash + Codex P2 slug-collision fix included finish 2026-05-20T18:55Z]` (Fase 2 2/N audit revert done; 3 file +553/-3 (route + tests + research); Codex slug @unique collision P2 caught pre-merge via new gh-api protocol, fixed in additional commit + regression test; 25/25 audit verde; 202/202 backend full suite; CI 6/6 pass)
- `[parallel-#2 OWNING Game-Database branch claude/parallel-gamedb-fase2-revert-ui-2026-05-20 start 2026-05-20T19:04Z]` (Ryzen, scope: Fase 2 3/N revert UI button su AuditHistoryPanel per DELETE entries, consume POST /api/audit/:logId/revert PR #130; snackbar feedback + query invalidation; pre-merge protocol applied)
- `[parallel-#2 DONE FASE2-3 https://github.com/MasterDD-L34D/Game-Database/pull/131 finish 2026-05-20T19:07Z]` (Fase 2 3/N revert UI button: Ripristina su AuditHistoryPanel per DELETE entries, consume POST /api/audit/:logId/revert PR #130, snackbar feedback localized, 3-way error surface; +4 vitest 7→11; end-to-end undo flow complete #122→#127→#130→#131; CI pending)
- `[parallel-#2 MERGED FASE2-3 #131 squash eba3997 finish 2026-05-20T19:10:48Z]` (revert UI Ripristina button su AuditHistoryPanel DELETE entries; consume POST /api/audit/:logId/revert; snackbar 3-way error localized; +4 vitest 7→11; CI 4/4 verde + 0 Codex comment protocol passed; end-to-end undo flow #122→#127→#130→#131 COMPLETE)
- `[parallel-#2 OWNING Game-Database branch claude/parallel-gamedb-fase2-revert-confirm-2026-05-20 start 2026-05-20T19:11Z]` (Ryzen, scope: Fase 2 4/N confirmation dialog before revert, prevent accidental resurrect, MUI Dialog + i18n + tests)
- `[parallel-#2 DONE FASE2-4 https://github.com/MasterDD-L34D/Game-Database/pull/132 finish 2026-05-20T19:14Z]` (Fase 2 4/N confirmation dialog before revert: MUI Dialog gate prima del POST /api/audit/:logId/revert, aria-labelledby + autoFocus a11y; +2 vitest cases dialog open/cancel + 3 refactored 11→13 verde; pre-merge protocol active)
- `[parallel-#2 MERGED FASE2-4 #132 squash 522abfd finish 2026-05-20T19:17:47Z]` (confirmation dialog before revert; MUI Dialog gate prima POST revert; +140/-9 in 3 file; 11→13 vitest AuditHistoryPanel verde; CI 4/4 + 0 Codex comments protocol passed)
- `[parallel-#2 OWNING Game-Database branch claude/parallel-gamedb-fase2-payload-renderer-2026-05-20 start 2026-05-20T19:21Z]` (Ryzen, scope: Fase 2 5/N audit payload renderer — sostituisci JSON.stringify con AuditPayloadRenderer key-value table action-aware (UPDATE patch / CREATE snapshot / DELETE removed); _revertedFrom highlight per audit-trail visualization)
- `[parallel-#2 DONE FASE2-5 https://github.com/MasterDD-L34D/Game-Database/pull/133 finish 2026-05-20T19:25Z]` (Fase 2 5/N AuditPayloadRenderer: structured MUI Table sostituisce JSON.stringify nel AuditHistoryPanel expandable; action-aware caption + _revertedFrom Chip audit-trail viz; 11 i18n key; +13 nuovi vitest AuditPayloadRenderer.test.tsx 13→26 audit tests verde; pre-merge protocol active)
- `[parallel-#2 MERGED FASE2-5 #133 squash 51d13e49ec135758bd993855051d4bbfde3675c4 finish 2026-05-20T19:30Z]` (audit payload renderer + revertedFrom chip; 5 file +337/-18; 26/26 audit dashboard tests verde; CI 4/4 + 0 Codex protocol passed)
- `[parallel-#2 OWNING Game-Database branch claude/parallel-gamedb-fase2-payload-diff-2026-05-20 start 2026-05-20T19:51Z]` (Ryzen, scope: Fase 2 6/N field-by-field diff UPDATE entries — AuditPayloadRenderer accept previousPayload, render oldValue → newValue + colored highlights)
- `[parallel-#2 DONE FASE2-6 https://github.com/MasterDD-L34D/Game-Database/pull/134 finish 2026-05-20T19:54Z]` (Fase 2 6/N field-by-field diff UPDATE entries: 3-column AuditPayloadRenderer diff mode, prior cell red + new cell green highlights, (invariato)/(non disponibile) markers, deepEqual nested; AuditHistoryPanel auto-wires previousPayload from items[idx+1]; +6 vitest 13→19 AuditPayloadRenderer + AuditHistoryPanel 13 unchanged = 32/32 verde; pre-merge protocol active)
- `[parallel-#2 MERGED FASE2-6 #134 squash ff98505 finish 2026-05-20T19:57:31Z]` (payload diff 3-column UPDATE entries, prior+new color-highlighted; +225/-32 in 4 file; 32/32 audit dashboard verde; CI 4/4 + 0 Codex protocol passed)
