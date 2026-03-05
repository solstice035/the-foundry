#!/usr/bin/env python3
"""
Engagement summary utilities for morning briefing integration.

Provides functions to format engagement data for inclusion in
the daily morning briefing.
"""

import json
import os


def load_engagement(date, workspace="~/.openclaw/workspace/foundry"):
    """
    Load engagement data for a specific date.

    Args:
        date: Date string in YYYY-MM-DD format
        workspace: Path to foundry workspace

    Returns:
        Engagement data dict or None if not found
    """
    workspace = os.path.expanduser(workspace)
    engagement_path = os.path.join(workspace, date, "engagement.json")

    if not os.path.exists(engagement_path):
        return None

    try:
        with open(engagement_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def format_engagement_summary(engagement_data):
    """
    Format engagement data for inclusion in morning briefing.

    Args:
        engagement_data: Engagement dict from engagement.json

    Returns:
        Formatted text string for briefing
    """
    if engagement_data is None:
        return "📊 Engagement: No data available (check not yet run)"

    summary = engagement_data.get("summary", {})
    repos = engagement_data.get("repos", [])

    # Overall stats
    total_repos = summary.get("total_repos", 0)
    total_stars = summary.get("total_stars", 0)
    total_forks = summary.get("total_forks", 0)
    total_issues = summary.get("total_issues", 0)

    lines = [
        "📊 GitHub Engagement",
        f"Portfolio: {total_repos} repos, {total_stars} stars, {total_forks} forks, {total_issues} issues",
    ]

    # High engagement repos
    high_engagement = summary.get("high_engagement_repos", [])
    if high_engagement:
        lines.append(f"🔥 High engagement: {', '.join(high_engagement)}")

    # Growth highlights (repos with significant deltas)
    growth_repos = []
    for repo in repos:
        growth = repo.get("growth")
        if growth:
            stars_delta = growth.get("stars_delta", 0)
            if stars_delta >= 5:  # Significant growth
                growth_repos.append(f"{repo['name']} (+{stars_delta} stars)")

    if growth_repos:
        lines.append(f"📈 Growth: {', '.join(growth_repos)}")

    # Action items summary
    action_items = summary.get("action_items", [])
    high_priority = [a for a in action_items if a.get("priority") == "high"]

    if high_priority:
        lines.append(f"⚡ High-priority actions: {len(high_priority)}")
        for item in high_priority[:3]:  # Top 3
            lines.append(f"   • {item['repo']}: {item['action']}")

    # Consensus Analyst triggers
    needs_consensus = summary.get("repos_needing_consensus", [])
    if needs_consensus:
        lines.append(f"🎯 Ready for Consensus Analyst: {', '.join(needs_consensus)}")

    return "\n".join(lines)


def format_engagement_details(engagement_data):
    """
    Format detailed engagement data for standalone report.

    Args:
        engagement_data: Engagement dict from engagement.json

    Returns:
        Formatted detailed text
    """
    if engagement_data is None:
        return "No engagement data available"

    summary = engagement_data.get("summary", {})
    repos = engagement_data.get("repos", [])

    lines = [
        "=" * 60,
        "GITHUB ENGAGEMENT REPORT",
        f"Date: {engagement_data.get('date')}",
        f"Checked at: {engagement_data.get('checked_at')}",
        "=" * 60,
        "",
        "SUMMARY",
        f"Total repos: {summary.get('total_repos', 0)}",
        f"Total stars: {summary.get('total_stars', 0)}",
        f"Total forks: {summary.get('total_forks', 0)}",
        f"Total issues: {summary.get('total_issues', 0)}",
        "",
    ]

    # Repository details
    if repos:
        lines.append("REPOSITORIES")
        for repo in repos:
            stats = repo.get("stats", {})
            growth = repo.get("growth")
            thresholds = repo.get("thresholds", {})

            lines.append(f"\n{repo['name']}")
            lines.append(f"  Age: {repo.get('age_days', 0)} days")
            lines.append(
                f"  Stats: {stats.get('stars', 0)} ⭐ | {stats.get('forks', 0)} 🍴 | {stats.get('issues', 0)} 📝"
            )

            if growth:
                deltas = []
                if growth.get("stars_delta", 0) != 0:
                    deltas.append(f"stars {growth['stars_delta']:+d}")
                if growth.get("forks_delta", 0) != 0:
                    deltas.append(f"forks {growth['forks_delta']:+d}")
                if growth.get("issues_delta", 0) != 0:
                    deltas.append(f"issues {growth['issues_delta']:+d}")

                if deltas:
                    lines.append(f"  Growth: {', '.join(deltas)}")

            # Threshold status
            threshold_marks = []
            if thresholds.get("crossed_25_stars"):
                threshold_marks.append("✅ 25 stars")
            if thresholds.get("crossed_50_stars"):
                threshold_marks.append("✅ 50 stars")
            if thresholds.get("has_external_issues"):
                threshold_marks.append("✅ external issues")
            if thresholds.get("eligible_for_consensus"):
                threshold_marks.append("🎯 CONSENSUS READY")

            if threshold_marks:
                lines.append(f"  Status: {', '.join(threshold_marks)}")

            # Notable issues
            notable = repo.get("notable_issues", [])
            if notable:
                lines.append("  Notable issues:")
                for issue in notable[:3]:
                    lines.append(
                        f"    #{issue['number']}: {issue['title']} (@{issue['author']})"
                    )

        lines.append("")

    # Action items
    action_items = summary.get("action_items", [])
    if action_items:
        lines.append("ACTION ITEMS")
        for item in action_items:
            priority = item.get("priority", "").upper()
            lines.append(f"\n[{priority}] {item['repo']}")
            lines.append(f"  {item['action']}")
            lines.append(f"  Reason: {item['reason']}")

    return "\n".join(lines)


def add_engagement_to_briefing(briefing_text, engagement_data):
    """
    Add engagement summary to an existing briefing.

    Args:
        briefing_text: Existing briefing text
        engagement_data: Engagement dict from engagement.json

    Returns:
        Updated briefing text with engagement section
    """
    engagement_section = format_engagement_summary(engagement_data)

    # Insert engagement section after the header and before the footer
    # Assumes briefing has a "Pipeline:" line near the end
    lines = briefing_text.split("\n")

    # Find the pipeline line
    insert_index = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("Pipeline:"):
            insert_index = i
            break

    # Insert engagement section before pipeline
    lines.insert(insert_index, "")
    lines.insert(insert_index, engagement_section)

    return "\n".join(lines)


if __name__ == "__main__":
    # Test with mock data
    mock_data = {
        "schema_version": 1,
        "date": "2026-02-26",
        "checked_at": "2026-02-26T12:00:00Z",
        "repos": [
            {
                "name": "foundry-20260218-pdf-privacy-tools",
                "age_days": 8,
                "stats": {"stars": 30, "forks": 5, "issues": 2, "external_issues": 1},
                "growth": {"stars_delta": 10, "forks_delta": 2, "issues_delta": 1},
                "thresholds": {
                    "crossed_25_stars": True,
                    "eligible_for_consensus": True,
                    "has_external_issues": False,
                },
            }
        ],
        "summary": {
            "total_repos": 1,
            "total_stars": 30,
            "total_forks": 5,
            "total_issues": 2,
            "high_engagement_repos": ["foundry-20260218-pdf-privacy-tools"],
            "repos_needing_consensus": ["foundry-20260218-pdf-privacy-tools"],
            "action_items": [
                {
                    "repo": "foundry-20260218-pdf-privacy-tools",
                    "action": "Trigger Consensus Analyst review",
                    "priority": "high",
                    "reason": "30 stars, 8 days old",
                }
            ],
        },
    }

    print("SUMMARY FORMAT:")
    print(format_engagement_summary(mock_data))
    print("\n" + "=" * 60 + "\n")
    print("DETAILED FORMAT:")
    print(format_engagement_details(mock_data))
