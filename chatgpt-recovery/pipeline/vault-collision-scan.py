#!/usr/bin/env python3
"""
vault-collision-scan.py -- Detect potential title/concept overlap between recovered
ChatGPT conversations and existing vault Cards/MOCs.

Method: tokenize titles + topic_labels, check overlap against existing vault filenames
+ frontmatter titles. Heuristic — produces candidate-collisions list for Eduardo review
before promote-cards.py runs.

Output: collision-candidates.md with severity ranked.
"""

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--classification', required=True, type=Path, help='conversations-classified.json source')
    p.add_argument('--vault', required=True, type=Path, help='Vault root (vault-shared/)')
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--min-overlap', type=int, default=3, help='Min words overlap to consider collision')
    return p.parse_args()


STOPWORDS = {'di', 'il', 'la', 'le', 'gli', 'un', 'una', 'per', 'che', 'e', 'a', 'da', 'in', 'su',
             'con', 'del', 'della', 'dei', 'delle', 'al', 'alla', 'alle', 'sul', 'sulla',
             'the', 'a', 'an', 'and', 'or', 'of', 'to', 'in', 'on', 'for', 'with', 'is', 'are'}


def tokenize(text):
    if not text:
        return set()
    words = re.findall(r'\b[a-zA-Zàèìòùáéíóú]{3,}\b', text.lower())
    return {w for w in words if w not in STOPWORDS}


def scan_vault(vault_root: Path):
    """Build index of existing vault Card filenames + frontmatter titles + collection names.
    Returns: {filepath: {tokens, title, collection, type}}
    """
    index = {}
    for md in vault_root.rglob('*.md'):
        rel = md.relative_to(vault_root)
        if 'node_modules' in str(rel) or '.git' in str(rel):
            continue

        # Quick read just first 50 lines (frontmatter + H1)
        try:
            content = md.read_text(encoding='utf-8', errors='ignore')[:3000]
        except Exception:
            continue

        title = None
        collection = None
        ctype = None

        # Parse frontmatter
        if content.startswith('---'):
            try:
                fm_end = content.index('---', 3)
                fm = content[3:fm_end]
                for line in fm.splitlines():
                    line = line.strip()
                    if line.startswith('title:'):
                        title = line.split(':', 1)[1].strip().strip('"').strip("'")
                    elif line.startswith('collection:'):
                        collection = line.split(':', 1)[1].strip()
                    elif line.startswith('type:'):
                        ctype = line.split(':', 1)[1].strip()
            except (ValueError, IndexError):
                pass

        # H1 fallback for title
        if not title:
            h1_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1).strip()

        # Tokens from filename + title
        stem = md.stem
        tokens = tokenize(stem.replace('-', ' ')) | tokenize(title or '')

        index[str(rel)] = {
            'tokens': tokens,
            'title': title or stem,
            'collection': collection,
            'type': ctype,
        }

    return index


def main():
    args = parse_args()
    classified_path = args.classification / 'conversations-classified.json'
    docs = json.loads(classified_path.read_text(encoding='utf-8'))

    print(f'Scanning vault: {args.vault} ...')
    vault_index = scan_vault(args.vault)
    print(f'  Indexed {len(vault_index)} vault files')

    # For each ChatGPT conv, compute token overlap with each vault file
    print(f'Cross-matching {len(docs)} ChatGPT conv vs vault index...')

    collisions = []  # (chatgpt_conv, vault_path, overlap_tokens, score)
    for d in docs:
        title = d.get('title', '')
        topic = d.get('topic_label', '')
        chat_tokens = tokenize(title) | tokenize(topic)
        if len(chat_tokens) < 2:
            continue

        for vault_path, vault_meta in vault_index.items():
            overlap = chat_tokens & vault_meta['tokens']
            if len(overlap) >= args.min_overlap:
                collisions.append({
                    'chat_id': (d.get('id') or '')[:8],
                    'chat_title': title,
                    'chat_topic': topic,
                    'vault_path': vault_path,
                    'vault_title': vault_meta['title'],
                    'vault_collection': vault_meta['collection'],
                    'vault_type': vault_meta['type'],
                    'overlap_tokens': sorted(overlap),
                    'score': len(overlap),
                })

    # Sort by score desc, deduplicate
    collisions.sort(key=lambda c: -c['score'])

    today = datetime.now().strftime('%Y-%m-%d')
    lines = [
        '---',
        f'id: chatgpt-recovery-collisions-{today}',
        f'type: report',
        f'status: live',
        f'created: {today}',
        f'collection: chatgpt-recovery-2026-05-14',
        f'tags: [report, collision-check, chatgpt-import, pre-promotion]',
        '---',
        '',
        f'# ChatGPT Recovery — Vault Collision Candidates ({today})',
        '',
        f'Pre-promotion check: ChatGPT conv titles vs existing vault Card titles.',
        f'Min overlap threshold: {args.min_overlap} content-words.',
        '',
        f'- Vault files scanned: {len(vault_index)}',
        f'- ChatGPT conv checked: {len(docs)}',
        f'- Collision candidates: **{len(collisions)}**',
        '',
        '## Top collisions (sorted by overlap score)',
        '',
        '| Score | ChatGPT conv | Vault file | Overlap tokens |',
        '|---|---|---|---|',
    ]

    for c in collisions[:100]:
        overlap_str = ', '.join(c['overlap_tokens'][:5])
        if len(c['overlap_tokens']) > 5:
            overlap_str += f' (+{len(c["overlap_tokens"]) - 5})'
        chat_short = c['chat_title'][:50].replace('|', '\\|')
        vault_short = c['vault_path'][:60].replace('|', '\\|')
        lines.append(f'| {c["score"]} | `{c["chat_id"]}` {chat_short} | {vault_short} | {overlap_str} |')

    lines.extend([
        '',
        f'## Notes',
        '',
        '- Heuristic match (tokenization + intersection), NOT semantic equivalence',
        '- High overlap = manual review BEFORE promotion (avoid Card duplicates in vault)',
        '- Disposition: merge content into existing Card OR rename promoted Card to disambiguate',
        '- Recommend manual filter: ignore matches where vault file is generic (e.g., README, index.md)',
        '',
    ])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Collision report: {args.output}')
    print(f'Top score collisions: {len(collisions)}')


if __name__ == '__main__':
    main()
