# BACKLOG

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/04_BOOTSTRAP_KIT/BACKLOG.md` + sezione "Primo sprint consigliato" inline.
>
> Normalizzato da: follow-up ADR non chiusi + "Da fare" JOURNAL recenti + criteri closure ADR-0014 + bug noti aperti.

## Snapshot 2026-05-28 (player-recap)

**Stato sezioni**:
- **Priorita' alta**: H1-H12 chiuse (12/12 ✅). 4 item "open" -> **TUTTI superseded/satisfied** 2026-05-28 (H2 dogfood n=36 surpasses n>=10 target; H3 cp1252 satisfied empirical n=36 zero retry-loop > n=15 threshold; H7 ADR-0023 superseded by ADR-0030 Hybrid A1).
- **Priorita' media**: M1-M14 mostly chiusi. Residui = **M3 closed-never-triggered** (H3 satisfied), **M5 dormant** (Synesthesia UniUPO ago 2026), **M14 deferred** Eduardo-direct.
- **Priorita' bassa**: L1-L5 opportunistic, keep-with-trigger.
- **ADR-0017 rollout**: 5/6 chiusi. **U0-test aider --browser** open.
- **Bloccato da**: B1-B3 tutti chiusi 2026-05-28 (Fase 6 closure done 2026-05-07 + ADR-0030 pivot Accepted 2026-05-18 supersede Fase 7 budget transition).
- **SPRINT_02**: T1/T3/T4/T8 ✅ done; T2 ✅ surpassed (n=36 vs target n>=20); T5/T6/T7 in-flight (sprint window 19/06).
- **X cross-repo orchestrator**: X1/X2 ✅; X3/X4/X5 Gate E window post-Max (now Hybrid A1 covers strategic; window relevance to re-evaluate post-2026-06-17 Max-2 expiration).

**Cose che devi fare adesso**:
- **U0-test** (~10min): prova aider --browser per 1-2 dev-loop session. Gate UX accettabile -> ADR-0017 step 1+ deferred.
- **M5 Synesthesia**: dormant UniUPO -- riapri ago 2026.
- **M14 AA01 Task D**: Eduardo-direct, vault Card 3/4 (sibling-peer boundary, non codemasterdd action).
- **L1-L5**: opportunistic, no action proattiva.
- **SPRINT_02 T5/T7**: end-sprint review entro 19/06.

Pattern di chiusura applicato post `superpowers:first-principles-infra-checklist` cleanup OPEN_DECISIONS: marker stale = anti-pattern #19 -> ground-truth verify (log conteggi + ADR status + sprint scope) prima di assumere "open".

---

## Priorità alta

- [x] ~~**H1** — Dogfood behavior-critical n+1 (target ≥5).~~ **DONE 2026-04-24 auto-mode**: #12 retry-logic parity bench-ollama (14B Q2 local), partial success con inherited-bug finding. Dataset behavior: 3 full + 1 partial + 1 reject = **5/5 target ✅**. Commit `dce8ee4`.
- [x] ~~**H2** — Dogfood cosmetic fino n≥10 cumulativo (attuale 7 dopo #11).~~ **DONE 2026-05-28 (SURPASSED empirical)**: dogfood cumulative n=36 (entries logs/aider-delegation-2026-04 + 2026-05). Target n>=10 cosmetic surpassed 3.6x via natural workflow accretion. SPRINT_02 T2 ratification (~13/5 notte).
- [x] ~~**H3** — Monitoring empirico fix cp1252 durante retry loop naturale.~~ **DONE 2026-05-28 (SATISFIED empirical, threshold n=15 surpassed 2.4x)**: cumulative n=36 dogfood post-fix-deploy, zero UnicodeEncodeError crash, zero natural-retry-loop trigger osservato. Soglia pazienza ADR-0014 (n=15) surpassed -> fix `chcp 65001 + PYTHONIOENCODING=utf-8` ratified empirical. Closes OD-002 (gia' closed 2026-05-07) loop. Reactivation trigger: 1° crash UnicodeEncodeError post-deploy (none observed).
- [x] ~~**H4** — Cost tracking cumulativo mensile `ccusage` + cloud logs.~~ **DONE 2026-04-24 auto-mode** (anticipato vs target fine-mese): sezione "Aggregati aprile 2026" popolata in `logs/aider-delegation-2026-04.md`. Cumulative cloud $0.0148 / 0.074% budget. ccusage Max $383.36 (non-OOP). Trigger ADR-0008 FULL-SOVEREIGN VIABLE confermato empiricamente. Refresh finale fine-mese (2026-04-30) residuo tracked.
- [x] ~~**H5** — Review settimana 2 formale (~2026-05-07): count dogfood, fail rate, ETA chiusura. Decisione on-track / extension.~~ **DONE 2026-04-24 (anticipata)**: sprint 01 early-hit ha reso review immediata sensata. Esito: **on-track, no mid-course correction**. 2/4 criteri ADR-0014 PASS (quality, cost), 2/4 on-track (reliability 11/20, privacy 1/3). Next checkpoint settimana 4 (~2026-05-17). Dettaglio in JOURNAL entry `2026-04-24 (review settimana 2 anticipata)`.
- [x] ~~**H6** — Validare empiricamente OD-006 (routing threshold constraint-count).~~ **DONE 2026-04-24**: n=6 data points cross-tier raccolti (dogfood #6/#7/#8/#9/#10/#11). OD-006 **chiuso via ADR-0016** (Proposed 2026-04-24). Follow-up: raccogliere n≥3 data points addizionali per gap (constraint=4, 2-transform LOCAL, 5-strict LOCAL) verso ADR-0016 Accepted.

### Task derivati da harsh review 2026-05-09 (Decisione 007)

- [x] ~~**H7** -- ADR-0023 strategic tier post-Max API on-demand.~~ **DONE 2026-05-28 (SUPERSEDED by ADR-0030 Hybrid A1, Accepted 2026-05-18)**: ADR-0023 originale supposeva "senza Pro $240/anno"; ADR-0030 ha acquisito Pro $20/mo -> strategic tier ora covered by Pro subscription, NON pay-per-use API on-demand. ADR-0023 status = SUPERSEDED-by-ADR-0030. Action items chiusi: `logs/claude-api-spend-2026-05.md` esiste; CLAUDE.md aggiornato (sezione 6 + 16 cita Hybrid A1 + ADR-0030).
- [x] ~~**H8** -- Privacy guard rail tecnico (V2 BLOCKING resolution).~~ **DONE 2026-05-09 mezzogiorno**: 4 wrapper cmd cloud (aider-groq/cerebras/gemini/openai) modificati con runtime check `git rev-parse --show-toplevel` + whitelist `~/.config/aider-privacy-whitelist.txt`. Test smoke: codemasterdd ALLOWED (exit 0) + synesthesia BLOCKED (exit 1) entrambi PASS. Setup script `scripts/setup/install-privacy-guard.ps1` (idempotente) + template wrapper `scripts/setup/aider-wrapper-template.txt`. CLAUDE.md aggiornato. **Effort reale: ~1h** (vs stima 1gg).
- [x] ~~**H9** -- Bench mixed-workload pre-19/05 (C1 + V3 sample size).~~ **DONE 2026-05-09 mezzogiorno** (commits `cbdf2ed` + `11cac69`): bench n=4 per tier 7B/14B Q2/30B MoE con 11 swap forced. Risultati: workflow time 79.17s (11 swap), throughput per-tier 100.75 / 17.62 / 32.98 tok/s, swap overhead 3047ms/swap = 42.3% del workflow misto. **Discovery positiva**: qwen3-coder:30b MoE A3B 32.98 tok/s (+43% upside vs doc precedente), competitive con 14B Q2 in throughput + capability superiore. Mitigation batched (run [4x7B -> 4x14B Q2 -> 4x30B]) saving 37% (49.9s con 2 swap). Decisione `OLLAMA_MAX_LOADED_MODELS=1` confermata (validation contrarian `=2` non payoff). Doc: `docs/research/bench-mixed-workload-2026-05-09.md` + `bench-batched-2026-05-09.md`. CLAUDE.md aggiornato con tabella mixed-workload + raccomandazione batching. Effort reale: ~3-4h.
- [x] ~~**H10** -- ADR status workflow update con flag "early-acceptance".~~ **DONE 2026-05-09 mezzogiorno**: ADR-0010 addendum (status workflow + early-acceptance flag spec + ratification check process). ADR-0021 + ADR-0022 retroactive flag applicato. DECISIONS_LOG ADR table sync. Ratification check date: ADR-0021 entro 2026-06-07 / ADR-0022 entro 2026-06-09. Effort reale: ~30min.
- [x] ~~**H11** -- Eduardo direct: attiva AA01 silent-driver mode su Sprint Impronta Ondata 1+2 status-phase-a.~~ **DONE 2026-05-09 sera (chiuso come superseded by reality)**: reality check ha rivelato che PR Game #2138 + #2139 sono **GIÀ MERGED** (memory v14 era stale, indicava DRAFT). Body PR #2138 menziona "design call 2026-05-09" -> work Ondata 1+2 status-phase-a completato organicamente via Claude Code session diretta (NON AA01-mediated). Audit AA01 workspace: 2 task PROPOSED del 25/04 (#001 voice-test-protocol-dafne + #002 day5-post-session-ritual) erano **STALE one-shot reactive** (eventi 25-26/04 passati 13gg fa). Action eseguita: 2/2 task archived con status=TIMEOUT (no SHIP gate richiesto), workspace pulito 0 attivi, INDEX.md aggiornato 3 entries, archive readonly. Eduardo manual residuo: zero (silent-driver Ondata 1+2 superseded). Effort reale: ~30min (audit AA01 + archive 2 task).
- [x] ~~**H12** -- Stop hook automatico per JOURNAL/COMPACT/memory drift mitigation (C3 risoluzione).~~ **DONE 2026-05-09 mezzogiorno**: 2 PowerShell hook scripts + .claude/settings.json (project-level) + .gitignore fix. Hook SessionStart salva HEAD in `.claude/.session-start-head`. Hook Stop compara HEAD attuale vs marker, se cambiato emette systemMessage con summary commit + reminder JOURNAL/COMPACT update. Test smoke: HEAD invariato silent ✅, HEAD changed emette systemMessage 3 commit summary PASS ✅. Skill `update-config` invocata. Effort reale ~45min vs stima 30-60min.

### Task derivati da harsh review (deferred SPRINT_02 / opportunistic)

- [x] ~~**M7** -- Backup automation API keys daily rotation (V4 mitigation).~~ **DONE 2026-05-09 sera**: `scripts/backup-api-keys.ps1` (~160 righe). Daily snapshot di `~/.config/api-keys/keys.env` -> `backup/api-keys/api-keys-YYYY-MM-DD.env` (gitignored via `backup/*`), idempotent (overwrite intra-giorno), retention configurable (default 30gg con cleanup automatico). Encryption opt-in via `-Encrypt` (DPAPI ConvertFrom-SecureString, user+machine bound, suffix `.env.enc`). ACL strict best-effort (graceful fallback a inherited se non admin -- SeSecurityPrivilege required). Integrity check round-trip post-write per entrambi i mode. Smoke 3/3 PASS: plain + encrypted (decrypt round-trip) + rotation 2-files-removed. Schedule daily 03:00: `schtasks /Create /SC DAILY /TN ApiKeysBackup /TR "powershell -File C:\dev\codemasterdd-ai-station\scripts\backup-api-keys.ps1 -Quiet" /ST 03:00`. Recovery procedure documentata in header (DPAPI decrypt snippet). Effort reale: ~30min (con 1 fix iter: ACL graceful fallback per non-admin run).
- [x] ~~**M8** -- Hook integrity smoke test settimanale (V4 mitigation).~~ **DONE 2026-05-09 sera**: `scripts/smoke-test-hooks.ps1` (~210 righe). 12 test cases: 5 commit-msg ADR-0011 (valid + missing type + >72ch + trailing period + uppercase) + 3 silent-corruption ADR-0008 (filename only + `# filename` + normal) + 4 silent-fail Python ADR-0020 (bare except + except:pass oneliner + bypass `# silent-ok` + logged except). Pattern: 1 scratch repo per test in `$env:TEMP/hook-smoke-$PID/` per evitare staging cross-contamination, cleanup garantito via try/finally. Smoke 12/12 PASS confermati. Modes: full + `-Quiet` (CI summary only) + `-ExitOnFail` (stop al primo fail). Schedule weekly: `schtasks /Create /SC WEEKLY /D SUN /TN HookIntegritySmoke /TR "powershell -File C:\dev\codemasterdd-ai-station\scripts\smoke-test-hooks.ps1 -Quiet" /ST 09:00` (Eduardo manual install). Effort reale: ~40min (con 2 fix iter: PS5.1 stderr 2>&1 wrapping + 1-repo-per-test isolation).
- [x] ~~**M9** -- Tooling `task-classify <file> <description>` per ridurre cognitive overhead decision tree (C2 risoluzione).~~ **DONE 2026-05-09 sera**: `scripts/task-classify.ps1` (~210 righe) implementa decision tree CLAUDE.md + ADR-0008/0016/0022. Mode interactive (5-6 domande con default + colored hints + Set-Clipboard) + parametric (`-Quiet` per pipe/test). 9/9 smoke PASS coprendo: cosmetic locale/cloud/cerebras, behavior locale/groq/borderline-4-constraint, multi-step opencode, cosmetic-subdir-self-ref mitigation, strategic short-circuit, constraints>=5 short-circuit. Install globale Eduardo manual: `Copy-Item scripts/task-classify.ps1 ~/.local/bin/` + `.cmd` wrapper. Effort reale: ~25min.
- [x] ~~**M10** -- Bench OpenCode + Groq con `--max-tokens` ridotto (E3 risoluzione).~~ **DONE 2026-05-09 sera**: bench empirico n=3 conclusivo, ADR-0022 finding **CONFERMATO**. Test runner `scripts/bench-opencode-cloud-free.ps1` + research doc `docs/research/bench-opencode-cloud-free-2026-05-09.md`. **Risultati**: T1 groq/llama-3.3-70b TPM 12000 vs OpenCode richiesto 49698 token (1st) + 32438 (retry) BLOCKED -2.7x..-4.1x; T4 cerebras/llama3.1-8b ctx 8192 vs richiesto 12228 BLOCKED -1.5x; T3 groq/qwen-2.5-coder-32b DECOMMISSIONED. **Discovery flag**: nessun `--max-tokens` esposto da OpenCode `run` (ipotesi M10 originale invalidata -- no knob disponibile per limitare INPUT context da CLI). **Side-action eseguita**: `~/.config/opencode/opencode.json` refresh, rimosso `qwen-2.5-coder-32b` deprecated dal provider Groq. **Decisione**: ADR-0022 status invariato (no addendum), pattern OpenCode = sovereign-only confermato cross-provider. Future trigger -> nuovo task L6 BACKLOG (plugin custom o tool-set trim) solo se gpt-4o-mini emergency budget eccessivo. Effort reale: ~1h (con 2 fix iter: PS5.1 Start-Process `+` array bug + hang inline workaround diretto bash+timeout).

## Priorità media

- [x] ~~**M1** — JOURNAL entry 2026-04-23 documentando integrazione framework archivio + 11 file governance + rationale.~~ **DONE**: entry in JOURNAL `2026-04-23 (sera — integrazione framework archivio)` + follow-up `2026-04-24 notte` aggiunta.
- [x] ~~**M2** — Memory refresh `project_session_resumption.md`.~~ **DONE 2026-04-24**: HEAD 9bcc2a4, tabella 11 dogfood, ADR-0016 reference, Sprint 01 early hit.
- [x] ~~**M3** — Wrapper PowerShell alternative (`aider-groq.ps1` etc.) **se H3 fallisce**.~~ **CLOSED-NEVER-TRIGGERED 2026-05-28**: H3 satisfied empirical (n=36 zero crash, threshold n=15 surpassed). Conditional trigger ("1° crash cp1252 post-deploy fix") MAI attivato. Closing definitively. Reactivation: solo se crash UnicodeEncodeError reale emerge in future workflow.
- [x] ~~**M4** — Integrate bench framework ↔ dogfood tracking: colonna "quality pass" nel log.~~ **DONE 2026-04-24**: insight = "colonna per-entry" non ha senso (quality bench è per-modello fisso). Implementato come reference table aggregata: template esteso con sezione "Quality bench ↔ reliability correlation" + diagnostic patterns. Log reale popolato con snapshot (5 stack al 100% pass@1 vs reliability variabile → conferma constraint-specific fail mode ADR-0016). Commit `70f4f69`.
- [ ] **M5** — Synesthesia privacy first-violation test: ≥1 sessione che tocchi `views/` (cloud OK) + `controllers/` (sovereign-only). Criterio 3 ADR-0014. **Priorità residua principale Sprint 01** (1/3 ancora).
- [x] ~~**M6** — Commit delle 11 modifiche governance + entry JOURNAL.~~ **DONE 2026-04-23/24**: 11 commit sessione cumulative (sera + notte).

### Task derivati da OCR screenshot wave 2026-05-12 (Eduardo trigger 12 top Claude Code repos)

- [x] ~~**M11** — AA01 Task A: skills collection evaluation~~ **PARTIAL DONE 2026-05-12 pomeriggio+tardo**: #3 obra/superpowers v5.1.0 **INSTALLED** PR #59 (Archon CALIBRATE 7-step + falsifying experiment 5/5 PASS) + #10 anthropics/skills **MARKETPLACE REGISTERED** PR #62 (17 skills bundle native accessible session). Residual Eduardo-direct **CHANGED 2026-05-12 sera re-eval calendarizzati** (allinea anti-pattern L-2026-05-002 audit churn + L-2026-05-011 dormancy workflow-driven): #1 affaan-m **DEPRECATED 1-week artificial deadline** -> trigger-condition organic (gap-emerge durante real use), monitor passivo via SPRINT_02 T8.2 superpowers skill auto-trigger observation. #5 Karpathy AUDIT-ONLY mantained (NO LICENSE blocker default copyright). Lesson L-2026-05-008 promoted + L-2026-05-013 re-eval calendarizzati pattern (in promotion).
- [x] ~~**M12** — AA01 Task B: subagent + memory~~ **DONE 2026-05-12 pomeriggio**: #4 thedotmack/claude-mem v13.2.0 **INSTALLED** PR #61 (Archon CALIBRATE PIVOT 3 blocker auto-resolved: Bun runtime + hook collision empirical NO conflict + privacy SAME-TIER). Lesson L-2026-05-009 promoted. Bun v1.3.13 pre-req installato. Worker port 37777 + 6 hook lifecycle attivi. **Bundle 1 B6 smoke verify 12/5 sera**: NO collision project-scope + workflow PASS.
- [x] ~~**M13** — AA01 Task C: dev-tools~~ **DONE 2026-05-12 mattina+pomeriggio**: #7 yamadashy/repomix v1.14.0 **INSTALLED** PR #58 via `npm install -g repomix`. Smoke test PASS (`docs/sessions/** + docs/aa01-handoff/**` pack 41886 bytes 12.160 tokens). #8 gsd-build/get-shit-done BOOKMARK reference comparativo vs AA01 (no install).
- [ ] **M14** — AA01 Task D: guides + awesome + design. **PARTIAL DEFERRED** Eduardo-direct: #2 + #6 + #12 vault Card 3/4 sibling-peer boundary pending. #9 dair-ai/Prompt-Engineering-Guide REFERENCE_INDEX link bookmark candidate.

### Task derivati da session 2026-05-12 sera (Bundle 1+2+3 cluster)

- [x] ~~**B1** — Memory drift fix `project_vault_shared.md` 6/7 → 7/7 PRODUCTION milestone hit.~~ **DONE 2026-05-12 sera Bundle 1 PR #63**. HEAD vault `2007a8a2` 7/7 PRODUCTION milestone confirmed empirical.
- [x] ~~**B2** — COMPACT_CONTEXT v21 → v22 drift fix.~~ **DONE 2026-05-12 sera Bundle 1 PR #63**. 13 PR drift + plugin ecosystem MAJOR upgrade + AA01 state aggiornato.
- [x] ~~**B4** — Reflexive ADR-0026 effectiveness audit.~~ **DONE 2026-05-12 sera Bundle 2 PR #64**. Research doc + 3 caso studi HIGH/HIGH/MEDIUM + 3 gap mitigation + ratification empirical support. ADR-0026 **Accepted ratificato auto 12/5 sera**.
- [x] ~~**B5** — Aider wrappers privacy guard rail smoke re-verify.~~ **DONE 2026-05-12 sera Bundle 1 PR #63**. 4/4 scenari PASS (codemasterdd+Game ALLOW, vault+synesthesia BLOCK).
- [x] ~~**B6** — claude-mem plugin post-install smoke + hook collision verify.~~ **DONE 2026-05-12 sera Bundle 1 PR #63**. Worker port 37777 ALIVE + NO collision project-scope.
- [x] ~~**B7** — Sub-agent ecosystem effectiveness review.~~ **DONE 2026-05-12 sera Bundle 3 PR #65**. 18 sub-agent (12 ready + 6 draft) + 9/12 smoke + 6 dormant workflow-driven. Research doc + 4 REC.
- [x] ~~**B8** — Hook chain effectiveness empirical smoke.~~ **DONE 2026-05-12 sera Bundle 3 PR #65**. 5 layer 5/5 PASS + 10/10 component checks cumulative cross-bundle. Research doc + 4 REC.
- [x] ~~**V1** — Vault handoff doc Eduardo-direct (sibling-peer boundary respected).~~ **DONE 2026-05-12 sera Bundle 1 PR #63**. Doc `docs/aa01-handoff/2026-05-12-vault-frontmatter-drift-handoff.md` (frontmatter drift 7/7 + CLAUDE.md drift 5-claim + README discoverability). Eduardo-direct action 30-45min one-shot.
- [x] ~~**V3** — MODEL_ROUTING Quality Gate cross-pattern adoption research.~~ **DONE 2026-05-12 sera Bundle 2 PR #64**. Research doc + 4 REC. **ADR-0028 Tier promotion methodology Quality Gate Step 2 DRAFTED Proposed 2026-05-13 notte tarda** (Eduardo override defer SPRINT_02+ Three Strikes trigger, V3 REC 4 originally DEFER). Trigger Accepted: 3-condition Three Strikes in ADR-0028 (1 regress + 1 successful manual application + 1 emergent tier promote request). MODEL_ROUTING.md section formal write deferred post-Accepted (REC 2).

### ADR ratification 2026-05-12 sera auto (residual cluster)

- [x] ~~**ADR-0025 Hyperspace Pods NO-GO**~~ **Ratified Accepted 2026-05-12 sera auto** via Eduardo authorization. Empirical support: D-017 99% confidence + pktmon evidence + L-2026-05-002.
- [x] ~~**ADR-0026 Cognitive workflow protocols**~~ **Ratified Accepted 2026-05-12 sera auto** via Eduardo authorization. Empirical support Bundle 2 reflexive audit (cite density + 3 caso studi HIGH + reflexive validation questa sessione).

### Re-eval calendarizzati 2026-05-12 sera (Eduardo "procedi con metodo")

Applicato Protocol 1 Refresh-verify + Protocol 2 Autoresearch ai 4 calendarizzati Eduardo-direct post cluster 12/5 sera. Shift approccio strategico: **deadline-driven -> trigger-emergent** + boundary respect cross-repo.

- [x] ~~**H7 ANTHROPIC_API_KEY** (pre-19/05)~~ **CONFIRMED 2026-05-12 sera re-eval**. Empirical evidence 49 PR/6gg pre-Max session rafforza razionale ADR-0023 tier 0 strategic. Action invariato (Eduardo-direct ~5min). Pre-19/05 mantained.
- [x] ~~**M11 #1 affaan-m post 1-week monitor**~~ **CHANGED 2026-05-12 sera re-eval**: deprecate 1-week artificial deadline (anti-pattern L-002 churn + L-011 dormancy workflow-driven OK) -> trigger-condition organic (gap-emerge real use). Monitor passivo via SPRINT_02 T8.2 superpowers skill auto-trigger observation.
- [x] ~~**Phase B Day 7 closure 2026-05-14**~~ **REMOVED 2026-05-12 sera re-eval**: Game-autonoma action (governance interna autosufficiente), codemasterdd osservatore passivo (memoria + CLAUDE.md "NON sovrascrive monitora solo"). Allinea L-2026-05-012 boundary cross-repo.
- [x] ~~**SPRINT_02 prima sessione 2026-05-20+**~~ **RETAINED + AMENDED 2026-05-12 sera re-eval**: scope refinement con cluster questa sessione findings (plugin ecosystem MAJOR + 12 lessons + ADR-0026). Aggiunti T8 plugin ecosystem dogfood + T9 methodology framework effectiveness post-Max + T10 Three Strikes Quality Gate trigger.

**Lesson cumulative pattern**: L-2026-05-013 (in promotion) -- "Re-eval calendarizzati pattern: deadline-driven -> trigger-emergent shift via Protocol 1+2 application".

### Task derivati da PR #69 harsh-review 2026-05-12 notte

Applicato ADR-0026 P1 Refresh-verify + P2 Autoresearch multi-source + skill `superpowers:requesting-code-review` (harsh-reviewer subagent) su PR cross-PC drift fix. 5 finding actionable + 1 pushback documentato. P3 Archon SKIP (no irreversible high-stakes); P4 AA01 SKIP (consistent L-002).

- [x] ~~**R1** -- Q2 Game canonical clone decision (fuse trigger BEFORE next Lenovo write).~~ **RESOLVED 2026-05-13 notte via ADR-0027 P1 Refresh-verify**: claim PR #69 "Ryzen AHEAD" era narrative drift L-2026-05-002 case-study. Reality empirical: Ryzen `Desktop\Game` HEAD `5d27fc50` PR #2139 OLDER, **0 ahead / 107 BEHIND origin/main**, dirty working tree (apps/backend/* deletions). Origin canonical de-facto, Lenovo synced primary client. NO ADR architectural needed. Cleanup Ryzen sandbox BACKLOG C1 low-priority.
- [x] ~~**R2** -- DHCP reservation router per Lenovo + Ryzen (kill IP drift class permanente).~~ **DONE 2026-05-13 notte**: TIM HUB DGA4132 AGTHP firmware reservation salvata via Metodo A (reservation FUORI DHCP pool `.100-.200`). Lenovo `e8:bf:e1:18:81:ca` -> `192.168.1.10` + Ryzen `d8:43:ae:b7:c4:e5` -> `192.168.1.11`. Post-reboot gateway, entrambi device sync immediato. Drift class permanently killed. **L-002 lesson applied empirical**: prima Eduardo intervened "non funziona", autoresearch web 6 search + 1 fetch ha rivelato TIM AGTHP firmware quirk (rifiuta save se IP in lease pool E currently leased) + workaround forum-validated (reservation outside DHCP pool). Pattern: **autoresearch FIRST per problemi technical specifici, NOT trial-and-error**. Promosso a lesson candidate L-2026-05-014 (in promotion).
- [x] ~~**R3** -- Ryzen `core.hooksPath` install.~~ **DORMANT 2026-05-13 notte via ADR-0027 empirical**: Eduardo NON commitica codemasterdd da Ryzen (clone su `codex/structural-reset` branch stale 6 ahead, non main, non active). Commit codemasterdd avviene Lenovo-side con hookPath globale attivo. Trigger reactivation: se Eduardo inizia commit codemasterdd Ryzen-side (futuro Q1 amendment), allora install hooksPath. Currently NO active trigger.
- [x] ~~**R4** -- Aider privacy whitelist Ryzen propagation (ADR-0023 H8 enforcement).~~ **DONE 2026-05-13 notte**: scp Lenovo `~/.config/aider-privacy-whitelist.txt` -> Ryzen `~/.config/aider-privacy-whitelist.txt` (1314 bytes), poi appended Ryzen path equivalents (3 mirror Lenovo policy: codemasterdd + Game + Game-Godot-v2 Ryzen paths). 9 Ryzen-only repos marked DEFAULT SOVEREIGN pending Q3 SPRINT_02 outcome. Vault Ryzen origin explicit exclusion. Total file 2295 bytes, 6 active entries. Trigger soddisfatto: Aider session Ryzen ora enforce-ready.
- [x] ~~**R5** -- Vault `Extras/config/llm-routing.json` IP update.~~ **DONE 2026-05-13 notte**: vault HEAD `1abaa743` "fix(routing): lenovo ollama ip 121 -> 10 post dhcp reservation". File now `"endpoint": "http://192.168.1.10:11434"` (post R2 DHCP reservation Lenovo locked `.10`). Sync 3-way: Ryzen + Lenovo + origin/main all at `1abaa743`. L-012 per-task auth pattern executed end-to-end: codemasterdd Claude Code edited+committed via SSH on Ryzen vault clone (boundary respected: single target file staged + Pathfinder dirty file preserved); wincredman blocked push non-interactive -> Eduardo-direct local push `cd C:\Users\VGit\Vault && git push origin main` ~30s; Lenovo `git pull --ff-only` synced read-only.

**Pushback documentato**: harsh-review #1 ASCII em-dash policy (5 em-dashes in new body prose CLAUDE.md:100/142/160/178/183). PUSHBACK applicato: ADR-0021 distingue "nuovi doc" strict vs "convention progetto" preserve. CLAUDE.md è long-running file con dozzine di em-dash storici (linee 1, 8, 13, 36, 42, 63-67, 96-99, 114-128, ...); switchare a `--` mid-file creerebbe inconsistenza, NON la fixerebbe. Eduardo approved 12/5 notte. Action: nessun fix em-dash.

### Task derivati da auto-mode session 2026-05-13 notte (post Phase 1 R2/R4/R5 closure)

ADR-0026 Protocol 1 Refresh-verify ha SHORT-CIRCUITED Archon 7-step needs per Q1/Q2/Q3/R3. Tutti resolved senza deep analysis (~3h Opus saved). Cleanup candidates aggiunti low-priority.

- [x] ~~**C1** -- Ryzen `Desktop\Game` sandbox cleanup.~~ **DONE 2026-05-21 (stale-resolved)**: `C:\Users\VGit\Desktop\Game` verificato GONE (consolidation a `C:\dev\Game` via OD-049 2026-05-19 rimosse il sandbox Desktop). Opzione (b) effettivamente avvenuta. No residuo.
- [x] ~~**C2** -- Ryzen `Desktop\repos\codemasterdd-ai-station` Codex branch cleanup.~~ **DONE 2026-05-21 (stale-resolved)**: `C:\Users\VGit\Desktop\repos\codemasterdd-ai-station` verificato GONE (consolidation C:\dev). Sandbox Codex `codex/structural-reset` rimosso col path. No residuo.
- [x] ~~**Q3-update** -- Add 5 active Ryzen-only repos a STATUS_MULTI_REPO.md.~~ **DONE 2026-05-21**: aggiunti 5 row snapshot table (Game-Database, claude-supermemory-local, compass-marketplace, Master-DD-Pathfinder-GPT, torneo-cremesi-site). 4 dormant (Gpt, Item-generator, LeaD, pathfinder-1e-homebrew) left silent per design. Informational.

## Priorità bassa

- [ ] **L1** — Re-bench discriminant hard problems custom (non-Leetcode). Fuori scope Fase 6.
- [ ] **L2** — Deepseek-r1 num_predict=5000 + extract thinking migliorato. Diminishing returns.
- [ ] **L3** — Cerebras paid tier evaluation (gpt-oss-120b, qwen-3-235b). Trigger: gap quality reale.
- [ ] **L4** — Gemma 4 multimodal dogfood reale. Opportunistic.
- [ ] **L5** — Skill install policy audit periodico (cadence 3 mesi).

## ADR-0017 rollout (Sprint 02, aperto 2026-04-24)

- [x] ~~**U0-scaffold** — Stack scaffolding completo (code + config + docs)~~ **DONE 2026-04-24 auto-mode maratona**: `infra/` + `scripts/quality-bench/promptfoo.*` + `apps/dogfood-ui/` + `.claude/agents/*` (5 sub-agent). 31 file nuovi, ~2700 LOC validati (Python AST + YAML parse + docker-compose config OK). Commit `6924482`. Eduardo può avviare stack quando pronto.
- [ ] **U0-test** — Step 0 quick-win: abilita `aider --browser`, prova 1-2 sessioni dev-loop. Gate: UX accettabile? Se sì → procedi. Se no → deferred step 1+.
- [x] ~~**U1-test** — Step 1 LiteLLM Proxy live infrastructure~~ **DONE 2026-04-24/25 sessione successiva auto-mode**: container `codemasterdd-litellm` UP 6h+, `/health/readiness` 200 (DB connected, success_callback `langfuse` attivo + 8 altri hook, v1.82.6). Config `infra/litellm/config.yaml` espone 10 modelli (7 local + 3 cloud free + 1 cloud paid) + master key via env + budget cap 50$/30d. **Gap residuo**: creazione virtual key via admin UI (`http://localhost:4000/ui`) richiede azione manuale Eduardo pre U3-test eval.
- [x] ~~**U2-test** — Step 2 Langfuse live~~ **DONE 2026-04-24/25**: container `codemasterdd-langfuse-web` UP 6h+, `/api/public/health` 200 (v2.95.11). Callback LiteLLM → Langfuse validato (7+ traces + 7 observations persistiti in Postgres durante sessione maratona). **Gap residuo**: creazione project + API key via UI (`http://localhost:3000`) se si vuole dashboard separato per queries.
- [x] ~~**U3-test** — Step 3 promptfoo live~~ **DONE 2026-04-25 insieme con Eduardo**: virtual key `dogfood-ui` creata via `http://localhost:4000/ui/` (Max Budget $5, 30d reset). Configs `promptfoo.config.yaml` + `promptfoo-smoke.yaml` aggiornate a `OPENAI_API_KEY` env var pattern (no key hardcoded in repo). **Smoke eval 4/4 PASS** (Qwen 7B local + Groq 70B cloud, 2 Python code-completion problems, 3s duration, 517 token totali). Output `results/promptfoo-smoke.json`. End-to-end LiteLLM proxy routing validato con virtual key.
- [x] ~~**U4-test** — Step 4 dogfood-ui live~~ **DONE 2026-04-24/25**: HTTP 200, v0.2.0, `/api/health` returns status ok (litellm/langfuse reachable, dafne unreachable atteso, db.count=0). 11 route registered (UI + API + Dafne proxy). **Finding side-effect**: Flask host process lanciato da worktree `mystifying-keller-84cb03`, DB path hardcoded a quel worktree → DB separato per-worktree non intenzionale. Non bloccante finché si legge dati dal log markdown (source of truth), ma U6 migrazione va orientata al worktree main/canonical.
- [x] ~~**U5** — ADR-0017 ratification: se U0-U4 test completati entro ~2026-05-17 review settimana 4 senza blocker → Status → Accepted + update CLAUDE.md scope repo evolution.~~ **DONE 2026-05-07 anticipato**: ADR-0017 **Accepted** in sessione Fase 6 closure (PR #4 mergeato). 5/5 criteri ratification PASS. Stack scaffold opt-in (Docker Desktop manual start). U1/U2/U4 validated. U3 promptfoo smoke 4/4 PASS via virtual key Eduardo-created.
- [x] ~~**U6** — Migrazione entries existing log → dogfood.sqlite~~ **SCRIPT READY 2026-04-25 auto-mode**: `scripts/migrate-log-to-sqlite.py` legge la cumulative table finale di `logs/aider-delegation-YYYY-MM.md` + enrichment dict hardcoded per cost/tokens/commit_hash dei 12 entries aprile. Parse validato dry-run: 12/12 entries mapped, outcomes/stack/constraint-count normalizzati. Supporta `--dry-run`, `--force` override, idempotency via duplicate check. **Esecuzione reale deferred**: DB canonical deve stare in main repo `C:/dev/codemasterdd-ai-station/apps/dogfood-ui/data/dogfood.sqlite`, non in worktree. Eduardo da main: `python scripts/migrate-log-to-sqlite.py --log logs/aider-delegation-2026-04.md --db apps/dogfood-ui/data/dogfood.sqlite`. Prerequisito: stop Flask `mystifying-keller-84cb03`, rilancia da main. Follow-up opzionale: secondary pass parser sezioni narrative per arricchire entries futuri senza manual enrichment dict update.

## Bloccato da (TUTTI RISOLTI 2026-05-28)

- [x] ~~**B1** — ADR-0015 Budget decision: richiede chiusura Fase 6 (tutti 4 criteri ADR-0014). ETA sblocco ~2026-05-20.~~ **DONE 2026-05-28 (stale-resolved)**: ADR-0015 **Accepted 2026-05-07** (Fase 6 closure anticipata, PR #4). Successivamente SUPERSEDED-by-ADR-0030 (Hybrid A1 pivot Accepted 2026-05-18). B1 unblock effettivo da 2026-05-07.
- [x] ~~**B2** — Fase 7 migration finalization (rinuncia Claude Max): dipende da 2026-05-19 (hard date) + B1.~~ **DONE 2026-05-28 (PIVOT cambiato)**: rinuncia Claude Max non e' piu' la transition path -> ADR-0030 Hybrid A1 Accepted 2026-05-18 ha ri-acquistato Claude Max +1mo (deadline ~17/06) + Pro $20/mo + Meridian. Fase 7 originale (full-sovereign $0-50/anno) e' SUPERSEDED.
- [x] ~~**B3** — Extension Fase 6 mirata con ADR-0014 Addendum: dipende da review settimana 2+4.~~ **DONE 2026-05-28 (no extension needed)**: review settimana 2 (H5) DONE 2026-04-24 + closure Fase 6 DONE 2026-05-07 senza extension. ADR-0014 closure verdict: on-track, no mid-course correction.

---

## Sprint corrente

> **SPRINT_01 ✅ CLOSED early-hit 2026-04-24** (target dataset 12 dogfood + ≥3 behavior raggiunto in 1gg, vs 2 settimane previste). Dettaglio storico in `SPRINT_01.md`.
>
> **SPRINT_02 🟡 PLANNING (finestra 20/05 → ~19/06)** — prima sessione full-sovereign post Claude Max expiration. Dettaglio in `SPRINT_02.md`. Sintesi qui per navigazione rapida.

- **Obiettivo sprint**: validare empiricamente scenario A (full-sovereign $0-50/anno) in uso normale + cleanup PR esterni opportunistico + cost tracking primo mese reale + raccolta dogfood organici post-closure (target soft n>=20 cumulative). Zero silent-corruption deve rimanere invariato.
- **Task T1** — Smoke test sovereign empirico ✅ **DONE 2026-05-07 anticipato** (PR #6, 2/3 wrapper PASS, pattern wrong-target-file documentato).
- **Task T2** — Dogfood organico continuativo (target soft n>=20 cumulative entro 19/06).
- **Task T3** — Stack ADR-0017 hot-restart procedure validation (<60s up + endpoint health).
- **Task T4** — Cleanup PR esterni opportunistico ✅ **DONE 2026-05-07** (4/4 PR triagati).
- **Task T5** — Cost tracking primo mese full-sovereign (~15/06): target <$5/mese, atteso <$1.
- **Task T6** — Privacy validation Synesthesia preview (opportunistic, skip se dormant come atteso).
- **Task T7** — Review fine sprint + ADR addendum se serve.
- **Definition of done**:
  - 5/5 task non-anticipated chiusi (T2/T3/T5/T6/T7)
  - Dataset >= 18 entries entro 2026-06-19, fail rate cumulative <15%, zero silent-corruption
  - Cost mensile cumulative <$5 confermato
  - Decisione SPRINT_03 scope chiara

### Task derivati da spec V3 cross-repo orchestrator (PR #87 Opt 1.5 REDUCED)

- [x] ~~**X1** Component 2 workflow doc + tracking template + dry-run validator (PR #87)~~ **DONE pre-Max**
- [x] ~~**X2** Component 3 escalation gates A-E + Gate E discipline + weekly reminder cron (PR #87)~~ **DONE pre-Max**
- [ ] **X3** Gate E empirical window 30gg post-Max (2026-05-20 -> 2026-06-19): Eduardo logging discipline + week 4 harsh-reviewer audit
- [ ] **X4** Gate E decision evaluation (~2026-06-20): BUILD full / BUILD MINIMAL / DEFER based on empirical events count
- [ ] **X5** Component 1 dashboard implementation (CONDITIONAL on X4 outcome >=5 events/wk OR 2-5 events/wk minimal scope)

---

## Dead weight / sospetti (da NON riaprire senza trigger)

- `docs/reference/agno-ollama-snippets.md` Pattern 2 → fixato, no-op pendente.
- `docs/reference/subagents-skills-candidates.md` → catalogo dormiente, nessun install pianificato.
- `final-research-and-snippets-2026-04-21-v3.md` (root) → source material esterno, triato.
- `docs/sessions/` → log historiche, congelate.
- Task #13/#14 vecchi (deepseek eval + API keys setup) → chiusi de-facto.
- `FIRST_PRINCIPLES_GAME_CHECKLIST.md` → skipped (Decisione 002 in `DECISIONS_LOG.md`).
