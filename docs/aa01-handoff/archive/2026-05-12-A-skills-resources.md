# AA01 Task A — Skills collection evaluation (4 repo)

> **🟢 RESOLVED 2026-05-12 (anti-rot pointer, no re-triage)** — Scaffold AA01 SUPERSEDED dalla decisione finale. Verdetti shippati: **#1** everything-claude-code = DEFER post-1wk-monitor superpowers · **#3** superpowers = INSTALLED v5.1.0 · **#5** forrestchang = AUDIT-ONLY (LICENSE missing) · **#10** anthropics/skills = MARKETPLACE registered (bundle=skip-dup). Fonte-verità: `docs/reference/subagents-skills-candidates.md` §"Riepilogo decisioni preliminari" + canonical `Vault-ops-remote/claude-global/canonical-config.json` `shipped_triage_reference_ANTI_ROT`. Nessuna azione autonoma residua (chiuso / time-gated / Eduardo-direct). NON re-triagare.

> **Preset**: `research-long`
> **Slug**: `2026-05-12-A-skills-resources`
> **Effort stima**: 4-6 ore (audit + selective install + collision check)
> **Trigger origin**: screenshot OCR Eduardo 2026-05-12, sessione codemasterdd
> **Reference master**: `docs/reference/subagents-skills-candidates.md` sezione "Wave 2026-05-12 categoria A"
> **BACKLOG entry**: M11

## Scope

Evaluation + selective install di 4 skills-collection repo. Cherry-pick selettivo (NO bulk install), audit security per-skill (Apache/MIT confermare, no shell eval network nascosti, repo manutenuto ultimi 90gg).

| # | Repo | Stars reali | Path install previsto |
|---|------|-------------|----------------------|
| 1 | `affaan-m/everything-claude-code` (REFRESH) | ~163-180k | `~/.claude/skills/` cherry-pick (escluso Memory Persistence se task B install claude-mem) |
| 3 | `obra/superpowers` | ~16.6k | `~/.claude/skills/` (DORMANT pending overlap audit vs #1) |
| 5 | `forrestchang/andrej-karpathy-skills` | ~117-123k | AUDIT-ONLY (lesson, NO install — single CLAUDE.md derivato) |
| 10 | `anthropics/skills` | ~132k | `~/.claude/skills/` selective (1-2 skill che match Synesthesia / Game / governance codemasterdd) |

## Criteri DRAFT -> PROPOSED

DRAFT contiene per ogni repo:
1. README scan + struttura skill files (count + categorie)
2. Audit security baseline:
   - License confermata (Apache/MIT/BSD acceptable, GPL valutare, no-license SKIP)
   - Last commit < 90gg (manutenuto)
   - Shell scripts grep: no `curl | bash`, no `eval`, no `wget` opachi
   - Skill files frontmatter: no tool `Bash` con comandi network non-dichiarati
3. Match use case codemasterdd (matrix: skill | use-case | priority HIGH/MED/LOW)
4. Collision check: vs nostri 18 sub-agent, vs `~/.claude/skills/` esistenti

PROPOSED: per ogni repo decisione INSTALL/BOOKMARK/DORMANT/SKIP + path target.

## Criteri SHIP (gate uscita)

- [ ] Skills high-priority installati in `~/.claude/skills/<skill>/SKILL.md`
- [ ] Verifica `claude code` ricarica skills (sessione test smoke 1 skill)
- [ ] JOURNAL entry codemasterdd `2026-05-XX` con elenco skills installati + use case
- [ ] Update `docs/reference/subagents-skills-candidates.md` con stato "INSTALLED" per ognuno (refresh tabella)
- [ ] Lesson `learnings/L-2026-05-NNN-skills-collection-cherry-pick.md` con pattern decisionali (overlap detection, audit gate, install location)

## Anti-pattern da evitare

- Install bulk repo intero (overhead skill duplicate, collision skills marketplace + cherry-pick)
- Skip audit security perche' "popolare" (stars != safe — soprattutto skills-collection)
- Doppia memory system (claude-mem + Memory Persistence di #1 entrambi) -> rotta SPOF sync
- Skill che richiede MCP server custom non gia in nostro stack -> ADR dedicato richiesto
- Skip collision check vs 18 sub-agent codemasterdd esistenti

## Note operative

- **Cherry-pick metodologia**: per ogni repo
  ```bash
  git clone --depth 1 git@github.com:<owner>/<repo>.git ~/tmp-eval/<repo>
  ls ~/tmp-eval/<repo>/skills/ # o equiv
  cat ~/tmp-eval/<repo>/skills/<skill>/SKILL.md # audit prima di copy
  cp -r ~/tmp-eval/<repo>/skills/<skill> ~/.claude/skills/
  rm -rf ~/tmp-eval/<repo>
  ```
- **Test smoke post-install**: `claude code --help` deve elencare nuovo skill. Trigger via `/<skill-name>` in sessione vuota.
- **Privacy guard rail**: tutti i 4 repo sono pubblici, no privacy concern. Codemasterdd repo e' whitelisted cloud OK.

## Output atteso (handoff post-SHIP)

- N skills installati (N atteso 2-5 totali cumulative cross-4-repo, NO 10+)
- 0-1 ADR draft se emerge architectural impact (es. skill che richiede MCP server custom)
- 1 lesson L-2026-05-NNN con criterio install + audit checklist riusabile
- Update tabella `subagents-skills-candidates.md` con status INSTALLED + path effettivo
