#!/usr/bin/env python3
"""
Epic 2.3: Trend Lifecycle Tracking - Test Suite

Tests lifecycle detection logic for rising, peaked, stable, and new trends.
Validates momentum scoring and engagement trajectory calculation.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple


class TrendMatcher:
    """Match trends across multiple nights using URL and fuzzy title matching."""
    
    @staticmethod
    def normalize_title(title: str) -> set:
        """Extract keywords from title for fuzzy matching."""
        import re
        stopwords = {'a', 'an', 'the', 'for', 'with', 'using', 'from', 'to', 
                    'in', 'on', 'at', 'by', 'show', 'hn', 'i', 'built', 'my', 
                    'first', 'based'}
        # Split on both spaces and hyphens to handle compound words
        words = re.split(r'[\s\-]+', title.lower())
        keywords = {w for w in words if len(w) > 3 and w not in stopwords}
        return keywords
    
    @staticmethod
    def jaccard_similarity(set1: set, set2: set) -> float:
        """Calculate Jaccard similarity between two sets."""
        if not set1 or not set2:
            return 0.0
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union)
    
    @staticmethod
    def match_trend(trend: dict, history: List[dict], threshold: float = 0.6) -> List[Tuple[str, dict]]:
        """
        Match a trend against historical trends.
        
        Returns list of (date, historical_trend) tuples for matches.
        """
        matches = []
        trend_url = trend.get('url', '')
        trend_keywords = TrendMatcher.normalize_title(trend['title'])
        
        for entry in history:
            date = entry['date']
            for hist_trend in entry['trends']:
                # Exact URL match
                if trend_url and hist_trend.get('url') == trend_url:
                    matches.append((date, hist_trend))
                    continue
                
                # Fuzzy title match
                # If historical trend has pre-computed keywords, use them
                # Otherwise extract from title
                if 'keywords' in hist_trend:
                    hist_keywords = set(hist_trend.get('keywords', []))
                else:
                    hist_keywords = TrendMatcher.normalize_title(hist_trend['title'])
                
                similarity = TrendMatcher.jaccard_similarity(trend_keywords, hist_keywords)
                if similarity >= threshold:
                    matches.append((date, hist_trend))
        
        return matches


class LifecycleCalculator:
    """Calculate lifecycle status and momentum for trends."""
    
    @staticmethod
    def calculate_trajectory(scores: List[float]) -> str:
        """
        Determine engagement trajectory from score history.
        
        Returns: "upward", "downward", or "flat"
        """
        if len(scores) < 2:
            return "flat"
        
        recent = scores[-1]
        median = sorted(scores[:-1])[len(scores[:-1]) // 2] if len(scores) > 2 else scores[0]
        
        threshold = 0.2  # 20% tolerance
        if recent > median * (1 + threshold):
            return "upward"
        elif recent < median * (1 - threshold):
            return "downward"
        else:
            return "flat"
    
    @staticmethod
    def calculate_status(appearances: int, trajectory: str) -> str:
        """
        Determine lifecycle status.
        
        Returns: "new", "rising", "peaked", or "stable"
        """
        if appearances <= 1:
            return "new"
        
        if trajectory == "upward":
            return "rising"
        elif trajectory == "downward":
            return "peaked"
        else:
            return "stable"
    
    @staticmethod
    def calculate_momentum(status: str, scores: List[float]) -> float:
        """
        Calculate momentum score multiplier (0.2 - 2.0).
        
        - new: 1.0
        - rising: 1.0 + growth_rate (capped at 2.0)
        - peaked: 1.0 - decline_rate (floor at 0.2)
        - stable: 1.0
        """
        if status == "new":
            return 1.0
        
        if len(scores) < 2:
            return 1.0
        
        first_score = scores[0]
        recent_score = scores[-1]
        
        if status == "rising":
            growth_rate = (recent_score - first_score) / first_score if first_score > 0 else 0
            momentum = 1.0 + min(growth_rate, 1.0)
            return min(momentum, 2.0)
        
        elif status == "peaked":
            decline_rate = (first_score - recent_score) / first_score if first_score > 0 else 0
            momentum = 1.0 - min(decline_rate, 0.8)
            return max(momentum, 0.2)
        
        else:  # stable
            return 1.0


def load_mock_history(start_date: str, num_days: int = 4) -> List[dict]:
    """Load mock trend history files."""
    history = []
    base_path = Path(__file__).parent / 'mock_trends'
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    for i in range(num_days):
        date = (start + timedelta(days=i)).strftime('%Y-%m-%d')
        file_path = base_path / f"{date}.json"
        
        if file_path.exists():
            with open(file_path) as f:
                history.append(json.load(f))
    
    return history


def enrich_trend_with_lifecycle(trend: dict, history: List[dict]) -> dict:
    """
    Enrich a single trend with lifecycle metadata.
    
    This is the core logic that would run in the Trend Researcher agent.
    """
    matcher = TrendMatcher()
    calc = LifecycleCalculator()
    
    # Match trend against history
    matches = matcher.match_trend(trend, history)
    
    # Build engagement history
    engagement_history = []
    for date, hist_trend in matches:
        engagement_history.append({
            'date': date,
            'score': hist_trend['engagement_score']
        })
    
    # Add current observation
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_score = trend.get('engagement_score', 0)
    engagement_history.append({
        'date': current_date,
        'score': current_score
    })
    
    # Sort by date
    engagement_history.sort(key=lambda x: x['date'])
    
    # Extract scores
    scores = [e['score'] for e in engagement_history]
    appearances = len(engagement_history)
    first_seen = engagement_history[0]['date']
    days_active = (datetime.strptime(engagement_history[-1]['date'], '%Y-%m-%d') - 
                   datetime.strptime(first_seen, '%Y-%m-%d')).days + 1
    
    # Calculate lifecycle metrics
    trajectory = calc.calculate_trajectory(scores)
    status = calc.calculate_status(appearances, trajectory)
    momentum_score = calc.calculate_momentum(status, scores)
    
    # Build lifecycle metadata
    trend['lifecycle'] = {
        'status': status,
        'trajectory': trajectory,
        'first_seen': first_seen,
        'appearances': appearances,
        'engagement_history': engagement_history,
        'days_active': days_active,
        'momentum_score': round(momentum_score, 2)
    }
    
    return trend


# ============================================================================
# TEST CASES
# ============================================================================

def test_new_trend():
    """Test: First-time trend should be marked as 'new'."""
    print("\n[TEST] New trend detection...")
    
    trend = {
        'id': 'trend-20260226-999',
        'title': 'Brand new trend never seen before',
        'url': 'https://example.com/new',
        'engagement_score': 50
    }
    
    history = load_mock_history('2026-02-23', num_days=3)
    enriched = enrich_trend_with_lifecycle(trend, history)
    
    assert enriched['lifecycle']['status'] == 'new', f"Expected 'new', got {enriched['lifecycle']['status']}"
    assert enriched['lifecycle']['appearances'] == 1, f"Expected 1 appearance, got {enriched['lifecycle']['appearances']}"
    assert enriched['lifecycle']['momentum_score'] == 1.0, f"Expected momentum 1.0, got {enriched['lifecycle']['momentum_score']}"
    
    print(f"✅ PASS: {enriched['lifecycle']}")


def test_rising_trend():
    """Test: Trend with increasing engagement should be marked as 'rising'."""
    print("\n[TEST] Rising trend detection...")
    
    # PDF Privacy Tools appears on all 4 nights with increasing engagement:
    # 2026-02-23: 45
    # 2026-02-24: 67
    # 2026-02-25: 102
    # 2026-02-26: 95 (slight dip but still rising overall)
    
    trend = {
        'id': 'trend-20260226-001',
        'title': 'Privacy-first PDF toolkit for browsers',
        'url': 'https://reddit.com/r/SideProject/pdf_privacy_tools',
        'engagement_score': 102  # Simulating 2026-02-25
    }
    
    # Load history up to 2026-02-24 (3 days)
    history = load_mock_history('2026-02-23', num_days=2)
    enriched = enrich_trend_with_lifecycle(trend, history)
    
    assert enriched['lifecycle']['status'] == 'rising', f"Expected 'rising', got {enriched['lifecycle']['status']}"
    assert enriched['lifecycle']['trajectory'] == 'upward', f"Expected 'upward', got {enriched['lifecycle']['trajectory']}"
    assert enriched['lifecycle']['appearances'] == 3, f"Expected 3 appearances, got {enriched['lifecycle']['appearances']}"
    assert enriched['lifecycle']['momentum_score'] > 1.0, f"Expected momentum > 1.0, got {enriched['lifecycle']['momentum_score']}"
    
    print(f"✅ PASS: {enriched['lifecycle']}")


def test_peaked_trend():
    """Test: Trend with declining engagement should be marked as 'peaked'."""
    print("\n[TEST] Peaked trend detection...")
    
    # Docker CLI appears on all 4 nights with declining engagement:
    # 2026-02-23: 120
    # 2026-02-24: 95
    # 2026-02-25: 78
    # 2026-02-26: 62
    
    trend = {
        'id': 'trend-20260226-002',
        'title': 'Docker TUI management CLI',
        'url': 'https://news.ycombinator.com/item?id=12345',
        'engagement_score': 62
    }
    
    history = load_mock_history('2026-02-23', num_days=3)
    enriched = enrich_trend_with_lifecycle(trend, history)
    
    assert enriched['lifecycle']['status'] == 'peaked', f"Expected 'peaked', got {enriched['lifecycle']['status']}"
    assert enriched['lifecycle']['trajectory'] == 'downward', f"Expected 'downward', got {enriched['lifecycle']['trajectory']}"
    assert enriched['lifecycle']['appearances'] == 4, f"Expected 4 appearances, got {enriched['lifecycle']['appearances']}"
    assert enriched['lifecycle']['momentum_score'] < 1.0, f"Expected momentum < 1.0, got {enriched['lifecycle']['momentum_score']}"
    
    print(f"✅ PASS: {enriched['lifecycle']}")


def test_stable_trend():
    """Test: Trend with flat engagement should be marked as 'stable'."""
    print("\n[TEST] Stable trend detection...")
    
    # RSS Reader appears on 3 nights with relatively flat engagement:
    # 2026-02-23: 67
    # 2026-02-24: 72
    # 2026-02-25: 65
    
    trend = {
        'id': 'trend-20260225-003',
        'title': 'Self-hosted RSS with AI summaries',
        'url': 'https://reddit.com/r/selfhosted/ai_rss',
        'engagement_score': 65
    }
    
    history = load_mock_history('2026-02-23', num_days=2)
    enriched = enrich_trend_with_lifecycle(trend, history)
    
    assert enriched['lifecycle']['status'] == 'stable', f"Expected 'stable', got {enriched['lifecycle']['status']}"
    assert enriched['lifecycle']['trajectory'] == 'flat', f"Expected 'flat', got {enriched['lifecycle']['trajectory']}"
    assert enriched['lifecycle']['momentum_score'] == 1.0, f"Expected momentum 1.0, got {enriched['lifecycle']['momentum_score']}"
    
    print(f"✅ PASS: {enriched['lifecycle']}")


def test_explosive_growth():
    """Test: Trend with explosive growth gets high momentum boost."""
    print("\n[TEST] Explosive growth momentum...")
    
    # GitHub Actions alternative explodes:
    # 2026-02-24: 140
    # 2026-02-25: 185
    # 2026-02-26: 245
    
    trend = {
        'id': 'trend-20260226-003',
        'title': 'GitHub Actions local alternative',
        'url': 'https://news.ycombinator.com/item?id=12347',
        'engagement_score': 245
    }
    
    history = load_mock_history('2026-02-24', num_days=2)
    enriched = enrich_trend_with_lifecycle(trend, history)
    
    assert enriched['lifecycle']['status'] == 'rising', f"Expected 'rising', got {enriched['lifecycle']['status']}"
    assert enriched['lifecycle']['momentum_score'] >= 1.5, f"Expected momentum >= 1.5, got {enriched['lifecycle']['momentum_score']}"
    
    print(f"✅ PASS: Explosive growth detected with momentum {enriched['lifecycle']['momentum_score']}")


def test_fuzzy_matching():
    """Test: Fuzzy title matching works when URLs differ or are missing."""
    print("\n[TEST] Fuzzy title matching...")
    
    # Similar titles, different IDs/URLs but matching keywords
    # We need at least 60% keyword overlap for fuzzy match
    trend = {
        'id': 'trend-20260226-042',
        'title': 'Privacy-first browser PDF tools',  # Keywords: privacy, browser, tools
        'url': None,  # No URL
        'engagement_score': 80
    }
    
    # Create history with matching trend
    history = [
        {
            'date': '2026-02-23',
            'trends': [
                {
                    'id': 'trend-20260223-001',
                    'title': 'Privacy-first PDF tools running entirely in browser',
                    'url': 'https://different-url.com',
                    'engagement_score': 45,
                    'keywords': ['privacy', 'browser', 'tools', 'running', 'entirely'],
                    'sources': ['reddit']
                }
            ]
        }
    ]
    
    enriched = enrich_trend_with_lifecycle(trend, history)
    
    # Should match based on keyword overlap (privacy, browser, tools)
    assert enriched['lifecycle']['appearances'] == 2, f"Expected 2 appearances (fuzzy match), got {enriched['lifecycle']['appearances']}"
    
    print(f"✅ PASS: Fuzzy matched {enriched['lifecycle']['appearances']} appearances")


def test_momentum_score_bounds():
    """Test: Momentum score stays within bounds (0.2 - 2.0)."""
    print("\n[TEST] Momentum score bounds...")
    
    # Test extreme rising case (should cap at 2.0)
    rising_scores = [10, 50, 150, 500]  # 50x growth
    calc = LifecycleCalculator()
    momentum = calc.calculate_momentum('rising', rising_scores)
    assert momentum <= 2.0, f"Rising momentum exceeded max: {momentum}"
    
    # Test extreme declining case (should floor at 0.2)
    peaked_scores = [500, 150, 50, 10]  # 98% decline
    momentum = calc.calculate_momentum('peaked', peaked_scores)
    assert momentum >= 0.2, f"Peaked momentum below min: {momentum}"
    
    print(f"✅ PASS: Momentum bounds enforced (rising: {calc.calculate_momentum('rising', rising_scores)}, peaked: {calc.calculate_momentum('peaked', peaked_scores)})")


def test_scoring_boost():
    """Test: Rising trends score higher than peaked trends with same base score."""
    print("\n[TEST] Rising vs Peaked scoring comparison...")
    
    base_score = 8.5
    
    # Rising trend
    rising = {
        'id': 'trend-001',
        'title': 'Rising tool',
        'url': 'https://example.com/rising',
        'engagement_score': 100
    }
    rising_history = [
        {
            'date': '2026-02-23',
            'trends': [{'id': 'x', 'title': 'Rising tool', 'url': 'https://example.com/rising', 
                       'engagement_score': 40, 'keywords': ['rising', 'tool']}]
        },
        {
            'date': '2026-02-24',
            'trends': [{'id': 'y', 'title': 'Rising tool', 'url': 'https://example.com/rising', 
                       'engagement_score': 70, 'keywords': ['rising', 'tool']}]
        }
    ]
    rising_enriched = enrich_trend_with_lifecycle(rising, rising_history)
    rising_final = base_score * rising_enriched['lifecycle']['momentum_score']
    
    # Peaked trend
    peaked = {
        'id': 'trend-002',
        'title': 'Peaked tool',
        'url': 'https://example.com/peaked',
        'engagement_score': 50
    }
    peaked_history = [
        {
            'date': '2026-02-23',
            'trends': [{'id': 'a', 'title': 'Peaked tool', 'url': 'https://example.com/peaked', 
                       'engagement_score': 120, 'keywords': ['peaked', 'tool']}]
        },
        {
            'date': '2026-02-24',
            'trends': [{'id': 'b', 'title': 'Peaked tool', 'url': 'https://example.com/peaked', 
                       'engagement_score': 85, 'keywords': ['peaked', 'tool']}]
        }
    ]
    peaked_enriched = enrich_trend_with_lifecycle(peaked, peaked_history)
    peaked_final = base_score * peaked_enriched['lifecycle']['momentum_score']
    
    assert rising_final > peaked_final, f"Rising score ({rising_final}) should be > peaked score ({peaked_final})"
    
    print(f"✅ PASS: Rising final score ({rising_final:.2f}) > Peaked final score ({peaked_final:.2f})")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run the complete test suite."""
    print("=" * 70)
    print("Epic 2.3: Trend Lifecycle Tracking - Test Suite")
    print("=" * 70)
    
    tests = [
        test_new_trend,
        test_rising_trend,
        test_peaked_trend,
        test_stable_trend,
        test_explosive_growth,
        test_fuzzy_matching,
        test_momentum_score_bounds,
        test_scoring_boost
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"💥 ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
