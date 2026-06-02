#!/usr/bin/env python3
"""
classify.py -- Classification pipeline per ChatGPT export brianjlacy structure.

Pipeline:
  1. Walk brianjlacy output (conversations + projects + custom-gpts)
  2. Extract messages from JSON 'mapping' tree (canonical OpenAI shape)
  3. Embed text chunks via nomic-embed-text (Ollama API)
  4. Cluster with BERTopic (UMAP + HDBSCAN)
  5. Label topics via Qwen 14B Q2 (Ollama API)
  6. Output: clusters JSON + topic-to-conv mapping + labels MD

Privacy: 100% sovereign (Ollama locale, no cloud).

Usage:
  python classify.py \
    --input <export_root> \
    --output <output_dir> \
    --embed-model nomic-embed-text \
    --label-model qwen2.5-coder:14b-instruct-q2_K
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterator

import frontmatter
import numpy as np
import ollama
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm
from umap import UMAP
from hdbscan import HDBSCAN

LABEL_PREFIX_RE = re.compile(r'^(label:|topic:|cluster:)\s*')

# Multilingual stopwords (Italian + English common terms that don't carry topic signal)
ITALIAN_STOPWORDS = [
    'di', 'un', 'una', 'uno', 'il', 'la', 'lo', 'le', 'gli', 'l',
    'per', 'che', 'chi', 'cui', 'che', 'cosa', 'come', 'dove', 'quando', 'perche',
    'e', 'ed', 'a', 'ai', 'al', 'allo', 'alla', 'alle', 'agli',
    'da', 'dai', 'dal', 'dalla', 'dalle', 'dagli', 'in', 'nel', 'nello', 'nella', 'nelle', 'negli',
    'su', 'sui', 'sul', 'sulla', 'sulle', 'sugli', 'con', 'coi', 'col',
    'non', 'si', 'no', 'gia', 'ancora', 'molto', 'poco', 'tanto', 'troppo', 'piu',
    'sono', 'sei', 'sia', 'siano', 'siamo', 'siete', 'fu', 'furono',
    'questo', 'questa', 'questi', 'queste', 'quello', 'quella', 'quelli', 'quelle',
    'esso', 'essa', 'essi', 'esse', 'lui', 'lei', 'loro', 'noi', 'voi',
    'mio', 'mia', 'miei', 'mie', 'tuo', 'tua', 'tuoi', 'tue', 'suo', 'sua', 'suoi', 'sue',
    'nostro', 'nostra', 'nostri', 'nostre', 'vostro', 'vostra', 'vostri', 'vostre',
    'essere', 'avere', 'fare', 'andare', 'dire', 'sapere', 'vedere', 'volere', 'dovere', 'potere',
    'pero', 'anche', 'quindi', 'percio', 'allora', 'mentre', 'pero', 'tutto', 'tutti', 'tutte',
    'ogni', 'qualche', 'altro', 'altra', 'altri', 'altre', 'stesso', 'stessa', 'stessi', 'stesse',
    'tale', 'tali', 'cose', 'cosa', 'parte', 'volta', 'modo', 'punto', 'caso',
    'ho', 'hai', 'ha', 'abbiamo', 'avete', 'hanno', 'ero', 'eri', 'era', 'eravamo', 'eravate', 'erano',
    'titolo', 'utente', 'assistente', 'gpt', 'chat', 'user', 'assistant',
    'penso', 'credo', 'forse', 'magari', 'certo', 'sicuro', 'davvero',
]

ENGLISH_STOPWORDS = [
    'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'else', 'so', 'because',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'am', 'do', 'does', 'did', 'doing',
    'have', 'has', 'had', 'having', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
    'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'from', 'about', 'as', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'over',
    'one', 'two', 'three', 'four', 'five', 'first', 'second', 'last',
    'all', 'any', 'each', 'every', 'no', 'not', 'only', 'own', 'other', 'some', 'such',
    'than', 'too', 'very', 'just', 'most', 'more', 'much', 'many', 'few',
    'title', 'user', 'assistant', 'chat', 'gpt', 'response', 'message',
    'use', 'using', 'used', 'make', 'made', 'get', 'got', 'see', 'know', 'want', 'need',
    'also', 'however', 'therefore', 'thus', 'while', 'where', 'when', 'how', 'what', 'why', 'who',
]

COMBINED_STOPWORDS = list(set(ITALIAN_STOPWORDS + ENGLISH_STOPWORDS))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--input', required=True, type=Path, help='brianjlacy export root')
    p.add_argument('--output', required=True, type=Path, help='Output dir for classified data')
    p.add_argument('--embed-model', default='nomic-embed-text', help='Ollama embed model')
    p.add_argument('--label-model', default='qwen2.5-coder:14b-instruct-q2_K', help='Ollama labeling model')
    p.add_argument('--min-topic-size', type=int, default=10, help='BERTopic min documents per cluster')
    p.add_argument('--nr-topics', default='none', help='BERTopic topic count: "auto" / "none" / integer (default: none = no reduction, lets clustering find natural topics)')
    p.add_argument('--max-conversations', type=int, default=0, help='Limit (0 = no limit, for testing)')
    p.add_argument('--include-projects', action='store_true', default=True)
    p.add_argument('--include-non-project', action='store_true', default=True)
    p.add_argument('--include-custom-gpts', action='store_true', default=True)
    p.add_argument('--language', default='multilingual', help='multilingual / italian / english')
    p.add_argument('--ollama-host', default='http://localhost:11434', help='Ollama API endpoint')
    p.add_argument('--verbose', action='store_true')
    return p.parse_args()


def log(msg: str, *args) -> None:
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}', *args, file=sys.stderr)


def extract_messages_from_mapping(conv_json: dict) -> list[dict]:
    """Traverse OpenAI conversation 'mapping' tree linear-first-child order.
    Same logic as brianjlacy formatter.js extractMessagesInOrder.

    On multi-root mappings (branched conversations), prefer the root that
    has the largest downstream tree (more messages reached via first-child walk).
    """
    mapping = conv_json.get('mapping') or {}
    if not mapping:
        return []

    # Find ALL nodes without parent (multi-root case = branched conversations)
    root_candidates = [nid for nid, node in mapping.items() if not node.get('parent')]
    if not root_candidates:
        return []

    def count_reachable(rid):
        cnt = 0
        cur = rid
        visited = set()
        while cur and cur not in visited:
            visited.add(cur)
            n = mapping.get(cur)
            if not n:
                break
            if n.get('message'):
                cnt += 1
            ch = n.get('children') or []
            cur = ch[0] if ch else None
        return cnt

    # Pick root with the longest first-child chain
    root_id = max(root_candidates, key=count_reachable)

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


def message_to_text(msg: dict) -> str:
    """Extract textual content from a single message node. Skip hidden/system context."""
    content = msg.get('content') or {}
    metadata = msg.get('metadata') or {}

    if metadata.get('is_visually_hidden_from_conversation'):
        return ''

    ct = content.get('content_type', '')

    if ct == 'text':
        return '\n'.join(p for p in content.get('parts', []) if isinstance(p, str))

    if ct == 'code':
        return content.get('text', '') or ''

    if ct == 'multimodal_text':
        parts = []
        for part in content.get('parts', []):
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and part.get('content_type') == 'image_asset_pointer':
                parts.append('[image]')
        return '\n'.join(parts)

    if ct in ('thoughts', 'reasoning_recap', 'tether_browsing_display'):
        return '\n'.join(p for p in content.get('parts', []) if isinstance(p, str))

    if ct == 'model_editable_context':
        return ''

    # Fallback string
    if isinstance(content, str):
        return content

    return ''


def conversation_to_doc(conv_json: dict, source_path: Path, project_name: str = None) -> dict:
    """Reduce one conversation to a single document for clustering.
    Strategy: concatenate first user msg + first assistant msg + last user msg (1024 char max).
    Rationale: enough signal for clustering, fast to embed.
    """
    messages = extract_messages_from_mapping(conv_json)
    if not messages:
        return None

    # Filter to user + assistant + tool
    relevant = [m for m in messages if (m.get('author') or {}).get('role') in ('user', 'assistant', 'tool')]
    if not relevant:
        return None

    # Heuristic doc text: first user prompt + first assistant response + title
    title = conv_json.get('title') or 'Untitled'
    first_user = next((message_to_text(m) for m in relevant if m.get('author', {}).get('role') == 'user'), '')
    first_assistant = next((message_to_text(m) for m in relevant if m.get('author', {}).get('role') == 'assistant'), '')

    # Truncate to keep embedding fast
    doc_text = f"TITLE: {title}\n\nUSER: {first_user[:600]}\n\nASSISTANT: {first_assistant[:1200]}"

    return {
        'id': conv_json.get('id') or conv_json.get('conversation_id') or source_path.stem,
        'title': title,
        'create_time': conv_json.get('create_time'),
        'update_time': conv_json.get('update_time'),
        'model': conv_json.get('default_model_slug') or conv_json.get('model'),
        'gizmo_id': conv_json.get('gizmo_id'),
        'project_name': project_name,
        'source_path': str(source_path),
        'message_count': len(relevant),
        'is_archived': conv_json.get('is_archived', False),
        'doc_text': doc_text,
    }


def walk_export(input_root: Path, args) -> Iterator[dict]:
    """Yield doc dicts from brianjlacy export structure.

    Structure expected:
      <root>/json/*.json                          (regular)
      <root>/projects/<Name>/json/*.json          (project-scoped)
      <root>/custom-gpts/<slug>/config.json       (custom GPTs, our scrape)
    """
    # Regular conversations
    if args.include_non_project:
        regular_dir = input_root / 'json'
        if regular_dir.is_dir():
            for f in sorted(regular_dir.glob('*.json')):
                try:
                    data = json.loads(f.read_text(encoding='utf-8'))
                    doc = conversation_to_doc(data, f, project_name=None)
                    if doc:
                        yield doc
                except (json.JSONDecodeError, OSError) as e:
                    log(f'Skipping {f}: {e}')

    # Project conversations
    if args.include_projects:
        projects_dir = input_root / 'projects'
        if projects_dir.is_dir():
            for proj_dir in sorted(projects_dir.iterdir()):
                if not proj_dir.is_dir():
                    continue
                proj_json_dir = proj_dir / 'json'
                if not proj_json_dir.is_dir():
                    continue
                for f in sorted(proj_json_dir.glob('*.json')):
                    try:
                        data = json.loads(f.read_text(encoding='utf-8'))
                        doc = conversation_to_doc(data, f, project_name=proj_dir.name)
                        if doc:
                            yield doc
                    except (json.JSONDecodeError, OSError) as e:
                        log(f'Skipping {f}: {e}')

    # Custom GPTs configs (treated as pseudo-conversations for topical overview)
    if args.include_custom_gpts:
        gpts_dir = input_root / 'custom-gpts'
        if gpts_dir.is_dir():
            for gpt_dir in sorted(gpts_dir.iterdir()):
                if not gpt_dir.is_dir():
                    continue
                config_json = gpt_dir / 'config.json'
                if not config_json.is_file():
                    continue
                try:
                    data = json.loads(config_json.read_text(encoding='utf-8'))
                    doc = {
                        'id': f'gpt-{gpt_dir.name}',
                        'title': data.get('name') or gpt_dir.name,
                        'create_time': None,
                        'update_time': data.get('scraped_at'),
                        'model': 'custom-gpt',
                        'gizmo_id': data.get('url', '').split('/')[-1],
                        'project_name': '_custom-gpts',
                        'source_path': str(config_json),
                        'message_count': 0,
                        'is_archived': False,
                        'doc_text': (
                            f"TITLE: {data.get('name', '')}\n\n"
                            f"DESCRIPTION: {data.get('description', '')[:300]}\n\n"
                            f"INSTRUCTIONS: {(data.get('instructions') or '')[:1200]}"
                        ),
                    }
                    yield doc
                except (json.JSONDecodeError, OSError) as e:
                    log(f'Skipping {config_json}: {e}')


def embed_docs(docs: list[dict], embed_model: str, ollama_host: str) -> tuple[np.ndarray, list[int]]:
    """Use Ollama nomic-embed-text per chunk. Embedding dim typical 768.

    Returns: (embeddings array, list of doc indices that FAILED embed)
    Failed indices should be treated as outliers downstream (excluded from clustering
    fit, then assigned -1 topic).
    """
    client = ollama.Client(host=ollama_host, timeout=120)
    embeddings = []
    failed_indices = []
    expected_dim = None
    log(f'Embedding {len(docs)} docs via Ollama model {embed_model} (timeout 120s/req) ...')
    for i, d in enumerate(tqdm(docs, desc='embed')):
        try:
            resp = client.embeddings(model=embed_model, prompt=d['doc_text'])
            emb = resp['embedding']
            if expected_dim is None:
                expected_dim = len(emb)
            elif len(emb) != expected_dim:
                log(f'Embed dim mismatch doc {d["id"]}: got {len(emb)}, expected {expected_dim}. Marking failed.')
                failed_indices.append(i)
                emb = [0.0] * expected_dim
            embeddings.append(emb)
        except Exception as e:
            log(f'Embed error for doc {d["id"]}: {e}. Marking failed (outlier downstream).')
            failed_indices.append(i)
            # Placeholder; will be excluded from clustering
            embeddings.append([0.0] * (expected_dim or 768))

    if failed_indices:
        log(f'Total embed failures: {len(failed_indices)}/{len(docs)} ({100*len(failed_indices)/len(docs):.1f}%)')

    return np.array(embeddings, dtype=np.float32), failed_indices


def cluster_topics(embeddings: np.ndarray, docs: list[dict], min_topic_size: int, nr_topics_arg: str):
    """BERTopic with pre-computed embeddings. Fast + reproducible."""
    # Parse nr_topics
    nr_topics = None
    if nr_topics_arg == 'auto':
        nr_topics = 'auto'
    elif nr_topics_arg == 'none' or nr_topics_arg is None:
        nr_topics = None
    else:
        try:
            nr_topics = int(nr_topics_arg)
        except ValueError:
            log(f'Invalid --nr-topics value "{nr_topics_arg}", defaulting to None')
            nr_topics = None

    log(f'Clustering {len(docs)} docs with BERTopic (min_topic_size={min_topic_size}, nr_topics={nr_topics})...')

    # Custom vectorizer filters italian + english stopwords for cleaner topic keywords.
    # NOTE: BERTopic aggregates docs per topic before passing to vectorizer, so min_df/max_df
    # would refer to topic count (small number), not original docs. Leave at defaults.
    vectorizer = CountVectorizer(stop_words=COMBINED_STOPWORDS, ngram_range=(1, 2))

    # Custom UMAP: n_neighbors=5 preserves local structure (smaller = more granular clusters)
    # n_components=10 (vs default 5) gives HDBSCAN more dimensions to discriminate
    umap_model = UMAP(n_neighbors=5, n_components=10, min_dist=0.0, metric='cosine', random_state=42)

    # Custom HDBSCAN: min_samples=1 allows looser cluster formation
    hdbscan_model = HDBSCAN(min_cluster_size=min_topic_size, min_samples=1, metric='euclidean',
                             cluster_selection_method='eom', prediction_data=True)

    topic_model = BERTopic(
        embedding_model=None,
        vectorizer_model=vectorizer,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        min_topic_size=min_topic_size,
        nr_topics=nr_topics,
        verbose=True,
        calculate_probabilities=False,
        language='multilingual',
    )

    texts = [d['doc_text'] for d in docs]
    topics, _ = topic_model.fit_transform(texts, embeddings=embeddings)

    return topic_model, topics


def label_topics_with_llm(topic_model, docs, topics, label_model: str, ollama_host: str) -> dict[int, str]:
    """Use Qwen 14B Q2 (or other Ollama model) to generate human-readable labels per topic.
    Uses both keyword hints AND sample document titles for better grounding.
    """
    client = ollama.Client(host=ollama_host)
    topic_info = topic_model.get_topic_info()
    labels = {}

    # Build topic_id -> sample titles map
    topic_to_titles = {}
    for d, t in zip(docs, topics):
        topic_to_titles.setdefault(int(t), []).append(d.get('title', ''))

    log(f'Labeling {len(topic_info)} topics via Ollama model {label_model} ...')
    for _, row in tqdm(topic_info.iterrows(), total=len(topic_info), desc='label'):
        topic_id = int(row['Topic'])
        if topic_id == -1:
            labels[topic_id] = 'outliers'
            continue

        keywords = topic_model.get_topic(topic_id)
        if not keywords:
            labels[topic_id] = f'topic-{topic_id}'
            continue

        keyword_str = ', '.join(k for k, _ in keywords[:8] if k)
        sample_titles = topic_to_titles.get(topic_id, [])[:8]
        titles_str = '\n'.join(f'- {t[:80]}' for t in sample_titles if t)

        prompt = (
            'You are a topic labeling expert. Given a CLUSTER of conversations with '
            'these keywords and sample titles (italian + english mixed), generate ONE short '
            'CONTENT-FOCUSED label (max 5 words, lowercase, hyphen-separated).\n\n'
            'RULES:\n'
            '1. AVOID generic labels like "chat-assistant", "user-interaction", "general-questions", "discussion" -- these are tautological for chat conversation clusters.\n'
            '2. The label must REFLECT THE KEYWORDS AND TITLES, not external knowledge. Do NOT invent domain names not present in the cluster.\n'
            '3. Use the DOMINANT topic-bearing terms from keywords + titles. Compose a hyphenated label from these terms only.\n'
            '4. If cluster has no clear topic (mixed/heterogeneous), output "mixed-misc".\n\n'
            f'Keywords: {keyword_str}\n\n'
            f'Sample titles:\n{titles_str}\n\n'
            f'Label (compose only from terms present above; max 5 words, lowercase, hyphenated):'
        )

        try:
            resp = client.generate(model=label_model, prompt=prompt, options={'temperature': 0.2, 'num_predict': 30})
            raw_label = resp.get('response', '').strip().lower()
            raw_label = raw_label.split('\n')[0].strip().strip('"').strip("'").strip()
            # Strip leading punctuation + "label:" prefix sometimes added by model
            raw_label = LABEL_PREFIX_RE.sub('', raw_label)
            raw_label = re.sub(r'[^a-z0-9-]+', '-', raw_label).strip('-')
            label = raw_label[:60] or f'topic-{topic_id}'
            labels[topic_id] = label
        except Exception as e:
            log(f'Label error for topic {topic_id}: {e}')
            labels[topic_id] = f'topic-{topic_id}'

    return labels


def write_outputs(output_dir: Path, docs: list[dict], topics: list[int], labels: dict[int, str], topic_model):
    output_dir.mkdir(parents=True, exist_ok=True)

    # docs.json -- per-conv assignment
    docs_with_topics = []
    for d, t in zip(docs, topics):
        docs_with_topics.append({**d, 'topic_id': int(t), 'topic_label': labels.get(int(t), 'unknown')})
    (output_dir / 'conversations-classified.json').write_text(
        json.dumps(docs_with_topics, indent=2, default=str), encoding='utf-8'
    )

    # topics-summary.md
    topic_to_docs = defaultdict(list)
    for d, t in zip(docs, topics):
        topic_to_docs[int(t)].append(d)

    md_lines = [
        '# ChatGPT Classification -- Topics Summary',
        f'\nGenerated: {datetime.now().isoformat()}',
        f'\nTotal conversations: {len(docs)}',
        f'Total topics: {len(set(topics))} (incl. outliers -1)\n',
        '## Topics overview\n',
        '| Topic ID | Label | Documents | Top keywords |',
        '|---|---|---|---|',
    ]

    for topic_id in sorted(topic_to_docs.keys(), key=lambda x: (x == -1, x)):
        label = labels.get(topic_id, f'topic-{topic_id}')
        n_docs = len(topic_to_docs[topic_id])
        keywords = topic_model.get_topic(topic_id) if topic_id != -1 else []
        kw_str = ', '.join(k for k, _ in keywords[:5]) if keywords else 'outliers'
        md_lines.append(f'| {topic_id} | `{label}` | {n_docs} | {kw_str} |')

    md_lines.append('\n## Per-topic conversations\n')
    for topic_id in sorted(topic_to_docs.keys(), key=lambda x: (x == -1, x)):
        label = labels.get(topic_id, f'topic-{topic_id}')
        md_lines.append(f'\n### Topic {topic_id}: `{label}` ({len(topic_to_docs[topic_id])} convs)\n')
        for d in topic_to_docs[topic_id][:50]:
            project = f" [{d['project_name']}]" if d['project_name'] else ''
            md_lines.append(f"- {d['title']}{project} -- `{d['id'][:8]}`")
        if len(topic_to_docs[topic_id]) > 50:
            md_lines.append(f'- ... ({len(topic_to_docs[topic_id]) - 50} more)')

    (output_dir / 'topics-summary.md').write_text('\n'.join(md_lines), encoding='utf-8')

    # bertopic model save (for re-use later)
    try:
        topic_model.save(str(output_dir / 'bertopic-model'), serialization='safetensors')
    except Exception as e:
        log(f'BERTopic save warning: {e}')

    log(f'Outputs written to {output_dir}')
    log(f'  - conversations-classified.json ({len(docs_with_topics)} docs)')
    log(f'  - topics-summary.md ({len(set(topics))} topics)')
    log(f'  - bertopic-model/ (re-loadable)')


def main():
    args = parse_args()

    log(f'Input: {args.input}')
    log(f'Output: {args.output}')
    log(f'Embed model: {args.embed_model}')
    log(f'Label model: {args.label_model}')

    # Step 1: walk + collect docs
    docs = list(walk_export(args.input, args))
    if args.max_conversations > 0:
        docs = docs[:args.max_conversations]
    log(f'Collected {len(docs)} docs')

    if len(docs) < args.min_topic_size:
        log(f'ERROR: fewer than {args.min_topic_size} docs collected ({len(docs)}). BERTopic min_topic_size requires this minimum. Verify input path structure or pass --min-topic-size lower.')
        sys.exit(1)

    # Step 2: embed
    embeddings, failed_indices = embed_docs(docs, args.embed_model, args.ollama_host)
    log(f'Embeddings shape: {embeddings.shape}')

    # Step 3: cluster (excluding failed embed docs which will be marked -1 outliers)
    valid_mask = np.ones(len(docs), dtype=bool)
    for fi in failed_indices:
        valid_mask[fi] = False
    if failed_indices:
        log(f'Excluding {len(failed_indices)} failed-embed docs from clustering (will be outliers)')

    valid_embeddings = embeddings[valid_mask]
    valid_docs = [d for i, d in enumerate(docs) if valid_mask[i]]
    topic_model, valid_topics = cluster_topics(valid_embeddings, valid_docs, args.min_topic_size, args.nr_topics)

    # Re-merge: failed-embed docs get topic_id = -1
    topics = []
    valid_iter = iter(valid_topics)
    for i in range(len(docs)):
        if valid_mask[i]:
            topics.append(int(next(valid_iter)))
        else:
            topics.append(-1)
    log(f'Topics found: {len(set(topics))} (incl. outliers)')

    # Step 4: label
    labels = label_topics_with_llm(topic_model, docs, topics, args.label_model, args.ollama_host)

    # Step 5: write
    write_outputs(args.output, docs, topics, labels, topic_model)

    log('Done.')


if __name__ == '__main__':
    main()
