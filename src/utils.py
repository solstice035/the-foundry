"""
Common utilities for The Foundry agents
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


def load_json(file_path: Path) -> Dict[str, Any]:
    """
    Load and parse a JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: Path, indent: int = 2) -> None:
    """
    Save data as JSON file.

    Args:
        data: Dictionary to save
        file_path: Destination path
        indent: JSON indentation (default: 2)
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def extract_keywords(text: str, stop_words: Optional[Set[str]] = None) -> List[str]:
    """
    Extract keywords from text for deduplication matching.

    Converts to lowercase, removes punctuation, filters stop words.

    Args:
        text: Input text (trend title, etc.)
        stop_words: Set of words to filter out

    Returns:
        List of keywords

    Example:
        >>> extract_keywords("AI-powered commit message generator")
        ['ai', 'powered', 'commit', 'message', 'generator']
    """
    if stop_words is None:
        stop_words = {
            "a",
            "an",
            "the",
            "for",
            "with",
            "using",
            "from",
            "to",
            "in",
            "on",
            "at",
            "by",
            "of",
            "is",
            "are",
            "was",
            "were",
        }

    # Lowercase and remove punctuation
    clean = re.sub(r"[^a-z0-9\s]", "", text.lower())

    # Split on whitespace
    words = clean.split()

    # Filter stop words and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    return keywords


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    Calculate Jaccard similarity between two sets.

    Jaccard similarity = |intersection| / |union|

    Args:
        set1: First set
        set2: Second set

    Returns:
        Similarity score (0.0 to 1.0)

    Example:
        >>> jaccard_similarity({'a', 'b', 'c'}, {'b', 'c', 'd'})
        0.5  # 2 in common, 4 total unique
    """
    if not set1 or not set2:
        return 0.0

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union if union > 0 else 0.0


def keyword_overlap(text1: str, text2: str, threshold: float = 0.5) -> float:
    """
    Calculate keyword overlap between two texts.

    Uses keyword extraction + Jaccard similarity.

    Args:
        text1: First text
        text2: Second text
        threshold: Similarity threshold (default: 0.5)

    Returns:
        Jaccard similarity score
    """
    keywords1 = set(extract_keywords(text1))
    keywords2 = set(extract_keywords(text2))

    return jaccard_similarity(keywords1, keywords2)


def is_duplicate(
    new_title: str, existing_titles: List[str], threshold: float = 0.5
) -> tuple[bool, Optional[str]]:
    """
    Check if a new title is a duplicate of any existing title.

    Args:
        new_title: Title to check
        existing_titles: List of existing titles
        threshold: Similarity threshold (default: 0.5 = 50% overlap)

    Returns:
        (is_duplicate, matching_title) tuple
    """
    for existing in existing_titles:
        similarity = keyword_overlap(new_title, existing)
        if similarity >= threshold:
            return (True, existing)

    return (False, None)


def get_today_date() -> str:
    """
    Get today's date in YYYY-MM-DD format.

    Returns:
        Date string (e.g., "2026-02-18")
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_today_datetime() -> str:
    """
    Get current datetime in ISO 8601 format.

    Returns:
        Datetime string (e.g., "2026-02-18T19:15:00Z")
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_engagement(
    value: float, platform: str, max_values: Optional[Dict[str, float]] = None
) -> float:
    """
    Normalize engagement score to 0-100 scale.

    Args:
        value: Raw engagement value (points, score, etc.)
        platform: Platform name ('hn', 'reddit')
        max_values: Platform-specific max values (optional)

    Returns:
        Normalized score (0-100)
    """
    if max_values is None:
        max_values = {
            "hn": 500,  # HN points
            "reddit": 2000,  # Reddit score
        }

    max_val = max_values.get(platform, 1000)
    normalized = (value / max_val) * 100

    return min(100, normalized)


def cross_source_amplification(source_count: int) -> float:
    """
    Calculate amplification multiplier for cross-source trends.

    Args:
        source_count: Number of sources where trend appeared

    Returns:
        Amplification multiplier

    Examples:
        >>> cross_source_amplification(1)
        1.0  # No amplification
        >>> cross_source_amplification(2)
        1.3
        >>> cross_source_amplification(4)
        2.0
    """
    if source_count <= 1:
        return 1.0
    elif source_count == 2:
        return 1.3
    elif source_count == 3:
        return 1.6
    else:  # 4+
        return 2.0


def validate_schema(data: Dict[str, Any], schema_path: Path) -> bool:
    """
    Validate JSON data against a schema.

    Args:
        data: Data to validate
        schema_path: Path to JSON schema file

    Returns:
        True if valid, raises exception if invalid

    Raises:
        jsonschema.ValidationError: If data doesn't match schema
    """
    import jsonschema

    schema = load_json(schema_path)
    jsonschema.validate(data, schema)
    return True
