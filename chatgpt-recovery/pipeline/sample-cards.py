#!/usr/bin/env python3
"""
sample-cards.py -- Stratified review sample for ChatGPT atomized Cards (Plan Phase 4).

Reads classification output + Cards directory, generates a stratified sample per topic:
  sample_size = max(5, ceil(sqrt(topic_doc_count)))

Sampling: random uniform within topic (seeded for reproducibility).

NOTE (harsh-reviewer P0 fix 2026-05-15): earlier docstring promised "medoid + 2 farthest
+ N-3 random" but the embedding-based selection branch was unreachable dead code (centroids
read from BERTopic but per-doc embeddings never cached). Removed false claim. To add real
medoid sampling, persist per-doc embeddings during classify.py + load here.

Output: review-sample-<date>.md with checkbox UI per topic, ready for Eduardo to mark
disposition (PROMOTE / RENAME / HOLD / DISCARD).

Usage:
  python sample-cards.py \
    --classification <classify_output_dir> \
    --cards <atomize_output_dir> \
    --output <review_dir>/review-sample-2026-05-14.md
"""

import argparse
import json
import math
import random
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--classification', required=True, type=Path, help='Dir with conversations-classified.json + bertopic-model/')
    p.add_argument('--cards', required=True, type=Path, help='Atomize Cards dir (used to verify card existence)')
    p.add_argument('--output', required=True, type=Path, help='Output markdown review file')
    p.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    p.add_argument('--min-sample', type=int, default=5, help='Minimum sample size per topic')
    # NOTE: --no-embeddings flag removed (was dead code per harsh-reviewer P0 #4 2026-05-15)
    return p.parse_args()


def load_classification(class_dir: Path):
    data_path = class_dir / 'conversations-classified.json'
    if not data_path.is_file():
        print(f'ERROR: {data_path} missing. Run classify.py first.', file=sys.stderr)
        sys.exit(1)
    return json.loads(data_path.read_text(encoding='utf-8'))


def sample_topic(docs_in_topic: list, sample_size: int, seed: int):
    """Select sample_size docs from topic via random uniform (seeded).
    Returns: (sample list, method-string).
    """
    if len(docs_in_topic) <= sample_size:
        return docs_in_topic[:], 'all (small cluster)'
    rnd = random.Random(seed)
    sample = rnd.sample(docs_in_topic, sample_size)
    return sample, 'random uniform (seeded)'


def main():
    args = parse_args()

    classified_docs = load_classification(args.classification)
    print(f'Loaded {len(classified_docs)} classified docs', file=sys.stderr)

    # Group by topic
    by_topic = defaultdict(list)
    for d in classified_docs:
        by_topic[d.get('topic_id', -1)].append(d)

    # Topic labels
    labels = {}
    for d in classified_docs:
        tid = d.get('topic_id', -1)
        labels[tid] = d.get('topic_label', f'topic-{tid}')

    # Build review markdown
    today = datetime.now().strftime('%Y-%m-%d')
    lines = [
        f'# ChatGPT Recovery -- Review Sample ({today})',
        '',
        f'Generated: {datetime.now().isoformat()}',
        f'Total classified docs: {len(classified_docs)}',
        f'Topics (incl. outliers): {len(by_topic)}',
        '',
        '## Instructions',
        '',
        'For each topic below: open the sample cards, mark disposition. Then save this file.',
        'Pipeline `promote-cards.py` reads this file (looks for `disposition: <value>` per topic).',
        '',
        'Dispositions:',
        '- `PROMOTE`: copy cards to canonical Spaces/<space>/_imported-2026-05-14/',
        '- `RENAME-THEN-PROMOTE`: rename topic_label first (set `rename_to: <new-label>`), then promote',
        '- `HOLD`: leave in staging _processed/Cards/ (review later)',
        '- `DISCARD`: delete from staging (not eligible for vault)',
        '',
        '---',
        '',
    ]

    for tid in sorted(by_topic.keys(), key=lambda x: (x == -1, x)):
        topic_docs = by_topic[tid]
        label = labels.get(tid, f'topic-{tid}')

        sample_size = max(args.min_sample, math.ceil(math.sqrt(len(topic_docs))))
        sample_size = min(sample_size, len(topic_docs))

        sample, method = sample_topic(topic_docs, sample_size, seed=args.seed + tid)

        # Build section
        lines.append(f'## Topic {tid}: `{label}` ({len(topic_docs)} docs)')
        lines.append('')
        lines.append(f'**Sample size**: {sample_size} (sampling: {method})')
        lines.append('')
        lines.append('```yaml')
        lines.append(f'topic_id: {tid}')
        lines.append(f'topic_label: {label}')
        lines.append(f'doc_count: {len(topic_docs)}')
        lines.append('disposition: HOLD  # PROMOTE / RENAME-THEN-PROMOTE / HOLD / DISCARD')
        lines.append('rename_to:    # (fill if RENAME-THEN-PROMOTE)')
        lines.append('target_space: # auto-derived from vault-cross-reference-map.yaml, override if needed')
        lines.append('notes:        # optional Eduardo notes')
        lines.append('```')
        lines.append('')
        lines.append('### Sample cards')
        lines.append('')

        for s in sample:
            conv_id_short = (s.get('id') or 'unknown')[:8]
            title = s.get('title', '(no title)')[:80].replace('|', '\\|')
            proj = f" [{s.get('project_name')}]" if s.get('project_name') else ''
            archived = ' [ARCHIVED]' if s.get('is_archived') else ''
            msg_count = s.get('message_count', '?')
            create = s.get('create_time', '?')
            if isinstance(create, (int, float)):
                try:
                    create = datetime.fromtimestamp(create).strftime('%Y-%m-%d')
                except Exception:
                    create = '?'

            cards_dir = args.cards / label
            card_pattern = f'{conv_id_short}_*'
            existing_cards = list(cards_dir.glob(f'{card_pattern}.md')) if cards_dir.is_dir() else []

            lines.append(f'- [ ] `{conv_id_short}` **{title}**{proj}{archived} -- {msg_count} msgs, {create}')
            if existing_cards:
                lines.append(f'  - Cards: {len(existing_cards)} atoms in [[{label}/]]')
                # Link to source card + first atom
                lines.append(f'  - Source: [[{label}/{conv_id_short}_source|{title}]]')

        lines.append('')
        lines.append('---')
        lines.append('')

    # Footer with summary
    total_sample = sum(max(args.min_sample, math.ceil(math.sqrt(len(by_topic[t])))) for t in by_topic.keys())
    lines.append('## Summary')
    lines.append('')
    lines.append(f'- Total topics: {len(by_topic)}')
    lines.append(f'- Total docs: {len(classified_docs)}')
    lines.append(f'- Estimated review effort: ~{total_sample} cards across all topics')
    lines.append('- Sampling method: sqrt-based stratification (Plan agent Phase 4 recommendation)')
    lines.append('')

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote review sample to {args.output}', file=sys.stderr)
    print(f'Total topics: {len(by_topic)}, estimated review effort: ~{total_sample} cards', file=sys.stderr)


if __name__ == '__main__':
    main()
