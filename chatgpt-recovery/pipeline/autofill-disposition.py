#!/usr/bin/env python3
"""
Script for rule-based disposition and target_space autofill for review-card YAML blocks.

autofill-disposition.py -- Auto-fill review-sample.md disposition YAML blocks
based on topic-label keyword -> vault Space mapping rules.

Conservative policy:
  - Clear domain topics -> PROMOTE with mapped target_space
  - Personal/sensitive (songs, comedy, proposal, account-meta) -> HOLD
  - mixed-misc / outliers / ambiguous -> HOLD (Eduardo manual later)

Output: rewrites review-sample.md in place with filled disposition blocks.
A backup .bak is created first.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path


# Ordered keyword -> (disposition, target_space). First match wins.
# Keywords matched against topic_label (lowercase).
RULES = [
    # Evo-Tactics game design
    (['evo', 'gioco-design', 'ecosistem', 'protocolli-ui', 'design-evolution'], 'PROMOTE', 'Dev/Evo-Tactics'),
    # GPT creation / prompt engineering
    (['gpts', 'gpt-model', 'instructions-document', 'custom-problem', 'text-block-repeat',
      'prompt-ottimizzazione', 'fantasy-detailed-prompt', 'cercare-gpts', 'request-denied',
      'pathfinder-narrative-instructions', 'map-generator-instructions'], 'PROMOTE', 'GPT-Prompts/MasterDD'),
    # Hao Jin campaign
    (['hao-jin', 'torneo-guida', 'dungeon-torneo'], 'PROMOTE', 'GDR/HaoJin'),
    # Mezieres UniUPO
    (['mezieres', 'uniupo', 'esame'], 'PROMOTE', 'UniUPO/Mezieres-PRO-2025'),
    # Valdombra
    (['valdombra'], 'PROMOTE', 'GDR/Valdombra'),
    # Torneo Cremesi
    (['cremesi'], 'PROMOTE', 'GDR/TorneoCremesi'),
    # Characters / NPC forge
    (['npc', 'character-craft', 'syron-hukc', 'varn-zanna', 'actor-profile',
      'avatar-decoration', 'nome-del-personaggio', 'creazione-personaggio-nome',
      'scheda-personaggio'], 'PROMOTE', 'GDR/CharacterForge'),
    # Worldbuilding / storyline
    (['beatrice', 'red-alfa', 'kalekot', 'cercatori-altare', 'mondo-fantasy',
      'syron'], 'PROMOTE', 'GDR/MondoFantasy'),
    # Pathfinder generic (broad -- keep after specific campaigns)
    (['pathfinder', 'druidi', 'lich-filatterio', 'magus', 'armi-potenziamento',
      'item-craft', 'loot', 'antipaladino', 'dispel-magic', 'ap-companion',
      'bardo', 'attacchi-combattere', 'build-combattimento', 'build-personaggio',
      'personaggio-creazione', 'creazione-personaggio', 'character-creation',
      'campagna-del-party', 'citt--altofumo', 'story-game', 'energia-termica',
      'mantello-magico', 'ironsworn', 'mappa-vtt', 'pathfinder-img'], 'PROMOTE', 'GDR/Pathfinder'),
    # Tech / dev meta
    (['api', 'router-diagnostic', 'file-zip', 'link-extraction', 'google-docs',
      'searching-details', 'game-time-tracker'], 'PROMOTE', 'Dev/_tech-meta'),
    # Personal / sensitive -> HOLD
    (['canzone', 'comedy', 'stand-up', 'fiori-anello', 'chatgpt-plus'], 'HOLD', '_personal'),
]

# Default for unmatched / mixed-misc / outliers
DEFAULT = ('HOLD', '')

LABEL_REGEX = re.compile(r'topic_label:\s*(.+)')
DISPOSITION_REGEX = re.compile(r'disposition:\s*\S+.*')
TARGET_SPACE_REGEX = re.compile(r'target_space:.*')


def classify_topic(label):
    ll = label.lower()
    if 'mixed-misc' in ll or 'outlier' in ll:
        return DEFAULT
    for keywords, disp, space in RULES:
        if any(k in ll for k in keywords):
            return disp, space
    return DEFAULT


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--review', required=True, type=Path)
    p.add_argument('--dry-run', action='store_true')
    return p.parse_args()


def main():
    args = parse_args()
    content = args.review.read_text(encoding='utf-8')

    if not args.dry_run:
        shutil.copy(args.review, str(args.review) + '.bak')

    # Each topic block has a ```yaml ... ``` section with topic_label + disposition
    yaml_pattern = re.compile(r'(```yaml\s*\n)(.*?)(\n```)', re.DOTALL)

    stats = {'PROMOTE': 0, 'HOLD': 0}
    space_count = {}

    def replace_block(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        # Extract topic_label
        label_match = LABEL_REGEX.search(body)
        if not label_match:
            return m.group(0)
        label = label_match.group(1).strip()
        disp, space = classify_topic(label)
        stats[disp] = stats.get(disp, 0) + 1
        if space:
            space_count[space] = space_count.get(space, 0) + 1

        # Rewrite disposition + target_space lines
        new_body = body
        new_body = DISPOSITION_REGEX.sub(f'disposition: {disp}', new_body)
        new_body = TARGET_SPACE_REGEX.sub(f'target_space: {space}', new_body)
        return head + new_body + tail

    new_content = yaml_pattern.sub(replace_block, content)

    if args.dry_run:
        print('DRY RUN -- disposition summary:', file=sys.stderr)
    else:
        args.review.write_text(new_content, encoding='utf-8')
        print(f'Updated {args.review} (backup: {args.review}.bak)', file=sys.stderr)

    print(f'PROMOTE: {stats.get("PROMOTE",0)} | HOLD: {stats.get("HOLD",0)}', file=sys.stderr)
    print('Target spaces:', file=sys.stderr)
    for sp, n in sorted(space_count.items(), key=lambda x: -x[1]):
        print(f'  {sp}: {n} topics', file=sys.stderr)


if __name__ == '__main__':
    main()
