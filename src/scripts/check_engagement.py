#!/usr/bin/env python3
"""
GitHub Engagement Monitoring for The Foundry

Checks engagement metrics (stars, forks, issues) for all foundry-* repos
in the jeevesbot-io organization. Compares to previous day's data and
triggers Consensus Analyst for high-engagement repos.

Usage:
    python3 check_engagement.py [--date YYYY-MM-DD] [--org OWNER] [--prefix PREFIX]

Output:
    ~/.openclaw/workspace/foundry/YYYY-MM-DD/engagement.json

Cron schedule: Daily at 12:00
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_ORG = "jeevesbot-io"
DEFAULT_PREFIX = "foundry-"
WORKSPACE = os.path.expanduser("~/.openclaw/workspace/foundry")


def run_gh_command(args):
    """Run gh CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: gh command failed: {e.stderr}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print("ERROR: gh command timed out", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON: {e}", file=sys.stderr)
        return None


def list_repos(org, prefix):
    """List all repositories matching the prefix in the organization."""
    # Use gh repo list with JSON output
    repos = run_gh_command(
        [
            "repo",
            "list",
            org,
            "--json",
            "name,url,createdAt,isPrivate",
            "--limit",
            "1000",
        ]
    )

    if repos is None:
        return []

    # Filter for repos matching prefix and public only
    matching = [
        r
        for r in repos
        if r["name"].startswith(prefix) and not r.get("isPrivate", True)
    ]

    return matching


def get_repo_stats(org, repo_name):
    """Fetch detailed stats for a single repository."""
    full_name = f"{org}/{repo_name}"

    # Get basic stats
    repo_data = run_gh_command(
        [
            "repo",
            "view",
            full_name,
            "--json",
            "stargazerCount,forkCount,watchers,createdAt,url",
        ]
    )

    if repo_data is None:
        return None

    # Get issues (both open and total count)
    issues_data = run_gh_command(
        [
            "issue",
            "list",
            "--repo",
            full_name,
            "--state",
            "open",
            "--json",
            "number,title,author,createdAt,url",
            "--limit",
            "100",
        ]
    )

    if issues_data is None:
        issues_data = []

    # Identify external issues (author not in org owner list)
    # For simplicity, we'll consider issues from users who aren't the repo owner
    external_issues = []
    for issue in issues_data:
        author_login = issue.get("author", {}).get("login", "")
        # External if author is not the org name (simplified heuristic)
        if author_login and author_login != org:
            external_issues.append(issue)

    stats = {
        "stars": repo_data.get("stargazerCount", 0),
        "forks": repo_data.get("forkCount", 0),
        "issues": len(issues_data),
        "watchers": repo_data.get("watchers", {}).get("totalCount", 0),
        "external_issues": len(external_issues),
    }

    # Calculate age in days
    created_at = repo_data.get("createdAt", "")
    age_days = 0
    if created_at:
        created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        age_days = (datetime.now(timezone.utc) - created_date).days

    return {
        "name": repo_name,
        "full_name": full_name,
        "url": repo_data.get("url", ""),
        "created_at": created_at,
        "age_days": age_days,
        "stats": stats,
        "notable_issues": [
            {
                "number": issue.get("number"),
                "title": issue.get("title", ""),
                "author": issue.get("author", {}).get("login", ""),
                "url": issue.get("url", ""),
                "created_at": issue.get("createdAt", ""),
                "is_external": True,
            }
            for issue in external_issues[:5]  # Top 5 external issues
        ],
    }


def load_previous_engagement(date):
    """Load engagement data from previous day."""
    prev_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    prev_path = os.path.join(WORKSPACE, prev_date, "engagement.json")

    if not os.path.exists(prev_path):
        return None

    try:
        with open(prev_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"WARNING: Failed to load previous engagement data: {e}", file=sys.stderr)
        return None


def calculate_growth(current_stats, previous_data, repo_name):
    """Calculate growth metrics compared to previous day."""
    if previous_data is None:
        return None

    # Find matching repo in previous data
    prev_repo = None
    for repo in previous_data.get("repos", []):
        if repo.get("name") == repo_name:
            prev_repo = repo
            break

    if prev_repo is None:
        return None

    prev_stats = prev_repo.get("stats", {})

    return {
        "stars_delta": current_stats["stars"] - prev_stats.get("stars", 0),
        "forks_delta": current_stats["forks"] - prev_stats.get("forks", 0),
        "issues_delta": current_stats["issues"] - prev_stats.get("issues", 0),
    }


def check_thresholds(stats, age_days):
    """Check if repo meets engagement thresholds."""
    return {
        "crossed_25_stars": stats["stars"] >= 25,
        "crossed_50_stars": stats["stars"] >= 50,
        "has_external_issues": stats["external_issues"] >= 2,
        "eligible_for_consensus": stats["stars"] >= 25 and age_days >= 3,
    }


def generate_action_items(repos):
    """Generate action items based on engagement metrics."""
    action_items = []

    for repo in repos:
        thresholds = repo.get("thresholds", {})
        stats = repo.get("stats", {})
        growth = repo.get("growth", {})

        # High priority: Eligible for Consensus Analyst
        if thresholds.get("eligible_for_consensus"):
            action_items.append(
                {
                    "repo": repo["name"],
                    "action": "Trigger Consensus Analyst review",
                    "priority": "high",
                    "reason": f"{stats['stars']} stars, {repo['age_days']} days old",
                }
            )

        # Medium priority: Notable growth
        if growth:
            stars_delta = growth.get("stars_delta", 0)
            if stars_delta >= 10:
                action_items.append(
                    {
                        "repo": repo["name"],
                        "action": "Monitor closely for virality",
                        "priority": "medium",
                        "reason": f"+{stars_delta} stars in 24h",
                    }
                )

        # Medium priority: External issues
        if stats.get("external_issues", 0) >= 2:
            action_items.append(
                {
                    "repo": repo["name"],
                    "action": "Review and respond to external issues",
                    "priority": "medium",
                    "reason": f"{stats['external_issues']} external issues",
                }
            )

        # Low priority: Approaching 25 stars
        if 15 <= stats["stars"] < 25:
            action_items.append(
                {
                    "repo": repo["name"],
                    "action": "Consider social promotion to reach 25 stars",
                    "priority": "low",
                    "reason": f"{stats['stars']} stars (approaching threshold)",
                }
            )

    return action_items


def trigger_consensus_analysts(engagement_data: dict[str, Any], date: str) -> int:
    """Spawn Consensus Analyst for repos that meet engagement thresholds.

    Checks each repo in summary.repos_needing_consensus and spawns the
    consensus-analyst agent if a consensus file does not already exist
    for today.

    Args:
        engagement_data: The full engagement data dict (with summary.repos_needing_consensus).
        date: Date string in YYYY-MM-DD format.

    Returns:
        Number of consensus analysts spawned.
    """
    repos_needing = engagement_data.get("summary", {}).get(
        "repos_needing_consensus", []
    )
    if not repos_needing:
        print("\nNo repos need consensus analysis.")
        return 0

    date_compact = date.replace("-", "")
    analysis_dir = Path.home() / ".openclaw" / "workspace" / "foundry" / "analysis"
    workspace_dir = Path.home() / ".openclaw" / "workspace" / "foundry"
    spawned = 0

    for repo_name in repos_needing:
        consensus_path = analysis_dir / f"{date_compact}-{repo_name}-consensus.json"

        if consensus_path.exists():
            print(f"\n  Consensus already exists for {repo_name}: {consensus_path}")
            continue

        # Find repo data for metrics and threshold info
        repo_data: dict[str, Any] | None = None
        for repo in engagement_data.get("repos", []):
            if repo.get("name") == repo_name:
                repo_data = repo
                break

        if repo_data is None:
            print(
                f"\n  WARNING: No repo data found for {repo_name}, skipping consensus trigger."
            )
            continue

        stats = repo_data.get("stats", {})
        thresholds = repo_data.get("thresholds", {})
        age_days = repo_data.get("age_days", 0)

        # Determine trigger type
        trigger_type = "crossed_25_stars"
        if thresholds.get("crossed_50_stars"):
            trigger_type = "crossed_50_stars"
        if thresholds.get("has_external_issues") and not thresholds.get(
            "crossed_25_stars"
        ):
            trigger_type = "external_issues"

        # Check for build.json and spec.json paths
        repo_date_dir = workspace_dir / f"{date_compact}-{repo_name}"
        build_json = repo_date_dir / "build.json"
        spec_json = repo_date_dir / "spec.json"

        # Also check date-formatted directories
        if not build_json.exists():
            build_json = workspace_dir / date / "build.json"
        if not spec_json.exists():
            spec_json = workspace_dir / date / "spec.json"

        paths_info = ""
        if build_json.exists():
            paths_info += f" Build metadata: {build_json}."
        if spec_json.exists():
            paths_info += f" Spec: {spec_json}."

        message = (
            f"Run Consensus Analyst on build: {repo_name} "
            f"(built {repo_data.get('created_at', 'unknown')}, "
            f"now {stats.get('stars', 0)} stars, {age_days} days old). "
            f"Threshold: {trigger_type}. "
            f"Current metrics: stars={stats.get('stars', 0)}, "
            f"forks={stats.get('forks', 0)}, "
            f"issues={stats.get('issues', 0)}, "
            f"age_days={age_days}."
            f"{paths_info} "
            f"Analyze and output consensus.json."
        )

        print(f"\n  Spawning Consensus Analyst for {repo_name}...")
        print(f"    Trigger: {trigger_type}")
        print(
            f"    Metrics: {stats.get('stars', 0)} stars, {stats.get('forks', 0)} forks, {stats.get('issues', 0)} issues"
        )

        try:
            subprocess.run(
                [
                    "openclaw",
                    "agent",
                    "--agent",
                    "consensus-analyst",
                    "--message",
                    message,
                ],
                check=True,
                timeout=120,
            )
            print(f"    Consensus Analyst spawned successfully for {repo_name}.")
            spawned += 1
        except subprocess.CalledProcessError as e:
            print(
                f"    ERROR: Failed to spawn Consensus Analyst for {repo_name}: {e}",
                file=sys.stderr,
            )
        except subprocess.TimeoutExpired:
            print(
                f"    ERROR: Consensus Analyst spawn timed out for {repo_name}.",
                file=sys.stderr,
            )
        except FileNotFoundError:
            print(
                "    ERROR: 'openclaw' command not found. Is it installed and on PATH?",
                file=sys.stderr,
            )

    print(f"\n  Consensus analysts spawned: {spawned}/{len(repos_needing)}")
    return spawned


def main():
    parser = argparse.ArgumentParser(
        description="Check GitHub engagement for Foundry repos"
    )
    parser.add_argument(
        "--date",
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Date for engagement check (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--org",
        default=DEFAULT_ORG,
        help=f"GitHub organization (default: {DEFAULT_ORG})",
    )
    parser.add_argument(
        "--prefix",
        default=DEFAULT_PREFIX,
        help=f"Repository prefix to filter (default: {DEFAULT_PREFIX})",
    )
    parser.add_argument(
        "--skip-consensus",
        action="store_true",
        default=False,
        help="Skip triggering Consensus Analyst for high-engagement repos",
    )
    args = parser.parse_args()

    date = args.date
    org = args.org
    prefix = args.prefix

    print(f"Checking engagement for {org}/{prefix}* repos on {date}")

    # List all matching repos
    repos = list_repos(org, prefix)
    print(f"Found {len(repos)} public repos matching '{prefix}'")

    if not repos:
        print("No repos found. Exiting.")
        sys.exit(0)

    # Load previous day's data for comparison
    previous_data = load_previous_engagement(date)

    # Collect stats for each repo
    repo_stats = []
    for repo in repos:
        print(f"  Fetching stats for {repo['name']}...")
        stats = get_repo_stats(org, repo["name"])

        if stats is None:
            print(f"    WARNING: Failed to fetch stats for {repo['name']}")
            continue

        # Add growth metrics
        stats["growth"] = calculate_growth(stats["stats"], previous_data, repo["name"])

        # Check thresholds
        stats["thresholds"] = check_thresholds(stats["stats"], stats["age_days"])

        repo_stats.append(stats)

    # Generate summary
    total_stars = sum(r["stats"]["stars"] for r in repo_stats)
    total_forks = sum(r["stats"]["forks"] for r in repo_stats)
    total_issues = sum(r["stats"]["issues"] for r in repo_stats)

    high_engagement = [
        r["name"]
        for r in repo_stats
        if r["thresholds"]["crossed_25_stars"] or r["thresholds"]["has_external_issues"]
    ]

    needs_consensus = [
        r["name"] for r in repo_stats if r["thresholds"]["eligible_for_consensus"]
    ]

    action_items = generate_action_items(repo_stats)

    summary = {
        "total_repos": len(repo_stats),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "total_issues": total_issues,
        "high_engagement_repos": high_engagement,
        "repos_needing_consensus": needs_consensus,
        "action_items": action_items,
    }

    # Build final engagement data
    engagement_data = {
        "schema_version": 1,
        "date": date,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "repos": repo_stats,
        "summary": summary,
    }

    # Write to output file
    day_dir = os.path.join(WORKSPACE, date)
    os.makedirs(day_dir, exist_ok=True)

    output_path = os.path.join(day_dir, "engagement.json")
    with open(output_path, "w") as f:
        json.dump(engagement_data, f, indent=2)

    print(f"\n✅ Engagement data written to {output_path}")
    print("\nSummary:")
    print(f"  Total repos: {summary['total_repos']}")
    print(f"  Total stars: {summary['total_stars']}")
    print(f"  Total forks: {summary['total_forks']}")
    print(f"  Total issues: {summary['total_issues']}")
    print(f"  High engagement: {len(high_engagement)}")
    print(f"  Needs consensus: {len(needs_consensus)}")
    print(f"  Action items: {len(action_items)}")

    if action_items:
        print("\nAction Items:")
        for item in action_items:
            print(f"  [{item['priority'].upper()}] {item['repo']}: {item['action']}")
            print(f"    Reason: {item['reason']}")

    # Trigger Consensus Analyst for qualifying repos
    if not args.skip_consensus:
        trigger_consensus_analysts(engagement_data, date)
    else:
        print("\nSkipping consensus analyst triggers (--skip-consensus flag set).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
