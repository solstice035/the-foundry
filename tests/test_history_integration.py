"""
Integration tests for history-based deduplication in the pipeline.

Tests cover:
1. history_dedup_trends() end-to-end
2. Graceful handling of missing/corrupt history.json
3. cleanup_history.py script behaviour
4. Round-trip: add build → dedup check → cleanup
"""

import unittest
import json
import tempfile
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from process_trends import history_dedup_trends
from dedup import add_build_to_history, cleanup_history


class TestHistoryDedupTrends(unittest.TestCase):
    """Test the history_dedup_trends integration function."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.history_path = os.path.join(self.tmpdir, 'history.json')
        self.summary_path = os.path.join(self.tmpdir, 'trends-summary.json')

        # Create history with a known build
        history = {
            'schema_version': 1,
            'builds': [
                {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'project_name': 'pdf-privacy-tools',
                    'title': 'Privacy-first PDF merge and split tool',
                    'keywords': ['privacy', 'first', 'pdf', 'merge', 'split', 'tool'],
                    'status': 'success',
                    'source': 'reddit'
                }
            ],
            'rejections': [],
            'dedup_window_days': 30
        }
        with open(self.history_path, 'w') as f:
            json.dump(history, f)

        # Create trends summary with one duplicate and one unique trend
        summary = {
            'schema_version': 1,
            'scan_date': datetime.now().isoformat(),
            'trends': [
                {
                    'id': 'trend-001',
                    'title': 'PDF merge split and privacy tool for browsers',
                    'source': 'hn',
                    'final_score': 75.0
                },
                {
                    'id': 'trend-002',
                    'title': 'Kubernetes cluster monitoring dashboard',
                    'source': 'reddit',
                    'final_score': 60.0
                }
            ]
        }
        with open(self.summary_path, 'w') as f:
            json.dump(summary, f)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_flags_duplicate_trend(self):
        """Duplicate trends should be flagged with previously_built."""
        stats = history_dedup_trends(self.summary_path, self.history_path)

        self.assertEqual(stats['duplicates_flagged'], 1)
        self.assertEqual(stats['total_trends'], 2)

        with open(self.summary_path) as f:
            data = json.load(f)

        # PDF trend should be flagged
        pdf_trend = data['trends'][0]
        self.assertTrue(pdf_trend['previously_built'])
        self.assertIn('duplicate_info', pdf_trend)
        self.assertGreater(pdf_trend['duplicate_info']['similarity'], 0.5)

        # K8s trend should NOT be flagged
        k8s_trend = data['trends'][1]
        self.assertFalse(k8s_trend['previously_built'])

    def test_adds_metadata(self):
        """Should add history_dedup_date and previously_built_flagged."""
        history_dedup_trends(self.summary_path, self.history_path)

        with open(self.summary_path) as f:
            data = json.load(f)

        self.assertIn('history_dedup_date', data)
        self.assertIn('previously_built_flagged', data)
        self.assertEqual(data['previously_built_flagged'], 1)

    def test_missing_history_creates_fresh(self):
        """Missing history.json should be created and no trends flagged."""
        os.remove(self.history_path)

        stats = history_dedup_trends(self.summary_path, self.history_path)

        self.assertTrue(stats['history_initialized'])
        self.assertEqual(stats['duplicates_flagged'], 0)
        self.assertTrue(os.path.exists(self.history_path))

        with open(self.history_path) as f:
            history = json.load(f)
        self.assertEqual(history['schema_version'], 1)
        self.assertEqual(len(history['builds']), 0)

    def test_corrupt_history_creates_fresh(self):
        """Corrupt history.json should be replaced with fresh."""
        with open(self.history_path, 'w') as f:
            f.write('not valid json {{{')

        stats = history_dedup_trends(self.summary_path, self.history_path)

        self.assertTrue(stats['history_initialized'])
        self.assertEqual(stats['duplicates_flagged'], 0)

    def test_empty_trends_list(self):
        """Empty trends list should work without errors."""
        summary = {'schema_version': 1, 'trends': []}
        with open(self.summary_path, 'w') as f:
            json.dump(summary, f)

        stats = history_dedup_trends(self.summary_path, self.history_path)
        self.assertEqual(stats['total_trends'], 0)
        self.assertEqual(stats['duplicates_flagged'], 0)


class TestRoundTrip(unittest.TestCase):
    """Test the full round-trip: add build → dedup → cleanup."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.history_path = os.path.join(self.tmpdir, 'history.json')
        self.summary_path = os.path.join(self.tmpdir, 'trends-summary.json')

        # Start with empty history
        history = {
            'schema_version': 1,
            'builds': [],
            'rejections': [],
            'dedup_window_days': 30
        }
        with open(self.history_path, 'w') as f:
            json.dump(history, f)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_add_then_dedup(self):
        """Build added to history should be detected as duplicate."""
        # Step 1: Add a build
        add_build_to_history(self.history_path, {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'project_name': 'git-commit-ai',
            'title': 'AI-powered git commit message generator',
            'status': 'success',
            'source': 'hn'
        })

        # Step 2: Create trends with similar title
        summary = {
            'schema_version': 1,
            'trends': [{
                'id': 'trend-001',
                'title': 'AI commit message generator for git',
                'source': 'reddit',
                'final_score': 70.0
            }]
        }
        with open(self.summary_path, 'w') as f:
            json.dump(summary, f)

        # Step 3: Run dedup
        stats = history_dedup_trends(self.summary_path, self.history_path)
        self.assertEqual(stats['duplicates_flagged'], 1)

    def test_cleanup_then_dedup(self):
        """After cleanup removes old builds, they shouldn't flag as duplicates."""
        # Add an old build (10 days ago)
        add_build_to_history(self.history_path, {
            'date': (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
            'project_name': 'old-tool',
            'title': 'Old developer tool for testing',
            'status': 'success',
            'source': 'hn'
        })

        # Cleanup with 7-day window
        stats = cleanup_history(self.history_path, archive_days=7)
        self.assertEqual(stats['builds_removed'], 1)

        # Now dedup should not flag similar trend
        summary = {
            'schema_version': 1,
            'trends': [{
                'id': 'trend-001',
                'title': 'Developer tool for testing code',
                'source': 'reddit',
                'final_score': 50.0
            }]
        }
        with open(self.summary_path, 'w') as f:
            json.dump(summary, f)

        dedup_stats = history_dedup_trends(self.summary_path, self.history_path)
        self.assertEqual(dedup_stats['duplicates_flagged'], 0)

    def test_recent_builds_survive_cleanup(self):
        """Builds within 7-day window should survive cleanup."""
        # Add builds at different ages
        for days_ago in [1, 3, 5, 8, 10]:
            add_build_to_history(self.history_path, {
                'date': (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d'),
                'project_name': f'tool-{days_ago}d-ago',
                'title': f'Tool built {days_ago} days ago',
                'status': 'success',
                'source': 'hn'
            })

        stats = cleanup_history(self.history_path, archive_days=7)
        self.assertEqual(stats['builds_removed'], 2)  # 8 and 10 days old

        with open(self.history_path) as f:
            history = json.load(f)
        self.assertEqual(len(history['builds']), 3)  # 1, 3, 5 days old survive


if __name__ == '__main__':
    unittest.main()
