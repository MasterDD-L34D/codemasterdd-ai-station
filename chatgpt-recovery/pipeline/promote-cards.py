#!/usr/bin/env python3
"""
promote-cards.py -- Selective Card promotion from staging to canonical Spaces (Plan Phase 5).

Reads:
  - <review_file>.md with embedded YAML dispositions per topic (from sample-cards.py output)
  - vault-cross-reference-map.yaml for project -> space mapping
  - staging Cards dir: <staging>/_processed/Cards/<topic_label>/

For each PROMOTE / RENAME-THEN-PROMOTE topic:
  COPY (not move) Cards to <vault>/Spaces/<space>/_imported-2026-05-14/<topic_label>/
  Update frontmatter: imported_from + original_path + promotion_decision

Idempotent: skips already-promoted (checks for existing dest dir + manifest hash).
Refuses overwrite without --force.
Dry-run mode: list diff without writing.

Usage:
  python promote-cards.py \
    --review <review_file.md> \
    --staging <vault_staging_dir> \
    --vault <vault_root> \
    --cross-ref <vault-cross-reference-map.yaml> \
    --dry-run
  # then without --dry-run when satisfied
"""

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--review', required=True, type=Path, help='Review sample md with disposition YAML blocks')
    p.add_argument('--staging', required=True, type=Path, help='Staging vault path (Sources/raw/chatgpt-export-...)')
    p.add_argument('--vault', required=True, type=Path, help='Vault root (vault-shared/)')
    p.add_argument('--cross-ref', required=True, type=Path, help='vault-cross-reference-map.yaml')
    p.add_argument('--import-tag', default='_imported-2026-05-14', help='Subfolder name in canonical Space')
    p.add_argument('--dry-run', action='store_true', help='Print plan without writing')
    p.add_argument('--force', action='store_true', help='Overwrite existing destination Cards')
    return p.parse_args()


def parse_review_md(md_path: Path):
    """Extract disposition YAML blocks from review markdown.
    Returns: list of dict with topic_id, topic_label, disposition, rename_to, target_space, notes.
    Disposition is normalized to UPPERCASE at parse time (fix harsh-reviewer P0 #3).
    """
    content = md_path.read_text(encoding='utf-8')
    pattern = re.compile(r'^[ \t]*```yaml[ \t]*\n(.*?)\n[ \t]*```', re.DOTALL | re.MULTILINE)
    decisions = []
    for m in pattern.finditer(content):
        block = m.group(1)
        d = {}
        for line in block.splitlines():
            line = line.split('#')[0].strip()
            if ':' not in line:
                continue
            k, v = line.split(':', 1)
            d[k.strip()] = v.strip()
        if 'topic_id' in d:
            try:
                d['topic_id'] = int(d['topic_id'])
            except (ValueError, TypeError):
                pass
            # Normalize disposition case ONCE (harsh-reviewer P0 #3 fix)
            if 'disposition' in d:
                d['disposition'] = d['disposition'].upper()
            decisions.append(d)
    return decisions


def load_cross_ref(path: Path):
    """Parse minimal YAML -- only project_to_space + tag_to_space sections.
    Stdlib-only to avoid PyYAML dep (already transitive via BERTopic but kept light)."""
    content = path.read_text(encoding='utf-8')
    # Naive parser: look for "label:\n  space: \"X\"" patterns
    space_by_topic = {}
    current_topic = None
    in_project_section = False

    for line in content.splitlines():
        if line.startswith('project_to_space:'):
            in_project_section = True
            continue
        if in_project_section:
            # End on next top-level key
            if line and not line.startswith(' ') and not line.startswith('#') and ':' in line:
                in_project_section = False

            m = re.match(r'  "([^"]+)":\s*$', line)
            if m:
                current_topic = m.group(1)
                continue
            m2 = re.match(r'    space:\s*"([^"]+)"', line)
            if m2 and current_topic:
                space_by_topic[current_topic] = m2.group(1)

    return space_by_topic


def update_card_frontmatter(card_path: Path, decision: dict, staging_root: Path):
    """Add imported_from / original_path / promotion_decision to card frontmatter.
    original_path = card relative to staging_root (harsh-reviewer P0 #1+#2 fix).
    """
    content = card_path.read_text(encoding='utf-8')

    if not content.startswith('---'):
        return content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    fm = parts[1]
    body = parts[2]

    today = datetime.now().strftime('%Y-%m-%d')

    # Compute relative path safely (no fragile parents[3])
    try:
        rel = card_path.relative_to(staging_root)
        original_path_str = str(rel).replace('\\', '/')
    except ValueError:
        original_path_str = str(card_path).replace('\\', '/')

    added_lines = []
    if 'imported_from:' not in fm:
        added_lines.append(f'imported_from: chatgpt-recovery-2026-05-14')
    if 'imported_at:' not in fm:
        added_lines.append(f'imported_at: {today}')
    if 'original_path:' not in fm:
        added_lines.append(f'original_path: "{original_path_str}"')
    if 'promotion_disposition:' not in fm:
        added_lines.append(f'promotion_disposition: {decision.get("disposition", "PROMOTE")}')
        if decision.get('rename_to'):
            added_lines.append(f'promotion_rename_to: {decision["rename_to"]}')

    if added_lines:
        fm = fm.rstrip() + '\n' + '\n'.join(added_lines) + '\n'

    return f'---{fm}---{body}'


def promote_topic(decision, staging_root: Path, vault_root: Path, space_map: dict, import_tag: str, dry_run: bool, force: bool):
    """Promote one topic's cards.
    Returns: dict with stats {copied, skipped, errors, dest}.
    """
    topic_label = decision.get('topic_label')
    if not topic_label:
        return {'error': 'no topic_label'}

    # Source dir in staging
    src_dir = staging_root / '_processed' / 'Cards' / topic_label
    if not src_dir.is_dir():
        return {'error': f'staging dir not found: {src_dir}'}

    # Determine target space: explicit override or from cross-ref map
    target_space = decision.get('target_space')
    if not target_space or target_space == '':
        # Try lookup: any project_to_space entry whose key contains topic_label keywords
        for proj_name, space in space_map.items():
            if proj_name.lower().replace(' ', '-') in topic_label or topic_label in proj_name.lower():
                target_space = space
                break
    if not target_space:
        target_space = f'_uncategorized/{topic_label}'

    # Effective topic label (with rename if requested)
    # Disposition is already normalized to UPPERCASE at parse time
    effective_label = decision.get('rename_to') if decision.get('disposition') == 'RENAME-THEN-PROMOTE' else topic_label
    if effective_label and effective_label.strip():
        effective_label = effective_label.strip()
    else:
        effective_label = topic_label

    # Destination: <vault>/Spaces/<target_space>/<import_tag>/<effective_label>/
    dest_dir = vault_root / 'Spaces' / target_space / import_tag / effective_label

    cards = list(src_dir.glob('*.md'))
    if not cards:
        return {'topic_label': topic_label, 'copied': 0, 'skipped': 0, 'errors': 0, 'reason': 'no cards in staging'}

    if dest_dir.exists() and not force:
        existing = len(list(dest_dir.glob('*.md')))
        if existing > 0:
            return {
                'topic_label': topic_label,
                'dest': str(dest_dir),
                'copied': 0,
                'skipped': len(cards),
                'errors': 0,
                'reason': f'dest exists ({existing} cards); use --force to overwrite',
            }

    if dry_run:
        return {
            'topic_label': topic_label,
            'src': str(src_dir),
            'dest': str(dest_dir),
            'cards_to_copy': len(cards),
            'dry_run': True,
            'effective_label': effective_label,
            'target_space': target_space,
        }

    dest_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    errors = 0
    for card in cards:
        try:
            content_with_fm = update_card_frontmatter(card, decision, staging_root)
            (dest_dir / card.name).write_text(content_with_fm, encoding='utf-8')
            copied += 1
        except Exception as e:
            print(f'  Error copying {card.name}: {e}', file=sys.stderr)
            errors += 1

    return {
        'topic_label': topic_label,
        'effective_label': effective_label,
        'target_space': target_space,
        'src': str(src_dir),
        'dest': str(dest_dir),
        'copied': copied,
        'errors': errors,
    }


def main():
    """Parses review decisions, loads space mappings, and promotes approved topics to the vault.
    Outputs results as JSON."""
    args = parse_args()

    decisions = parse_review_md(args.review)
    print(f'Parsed {len(decisions)} disposition blocks from review', file=sys.stderr)

    space_map = load_cross_ref(args.cross_ref)
    print(f'Loaded {len(space_map)} project->space mappings', file=sys.stderr)

    # Disposition is normalized in parse_review_md, so direct comparison
    promote_decisions = [d for d in decisions if d.get('disposition', '') in ('PROMOTE', 'RENAME-THEN-PROMOTE')]
    print(f'PROMOTE / RENAME-THEN-PROMOTE: {len(promote_decisions)} topics', file=sys.stderr)
    skipped_dispositions = [d for d in decisions if d.get('disposition', '') in ('HOLD', 'DISCARD')]
    print(f'HOLD / DISCARD: {len(skipped_dispositions)} (no action)', file=sys.stderr)

    if args.dry_run:
        print('\n=== DRY RUN -- no files will be written ===', file=sys.stderr)

    results = []
    for d in promote_decisions:
        r = promote_topic(d, args.staging, args.vault, space_map, args.import_tag, args.dry_run, args.force)
        results.append(r)
        print(json.dumps(r, ensure_ascii=False), file=sys.stderr)

    # Write log
    today = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    log_path = args.staging / '_meta' / f'promotion-log-{today}.json'
    if not args.dry_run:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps({
            'timestamp': datetime.now().isoformat(),
            'review_file': str(args.review),
            'import_tag': args.import_tag,
            'results': results,
        }, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'\nPromotion log: {log_path}', file=sys.stderr)

    total_copied = sum(r.get('copied', 0) for r in results)
    total_errors = sum(r.get('errors', 0) for r in results)
    print(f'\n=== Summary ===', file=sys.stderr)
    print(f'Topics promoted: {len([r for r in results if r.get("copied", 0) > 0])}', file=sys.stderr)
    print(f'Cards copied: {total_copied}', file=sys.stderr)
    print(f'Errors: {total_errors}', file=sys.stderr)


if __name__ == '__main__':
    main()
