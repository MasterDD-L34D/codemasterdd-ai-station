#!/usr/bin/env python3
"""
enrich-cards.py -- Post-process Cards to add bucket/date/has-files/lang tags.

Reads existing Cards in vault-convention format, adds:
  - msg_count_bucket: short (<=5 msg) / medium (6-30) / long (31+)
  - date_year: extracted from create_time
  - has_image_refs: true if `![image:` present in body
  - language: re-detected (overrides existing if confidence higher)

Modifies frontmatter in place. Idempotent (skips Cards already enriched).
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from tqdm import tqdm


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cards-dir', required=True, type=Path)
    p.add_argument('--dry-run', action='store_true')
    return p.parse_args()


_IT_MARKERS_RE = re.compile('\\b(che|della|degli|delle|sono|essere|sua|suo|nei|questo|pi\u00f9|per\u00f2|come|perch\u00e9)\\b', re.IGNORECASE)
_EN_MARKERS_RE = re.compile(r'\b(the|and|with|that|for|this|from|have|been|use)\b', re.IGNORECASE)


def detect_lang(text):
    it = len(_IT_MARKERS_RE.findall(text))
    en = len(_EN_MARKERS_RE.findall(text))
    if it > en + 3:
        return 'it'
    if en > it + 3:
        return 'en'
    return 'mixed'


def msg_count_bucket(total):
    try:
        n = int(total)
    except (ValueError, TypeError):
        return 'unknown'
    if n <= 5:
        return 'short'
    if n <= 30:
        return 'medium'
    return 'long'


def has_image_refs(body):
    return '![image:' in body or '![image]' in body


def enrich_card(card_path: Path, dry_run: bool):
    content = card_path.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return None  # no frontmatter, skip

    try:
        fm_end = content.index('---', 3)
    except ValueError:
        return None

    fm_block = content[3:fm_end]
    body = content[fm_end + 3:]

    # Idempotent check
    if 'enriched: true' in fm_block:
        return 'already-enriched'

    # Extract msg_idx_total + create_time + existing language from frontmatter
    total_match = re.search(r'msg_idx_total:\s*(\d+)', fm_block)
    create_match = re.search(r'create_time:\s*([\d.]+)', fm_block)
    msg_total = total_match.group(1) if total_match else None
    create_time = create_match.group(1) if create_match else None

    # New fields
    bucket = msg_count_bucket(msg_total)
    date_year = ''
    if create_time:
        try:
            date_year = str(datetime.fromtimestamp(float(create_time)).year)
        except (ValueError, OSError):
            pass

    has_img = has_image_refs(body)
    lang = detect_lang(body)

    # Append new fields to frontmatter
    new_fields = [
        'enriched: true',
        f'msg_count_bucket: {bucket}',
        f'date_year: {date_year}',
        f'has_image_refs: {str(has_img).lower()}',
        f'language_recheck: {lang}',
    ]

    new_fm = fm_block.rstrip() + '\n' + '\n'.join(new_fields) + '\n'
    new_content = f'---{new_fm}---{body}'

    if not dry_run:
        card_path.write_text(new_content, encoding='utf-8')

    return 'enriched'


def main():
    args = parse_args()
    cards_dir = args.cards_dir

    if not cards_dir.is_dir():
        print(f'ERROR: {cards_dir} not found', file=sys.stderr)
        sys.exit(1)

    cards = list(cards_dir.rglob('*.md'))
    if not cards:
        print(f'No .md cards found under {cards_dir}', file=sys.stderr)
        sys.exit(0)

    stats = {'enriched': 0, 'already-enriched': 0, 'no-fm': 0, 'error': 0}
    for c in tqdm(cards, desc='enrich'):
        try:
            r = enrich_card(c, args.dry_run)
            if r is None:
                stats['no-fm'] += 1
            else:
                stats[r] += 1
        except Exception as e:
            stats['error'] += 1
            print(f'Error {c}: {e}', file=sys.stderr)

    print(f'\nEnrichment stats: {stats}')
    print(f'Total cards: {len(cards)}')
    if args.dry_run:
        print('(DRY RUN -- no files written)')


if __name__ == '__main__':
    main()
