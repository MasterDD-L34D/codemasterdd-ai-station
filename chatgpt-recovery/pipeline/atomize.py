#!/usr/bin/env python3
"""
atomize.py -- Atomize conversations to per-message Cards for Obsidian vault.

Reads brianjlacy JSON export + topic-classified output from classify.py.
Outputs vault/Cards/{topic_label}/{conv_id12}_msg-{msg_idx:03d}_{role}.md
each containing a single self-contained message with backlinks.

Strategy:
  - User messages: kept as "questions" / "intents"
  - Assistant messages: kept as "answers" / "outputs"
  - Tool messages: kept as "context" if substantive (else skipped)
  - Each card has YAML frontmatter with topic_label + conv_id + role + msg_idx + timestamps
  - Each card has wikilinks to neighbors (prev/next) + back to source conv

Usage:
  python atomize.py \
    --input <export_root> \
    --classification <classify_output_dir> \
    --output <vault_cards_dir> \
    --min-msg-length 40
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from tqdm import tqdm


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--input', required=True, type=Path, help='brianjlacy export root')
    p.add_argument('--classification', required=True, type=Path, help='classify.py output dir (contains conversations-classified.json)')
    p.add_argument('--output', required=True, type=Path, help='Vault Cards output dir')
    p.add_argument('--min-msg-length', type=int, default=40, help='Min message char length to atomize')
    p.add_argument('--skip-tool-messages', action='store_true', default=False)
    p.add_argument('--max-msg-per-conv', type=int, default=0, help='0 = no limit')
    p.add_argument('--verbose', action='store_true')
    return p.parse_args()


def log(msg, *args):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', *args, file=sys.stderr)


def sanitize_filename(name):
    if not name:
        return 'untitled'
    s = re.sub(r'[<>:"/\\|?*]', '_', name)
    s = re.sub(r'\.{2,}', '_', s)
    s = re.sub(r'\s+', '_', s)
    return s[:80] or 'untitled'


def extract_messages_from_mapping(conv_json):
    mapping = conv_json.get('mapping') or {}
    if not mapping:
        return []
    root_candidates = [nid for nid, node in mapping.items() if not node.get('parent')]
    if not root_candidates:
        return []

    def reach(rid):
        c = 0
        cur = rid
        visited = set()
        while cur and cur not in visited:
            visited.add(cur)
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
    cur = root_id
    visited = set()
    while cur and cur not in visited:
        visited.add(cur)
        node = mapping.get(cur)
        if not node:
            break
        msg = node.get('message')
        if msg and msg.get('content'):
            messages.append(msg)
        children = node.get('children') or []
        cur = children[0] if children else None
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
        for part in content.get('parts', []):
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and part.get('content_type') == 'image_asset_pointer':
                pointer = (part.get('asset_pointer') or '').replace('sediment://', '').replace('file-service://', '')
                parts.append(f'![image: {pointer}]')
        return '\n'.join(parts)

    if ct == 'thoughts':
        text = '\n'.join(p for p in content.get('parts', []) if isinstance(p, str))
        return f'<details>\n<summary>Thinking</summary>\n\n{text}\n\n</details>' if text.strip() else ''

    if ct == 'reasoning_recap':
        text = '\n'.join(p for p in content.get('parts', []) if isinstance(p, str))
        return f'*Reasoning recap: {text}*' if text.strip() else ''

    if ct == 'tether_browsing_display':
        text = '\n'.join(p for p in content.get('parts', []) if isinstance(p, str))
        return f'> **Browsing Result:** {text}' if text.strip() else ''

    if ct == 'model_editable_context':
        return ''

    return ''


def yaml_escape(s):
    if not s:
        return '""'
    s = str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    return f'"{s}"'


def detect_language(text):
    """Heuristic: italian if dominant, else default english/mixed."""
    it_markers = len(re.findall(r'\b(che|della|degli|delle|sono|essere|sua|suo|nei|questo|questa|più|però|come|quindi|perché)\b', text, re.IGNORECASE))
    en_markers = len(re.findall(r'\b(the|and|with|that|for|this|from|have|been|use|user)\b', text, re.IGNORECASE))
    if it_markers > en_markers:
        return 'it'
    if en_markers > 3:
        return 'en'
    return 'mixed'


def build_card_content(doc, msg, msg_idx, role, total_msgs, conv_title, prev_atom, next_atom):
    """Build markdown content with resolved wikilinks (no wildcards).
    prev_atom / next_atom: dicts with 'filename_stem' or None.
    Length filtering is done in pass 1 by caller — no threshold here.

    Frontmatter aligned with vault-shared conventions (Explore agent finding 2026-05-14):
    id, type:card, status:live, created, language, collection, source_ref, source_sha256, char_count.
    """
    text = message_to_text(msg).strip()
    if not text:
        return None

    # Vault-convention required fields
    # NOTE: ChatGPT conv IDs are timestamp-sequential UUIDs; first 8 chars collide
    # heavily among conv from same time period. Use 12 chars for card_id uniqueness.
    full_conv_id = doc.get('id') or 'unknown'
    conv_id_uniq = full_conv_id[:12]  # filenames + wikilinks + card_id (collision-safe)
    collection = doc.get('topic_label') or 'unknown'
    card_id = f'chatgpt-{conv_id_uniq}-msg-{msg_idx:03d}-{role}'
    sha256 = hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]
    language = detect_language(text)
    char_count = len(text)
    today = datetime.now().strftime('%Y-%m-%d')

    # Source ref: relative path to source conversation JSON (Obsidian wikilink-ready)
    source_path_str = doc.get('source_path') or ''

    fm_lines = [
        '---',
        # Vault-convention universal (100%)
        f'id: {card_id}',
        f'type: card',
        f'status: live',
        f'created: {today}',
        # Common (80-100%)
        f'language: {language}',
        f'collection: {collection}',
        f'tags: [card, {collection}, chatgpt-import, section-atomize, {language}, role-{role}]',
        f'last_verified: {today}',
        f'source_ref: {yaml_escape(source_path_str)}',
        # Metadata (60-95%)
        f'source_section: "msg-{msg_idx:03d}-{role}"',
        f'source_sha256: {sha256}',
        f'char_count: {char_count}',
        # ChatGPT-specific (extension)
        f'card_type: chat-atom',
        f'role: {role}',
        f'topic_label: {doc["topic_label"]}',
        f'topic_id: {doc["topic_id"]}',
        f'conv_id: {doc["id"]}',
        f'conv_title: {yaml_escape(conv_title)}',
        f'msg_idx: {msg_idx}',
        f'msg_idx_total: {total_msgs}',
        f'project_name: {yaml_escape(doc.get("project_name") or "")}',
        f'model: {doc.get("model") or ""}',
        f'create_time: {doc.get("create_time") or ""}',
        f'gizmo_id: {doc.get("gizmo_id") or ""}',
        f'is_archived: {doc.get("is_archived", False)}',
        '---',
        '',
    ]

    body_lines = [
        f'# {role.capitalize()} -- msg {msg_idx}/{total_msgs}',
        '',
        f'> From conversation: [[{doc["id"][:12]}_source|{conv_title}]]',
        f'> Topic: `{doc["topic_label"]}` | Role: `{role}` | msg `{msg_idx}/{total_msgs}`',
        '',
        text,
        '',
    ]

    # Navigation backlinks (resolved, no wildcards)
    nav_parts = []
    if prev_atom:
        nav_parts.append(f'-- [[{prev_atom["filename_stem"]}|<- previous ({prev_atom["role"]} {prev_atom["msg_idx"]})]]')
    if next_atom:
        nav_parts.append(f'[[{next_atom["filename_stem"]}|next ({next_atom["role"]} {next_atom["msg_idx"]}) ->]]')

    if nav_parts:
        body_lines.extend(['---', ' '.join(nav_parts), ''])

    return '\n'.join(fm_lines) + '\n'.join(body_lines)


def write_conv_source_card(source_path_out, doc, conv_title, all_atoms):
    """Companion card per conversazione completa with list of atom cards + source ref.
    Vault-convention compliant frontmatter (id/type/status/created/collection)."""
    today = datetime.now().strftime('%Y-%m-%d')
    full_conv_id = doc.get("id") or "unknown"
    conv_id_uniq = full_conv_id[:12]
    collection = doc.get("topic_label") or "unknown"
    fm_lines = [
        '---',
        f'id: chatgpt-{conv_id_uniq}-source',
        f'type: card',
        f'status: live',
        f'created: {today}',
        f'collection: {collection}',
        f'tags: [card, {collection}, chatgpt-import, source]',
        f'last_verified: {today}',
        f'source_ref: {yaml_escape(doc.get("source_path") or "")}',
        f'atom_count: {len(all_atoms)}',
        f'card_type: chat-conv-source',
        f'conv_id: {doc["id"]}',
        f'conv_title: {yaml_escape(conv_title)}',
        f'topic_label: {doc["topic_label"]}',
        f'topic_id: {doc["topic_id"]}',
        f'project_name: {yaml_escape(doc.get("project_name") or "")}',
        f'model: {doc.get("model") or ""}',
        f'create_time: {doc.get("create_time") or ""}',
        '---',
        '',
        f'# {conv_title}',
        '',
        f'> Source conversation. Topic: `{doc["topic_label"]}`. {len(all_atoms)} atoms.',
        f'> Original brianjlacy export: `{doc.get("source_path", "")}`',
        '',
        '## Atoms',
        '',
    ]
    for atom in all_atoms:
        fm_lines.append(f'- [[{atom["filename_stem"]}|{atom["role"]} {atom["msg_idx"]}]]')
    source_path_out.write_text('\n'.join(fm_lines), encoding='utf-8')


def main():
    args = parse_args()

    classification_json = args.classification / 'conversations-classified.json'
    if not classification_json.is_file():
        log(f'ERROR: {classification_json} missing. Run classify.py first.')
        sys.exit(1)

    docs_classified = json.loads(classification_json.read_text(encoding='utf-8'))
    log(f'Loaded {len(docs_classified)} classified docs')

    args.output.mkdir(parents=True, exist_ok=True)

    stats = {'atoms_written': 0, 'convs_processed': 0, 'skipped': 0}

    for doc in tqdm(docs_classified, desc='atomize'):
        source_path = Path(doc['source_path'])
        if not source_path.is_file():
            log(f'Skipping (source missing): {source_path}')
            stats['skipped'] += 1
            continue

        try:
            conv_json = json.loads(source_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError) as e:
            log(f'Skipping (read error): {source_path}: {e}')
            stats['skipped'] += 1
            continue

        messages = extract_messages_from_mapping(conv_json)
        conv_title = conv_json.get('title') or doc.get('title') or 'Untitled'
        # 12-char prefix matches card_id uniqueness (ChatGPT UUIDs are timestamp-
        # sequential; 8-char prefixes collide among same-period convs -> filename
        # overwrite). Keep filenames/wikilinks consistent with card_id.
        conv_id_uniq = (doc.get('id') or 'unknown')[:12]

        # Topic-based folder
        topic_label = doc.get('topic_label') or 'unknown'
        topic_folder = args.output / topic_label
        topic_folder.mkdir(exist_ok=True)

        # Pass 1: collect candidate atoms (filter by min-length + role)
        candidate_atoms = []
        msg_count_atomized = 0
        for msg_idx, msg in enumerate(messages):
            if args.max_msg_per_conv and msg_count_atomized >= args.max_msg_per_conv:
                break

            role = (msg.get('author') or {}).get('role', 'unknown')
            allowed_roles = {'user', 'assistant'}
            if not args.skip_tool_messages:
                allowed_roles.add('tool')
            if role not in allowed_roles:
                continue

            text = message_to_text(msg).strip()
            if len(text) < args.min_msg_length:
                continue

            filename_stem = f'{conv_id_uniq}_msg-{msg_idx:03d}_{role}'
            candidate_atoms.append({
                'msg_idx': msg_idx,
                'role': role,
                'filename_stem': filename_stem,
                'msg': msg,
            })
            msg_count_atomized += 1

        # Pass 2: write with resolved prev/next backlinks
        all_atoms = []
        for i, atom in enumerate(candidate_atoms):
            prev_atom = candidate_atoms[i - 1] if i > 0 else None
            next_atom = candidate_atoms[i + 1] if i < len(candidate_atoms) - 1 else None
            card_path = topic_folder / f'{atom["filename_stem"]}.md'
            content = build_card_content(doc, atom['msg'], atom['msg_idx'], atom['role'],
                                          len(messages), conv_title, prev_atom, next_atom)
            if content:
                card_path.parent.mkdir(parents=True, exist_ok=True)
                card_path.write_text(content, encoding='utf-8')
                all_atoms.append({'msg_idx': atom['msg_idx'], 'role': atom['role'], 'filename_stem': atom['filename_stem']})
                stats['atoms_written'] += 1

        # Companion source card
        if all_atoms:
            source_card_path = topic_folder / f'{conv_id_uniq}_source.md'
            write_conv_source_card(source_card_path, doc, conv_title, all_atoms)
            stats['convs_processed'] += 1

    log(f'\n=== Atomize stats ===')
    log(f'Atoms written: {stats["atoms_written"]}')
    log(f'Conversations processed: {stats["convs_processed"]}')
    log(f'Skipped (read err / missing source): {stats["skipped"]}')
    log(f'Output: {args.output}')


if __name__ == '__main__':
    main()
