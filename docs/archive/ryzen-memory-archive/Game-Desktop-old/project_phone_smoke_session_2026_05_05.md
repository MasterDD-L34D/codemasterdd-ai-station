# Phone smoke test session — 2026-05-05 FULL handoff (closure + audit handoff)

## Stato finale sessione

**11 PR Game/ + 3 PR Game-Godot-v2 merged main** in singola sessione. Phone smoke runtime userland ESEGUITO con master-dd → 5 bug critici trovati + fixati live iterativamente. Cutover Fase 3 ADR formal **PROPOSED** (PR #2055). Repo audit handoff doc **shipped** per next session.

## Phone smoke 2026-05-05 runtime — 5 bug bundle shipped

| Bug | Sintomo | Fix |
|---|---|---|
| **B1** | Phone Crea Stanza non mostra codice (view transitions immediato) | Share screen overlay con codice + deep-link + Continue CTA |
| **B2** | 30s grace troppo corto cross-device mobile | 30s → 90s + env override `LOBBY_HOST_TRANSFER_GRACE_MS` |
| **B3** | Host stuck MODE_WAITING senza UI advance phase | Bottone "Inizia mondo (host)" runtime in MODE_WAITING |
| **B4** | "Errore [unknown_type]: player_connected" toast cover-screen | Riconosci 3 presence events come info-only |
| **B5** | setPhase non trigger phone transition | `publishPhaseChange` versionato + composer `event_received` → swap mode |

**Verified live B1+B2+B3+B4** post-rebuild + master-dd retest. **B5 shipped post-build**, runtime-verify deferred.

## Smoke verdict CONDITIONAL

- ✅ WS lobby cross-device 2-phone end-to-end
- ✅ Lobby create + share screen + deep-link join
- ✅ JWT auth + tunnel + shared mode
- ✅ Presence broadcasts swallow (no error toast)
- 🟡 Phase transition runtime NOT-VERIFIED (B5 shipped, retest pending)
- ❌ Combat 5 round + p95 capture DEFERRED
- ❌ Airplane mode reconnect DEFERRED

## PR shipped tutti merged

| # | Repo | PR | SHA | Topic |
|---|---|---|---|---|
| 1 | Game | #2045 | (origin) | docs origin phone smoke step-by-step |
| 2 | Game | #2047 | (Codex P1+P2) | fix Codex review |
| 3 | Game | #2048 | `b3fbde5c` | gitignore `.env` + doc redirect upstream |
| 4 | Game | #2049 | (closed) | replaced by #2050 (base deleted post-#2048 squash) |
| 5 | Game | #2050 | `beec9bda` | drop MSYS workaround section |
| 6 | Game | #2051 | `5aba1fff` | drift Item 10 close-mark (phone smoke) |
| 7 | Game | #2052 | `e53368cd` | drift Items 1+2+Ennea close-mark |
| 8 | Game | #2053 | `97185317` | fix(ws): grace 30→90s + setPhase→publishPhaseChange + smoke results |
| 9 | Game | #2054 | `95aa60a5` | CLAUDE.md sync sprint context 2026-05-05 |
| 10 | Game | #2055 | `89e8481d` | **ADR-2026-05-05 cutover Fase 3 formal — Scenario 3 STAGED canary** |
| 11 | Game | NEXT | (handoff doc) | repo content audit handoff next session |
| 12 | Game-Godot-v2 | #168 | `e3efe53` | fix MSYS build_web + serve_local |
| 13 | Game-Godot-v2 | #169 | `ddacd860` | fix phone smoke 5-bug bundle (B1+B3+B4+B5) |
| 14 | Game-Godot-v2 | #170 | `2d45329d` | CLAUDE.md sync sprint context 2026-05-05 |

## Drift sync 2026-05-04 final status

| Item | Pre | Post |
|---|:-:|:-:|
| 1 M.7 p95 | 🟡 PARTIAL | 🟢 ENGINE+WIRE LIVE (#166) |
| 2 N.7 5/5 | 🟡 3/5 | 🟢 4/5 GATE 0 NEAR-PASS (CampaignState + LineageMergeService #165) |
| 3 Beehave | ✅ | ✅ |
| 4 Caller-wire | ✅ | ✅ |
| 5 Combat stubs | ✅ | ✅ |
| 6 Skiv asset | ❌ | ❌ (userland Path 3 ~6-9h) |
| 7 Cutover ADR | ❌ | ❌ depends Item 9 |
| 8 ERMES | ⏸ | ⏸ correct deferred |
| 9 Char creation TV | ❌ | ❌ dev ~6-10h |
| 10 Phone smoke | ⏸ | 🟡 GUIDA SHIPPED (~45 min userland) |
| Ennea drift | ❌ schema | ✅ RESOLVED (#167 + #2041) |

## Critical path Fase 3 cutover post-2026-05-05

~2-3h totale:
1. **Item 9 phone smoke** (~45 min userland, master-dd) — guida + tooling shipped
2. **Item 6 cutover ADR formal** (1-2h, post-results submission)

## Key infra discovery

`Game-Godot-v2/tools/deploy/deploy-quick.sh` shared mode supersede 3-port setup originale doc PR #2045:
- 1 sola porta 3334 (REST + WS + phone HTML5 same-origin, `LOBBY_WS_SHARED=true`)
- Auto AUTH_SECRET + build + mount + boot + Cloudflare Quick Tunnel
- ~30s subsequent runs
- `WebOriginResolver.gd` auto-detect via JavaScriptBridge

## Bug fixes Game-Godot-v2 PR #168

`tools/web/build_web.sh`:
- `$USER` unbound MSYS → bilingual `RESOLVED_USER="${USER:-${USERNAME:-}}"`
- `command -v "*.cmd"` fail MSYS → 6-candidate fallback chain `.cmd` + `.exe console` + `.exe windowed` via `$LOCALAPPDATA` + `/c/Users/$RESOLVED_USER/...`
- Helper `godot_resolve` uses `-f` not `-x` (Windows .cmd no exec bit)

`tools/web/serve_local.sh`:
- `path.join(ROOT, url).startsWith(path.resolve(ROOT))` relative-vs-absolute → 403 forbidden always
- Fix: pre-compute `ROOT_ABS = path.resolve(ROOT)` + `file = path.resolve(path.join(ROOT_ABS, url))` + guard `file.startsWith(ROOT_ABS + path.sep)` cross-platform

Smoke verified:
- `unset USER GODOT_BIN && bash tools/web/build_web.sh --mode=phone` → success 22M index.pck
- `serve_local.sh`: 200 root + index + CORS preserved + traversal blocked

## Resume command (single line, post-#168 zero env required)

```bash
cd /c/Users/VGit/Desktop/Game-Godot-v2 && bash tools/deploy/deploy-quick.sh
```

Stampa `https://<random>.trycloudflare.com/phone/` (subdomain ephemeral, cambia ogni run).

## Pre-flight 5/5 verified locale

- Godot 4.6.2.stable.official.71f334935 ✅
- export_presets.cfg preset.0 Web ✅
- Game-Godot-v2 main HEAD `e3efe53` (post #166 + #167 + #168) ✅
- cloudflared 2025.8.1 (winget installed) ✅
- npm deps Game/ ✅ + AUTH_SECRET in Game/.env (gitignored post #2048) ✅
- HTML5 build cached `dist/web/` 22M ✅

## Phone smoke test scenarios pending

Doc canonical: [`docs/playtest/2026-05-05-phone-smoke-step-by-step.md`](https://github.com/MasterDD-L34D/Game/blob/main/docs/playtest/2026-05-05-phone-smoke-step-by-step.md)

- **5a** iOS Safari → lobby create → 4-letter code (~5 min)
- **5b** Android Chrome → join `/phone/?room=XXXX` → world setup vote (~5 min)
- **5c** Combat enc_tutorial_01 → 5 round play + p95 capture (~20 min)
- **5d** Airplane mode 5s → reconnect verify state preserved (~5 min)

Verdict gate Sprint M.7:
- p95 <100ms PASS ✅
- 100-200ms CONDITIONAL ⚠️
- >200ms ABORT ❌

`TelemetryCollector` running per action (#166 wired in main.gd line 578+718). Read p95 via console `print(_telemetry.compute_p95_ms())` (debrief HUD surface NOT wired yet, fallback OK per smoke).

## Post-smoke action

1. Compile `docs/playtest/2026-05-XX-phone-smoke-results.md` con verdict template + bug + UX impressions
2. PR submit results doc → Item 10 final close-mark
3. Item 6 cutover ADR formal draft (master-dd + dev, 1-2h) → cutover Fase 3 approved se results PASS or CONDITIONAL accettato

## Next session — repo content audit (handoff doc shipped)

**Handoff doc canonical**: [`docs/planning/2026-05-05-repo-content-audit-handoff.md`](../../../../Desktop/Game/docs/planning/2026-05-05-repo-content-audit-handoff.md)

**Scope**: scan systematic Game/ + Game-Godot-v2 → identify:

- Dead code (zero callers)
- Stub registry triage (Tier 1/2/3)
- Engine LIVE Surface DEAD violations (Gate 5 anti-pattern)
- YAML data orphan (defined no consumer) + hardcoded runtime missing YAML
- Unused asset references

**Methodology**:

- **Phase 1** (~2h autonomous): 3 agent parallel — `repo-archaeologist` Game/ + Godot v2 + `balance-illuminator` cross-stack
- **Phase 2** (~1h autonomous): live runtime probe via `deploy-quick.sh` + curl + trait fire log
- **Phase 3** (~1h master-dd verdict): triage decision matrix + 1-3 cleanup PR

**Deliverable**: 3 report docs + 1-3 cleanup PR (dead code delete + stub registry rationalization + Gate 5 violation closures).

**Pre-cutover Phase A repo state target**: lean + intentional + zero ghost.

## Pending USERLAND PARALLEL (does NOT block audit)

1. Master-dd phone smoke retry (~30 min) — verify B5 + combat 5c + airplane 5d → unblocks Phase A trigger
2. Phase A ACCEPTED verdict (post-retry)
3. Phase B trigger 7gg grace + 1+ playtest

**Default 14gg** (2026-05-19): Phase A ACCEPTED ASAP + Phase B 7gg grace + S5 playtest only.

## Resume next session — repo audit (autonomous)

```bash
cd /c/Users/VGit/Desktop/Game-Godot-v2 && bash tools/deploy/deploy-quick.sh
```

Smoke retry scope (~30 min):

1. Crea Stanza Android → vedi share screen (B1 verified)
2. Unisciti iOS deep-link `?room=XXXX` (B4 no error toast)
3. Tap "Inizia mondo (host)" Android → **VERIFY** entrambi phone transitionano MODE_CHARACTER_CREATION (B5 runtime test pending)
4. Continue scenario tutorial → 5 round combat
5. Capture p95 via Godot console `print(_telemetry.compute_p95_ms())` (debug HUD widget non shipped, console fallback OK)
6. Airplane mode 5s test reconnect

Then submit results addendum + close-mark drift sync Item 10 final → Cutover Fase 3 ADR formal.

## Trigger phrase resume

**Audit autonomous** (raccomandato next session — no userland dep):

> "leggi docs/planning/2026-05-05-repo-content-audit-handoff.md, esegui Phase 1 static scan 3 agent parallel su Game/ + Game-Godot-v2"

OR

> "resume repo content audit 2026-05-05, audit stub registry + Engine LIVE Surface DEAD + YAML orphan"

**Userland parallel** (smoke retry, master-dd):

> "resume phone smoke retry 2026-05-05, verify B5 phase transition runtime + combat 5 round p95"
