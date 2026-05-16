#!/usr/bin/env python3
"""
build-moc-stub.py -- Generate Atlas MOC skeleton from classification + cross-ref map.

Output: chatgpt-recovery-2026-05-14-moc.md ready for vault Atlas/ folder.
Frontmatter follows vault MOC convention (type:moc + standard fields).
Sections: stats, topics table, per-topic cards listing, cross-ref to vault Spaces.
"""

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--classification', required=True, type=Path, help='conversations-classified.json source')
    p.add_argument('--cross-ref', type=Path, help='vault-cross-reference-map.yaml (optional, for space hints)')
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--export-date', default='2026-05-14')
    return p.parse_args()


def main():
    args = parse_args()
    classified_path = args.classification / 'conversations-classified.json'
    docs = json.loads(classified_path.read_text(encoding='utf-8'))

    by_topic = defaultdict(list)
    for d in docs:
        by_topic[d.get('topic_id', -1)].append(d)

    labels = {}
    for d in docs:
        tid = d.get('topic_id', -1)
        labels[tid] = d.get('topic_label', f'topic-{tid}')

    today = datetime.now().strftime('%Y-%m-%d')

    lines = [
        '---',
        f'id: chatgpt-recovery-{args.export_date}-moc',
        f'type: moc',
        f'status: live',
        f'created: {today}',
        f'collection: chatgpt-recovery-{args.export_date}',
        f'card_count: {len(docs)}',
        f'topic_count: {len(by_topic)}',
        f'source_ref: Sources/raw/chatgpt-export-{args.export_date}/',
        f'tags: [moc, chatgpt-recovery, chatgpt-import, raw-collection]',
        f'last_verified: {today}',
        '---',
        '',
        f'# ChatGPT Recovery — MOC ({args.export_date})',
        '',
        f'Map of Content for ChatGPT Business workspace recovery operation on {args.export_date}.',
        f'Pipeline: brianjlacy/export-chatgpt → BERTopic clustering → Qwen 14B Q2 labeling → atomize per-message Cards.',
        '',
        '## Stats',
        '',
        f'- Conversations classified: **{len(docs)}**',
        f'- Topics detected: **{len(by_topic)}** (incl. outliers)',
        f'- Outliers (-1): {len(by_topic.get(-1, []))} conv ({100*len(by_topic.get(-1, []))/len(docs):.1f}%)',
        f'- Atomization method: per-message section-atomize with vault-convention frontmatter',
        '',
        '## Source',
        '',
        f'- Raw export: [[../Sources/raw/chatgpt-export-{args.export_date}/]]',
        f'- Memory items: [[../Sources/raw/chatgpt-export-{args.export_date}/_processed/memory/INDEX|83 memory cards]]',
        f'- Custom instructions: [[../Sources/raw/chatgpt-export-{args.export_date}/custom-instructions]]',
        f'- Pipeline runbook: [chatgpt-recovery/](https://github.com/MasterDD-L34D/codemasterdd-ai-station/tree/main/chatgpt-recovery)',
        '',
        '## Topics overview',
        '',
        '| Topic ID | Label | Docs | Sample title |',
        '|---|---|---|---|',
    ]

    for tid in sorted(by_topic.keys(), key=lambda x: (x == -1, x)):
        topic_docs = by_topic[tid]
        label = labels.get(tid, f'topic-{tid}')
        sample = topic_docs[0].get('title', '(no title)')[:60].replace('|', '\\|')
        lines.append(f'| {tid} | [[#Topic {tid}: `{label}`|{label}]] | {len(topic_docs)} | {sample} |')

    lines.extend([
        '',
        '## Per-topic Cards',
        '',
    ])

    for tid in sorted(by_topic.keys(), key=lambda x: (x == -1, x)):
        topic_docs = by_topic[tid]
        label = labels.get(tid, f'topic-{tid}')
        lines.append(f'### Topic {tid}: `{label}` ({len(topic_docs)} docs)')
        lines.append('')

        # Sample first 10 + last 5 conv titles + count remaining
        n = len(topic_docs)
        if n <= 15:
            preview = topic_docs
        else:
            preview = topic_docs[:10] + [None] + topic_docs[-5:]

        for d in preview:
            if d is None:
                lines.append(f'- ... ({n-15} more)')
                continue
            conv_id_short = (d.get('id') or 'unknown')[:8]
            title = d.get('title', '(no title)').replace('|', '\\|')
            proj = f" [{d.get('project_name')}]" if d.get('project_name') else ''
            create = d.get('create_time', '')
            if isinstance(create, (int, float)):
                try:
                    create = datetime.fromtimestamp(create).strftime('%Y-%m-%d')
                except Exception:
                    create = ''

            lines.append(f'- `{conv_id_short}` **{title}**{proj} ({create})')
            lines.append(f'  - Cards: [[../_processed/Cards/{label}/{conv_id_short}_source|→ source]]')

        lines.append('')

    lines.extend([
        '## Review workflow',
        '',
        f'1. Open [[../_processed/classification/topics-summary|topics-summary.md]] for full topic detail',
        f'2. Run sample-cards.py + review [[review-sample-{args.export_date}|review-sample-{args.export_date}.md]] (~143 cards)',
        f'3. For each topic mark disposition: PROMOTE / RENAME-THEN-PROMOTE / HOLD / DISCARD',
        f'4. Run promote-cards.py with dry-run, then full',
        f'5. Promoted cards land in `Spaces/<space>/_imported-{args.export_date}/<topic>/`',
        '',
        '## Promotion log',
        '',
        f'_(filled by promote-cards.py post-review)_',
        '',
        '## Caveats',
        '',
        '- Some image/file downloads failed (HTTP 422 brianjlacy multi-part file_id bug). See `.export-progress.json:failedFileIds`.',
        '- LLM topic labels via qwen2.5-coder:14b-instruct-q2_K — review for italian-language nuance',
        '- Multi-root mapping handled via "longest chain" heuristic (atomize.py:reach)',
        '- Bearer token (used for fetch) MUST be rotated post-pipeline (P0 OWASP — see [agent-lessons](agent-lessons-2026-05-14.md))',
        '',
        '## Cross-references',
        '',
        f'- ADR governance: [[../../docs/adr/0030-chatgpt-recovery-classification-pipeline|ADR-0030]]',
        f'- Agent lessons: [chatgpt-recovery/agent-lessons-2026-05-14.md](https://github.com/MasterDD-L34D/codemasterdd-ai-station/blob/main/chatgpt-recovery/agent-lessons-2026-05-14.md)',
        f'- Vault cross-reference map: [chatgpt-recovery/vault-cross-reference-map.yaml](https://github.com/MasterDD-L34D/codemasterdd-ai-station/blob/main/chatgpt-recovery/vault-cross-reference-map.yaml)',
        '',
    ])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'MOC stub written to {args.output}')


if __name__ == '__main__':
    main()
