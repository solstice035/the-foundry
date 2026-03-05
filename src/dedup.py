"""
Deduplication utilities for The Foundry.

Implements keyword extraction and Jaccard similarity-based deduplication
to prevent building duplicate projects.
"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# Common stop words to filter out
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "will",
    "with",
    "the",
    "this",
    "but",
    "they",
    "have",
    "had",
    "what",
    "when",
    "where",
    "who",
    "which",
    "why",
    "how",
    "all",
    "each",
    "every",
    "both",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "can",
    "just",
    "should",
    "now",
    "using",
}


def extract_keywords(title: str) -> List[str]:
    """
    Extract keywords from a trend title.

    Process:
    1. Lowercase and remove all punctuation (including hyphens)
    2. Split on whitespace
    3. Basic stemming (remove common suffixes)
    4. Filter out stop words
    5. Filter out words <= 2 characters
    6. Return unique keywords

    Args:
        title: The trend title or project description

    Returns:
        List of keyword strings

    Example:
        >>> extract_keywords("Privacy-first PDF tool to merge and split PDFs")
        ['privaci', 'pdf', 'tool', 'merg', 'split']
    """
    if not title:
        return []

    # Lowercase and remove all punctuation
    clean = re.sub(r"[^a-z0-9\s]", " ", title.lower())

    # Split on whitespace
    words = clean.split()

    # Basic stemming - remove common suffixes
    def stem_word(word):
        # Remove plural 's' or 'es'
        if word.endswith("ies") and len(word) > 4:
            return word[:-3] + "y"
        if word.endswith("es") and len(word) > 3:
            return word[:-2]
        if word.endswith("s") and len(word) > 3:
            return word[:-1]
        # Remove -ing
        if word.endswith("ing") and len(word) > 5:
            return word[:-3]
        # Remove -ed
        if word.endswith("ed") and len(word) > 4:
            return word[:-2]
        # Remove -er
        if word.endswith("er") and len(word) > 4:
            return word[:-2]
        return word

    # Filter stop words, apply stemming, and filter short words
    keywords = []
    for w in words:
        if w not in STOP_WORDS and len(w) > 2:
            stemmed = stem_word(w)
            if len(stemmed) > 2:
                keywords.append(stemmed)

    # Return unique keywords while preserving order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)

    return unique_keywords


def jaccard_similarity(keywords1: List[str], keywords2: List[str]) -> float:
    """
    Calculate Jaccard similarity between two keyword sets.

    Jaccard similarity = |A ∩ B| / |A ∪ B|

    Args:
        keywords1: First set of keywords
        keywords2: Second set of keywords

    Returns:
        Similarity score from 0.0 (no overlap) to 1.0 (identical)

    Example:
        >>> jaccard_similarity(['pdf', 'merge', 'split'], ['pdf', 'tool', 'merge'])
        0.5  # 2 common words / 4 unique words
    """
    if not keywords1 or not keywords2:
        return 0.0

    set1 = set(keywords1)
    set2 = set(keywords2)

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    if union == 0:
        return 0.0

    return intersection / union


def is_duplicate(
    title: str, history: Dict, threshold: float = 0.5, window_days: int = 30
) -> Optional[Dict]:
    """
    Check if a trend title is a duplicate of a recent build.

    Args:
        title: The trend title to check
        history: History dict loaded from history.json
        threshold: Jaccard similarity threshold (default 0.5 = 50%)
        window_days: How many days back to check (default 30)

    Returns:
        Dict with duplicate info if found, None otherwise
        Format: {
            'is_duplicate': True,
            'matched_build': {...},
            'similarity': 0.75,
            'matched_keywords': ['pdf', 'merge']
        }

    Example:
        >>> history = {'builds': [{'date': '2026-02-18', 'title': 'PDF merge tool', 'keywords': ['pdf', 'merge']}]}
        >>> is_duplicate('New PDF merging utility', history)
        {'is_duplicate': True, 'matched_build': {...}, 'similarity': 0.66, ...}
    """
    # Extract keywords from the new title
    new_keywords = extract_keywords(title)

    if not new_keywords:
        return None

    # Calculate cutoff date
    cutoff_date = (datetime.now() - timedelta(days=window_days)).strftime("%Y-%m-%d")

    # Check builds
    builds = history.get("builds", [])
    for build in builds:
        # Skip builds outside the window
        if build.get("date", "") < cutoff_date:
            continue

        # Get keywords from build
        build_keywords = build.get("keywords", [])
        if not build_keywords:
            # Fallback: extract from build title if keywords missing
            build_keywords = extract_keywords(build.get("title", ""))

        # Calculate similarity
        similarity = jaccard_similarity(new_keywords, build_keywords)

        # Check if it exceeds threshold
        if similarity >= threshold:
            matched_keywords = list(set(new_keywords) & set(build_keywords))
            return {
                "is_duplicate": True,
                "matched_build": build,
                "similarity": similarity,
                "matched_keywords": matched_keywords,
                "reason": f"Duplicate of {build.get('date')} build '{build.get('project_name')}' ({similarity:.0%} keyword overlap)",
            }

    # Check rejections
    rejections = history.get("rejections", [])
    for rejection in rejections:
        # Skip rejections outside the window
        if rejection.get("date", "") < cutoff_date:
            continue

        # Get keywords from rejection
        rejection_keywords = rejection.get("keywords", [])
        if not rejection_keywords:
            # Fallback: extract from rejection title if keywords missing
            rejection_keywords = extract_keywords(rejection.get("title", ""))

        # Calculate similarity
        similarity = jaccard_similarity(new_keywords, rejection_keywords)

        # Check if it exceeds threshold
        if similarity >= threshold:
            matched_keywords = list(set(new_keywords) & set(rejection_keywords))
            return {
                "is_duplicate": True,
                "matched_rejection": rejection,
                "similarity": similarity,
                "matched_keywords": matched_keywords,
                "reason": f"Duplicate of {rejection.get('date')} rejection: {rejection.get('reason')} ({similarity:.0%} keyword overlap)",
            }

    return None


def add_build_to_history(history_path: str, build_info: Dict) -> None:
    """
    Append a successful build to history.json.

    Args:
        history_path: Path to history.json
        build_info: Dict with keys: date, project_name, title, repo_url, status, source
                   (keywords will be auto-extracted if not provided)
    """
    import json

    # Load existing history
    try:
        with open(history_path, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize if missing or corrupted
        history = {
            "schema_version": 1,
            "builds": [],
            "rejections": [],
            "dedup_window_days": 30,
        }

    # Extract keywords if not provided
    if "keywords" not in build_info:
        build_info["keywords"] = extract_keywords(build_info.get("title", ""))

    # Append to builds
    history["builds"].append(build_info)

    # Write back
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)


def add_rejection_to_history(history_path: str, rejection_info: Dict) -> None:
    """
    Append a rejection to history.json.

    Args:
        history_path: Path to history.json
        rejection_info: Dict with keys: date, title, reason, source
                       (keywords will be auto-extracted if not provided)
    """
    import json

    # Load existing history
    try:
        with open(history_path, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize if missing or corrupted
        history = {
            "schema_version": 1,
            "builds": [],
            "rejections": [],
            "dedup_window_days": 30,
        }

    # Extract keywords if not provided
    if "keywords" not in rejection_info:
        rejection_info["keywords"] = extract_keywords(rejection_info.get("title", ""))

    # Append to rejections
    history["rejections"].append(rejection_info)

    # Write back
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)


def cleanup_history(history_path: str, archive_days: int = 90) -> Dict:
    """
    Clean up old entries from history.json.

    Removes builds and rejections older than archive_days.

    Args:
        history_path: Path to history.json
        archive_days: Keep entries from the last N days (default 90)

    Returns:
        Dict with cleanup stats: {'builds_removed': 2, 'rejections_removed': 1}
    """
    import json

    # Load history
    with open(history_path, "r") as f:
        history = json.load(f)

    # Calculate cutoff date
    cutoff_date = (datetime.now() - timedelta(days=archive_days)).strftime("%Y-%m-%d")

    # Filter builds
    old_builds_count = len(history.get("builds", []))
    history["builds"] = [
        b for b in history.get("builds", []) if b.get("date", "") >= cutoff_date
    ]
    builds_removed = old_builds_count - len(history["builds"])

    # Filter rejections
    old_rejections_count = len(history.get("rejections", []))
    history["rejections"] = [
        r for r in history.get("rejections", []) if r.get("date", "") >= cutoff_date
    ]
    rejections_removed = old_rejections_count - len(history["rejections"])

    # Write back
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    return {"builds_removed": builds_removed, "rejections_removed": rejections_removed}


if __name__ == "__main__":
    # Quick test
    print("Testing keyword extraction:")
    title = "Privacy-first PDF tool to merge and split PDFs in the browser"
    keywords = extract_keywords(title)
    print(f"  Title: {title}")
    print(f"  Keywords: {keywords}")
    print()

    print("Testing Jaccard similarity:")
    kw1 = ["pdf", "merge", "split", "browser"]
    kw2 = ["pdf", "tool", "merge", "compress"]
    sim = jaccard_similarity(kw1, kw2)
    print(f"  Set 1: {kw1}")
    print(f"  Set 2: {kw2}")
    print(f"  Similarity: {sim:.2%}")
    print()

    print("Testing duplicate detection:")
    history = {
        "schema_version": 1,
        "builds": [
            {
                "date": "2026-02-18",
                "project_name": "pdf-privacy-tools",
                "title": "Privacy-first PDF merge tool",
                "keywords": ["pdf", "privacy", "merge", "browser"],
            }
        ],
        "rejections": [],
        "dedup_window_days": 30,
    }

    test_title = "New PDF merging and splitting utility"
    result = is_duplicate(test_title, history)
    print(f"  New title: {test_title}")
    if result:
        print(f"  DUPLICATE FOUND: {result['reason']}")
        print(f"  Similarity: {result['similarity']:.0%}")
        print(f"  Matched keywords: {result['matched_keywords']}")
    else:
        print("  No duplicate found")
