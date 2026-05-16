#!/usr/bin/env python3
"""
scan-gpt-refs.py -- Scan ChatGPT conversation JSONs for references to shared Custom GPTs.

Detects URL patterns:
  - https://chatgpt.com/g/g-<id>-<slug>
  - https://chat.openai.com/g/g-<id>-<slug>

Useful when Eduardo's conv mention or use OTHER people's GPTs (he owns 0 himself).
Builds inventory + freq table for vault context taxonomy.
"""

import argparse
import json
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

from tqdm import tqdm


GPT_URL_PATTERN = re.compile(r'https?://(?:chat\.openai\.com|chatgpt\.com)/g/g-([A-Za-z0-9]+)(?:-([a-z0-9-]+))?', re.IGNORECASE)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True, type=Path, help='brianjlacy export root')
    p.add_argument('--output', required=True, type=Path)
    return p.parse_args()


def extract_text_from_mapping(conv_json):
    """Concatenate all message text from conv (linear walk)."""
    mapping = conv_json.get('mapping') or {}
    if not mapping:
        return ''

    root_candidates = [nid for nid, node in mapping.items() if not node.get('parent')]
    if not root_candidates:
        return ''

    def reach(rid):
        c, cur = 0, rid
        v = set()
        while cur and cur not in v:
            v.add(cur)
            n = mapping.get(cur)
            if not n:
                break
            if n.get('message'):
                c += 1
            ch = n.get('children') or []
            cur = ch[0] if ch else None
        return c

    root_id = max(root_candidates, key=reach)
    texts = []
    cur, v = root_id, set()
    while cur and cur not in v:
        v.add(cur)
        node = mapping.get(cur)
        if not node:
            break
        msg = node.get('message')
        if msg and msg.get('content'):
            ct = msg['content']
            if isinstance(ct, dict):
                for part in ct.get('parts', []) or []:
                    if isinstance(part, str):
                        texts.append(part)
                if ct.get('text'):
                    texts.append(ct['text'])
        ch = node.get('children') or []
        cur = ch[0] if ch else None

    return '\n'.join(texts)


def main():
    args = parse_args()

    # Walk all conv JSONs in input root
    json_files = []
    for sub in ('json', 'projects'):
        sub_path = args.input / sub
        if sub_path.is_dir():
            json_files.extend(sub_path.rglob('*.json'))

    # Skip index files
    json_files = [f for f in json_files if 'index' not in f.name.lower()]

    gpt_refs = defaultdict(list)  # gpt_id -> list of (conv_id, conv_title, slug)
    gpt_slugs = defaultdict(set)

    for jf in tqdm(json_files, desc='scan conv'):
        try:
            data = json.loads(jf.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            continue

        conv_id = data.get('id') or data.get('conversation_id') or jf.stem
        conv_title = data.get('title') or '(no title)'
        text = extract_text_from_mapping(data)

        for match in GPT_URL_PATTERN.finditer(text):
            gpt_id = match.group(1)
            slug = match.group(2) or ''
            gpt_refs[gpt_id].append({'conv_id': conv_id[:8], 'conv_title': conv_title, 'slug': slug})
            if slug:
                gpt_slugs[gpt_id].add(slug)

    # Build report
    today = datetime.now().strftime('%Y-%m-%d')
    total_refs = sum(len(v) for v in gpt_refs.values())

    lines = [
        '---',
        f'id: chatgpt-recovery-gpt-refs-{today}',
        f'type: index',
        f'status: live',
        f'created: {today}',
        f'collection: chatgpt-recovery-2026-05-14',
        f'tags: [index, chatgpt-import, gpt-references, third-party-gpts]',
        '---',
        '',
        f'# ChatGPT — Shared GPT references detected ({today})',
        '',
        f'Scanned {len(json_files)} conversation JSONs for Custom GPT URLs (`chat.openai.com/g/g-...`).',
        f'Distinct GPTs referenced: **{len(gpt_refs)}**',
        f'Total references: {total_refs}',
        '',
        '_Note: Eduardo owns 0 Custom GPTs himself (per audit). These references are to OTHER people\'s GPTs._',
        '',
        '## GPTs by frequency',
        '',
        '| # | GPT ID | Inferred slug(s) | Conv refs |',
        '|---|---|---|---|',
    ]

    sorted_refs = sorted(gpt_refs.items(), key=lambda x: -len(x[1]))
    for i, (gpt_id, refs) in enumerate(sorted_refs, 1):
        slugs = ', '.join(sorted(gpt_slugs[gpt_id])[:3]) or '(no slug)'
        lines.append(f'| {i} | `{gpt_id}` | {slugs} | {len(refs)} |')

    lines.extend(['', '## Per-GPT conversation list (sample top 20)', ''])
    for gpt_id, refs in sorted_refs[:20]:
        slug = sorted(gpt_slugs[gpt_id])[0] if gpt_slugs[gpt_id] else '(no slug)'
        lines.append(f'### `{gpt_id}` — {slug} ({len(refs)} refs)')
        lines.append('')
        for r in refs[:8]:
            lines.append(f'- `{r["conv_id"]}` {r["conv_title"][:60]}')
        if len(refs) > 8:
            lines.append(f'- ... ({len(refs) - 8} more)')
        lines.append('')

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\nReport: {args.output}', file=sys.stderr)
    print(f'Distinct GPTs: {len(gpt_refs)} | Total refs: {total_refs}', file=sys.stderr)


if __name__ == '__main__':
    main()
