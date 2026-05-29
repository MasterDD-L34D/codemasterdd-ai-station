#!/usr/bin/env python3
"""
atomize-memory.py -- Convert ChatGPT Memory items to vault Cards.

Reads memory-items.json (from fetch-memories-and-instructions.py output) and
produces 1 Card per memory item with frontmatter + content + heuristic tags.

Tag heuristics (case-insensitive substring match):
  - pathfinder/PF/PG -> rpg-pathfinder
  - evo-tactics      -> evo-tactics
  - chiara           -> personal-life
  - napugol          -> personal-language
  - synesthesia/UniUPO -> uniupo-academic
  - gpt/agent/AI     -> ai-tooling
  - ecosistem        -> game-ecosystem
  - manual/scheda    -> rpg-character-sheet

LLM tag refinement deferred to classify.py later. This script is rule-based
for speed (runs in <2 seconds for 83 items).

Output:
  <output>/Cards/<NN>_<slug>.md
  <output>/INDEX.md (listing all cards + tag matrix)
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


# Heuristic tag rules: (regex, tag_label)
TAG_RULES = [
    (r'\b(pathfinder|PF\s*1?e?|PG|PNG|d20)\b', 'rpg-pathfinder'),
    (r'\b(evo[\s-]?tactics|tactical)\b', 'evo-tactics'),
    (r'\b(chiara|fidanzata|compagna)\b', 'personal-life'),
    (r'\bnapugol\b', 'personal-language'),
    (r'\b(synesthesia|sinestesia|uniupo|esame)\b', 'uniupo-academic'),
    (r'\b(custom gpt|gpts|agent|ai)\b', 'ai-tooling'),
    (r'\becosistem', 'game-ecosystem'),
    (r'\b(manuale|scheda|stat block|character sheet)\b', 'rpg-character-sheet'),
    (r'\b(loot|wealth|tesoro)\b', 'rpg-loot'),
    (r'\b(viaggio|napoli|barcellona|catalogna)\b', 'travel-iberia'),
    (r'\b(foresta|biome|biom|naturalistic)\b', 'game-ecology'),
    (r'\b(software|app|architettura|build)\b', 'software-build'),
    (r'\b(checklist|TODO|table|tabella)\b', 'formatting-preference'),
    (r'\b(mondo fantasy|worldbuilding|lore)\b', 'worldbuilding'),
    (r'\b(combat|combattimento|stat|skill)\b', 'game-mechanics'),
    (r'\b(arena|hao jin|cremesi|torneo)\b', 'campaign-instances'),
    (r'\b(spagnolo|napoletano|italiano|inglese|linguistic)\b', 'linguistic'),
]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--input', required=True, type=Path, help='memory-items.json path')
    p.add_argument('--output', required=True, type=Path, help='Output dir (will create Cards/ subdir)')
    p.add_argument('--verbose', action='store_true')
    return p.parse_args()


def slugify(s, maxlen=60):
    if not s:
        return 'untitled'
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s[:maxlen] or 'untitled'


COMPILED_TAG_RULES = [(re.compile(pattern, re.IGNORECASE), label) for pattern, label in TAG_RULES]

def detect_tags(content):
    tags = set()
    for compiled_pattern, label in COMPILED_TAG_RULES:
        if compiled_pattern.search(content):
            tags.add(label)
    return sorted(tags)


_IT_MARKERS_RE = re.compile(r'\b(che|della|degli|delle|sono|essere|sua|suo|nei|questo|questa|piu|pero|come|quindi|perche|sempre|pero)\b', re.IGNORECASE)
_EN_MARKERS_RE = re.compile(r'\b(the|and|with|that|for|this|from|have|been|were|been|use|user)\b', re.IGNORECASE)


def detect_language(content):
    """Heuristic: italian if mostly italian words, else default."""
    italian_markers = _IT_MARKERS_RE.findall(content)
    english_markers = _EN_MARKERS_RE.findall(content)
    if len(italian_markers) > len(english_markers):
        return 'italian'
    elif len(english_markers) > 5:
        return 'english'
    return 'mixed'


def yaml_escape(s):
    if not s:
        return '""'
    s = str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    return f'"{s}"'


# Map detected heuristic tags -> PII sensitivity tags (privacy-policy-enforcer agent finding 2026-05-14)
TAG_TO_PII = {
    'personal-life': 'personal-name',
    'travel-iberia': 'location-travel',
    'campaign-instances': 'character-hobby',
    'rpg-character-sheet': 'character-hobby',
    'uniupo-academic': 'academic-institution',
    'personal-language': 'personal-language-codename',
    'linguistic': 'personal-language-codename',
    'formatting-preference': 'personal-preference',
}

# Audience hint mapping
COLLECTION_TO_AUDIENCE = {
    'personal-life': 'internal',
    'travel-iberia': 'internal',
    'campaign-instances': 'team',  # GDR group acceptable
    'evo-tactics': 'public',  # public repo
    'ai-tooling': 'team',
    'uniupo-academic': 'internal',
    'game-ecosystem': 'public',
    'worldbuilding': 'team',
}


def derive_pii_tags(domain_tags):
    pii = set()
    for t in domain_tags:
        if t in TAG_TO_PII:
            pii.add(TAG_TO_PII[t])
    return sorted(pii)


def derive_audience(domain_tags):
    """Strictest audience wins. internal > team > public."""
    audiences = ['public']
    for t in domain_tags:
        if t in COLLECTION_TO_AUDIENCE:
            audiences.append(COLLECTION_TO_AUDIENCE[t])
    order = {'internal': 0, 'team': 1, 'public': 2}
    return min(audiences, key=lambda a: order.get(a, 99))


def write_card(item, idx, output_dir):
    content = item.get('content', item.get('text', '')).strip()
    if not content:
        return None

    mem_id = item.get('id', f'unknown-{idx}')
    updated = item.get('updated_at', item.get('created_at', ''))
    tags = detect_tags(content)
    lang = detect_language(content)
    pii_tags = derive_pii_tags(tags)
    audience = derive_audience(tags)

    # Title heuristic: first sentence (up to 80 char)
    title_match = re.match(r'^(.{20,150}?)[.!?\n]', content)
    title = title_match.group(1).strip() if title_match else content[:80].strip()
    title = re.sub(r'\s+', ' ', title)[:100]

    slug = slugify(title, maxlen=50)
    filename = f'{idx:03d}_{slug}.md'
    path = output_dir / filename

    today = datetime.now().strftime('%Y-%m-%d')
    sha256 = hashlib.sha256(content.encode('utf-8')).hexdigest()[:8]
    char_count = len(content)
    # Vault language code: it/en/mixed
    lang_code = {'italian': 'it', 'english': 'en', 'mixed': 'mixed'}.get(lang, lang)

    all_tags = ['card', 'chatgpt-memory', 'raw-collection', f'lang-{lang_code}'] + tags
    pii_tags_str = ', '.join(pii_tags) if pii_tags else ''

    fm = [
        '---',
        # Vault-convention universal
        f'id: chatgpt-memory-{mem_id[:12] if mem_id else idx}',
        f'type: card',
        f'status: live',
        f'created: {today}',
        # Common
        f'language: {lang_code}',
        f'collection: chatgpt-memory',
        f'tags: [{", ".join(all_tags)}]',
        f'last_verified: {today}',
        f'source_ref: chatgpt-export-2026-05-14/memory-items.json',
        # Metadata
        f'source_section: "memory-item-{mem_id[:8] if mem_id else idx}"',
        f'source_sha256: {sha256}',
        f'char_count: {char_count}',
        # Privacy (privacy-policy-enforcer)
        f'pii_tags: [{pii_tags_str}]',
        f'canonical_audience: {audience}',
        # ChatGPT-memory extension
        f'card_type: chatgpt-memory',
        f'chatgpt_memory_id: {mem_id}',
        f'chatgpt_memory_updated: {updated}',
        f'title: {yaml_escape(title)}',
        '---',
        '',
        f'# {title}',
        '',
        content,
        '',
        '---',
        '',
        f'_ChatGPT memory item exported {today}. Last updated: {updated}. Audience: `{audience}`._',
    ]

    path.write_text('\n'.join(fm), encoding='utf-8')
    return {
        'idx': idx,
        'filename': filename,
        'title': title,
        'tags': tags,
        'pii_tags': pii_tags,
        'audience': audience,
        'lang': lang_code,
        'mem_id': mem_id,
        'updated': updated,
    }


def write_index(output_dir, cards_meta):
    """Build INDEX.md with cards listing + tag matrix."""
    # Tag frequency
    tag_freq = {}
    for c in cards_meta:
        for t in c['tags']:
            tag_freq[t] = tag_freq.get(t, 0) + 1
    sorted_tags = sorted(tag_freq.items(), key=lambda x: -x[1])

    lines = [
        f'# Memory Cards Index -- 2026-05-14',
        '',
        f'Generated: {datetime.now().isoformat()}',
        f'Total cards: {len(cards_meta)}',
        '',
        '## Tag frequency',
        '',
        '| Tag | Count |',
        '|---|---|',
    ]
    for tag, count in sorted_tags:
        lines.append(f'| `{tag}` | {count} |')

    lines.extend(['', '## Cards by index', '', '| # | Title | Tags | Lang | Updated |', '|---|---|---|---|---|'])
    for c in cards_meta:
        tags_str = ', '.join(f'`{t}`' for t in c['tags'])
        title_clean = c['title'].replace('|', '\\|')
        lines.append(f'| {c["idx"]} | [[{c["filename"].replace(".md", "")}\\|{title_clean}]] | {tags_str} | {c["lang"]} | {c["updated"]} |')

    lines.extend(['', '## Cards by tag', ''])
    for tag in [t for t, _ in sorted_tags]:
        lines.append(f'### `{tag}` ({tag_freq[tag]} cards)\n')
        for c in cards_meta:
            if tag in c['tags']:
                lines.append(f'- [[{c["filename"].replace(".md", "")}|{c["title"]}]]')
        lines.append('')

    (output_dir / 'INDEX.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    args = parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8'))
    memories = data.get('memories', [])
    if not memories:
        print('No memories in input file.', file=sys.stderr)
        sys.exit(1)

    cards_dir = args.output / 'Cards'
    cards_dir.mkdir(parents=True, exist_ok=True)

    cards_meta = []
    for i, item in enumerate(memories, 1):
        meta = write_card(item, i, cards_dir)
        if meta:
            cards_meta.append(meta)
            if args.verbose:
                print(f'  {i:03d}: {meta["title"][:60]} [{", ".join(meta["tags"]) or "no-tags"}]')

    write_index(args.output, cards_meta)
    print(f'Wrote {len(cards_meta)} memory cards to {cards_dir}')
    print(f'Index: {args.output / "INDEX.md"}')


if __name__ == '__main__':
    main()
