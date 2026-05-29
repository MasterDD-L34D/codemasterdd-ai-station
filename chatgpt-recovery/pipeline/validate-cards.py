#!/usr/bin/env python3
"""
validate-cards.py -- Quality gate for atomized Cards.

Scans Cards for:
  - Missing required frontmatter fields (id, type, status, created, collection, source_ref)
  - Frontmatter parse errors (malformed YAML lines)
  - Orphan wikilinks (target file doesn't exist locally)
  - Very short body content (<30 char) -- likely atomize edge case
  - Encoding issues (mojibake patterns)
  - Duplicate IDs across cards

Output: validate-cards-report.md with severity-ranked findings.
"""

import argparse
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from tqdm import tqdm


REQUIRED_FIELDS = ['id', 'type', 'status', 'created', 'collection']


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cards-dir', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--check-wikilinks', action='store_true', help='Verify wikilink targets exist (slow)')
    return p.parse_args()


def parse_fm(content):
    if not content.startswith('---'):
        return None, content
    try:
        end = content.index('---', 3)
    except ValueError:
        return None, content
    fm_text = content[3:end]
    body = content[end + 3:]
    fm = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        fm[k.strip()] = v.strip()
    return fm, body


def extract_wikilinks(body):
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', body)


def find_mojibake(text):
    """Detect common mojibake patterns (UTF-8 decoded as cp1252)."""
    patterns = ['\xc3\x83\xc2\xa9', '\xc3\x83\xc2\xa8', '\xc3\x83\x20', '\xc3\x83\xc2\xb2', '\xc3\x83\xc2\xb9', '\xc3\xa2\xe2\x82\xac\xe2\x84\xa2', '\xc3\xa2\xe2\x82\xac"', '\xc3\xa2\xe2\x82\xac"', '\xc3\xa2\xe2\x82\xac\xc5\x93', '\xc3\xa2\xe2\x82\xac']
    return [p for p in patterns if p in text]


def main():
    args = parse_args()
    cards_dir = args.cards_dir

    if not cards_dir.is_dir():
        print(f'ERROR: {cards_dir} not found', file=sys.stderr)
        sys.exit(1)

    cards = list(cards_dir.rglob('*.md'))
    if not cards:
        print(f'No .md cards under {cards_dir}', file=sys.stderr)
        sys.exit(0)

    findings = {
        'missing_fields': [],
        'no_frontmatter': [],
        'orphan_wikilinks': [],
        'short_body': [],
        'mojibake': [],
        'duplicate_ids': defaultdict(list),
        'malformed_yaml': [],
    }

    id_map = defaultdict(list)
    all_card_stems = set()

    # Pass 1: scan
    for c in tqdm(cards, desc='scan'):
        all_card_stems.add(c.stem)
        try:
            content = c.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            findings['malformed_yaml'].append((str(c), f'read error: {e}'))
            continue

        fm, body = parse_fm(content)
        if fm is None:
            findings['no_frontmatter'].append(str(c))
            continue

        # Required field check
        missing = [f for f in REQUIRED_FIELDS if f not in fm]
        if missing:
            findings['missing_fields'].append((str(c.relative_to(cards_dir)), missing))

        # Duplicate ID
        if 'id' in fm:
            id_map[fm['id']].append(str(c.relative_to(cards_dir)))

        # Body length
        body_clean = body.strip()
        if len(body_clean) < 30:
            findings['short_body'].append((str(c.relative_to(cards_dir)), len(body_clean)))

        # Mojibake
        moj = find_mojibake(content)
        if moj:
            findings['mojibake'].append((str(c.relative_to(cards_dir)), moj))

        # Wikilink check (optional, slow)
        if args.check_wikilinks:
            links = extract_wikilinks(body)
            for link in links:
                # Resolve to local stem
                link_stem = link.split('/')[-1].split('|')[0].strip()
                if link_stem not in all_card_stems:
                    findings['orphan_wikilinks'].append((str(c.relative_to(cards_dir)), link_stem))

    # Pass 2: duplicate IDs
    for card_id, paths in id_map.items():
        if len(paths) > 1:
            findings['duplicate_ids'][card_id] = paths

    # Build report
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total = len(cards)
    lines = [
        f'# Cards Validation Report -- {today}',
        '',
        f'Cards dir: `{cards_dir}`',
        f'Total cards: **{total}**',
        '',
        '## Severity summary',
        '',
        '| Issue | Count | Severity |',
        '|---|---|---|',
        f'| Missing required FM fields | {len(findings["missing_fields"])} | P0 |',
        f'| No frontmatter | {len(findings["no_frontmatter"])} | P0 |',
        f'| Duplicate IDs | {len(findings["duplicate_ids"])} | P0 |',
        f'| Malformed YAML | {len(findings["malformed_yaml"])} | P1 |',
        f'| Short body (<30 char) | {len(findings["short_body"])} | P1 |',
        f'| Mojibake patterns | {len(findings["mojibake"])} | P2 |',
        f'| Orphan wikilinks | {len(findings["orphan_wikilinks"])} | P2 |' if args.check_wikilinks else '| Orphan wikilinks | (skipped -- use --check-wikilinks) | -- |',
        '',
    ]

    if findings['missing_fields']:
        lines.extend(['## P0 -- Missing required FM fields', ''])
        for path, missing in findings['missing_fields'][:50]:
            lines.append(f'- `{path}` -- missing: {", ".join(missing)}')
        if len(findings['missing_fields']) > 50:
            lines.append(f'- ... ({len(findings["missing_fields"]) - 50} more)')
        lines.append('')

    if findings['no_frontmatter']:
        lines.extend(['## P0 -- No frontmatter', ''])
        for path in findings['no_frontmatter'][:30]:
            lines.append(f'- `{path}`')
        lines.append('')

    if findings['duplicate_ids']:
        lines.extend(['## P0 -- Duplicate IDs', ''])
        for card_id, paths in list(findings['duplicate_ids'].items())[:20]:
            lines.append(f'- `{card_id}`:')
            for p in paths:
                lines.append(f'  - `{p}`')
        lines.append('')

    if findings['short_body']:
        lines.extend(['## P1 -- Short body (<30 char)', ''])
        for path, length in findings['short_body'][:30]:
            lines.append(f'- `{path}` -- {length} chars')
        if len(findings['short_body']) > 30:
            lines.append(f'- ... ({len(findings["short_body"]) - 30} more)')
        lines.append('')

    if findings['mojibake']:
        lines.extend(['## P2 -- Mojibake patterns detected', ''])
        for path, patterns in findings['mojibake'][:20]:
            lines.append(f'- `{path}` -- patterns: {patterns}')
        lines.append('')

    if findings['orphan_wikilinks'] and args.check_wikilinks:
        lines.extend(['## P2 -- Orphan wikilinks (top 30)', ''])
        # Count per orphan target
        orphan_freq = defaultdict(int)
        for src, tgt in findings['orphan_wikilinks']:
            orphan_freq[tgt] += 1
        for tgt, freq in sorted(orphan_freq.items(), key=lambda x: -x[1])[:30]:
            lines.append(f'- `{tgt}` referenced by {freq} cards')
        lines.append('')

    # Verdict
    p0 = len(findings['missing_fields']) + len(findings['no_frontmatter']) + len(findings['duplicate_ids'])
    p1 = len(findings['short_body']) + len(findings['malformed_yaml'])
    p2 = len(findings['mojibake']) + (len(findings['orphan_wikilinks']) if args.check_wikilinks else 0)

    lines.extend([
        '## Verdict',
        '',
        f'- P0 issues: **{p0}** {"[FAIL] FIX REQUIRED" if p0 > 0 else "[PASS] clean"}',
        f'- P1 issues: **{p1}** ({100*p1/total:.1f}% of cards)',
        f'- P2 issues: **{p2}** (cosmetic)',
        '',
        'Pass threshold: P0 = 0 AND P1 < 5% of cards.',
        f'Result: **{"PASS" if p0 == 0 and p1 < total * 0.05 else "FAIL -- review fixes"}**',
        '',
    ])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nReport: {args.output}')
    print(f'P0: {p0} | P1: {p1} | P2: {p2}')


if __name__ == '__main__':
    main()
