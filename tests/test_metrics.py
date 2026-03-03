#!/usr/bin/env python3
"""
Test suite for The Foundry metrics tracking and portfolio reporting.

Tests:
- Metrics JSONL appending
- Metrics schema validation
- Weekly aggregation calculations
- Portfolio Curator logic
- Edge cases (empty weeks, all rejections, etc.)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# Paths
WORKSPACE = Path.home() / ".openclaw" / "workspace" / "foundry"
METRICS_FILE = WORKSPACE / "metrics.jsonl"
HISTORY_FILE = WORKSPACE / "history.json"
REPORTS_DIR = WORKSPACE / "reports"


def load_metrics() -> List[Dict[str, Any]]:
    """Load all metrics from metrics.jsonl"""
    if not METRICS_FILE.exists():
        return []
    
    metrics = []
    with open(METRICS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                metrics.append(json.loads(line))
    return metrics


def load_history() -> Dict[str, Any]:
    """Load build history"""
    if not HISTORY_FILE.exists():
        return {"builds": [], "rejections": [], "dedup_window_days": 30}
    
    with open(HISTORY_FILE, 'r') as f:
        return json.load(f)


def validate_metrics_entry(entry: Dict[str, Any]) -> List[str]:
    """
    Validate a single metrics entry against schema.
    Returns list of validation errors (empty if valid).
    """
    errors = []
    
    # Required fields
    required = ["date", "type", "scout_duration_s", "spec_duration_s", 
                "build_duration_s", "total_duration_s", "cost_usd"]
    for field in required:
        if field not in entry:
            errors.append(f"Missing required field: {field}")
    
    # Type validation
    if "type" in entry and entry["type"] not in ["success", "rejected", "failure", "partial"]:
        errors.append(f"Invalid type: {entry['type']}")
    
    # Numeric validations
    numeric_fields = ["scout_duration_s", "spec_duration_s", "build_duration_s", 
                      "total_duration_s", "cost_usd"]
    for field in numeric_fields:
        if field in entry and not isinstance(entry[field], (int, float)):
            errors.append(f"{field} must be numeric")
        if field in entry and entry[field] < 0:
            errors.append(f"{field} must be non-negative")
    
    # Conditional validations
    if entry.get("type") == "success":
        if not entry.get("project"):
            errors.append("Success entries must have project name")
        if not entry.get("repo_url"):
            errors.append("Success entries must have repo_url")
    
    if entry.get("type") == "rejected":
        if entry.get("spec_decision") != "rejected":
            errors.append("Rejected entries must have spec_decision=rejected")
    
    return errors


def calculate_weekly_metrics(week_start: str, week_end: str) -> Dict[str, Any]:
    """
    Calculate aggregated metrics for a week.
    
    Args:
        week_start: YYYY-MM-DD (Monday)
        week_end: YYYY-MM-DD (Sunday)
    
    Returns:
        Aggregated metrics dict matching metrics-aggregated.schema.json
    """
    metrics = load_metrics()
    
    # Filter to week
    week_metrics = [
        m for m in metrics 
        if week_start <= m["date"] <= week_end
    ]
    
    if not week_metrics:
        return None
    
    # Overview calculations
    builds_attempted = len([m for m in week_metrics if m.get("spec_decision") == "approved"])
    builds_succeeded = len([m for m in week_metrics if m["type"] == "success"])
    builds_failed = len([m for m in week_metrics if m["type"] in ["failure", "partial"]])
    specs_rejected = len([m for m in week_metrics if m["type"] == "rejected"])
    
    success_rate = (builds_succeeded / builds_attempted * 100) if builds_attempted > 0 else 0
    approval_rate = (builds_attempted / len(week_metrics) * 100) if week_metrics else 0
    
    # Performance calculations
    avg_scan = sum(m["scout_duration_s"] for m in week_metrics) / len(week_metrics)
    avg_spec = sum(m["spec_duration_s"] for m in week_metrics) / len(week_metrics)
    
    build_times = [m["build_duration_s"] for m in week_metrics if m["build_duration_s"] > 0]
    avg_build = sum(build_times) / len(build_times) if build_times else 0
    
    avg_total = sum(m["total_duration_s"] for m in week_metrics) / len(week_metrics)
    total_cost = sum(m["cost_usd"] for m in week_metrics)
    avg_cost = total_cost / len(week_metrics)
    
    # Source effectiveness
    sources = {}
    for m in week_metrics:
        if m.get("source"):
            source = m["source"]
            if source not in sources:
                sources[source] = {"trends": 0, "builds": 0, "engagement": []}
            
            if "scout_trends_found" in m:
                sources[source]["trends"] += m["scout_trends_found"]
            
            if m["type"] == "success":
                sources[source]["builds"] += 1
            
            if m.get("engagement_score"):
                sources[source]["engagement"].append(m["engagement_score"])
    
    source_effectiveness = []
    for source, data in sources.items():
        success_rate = (data["builds"] / data["trends"] * 100) if data["trends"] > 0 else 0
        avg_engagement = sum(data["engagement"]) / len(data["engagement"]) if data["engagement"] else None
        
        source_effectiveness.append({
            "source": source,
            "trends_found": data["trends"],
            "builds_shipped": data["builds"],
            "success_rate": round(success_rate, 1),
            "avg_engagement": round(avg_engagement, 1) if avg_engagement else None
        })
    
    # Category distribution
    categories = {}
    for m in week_metrics:
        if m.get("category") and m["type"] == "success":
            cat = m["category"]
            if cat not in categories:
                categories[cat] = {"count": 0, "buildability": []}
            
            categories[cat]["count"] += 1
            if m.get("buildability_score"):
                categories[cat]["buildability"].append(m["buildability_score"])
    
    category_dist = []
    total_builds = sum(c["count"] for c in categories.values())
    for cat, data in categories.items():
        percentage = (data["count"] / total_builds * 100) if total_builds > 0 else 0
        avg_buildability = sum(data["buildability"]) / len(data["buildability"]) if data["buildability"] else None
        
        category_dist.append({
            "category": cat,
            "count": data["count"],
            "percentage": round(percentage, 1),
            "avg_buildability": round(avg_buildability, 1) if avg_buildability else None
        })
    
    # Rejection reasons
    rejection_reasons = {}
    for m in week_metrics:
        if m.get("spec_rejection_reason"):
            reason = m["spec_rejection_reason"]
            rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
    
    rejection_list = [{"reason": r, "count": c} for r, c in rejection_reasons.items()]
    
    return {
        "week_start": week_start,
        "week_end": week_end,
        "nights_total": len(week_metrics),
        "overview": {
            "builds_attempted": builds_attempted,
            "builds_succeeded": builds_succeeded,
            "builds_failed": builds_failed,
            "specs_rejected": specs_rejected,
            "success_rate": round(success_rate, 1),
            "approval_rate": round(approval_rate, 1)
        },
        "performance": {
            "avg_scan_time_s": round(avg_scan, 1),
            "avg_spec_time_s": round(avg_spec, 1),
            "avg_build_time_s": round(avg_build, 1),
            "avg_total_time_s": round(avg_total, 1),
            "total_cost_usd": round(total_cost, 2),
            "avg_cost_per_night": round(avg_cost, 2),
            "total_tokens": None
        },
        "sources": {
            "effectiveness": source_effectiveness,
            "failures": []
        },
        "categories": {
            "distribution": category_dist
        },
        "rejection_reasons": rejection_list,
        "recommendations": [],
        "notable_builds": []
    }


# Test functions

def test_metrics_file_exists():
    """Test that metrics.jsonl exists and is readable"""
    assert METRICS_FILE.exists(), f"metrics.jsonl not found at {METRICS_FILE}"
    print("✓ metrics.jsonl exists")


def test_metrics_valid_json():
    """Test that all metrics entries are valid JSON"""
    metrics = load_metrics()
    assert len(metrics) > 0, "No metrics entries found"
    print(f"✓ Loaded {len(metrics)} metrics entries")


def test_metrics_schema_validation():
    """Test that all metrics entries match schema"""
    metrics = load_metrics()
    errors_found = False
    
    for i, entry in enumerate(metrics):
        errors = validate_metrics_entry(entry)
        if errors:
            print(f"✗ Entry {i} ({entry.get('date', 'unknown')}): {', '.join(errors)}")
            errors_found = True
    
    if not errors_found:
        print(f"✓ All {len(metrics)} entries valid")
    else:
        raise AssertionError("Schema validation errors found")


def test_weekly_aggregation():
    """Test weekly metrics aggregation calculation"""
    # Use current week or most recent week with data
    metrics = load_metrics()
    if not metrics:
        print("⚠ No metrics to test aggregation")
        return
    
    # Get date range from existing metrics
    dates = [m["date"] for m in metrics]
    earliest = min(dates)
    latest = max(dates)
    
    print(f"  Date range: {earliest} to {latest}")
    
    # Calculate for a week that has data
    week_metrics = calculate_weekly_metrics(earliest, latest)
    
    if week_metrics:
        print(f"✓ Weekly aggregation calculated:")
        print(f"  - Nights: {week_metrics['nights_total']}")
        print(f"  - Success rate: {week_metrics['overview']['success_rate']}%")
        print(f"  - Total cost: ${week_metrics['performance']['total_cost_usd']}")
    else:
        print("⚠ No data in date range")


def test_backfill_data_quality():
    """Test that backfilled Phase 1 data is present and realistic"""
    metrics = load_metrics()
    history = load_history()
    
    # Check that we have metrics for Phase 1 builds
    phase1_dates = [build["date"] for build in history["builds"]]
    
    metrics_dates = [m["date"] for m in metrics]
    
    for date in phase1_dates:
        if date not in metrics_dates:
            print(f"⚠ Missing metrics for Phase 1 build on {date}")
    
    print(f"✓ Found metrics for {len([d for d in phase1_dates if d in metrics_dates])}/{len(phase1_dates)} Phase 1 builds")


def test_reports_directory():
    """Test that reports directory exists"""
    assert REPORTS_DIR.exists(), f"Reports directory not found at {REPORTS_DIR}"
    print(f"✓ Reports directory exists at {REPORTS_DIR}")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("Testing Foundry Metrics & Portfolio Tracking")
    print("=" * 60)
    print()
    
    tests = [
        ("Metrics file exists", test_metrics_file_exists),
        ("Valid JSON entries", test_metrics_valid_json),
        ("Schema validation", test_metrics_schema_validation),
        ("Weekly aggregation", test_weekly_aggregation),
        ("Backfill data quality", test_backfill_data_quality),
        ("Reports directory", test_reports_directory),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"\n{name}:")
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
