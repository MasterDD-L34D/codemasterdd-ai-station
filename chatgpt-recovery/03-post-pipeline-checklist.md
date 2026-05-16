# Post-Pipeline Checklist Eduardo — ChatGPT Recovery 2026-05-14

Quando bulk export completa, esegui in ordine. Ogni step ha owner + dep + checklist.

---

## Pre-Phase 0: bulk export completo?

- [ ] `.export-progress.json` mostra `indexingComplete: true` + `projectsIndexingComplete: true`
- [ ] Tutti i 12 projects in `.export-progress.json:projects` con `indexingComplete: true`
- [ ] Conv count totale ≥ 3000 (~2229 projects + ~661 regular regular bucket pivot)
- [ ] `failedFileIds` count < 50 (HTTP 422 multi-part bug acceptable; >50 = caveat)
- [ ] Bearer token still valid (esp 2026-05-24)

Se questi NON sono ✅, ripeti bulk fino completion. Resumable.

---

## Phase 0: pre-flight + decision (10 min)

- [ ] Snapshot vault HEAD as rollback anchor:
  ```powershell
  cd C:\dev\vault-shared
  git rev-parse HEAD | Out-File _meta\pre-stage-vault-head.txt
  ```
- [ ] Verifica disk free ≥ 5GB su `C:/dev/vault-shared/`
- [ ] Verifica Ollama running: `ollama list` shows `nomic-embed-text` + `qwen2.5-coder:14b-instruct-q2_K`
- [ ] **DECISIONE**: avvia orchestrator full `-NonInteractive` o run interactive? (`-NonInteractive` raccomandato per overnight unattended)

---

## Phase 1: Staging (20 min auto)

- [ ] Run orchestrator:
  ```powershell
  cd C:\dev\codemasterdd-ai-station\.claude\worktrees\affectionate-easley-a43479\chatgpt-recovery
  scripts\run-post-export-pipeline.ps1 -NonInteractive
  ```
- [ ] Verifica `vault-shared/Sources/raw/chatgpt-export-2026-05-14/` populated
- [ ] Verifica `_meta/provenance.json` + `_meta/staging.log` presenti
- [ ] File count parity: source = dest + 1 (excluded `.export-progress.json`)

---

## Phase 2: Classification (60-180 min, LLM-bound, mostly auto)

L'orchestrator esegue automaticamente. Tu monitori:

- [ ] BERTopic + nomic embedding completo senza OOM
- [ ] Qwen 14B Q2 labeling completo (~25-100 topics)
- [ ] Output: `_processed/classification/topics-summary.md` + `conversations-classified.json`
- [ ] **DECISIONE GATE**: open `topics-summary.md`, spot-check 10 topic labels vs top-5 docs each
  - Acceptance: ≥70% labels semantically corretti + outliers ≤25%
  - Se NO → re-run con tuning (vedi `02-bulk-export-runbook.md` Phase 2 troubleshooting)

---

## Phase 3: Atomization (30-60 min, mostly auto)

- [ ] Cards generated in `vault-shared/Sources/raw/chatgpt-export-2026-05-14/_processed/Cards/<topic>/`
- [ ] Expected: ~50k-150k atoms (3500+ conv × ~30 atoms/conv)
- [ ] Verifica per ogni conv touched: `<conv_short>_source.md` companion + per-message atoms
- [ ] Verifica frontmatter vault-convention compliant (`id`, `type:card`, `status:live`, ecc.)

---

## Phase 4: Review sampling (90-180 min Eduardo)

- [ ] Run sample-cards.py:
  ```powershell
  pipeline\.venv\Scripts\python.exe pipeline\sample-cards.py `
    --classification "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14\_processed\classification" `
    --cards "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14\_processed\Cards" `
    --output "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14\_meta\review-sample-2026-05-14.md"
  ```
- [ ] Apri `review-sample-2026-05-14.md` (≈143-300 cards across topics)
- [ ] Per ogni topic, fill YAML block disposition:
  - `disposition: PROMOTE` — copy Cards canonical Spaces
  - `disposition: RENAME-THEN-PROMOTE` + `rename_to: <new-label>` — rename poi promote
  - `disposition: HOLD` — leave in `_processed/Cards/` (review more later)
  - `disposition: DISCARD` — non eligible per vault
- [ ] Cross-check con `vault-collisions-2026-05-14.md`: per overlap >=3 token, considera merge vs disambiguate

---

## Phase 5: Promotion (60-120 min mixed)

- [ ] Dry-run promote-cards.py:
  ```powershell
  pipeline\.venv\Scripts\python.exe pipeline\promote-cards.py `
    --review "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14\_meta\review-sample-2026-05-14.md" `
    --staging "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14" `
    --vault "C:\dev\vault-shared" `
    --cross-ref "C:\dev\codemasterdd-ai-station\.claude\worktrees\affectionate-easley-a43479\chatgpt-recovery\vault-cross-reference-map.yaml" `
    --dry-run
  ```
- [ ] Review dry-run output: per ogni topic verifica src + dest path + count
- [ ] Apply full:
  ```powershell
  # rimuovi --dry-run
  ```
- [ ] Verifica `_meta/promotion-log-<timestamp>.json` listed promoted topics
- [ ] Spaces canonical hanno `_imported-2026-05-14/<topic_label>/` subdir con frontmatter `imported_from: chatgpt-recovery-2026-05-14`

---

## Phase 6: Atlas MOC (15 min)

- [ ] Copy MOC stub a vault Atlas:
  ```powershell
  cp "C:\dev\vault-shared\Sources\raw\chatgpt-export-2026-05-14\_meta\chatgpt-recovery-moc-stub.md" `
     "C:\dev\vault-shared\Atlas\chatgpt-recovery-2026-05-14-moc.md"
  ```
- [ ] Update wikilinks dentro MOC (rilavorare path se Spaces structure cambia)
- [ ] Add backlinks ai promoted Cards (Obsidian fa auto, but verifica)

---

## Phase 7: Cleanup + final commit (20 min)

- [ ] Verifica bearer env-file deleted (orchestrator trap dovrebbe averlo fatto):
  ```powershell
  Test-Path "$env:TEMP\chatgpt-bearer.env"  # expected: False
  ```
- [ ] Rotate bearer JWT in ChatGPT UI:
  - Settings → "Log out all other sessions"
  - Re-login → new bearer generated
  - Rationale: P0 OWASP — old bearer è in Claude Code session jsonl, scaduto 2026-05-24 ma rotare ora chiude window
- [ ] Compress backup source:
  ```powershell
  Compress-Archive "C:\dev\chatgpt-full-export-2026-05-14" `
    "C:\dev\backup\chatgpt-full-export-2026-05-14.zip"
  Remove-Item "C:\dev\chatgpt-full-export-2026-05-14" -Recurse -Force
  ```
- [ ] vault-shared git commit:
  ```powershell
  cd C:\dev\vault-shared
  git add Spaces/ Atlas/ Sources/
  git commit -m "import: chatgpt-recovery 2026-05-14 — N topics, M cards promoted"
  git tag chatgpt-import-2026-05-14
  ```
- [ ] codemasterdd commit (scripts + governance):
  ```powershell
  cd C:\dev\codemasterdd-ai-station
  git add chatgpt-recovery/ docs/adr/0030-*.md COMPACT_CONTEXT.md DECISIONS_LOG.md JOURNAL.md
  # NB: chatgpt-recovery/.gitignore esclude test-fixtures/partial-*/ (PII data)
  git commit -m "feat(chatgpt-recovery): pipeline + ADR-0030 + agent-lessons + governance"
  ```

---

## Done criteria

Recovery completa quando TUTTE le condizioni hold:

- [ ] `final-summary.md` in `_meta/` con counts validati
- [ ] ≥80% expected clusters da `expected_topic_clusters` materialized con label semantic OK
- [ ] PROMOTE topics copied a canonical Spaces + appears in Atlas MOC
- [ ] git tag `chatgpt-import-2026-05-14` su vault-shared
- [ ] Bearer env-file deleted, token rotated
- [ ] Source export compressed + removed
- [ ] BACKLOG P0/P1 ChatGPT recovery items chiusi (token rotation, vault stage)

---

## Open questions Eduardo (decide pre-Phase 4)

- [ ] Promotion granularity: copy ALL high-quality topics o sub-select (es. solo Dev/Evo-Tactics + UniUPO, skip GDR Pathfinder se duplicates con esistenti)?
- [ ] _personal/* path: dove landano memory cards con `audience: internal` (Chiara, viaggio, ecc.)? Sources/raw + tag, MAI in Spaces canonical?
- [ ] Entity index curation: vuoi che io scriva script LLM-based per filtrare entity false positives, o curi manualmente top 50?
- [ ] Promote chatgpt-recovery/ workspace al main repo o leave in worktree + archive in AA01?
