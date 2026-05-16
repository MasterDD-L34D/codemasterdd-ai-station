#!/usr/bin/env python3
"""
extract-entities.py -- Build entity index from classified ChatGPT conversations.

Identifies proper nouns / named entities (characters, locations, concepts) appearing
across conversations. Useful as vault taxonomy seed for autotag + cross-link.

Method: heuristic capitalized-word frequency analysis on titles + sample messages.
NOT LLM-based (avoid latency). Output is candidate list — Eduardo curates.

Output: entities-index.md with frequency table + per-entity conv list.
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


# Skip generic capitalized words (sentence starters, common verbs/nouns uppercased)
# Extended after 2026-05-15 false-positive analysis ("Put", "Ecco", "Include", etc.)
SKIP_WORDS = {
    # Italian articles/prepositions
    'L', 'La', 'Le', 'Il', 'Lo', 'Gli', 'Un', 'Una', 'Uno', 'Del', 'Della', 'Dei', 'Delle',
    'Per', 'Con', 'Da', 'In', 'Su', 'Tra', 'Fra', 'A', 'Al', 'Allo', 'Alla', 'Alle', 'Ai', 'Agli',
    'Sul', 'Sulla', 'Sullo', 'Sui', 'Sugli', 'Sulle', 'Coi', 'Cogli', 'Colle',
    'E', 'Ed', 'O', 'Od', 'Ma', 'Se', 'Mentre', 'Quando', 'Dove', 'Perché', 'Poiché',
    # Italian common verbs (often sentence-start capitalized)
    'Sono', 'Sei', 'Siamo', 'Siete', 'Sia', 'Sarà', 'Era', 'Eri', 'Eravate', 'Erano',
    'Ho', 'Hai', 'Ha', 'Abbiamo', 'Avete', 'Hanno', 'Avere', 'Essere',
    'Posso', 'Puoi', 'Può', 'Possiamo', 'Potete', 'Possono', 'Potrebbe', 'Potrebbero',
    'Voglio', 'Vuoi', 'Vuole', 'Vogliamo', 'Volete', 'Vogliono', 'Vorrei', 'Vorrebbe',
    'Devo', 'Devi', 'Deve', 'Dobbiamo', 'Dovete', 'Devono', 'Dovrebbe',
    'Faccio', 'Fai', 'Fa', 'Facciamo', 'Fate', 'Fanno', 'Fare',
    'Vado', 'Vai', 'Va', 'Andiamo', 'Andate', 'Vanno', 'Andare',
    'Sai', 'Sappiamo', 'Sapete', 'Sanno', 'Sapere',
    'Penso', 'Pensa', 'Pensi', 'Credo', 'Credi', 'Crede',
    'Dice', 'Disse', 'Dicono', 'Dico', 'Dici',
    'Crea', 'Creare', 'Creo', 'Crei', 'Creiamo', 'Crearlo', 'Creazione',
    'Iniziamo', 'Inizia', 'Inizio',
    # Italian common adjectives/exclamations
    'Ecco', 'Certo', 'Certamente', 'Perfetto', 'Bene', 'Bravo', 'Buona', 'Buon',
    'Ciao', 'Salve', 'Grazie', 'Prego', 'Scusa', 'Scusi',
    'Tuttavia', 'Quindi', 'Pertanto', 'Inoltre', 'Quanto', 'Tanto', 'Molto', 'Poco',
    'Questo', 'Questa', 'Questi', 'Queste', 'Quello', 'Quella', 'Quelli', 'Quelle',
    'Ogni', 'Tutti', 'Tutto', 'Tutta', 'Tutte', 'Alcuni', 'Altre', 'Altro', 'Altra',
    # Italian common nouns appearing in title contexts
    'Nome', 'Tipo', 'Stato', 'Livello', 'Punto', 'Punti', 'Parte', 'Parti', 'Caso', 'Casi',
    'Cosa', 'Cose', 'Modo', 'Modi', 'Volta', 'Volte', 'Anno', 'Mese', 'Giorno', 'Ora',
    'Razza', 'Classe', 'Classi', 'Personaggio', 'Personaggi', 'Descrizione', 'Descrizioni',
    'Spunti', 'Idea', 'Idee', 'Esempio', 'Esempi',
    'File', 'Files', 'Documento', 'Documenti', 'Allineamento', 'Peso',
    'Guida', 'Guide', 'Note', 'Notes',
    'Creazione', 'Creare', 'Aggiungere', 'Aggiungi',
    'Storia', 'Storie',  # too generic; could be entity but ambiguous
    # English common (sentence starters from assistant outputs)
    'The', 'This', 'That', 'These', 'Those', 'It', 'Is', 'Are', 'Was', 'Were', 'Be', 'Been', 'Being',
    'For', 'With', 'From', 'To', 'Of', 'On', 'At', 'By', 'As', 'About', 'After', 'Before',
    'And', 'Or', 'But', 'If', 'Then', 'When', 'Where', 'How', 'Why', 'What', 'Who',
    'I', 'You', 'He', 'She', 'We', 'They', 'Me', 'Him', 'Her', 'Us', 'Them',
    'Please', 'Note', 'Include', 'Includes', 'Put', 'Get', 'Got', 'Use', 'Used', 'Make', 'Made',
    'See', 'Look', 'Looking', 'Find', 'Found', 'Show', 'Showing',
    'Set', 'Sets', 'Setting', 'Reset', 'Repeat', 'Reapeat',  # common typos too
    'Take', 'Takes', 'Took', 'Give', 'Gives', 'Gave', 'Add', 'Adding', 'Added',
    'New', 'Old', 'First', 'Second', 'Third', 'Last', 'Next', 'Previous',
    'Title', 'Type', 'Card', 'Test', 'Demo', 'Example', 'Step', 'Steps',
    'Yes', 'No', 'Ok', 'Sure', 'Maybe', 'Perhaps',
    # Italian/English numeral words
    'Io', 'Tu', 'Lui', 'Lei', 'Noi', 'Voi', 'Loro',
    'Sì', 'Si',
    # ChatGPT-specific noise
    'Eduardo', 'User', 'Assistant', 'ChatGPT', 'GPT', 'Gpts', 'GPTs', 'Master',
    'Pathfinder',  # dominates frequency, skip (real domain noise)
    'Razza', 'Classe', 'Abilità',  # generic GDR terms
}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--classification', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--min-freq', type=int, default=3, help='Minimum frequency to include in index')
    p.add_argument('--top-n', type=int, default=200, help='Top N entities to write')
    return p.parse_args()


def extract_entities_from_text(text):
    """Find capitalized tokens, potentially multi-word (e.g., "Vhar'nak", "Hao Jin").
    Returns: list of entity strings.
    """
    if not text:
        return []
    # Multi-word capitalized phrases (e.g., "Hao Jin", "Master DD")
    # Match: word starting with uppercase, possibly followed by another uppercase word
    pattern = re.compile(r"\b([A-ZÀÈÌÒÙÁÉÍÓÚ][a-zàèìòùáéíóúñç']+(?:[ -][A-ZÀÈÌÒÙÁÉÍÓÚ][a-zàèìòùáéíóúñç']+)*)\b")
    candidates = pattern.findall(text)
    return [c for c in candidates if c not in SKIP_WORDS and len(c) >= 3]


def main():
    args = parse_args()
    classified_path = args.classification / 'conversations-classified.json'
    docs = json.loads(classified_path.read_text(encoding='utf-8'))

    # Tally entities across titles + doc_text (compressed summary)
    counter = Counter()
    entity_to_convs = defaultdict(list)

    for d in docs:
        title = d.get('title', '')
        doc_text = d.get('doc_text', '')
        combined = f'{title}\n{doc_text[:500]}'  # cap to avoid skew

        entities = extract_entities_from_text(combined)
        seen_in_doc = set()
        for e in entities:
            if e in seen_in_doc:
                continue  # count once per conv
            seen_in_doc.add(e)
            counter[e] += 1
            entity_to_convs[e].append({
                'id': (d.get('id') or '')[:8],
                'title': title,
                'topic': d.get('topic_label', ''),
            })

    # Filter by min_freq + sort
    top = [(e, n) for e, n in counter.most_common(args.top_n * 2) if n >= args.min_freq][:args.top_n]

    today = datetime.now().strftime('%Y-%m-%d')
    lines = [
        '---',
        f'id: chatgpt-recovery-entities-{today}',
        f'type: index',
        f'status: live',
        f'created: {today}',
        f'collection: chatgpt-recovery-2026-05-14',
        f'tags: [index, entities, chatgpt-import]',
        '---',
        '',
        f'# ChatGPT Recovery — Entity Index ({today})',
        '',
        f'Heuristic proper-noun frequency analysis on {len(docs)} classified conversations.',
        f'Top {len(top)} entities (frequency >= {args.min_freq}).',
        '',
        '_Method: regex capitalized-word + multi-word phrase pattern, skip-word filtered. NOT LLM-based._',
        '',
        '## Top entities',
        '',
        '| # | Entity | Freq | Top topics |',
        '|---|---|---|---|',
    ]

    for i, (entity, freq) in enumerate(top, 1):
        convs = entity_to_convs[entity]
        topics = Counter(c['topic'] for c in convs).most_common(3)
        topics_str = ', '.join(f'`{t}` ({n})' for t, n in topics)
        lines.append(f'| {i} | **{entity}** | {freq} | {topics_str} |')

    lines.extend([
        '',
        '## Per-entity conversations',
        '',
        '_(Sample: top 50 entities only, max 8 conv each)_',
        '',
    ])

    for entity, freq in top[:50]:
        lines.append(f'### {entity} ({freq})')
        lines.append('')
        for c in entity_to_convs[entity][:8]:
            lines.append(f'- `{c["id"]}` {c["title"][:80]} _(topic: `{c["topic"]}`)_')
        if len(entity_to_convs[entity]) > 8:
            lines.append(f'- ... ({len(entity_to_convs[entity]) - 8} more)')
        lines.append('')

    lines.extend([
        '## Usage hints',
        '',
        '- High-freq entities (>= 10) likely warrant dedicated vault tags (`tag-<slug>`)',
        '- Character/NPC entities → vault Spaces/GDR/CharacterForge/ candidates',
        '- Location entities → worldbuilding tags',
        '- Eduardo curates: remove false positives (auto-detected sometimes catches phrases)',
        '',
    ])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Entity index: {args.output}')
    print(f'Top entities (freq >= {args.min_freq}): {len(top)}')


if __name__ == '__main__':
    main()
