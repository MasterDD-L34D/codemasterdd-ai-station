#!/usr/bin/env python3
"""Generate mock brianjlacy-shaped export data for pipeline smoke testing.

Produces 15 conversations across 3 buckets (regular, 2 projects) + 1 custom GPT.
Each conv has a realistic OpenAI 'mapping' tree shape with 4-8 messages.
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path(__file__).parent / 'mock-export'


def make_conv(title: str, project_name: str = None, messages_data: list = None, idx: int = 0):
    """Build a single conversation JSON in OpenAI mapping shape."""
    conv_id = str(uuid.uuid4())
    create_time = (datetime.now() - timedelta(days=idx * 3)).timestamp()
    update_time = create_time + 600

    # Build linear mapping tree
    mapping = {}
    parent_id = None
    root_id = str(uuid.uuid4())
    # Root node (no message)
    mapping[root_id] = {'id': root_id, 'message': None, 'parent': None, 'children': []}
    prev_id = root_id

    for i, (role, text) in enumerate(messages_data):
        node_id = str(uuid.uuid4())
        msg = {
            'id': node_id,
            'author': {'role': role, 'name': None, 'metadata': {}},
            'content': {'content_type': 'text', 'parts': [text]},
            'create_time': create_time + i * 60,
            'metadata': {}
        }
        mapping[node_id] = {'id': node_id, 'message': msg, 'parent': prev_id, 'children': []}
        mapping[prev_id]['children'].append(node_id)
        prev_id = node_id

    conv = {
        'id': conv_id,
        'title': title,
        'create_time': create_time,
        'update_time': update_time,
        'mapping': mapping,
        'moderation_results': [],
        'current_node': prev_id,
        'plugin_ids': None,
        'conversation_id': conv_id,
        'conversation_template_id': None,
        'gizmo_id': f'g-p-{"a" * 32}' if project_name else None,
        'is_archived': False,
        'safe_urls': [],
        'default_model_slug': 'gpt-4o',
    }
    return conv_id, conv


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Bucket 1: Regular non-project conversations (5 items)
    regular_data = [
        ('Python list comprehension help', [
            ('user', 'How do I use list comprehensions in Python with conditions?'),
            ('assistant', 'List comprehensions support filter conditions: `[x for x in items if x > 0]`. You can chain multiple conditions too.'),
            ('user', 'What about nested ones?'),
            ('assistant', 'Nested comprehensions: `[[y for y in row if y] for row in matrix]`. Outer first, then inner.'),
        ]),
        ('SQL JOIN performance tuning', [
            ('user', 'My JOIN query is slow on 10M row table. How to optimize?'),
            ('assistant', 'Check indexes on join columns. Use EXPLAIN ANALYZE. Consider denormalization or materialized views if read-heavy.'),
            ('user', 'Should I use INNER vs LEFT?'),
            ('assistant', 'INNER is generally faster when you only need matching rows. Use LEFT only when you need unmatched rows preserved.'),
        ]),
        ('Recipe for pasta carbonara', [
            ('user', 'Authentic carbonara recipe please'),
            ('assistant', 'Eggs, guanciale, pecorino, black pepper, pasta. NO cream. NO garlic. Render guanciale, mix eggs+cheese off heat, toss with hot pasta.'),
            ('user', 'How much pasta water?'),
            ('assistant', 'Add 1-2 tablespoons at time to emulsify. Stop when creamy. Too much = soup.'),
        ]),
        ('Git rebase vs merge debate', [
            ('user', 'When should I use rebase vs merge?'),
            ('assistant', 'Rebase: clean linear history, feature branches. Merge: shared branches, preserving context. Never rebase shared/published branches.'),
            ('user', 'Interactive rebase?'),
            ('assistant', 'For squashing/reordering commits before merging. `git rebase -i HEAD~5` opens editor. Mark commits with squash/fixup/edit/drop.'),
        ]),
        ('JavaScript async/await error handling', [
            ('user', 'Best pattern for try/catch with async?'),
            ('assistant', 'Wrap awaits in try/catch. For multiple awaits, consider Promise.allSettled to handle partial failures. Use error boundaries at top level.'),
            ('user', 'Promise.all vs Promise.allSettled?'),
            ('assistant', 'Promise.all rejects on first failure. Promise.allSettled always resolves with status array. Use allSettled when you want all results regardless of failures.'),
        ]),
    ]

    print('Writing regular conversations...')
    for idx, (title, msgs) in enumerate(regular_data):
        conv_id, conv = make_conv(title, project_name=None, messages_data=msgs, idx=idx)
        date_prefix = datetime.fromtimestamp(conv['create_time']).strftime('%Y-%m-%d')
        safe_title = title.replace(' ', '_').replace('/', '-').replace('\\', '-').replace(':', '-')[:40]
        path = OUT / 'json' / f'{date_prefix}_{safe_title}_{conv_id[:8]}.json'
        path.write_text(json.dumps(conv, indent=2), encoding='utf-8')

    # Bucket 2: Evo-Tactics project (4 items)
    evo_data = [
        ('Trait balance: Wild Hunter vs Tracker', [
            ('user', 'In Evo-Tactics, Wild Hunter trait gives +2 STR vs prey. Tracker gives +1 perception. Which is better for solo player early game?'),
            ('assistant', 'Wild Hunter scales better in combat (direct damage), Tracker is utility (scouting). Early game solo = Wild Hunter wins encounter outcomes. Tracker shines in 2+ player parties for info advantage.'),
            ('user', 'What about late game?'),
            ('assistant', 'Late game: Tracker compounds with build-up bonuses (ambush, surprise). Wild Hunter caps at +2. Tracker can stack to +5 in optimal builds. Late game Tracker > Wild Hunter for skilled players.'),
        ]),
        ('Biome design: Mire vs Marsh distinction', [
            ('user', 'I have Mire and Marsh biomes. Are they too similar?'),
            ('assistant', 'Mire = dense, stuck movement, ambush opportunities. Marsh = open water+mud, ranged combat favored, slow encounter pace. If only stat differences mirror each other, merge them. If different combat tempo, keep both.'),
            ('user', 'Should they have unique species?'),
            ('assistant', 'Yes: Mire-only species (e.g., Ambush Predator) reinforces ambush identity. Marsh-only (e.g., Wading Heron) reinforces ranged. Unique species = distinct player fantasies.'),
        ]),
        ('Combat math: d20 + stat vs DC scale', [
            ('user', 'My d20 + STR combat: average roll is 13, mid-game STR is 5. So 18 vs DC. DC tier 1 = 15, tier 2 = 20. Feels too forgiving early.'),
            ('assistant', 'Math right. To tighten: raise DC tier 1 to 17 (75% hit), or reduce starting STR to 3 (avg 16 vs 15 = 60% hit). Sweet spot for D&D-style is 60-70% hit early, 45-55% mid, 35-45% late.'),
            ('user', 'Critical fails?'),
            ('assistant', 'Critical fail on natural 1 = consider auto-miss + minor penalty (drop weapon, slip). Adds variance + memorable moments. Not just "miss" — narrative consequence.'),
        ]),
        ('Onboarding: first 5 min new player', [
            ('user', 'New player onboarding: what should they understand in first 5 minutes?'),
            ('assistant', '1. Core loop (explore -> encounter -> resolve -> evolve). 2. d20 + stat = check. 3. Death = restart but keep meta-progression. Drip-feed traits/species after they hit first encounter.'),
            ('user', 'Tutorial encounter design?'),
            ('assistant', 'Single low-stakes combat: 1 enemy, 1 stat check, 1 movement decision. Win = explanation popup ("you used STR"). Lose = "try different stat" hint. No instant deaths in tutorial.'),
        ]),
    ]

    print('Writing Evo-Tactics project conversations...')
    for idx, (title, msgs) in enumerate(evo_data):
        conv_id, conv = make_conv(title, project_name='Evo-Tactics-Test', messages_data=msgs, idx=idx)
        date_prefix = datetime.fromtimestamp(conv['create_time']).strftime('%Y-%m-%d')
        safe_title = title.replace(' ', '_').replace(':', '_')[:40]
        path = OUT / 'projects' / 'Evo-Tactics-Test' / 'json' / f'{date_prefix}_{safe_title}_{conv_id[:8]}.json'
        path.write_text(json.dumps(conv, indent=2), encoding='utf-8')

    # Bucket 3: UniUPO academic project (4 items)
    uni_data = [
        ('Synesthesia clinical literature review', [
            ('user', 'Recent peer-reviewed studies on grapheme-color synesthesia in adults?'),
            ('assistant', 'Look at Simner et al 2024 cohort study (n=200). Also Rouw & Scholte 2023 fMRI work on V4 hyperactivation. Both confirm consistent letter-color mappings across decades.'),
            ('user', 'Methodological critiques?'),
            ('assistant', 'Self-report bias in cohort selection. Most studies rely on Test of Genuineness (Eagleman). Sample skews toward female, art-adjacent professions. Bigger random samples needed.'),
        ]),
        ('UniUPO thesis structure proposal', [
            ('user', 'My UniUPO thesis is on synesthesia + cognition. Structure suggestions?'),
            ('assistant', 'Standard 5-chapter: 1. Intro+definitions, 2. Literature review, 3. Methods/your contribution, 4. Results, 5. Discussion+future work. Keep methods rigorous — review boards focus there.'),
            ('user', 'Original contribution? I cant do an experiment.'),
            ('assistant', 'Meta-analysis of existing studies is valid original work. Or theoretical synthesis bridging cognitive neuroscience + phenomenology. Both publishable, no IRB needed.'),
        ]),
        ('Exam preparation strategy psychology', [
            ('user', 'UniUPO exam in August on developmental psychology. How to prep efficiently?'),
            ('assistant', 'Spaced repetition (Anki cards) for definitions + key studies. Practice essays on canonical questions. Review past exam paper format. Schedule 60-min sessions, not marathons.'),
            ('user', 'How many hours total?'),
            ('assistant', 'Rule of thumb: 30-40 hours for a 6 CFU exam if material is already familiar. Add 50% if first exposure. So 40-60 hours over 4-6 weeks = sustainable.'),
        ]),
        ('Research ethics IRB application process', [
            ('user', 'I need IRB approval for online survey on synesthesia. Process?'),
            ('assistant', 'Italian universities: submit protocol to ethics committee with informed consent doc, data handling plan, debriefing materials. Usually 2-6 weeks. Online surveys are usually low-risk = expedited review.'),
            ('user', 'What about GDPR?'),
            ('assistant', 'GDPR-compliant consent form mandatory. Specify: what data collected, purpose, retention, withdrawal right, data controller. Pseudonymize from collection. Self-hosted survey tool > Google Forms for control.'),
        ]),
    ]

    print('Writing UniUPO project conversations...')
    for idx, (title, msgs) in enumerate(uni_data):
        conv_id, conv = make_conv(title, project_name='UniUPO-Test', messages_data=msgs, idx=idx)
        date_prefix = datetime.fromtimestamp(conv['create_time']).strftime('%Y-%m-%d')
        safe_title = title.replace(' ', '_').replace(':', '_')[:40]
        path = OUT / 'projects' / 'UniUPO-Test' / 'json' / f'{date_prefix}_{safe_title}_{conv_id[:8]}.json'
        path.write_text(json.dumps(conv, indent=2), encoding='utf-8')

    # Bucket 4: Custom GPT config (1 item)
    print('Writing Custom GPT config...')
    gpt_config = {
        'url': 'https://chatgpt.com/g/g-mockEvoTacticsHelper',
        'scraped_at': datetime.now().isoformat(),
        'name': 'Evo-Tactics Design Helper',
        'description': 'Assistant for Evo-Tactics tabletop d20 game design decisions',
        'instructions': 'You are an expert game designer specialized in tactical d20 games. When asked about balance, trait design, biome interactions, or core loops in Evo-Tactics, provide first-principles reasoning grounded in player fantasy and combat tempo. Always check for: 1) does this serve a player fantasy, 2) does it create meaningful decisions, 3) is the math balanced. Cite specific traits/species/biomes from the game when relevant.',
        'conversation_starters': [
            'Help me balance a new trait',
            'Review my biome design',
            'Suggest core loop improvements',
            'Critique my onboarding flow'
        ],
        'capabilities': {
            'Web Browsing': True,
            'DALL-E Image Generation': False,
            'Code Interpreter & Data Analysis': True
        },
        'knowledge_files': [
            'evo-tactics-design-doc.pdf',
            'trait-list-v2.json',
            'biome-reference.md'
        ],
        'actions_count': 0,
    }
    gpt_path = OUT / 'custom-gpts' / 'test-gpt-evo' / 'config.json'
    gpt_path.write_text(json.dumps(gpt_config, indent=2), encoding='utf-8')

    # Project index files
    print('Writing project-index.json...')
    project_index = [
        {
            'id': f'g-p-{"a" * 32}',
            'name': 'Evo-Tactics-Test',
            'description': 'Test project for Evo-Tactics design conversations',
            'instructions': 'Help with tactical game design',
            'workspace_id': 'mock-workspace-id',
            'created_at': '2026-01-01T00:00:00Z',
            'updated_at': '2026-05-14T00:00:00Z',
            'num_interactions': 4,
            'files': [],
            'conversation_count': 4
        },
        {
            'id': f'g-p-{"b" * 32}',
            'name': 'UniUPO-Test',
            'description': 'Test project for UniUPO academic',
            'instructions': 'Academic synesthesia research support',
            'workspace_id': 'mock-workspace-id',
            'created_at': '2026-01-15T00:00:00Z',
            'updated_at': '2026-05-13T00:00:00Z',
            'num_interactions': 4,
            'files': [],
            'conversation_count': 4
        }
    ]
    (OUT / 'projects' / 'project-index.json').write_text(json.dumps(project_index, indent=2), encoding='utf-8')

    # Count files generated
    total = sum(1 for _ in OUT.rglob('*.json'))
    print(f'\nMock data generated. Total JSON files: {total}')
    print(f'Output root: {OUT}')


if __name__ == '__main__':
    main()
