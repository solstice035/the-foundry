#!/usr/bin/env python3
"""Weekly Metrics Aggregation for The Foundry.

Reads metrics.jsonl, filters to a Monday-Sunday week, and computes
aggregated metrics for the portfolio curator's weekly report.

Usage:
    python3 aggregate_metrics.py --week-of 2026-03-03 [--metrics-path PATH]

Output:
    ~/.openclaw/workspace/foundry/reports/metrics-aggregated-YYYY-MM-DD.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import structlog

log = structlog.get_logger()

DEFAULT_METRICS_PATH = (
    Path.home() / ".openclaw" / "workspace" / "foundry" / "metrics.jsonl"
)
DEFAULT_REPORTS_DIR = Path.home() / ".openclaw" / "workspace" / "foundry" / "reports"


def get_week_bounds(week_of: date) -> tuple[date, date]:
    """Return (Monday, Sunday) for the week containing the given date.

    Args:
        week_of: Any date within the target week.

    Returns:
        Tuple of (week_start, week_end) where week_start is Monday
        and week_end is Sunday.
    """
    monday = week_of - timedelta(days=week_of.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def load_metrics(
    metrics_path: Path, week_start: date, week_end: date
) -> list[dict[str, Any]]:
    """Load and filter metrics.jsonl to the given week.

    Args:
        metrics_path: Path to metrics.jsonl file.
        week_start: Monday of the target week.
        week_end: Sunday of the target week.

    Returns:
        List of metric entries within the date range.

    Raises:
        FileNotFoundError: If metrics_path does not exist.
    """
    if not metrics_path.exists():
        raise FileNotFoundError(f"Metrics file not found: {metrics_path}")

    entries: list[dict[str, Any]] = []
    with metrics_path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                log.warning("skipping_invalid_json", line_num=line_num)
                continue

            entry_date_str = entry.get("date")
            if not entry_date_str:
                log.warning("skipping_entry_no_date", line_num=line_num)
                continue

            try:
                entry_date = date.fromisoformat(entry_date_str)
            except ValueError:
                log.warning(
                    "skipping_invalid_date", line_num=line_num, date=entry_date_str
                )
                continue

            if week_start <= entry_date <= week_end:
                entries.append(entry)

    log.info(
        "metrics_loaded",
        total=len(entries),
        week_start=str(week_start),
        week_end=str(week_end),
    )
    return entries


def _safe_avg(values: list[float | int]) -> float:
    """Compute average of a list, returning 0.0 if empty."""
    return round(sum(values) / len(values), 2) if values else 0.0


def compute_overview(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute overview section: build counts and rates.

    Args:
        entries: Filtered metric entries for the week.

    Returns:
        Overview dict with builds_attempted, builds_succeeded, etc.
    """
    nights_total = len(entries)
    specs_rejected = sum(1 for e in entries if e.get("type") == "rejected")
    builds_attempted = sum(
        1 for e in entries if e.get("type") in ("success", "failure", "partial")
    )
    builds_succeeded = sum(1 for e in entries if e.get("type") == "success")
    builds_failed = sum(1 for e in entries if e.get("type") in ("failure", "partial"))

    success_rate = (
        round((builds_succeeded / builds_attempted * 100), 1)
        if builds_attempted > 0
        else 0.0
    )
    approval_rate = (
        round(((nights_total - specs_rejected) / nights_total * 100), 1)
        if nights_total > 0
        else 0.0
    )

    return {
        "builds_attempted": builds_attempted,
        "builds_succeeded": builds_succeeded,
        "builds_failed": builds_failed,
        "specs_rejected": specs_rejected,
        "success_rate": success_rate,
        "approval_rate": approval_rate,
    }


def compute_performance(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute performance section: average timings, cost, tokens.

    Args:
        entries: Filtered metric entries for the week.

    Returns:
        Performance dict with avg timings, costs, and token totals.
    """
    scan_times = [
        e["scout_duration_s"] for e in entries if e.get("scout_duration_s") is not None
    ]
    spec_times = [
        e["spec_duration_s"] for e in entries if e.get("spec_duration_s") is not None
    ]
    build_times = [
        e["build_duration_s"]
        for e in entries
        if e.get("build_duration_s") is not None and e["build_duration_s"] > 0
    ]
    total_times = [
        e["total_duration_s"] for e in entries if e.get("total_duration_s") is not None
    ]

    costs = [e.get("cost_usd", 0) for e in entries]
    total_cost = round(sum(costs), 2)
    avg_cost = round(total_cost / len(entries), 2) if entries else 0.0

    tokens = [e["tokens_used"] for e in entries if e.get("tokens_used") is not None]
    total_tokens = sum(tokens) if tokens else None

    return {
        "avg_scan_time_s": _safe_avg(scan_times),
        "avg_spec_time_s": _safe_avg(spec_times),
        "avg_build_time_s": _safe_avg(build_times),
        "avg_total_time_s": _safe_avg(total_times),
        "total_cost_usd": total_cost,
        "avg_cost_per_night": avg_cost,
        "total_tokens": total_tokens,
    }


def compute_sources(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute source effectiveness from scout_sources_succeeded and source fields.

    Args:
        entries: Filtered metric entries for the week.

    Returns:
        Sources dict with effectiveness array.
    """
    # Track which sources found trends (from scout_sources_succeeded)
    source_trends: dict[str, int] = defaultdict(int)
    for e in entries:
        for src in e.get("scout_sources_succeeded", []):
            source_trends[src] += e.get("scout_trends_found", 0)

    # Track which source led to a successful build (from source field)
    source_builds: dict[str, int] = defaultdict(int)
    source_engagement: dict[str, list[float]] = defaultdict(list)
    for e in entries:
        src = e.get("source")
        if src and e.get("type") == "success":
            source_builds[src] += 1
        if src and e.get("engagement_score") is not None:
            source_engagement[src].append(e["engagement_score"])

    all_sources = set(source_trends.keys()) | set(source_builds.keys())
    effectiveness = []
    for src in sorted(all_sources):
        trends = source_trends.get(src, 0)
        shipped = source_builds.get(src, 0)
        rate = round((shipped / trends * 100), 1) if trends > 0 else 0.0
        avg_eng = (
            min(
                round(sum(source_engagement[src]) / len(source_engagement[src]), 1),
                100.0,
            )
            if source_engagement[src]
            else None
        )
        effectiveness.append(
            {
                "source": src,
                "trends_found": trends,
                "builds_shipped": shipped,
                "success_rate": rate,
                "avg_engagement": avg_eng,
            }
        )

    return {"effectiveness": effectiveness}


def compute_categories(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute category distribution.

    Args:
        entries: Filtered metric entries for the week.

    Returns:
        Categories dict with distribution array.
    """
    cat_counts: Counter[str] = Counter()
    cat_buildability: dict[str, list[float]] = defaultdict(list)

    for e in entries:
        cat = e.get("category") or "unknown"
        cat_counts[cat] += 1
        if e.get("buildability_score") is not None:
            cat_buildability[cat].append(e["buildability_score"])

    total = sum(cat_counts.values())
    distribution = []
    for cat, count in cat_counts.most_common():
        pct = round((count / total * 100), 1) if total > 0 else 0.0
        avg_build = (
            round(sum(cat_buildability[cat]) / len(cat_buildability[cat]), 1)
            if cat_buildability[cat]
            else None
        )
        distribution.append(
            {
                "category": cat,
                "count": count,
                "percentage": pct,
                "avg_buildability": avg_build,
            }
        )

    return {"distribution": distribution}


def compute_rejection_reasons(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group and count rejection reasons.

    Args:
        entries: Filtered metric entries for the week.

    Returns:
        List of {reason, count} dicts sorted by count descending.
    """
    reasons: Counter[str] = Counter()
    for e in entries:
        reason = e.get("spec_rejection_reason")
        if reason:
            reasons[reason] += 1

    return [{"reason": r, "count": c} for r, c in reasons.most_common()]


def compute_notable_builds(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Find notable builds by engagement and buildability scores.

    Args:
        entries: Filtered metric entries for the week.

    Returns:
        List of notable build dicts, sorted by engagement descending.
    """
    successful = [e for e in entries if e.get("type") == "success" and e.get("project")]
    # Sort by engagement_score descending, take top 5
    successful.sort(key=lambda e: e.get("engagement_score", 0), reverse=True)

    notable = []
    for e in successful[:5]:
        build: dict[str, Any] = {"date": e["date"], "project": e["project"]}
        if e.get("repo_url"):
            build["repo_url"] = e["repo_url"]
        if e.get("buildability_score") is not None:
            build["buildability_score"] = e["buildability_score"]
        if e.get("engagement_score") is not None:
            build["engagement_score"] = e["engagement_score"]
        notable.append(build)

    return notable


def generate_recommendations(
    entries: list[dict[str, Any]],
    overview: dict[str, Any],
    performance: dict[str, Any],
    sources: dict[str, Any],
) -> list[str]:
    """Auto-generate actionable insights from the aggregated data.

    Args:
        entries: Filtered metric entries for the week.
        overview: Computed overview section.
        performance: Computed performance section.
        sources: Computed sources section.

    Returns:
        List of recommendation strings.
    """
    recs: list[str] = []

    # Source dominance
    effectiveness = sources.get("effectiveness", [])
    total_shipped = sum(s["builds_shipped"] for s in effectiveness)
    if total_shipped > 0:
        for s in effectiveness:
            pct = round(s["builds_shipped"] / total_shipped * 100)
            if pct >= 50:
                recs.append(
                    f"{s['source'].title()} sourced {pct}% of successful builds -- consider increasing scan depth for this source."
                )

    # Low success rate
    if overview["builds_attempted"] > 0 and overview["success_rate"] < 50:
        recs.append(
            f"Success rate is {overview['success_rate']}% -- investigate build failures and consider adjusting spec criteria."
        )

    # High rejection rate
    if overview.get("approval_rate", 100) < 50:
        recs.append(
            f"Approval rate is {overview['approval_rate']}% -- scout may need broader source coverage or adjusted trend thresholds."
        )

    # Cost trending
    if performance["avg_cost_per_night"] > 0.50:
        recs.append(
            f"Average cost per night is ${performance['avg_cost_per_night']:.2f} -- review model selection and token usage."
        )

    # Build time
    if performance["avg_build_time_s"] > 600:
        recs.append(
            f"Average build time is {performance['avg_build_time_s']:.0f}s -- investigate timeouts or complexity issues."
        )

    # No entries
    if not entries:
        recs.append(
            "No pipeline runs recorded this week -- check cron schedules and agent health."
        )

    # Source failures
    failure_sources: Counter[str] = Counter()
    for e in entries:
        for src in e.get("scout_sources_failed", []):
            failure_sources[src] += 1
    for src, count in failure_sources.most_common():
        if count >= 3:
            recs.append(
                f"Source '{src}' failed {count} times this week -- check API credentials and rate limits."
            )

    # If no recs generated, add a positive one
    if not recs and entries:
        recs.append("All metrics within normal ranges. Pipeline operating smoothly.")

    return recs


def aggregate(
    entries: list[dict[str, Any]], week_start: date, week_end: date
) -> dict[str, Any]:
    """Aggregate all metric sections from filtered entries.

    Args:
        entries: Filtered metric entries for the week.
        week_start: Monday of the target week.
        week_end: Sunday of the target week.

    Returns:
        Complete aggregated metrics dict conforming to the schema.
    """
    overview = compute_overview(entries)
    performance = compute_performance(entries)
    sources = compute_sources(entries)
    categories = compute_categories(entries)
    rejection_reasons = compute_rejection_reasons(entries)
    notable_builds = compute_notable_builds(entries)
    recommendations = generate_recommendations(entries, overview, performance, sources)

    return {
        "week_start": str(week_start),
        "week_end": str(week_end),
        "nights_total": len(entries),
        "overview": overview,
        "performance": performance,
        "sources": sources,
        "categories": categories,
        "rejection_reasons": rejection_reasons,
        "notable_builds": notable_builds,
        "recommendations": recommendations,
    }


def write_report(report: dict[str, Any], week_start: date, reports_dir: Path) -> Path:
    """Write the aggregated report to JSON file.

    Args:
        report: Aggregated metrics dict.
        week_start: Monday of the target week (used in filename).
        reports_dir: Directory to write the report to.

    Returns:
        Path to the written report file.
    """
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / f"metrics-aggregated-{week_start}.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write("\n")

    log.info("report_written", path=str(output_path))
    return output_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Parsed namespace with week_of and metrics_path.
    """
    parser = argparse.ArgumentParser(
        description="Aggregate weekly metrics from The Foundry pipeline runs.",
    )
    parser.add_argument(
        "--week-of",
        required=True,
        type=str,
        help="Any date in the target week (YYYY-MM-DD). Script finds the Monday.",
    )
    parser.add_argument(
        "--metrics-path",
        type=str,
        default=str(DEFAULT_METRICS_PATH),
        help=f"Path to metrics.jsonl (default: {DEFAULT_METRICS_PATH})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the metrics aggregation script.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, 1 for error).
    """
    args = parse_args(argv)

    try:
        week_of = date.fromisoformat(args.week_of)
    except ValueError:
        log.error("invalid_date", date=args.week_of)
        print(
            f"Error: Invalid date format '{args.week_of}'. Use YYYY-MM-DD.",
            file=sys.stderr,
        )
        return 1

    metrics_path = Path(args.metrics_path)
    week_start, week_end = get_week_bounds(week_of)

    log.info(
        "aggregating_metrics",
        week_start=str(week_start),
        week_end=str(week_end),
        metrics_path=str(metrics_path),
    )

    try:
        entries = load_metrics(metrics_path, week_start, week_end)
    except FileNotFoundError as exc:
        log.error("metrics_file_not_found", path=str(metrics_path))
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    report = aggregate(entries, week_start, week_end)
    output_path = write_report(report, week_start, DEFAULT_REPORTS_DIR)

    print(f"Report written to: {output_path}")
    print(f"Week: {week_start} to {week_end} ({report['nights_total']} nights)")
    print(
        f"Builds: {report['overview']['builds_succeeded']}/{report['overview']['builds_attempted']} succeeded ({report['overview']['success_rate']}%)"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
