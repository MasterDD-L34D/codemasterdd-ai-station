#!/usr/bin/env python3
"""
project-preview.py -- Per-project atomize preview, scoped output.

For each project subfolder in <export>/projects/<name>/json/, runs atomize on
its conv set + outputs Cards in <output>/<project_slug>/Cards/.
Uses project_name as collection (not BERTopic topic_label).

Useful for previewing target project content (e.g., Evo-Tactics) BEFORE the
full classify+atomize on combined dataset runs post-bulk.

Output structure:
  <output>/
    <project_slug>/
      Cards/
        <conv_short>_msg-NNN_role.md   (vault-convention frontmatter)
        <conv_short>_source.md          (companion)
      INDEX.md
  PROJECT_PREVIEW_INDEX.md (cross-project summary)
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--input', required=True, type=Path, help='brianjlacy export root (with projects/ subdir)')
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--min-msg-length', type=int, default=50)
    p.add_argument('--project-filter', help='Limit to projects matching substring (e.g., "Evo")')
    return p.parse_args()


def slugify(s, maxlen=60):
    if not s:
        return 'untitled'
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')[:maxlen] or 'untitled'


def extract_messages_from_mapping(conv_json):
    mapping = conv_json.get('mapping') or {}
    if not mapping:
        return []
    root_candidates = [nid for nid, node in mapping.items() if not node.get('parent')]
    if not root_candidates:
        return []

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
    messages = []
    cur, v = root_id, set()
    while cur and cur not in v:
        v.add(cur)
        node = mapping.get(cur)
        if not node:
            break
        msg = node.get('message')
        if msg and msg.get('content'):
            messages.append(msg)
        ch = node.get('children') or []
        cur = ch[0] if ch else None
    return messages


def message_to_text(msg):
    content = msg.get('content') or {}
    metadata = msg.get('metadata') or {}
    if metadata.get('is_visually_hidden_from_conversation'):
        return ''
    ct = content.get('content_type', '')
    if ct == 'text':
        return '\n'.join(p for p in content.get('parts', []) if isinstance(p, str))
    if ct == 'code':
        return '```\n' + (content.get('text', '') or '') + '\n```'
    if ct == 'multimodal_text':
        parts = []
        for p in content.get('parts', []):
            if isinstance(p, str):
                parts.append(p)
            elif isinstance(p, dict) and p.get('content_type') == 'image_asset_pointer':
                pointer = (p.get('asset_pointer') or '').replace('sediment://', '').replace('file-service://', '')
                parts.append(f'![image: {pointer}]')
        return '\n'.join(parts)
    if ct == 'thoughts':
        text = '\n'.join(p for p in content.get('parts', []) if isinstance(p, str))
        return f'<details>\n<summary>Thinking</summary>\n\n{text}\n\n</details>' if text.strip() else ''
    if ct in ('reasoning_recap', 'tether_browsing_display'):
        return '\n'.join(p for p in content.get('parts', []) if isinstance(p, str))
    return ''


def detect_language(text):
    it = len(re.findall(r'\b(che|della|degli|delle|sono|essere|sua|suo|nei|questo|questa|più|però|come|quindi|perché)\b', text, re.IGNORECASE))
    en = len(re.findall(r'\b(the|and|with|that|for|this|from|have|been|use|user)\b', text, re.IGNORECASE))
    if it > en:
        return 'it'
    if en > 3:
        return 'en'
    return 'mixed'


def yaml_escape(s):
    if not s:
        return '""'
    s = str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    return f'"{s}"'


def atomize_conv(conv_json, conv_path, project_slug, project_name, output_dir, min_msg_length):
    """Atomize one conv. Returns list of atom meta dicts."""
    messages = extract_messages_from_mapping(conv_json)
    conv_id = conv_json.get('id') or conv_json.get('conversation_id') or 'unknown'
    conv_id_short = conv_id[:8]
    conv_title = conv_json.get('title') or 'Untitled'

    # Pass 1: filter candidate atoms
    candidates = []
    for msg_idx, msg in enumerate(messages):
        role = (msg.get('author') or {}).get('role', 'unknown')
        if role not in ('user', 'assistant', 'tool'):
            continue
        text = message_to_text(msg).strip()
        if len(text) < min_msg_length:
            continue
        slug = f'{conv_id_short}_msg-{msg_idx:03d}_{role}'
        candidates.append({'msg_idx': msg_idx, 'role': role, 'text': text, 'msg': msg, 'slug': slug})

    if not candidates:
        return []

    # Pass 2: write with resolved prev/next backlinks
    today = datetime.now().strftime('%Y-%m-%d')
    atoms = []
    for i, atom in enumerate(candidates):
        prev_atom = candidates[i - 1] if i > 0 else None
        next_atom = candidates[i + 1] if i < len(candidates) - 1 else None

        text = atom['text']
        sha = hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]
        lang = detect_language(text)
        card_id = f'chatgpt-{project_slug}-{atom["slug"]}'

        fm = [
            '---',
            f'id: {card_id}',
            f'type: card',
            f'status: live',
            f'created: {today}',
            f'language: {lang}',
            f'collection: {project_slug}',
            f'tags: [card, {project_slug}, chatgpt-import, section-atomize, {lang}, role-{atom["role"]}, project-preview]',
            f'last_verified: {today}',
            f'source_ref: {yaml_escape(str(conv_path))}',
            f'source_section: "msg-{atom["msg_idx"]:03d}-{atom["role"]}"',
            f'source_sha256: {sha}',
            f'char_count: {len(text)}',
            f'card_type: chat-atom',
            f'role: {atom["role"]}',
            f'project_name: {yaml_escape(project_name)}',
            f'conv_id: {conv_id}',
            f'conv_title: {yaml_escape(conv_title)}',
            f'msg_idx: {atom["msg_idx"]}',
            f'msg_idx_total: {len(messages)}',
            f'model: {conv_json.get("default_model_slug") or conv_json.get("model") or ""}',
            f'create_time: {conv_json.get("create_time") or ""}',
            f'is_archived: {conv_json.get("is_archived", False)}',
            f'gizmo_id: {conv_json.get("gizmo_id") or ""}',
            '---',
            '',
            f'# {atom["role"].capitalize()} -- msg {atom["msg_idx"]}/{len(messages)}',
            '',
            f'> From conversation: [[{conv_id_short}_source|{conv_title}]]',
            f'> Project: `{project_name}` | Role: `{atom["role"]}` | msg `{atom["msg_idx"]}/{len(messages)}`',
            '',
            text,
            '',
        ]
        nav = []
        if prev_atom:
            nav.append(f'-- [[{prev_atom["slug"]}|<- prev ({prev_atom["role"]} {prev_atom["msg_idx"]})]]')
        if next_atom:
            nav.append(f'[[{next_atom["slug"]}|next ({next_atom["role"]} {next_atom["msg_idx"]}) ->]]')
        if nav:
            fm.extend(['---', ' '.join(nav), ''])

        card_path = output_dir / f'{atom["slug"]}.md'
        card_path.write_text('\n'.join(fm), encoding='utf-8')
        atoms.append({'slug': atom['slug'], 'role': atom['role'], 'msg_idx': atom['msg_idx']})

    # Source companion
    src_path = output_dir / f'{conv_id_short}_source.md'
    src_lines = [
        '---',
        f'id: chatgpt-{project_slug}-{conv_id_short}-source',
        f'type: card',
        f'status: live',
        f'created: {today}',
        f'collection: {project_slug}',
        f'tags: [card, {project_slug}, chatgpt-import, source]',
        f'last_verified: {today}',
        f'card_type: chat-conv-source',
        f'conv_id: {conv_id}',
        f'conv_title: {yaml_escape(conv_title)}',
        f'project_name: {yaml_escape(project_name)}',
        f'atom_count: {len(atoms)}',
        '---',
        '',
        f'# {conv_title}',
        '',
        f'> Source conversation. Project: `{project_name}`. {len(atoms)} atoms.',
        '',
        '## Atoms',
        '',
    ]
    for a in atoms:
        src_lines.append(f'- [[{a["slug"]}|{a["role"]} {a["msg_idx"]}]]')
    src_path.write_text('\n'.join(src_lines), encoding='utf-8')

    return atoms


def main():
    args = parse_args()
    proj_root = args.input / 'projects'
    if not proj_root.is_dir():
        print(f'ERROR: {proj_root} not found', file=sys.stderr)
        sys.exit(1)

    args.output.mkdir(parents=True, exist_ok=True)

    cross_proj_summary = []
    total_atoms = 0
    total_convs = 0

    for proj_dir in sorted(proj_root.iterdir()):
        if not proj_dir.is_dir():
            continue
        if args.project_filter and args.project_filter.lower() not in proj_dir.name.lower():
            continue

        proj_json_dir = proj_dir / 'json'
        if not proj_json_dir.is_dir():
            continue

        conv_files = sorted(proj_json_dir.glob('*.json'))
        if not conv_files:
            continue

        project_name = proj_dir.name.replace('_', ' ')
        project_slug = slugify(proj_dir.name, maxlen=40)
        proj_out = args.output / project_slug / 'Cards'
        proj_out.mkdir(parents=True, exist_ok=True)

        proj_atom_count = 0
        proj_conv_count = 0
        for conv_path in conv_files:
            try:
                conv_json = json.loads(conv_path.read_text(encoding='utf-8'))
                atoms = atomize_conv(conv_json, conv_path, project_slug, project_name, proj_out, args.min_msg_length)
                proj_atom_count += len(atoms)
                proj_conv_count += 1
            except (json.JSONDecodeError, OSError) as e:
                print(f'Skip {conv_path}: {e}', file=sys.stderr)

        # Per-project INDEX
        idx_lines = [
            '---',
            f'id: {project_slug}-preview-index',
            f'type: moc',
            f'status: live',
            f'created: {datetime.now().strftime("%Y-%m-%d")}',
            f'collection: {project_slug}',
            f'card_count: {proj_atom_count}',
            f'source_ref: chatgpt-export-2026-05-14/projects/{proj_dir.name}/',
            f'tags: [moc, {project_slug}, chatgpt-import, project-preview]',
            '---',
            '',
            f'# {project_name} — Preview MOC',
            '',
            f'Per-project atomize preview. {proj_conv_count} conv processed, {proj_atom_count} atoms.',
            '',
            '_Generated BEFORE final classify on combined dataset. Use for sanity preview only._',
            '',
            '## Cards',
            '',
        ]
        for card in sorted(proj_out.glob('*_source.md')):
            idx_lines.append(f'- [[{card.stem}|{card.stem}]]')
        (args.output / project_slug / 'INDEX.md').write_text('\n'.join(idx_lines), encoding='utf-8')

        cross_proj_summary.append({
            'slug': project_slug,
            'name': project_name,
            'conv_count': proj_conv_count,
            'atom_count': proj_atom_count,
        })
        total_atoms += proj_atom_count
        total_convs += proj_conv_count
        print(f'{project_name}: {proj_conv_count} conv -> {proj_atom_count} atoms', file=sys.stderr)

    # Cross-project summary
    summary_lines = [
        '---',
        f'id: chatgpt-project-preview-index',
        f'type: index',
        f'status: live',
        f'created: {datetime.now().strftime("%Y-%m-%d")}',
        f'collection: chatgpt-recovery-2026-05-14',
        f'tags: [index, chatgpt-import, project-preview]',
        '---',
        '',
        f'# ChatGPT Project Preview — Cross-project summary',
        '',
        f'Generated: {datetime.now().isoformat()}',
        f'Total projects processed: {len(cross_proj_summary)}',
        f'Total conv: {total_convs}',
        f'Total atoms: {total_atoms}',
        '',
        '_Per-project atomize preview (BEFORE final classify on combined dataset)._',
        '',
        '## Projects',
        '',
        '| Project | Conv | Atoms | Index |',
        '|---|---|---|---|',
    ]
    for p in cross_proj_summary:
        summary_lines.append(f'| {p["name"]} | {p["conv_count"]} | {p["atom_count"]} | [[{p["slug"]}/INDEX|{p["slug"]}]] |')

    (args.output / 'PROJECT_PREVIEW_INDEX.md').write_text('\n'.join(summary_lines), encoding='utf-8')
    print(f'\nTotal: {len(cross_proj_summary)} projects, {total_convs} conv, {total_atoms} atoms', file=sys.stderr)
    print(f'Output: {args.output}', file=sys.stderr)


if __name__ == '__main__':
    main()
