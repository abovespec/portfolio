#!/usr/bin/env python3
"""
INF-163: Add internal linking between blog articles on each site.

For each site with 3+ articles:
- Identifies topically related articles via TF-IDF cosine similarity
- Injects 2-3 contextual inline links per article into body paragraphs
- Prefers non-circular pairs; allows circular as fallback if needed
- Appends a "See also" section as last resort for structured/short articles
"""

import re
import os
import sys
import math
from pathlib import Path
from collections import Counter

SITES_DIR = Path("/home/abovespec/site-network/sites")
MIN_ARTICLES_FOR_SITE = 3
TARGET_LINKS_PER_ARTICLE = 3
MIN_LINKS_PER_ARTICLE = 2
# Minimum character gap between two injected link positions
MIN_LINK_GAP = 250

STOP_WORDS = {
    "a","an","the","and","or","but","if","in","on","at","to","for","of","with",
    "is","are","was","were","be","been","being","have","has","had","do","does",
    "did","will","would","could","should","may","might","shall","can","not","no",
    "it","its","this","that","these","those","i","you","he","she","we","they",
    "what","which","who","when","where","how","why","your","our","their","my",
    "from","as","by","about","into","through","during","including","before",
    "after","above","below","between","each","than","so","any","all","both",
    "few","more","most","other","some","such","up","out","use","used","using",
    "also","well","then","there","here","just","even","only","very",
    "while","make","made","get","got","take","taken","give","given",
}


def tokenize(text: str) -> list[str]:
    words = re.findall(r'[a-z]+', text.lower())
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]


def parse_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith('---'):
        return {}, content
    end = content.find('\n---', 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end]
    body = content[end + 4:].lstrip('\n')
    fm = {}
    for line in fm_text.splitlines():
        if ':' in line:
            key, _, val = line.partition(':')
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, body


def extract_tags(content: str) -> list[str]:
    match = re.search(r'^tags:\s*\[([^\]]*)\]', content, re.MULTILINE)
    if not match:
        return []
    raw = match.group(1)
    return [t.strip().strip('"').strip("'").lower() for t in raw.split(',')]


def count_existing_blog_links(body: str) -> int:
    return len(re.findall(r'\(/blog/[^)]+\)', body))


def compute_tfidf_vectors(articles: list[dict]) -> dict[str, dict[str, float]]:
    tf = {}
    for art in articles:
        slug = art['slug']
        title_tokens = tokenize(art.get('title', '')) * 3
        tag_tokens = [w for tag in art.get('tags', []) for w in tag.split()] * 3
        body_tokens = tokenize(art['body'])
        all_tokens = title_tokens + tag_tokens + body_tokens
        counts = Counter(all_tokens)
        total = sum(counts.values())
        tf[slug] = {term: count / total for term, count in counts.items()}

    N = len(articles)
    df = Counter()
    for vec in tf.values():
        for term in vec:
            df[term] += 1
    idf = {term: math.log(N / count + 1) for term, count in df.items()}

    tfidf = {}
    for slug, vec in tf.items():
        tfidf[slug] = {term: score * idf.get(term, 1.0) for term, score in vec.items()}
    return tfidf


def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    common = set(vec_a) & set(vec_b)
    if not common:
        return 0.0
    dot = sum(vec_a[t] * vec_b[t] for t in common)
    mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
    mag_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def build_paragraphs(body: str) -> list[tuple[int, int, str]]:
    para_pattern = re.compile(r'\n{2,}')
    paragraphs = []
    start = 0
    for m in para_pattern.finditer(body):
        paragraphs.append((start, m.start(), body[start:m.start()]))
        start = m.end()
    paragraphs.append((start, len(body), body[start:]))
    return paragraphs


def is_injectable_paragraph(para: str, pstart: int, min_offset: int) -> bool:
    """Return True if this paragraph is a valid injection point."""
    stripped = para.strip()
    if pstart < min_offset:
        return False
    if not stripped or len(stripped) < 40:
        return False
    if stripped.startswith('#'):
        return False
    if stripped.startswith('```') or para.startswith('    '):
        return False
    return True


def find_best_paragraph(
    body: str,
    target_title: str,
    used_positions: list[int],
    min_offset: int = 100,
) -> int:
    """
    Return the character offset after the best paragraph for link injection.
    Falls back through progressively relaxed constraints.
    Returns -1 if no suitable position found.
    """
    keywords = set(tokenize(target_title))
    paragraphs = build_paragraphs(body)

    def score_and_pick(paras, gap: int) -> int:
        best_score = -1
        best_end = -1
        for (pstart, pend, para) in paras:
            if not is_injectable_paragraph(para, pstart, min_offset):
                continue
            too_close = any(abs(pend - used) < gap for used in used_positions)
            if too_close:
                continue
            score = len(keywords & set(tokenize(para))) if keywords else 0
            if score > best_score:
                best_score = score
                best_end = pend
        return best_end

    # Pass 1: normal constraints
    result = score_and_pick(paragraphs, MIN_LINK_GAP)
    if result != -1:
        return result

    # Pass 2: halved gap constraint
    result = score_and_pick(paragraphs, MIN_LINK_GAP // 2)
    if result != -1:
        return result

    # Pass 3: no gap constraint (any qualifying paragraph)
    result = score_and_pick(paragraphs, 0)
    if result != -1:
        return result

    # Pass 4: no gap, no min_offset (any paragraph at all)
    for (pstart, pend, para) in paragraphs:
        stripped = para.strip()
        if not stripped or len(stripped) < 40:
            continue
        if stripped.startswith('#') or stripped.startswith('```'):
            continue
        return pend

    return -1


def link_already_exists(body: str, target_slug: str) -> bool:
    return f'/blog/{target_slug}' in body


def build_link_sentence(target_title: str, target_slug: str) -> str:
    return f'\n\nFor more on this topic, see [*{target_title}*](/blog/{target_slug}).'


def build_seealso_section(targets: list[tuple[str, str]]) -> str:
    """Build a '## See also' section for articles where inline injection fails."""
    lines = ['\n\n## See Also\n']
    for title, slug in targets:
        lines.append(f'- [*{title}*](/blog/{slug})')
    return '\n'.join(lines)


def process_site(site_path: Path) -> int:
    blog_dir = site_path / "src" / "content" / "blog"
    if not blog_dir.exists():
        return 0

    md_files = list(blog_dir.glob("*.md"))
    if len(md_files) < MIN_ARTICLES_FOR_SITE:
        return 0

    articles = []
    for md_file in sorted(md_files):
        raw = md_file.read_text(encoding='utf-8')
        fm, body = parse_frontmatter(raw)
        tags = extract_tags(raw)
        articles.append({
            'slug': md_file.stem,
            'title': fm.get('title', md_file.stem),
            'tags': tags,
            'body': body,
            'path': md_file,
            'raw': raw,
        })

    if len(articles) < MIN_ARTICLES_FOR_SITE:
        return 0

    tfidf = compute_tfidf_vectors(articles)
    slug_to_art = {art['slug']: art for art in articles}

    # Pre-populate linked pairs from existing links
    linked_pairs: set[tuple[str, str]] = set()
    for art in articles:
        for m in re.finditer(r'\(/blog/([^)]+)\)', art['body']):
            linked_pairs.add((art['slug'], m.group(1)))

    total_added = 0

    for art in articles:
        src_slug = art['slug']
        existing = count_existing_blog_links(art['body'])
        if existing >= TARGET_LINKS_PER_ARTICLE:
            continue

        # Score all other articles by TF-IDF similarity
        scores = []
        for other in articles:
            if other['slug'] == src_slug:
                continue
            sim = cosine_similarity(tfidf[src_slug], tfidf[other['slug']])
            scores.append((sim, other['slug']))
        scores.sort(reverse=True)

        # Split targets into: preferred (non-circular) and fallback (circular)
        preferred = [(sim, slug) for sim, slug in scores
                     if (slug, src_slug) not in linked_pairs]
        fallback = [(sim, slug) for sim, slug in scores
                    if (slug, src_slug) in linked_pairs]

        # Try preferred first, then fallback
        candidate_queue = preferred + fallback

        added = 0
        needed = TARGET_LINKS_PER_ARTICLE - existing
        modified_body = art['body']
        used_positions: list[int] = []
        seealso_targets: list[tuple[str, str]] = []

        # Pre-populate used positions from existing internal links
        for m in re.finditer(r'\(/blog/[^)]+\)', modified_body):
            used_positions.append(m.start())

        for _, target_slug in candidate_queue:
            if added >= needed:
                break
            if link_already_exists(modified_body, target_slug):
                continue

            target = slug_to_art[target_slug]
            insert_pos = find_best_paragraph(
                modified_body, target['title'], used_positions
            )

            if insert_pos == -1:
                # Queue for "See also" section if we can't inject inline
                seealso_targets.append((target['title'], target_slug))
                continue

            link_sentence = build_link_sentence(target['title'], target_slug)
            modified_body = (
                modified_body[:insert_pos]
                + link_sentence
                + modified_body[insert_pos:]
            )
            used_positions.append(insert_pos)
            linked_pairs.add((src_slug, target_slug))
            added += 1
            total_added += 1

        # If still short of MIN_LINKS_PER_ARTICLE, append a See Also section
        remaining_needed = needed - added
        if remaining_needed > 0 and seealso_targets:
            sa_entries = seealso_targets[:remaining_needed]
            # Also pick more from candidate_queue if we have them
            if len(sa_entries) < remaining_needed:
                for _, tslug in candidate_queue:
                    if len(sa_entries) >= remaining_needed:
                        break
                    if not link_already_exists(modified_body, tslug):
                        if tslug not in [s for _, s in sa_entries]:
                            sa_entries.append((slug_to_art[tslug]['title'], tslug))

            modified_body = modified_body.rstrip() + build_seealso_section(sa_entries)
            for t, s in sa_entries:
                linked_pairs.add((src_slug, s))
                added += 1
                total_added += 1

        if added > 0:
            new_content = art['raw'].replace(art['body'], modified_body, 1)
            art['path'].write_text(new_content, encoding='utf-8')
            art['body'] = modified_body
            art['raw'] = new_content

    return total_added


def main():
    site_filter = sys.argv[1] if len(sys.argv) > 1 else None
    grand_total = 0

    for site_path in sorted(SITES_DIR.iterdir()):
        if not site_path.is_dir():
            continue
        if site_filter and site_path.name != site_filter:
            continue

        blog_dir = site_path / "src" / "content" / "blog"
        if not blog_dir.exists():
            continue
        count = len(list(blog_dir.glob("*.md")))
        if count < MIN_ARTICLES_FOR_SITE:
            continue

        added = process_site(site_path)
        if added > 0:
            print(f"  {site_path.name}: +{added} links")
        else:
            print(f"  {site_path.name}: (no new links needed)")
        grand_total += added

    print(f"\nTotal links added: {grand_total}")


if __name__ == "__main__":
    main()
