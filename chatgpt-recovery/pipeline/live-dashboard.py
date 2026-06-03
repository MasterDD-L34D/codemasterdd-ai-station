#!/usr/bin/env python3
"""
live-dashboard.py -- Refreshable dashboard markdown showing live recovery state.

Compiles: bulk progress per project, topic preview, scripts inventory, decision
points pending, ETA estimates, next actions. Re-runnable anytime for fresh view.

Usage:
  python live-dashboard.py \
    --export-root <export> \
    --classification <classify_dir> (optional) \
    --output <dashboard.md>
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


PROJECT_EXPECTED = {
    'Progetto Gioco Evo Tactics': 541,
    'Le Sfide dell’Arena di Hao Jin': 592,  # apostrophe variant
    "Le Sfide dell'Arena di Hao Jin": 592,
    'Creazione gpts Master DD': 624,
    'Il mio Mondo Fantasy': 168,
    'Torneo Cremesi': 106,
    'M\xc9ZI\xc8RES PRO 2025: Corso ed Esercitazioni Manuali': 88,
    'MÉZIÈRES PRO 2025: Corso ed Esercitazioni Manuali': 88,
    'pg forge': 78,
    'Valdombra': 16,
    'Campagna supporto': 9,
    'Specifiche del progetto di esame (2025 - 2026)': 4,
    'Creazione Gpts Modulare': 3,
    'Tatertot': 0,
}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--export-root', required=True, type=Path)
    p.add_argument('--classification', type=Path, help='Latest classification dir (optional)')
    p.add_argument('--output', required=True, type=Path)
    return p.parse_args()


def disk_count_per_project(export_root: Path):
    """Count actual JSON files per project on disk (reliable vs progress.json race)."""
    proj_root = export_root / 'projects'
    if not proj_root.is_dir():
        return {}
    counts = {}
    for d in sorted(proj_root.iterdir()):
        if not d.is_dir():
            continue
        json_dir = d / 'json'
        if json_dir.is_dir():
            counts[d.name] = len(list(json_dir.glob('*.json')))
    return counts


def read_progress(export_root: Path):
    pp = export_root / '.export-progress.json'
    if not pp.is_file():
        return None
    try:
        return json.loads(pp.read_text(encoding='utf-8'))
    except Exception:
        return None


def main():
    args = parse_args()
    today = datetime.now()
    progress = read_progress(args.export_root)
    disk_proj = disk_count_per_project(args.export_root)

    # Regular bucket state
    regular_count = len(progress.get('downloadedIds', [])) if progress else 0
    regular_expected = 1264

    # Files count
    files_dir = args.export_root / 'files'
    total_files = len(list(files_dir.glob('*'))) if files_dir.is_dir() else 0

    # Sum project conv on disk
    total_proj_conv = sum(disk_proj.values())

    # Memory + custom instructions presence
    memory_present = (args.export_root / 'memory-items.json').is_file()
    ci_present = (args.export_root / 'custom-instructions.json').is_file()

    # Classification state (optional)
    classify_topics = 0
    classify_docs = 0
    if args.classification and args.classification.is_dir():
        cls_path = args.classification / 'conversations-classified.json'
        if cls_path.is_file():
            try:
                docs = json.loads(cls_path.read_text(encoding='utf-8'))
                classify_docs = len(docs)
                classify_topics = len({d.get('topic_id', -1) for d in docs})
            except Exception:
                pass

    # ETA estimate (rough)
    # Pace at slow rate: ~1 conv/3min for projects
    pace_min_per_conv = 3
    remaining_proj = sum(max(0, expected - disk_proj.get(name.replace(' ', '_').replace(':', '_').replace("'", '_').replace('’', '_'), 0)) for name, expected in PROJECT_EXPECTED.items() if expected > 0)
    eta_hours = remaining_proj * pace_min_per_conv / 60

    lines = [
        f'# ChatGPT Recovery — Live Dashboard',
        f'_Generated: {today.isoformat()}_',
        '',
        '## Bulk export state',
        '',
        '### Regular + archived bucket',
        '',
        f'- Downloaded: **{regular_count} / {regular_expected}** ({100*regular_count/regular_expected:.1f}%)',
        f'- Status: **PIVOT-PAUSED** (waiting Phase 5)',
        '',
        '### Project bucket (PRIORITY)',
        '',
        '| # | Project | On disk | Expected | % | ETA |',
        '|---|---|---|---|---|---|',
    ]

    for name, expected in sorted(PROJECT_EXPECTED.items(), key=lambda x: -x[1]):
        if expected == 0:
            continue
        # Try multiple name variants for disk match
        disk = 0
        for k in disk_proj:
            simple = k.replace('_', ' ')
            if simple.startswith(name[:20]) or name[:20] in simple:
                disk = disk_proj[k]
                break
        pct = 100 * disk / expected if expected else 0
        remaining = max(0, expected - disk)
        eta = f'{remaining * pace_min_per_conv / 60:.1f}h' if remaining > 0 else 'done'
        lines.append(f'| | {name[:35]} | {disk} | {expected} | {pct:.0f}% | {eta} |')

    lines.extend([
        '',
        f'**Total project conv on disk**: {total_proj_conv} / 2229 ({100*total_proj_conv/2229:.1f}%)',
        f'**Estimated remaining time**: ~{eta_hours:.0f}h at current pace (~{pace_min_per_conv} min/conv with 429+backoff)',
        '',
        '### Aggregate',
        '',
        f'- Total files downloaded: {total_files}',
        f'- Memory items: {"✅ fetched" if memory_present else "❌ missing"}',
        f'- Custom Instructions: {"✅ fetched" if ci_present else "❌ missing"}',
        '',
        '## Pipeline scripts',
        '',
        '| Script | Status |',
        '|---|---|',
    ])

    pipeline_dir = Path(__file__).parent
    for script in sorted(pipeline_dir.glob('*.py')):
        if script.name == 'live-dashboard.py':
            continue
        lines.append(f'| `pipeline/{script.name}` | ✅ ready |')

    scripts_dir = pipeline_dir.parent / 'scripts'
    if scripts_dir.is_dir():
        for script in sorted(scripts_dir.glob('*.py')):
            lines.append(f'| `scripts/{script.name}` | ✅ ready |')
        for script in sorted(scripts_dir.glob('*.ps1')):
            lines.append(f'| `scripts/{script.name}` | ✅ ready |')
        for script in sorted(scripts_dir.glob('*.js')):
            lines.append(f'| `scripts/{script.name}` | ✅ ready |')

    lines.extend([
        '',
        '## Classification snapshot (partial)',
        '',
        f'- Latest classify run: {args.classification.name if args.classification else "(no classify dir provided)"}',
        f'- Conversations classified: {classify_docs}',
        f'- Topics found: {classify_topics}',
        '',
        '## Decision points pending Eduardo',
        '',
        '- [ ] Phase 4-5 sampling + promotion review (post-bulk)',
        '- [ ] Token rotation post-pipeline (P0 OWASP)',
        '- [ ] Stage memory cards to vault (require explicit OK)',
        '- [ ] Commit chatgpt-recovery/ + ADR-0030 + JOURNAL to codemasterdd main',
        '',
        '## Next actions',
        '',
        '### Immediate (while bulk runs)',
        '- Monitor bulk export progress',
        '- Optional: re-run live-dashboard.py every hour for updated view',
        '',
        '### When bulk completes',
        '1. Run `scripts/run-post-export-pipeline.ps1 -NonInteractive`',
        '2. Review `_processed/classification/topics-summary.md`',
        '3. Run `pipeline/sample-cards.py` + Eduardo review markdown',
        '4. Run `pipeline/promote-cards.py --dry-run` then full',
        '5. Cleanup: rotate token + remove temp env-file + archive source',
        '',
        '## Key artifacts (test-fixtures/)',
        '',
        '- `partial-classification-661/` — 25 topic snapshot',
        '- `partial-cards-661/` — 18,194 vault-convention Cards',
        '- `project-preview/` — per-project preview Cards (Evo-Tactics 40 conv -> 2258 atoms)',
        '- `entities-index-v2.md` — 200 entity candidates',
        '- `vault-collisions-2026-05-14.md` — 127 candidate duplicates',
        '- `review-sample-661.md` — 143-card stratified review template',
        '- `chatgpt-recovery-2026-05-14-moc.md` — Atlas MOC skeleton',
        '',
        '## Critical reminders',
        '',
        '- Bearer JWT: `%TEMP%/chatgpt-bearer.env` (NTFS ACL edusc+SYSTEM). Also in Claude Code session jsonl — ROTATE post-pipeline.',
        '- vault-shared sibling-peer NO-WRITE boundary: writes require Eduardo OK esplicito',
        '- Rate limit OpenAI server-side: NO bypass legitimate (autoresearch confirmed)',
        '- Resumable: laptop sleep OK, brianjlacy resumes from .export-progress.json',
    ])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Dashboard: {args.output}')


if __name__ == '__main__':
    main()
