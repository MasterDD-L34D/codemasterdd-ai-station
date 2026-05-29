#!/usr/bin/env python3
"""
fetch-memories-and-instructions.py -- Direct API fetch for ChatGPT Memory items + Custom Instructions.

Replaces MemPort Chrome extension + manual Custom Instructions copy.
Uses same bearer token as brianjlacy bulk export. Only 2 API calls (tiny scope).

Output:
  <output>/memory-items.json       -- full /backend-api/memories response
  <output>/memory-items.md         -- human-readable Markdown
  <output>/custom-instructions.json -- full /backend-api/user_system_messages response
  <output>/custom-instructions.md   -- human-readable Markdown

Usage:
  CHATGPT_BEARER_TOKEN=eyJ... python fetch-memories-and-instructions.py --output <dir>
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

API_BASE = 'https://chatgpt.com/backend-api'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--bearer', help='Bearer token (or CHATGPT_BEARER_TOKEN env var)')
    p.add_argument('--account-id', help='Teams account ID (or CHATGPT_ACCOUNT_ID env var)')
    p.add_argument('--output', required=True, type=Path)
    return p.parse_args()


def api_get(url, bearer, account_id):
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {bearer}')
    req.add_header('Accept', 'application/json')
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', USER_AGENT)
    if account_id:
        req.add_header('chatgpt-account-id', account_id)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return 0, None


def fmt_ts(ts):
    if not ts:
        return ''
    try:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts).isoformat()
        return str(ts)
    except Exception:
        return str(ts)


def memory_to_md(data):
    lines = [
        f'# ChatGPT Memory Items Export -- {datetime.now().isoformat()}',
        '',
        f'Memory tokens used: {data.get("memory_num_tokens", "?")} / {data.get("memory_max_tokens", "?")}',
        f'Total items: {len(data.get("memories", []))}',
        '',
        '## Items',
        '',
    ]
    for i, m in enumerate(data.get('memories', [])):
        lines.append(f'### {i + 1}. (id `{m.get("id", "?")}`)')
        lines.append('')
        lines.append(m.get('content', m.get('text', '_(no content field)_')))
        meta_bits = []
        if m.get('created_at'):
            meta_bits.append(f'created: {fmt_ts(m["created_at"])}')
        if m.get('updated_at'):
            meta_bits.append(f'updated: {fmt_ts(m["updated_at"])}')
        if meta_bits:
            lines.append('')
            lines.append(f'_{" | ".join(meta_bits)}_')
        lines.append('')
    return '\n'.join(lines)


def instructions_to_md(data):
    lines = [
        f'# Custom Instructions Export -- {datetime.now().isoformat()}',
        '',
        f'Enabled: {data.get("enabled", "?")}',
        f'Personality type: `{data.get("personality_type_selection", "default")}`',
        f'Traits enabled: {data.get("traits_enabled", "?")}',
        '',
        '## About you',
        '',
        data.get('about_user_message') or '_(empty)_',
        '',
        '## How would you like ChatGPT to respond',
        '',
        data.get('about_model_message') or '_(empty)_',
        '',
        '## Name preference',
        '',
        data.get('name_user_message') or '_(empty)_',
        '',
        '## Role preference',
        '',
        data.get('role_user_message') or '_(empty)_',
        '',
        '## Traits (model)',
        '',
        data.get('traits_model_message') or '_(empty)_',
        '',
        '## Personality traits',
        '',
    ]
    pt = data.get('personality_traits') or []
    if isinstance(pt, list):
        for t in pt:
            lines.append(f'- {t}')
    else:
        lines.append(str(pt))
    lines.append('')
    lines.append('## Other')
    lines.append('')
    lines.append(data.get('other_user_message') or '_(empty)_')
    lines.append('')
    lines.append('## Disabled tools')
    lines.append('')
    dt = data.get('disabled_tools') or []
    if isinstance(dt, list):
        for t in dt:
            lines.append(f'- {t}')
    else:
        lines.append(str(dt))
    return '\n'.join(lines)


def main():
    args = parse_args()
    if args.bearer:
        print('WARNING: passing --bearer via CLI exposes token via process arg list (CWE-214). Prefer CHATGPT_BEARER_TOKEN env var sourced from env-file with restricted ACL.', file=sys.stderr)
    bearer = (args.bearer or os.environ.get('CHATGPT_BEARER_TOKEN', '')).strip()
    if bearer.startswith('Bearer '):
        bearer = bearer[7:]
    account_id = args.account_id or os.environ.get('CHATGPT_ACCOUNT_ID')

    if not bearer:
        print('ERROR: bearer token missing', file=sys.stderr)
        sys.exit(1)

    args.output.mkdir(parents=True, exist_ok=True)

    print('Fetching memories...')
    status, mem_data = api_get(f'{API_BASE}/memories', bearer, account_id)
    if status == 200 and mem_data:
        (args.output / 'memory-items.json').write_text(json.dumps(mem_data, indent=2, ensure_ascii=False), encoding='utf-8')
        (args.output / 'memory-items.md').write_text(memory_to_md(mem_data), encoding='utf-8')
        print(f'  OK: {len(mem_data.get("memories", []))} items saved')
    else:
        print(f'  FAILED: status={status}')

    print('Fetching custom instructions...')
    status, ci_data = api_get(f'{API_BASE}/user_system_messages', bearer, account_id)
    if status == 200 and ci_data:
        (args.output / 'custom-instructions.json').write_text(json.dumps(ci_data, indent=2, ensure_ascii=False), encoding='utf-8')
        (args.output / 'custom-instructions.md').write_text(instructions_to_md(ci_data), encoding='utf-8')
        print('  OK: instructions saved')
    else:
        print(f'  FAILED: status={status}')

    print(f'\nOutput: {args.output}')


if __name__ == '__main__':
    main()
