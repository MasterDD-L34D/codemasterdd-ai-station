# AA01 Task D — Guides + awesome-list + design-resource (4 repo)

> **Preset**: `research-long` (lightweight — bookmark-heavy, no install eseguibile)
> **Slug**: `2026-05-12-D-guides-awesome-design-resources`
> **Effort stima**: 1-2 ore (review + vault Card creation Eduardo direct)
> **Trigger origin**: screenshot OCR Eduardo 2026-05-12, sessione codemasterdd
> **Reference master**: `docs/reference/subagents-skills-candidates.md` sezione "Wave 2026-05-12 categoria D"
> **BACKLOG entry**: M14

## Scope

| # | Repo | Stars reali | Pattern adozione |
|---|------|-------------|------------------|
| 2 | `shanraisshan/claude-code-best-practice` | ~48.8k | vault Card sovereign + cross-pattern review vs nostri ADR |
| 6 | `hesreallyhim/awesome-claude-code` (REFRESH) | ~41.6k | vault Atlas index + re-scan curator post-Apr 22 |
| 9 | `dair-ai/Prompt-Engineering-Guide` | ~58.2k | vault Atlas + link in `REFERENCE_INDEX.md` codemasterdd |
| 12 | `VoltAgent/awesome-design-md` | ~74-75k | clone read-only `C:\dev\awesome-design-md-ref\` SE trigger (Synesthesia M5 attivazione o Godot v2 UX phase) |

## Criteri DRAFT -> PROPOSED

**Repo #2 best-practice**:
1. Clone shallow + scan README + table of contents
2. Cross-pattern review vs nostri ADR (cherry-pick contestualizzati):
   - 0007 quantization findings
   - 0008 silent-corruption (cosmetic vs behavior diff format)
   - 0016 constraint-count
   - 0022 OpenCode tool-use
   - 0026 cognitive workflow protocols
3. Output: 1-pager lesson "Cross-pattern delta" — cosa best-practice ha che noi NON abbiamo
4. Vault Card draft (Eduardo direct write)

**Repo #6 awesome-claude-code refresh**:
1. Re-scan curator list (vs sezione "Reference esterni" gia documentata line 48-56 file reference)
2. Identifica entry post-Apr 22 non ancora catalogati
3. Trigger eventuale BOOKMARK aggiunto a tabella esistente

**Repo #9 dair-ai prompt eng guide**:
1. Clone shallow read README + lessons/ structure
2. Lookup di sezioni rilevanti:
   - RAG (utility cross vault-shared + agent design)
   - AI agents (overlap con nostri 18 sub-agent + ADR-0018 readiness)
   - Context engineering (matches ADR-0026 cognitive workflow)
3. Aggiungere link in `REFERENCE_INDEX.md` sezione esterna

**Repo #12 awesome-design-md**:
1. README scan + lista DESIGN.md collected (brand systems Linear, Vercel, Stripe, ecc?)
2. **Trigger condizionale**: NON clonare ora. Trigger se:
   - Synesthesia M5 BACKLOG riattivata (UI work post-ago 2026)
   - Game-Godot-v2 UX phase (post Path A canonical closure)
3. PROPOSED: BOOKMARK con trigger-condition documentato

PROPOSED: 4 decisioni BOOKMARK + 0-N vault Card draft (Eduardo direct) + 0-1 lesson cross-pattern.

## Criteri SHIP

- [ ] 4 entry in vault Eduardo direct (Card per #2, Atlas index per #6+#9, trigger-doc per #12)
- [ ] `REFERENCE_INDEX.md` codemasterdd aggiornato con link esterno a #9
- [ ] 1 lesson `learnings/L-2026-05-NNN-claude-best-practice-cross-pattern.md` (output da #2 review)
- [ ] `subagents-skills-candidates.md` tabella aggiornata con stato BOOKMARK per ognuno
- [ ] JOURNAL entry sessione

## Anti-pattern

- Vault Card creation da codemasterdd Claude Code session (boundary: vault e' Eduardo direct write, NO automatized)
- Clone `awesome-design-md` ora senza trigger (overhead disk + outdated quando emergera' use case)
- Skip lesson cross-pattern review di #2 (perdita valore audit comparativo)
- Aggiornare REFERENCE_INDEX.md con tutti i 12 link (overkill — solo #9 e' canonical reference esterna; gli altri vivono in vault o file reference esistente)

## Note operative

- **Vault boundary** (CLAUDE.md sezione vault-shared): "codemasterdd NON scrive su vault-shared. Vault-shared self-governs. Eduardo media bidirezionale via personal workflow." -> Quindi Task D output e' 90% scaffold + Eduardo direct execution per vault parts.
- **REFERENCE_INDEX.md**: file codemasterdd, scrivibile da Claude Code session. Aggiungere link a #9 dair-ai sezione external resources (creare sezione se non esiste).
- **Privacy concern**: tutti pubblici, cloud OK. Nessun trigger guard rail.

## Output atteso

- 1 lesson cross-pattern (#2 vs nostri ADR)
- 1-4 vault Card Eduardo direct (post-handoff, non SHIP gate codemasterdd)
- 1 link aggiunto a `REFERENCE_INDEX.md` (#9)
- Tabella `subagents-skills-candidates.md` aggiornata
- 0 file clonati su disco fino a trigger #12 (Synesthesia/Godot)
