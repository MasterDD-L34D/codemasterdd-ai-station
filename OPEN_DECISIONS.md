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
| OD-011 | Biome-SoT cross-repo: contro quale file biome validano i canonical_refs swarm/Game? | OPEN (hub-watch) 2026-06-20 | Owner decisione = Game-canon. Hub sorveglia; nessuna azione codemasterdd finche' swarm PARKED. Body sotto; autoritativo = evo-swarm OD-007 (#127) + RFC#4-S3 finding F2 |
| OD-012 | Variante "nightmare" hc06: serve WR<10%? Il knob-space SoT non ci arriva (floor greedy ~15%, MAP-Elites edm-run 2026-07-02) | OPEN (hub-watch) 2026-07-02 | Owner = Game design. Nessuna azione finche' non nasce l'esigenza di una variante ultra-hard. Body sotto; dati = Game docs/research/2026-07-02-map-elites-v2-edm-run-results.md |

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

### OD-011 -- Biome-SoT cross-repo: contro quale file biome validano i canonical_refs?

- **Livello**: cross-repo (codemasterdd hub-watch; owner decisione = Game canon)
- **Stato**: OPEN (hub-watch) 2026-06-20
- **Ambiguita' originale**: swarm e Game leggono SoT biome DIVERSI (ground-truth verificato 2026-06-20, entrambi i loader letti). Swarm `verify-swarm-claims.py` (`load_canonical_index`, `glob biomes*.yaml`) -> `data/core/biomes.yaml` + `biomes_expansion.yaml` + `biome_aliases.yaml` (~40 id, con artefatto loader: il literal 'aliases' nel set). Game `check-canon-consistency.cjs` (`loadCanonIndex` :274) -> `packs/evo_tactics_pack/data/biomes.yaml` (~27 id; varianti che lo swarm non ha: deserto_caldo, caverna_risonante, sinaptic_trench; spelling pack `savanna` vs core `savana`).
- **Perche' conta**: il gate entity-grounding swarm (lever-1, evo-swarm #124) hard-rejecta i canonical_refs hallucinated; sul biome dimension puo' false-reject un ref pack legittimo o false-accept uno slug expansion. Stessa classe-bug del Game #2813 ma a livello SOURCE-FILE. Converge col finding F2 del workflow RFC#4-S3 (`*.biome.yaml` zero reader runtime; biomeAdapter legge `data/core/biomes.yaml`): multi-source biome reale.
- **Miglior default proposto**: Game-canon-owner decide quale file e' la SoT autorevole -- 3 ipotesi: (a) core+expansion = forward-SoT, pack runtime-derivato; (b) pack = runtime-SoT, core/expansion draft; (c) due viste legittime con mapping esplicito (savana<->savanna alias cross-file). Poi parity-test come regression-guard verde (non xfail-dalla-nascita).
- **Rischio se ignorata**: drift silenzioso biome-dimension del gate. Impatto MINORE (hallucination run-5 = species/trait, non biome) -> non urgente.
- **File/moduli**: evo-swarm `scripts/verify-swarm-claims.py`; Game `scripts/check-canon-consistency.cjs` + `data/core/biomes.yaml` + `biomes_expansion.yaml` + `packs/evo_tactics_pack/data/biomes.yaml`.
- **Prossima azione**: nessuna codemasterdd-side finche' swarm PARKED. Body autoritativo = evo-swarm `OPEN_DECISIONS.md` OD-007 (#127, mergiato 2026-06-20). Hub-watch.
- **Trigger reactivation**: riattivazione swarm runtime OR Game-canon-owner apre la decisione SoT-biome OR prossimo audit cross-repo opportunistico.

### OD-012 -- Variante "nightmare" hc06: WR<10% richiede lever fuori dal knob-space SoT

- **Livello**: cross-repo (codemasterdd hub-watch; owner decisione = Game design)
- **Stato**: OPEN (hub-watch) 2026-07-02
- **Ambiguita' originale**: la mappa MAP-Elites v2 edm-run (50 iter N=40, knob-space
  SoT-full: boss_hp 0.50-1.30 + enemy_damage 1.0-2.5 + turn_limit 25-35) mostra WR
  minimo osservato 15% -- la colonna 0-10% e' irraggiungibile. Floor strutturale del
  greedy AI su hc06: anche boss 1.26 + edm 1.9 resta ~15%.
- **Perche' conta**: se in futuro il design vuole un hc06 "quasi impossibile"
  (nightmare/prestige), il knob-space canonico NON puo' produrlo: serve estendere il
  SoT (boss_hp >1.30, cap <25, nuovo lever) o cambiare regime AI -- decisione design,
  non tuning.
- **Miglior default**: nessuna azione. La mappa QD e' l'evidenza; si riapre solo su
  esigenza design reale.
- **Rischio se ignorata**: zero oggi (nessuna variante nightmare in roadmap).
- **File/moduli**: Game `docs/research/2026-07-02-map-elites-v2-edm-run-results.md`
  (finding F-A) + `docs/playtest/canonical-suite.yaml` (knob_space SoT) +
  `tools/py/calibrate_map_elites.py`.
- **Prossima azione**: nessuna. Hub-watch.
- **Trigger reactivation**: richiesta design di variante ultra-hard hc06 OR modifica
  del knob_space nel manifest OR cambio policy AI di riferimento (greedy -> altro).

---

## Regola pratica

Se la decisione:
- blocca davvero il gameplay core / vision strategica (es. ADR-0001 fondamentale)
- cambia scope/priorità prodotto
- impatta più sistemi in modo irreversibile

**non basta questo file**: serve ADR esplicito in `docs/adr/` + approvazione utente esplicita.
