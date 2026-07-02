# Runbook -- Godot doc-comment campaign handoff (OpenCode / any agent)

Self-contained procedure to CONTINUE the GDScript doc-comment campaign on
`Game-Godot-v2` without Claude/Max. Any agent that can run PowerShell + git + gh
+ curl (OpenCode 30B, Aider, a future Claude session, a human) can drive this.
The safety is the **ground-truth gate** (section 4) -- it is 100% mechanical
(pass/fail, no judgment), so delegating the loop stays safe.

Companion docs: `docs/runbook/jules-session-triage-via-cli.md` (generic Jules CLI),
GGv2 `docs/godot-v2/doc-comment-campaign.md` (the coverage tracker = state SoT).

## 0. What + why + state

- **What**: add `##` GDScript doc-comments to the PUBLIC API (non `_`-prefixed
  funcs + class) of `C:/dev/Game-Godot-v2/scripts/**/*.gd`.
- **Why**: Godot in-editor class reference + autocomplete tooltips. The comments
  are INERT -- comment-only, additions-only, ZERO behavior change.
- **State (2026-06-06)**: 99 / 251 (39%). Tracker (scan-regenerated) is the SoT:
  `Game-Godot-v2/docs/godot-v2/doc-comment-campaign.md`.
- **Machine**: Ryzen `DESKTOP-T77TMKT` / `VGit`. SOLE Jules handler (Lenovo backed off).
- **Auth**: Eduardo authorized THIS campaign's auto-merge (external repo,
  doc-comment-only lane). Do NOT extend the auto-merge to any non-doc-comment work.

## 1. Pre-flight (every session, before any dispatch)

```powershell
# (a) identity -- MUST be Ryzen
Write-Output ('PC=' + $env:COMPUTERNAME + ' USER=' + $env:USERNAME)   # PC=DESKTOP-T77TMKT USER=VGit

# (b) cdd wrapper currency -- the stale-wrapper trap (gate-4 paginated-abort if pre-#307)
git -C C:/dev/codemasterdd-ai-station fetch origin main --quiet
git -C C:/dev/codemasterdd-ai-station merge --ff-only origin/main      # only if on main
(Select-String -Path C:/dev/codemasterdd-ai-station/scripts/fleet/jules-dispatch.ps1 -Pattern 'Get-AllSessionPages' | Measure-Object).Count   # MUST be 3

# (c) GGv2 currency
git -C C:/dev/Game-Godot-v2 fetch origin main --quiet
```

If (a) != Ryzen -> STOP. If (b) count != 3 -> `ff-only` main first (a stale local
main reverts the wrapper to the pre-#307 version that aborts on a paginated
session list once >100 lifetime Jules sessions exist).

## 2. Pick a target (scan)

```powershell
$repo='C:/dev/Game-Godot-v2'
$files = @(git -C $repo ls-tree -r --name-only origin/main scripts) | Where-Object { $_ -like '*.gd' }
$rows = foreach ($f in $files) {
  $lines = @(git -C $repo show "origin/main:$f")
  if ($lines | Where-Object { $_ -match '^\s*##' } | Select-Object -First 1) { continue }   # already documented
  $pub = @($lines | Where-Object { $_ -match '^(static\s+)?func\s+[A-Za-z]' }).Count
  $na = (($lines -join "`n").ToCharArray() | Where-Object { [int]$_ -gt 127 }).Count
  [pscustomobject]@{ File=$f; Pub=$pub; Lines=$lines.Count; NA=$na }
}
$rows | Where-Object { $_.Pub -ge 2 -and $_.Lines -le 150 } | Sort-Object NA, @{e='Pub';Descending=$true}, Lines | Format-Table -AutoSize
```

Prefer **Pub >= 2, Lines <= 150, NA low**. Batch 3 SMALL files (a "trio") for fast
cadence; for files >100 lines do 1-2 at a time (rewrite-risk). See section 7 (bad targets).

## 3. Write the strict task-file (the #1 cognitive step)

Read each target, enumerate the EXACT public funcs (skip `_`-prefixed). Write
`C:/dev/codemasterdd-ai-station/logs/jules-tasks/godot-doc-<name>.md` from the
template in section 9. STRICT-PROMPT RULE (load-bearing -- proven 3/3 clean vs
generic 2/4):

- EXACT function list, with the VERBATIM `##` text to write above each.
- "ONLY add `##` lines. ZERO deletions. Every pre-existing line BYTE-IDENTICAL.
  No rename / refactor / reorder / re-indent."
- Placement: the `##` block goes DIRECTLY above the declaration, AFTER any
  existing leading `#` comment (so the doc-comment attaches to the member). If
  `class_name` is the first line, the class `##` goes at the very top of the file.
- ASCII-only NEW lines (`--` not em-dash). Each `##` line **<= 100 chars** (gdlint
  max-line-length 100 -- gdformat does NOT catch this, so bake it into the prompt).
- Preserve existing non-ASCII bytes (em-dash/arrow in headers): do NOT re-encode.

## 4. GROUND-TRUTH GATE (THE SAFETY -- never skip, never merge on any fail)

After extracting the patch (section 5), run this and require ALL green:

```powershell
$lines = (Get-Content $patchFile -Raw) -split "`n"
$adds = @($lines | Where-Object { $_ -match '^\+' -and $_ -notmatch '^\+\+\+' })
$dels = @($lines | Where-Object { $_ -match '^-' -and $_ -notmatch '^---' })
$naAdd = 0; foreach ($l in $adds) { foreach ($ch in $l.ToCharArray()) { if ([int]$ch -gt 127) { $naAdd++ } } }
$nonDocAdds = @($adds | Where-Object { $_ -notmatch '^\+\s*##' })
$diffFiles = @($lines | Where-Object { $_ -match '^diff --git' })
Write-Output ("diff_git=$($diffFiles.Count)  adds=$($adds.Count)  dels=$($dels.Count)  naAdd=$naAdd  nonDocAdds=$($nonDocAdds.Count)")
```

Require: `diff_git == N` (only the N target files) AND `dels == 0` AND `naAdd == 0`
AND `nonDocAdds == 0` AND `adds == expected` (sum of the class+func `##` lines you
specified). THEN apply on a fresh branch (section 6) and require `gdformat --check`
= "unchanged" and `gdlint` = "no problems". ANY fail -> reject that file, ship only
clean siblings, or re-dispatch with a tighter prompt. Do not "fix it by hand" --
re-dispatch (keeps the additions-only guarantee).

## 5. Dispatch + monitor + extract

```powershell
# dispatch (cd codemasterdd). NEVER -ForceBlind (classifier blocks it + defeats dedup).
# If your PROCESS CWD differs from the PS location (e.g. dispatching from a git worktree),
# pass -TaskFile as an ABSOLUTE path: .NET [IO.File] resolves relative paths against the
# process CWD, not the PS location (seen 2026-07-02: ReadAllText threw on a valid path).
cd C:/dev/codemasterdd-ai-station
& scripts/fleet/jules-dispatch.ps1 -Repo Game-Godot-v2 -TaskFile logs/jules-tasks/godot-doc-<name>.md -Target "scripts/<dir>/<a>.gd,scripts/<dir>/<b>.gd"
# -> prints "DISPATCHED session <SID> (state=QUEUED)". Save <SID>.
```

Monitor with an INLINE background bash poll (do NOT Write a .sh file -- tdd-guard
blocks new operational scripts). REST base `https://jules.googleapis.com/v1alpha`,
header `x-goog-api-key`, key in `~/.config/api-keys/keys.env` (JULES_API_KEY):

```bash
set -a; source ~/.config/api-keys/keys.env; set +a
sid=<SID>
for i in $(seq 1 150); do
  state=$(curl -s -H "x-goog-api-key: $JULES_API_KEY" "https://jules.googleapis.com/v1alpha/sessions/$sid" | python -c "import sys,json
try: print(json.load(sys.stdin).get('state',''))
except: print('ERR')")
  echo "[poll $i] $state"; case "$state" in COMPLETED|FAILED|CANCELLED|ARCHIVED) echo TERMINAL=$state; break;; esac; sleep 20
done
```

Extract the patch (PowerShell):

```powershell
$apiKey = ((Get-Content "$HOME/.config/api-keys/keys.env" | Where-Object { $_ -match '^JULES_API_KEY=' }) -replace '^JULES_API_KEY=','')
$hdr = @{ 'x-goog-api-key' = $apiKey }
$s = Invoke-RestMethod -Headers $hdr "https://jules.googleapis.com/v1alpha/sessions/<SID>"
$patch = $s.outputs[0].changeSet.gitPatch.unidiffPatch
# FAILED session with empty outputs -> fall back to an EARLY activities snapshot:
#   $s.activities[].artifacts[].changeSet.gitPatch.unidiffPatch  (take a pre-pollution one)
# DELIVERY-MISS (seen 2026-07-02, sid 15385179988696772982): a session can be COMPLETED with
# NO outputs field at all AND GET /activities returning {} -- nothing recoverable via API.
# Wait ~2 min, re-GET once; if still empty, RE-DISPATCH the same task-file (gate-4 passes:
# the dead session is terminal, so there is no active-overlap). Second run came back clean.
[IO.File]::WriteAllText('C:/dev/codemasterdd-ai-station/logs/jules-tasks/patch-<name>.diff', $patch, (New-Object Text.UTF8Encoding $false))
```

## 6. Apply + verify + ship

```powershell
# Currency-Gate: branch from CURRENT origin/main. Verify branch-show-current (collision-safe).
git -C C:/dev/Game-Godot-v2 fetch origin main --quiet
git -C C:/dev/Game-Godot-v2 checkout -b chore/jules-godot-<dir>-doccomments-N origin/main
git -C C:/dev/Game-Godot-v2 branch --show-current      # MUST equal the branch you just made
git -C C:/dev/Game-Godot-v2 apply --ignore-whitespace C:/dev/codemasterdd-ai-station/logs/jules-tasks/patch-<name>.diff
Push-Location C:/dev/Game-Godot-v2
gdformat --check <files...>   # MUST say "<n> files would be left unchanged"
gdlint <files...>             # MUST say "Success: no problems found"
Pop-Location
```

Commit with ADR-0011 trailers, push, PR, merge --rebase:

```powershell
$traceId = (python -c "import time,secrets; ms=int(time.time()*1000)&((1<<48)-1); ra=secrets.randbits(12); rb=secrets.randbits(62); v=(ms<<80)|(0x7<<76)|(ra<<64)|(0b10<<62)|rb; h='%032x'%v; print('%s-%s-%s-%s-%s'%(h[0:8],h[8:12],h[12:16],h[16:20],h[20:32]))").Trim()
git -C C:/dev/Game-Godot-v2 add <files...>
# message body MUST be ASCII + have ZERO double-quotes when using -m (see gotchas). Trailers:
#   Coding-Agent: <your-agent-id>    (e.g. opencode-qwen3-coder-30b)
#   Trace-Id: $traceId               (NO Co-Authored-By trailer, ever)
git -C C:/dev/Game-Godot-v2 commit -m $msg
git -C C:/dev/Game-Godot-v2 push -u origin chore/jules-godot-<dir>-doccomments-N
# SEPARATE call (do not chain a temp-file Remove-Item -- see gotchas):
$pr = gh pr create -R MasterDD-L34D/Game-Godot-v2 --base main --head chore/jules-godot-<dir>-doccomments-N --title "docs(<dir>): ..." --body '...'
gh pr merge ($pr -split '/')[-1] -R MasterDD-L34D/Game-Godot-v2 --rebase --delete-branch   # --rebase preserves trailers; squash DROPS them
```

## 7. Bad targets (skip)

- **> 150 lines** = rewrite-risk. If it is high-value (many public funcs), do it
  ALONE or as a pair, never in a fast trio.
- **0-1 public func** = class-only doc, low value -- usually skip.
- **High non-ASCII** (NA > ~10), e.g. host-views = mojibake-on-rewrite risk.
- **Minified / single-letter-name** files. (GDScript itself is NOT a bad target --
  30+ files shipped clean; doc-comments on .gd are the proven lane.)

## 8. PS 5.1 gotchas (each one cost real time -- avoid)

- **commit -m with double-quotes** in the body -> PS native-arg quoting splits the
  string -> git sees a stray pathspec and aborts. Fix: keep the body double-quote-free
  and use `-m` here-string, OR write the body to a file and `git commit -F <file>`.
- **Do NOT combine** commit+push+PR+merge in one call that ends with a temp-file
  `Remove-Item` -- the sandbox blocks `Remove-Item` on an empty/odd path and aborts
  the WHOLE command (the merge silently never runs). Split into commit+push, then
  PR+merge. Skip the temp-file cleanup entirely.
- **LF patch vs CRLF repo** -> always `git apply --ignore-whitespace`.
- **Branch-name collision** with a prior merged leftover -> `checkout -b` fails but
  you stay on the OLD branch and apply to the wrong base. ALWAYS check
  `branch --show-current` after; bump the `-N` suffix on collision.
- **Native git/gh stderr-on-success** -> the tool may report exit 255 noise; trust
  the explicit `$LASTEXITCODE` you print, not the wrapper's exit.
- **.NET IO vs PS location** -> `[IO.File]::ReadAllText`/`ReadAllBytes` resolve RELATIVE
  paths against the PROCESS CWD, which `Set-Location`/`Push-Location` do NOT move. From a
  worktree (or any mismatched CWD) pass ABSOLUTE paths, or align
  `[Environment]::CurrentDirectory` with the PS location first.

## 9. Embedded task-file TEMPLATE (copy + adapt per batch)

```
# Jules scoped task: GDScript doc-comments for N scripts/<dir>/ files

## Scope (N files, docstring-only, no logic change, no behavior change)
Add Godot doc-comments (## blocks) to EXACTLY these files, nothing else:
- scripts/<dir>/<a>.gd
- scripts/<dir>/<b>.gd
Comment-only. Do NOT touch any other file. Do NOT touch private (_-prefixed) functions
(in particular do NOT add a ## block to `_<privatename>`).

## Exact edits -- add EACH ## block VERBATIM immediately ABOVE the named line, nothing else
## IMPORTANT: where a plain `#` comment already sits directly above a function (or class_name),
## place the new ## block BETWEEN that `#` comment and the declaration (so the ## attaches).

### File: scripts/<dir>/<a>.gd
1. Above `class_name <ClassA>`:
   ## <one-line class summary, <=100 chars, ASCII>.
   ## <optional second line>.
2. Above `static func <fn1>(<exact signature>) -> <Ret>:`:
   ## <what it does + return/edge, <=100 chars>.
... (one numbered entry per PUBLIC func, verbatim ## text)

## Hard constraints (ADR-0035 scoped-strict)
- ONLY add ## lines. ZERO deletions. Every pre-existing line BYTE-IDENTICAL.
- Do NOT rename/refactor/reformat/reorder/re-indent; do NOT change any signal or signature.
- Preserve every existing byte exactly (incl. non-ASCII em-dash/arrow in headers); no re-encode.
- ASCII-only for NEW lines (no smart quotes, no em-dash; write `--`).
- Each new ## line <= 100 chars (gdlint max-line-length 100).
- Place each ## block DIRECTLY above its declaration, AFTER any existing leading `#` comment.

## Acceptance (verifiable)
- `git diff` shows ONLY added ## lines (ZERO deleted/changed) across the N files.
- gdformat unchanged; every new ## line <= 100 chars (gdlint-clean).
- Only the N files above modified.
```

The dispatch wrapper appends its own anti-pollution clause and runs 5 fail-closed
gates (repo-whitelist / ASCII-lint / scoped-template-lint / dedup-vs-active /
dispatch). The task-file MUST contain the markers it lints for: a target path,
"no logic change"/"docstring", "ascii-only", and "acceptance" -- the template has them.

## 10. NEXT-TARGETS QUEUE (scan @ 99/251, 2026-06-06)

Work small trios first (fast), then the big high-value ones 1-2 at a time, then STOP.

- **Fast lane (small, Pub>=2)**: `ui/lobby_spectator_poll.gd` (2pub,55L), plus
  re-scan section 2 each session -- new small files surface as siblings get done.
- **Big high-value (1-2 at a time, >100L)**: `services/telemetry_collector.gd`
  (7pub,143L), `phone/phone_coop_vote_wire.gd` (8pub,130L), `ai/sistema_intents.gd`
  (5pub,125L), `combat/sense_reveal.gd` (6pub,148L), `session/combat_emitter_caller.gd`
  (4pub,121L), `main_thoughts_ritual.gd` (4pub,82L).
- **Tail (low value -- STOP here)**: zero/one-public-func files, high-non-ASCII
  host-views (`ui/*_host_view.gd`, `ui/job_card_panel.gd` 18NA, `ui/unit_info_panel.gd`
  22NA). Class-only docs add little; do not chase 100% for its own sake.

## 11. Wrap-up (end of a working session)

1. Regen the tracker by SCAN (section 2 count) -> edit
   `Game-Godot-v2/docs/godot-v2/doc-comment-campaign.md` snapshot + per-dir table +
   batch rows -> branch+PR+merge (NOT a hand-patch drift).
2. Prune merged leftover branches (cherry-verified, only `+`-free ones):
   `git -C C:/dev/Game-Godot-v2 checkout --detach origin/main` then for each
   `chore/jules-godot-*` / `chore/tracker-regen-*`: keep if `git cherry origin/main <b>`
   has any `^\+` line, else `git branch -D <b>`.
3. JOURNAL: add an entry to `codemasterdd JOURNAL.md` and land via
   `scripts/fleet/journal-land.ps1 -Subject "docs(journal): <desc>"`.

## 12. Honest caveat (read before grinding)

These doc-comments are INERT polish -- no wiring, no tests; "completion" is purely
the coverage % reaching 100%. Per ADR-0023 post-Max routing this is LOW priority:
correct for a free/sovereign tool (OpenCode) or a pause, NOT worth Claude-API budget.
STOP when the value clearly drops (the remaining tail is large / zero-pub / high-NA).
A clean stop at any % with an accurate tracker + zero pending branches is a fine outcome.
