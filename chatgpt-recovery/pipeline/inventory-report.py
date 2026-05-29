#!/usr/bin/env python3
"""
inventory-report.py -- Per-project + per-bucket file inventory report.

Scans brianjlacy export root + emits:
  - Per-project conv count + file count + file types breakdown + disk size
  - Regular bucket conv count + file count
  - Memory items count
  - Total recovery stats
  - Failed file_ids count + sample

Output: inventory-report.md (vault-friendly).
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True, type=Path, help='brianjlacy export root')
    p.add_argument('--output', required=True, type=Path)
    return p.parse_args()


def dir_stats(d: Path):
    """Count + size of dir contents (recursive)."""
    if not d.is_dir():
        return {'count': 0, 'size_mb': 0.0, 'by_ext': {}}
    files = list(d.rglob('*'))
    files = [f for f in files if f.is_file()]
    total_size = sum(f.stat().st_size for f in files)
    by_ext = Counter(f.suffix.lower().lstrip('.') or 'noext' for f in files)
    return {
        'count': len(files),
        'size_mb': round(total_size / (1024 * 1024), 2),
        'by_ext': dict(by_ext.most_common()),
    }


def main():
    args = parse_args()
    root = args.input
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Regular bucket
    json_dir = root / 'json'
    markdown_dir = root / 'markdown'
    files_dir = root / 'files'

    regular_conv = len(list(json_dir.glob('*.json'))) if json_dir.is_dir() else 0
    regular_md = len(list(markdown_dir.glob('*.md'))) if markdown_dir.is_dir() else 0
    files_stats = dir_stats(files_dir)

    # Index info
    index_file = root / 'conversation-index.json'
    index_count = 0
    if index_file.is_file():
        try:
            index_count = len(json.loads(index_file.read_text(encoding='utf-8')))
        except Exception:
            pass

    # Project bucket
    projects_root = root / 'projects'
    project_stats = []
    project_index_file = projects_root / 'project-index.json'
    project_meta = {}
    if project_index_file.is_file():
        try:
            for p in json.loads(project_index_file.read_text(encoding='utf-8')):
                project_meta[p['id']] = p
        except Exception:
            pass

    if projects_root.is_dir():
        for pd in sorted(projects_root.iterdir()):
            if not pd.is_dir():
                continue
            p_json = pd / 'json'
            p_md = pd / 'markdown'
            p_files = pd / 'files'
            p_idx_file = pd / 'conversation-index.json'

            conv_count = len(list(p_json.glob('*.json'))) if p_json.is_dir() else 0
            md_count = len(list(p_md.glob('*.md'))) if p_md.is_dir() else 0
            files = dir_stats(p_files)

            idx_count = 0
            if p_idx_file.is_file():
                try:
                    idx_count = len(json.loads(p_idx_file.read_text(encoding='utf-8')))
                except Exception:
                    pass

            project_stats.append({
                'name': pd.name.replace('_', ' '),
                'conv_count': conv_count,
                'md_count': md_count,
                'idx_count': idx_count,
                'files': files,
            })

    # Memory + Custom Instructions
    mem_file = root / 'memory-items.json'
    mem_count = 0
    if mem_file.is_file():
        try:
            mem_count = len(json.loads(mem_file.read_text(encoding='utf-8')).get('memories', []))
        except Exception:
            pass

    ci_file = root / 'custom-instructions.json'
    ci_present = ci_file.is_file()

    # Progress JSON state
    progress_file = root / '.export-progress.json'
    progress = {}
    if progress_file.is_file():
        try:
            progress = json.loads(progress_file.read_text(encoding='utf-8'))
        except Exception:
            pass
    failed_count = len(progress.get('failedFileIds', {}))

    # Aggregate totals
    total_project_conv = sum(p['conv_count'] for p in project_stats)
    total_project_files = sum(p['files']['count'] for p in project_stats)
    total_project_size = sum(p['files']['size_mb'] for p in project_stats)
    total_all_conv = regular_conv + total_project_conv
    total_all_files = files_stats['count'] + total_project_files
    total_all_size = files_stats['size_mb'] + total_project_size

    # Build report
    lines = [
        f'# ChatGPT Recovery -- Inventory Report ({today})',
        '',
        f'Source: `{root}`',
        '',
        '## Aggregate totals',
        '',
        '| Metric | Value |',
        '|---|---|',
        f'| Total conversations on disk | **{total_all_conv}** |',
        f'| Regular bucket | {regular_conv} |',
        f'| Project bucket | {total_project_conv} |',
        f'| Memory items | {mem_count} |',
        f'| Custom Instructions | {"captured" if ci_present else "missing"} |',
        f'| Total file assets | **{total_all_files}** |',
        f'| Total disk size | **{round(total_all_size, 1)} MB** |',
        f'| Failed file downloads | {failed_count} (brianjlacy multi-part bug) |',
        f'| Conversation index total | {index_count} |',
        '',
        '## Regular bucket',
        '',
        f'- Conversations: {regular_conv} / {index_count} index',
        f'- Recovery rate: {100 * regular_conv / index_count if index_count else 0:.1f}%',
        f'- Markdown files: {regular_md}',
        f'- File assets: {files_stats["count"]} ({files_stats["size_mb"]} MB)',
        f'- File types: {", ".join(f"{ext}={n}" for ext, n in files_stats["by_ext"].items())}',
        '',
        '## Projects breakdown',
        '',
        '| Project | Conv on disk | Index | % | Files | Size MB |',
        '|---|---|---|---|---|---|',
    ]

    for p in project_stats:
        rate = 100 * p['conv_count'] / p['idx_count'] if p['idx_count'] else 0
        lines.append(
            f'| {p["name"][:40]} | {p["conv_count"]} | {p["idx_count"]} | '
            f'{rate:.0f}% | {p["files"]["count"]} | {p["files"]["size_mb"]} |'
        )

    lines.extend([
        '',
        '## Per-project file types',
        '',
    ])
    for p in project_stats:
        if p['files']['count'] == 0:
            continue
        types_str = ', '.join(f'{ext}={n}' for ext, n in p['files']['by_ext'].items())
        lines.append(f'- **{p["name"]}** ({p["files"]["count"]} files, {p["files"]["size_mb"]} MB): {types_str}')

    lines.extend([
        '',
        '## Failed file_ids (brianjlacy bug HTTP 422 multi-part)',
        '',
        f'Total failed: {failed_count}',
        '',
    ])

    if failed_count > 0:
        failed = progress.get('failedFileIds', {})
        sample = list(failed.keys())[:10]
        lines.append('Sample file_ids:')
        for fid in sample:
            lines.append(f'- `{fid}`')
        if failed_count > 10:
            lines.append(f'- ... ({failed_count - 10} more)')

    lines.extend([
        '',
        '## Caveats',
        '',
        '- Failed file_ids: multi-part PDF format `<hash>#file_<id>#p_<N>.png` triggers HTTP 422 on backend-api/files/download endpoint. Known brianjlacy bug, non-fatal. Affected files are typically multi-page PDF screenshots.',
        '- `num_interactions` in gizmo metadata = message count (NOT conversation count). Real conv counts come from `conversation-index.json` per project.',
        '- Memory items: 83 items captured separately via `/backend-api/memories` direct API call (replaces MemPort Chrome extension).',
        '- Custom Instructions: textarea content captured but flag `enabled: true` with empty textareas (Eduardo did not populate ChatGPT Custom Instructions).',
        '',
    ])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Inventory report: {args.output}', file=sys.stderr)
    print(f'Summary: {total_all_conv} conv, {total_all_files} files, {round(total_all_size, 1)} MB', file=sys.stderr)


if __name__ == '__main__':
    main()
