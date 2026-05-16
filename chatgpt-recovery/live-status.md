# ChatGPT Recovery — Live Dashboard
_Generated: 2026-05-15T03:23:52.367410_

## Bulk export state

### Regular + archived bucket

- Downloaded: **746 / 1264** (59.0%)
- Status: **PIVOT-PAUSED** (waiting Phase 5)

### Project bucket (PRIORITY)

| # | Project | On disk | Expected | % | ETA |
|---|---|---|---|---|---|
| | Creazione gpts Master DD | 0 | 624 | 0% | 31.2h |
| | Le Sfide dell’Arena di Hao Jin | 0 | 592 | 0% | 29.6h |
| | Le Sfide dell'Arena di Hao Jin | 0 | 592 | 0% | 29.6h |
| | Progetto Gioco Evo Tactics | 40 | 541 | 7% | 25.1h |
| | Il mio Mondo Fantasy | 13 | 168 | 8% | 7.8h |
| | Torneo Cremesi | 0 | 106 | 0% | 5.3h |
| | MÉZIÈRES PRO 2025: Corso ed Esercit | 0 | 88 | 0% | 4.4h |
| | pg forge | 1 | 78 | 1% | 3.9h |
| | Valdombra | 1 | 16 | 6% | 0.8h |
| | Campagna supporto | 0 | 9 | 0% | 0.5h |
| | Specifiche del progetto di esame (2 | 1 | 4 | 25% | 0.1h |
| | Creazione Gpts Modulare | 0 | 3 | 0% | 0.1h |

**Total project conv on disk**: 57 / 2229 (2.6%)
**Estimated remaining time**: ~138h at current pace (~3 min/conv with 429+backoff)

### Aggregate

- Total files downloaded: 1670
- Memory items: ✅ fetched
- Custom Instructions: ✅ fetched

## Pipeline scripts

| Script | Status |
|---|---|
| `pipeline/atomize-memory.py` | ✅ ready |
| `pipeline/atomize.py` | ✅ ready |
| `pipeline/build-moc-stub.py` | ✅ ready |
| `pipeline/classify.py` | ✅ ready |
| `pipeline/extract-entities.py` | ✅ ready |
| `pipeline/project-preview.py` | ✅ ready |
| `pipeline/promote-cards.py` | ✅ ready |
| `pipeline/sample-cards.py` | ✅ ready |
| `pipeline/vault-collision-scan.py` | ✅ ready |
| `scripts/auto-audit.py` | ✅ ready |
| `scripts/fetch-memories-and-instructions.py` | ✅ ready |
| `scripts/run-post-export-pipeline.ps1` | ✅ ready |
| `scripts/setup-playwright.ps1` | ✅ ready |
| `scripts/stage-to-vault.ps1` | ✅ ready |
| `scripts/scrape-custom-gpts.js` | ✅ ready |

## Classification snapshot (partial)

- Latest classify run: partial-classification-661
- Conversations classified: 659
- Topics found: 25

## Decision points pending Eduardo

- [ ] Phase 4-5 sampling + promotion review (post-bulk)
- [ ] Token rotation post-pipeline (P0 OWASP)
- [ ] Stage memory cards to vault (require explicit OK)
- [ ] Commit chatgpt-recovery/ + ADR-0030 + JOURNAL to codemasterdd main

## Next actions

### Immediate (while bulk runs)
- Monitor bulk export progress
- Optional: re-run live-dashboard.py every hour for updated view

### When bulk completes
1. Run `scripts/run-post-export-pipeline.ps1 -NonInteractive`
2. Review `_processed/classification/topics-summary.md`
3. Run `pipeline/sample-cards.py` + Eduardo review markdown
4. Run `pipeline/promote-cards.py --dry-run` then full
5. Cleanup: rotate token + remove temp env-file + archive source

## Key artifacts (test-fixtures/)

- `partial-classification-661/` — 25 topic snapshot
- `partial-cards-661/` — 18,194 vault-convention Cards
- `project-preview/` — per-project preview Cards (Evo-Tactics 40 conv -> 2258 atoms)
- `entities-index-v2.md` — 200 entity candidates
- `vault-collisions-2026-05-14.md` — 127 candidate duplicates
- `review-sample-661.md` — 143-card stratified review template
- `chatgpt-recovery-2026-05-14-moc.md` — Atlas MOC skeleton

## Critical reminders

- Bearer JWT: `%TEMP%/chatgpt-bearer.env` (NTFS ACL edusc+SYSTEM). Also in Claude Code session jsonl — ROTATE post-pipeline.
- vault-shared sibling-peer NO-WRITE boundary: writes require Eduardo OK esplicito
- Rate limit OpenAI server-side: NO bypass legitimate (autoresearch confirmed)
- Resumable: laptop sleep OK, brianjlacy resumes from .export-progress.json