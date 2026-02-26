#!/usr/bin/env python3
"""
Tests for GitHub Engagement Monitoring

Tests the engagement check script with real data from pdf-privacy-tools repo.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scripts.check_engagement import (
    calculate_growth,
    check_thresholds,
    generate_action_items,
    list_repos,
    get_repo_stats,
)


def test_list_repos():
    """Test 1: List repositories with foundry- prefix."""
    print("=" * 60)
    print("TEST 1: List foundry-* repos")
    print("=" * 60)
    
    repos = list_repos("jeevesbot-io", "foundry-")
    
    if repos is None:
        print("❌ FAIL: Failed to fetch repos")
        return False
    
    print(f"Found {len(repos)} public foundry-* repos")
    
    if len(repos) == 0:
        print("⚠️  WARNING: No repos found (this is OK if none exist yet)")
        return True
    
    for repo in repos[:5]:  # Show first 5
        print(f"  • {repo['name']} (created {repo.get('createdAt', 'unknown')})")
    
    print("✅ PASS: Repository listing works")
    return True


def test_get_repo_stats():
    """Test 2: Fetch stats for pdf-privacy-tools."""
    print("\n" + "=" * 60)
    print("TEST 2: Fetch stats for foundry-20260218-pdf-privacy-tools")
    print("=" * 60)
    
    stats = get_repo_stats("jeevesbot-io", "foundry-20260218-pdf-privacy-tools")
    
    if stats is None:
        print("❌ FAIL: Failed to fetch repo stats")
        return False
    
    print(f"Repository: {stats['full_name']}")
    print(f"URL: {stats['url']}")
    print(f"Age: {stats['age_days']} days")
    print(f"\nStats:")
    print(f"  Stars: {stats['stats']['stars']}")
    print(f"  Forks: {stats['stats']['forks']}")
    print(f"  Issues: {stats['stats']['issues']}")
    print(f"  External issues: {stats['stats']['external_issues']}")
    print(f"  Watchers: {stats['stats']['watchers']}")
    
    if stats['notable_issues']:
        print(f"\nNotable issues:")
        for issue in stats['notable_issues']:
            print(f"  #{issue['number']}: {issue['title']} (@{issue['author']})")
    
    # Validate schema
    required_fields = ["name", "full_name", "url", "created_at", "age_days", "stats"]
    for field in required_fields:
        if field not in stats:
            print(f"❌ FAIL: Missing required field: {field}")
            return False
    
    print("\n✅ PASS: Stats fetched and validated")
    return True


def test_threshold_detection():
    """Test 3: Threshold detection logic."""
    print("\n" + "=" * 60)
    print("TEST 3: Threshold detection")
    print("=" * 60)
    
    # Test case 1: Low engagement
    stats1 = {"stars": 5, "external_issues": 0}
    thresholds1 = check_thresholds(stats1, 10)
    
    print("Case 1: 5 stars, 0 external issues, 10 days old")
    print(f"  25 stars threshold: {thresholds1['crossed_25_stars']} (expected False)")
    print(f"  50 stars threshold: {thresholds1['crossed_50_stars']} (expected False)")
    print(f"  External issues: {thresholds1['has_external_issues']} (expected False)")
    print(f"  Consensus eligible: {thresholds1['eligible_for_consensus']} (expected False)")
    
    if any([
        thresholds1['crossed_25_stars'],
        thresholds1['crossed_50_stars'],
        thresholds1['has_external_issues'],
        thresholds1['eligible_for_consensus']
    ]):
        print("❌ FAIL: Low engagement case triggered thresholds")
        return False
    
    # Test case 2: Exactly at 25 stars, 3 days old
    stats2 = {"stars": 25, "external_issues": 1}
    thresholds2 = check_thresholds(stats2, 3)
    
    print("\nCase 2: 25 stars, 1 external issue, 3 days old")
    print(f"  25 stars threshold: {thresholds2['crossed_25_stars']} (expected True)")
    print(f"  50 stars threshold: {thresholds2['crossed_50_stars']} (expected False)")
    print(f"  External issues: {thresholds2['has_external_issues']} (expected False)")
    print(f"  Consensus eligible: {thresholds2['eligible_for_consensus']} (expected True)")
    
    if not thresholds2['crossed_25_stars']:
        print("❌ FAIL: 25 stars threshold not triggered")
        return False
    if not thresholds2['eligible_for_consensus']:
        print("❌ FAIL: Consensus threshold not triggered")
        return False
    
    # Test case 3: High engagement
    stats3 = {"stars": 60, "external_issues": 3}
    thresholds3 = check_thresholds(stats3, 5)
    
    print("\nCase 3: 60 stars, 3 external issues, 5 days old")
    print(f"  25 stars threshold: {thresholds3['crossed_25_stars']} (expected True)")
    print(f"  50 stars threshold: {thresholds3['crossed_50_stars']} (expected True)")
    print(f"  External issues: {thresholds3['has_external_issues']} (expected True)")
    print(f"  Consensus eligible: {thresholds3['eligible_for_consensus']} (expected True)")
    
    if not all([
        thresholds3['crossed_25_stars'],
        thresholds3['crossed_50_stars'],
        thresholds3['has_external_issues'],
        thresholds3['eligible_for_consensus']
    ]):
        print("❌ FAIL: High engagement case didn't trigger all thresholds")
        return False
    
    # Test case 4: Too young for consensus
    stats4 = {"stars": 30, "external_issues": 0}
    thresholds4 = check_thresholds(stats4, 2)
    
    print("\nCase 4: 30 stars, 0 external issues, 2 days old")
    print(f"  25 stars threshold: {thresholds4['crossed_25_stars']} (expected True)")
    print(f"  Consensus eligible: {thresholds4['eligible_for_consensus']} (expected False)")
    
    if thresholds4['eligible_for_consensus']:
        print("❌ FAIL: Consensus triggered for repo younger than 3 days")
        return False
    
    print("\n✅ PASS: All threshold cases validated")
    return True


def test_growth_calculation():
    """Test 4: Growth calculation vs previous day."""
    print("\n" + "=" * 60)
    print("TEST 4: Growth calculation")
    print("=" * 60)
    
    # Mock previous data
    previous_data = {
        "repos": [
            {
                "name": "foundry-20260218-pdf-privacy-tools",
                "stats": {
                    "stars": 10,
                    "forks": 2,
                    "issues": 1
                }
            }
        ]
    }
    
    # Current stats
    current_stats = {
        "stars": 15,
        "forks": 3,
        "issues": 2
    }
    
    growth = calculate_growth(current_stats, previous_data, "foundry-20260218-pdf-privacy-tools")
    
    if growth is None:
        print("❌ FAIL: Growth calculation returned None")
        return False
    
    print(f"Current stats: {current_stats}")
    print(f"Previous stats: {previous_data['repos'][0]['stats']}")
    print(f"\nGrowth:")
    print(f"  Stars: +{growth['stars_delta']} (expected +5)")
    print(f"  Forks: +{growth['forks_delta']} (expected +1)")
    print(f"  Issues: +{growth['issues_delta']} (expected +1)")
    
    if growth['stars_delta'] != 5:
        print("❌ FAIL: Stars delta incorrect")
        return False
    if growth['forks_delta'] != 1:
        print("❌ FAIL: Forks delta incorrect")
        return False
    if growth['issues_delta'] != 1:
        print("❌ FAIL: Issues delta incorrect")
        return False
    
    # Test with no previous data
    growth_none = calculate_growth(current_stats, None, "foundry-20260218-pdf-privacy-tools")
    if growth_none is not None:
        print("❌ FAIL: Growth with no previous data should return None")
        return False
    
    print("\n✅ PASS: Growth calculation validated")
    return True


def test_action_items():
    """Test 5: Action item generation."""
    print("\n" + "=" * 60)
    print("TEST 5: Action item generation")
    print("=" * 60)
    
    repos = [
        {
            "name": "high-engagement-repo",
            "age_days": 5,
            "stats": {"stars": 30, "external_issues": 3},
            "thresholds": {
                "crossed_25_stars": True,
                "eligible_for_consensus": True,
                "has_external_issues": True
            },
            "growth": {"stars_delta": 15}
        },
        {
            "name": "medium-engagement-repo",
            "age_days": 2,
            "stats": {"stars": 20, "external_issues": 0},
            "thresholds": {
                "crossed_25_stars": False,
                "eligible_for_consensus": False,
                "has_external_issues": False
            },
            "growth": {"stars_delta": 3}
        },
        {
            "name": "low-engagement-repo",
            "age_days": 1,
            "stats": {"stars": 5, "external_issues": 0},
            "thresholds": {
                "crossed_25_stars": False,
                "eligible_for_consensus": False,
                "has_external_issues": False
            },
            "growth": None
        }
    ]
    
    action_items = generate_action_items(repos)
    
    print(f"Generated {len(action_items)} action items:")
    for item in action_items:
        print(f"\n  [{item['priority'].upper()}] {item['repo']}")
        print(f"  Action: {item['action']}")
        print(f"  Reason: {item['reason']}")
    
    # Validate action items
    high_priority = [a for a in action_items if a['priority'] == 'high']
    medium_priority = [a for a in action_items if a['priority'] == 'medium']
    
    print(f"\nPriority breakdown:")
    print(f"  High: {len(high_priority)}")
    print(f"  Medium: {len(medium_priority)}")
    print(f"  Low: {len([a for a in action_items if a['priority'] == 'low'])}")
    
    if len(high_priority) == 0:
        print("❌ FAIL: No high-priority action items for high-engagement repo")
        return False
    
    consensus_actions = [a for a in action_items if "Consensus Analyst" in a['action']]
    if len(consensus_actions) == 0:
        print("❌ FAIL: No Consensus Analyst trigger action item")
        return False
    
    print("\n✅ PASS: Action items generated correctly")
    return True


def test_full_integration():
    """Test 6: Full integration test with real repo."""
    print("\n" + "=" * 60)
    print("TEST 6: Full integration test")
    print("=" * 60)
    
    # Run the actual script
    result = subprocess.run(
        ["python3", "src/scripts/check_engagement.py", "--date", "2026-02-26"],
        cwd=os.path.expanduser("~/projects/the-foundry"),
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        print(f"❌ FAIL: Script exited with code {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        return False
    
    print("Script output:")
    print(result.stdout)
    
    # Check that output file was created
    output_path = os.path.expanduser("~/.openclaw/workspace/foundry/2026-02-26/engagement.json")
    
    # If no repos found, it's OK - the script exits gracefully
    if "No repos found" in result.stdout:
        print("\n⚠️  No public repos found - this is OK for testing")
        print("   When public repos exist, they will be tracked")
        print("\n✅ PASS: Script handles no-repos case correctly")
        return True
    
    if not os.path.exists(output_path):
        print(f"❌ FAIL: Output file not created at {output_path}")
        return False
    
    # Validate output schema
    with open(output_path) as f:
        data = json.load(f)
    
    required_fields = ["schema_version", "date", "checked_at", "repos", "summary"]
    for field in required_fields:
        if field not in data:
            print(f"❌ FAIL: Missing required field in output: {field}")
            return False
    
    if data["schema_version"] != 1:
        print(f"❌ FAIL: Wrong schema version: {data['schema_version']}")
        return False
    
    print(f"\n✅ Output file created and validated")
    print(f"   Path: {output_path}")
    print(f"   Repos checked: {data['summary']['total_repos']}")
    print(f"   Total stars: {data['summary']['total_stars']}")
    
    print("\n✅ PASS: Full integration test completed")
    return True


def main():
    """Run all tests."""
    results = []
    
    results.append(("List repos", test_list_repos()))
    results.append(("Get repo stats", test_get_repo_stats()))
    results.append(("Threshold detection", test_threshold_detection()))
    results.append(("Growth calculation", test_growth_calculation()))
    results.append(("Action items", test_action_items()))
    results.append(("Full integration", test_full_integration()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
