#!/usr/bin/env python3
"""
auto-audit.py -- Auto-fill audit checklist via ChatGPT backend-api calls.

Replaces manual UI counting (sections B-G of 01-PREFLIGHT-AUDIT.md) with
direct API probing. Uses same bearer token that brianjlacy will use for export.

Probes:
  - /backend-api/me                           -> user profile
  - /backend-api/accounts/check               -> Teams account info
  - /backend-api/conversations?limit=1        -> total regular conversations
  - /backend-api/conversations?is_archived=true&limit=1 -> archived count
  - /backend-api/gizmos/snorlax/sidebar       -> projects list (snorlax type)
  - /backend-api/gizmos/mine                  -> owned Custom GPTs (best-effort)
  - /backend-api/user_system_messages         -> custom instructions
  - /backend-api/memories                     -> memory items (best-effort)

Output: YAML audit decisions matrix + recommended brianjlacy flags.

Usage:
  CHATGPT_BEARER_TOKEN=eyJ... python auto-audit.py --output audit-result.yaml
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

API_BASE = 'https://chatgpt.com/backend-api'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--bearer', help='Bearer token (or CHATGPT_BEARER_TOKEN env var)')
    p.add_argument('--account-id', help='Teams account ID (auto-detected from JWT if absent)')
    p.add_argument('--output', type=Path, default=Path('audit-result.yaml'), help='Output YAML file')
    p.add_argument('--delay', type=float, default=2.0, help='Delay between probes (seconds)')
    p.add_argument('--verbose', action='store_true')
    return p.parse_args()


def log(msg, *args):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}', *args, file=sys.stderr)


def vlog(msg, *args):
    pass  # set via --verbose below


def decode_jwt_payload(token):
    """Decode JWT middle segment (no signature verification)."""
    import base64
    parts = token.split('.')
    if len(parts) != 3:
        return None
    try:
        payload_b64 = parts[1]
        # Add padding
        payload_b64 += '=' * (-len(payload_b64) % 4)
        payload = base64.urlsafe_b64decode(payload_b64)
        return json.loads(payload)
    except Exception:
        return None


def api_get(url, bearer, account_id=None, timeout=30):
    """GET request with auth headers. Returns parsed JSON or None on error."""
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {bearer}')
    req.add_header('Accept', 'application/json')
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', USER_AGENT)
    if account_id:
        req.add_header('chatgpt-account-id', account_id)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode('utf-8')
            return {'status': resp.status, 'data': json.loads(body)}
    except urllib.error.HTTPError as e:
        return {'status': e.code, 'data': None, 'error': str(e)}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        return {'status': 0, 'data': None, 'error': str(e)}


def probe_user_profile(bearer, account_id):
    log('Probing /backend-api/me ...')
    r = api_get(f'{API_BASE}/me', bearer, account_id)
    if r['status'] == 200:
        d = r['data']
        return {
            'email': d.get('email'),
            'name': d.get('name'),
            'phone_number': d.get('phone_number'),
            'has_subscription': bool(d.get('subscription_plan')),
            'plan': d.get('subscription_plan'),
        }
    log(f'  Failed: status={r["status"]} err={r.get("error")}')
    return {'error': r.get('error') or f'HTTP {r["status"]}'}


def probe_teams_account(bearer):
    log('Probing /backend-api/accounts/check ...')
    r = api_get(f'{API_BASE}/accounts/check/v4-2023-04-27', bearer)
    if r['status'] == 200:
        d = r['data']
        accounts = d.get('accounts', {})
        # First key is usually default account
        result = []
        for k, v in accounts.items():
            account = v.get('account', {})
            result.append({
                'account_id': account.get('account_id'),
                'name': account.get('name'),
                'plan_type': account.get('plan_type'),
                'workspace_name': v.get('workspace_name'),
                'role': v.get('role'),
                'is_business_user': account.get('is_business_user'),
            })
        return result
    log(f'  Failed: status={r["status"]} err={r.get("error")}')
    return [{'error': r.get('error') or f'HTTP {r["status"]}'}]


def probe_conversations_count(bearer, account_id, is_archived=False):
    log(f'Probing /backend-api/conversations (archived={is_archived}) ...')
    url = f'{API_BASE}/conversations?offset=0&limit=1&order=updated&is_archived={"true" if is_archived else "false"}'
    r = api_get(url, bearer, account_id)
    if r['status'] == 200:
        d = r['data']
        return {
            'total': d.get('total', 0),
            'has_items': bool(d.get('items')),
            'sample_title': (d.get('items') or [{}])[0].get('title') if d.get('items') else None,
        }
    log(f'  Failed: status={r["status"]} err={r.get("error")}')
    return {'error': r.get('error') or f'HTTP {r["status"]}'}


def probe_projects(bearer, account_id):
    log('Probing /backend-api/gizmos/snorlax/sidebar ...')
    projects = []
    cursor = None
    pages = 0
    while True:
        url = f'{API_BASE}/gizmos/snorlax/sidebar?owned_only=true&conversations_per_gizmo=0'
        if cursor:
            url += f'&cursor={urllib.parse.quote(cursor)}'
        r = api_get(url, bearer, account_id)
        if r['status'] != 200:
            log(f'  Failed: status={r["status"]} err={r.get("error")}')
            return {'error': r.get('error') or f'HTTP {r["status"]}', 'projects': projects}

        d = r['data']
        for item in d.get('items', []):
            g = (item.get('gizmo') or {}).get('gizmo') or item.get('gizmo') or {}
            if not g.get('id'):
                continue
            projects.append({
                'id': g.get('id'),
                'name': (g.get('display') or {}).get('name') or 'Untitled',
                'num_interactions': g.get('num_interactions', 0),
                'files_count': len((item.get('gizmo') or {}).get('files', [])),
            })
        cursor = d.get('cursor')
        pages += 1
        if not cursor or pages >= 20:  # safety cap
            break
        time.sleep(0.5)

    return {'count': len(projects), 'projects': projects}


def probe_custom_gpts_owned(bearer, account_id):
    """Best-effort: try multiple endpoint variants."""
    log('Probing Custom GPTs (multiple endpoint attempts) ...')
    endpoints = [
        '/gizmos/mine',
        '/gizmos/discovery/mine',
        '/gizmos/g-discovery/mine',
        '/me/gizmos',
    ]
    for ep in endpoints:
        url = f'{API_BASE}{ep}'
        log(f'  Trying {ep} ...')
        r = api_get(url, bearer, account_id)
        if r['status'] == 200:
            d = r['data']
            items = d.get('items') or d.get('gizmos') or (d if isinstance(d, list) else [])
            return {
                'endpoint': ep,
                'count': len(items),
                'gpts': [
                    {
                        'id': g.get('id') or g.get('short_url'),
                        'name': (g.get('display') or {}).get('name') or g.get('name'),
                        'created_at': g.get('created_at'),
                    } for g in items
                ][:30],
            }
        time.sleep(0.3)
    return {'error': 'No working endpoint found', 'count': None}


def probe_memories(bearer, account_id):
    """Best-effort: ChatGPT Memory items."""
    log('Probing memory items ...')
    endpoints = [
        '/memories',
        '/me/memories',
        '/user_system_messages',
    ]
    results = {}
    for ep in endpoints:
        url = f'{API_BASE}{ep}'
        log(f'  Trying {ep} ...')
        r = api_get(url, bearer, account_id)
        results[ep] = {'status': r['status'], 'has_data': r['data'] is not None}
        if r['status'] == 200:
            d = r['data']
            results[ep]['summary'] = {
                'keys': list(d.keys()) if isinstance(d, dict) else None,
                'list_count': len(d) if isinstance(d, list) else None,
                'memories_count': len(d.get('memories', [])) if isinstance(d, dict) else None,
            }
        time.sleep(0.3)
    return results


def derive_recommendations(audit):
    """Generate recommended brianjlacy flags + path decisions based on counts."""
    recs = {
        'brianjlacy_flags': [],
        'memory_tool': 'manual',
        'custom_gpts_path': 'A_manual',
        'estimated_total_time_min': 0,
    }

    conv = audit.get('conversations_regular', {})
    arch = audit.get('conversations_archived', {})
    proj = audit.get('projects', {})
    gpts = audit.get('custom_gpts', {})

    total_conv = (conv.get('total') or 0) + sum(p.get('num_interactions', 0) for p in proj.get('projects', []))
    total_archived = arch.get('total') or 0

    # Flag: include-archived
    if total_archived > 0:
        recs['brianjlacy_flags'].append('--include-archived')

    # Flag: throttle (scale based on volume)
    if total_conv > 500:
        recs['brianjlacy_flags'].append('--throttle 12')
    elif total_conv > 200:
        recs['brianjlacy_flags'].append('--throttle 8')
    else:
        recs['brianjlacy_flags'].append('--throttle 5')

    # Flag: no-user-dir (cleaner output)
    recs['brianjlacy_flags'].append('--no-user-dir')

    # Memory tool decision
    # (can't auto-count via API reliably, leave to user)
    recs['memory_tool'] = 'memport (recommended)'

    # Custom GPTs path decision
    gpts_count = gpts.get('count')
    if gpts_count is None:
        recs['custom_gpts_path'] = 'A_manual (endpoint probe failed, manual verification needed)'
    elif gpts_count == 0:
        recs['custom_gpts_path'] = 'SKIP (no Custom GPTs owned)'
    elif gpts_count <= 5:
        recs['custom_gpts_path'] = 'A_manual (5-10 min/GPT)'
    elif gpts_count <= 15:
        recs['custom_gpts_path'] = 'A_manual or B_playwright (choice based on time budget)'
    else:
        recs['custom_gpts_path'] = 'B_playwright (scrape-custom-gpts.js)'

    # Time estimate
    bulk_min = max(5, (total_conv + total_archived) * 5 / 60)  # ~5s per conv with throttle 5
    gpts_min = (gpts_count or 0) * (3 if 'B_' in recs['custom_gpts_path'] else 8)
    recs['estimated_total_time_min'] = round(bulk_min + 15 + gpts_min, 1)

    return recs


def write_yaml(audit, recs, output: Path):
    """Hand-write YAML (avoid PyYAML dep)."""
    lines = [
        f'# ChatGPT Workspace Audit -- {datetime.now().isoformat()}',
        f'# Auto-generated by auto-audit.py',
        '',
        'audit:',
    ]

    def emit(key, val, indent='  '):
        if isinstance(val, dict):
            lines.append(f'{indent}{key}:')
            for k, v in val.items():
                emit(k, v, indent + '  ')
        elif isinstance(val, list):
            lines.append(f'{indent}{key}:')
            for item in val:
                if isinstance(item, dict):
                    lines.append(f'{indent}  -')
                    for k, v in item.items():
                        emit(k, v, indent + '    ')
                else:
                    lines.append(f'{indent}  - {json.dumps(item, ensure_ascii=False)}')
        elif val is None:
            lines.append(f'{indent}{key}: null')
        elif isinstance(val, bool):
            lines.append(f'{indent}{key}: {str(val).lower()}')
        elif isinstance(val, (int, float)):
            lines.append(f'{indent}{key}: {val}')
        else:
            lines.append(f'{indent}{key}: {json.dumps(val, ensure_ascii=False)}')

    for k, v in audit.items():
        emit(k, v)

    lines.append('')
    lines.append('recommendations:')
    for k, v in recs.items():
        emit(k, v)

    output.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    log(f'Audit written to {output}')


def main():
    args = parse_args()
    global vlog
    if args.verbose:
        def vlog(msg, *a):
            log(f'[VERBOSE] {msg}', *a)

    bearer = args.bearer or os.environ.get('CHATGPT_BEARER_TOKEN')
    if not bearer:
        print('ERROR: provide --bearer or CHATGPT_BEARER_TOKEN env var', file=sys.stderr)
        sys.exit(1)

    if args.bearer:
        log('WARNING: passing --bearer via CLI exposes token via process arg list (CWE-214). Prefer CHATGPT_BEARER_TOKEN env var sourced from env-file with restricted ACL.')

    bearer = bearer.strip()
    if bearer.startswith('Bearer '):
        bearer = bearer[7:]

    # Auto-detect account ID from JWT if not provided
    account_id = args.account_id
    payload = decode_jwt_payload(bearer)
    if payload:
        if not account_id and payload.get('https://api.openai.com/auth'):
            auth_section = payload['https://api.openai.com/auth']
            account_id = auth_section.get('account_id') or auth_section.get('chatgpt_account_id')
        log(f'JWT decoded: sub={payload.get("sub")[:30] if payload.get("sub") else "?"}... exp={payload.get("exp")}')
        if payload.get('exp'):
            exp_dt = datetime.fromtimestamp(payload['exp'])
            now = datetime.now()
            remaining = (exp_dt - now).total_seconds() / 60
            log(f'Token expires in {remaining:.1f} minutes ({exp_dt})')
            if remaining < 5:
                log('WARNING: token expires very soon, may fail mid-audit')

    if account_id:
        log(f'Account ID: {account_id}')

    audit = {'timestamp': datetime.now().isoformat()}

    # Run probes (each with delay to be nice to API)
    audit['user_profile'] = probe_user_profile(bearer, account_id)
    time.sleep(args.delay)

    audit['teams_account'] = probe_teams_account(bearer)
    time.sleep(args.delay)

    audit['conversations_regular'] = probe_conversations_count(bearer, account_id, is_archived=False)
    time.sleep(args.delay)

    audit['conversations_archived'] = probe_conversations_count(bearer, account_id, is_archived=True)
    time.sleep(args.delay)

    audit['projects'] = probe_projects(bearer, account_id)
    time.sleep(args.delay)

    audit['custom_gpts'] = probe_custom_gpts_owned(bearer, account_id)
    time.sleep(args.delay)

    audit['memories_probe'] = probe_memories(bearer, account_id)

    # Derive recommendations
    recs = derive_recommendations(audit)

    write_yaml(audit, recs, args.output)

    # Print summary to stdout
    print('\n=== AUDIT SUMMARY ===')
    print(f'User: {audit["user_profile"].get("email", "?")}')
    workspaces = [a for a in audit.get("teams_account", []) if a.get("workspace_name")]
    if workspaces:
        print(f'Workspace(s): {", ".join(a["workspace_name"] for a in workspaces)}')
    print(f'Regular conversations: {audit["conversations_regular"].get("total", "?")}')
    print(f'Archived conversations: {audit["conversations_archived"].get("total", "?")}')
    print(f'Projects: {audit["projects"].get("count", "?")}')
    print(f'Custom GPTs: {audit["custom_gpts"].get("count", "?")}')
    print(f'\n--- Recommendations ---')
    print(f'brianjlacy flags: {" ".join(recs["brianjlacy_flags"])}')
    print(f'Custom GPTs path: {recs["custom_gpts_path"]}')
    print(f'Estimated total time: ~{recs["estimated_total_time_min"]} min')
    print(f'\nFull audit: {args.output}')


if __name__ == '__main__':
    main()
