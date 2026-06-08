# OPEN_DECISIONS

> Schema conforme a `Archivio_Libreria_Operativa_Progetti/07_CLAUDE_CODE_OPERATING_PACKAGE/OPEN_DECISIONS.template.md`.
>
> Per tutto ciò che è ambiguo ma **non abbastanza bloccante** da fermare l'intera sessione. Decisioni vision-sensitive / core-changing vanno in ADR separato.
>
> **Archivio bodies chiusi**: `docs/archive/OPEN_DECISIONS-archive.md` (full OD-001..009 estratti 2026-06-03).

---

## Snapshot 2026-06-03 (player-recap)

**1 decisione aperta (OD-010, monitoring) al 2026-06-08.** (9 OD CLOSED 001-009 + OD-010 sorveglianza.)

**Stato**: 9 OD CLOSED (001-009 tutti). I bodies completi sono in `docs/archive/OPEN_DECISIONS-archive.md`. OD-009 closure via opzione B Decommission codice (stack ADR-0017 rimosso 2026-05-28 sera, commit `672728c`). Le decisioni vision/architettura vivono in `docs/adr/` (34 ADR, di cui 6 SUPERSEDED inline). Cose che impattano cross-repo o l'utente sono tracciate nei `BACKLOG.md` / `STATUS_MULTI_REPO.md` / `JOURNAL.md` corrispondenti.

| OD | Domanda originale (in italiano) | Verdict | Cosa devi fare adesso |
|----|----------------------------------|---------|------------------------|
| OD-001 | Quale scenario budget post-Claude-Max? | ✅ CLOSED (A full-sovereign, ADR-0015 Accepted) | Niente |
| OD-002 | Fix cp1252 Windows wrapper tiene? | ✅ CLOSED (n=15 dogfood clean) | Niente (re-trigger solo se crash UnicodeEncodeError in SPRINT_02) |
| OD-003 | Default tier 3 cloud: Groq vs Cerebras? | ✅ CLOSED (Cerebras 8B cosmetic + Groq 70B behavior) | Niente |
| OD-004 | Schema DECISIONS_LOG ibrido funziona? | ✅ CLOSED 2026-05-28 (ratificato empirico: 10 Decisioni in 5 settimane, zero confusione) | Niente. Continua schema attuale |
| OD-005 | Serve FIRST_PRINCIPLES_INFRA_CHECKLIST? | ✅ CLOSED 2026-05-28 (MINIMAL-BUILD shipped: `FIRST_PRINCIPLES_INFRA_CHECKLIST.md` root) | Usalo prima di refactor / reboot / "vale la pena tenere?" |
| OD-006 | Constraint-count come 2a dimensione routing? | ✅ CLOSED (ADR-0016 Proposed n=11 data points) | Niente |
| OD-007 | AA01 capability registry / scan automatico? | ✅ CLOSED 2026-05-28 sera (3-layer cross-fleet shipped: L1 drill-down link + L2 LITE skill global discoverable + L3 STRONG-PURE directive auto-appended via deploy script. Lenovo live; Ryzen + behavioral smoke pending Eduardo) | Eduardo-manual: open fresh Claude Code session per 3-prompt behavioral smoke (T12); Ryzen `git pull origin main` + `.\scripts\setup\deploy-global-skills.ps1 -Apply` (T13) |
| OD-008 | Cross-repo Phase B Day 7 closure tracking? | ✅ CLOSED 2026-05-28 (codemasterdd-side: Phase B closure 2026-05-14 confermata in STATUS_MULTI_REPO + Game [OD-024..031] post-cutover audit ✅ SHIPPED + ADR-0024 addendum shipped PR #55) | **Lato codemasterdd niente**. Side-note opzionale: Game `OPEN_DECISIONS.md` ha ancora OD-023 marcata "APERTA 2026-05-12" -- housekeeping Game-side quando vuoi (non blocca nulla) |
| OD-009 | Stack ADR-0017 (LiteLLM+Langfuse+Postgres+dogfood-ui) post-Hybrid-A1 value review? | ✅ CLOSED 2026-05-28 sera (Decommission codice shipped: `git rm -r infra/ apps/dogfood-ui/` + ADR-0017 status SUPERSEDED-by-ADR-0030 + runbook hot-restart DEPRECATED) | Nessuna. Reversibile via git history se future need emerge |
| OD-010 | Re-visit-trigger combat Godot (tutorial->generale = N=40) orfano? | OPEN (monitoring) 2026-06-08 | Sorveglianza hub; nessuna azione finche' combat Godot = tutorial/preview. Trigger: Godot-combat -> general -> N=40 re-validation + ADR (body sotto) |

**Decisioni vision/architettura**: vivono in `docs/adr/` (24+ ADR Accepted). Per cose nuove rilevanti usa ADR-NNNN MADR format (vedi `docs/adr/0000-template.md` se esiste oppure copia struttura ADR esistente).

---

## Pattern operativo non-ADR

Per future cose minori: apri una nuova **OD-NNN** qui sotto con i campi standard:

- **Livello** (system / workflow / tooling / repo / cross-repo ...)
- **Stato** (OPEN / EVALUATING / CLOSED + data)
- **Ambiguità originale**
- **Perché conta**
- **Miglior default proposto**
- **Rischio se ignorata**
- **File o moduli coinvolti**
- **Prossima azione** + **Trigger reactivation** (se applicabile)

Quando chiudi una OD: aggiorna la riga in tabella + sposta il body in `docs/archive/OPEN_DECISIONS-archive.md`.

### OD-010 -- Re-visit-trigger combat Godot (tutorial->generale = N=40) e' orfano

- **Livello**: cross-repo (codemasterdd watch su Game-Godot-v2)
- **Stato**: OPEN (monitoring) 2026-06-08
- **Ambiguita' originale**: il combat Godot e' d20 client-side scoped tutorial/preview, divergente-by-design dal balance engine backend (N=40 ratificato). Difendibile SOLO finche' tutorial-scoped (combat-engine-divergence.md sez.6/7). Il trigger di re-visit vive SOLO nei doc Godot.
- **Perche' conta**: trigger orfano = silent-fail (stesso pattern del check-60gg di ADR-0024 mai eseguito). Se Godot-combat scala a general senza N=40, balance-drift non rilevato (failure-mode R6-2015 da latente -> attivo).
- **Miglior default**: il tripwire test `test_combat_engine_parity_contract.gd` (#371) resta il gate tecnico; questa OD = sorveglianza-intento a livello hub.
- **Rischio se ignorata**: combat shipped generale con balance non-ratificato.
- **File/moduli**: `Game-Godot-v2/scripts/session/combat_session.gd` + `scripts/combat/d20_resolver.gd` + `tests/unit/test_combat_engine_parity_contract.gd`; doc `Game-Godot-v2/docs/godot-v2/architecture/combat-engine-divergence.md`; origine codemasterdd ADR-0024 addendum reconcile.
- **Prossima azione**: nessuna finche' combat Godot resta tutorial/preview.
- **Trigger reactivation**: PR/commit che porta Godot-combat fuori tutorial/preview (general combat / enemy roster reale / ranked) -> apri N=40 re-validation + ADR. Check opportunistico al prossimo audit cross-repo (repo-health-auditor).

---

## Regola pratica

Se la decisione:
- blocca davvero il gameplay core / vision strategica (es. ADR-0001 fondamentale)
- cambia scope/priorità prodotto
- impatta più sistemi in modo irreversibile

**non basta questo file**: serve ADR esplicito in `docs/adr/` + approvazione utente esplicita.
