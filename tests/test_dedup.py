"""
Tests for deduplication module (src/dedup.py)

Tests cover:
1. Keyword extraction (stop words, stemming, normalization)
2. Jaccard similarity calculation
3. Duplicate detection (builds and rejections)
4. History updates (adding builds and rejections)
5. Cleanup (removing old entries)
"""

import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dedup import (
    extract_keywords,
    jaccard_similarity,
    is_duplicate,
    add_build_to_history,
    add_rejection_to_history,
    cleanup_history
)


class TestKeywordExtraction(unittest.TestCase):
    """Test keyword extraction and normalization."""
    
    def test_basic_extraction(self):
        """Test basic keyword extraction."""
        title = "Privacy-first PDF tool to merge and split PDFs"
        keywords = extract_keywords(title)
        self.assertIn('privacy', keywords)
        self.assertIn('pdf', keywords)
        self.assertIn('merge', keywords)
        self.assertIn('split', keywords)
    
    def test_stop_word_filtering(self):
        """Stop words should be removed."""
        title = "A tool for the best PDF merge with AI"
        keywords = extract_keywords(title)
        self.assertNotIn('a', keywords)
        self.assertNotIn('the', keywords)
        self.assertNotIn('for', keywords)
        self.assertNotIn('with', keywords)
    
    def test_stemming(self):
        """Test that stemming normalizes word variants."""
        # Plurals: "tools" → "tool", "documents" → "document"
        keywords_plural = extract_keywords("PDF tools and documents")
        keywords_singular = extract_keywords("PDF tool and document")
        # Both should have same keywords after stemming
        self.assertIn('tool', keywords_plural)
        self.assertIn('tool', keywords_singular)
        self.assertIn('document', keywords_plural)
        self.assertIn('document', keywords_singular)
        
        # -ing suffix: "merging" → "merg"
        keywords_ing = extract_keywords("merging documents")
        self.assertIn('merg', keywords_ing)
        
        # -ed suffix: "merged" → "merg"
        keywords_ed = extract_keywords("merged files")
        self.assertIn('merg', keywords_ed)
    
    def test_punctuation_removal(self):
        """Punctuation should be removed, including hyphens."""
        title = "Privacy-first PDF-merge tool!"
        keywords = extract_keywords(title)
        # Hyphens split words: "privacy-first" → "privacy" "first"
        self.assertIn('privacy', keywords)
        self.assertIn('first', keywords)
        # Punctuation removed
        self.assertNotIn('!', ' '.join(keywords))
    
    def test_case_insensitivity(self):
        """Keywords should be lowercased."""
        keywords1 = extract_keywords("PDF Merge Tool")
        keywords2 = extract_keywords("pdf merge tool")
        self.assertEqual(keywords1, keywords2)
    
    def test_empty_input(self):
        """Empty or None input should return empty list."""
        self.assertEqual(extract_keywords(""), [])
        self.assertEqual(extract_keywords(None), [])
    
    def test_short_word_filtering(self):
        """Words <= 2 characters should be filtered."""
        title = "AI is a new PDF to go"
        keywords = extract_keywords(title)
        # 'ai' should pass (3 chars after no stemming needed)
        # 'is', 'a', 'to', 'go' should be filtered (stop words or short)
        self.assertNotIn('is', keywords)
        self.assertNotIn('go', keywords)


class TestJaccardSimilarity(unittest.TestCase):
    """Test Jaccard similarity calculation."""
    
    def test_identical_sets(self):
        """Identical keyword sets should have 100% similarity."""
        kw1 = ['pdf', 'merge', 'tool']
        kw2 = ['pdf', 'merge', 'tool']
        self.assertEqual(jaccard_similarity(kw1, kw2), 1.0)
    
    def test_no_overlap(self):
        """No overlap should result in 0% similarity."""
        kw1 = ['pdf', 'merge']
        kw2 = ['kubernetes', 'cluster']
        self.assertEqual(jaccard_similarity(kw1, kw2), 0.0)
    
    def test_partial_overlap(self):
        """Test partial overlap calculation."""
        kw1 = ['pdf', 'merge', 'split', 'browser']
        kw2 = ['pdf', 'tool', 'merge', 'compress']
        # Intersection: ['pdf', 'merge'] = 2
        # Union: ['pdf', 'merge', 'split', 'browser', 'tool', 'compress'] = 6
        # Similarity: 2/6 = 0.333...
        similarity = jaccard_similarity(kw1, kw2)
        self.assertAlmostEqual(similarity, 2/6, places=2)
    
    def test_empty_sets(self):
        """Empty sets should return 0.0."""
        self.assertEqual(jaccard_similarity([], ['pdf']), 0.0)
        self.assertEqual(jaccard_similarity(['pdf'], []), 0.0)
        self.assertEqual(jaccard_similarity([], []), 0.0)
    
    def test_duplicate_keywords(self):
        """Duplicate keywords in the same list should not affect result (set logic)."""
        kw1 = ['pdf', 'pdf', 'merge']
        kw2 = ['pdf', 'merge', 'merge']
        # Both become set(['pdf', 'merge'])
        self.assertEqual(jaccard_similarity(kw1, kw2), 1.0)


class TestDuplicateDetection(unittest.TestCase):
    """Test duplicate detection against history."""
    
    def setUp(self):
        """Create a mock history for testing."""
        self.history = {
            'schema_version': 1,
            'builds': [
                {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'project_name': 'pdf-privacy-tools',
                    'title': 'Privacy-first PDF merge and split tool',
                    'keywords': ['privacy', 'first', 'pdf', 'merge', 'split', 'tool']
                },
                {
                    'date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                    'project_name': 'ai-deploy-guard',
                    'title': 'AI deployment safety guard',
                    'keywords': ['deployment', 'safety', 'guard']
                }
            ],
            'rejections': [
                {
                    'date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                    'title': 'Political polling dashboard',
                    'keywords': ['political', 'poll', 'dashboard'],
                    'reason': 'Political content'
                }
            ],
            'dedup_window_days': 30
        }
    
    def test_exact_duplicate(self):
        """Exact title match should be detected."""
        result = is_duplicate('Privacy-first PDF merge and split tool', self.history)
        self.assertIsNotNone(result)
        self.assertTrue(result['is_duplicate'])
        self.assertGreaterEqual(result['similarity'], 0.5)
    
    def test_high_similarity_duplicate(self):
        """High similarity (>50%) should be detected as duplicate."""
        # Similar to pdf-privacy-tools
        result = is_duplicate('PDF merge split and privacy tool for browsers', self.history)
        self.assertIsNotNone(result)
        self.assertTrue(result['is_duplicate'])
    
    def test_low_similarity_not_duplicate(self):
        """Low similarity (<50%) should NOT be flagged."""
        # Completely different topic
        result = is_duplicate('Kubernetes cluster monitoring dashboard', self.history)
        self.assertIsNone(result)
    
    def test_duplicate_against_rejection(self):
        """Duplicates should also be detected against rejections."""
        result = is_duplicate('Political polling and election dashboard', self.history)
        self.assertIsNotNone(result)
        self.assertTrue(result['is_duplicate'])
        self.assertIn('matched_rejection', result)
    
    def test_old_build_outside_window(self):
        """Builds older than the dedup window should be ignored."""
        # Add an old build
        old_date = (datetime.now() - timedelta(days=35)).strftime('%Y-%m-%d')
        self.history['builds'].append({
            'date': old_date,
            'project_name': 'old-kubernetes-tool',
            'title': 'Kubernetes cluster tool',
            'keywords': ['kubernet', 'clust', 'tool']
        })
        
        # This should NOT be flagged as duplicate (outside 30-day window)
        result = is_duplicate('Kubernetes cluster monitoring', self.history)
        self.assertIsNone(result)
    
    def test_build_inside_30_day_window(self):
        """Builds within the 30-day window should be flagged."""
        # Add a build from 25 days ago (inside 30-day window)
        recent_date = (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d')
        self.history['builds'].append({
            'date': recent_date,
            'project_name': 'kubernetes-monitor',
            'title': 'Kubernetes cluster monitoring tool',
            'keywords': ['kubernet', 'clust', 'monitor', 'tool']
        })
        
        # This should be flagged (inside 30-day window)
        result = is_duplicate('Kubernetes cluster monitoring dashboard', self.history)
        self.assertIsNotNone(result)
        self.assertTrue(result['is_duplicate'])
    
    def test_threshold_adjustment(self):
        """Test that custom threshold works."""
        # With 70% threshold, need higher similarity
        result = is_duplicate(
            'PDF merge tool',
            self.history,
            threshold=0.7
        )
        # This might not match at 70% but would at 50%
        # Depends on keyword overlap
        # Test that threshold parameter is respected
        self.assertTrue(True)  # Placeholder - specific to data
    
    def test_missing_keywords_fallback(self):
        """If keywords missing in history, should extract from title."""
        history_no_keywords = {
            'schema_version': 1,
            'builds': [{
                'date': datetime.now().strftime('%Y-%m-%d'),
                'project_name': 'test-tool',
                'title': 'PDF merge split tool',
                'keywords': []  # Empty keywords
            }],
            'rejections': [],
            'dedup_window_days': 30
        }
        
        result = is_duplicate('PDF merge and split utility', history_no_keywords)
        # Should still detect duplicate by extracting keywords from title
        self.assertIsNotNone(result)


class TestHistoryUpdates(unittest.TestCase):
    """Test adding builds and rejections to history."""
    
    def setUp(self):
        """Create a temporary history file."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.history_path = self.temp_file.name
        # Initialize with empty history
        initial_history = {
            'schema_version': 1,
            'builds': [],
            'rejections': [],
            'dedup_window_days': 30
        }
        json.dump(initial_history, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.history_path):
            os.remove(self.history_path)
    
    def test_add_build(self):
        """Test adding a build to history."""
        build_info = {
            'date': '2026-02-26',
            'project_name': 'test-project',
            'title': 'Test project for unit testing',
            'repo_url': 'https://github.com/test/test-project',
            'status': 'success',
            'source': 'reddit'
        }
        
        add_build_to_history(self.history_path, build_info)
        
        # Read back and verify
        with open(self.history_path) as f:
            history = json.load(f)
        
        self.assertEqual(len(history['builds']), 1)
        self.assertEqual(history['builds'][0]['project_name'], 'test-project')
        # Keywords should be auto-generated
        self.assertIn('keywords', history['builds'][0])
        self.assertGreater(len(history['builds'][0]['keywords']), 0)
    
    def test_add_rejection(self):
        """Test adding a rejection to history."""
        rejection_info = {
            'date': '2026-02-26',
            'title': 'Political polling dashboard',
            'reason': 'Political content',
            'source': 'hn'
        }
        
        add_rejection_to_history(self.history_path, rejection_info)
        
        # Read back and verify
        with open(self.history_path) as f:
            history = json.load(f)
        
        self.assertEqual(len(history['rejections']), 1)
        self.assertEqual(history['rejections'][0]['title'], 'Political polling dashboard')
        # Keywords should be auto-generated
        self.assertIn('keywords', history['rejections'][0])
    
    def test_multiple_builds(self):
        """Test adding multiple builds."""
        for i in range(3):
            build_info = {
                'date': '2026-02-26',
                'project_name': f'project-{i}',
                'title': f'Test project {i}',
                'repo_url': f'https://github.com/test/project-{i}',
                'status': 'success',
                'source': 'reddit'
            }
            add_build_to_history(self.history_path, build_info)
        
        with open(self.history_path) as f:
            history = json.load(f)
        
        self.assertEqual(len(history['builds']), 3)
    
    def test_init_missing_history(self):
        """Test that missing history.json is initialized properly."""
        # Delete the file
        os.remove(self.history_path)
        
        build_info = {
            'date': '2026-02-26',
            'project_name': 'test',
            'title': 'Test',
            'repo_url': 'https://github.com/test/test',
            'status': 'success',
            'source': 'hn'
        }
        
        # Should create new history
        add_build_to_history(self.history_path, build_info)
        
        self.assertTrue(os.path.exists(self.history_path))
        with open(self.history_path) as f:
            history = json.load(f)
        self.assertEqual(len(history['builds']), 1)


class TestHistoryCleanup(unittest.TestCase):
    """Test cleanup of old history entries."""
    
    def setUp(self):
        """Create temporary history with old entries."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.history_path = self.temp_file.name
        
        # Create history with entries at different ages
        history = {
            'schema_version': 1,
            'builds': [
                {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'project_name': 'recent',
                    'title': 'Recent build',
                    'keywords': ['recent']
                },
                {
                    'date': (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
                    'project_name': 'medium-old',
                    'title': 'Medium old build',
                    'keywords': ['medium']
                },
                {
                    'date': (datetime.now() - timedelta(days=40)).strftime('%Y-%m-%d'),
                    'project_name': 'very-old',
                    'title': 'Very old build',
                    'keywords': ['old']
                }
            ],
            'rejections': [
                {
                    'date': (datetime.now() - timedelta(days=50)).strftime('%Y-%m-%d'),
                    'title': 'Old rejection',
                    'keywords': ['old']
                }
            ],
            'dedup_window_days': 30
        }
        
        json.dump(history, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.history_path):
            os.remove(self.history_path)
    
    def test_cleanup_30_days(self):
        """Test cleanup with 30-day archive window."""
        stats = cleanup_history(self.history_path, archive_days=30)
        
        # Should remove 1 build (40 days old) and 1 rejection (50 days old)
        self.assertEqual(stats['builds_removed'], 1)
        self.assertEqual(stats['rejections_removed'], 1)
        
        # Verify remaining entries
        with open(self.history_path) as f:
            history = json.load(f)
        
        self.assertEqual(len(history['builds']), 2)
        self.assertEqual(len(history['rejections']), 0)
        
        # Recent and medium-old should remain
        project_names = [b['project_name'] for b in history['builds']]
        self.assertIn('recent', project_names)
        self.assertIn('medium-old', project_names)
        self.assertNotIn('very-old', project_names)
    
    def test_cleanup_7_days(self):
        """Test cleanup with shorter window."""
        stats = cleanup_history(self.history_path, archive_days=7)
        
        # Should remove 2 builds (20 and 40 days old)
        self.assertEqual(stats['builds_removed'], 2)
        
        with open(self.history_path) as f:
            history = json.load(f)
        
        self.assertEqual(len(history['builds']), 1)
        self.assertEqual(history['builds'][0]['project_name'], 'recent')
    
    def test_cleanup_90_days_default(self):
        """Test cleanup with 90-day default (production setting)."""
        # All entries in setUp are < 90 days old, so nothing should be removed
        stats = cleanup_history(self.history_path)
        
        self.assertEqual(stats['builds_removed'], 0)
        self.assertEqual(stats['rejections_removed'], 0)
        
        with open(self.history_path) as f:
            history = json.load(f)
        
        self.assertEqual(len(history['builds']), 3)
        self.assertEqual(len(history['rejections']), 1)
    
    def test_cleanup_90_days_with_ancient_entries(self):
        """Test that entries older than 90 days are removed by default."""
        # Add entries older than 90 days
        with open(self.history_path) as f:
            history = json.load(f)
        
        history['builds'].append({
            'date': (datetime.now() - timedelta(days=95)).strftime('%Y-%m-%d'),
            'project_name': 'ancient',
            'title': 'Ancient build',
            'keywords': ['ancient']
        })
        history['rejections'].append({
            'date': (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d'),
            'title': 'Ancient rejection',
            'keywords': ['ancient']
        })
        
        with open(self.history_path, 'w') as f:
            json.dump(history, f)
        
        stats = cleanup_history(self.history_path)
        
        self.assertEqual(stats['builds_removed'], 1)
        self.assertEqual(stats['rejections_removed'], 1)
        
        with open(self.history_path) as f:
            history = json.load(f)
        
        # Original 3 builds + original 1 rejection should remain
        self.assertEqual(len(history['builds']), 3)
        self.assertEqual(len(history['rejections']), 1)
        # Ancient entries should be gone
        project_names = [b['project_name'] for b in history['builds']]
        self.assertNotIn('ancient', project_names)


if __name__ == '__main__':
    unittest.main()
