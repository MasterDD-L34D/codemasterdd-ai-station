# Jules tasking -- hardened prompts + verdetti (2026-06-02)

> Sessione "incaricare Jules": suggerimenti letti live via Claude-in-Chrome
> (read-only, sweep 7/7 repo configurati). Wiring + meccanica = vedi
> `docs/jules/JULES-CAPABILITIES-MASTER.md` §9. Il **lancio (Start) = Eduardo**.
> Uso: su jules.google -> apri il suggerimento -> bottone **"edit"** -> incolla
> il prompt sotto (sostituisce il template generico) -> **Start**. Cosi' il
> suggerimento high-signal di Jules eredita il guard-rail anti-#10/anti-S5.

## 1. Verdetti sui suggerimenti aperti

### codemasterdd -- "API Secret Exposure to Frontend" -> NON TASKARE (accepted-risk)

- **Location**: `apps/cross-repo-dashboard/app.py:690` -> `templates/cr_index.html:293`
  (`window.__API_SECRET__ = {{ api_secret|tojson }}`) -> `static/app.js` (Bearer
  token su `/api/draft-pr` + `/api/coord-event`).
- **Ground-truth verificato 2026-06-02**: host-binding = **127.0.0.1 SOLO**
  (`app.py:863` Werkzeug dev + `app.py:874` waitress prod + `tray.pyw:63/66`).
  Tool localhost single-user. Stack ADR-0017 down (non in esecuzione).
- Il token autentica JS **same-origin** a endpoint che lanciano PowerShell ->
  scopo = **anti-CSRF/cross-origin**, NON confidenzialita' dal proprio utente.
  Il viewer della pagina E' l'owner del token. **Zero escalation.**
- Gia' documentato inline: Codex P2 #111 + harsh-reviewer P0.2 (2026-05-14).
- Jules legge "secret in template" SENZA il threat-model localhost = pattern
  **S5/S6** (premise-questionable / behavior-change-under-security-title). Il
  suo "fix" (rimuovi secret + auth diversa) ROMPEREBBE l'auth same-origin o
  riaprirebbe il gap CSRF di #111.
- **Azione**: DISMISS la suggestion (close). NON taskare.
- **Precondizione futura**: se il binding cambia da `127.0.0.1` a `0.0.0.0` /
  reverse-proxy -> il rischio diventa reale, ri-valutare.

## 2. Prompt hardened pronti (paste in "edit" prima di Start)

### Game -- Code Duplication `flint_status_stdlib.py` (Jules-suggested, AST-detected)

```
Repo: MasterDD-L34D/Game   Base: main

TASK (single, narrow): Resolve the exact code duplication between
`tools/py/flint_status_stdlib.py` and `flint/tools/flint_status_stdlib.py`
(AST-detected duplicate blocks, ref tools/py/flint_status_stdlib.py:39).

HARD CONSTRAINTS (non-negotiable):
1. Do NOT delete either file blindly. FIRST determine, with evidence:
   (a) is each file imported/invoked, and from where? (grep the whole repo
       for both module paths + any dynamic/string import);
   (b) is `flint/tools/flint_status_stdlib.py` intentionally standalone /
       vendored (a no-deps copy meant to run on its own)? Check for
       packaging, entrypoints, CI that runs it in isolation, or a header
       saying so.
2. ONLY if no standalone/packaging constraint exists: dedupe by making the
   duplicate import the shared functions from a single canonical module.
   Do NOT invent a new shared location -- reuse the module already imported
   by the most callers.
3. If a standalone constraint exists (or it is unclear): do NOT change code.
   REPORT the finding in the PR description and stop. Preserve functionality
   over cleanliness.
4. ZERO behavior change. No logic/output change to either tool. Minimal diff.
   No dependency bumps, no unrelated files, no generated artifacts.
5. Keep/add a test that runs both tools' entrypoint and asserts identical
   output before/after. Run the full suite. PR must be CI-green.
6. PR title accurate (not generic "code health"). Conventional:
   `refactor(tools): dedupe flint_status_stdlib`.

After completing: confirm the branch diff is NON-EMPTY and pushed. If the
push produced no diff on the remote branch, say so explicitly.
```

### Generico -- "Unused import: X" (S5-guarded, riusabile per os/sys/...)

```
Repo: <repo>   Base: main

TASK (single, narrow): Remove the unused import `<NAME>` from `<FILE>`.

HARD CONSTRAINTS:
1. Before removing: grep the ENTIRE repo + the file itself for `<NAME>`,
   including dynamic usage (getattr, string refs, __all__, re-export,
   conditional / TYPE_CHECKING, test monkeypatch). If ANY real use exists,
   leave it and REPORT (it is not unused).
2. Touch ONLY `<FILE>`. Remove only the single unused import line. Nothing
   else. No reformatting, no reordering of other imports, no dep changes.
3. ZERO behavior change. Run lint + full test suite. PR must be CI-green.
4. PR title accurate. Conventional: `chore(<scope>): remove unused import <NAME>`.

After completing: confirm branch diff NON-EMPTY and pushed.
```

## 3. Note operative

- I 3 candidati Game code-health (unused import os, unused import sys,
  duplication flint_status_stdlib.py) sono **low-risk, fuori freeze-path**
  (`services/generation|rules|combat`) -- a differenza dei vecchi
  "function-too-long" su `services/generation/orchestrator.py` (= DEFER).
- Lancio raccomandato **uno alla volta** (R5 anti-noise; volume > review-rate
  = failure-mode #1). Post-PR: triage `jules-pr-triager` + ground-truth
  (session > PR, check `gitPatch` se diff vuoto, mai close silenzioso).
- Limite osservato: 0/100 sessioni/giorno, modello Gemini 3.1 Pro, piano PRO.
