# VC governance review -- push/PR/merge model vs authoritative practice (2026-05-28)

> **Trigger**: Eduardo -- "non mi e' chiaro perche' push diretti su repo privati anche
> se coordinati; rivedi la struttura confrontandoti con fonti/repo autorevoli".
> **Method**: Protocol 2 autoresearch (multi-source, web) + synthesis con stato interno.
> **Authored-from**: Lenovo (CodeMasterDD / edusc / .10). Usabile cross-fleet.
> **Scope**: modello version-control (push diretto vs PR-gate vs branch-protection) +
> coordinamento multi-repo/fleet + governance commit-agent. NON l'intera architettura
> 7-repo (se vuoi quella, scope separato).

## Repo legend (path nei backtick)

I path nei `backtick` qui sotto sono relativi al repo di volta in volta nominato in prosa. Cross-fleet:

- **codemasterdd** = `C:/dev/codemasterdd-ai-station/...` -- https://github.com/MasterDD-L34D/codemasterdd-ai-station (PRIVATE)
- **Game** = `C:/dev/Game/...` (entrambi PC) -- https://github.com/MasterDD-L34D/Game (PUBLIC)
- **vault** = `C:/dev/vault/Spaces/Dev/Evo-Tactics/...` -- https://github.com/MasterDD-L34D/vault (PRIVATE sovereign)

Dove il contesto rende ambiguo (es. sia codemasterdd sia Game hanno un `.github/workflows/ci.yml`), il repo e' esplicitato in prosa.

## Verdetto

**La struttura e' sana e ricalca pattern riconosciuti come buoni.** La variazione di
modello per-repo (in base al RUOLO del repo) e' una feature, non un'anomalia. Nessun
fix urgente; 4 punti di hardening (sotto), 3 gia' azionati in questa sessione.

## Il dubbio chiarito: sync e review-gate sono ORTOGONALI

"Coordinato/synced tra macchine" **non implica** PR.
- `git pull` tiene aggiornate le *copie di lavoro* sulle varie macchine.
- Il PR controlla *cosa entra in main* (review + CI-gate + audit-trail).
Sono due concern indipendenti. Che `main` si aggiorni via push-diretto o via PR-merged,
il meccanismo di coordinamento (pull dall'origin GitHub = hub) e' identico. Il PR aggiunge
**review**, non coordinamento. L'intuizione di Eduardo era corretta.

## Modello per-repo vs fonti

| Nostro repo | Modello | Modello noto | Verdetto fonti |
|---|---|---|---|
| codemasterdd (private, infra, solo-author + agenti) | **push diretto a main**, no PR, no branch-protection | Trunk-based development | **Corretto.** trunkbaseddevelopment.com: "very small teams may commit direct to the trunk". DORA: PR *async self-approved* = ritardo (pitfall) senza valore secondo-reviewer. Fowler: "PR necessari per review = rubbish" |
| vault (private, sovereign knowledge) | **branch + PR only**, merge Eduardo | Ship/Show/**Ask** (Fowler) | **Legit ma e' una SCELTA** (gate-oversight deliberato), non necessita'. Vale se la pausa-review ti da' valore reale; altrimenti e' overhead self-approved. Downgrade a "Show" (push + PR informativa) se diventa solo attrito |
| Game / Godot-v2 / Game-Database (public) | branch-protection + required checks + PR | GitHub flow | **Corretto** (public + contributor esterni + CI gate reale) |
| Multi-repo: origin GitHub = hub, `git pull` per-PC, SSH fleet | Polyrepo standard | **Normale.** Submodule / monorepo / `repo`-tool servono per *dipendenze inter-repo atomiche*; 7 repo loose -> sarebbero over-engineering |
| Commit-agent: trailer `Coding-Agent` + `Trace-Id`, no `Co-Authored-By` | Guardrail layered + review non-bloccante | **Allineato** (hook + trailer). La rinuncia a `Co-Authored-By` (ADR-0011) e' scelta interna difendibile ma diverge dal default piattaforma |

Sintesi fonti: la decomposizione del valore di un PR e' (1) review umana -- nulla senza
secondo reviewer; (2) CI-gate -- ottenibile via hook/CI **senza** PR; (3) audit-trail --
gia' coperto dai trailer commit. Quindi push-diretto su repo private solo-owner = corretto;
PR-flow su public = corretto; modelli diversi per ruolo = esplicitamente supportato
(GitHub Well-Architected: "tailored team workflows per repository").

## Red flag + azioni (questa sessione)

| # | Flag | Severita' | Azione |
|---|------|-----------|--------|
| 1 | codemasterdd: push-diretto **senza CI server-side** -> commit-agent sbagliato atterra non-verificato (e i pre-commit hook locali sono bypassabili con --no-verify / assenti su clone fresco) | P1 | **FATTO**: `.github/workflows/ci.yml` -- safety-net non-bloccante: ASCII guard ADR-0021 su file changed + pytest (`scripts/tests`). No PR, nessun overhead |
| 2 | Admin-override merge su Game = config-smell (required-check path-filtered "skipping" restano Pending = footgun GitHub noto) | P2 | **FATTO + IMPLEMENTATO 2026-05-28 sera**: Game issue [#2410](https://github.com/MasterDD-L34D/Game/issues/2410) (CLOSED COMPLETED) -> [PR #2413](https://github.com/MasterDD-L34D/Game/pull/2413) MERGED (`9f918e26`) aggiunge job `ci-gate` aggregator + branch protection swap-pata a required `[governance, ci-gate]` (strict=true, enforce_admins=false invariati). Tooling-only PR ora CLEAN senza admin |
| 3 | SPOF: origin GitHub = unica copia off-machine (i 2 PC clonano ma dipendono dall'account) | P2 | **FATTO**: `scripts/backup/mirror-repos.ps1` (bare-mirror idempotente). Smoke su codemasterdd (201 refs). Runbook sotto |
| 4 | No backup-reviewer per commit-agent (inerente al solo-work) | P3 | Opzionale: Claude review non-bloccante anche su infra. Mitigato dai hook + harsh-reviewer on-demand (Protocol 5) |

## Mirror backup -- runbook

```powershell
# GitHub-account-loss insurance (bare mirror locale, idempotente):
powershell -ExecutionPolicy Bypass -File scripts\backup\mirror-repos.ps1
# default Dest = C:\dev\_mirror-backup (fuori da ogni repo). Repos = i 7 fleet.
# subset: ... mirror-repos.ps1 -Dest E:\git-mirrors -Repos codemasterdd-ai-station,vault
```
Per insurance anche contro disk-loss: sincronizza `$Dest` su disco esterno o cloud
(es. `robocopy` su drive esterno, oppure secondo `git push` verso altro remote).
Schedulazione (Task Scheduler) = scelta infra di Eduardo, non forzata qui.

## Decisioni risolte (2026-05-28, delega Eduardo "implementa le decisioni")

- **D1 vault PR-gate -> TENERE.** Vault = knowledge SoT sovereign; il merge-gate umano e' l'oversight value reale, costo basso (merge occasionali). Downgrade a Show scartato. No-change (gia' la policy attuale, CLAUDE.md vault boundary).
- **D2 codemasterdd CI -> NON-bloccante (confermato).** Trunk-based + solo-owner. Il gap "commit non verificato" e' gia' coperto a 2 layer: pre-commit locale (ASCII/silent-fail/silent-corruption, ADR-0008/0020/0021) + CI server-side (`ci.yml`, ADR-0021 + pytest). Pre-push hook = ridondante col pre-commit -> niente gold-plating. No branch-protection (eviterebbe il direct-push che e' il punto). No-change.
- **D3 mirror -> DECISO + REGISTRATO 2026-05-28 sera**: settimanale, target local bare (`C:\dev\_mirror-backup`) come GitHub-account-loss insurance sovereign; copia su drive esterno = step disk-loss manuale. Pre-req verificati: SSH key passphrase-less (run detached OK) + clone --mirror private (vault) OK non-interattivo. **7/7 repo mirrorati** localmente (Game 5689 commit / 2760 ref, vault 657, codemasterdd 733, ecc.). Task Scheduler **`codemasterdd-mirror-backup` registrato post-OK-esplicito Eduardo** (State=Ready, NextRun Dom 2026-05-31 10:00, ExecutionTimeLimit 1h, log -> `codemasterdd/logs/mirror-backup.log`). Caveat post-ship: script aveva un false-fail (`$ErrorActionPreference=Stop` + git stderr "Cloning into..." = NativeCommandError -> clone riusciti marcati FAIL); fix shipped in commit `db5c266` (`Continue` + gate solo su `$LASTEXITCODE`). Lesson `aa01/learnings/L-2026-05-040`. Comando di registrazione (per ri-creare il task se mai eliminato):
  ```powershell
  $r="C:\dev\codemasterdd-ai-station"
  $a=New-ScheduledTaskAction -Execute powershell.exe -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"& '$r\scripts\backup\mirror-repos.ps1' *>> '$r\logs\mirror-backup.log'`""
  $t=New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 10:00am
  $s=New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1)
  Register-ScheduledTask -TaskName "codemasterdd-mirror-backup" -Action $a -Trigger $t -Settings $s -Force
  ```

## Sources

- [DORA -- Trunk-based development](https://dora.dev/capabilities/trunk-based-development/)
- [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/)
- [Martin Fowler -- Pull Request](https://martinfowler.com/bliki/PullRequest.html)
- [Martin Fowler -- Ship / Show / Ask](https://martinfowler.com/articles/ship-show-ask.html)
- [GitHub Blog -- Agent pull requests, how to review them](https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/)
- [InfoQ -- Anthropic agent-based code review for Claude Code](https://www.infoq.com/news/2026/04/claude-code-review/)
- [GitHub Well-Architected -- Repository architecture strategy](https://wellarchitected.github.com/library/architecture/recommendations/scaling-git-repositories/repository-architecture-strategy/)
- [GitHub Docs -- Troubleshooting required status checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks)
- [GitHub Community #44490 -- skipped path-filtered required checks](https://github.com/orgs/community/discussions/44490)
