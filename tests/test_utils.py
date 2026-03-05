"""
Tests for src/utils.py
"""

from src.utils import (
    extract_keywords,
    jaccard_similarity,
    keyword_overlap,
    is_duplicate,
    normalize_engagement,
    cross_source_amplification,
)


class TestKeywordExtraction:
    """Test keyword extraction utilities"""

    def test_extract_keywords_basic(self):
        """Test basic keyword extraction"""
        text = "AI-powered commit message generator"
        keywords = extract_keywords(text)

        assert "aipowered" in keywords or "ai" in keywords
        assert "commit" in keywords
        assert "message" in keywords
        assert "generator" in keywords
        # Stop words should be filtered
        assert "the" not in keywords
        assert "a" not in keywords

    def test_extract_keywords_with_punctuation(self):
        """Test keyword extraction handles punctuation"""
        text = "Real-time collaborative whiteboard (WebSocket)"
        keywords = extract_keywords(text)

        assert "realtime" in keywords or "real" in keywords
        assert "collaborative" in keywords
        assert "whiteboard" in keywords
        assert "websocket" in keywords

    def test_extract_keywords_filters_short_words(self):
        """Test that words <=2 chars are filtered"""
        text = "AI ML is at a new level"
        keywords = extract_keywords(text)

        # Short words filtered
        assert "is" not in keywords
        assert "at" not in keywords
        assert "a" not in keywords
        # But longer words kept
        assert "new" in keywords
        assert "level" in keywords


class TestJaccardSimilarity:
    """Test Jaccard similarity calculations"""

    def test_identical_sets(self):
        """Test similarity of identical sets"""
        set1 = {"a", "b", "c"}
        set2 = {"a", "b", "c"}

        assert jaccard_similarity(set1, set2) == 1.0

    def test_disjoint_sets(self):
        """Test similarity of completely different sets"""
        set1 = {"a", "b", "c"}
        set2 = {"d", "e", "f"}

        assert jaccard_similarity(set1, set2) == 0.0

    def test_partial_overlap(self):
        """Test similarity with partial overlap"""
        set1 = {"a", "b", "c"}
        set2 = {"b", "c", "d"}

        # 2 in common, 4 total unique
        assert jaccard_similarity(set1, set2) == 0.5

    def test_empty_sets(self):
        """Test similarity with empty sets"""
        assert jaccard_similarity(set(), set()) == 0.0
        assert jaccard_similarity({"a"}, set()) == 0.0


class TestKeywordOverlap:
    """Test keyword overlap detection"""

    def test_similar_titles(self):
        """Test overlap between similar titles"""
        title1 = "AI-powered commit message generator"
        title2 = "Commit message generator using AI"

        overlap = keyword_overlap(title1, title2)

        # Should have high overlap (ai, commit, message, generator)
        assert overlap > 0.7

    def test_different_titles(self):
        """Test overlap between different titles"""
        title1 = "AI commit message generator"
        title2 = "Real-time collaborative whiteboard"

        overlap = keyword_overlap(title1, title2)

        # Should have low/no overlap
        assert overlap < 0.2


class TestDuplicateDetection:
    """Test duplicate detection"""

    def test_exact_duplicate(self):
        """Test detection of exact duplicate"""
        new_title = "AI commit message generator"
        existing = ["AI commit message generator tool"]

        is_dup, match = is_duplicate(new_title, existing, threshold=0.5)

        assert is_dup
        assert match == "AI commit message generator tool"

    def test_not_duplicate(self):
        """Test non-duplicate detection"""
        new_title = "Web scraper for GitHub trending"
        existing = ["AI commit message generator"]

        is_dup, match = is_duplicate(new_title, existing, threshold=0.5)

        assert not is_dup
        assert match is None

    def test_threshold_sensitivity(self):
        """Test threshold affects duplicate detection"""
        new_title = "AI powered tool"
        existing = ["AI powered commit message tool"]

        # High threshold (0.8) = not duplicate
        is_dup_high, _ = is_duplicate(new_title, existing, threshold=0.8)
        assert not is_dup_high

        # Low threshold (0.5) = is duplicate
        is_dup_low, _ = is_duplicate(new_title, existing, threshold=0.5)
        assert is_dup_low


class TestEngagementNormalization:
    """Test engagement score normalization"""

    def test_hn_normalization(self):
        """Test HN points normalization"""
        # 250 points on HN (max 500)
        score = normalize_engagement(250, "hn")
        assert score == 50.0

    def test_reddit_normalization(self):
        """Test Reddit score normalization"""
        # 1000 score on Reddit (max 2000)
        score = normalize_engagement(1000, "reddit")
        assert score == 50.0

    def test_x_normalization(self):
        """Test X retweets normalization"""
        # 100 retweets on X (max 500)
        score = normalize_engagement(100, "x")
        assert score == 20.0

    def test_max_capping(self):
        """Test that scores are capped at 100"""
        # 1000 points on HN (exceeds max 500)
        score = normalize_engagement(1000, "hn")
        assert score == 100.0


class TestCrossSourceAmplification:
    """Test cross-source amplification multipliers"""

    def test_single_source(self):
        """Test no amplification for single source"""
        assert cross_source_amplification(1) == 1.0

    def test_two_sources(self):
        """Test 1.3x amplification for 2 sources"""
        assert cross_source_amplification(2) == 1.3

    def test_three_sources(self):
        """Test 1.6x amplification for 3 sources"""
        assert cross_source_amplification(3) == 1.6

    def test_four_plus_sources(self):
        """Test 2.0x amplification for 4+ sources"""
        assert cross_source_amplification(4) == 2.0
        assert cross_source_amplification(5) == 2.0
