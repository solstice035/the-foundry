#!/usr/bin/env python3
"""
History cleanup script for The Foundry nightly pipeline.

Removes entries from history.json older than the configured archive window.
Optional deep cleanup prunes old workspace directories, trend-history, and forecasts.
Designed to be called at pipeline start (by the Blacksmith) or via cron.

Usage:
    python3 src/scripts/cleanup_history.py [--days 7] [--history-path PATH]
    python3 src/scripts/cleanup_history.py [--days 7] --deep [--dry-run]

Default: removes entries older than 7 days from the standard history.json path.
"""

import argparse
import json
import re
import shutil
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import structlog

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dedup import cleanup_history

log = structlog.get_logger(__name__)

DEFAULT_HISTORY_PATH = os.path.expanduser("~/.openclaw/workspace/foundry/history.json")
DEFAULT_ARCHIVE_DAYS = 7
DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace" / "foundry"

DATE_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def deep_cleanup(
    workspace: Path,
    dry_run: bool = False,
    workspace_days: int = 14,
    trend_history_days: int = 14,
    forecast_days: int = 30,
) -> Dict[str, List[str]]:
    """Prune old workspace directories, trend-history files, and forecast files.

    Args:
        workspace: Root workspace path (~/.openclaw/workspace/foundry).
        dry_run: If True, report what would be removed without deleting.
        workspace_days: Remove date directories older than this many days.
        trend_history_days: Remove trend-history JSON files older than this many days.
        forecast_days: Remove forecast JSON files older than this many days.

    Returns:
        Dict with keys 'date_dirs', 'trend_files', 'forecast_files', each a list
        of paths that were removed (or would be removed in dry-run mode).
    """
    removed: Dict[str, List[str]] = {
        "date_dirs": [],
        "trend_files": [],
        "forecast_files": [],
    }

    today = datetime.now().date()

    # --- 1. Workspace date directories: YYYY-MM-DD/ ---
    ws_cutoff = today - timedelta(days=workspace_days)
    log.info(
        "deep_cleanup.date_dirs",
        workspace=str(workspace),
        cutoff=str(ws_cutoff),
        dry_run=dry_run,
    )
    if workspace.is_dir():
        for entry in sorted(workspace.iterdir()):
            if entry.is_dir() and DATE_DIR_RE.match(entry.name):
                try:
                    dir_date = datetime.strptime(entry.name, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if dir_date < ws_cutoff:
                    removed["date_dirs"].append(str(entry))
                    if not dry_run:
                        shutil.rmtree(entry)
                        log.info("deep_cleanup.removed_dir", path=str(entry))

    # --- 2. Trend-history files: trend-history/YYYY-MM-DD.json ---
    trend_dir = workspace / "trend-history"
    th_cutoff = today - timedelta(days=trend_history_days)
    log.info(
        "deep_cleanup.trend_history",
        path=str(trend_dir),
        cutoff=str(th_cutoff),
        dry_run=dry_run,
    )
    if trend_dir.is_dir():
        for f in sorted(trend_dir.iterdir()):
            if f.is_file() and f.suffix == ".json" and DATE_DIR_RE.match(f.stem):
                try:
                    file_date = datetime.strptime(f.stem, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if file_date < th_cutoff:
                    removed["trend_files"].append(str(f))
                    if not dry_run:
                        f.unlink()
                        log.info("deep_cleanup.removed_trend", path=str(f))

    # --- 3. Forecast files: forecasts/forecast-*.json ---
    forecast_dir = workspace / "forecasts"
    fc_cutoff = today - timedelta(days=forecast_days)
    log.info(
        "deep_cleanup.forecasts",
        path=str(forecast_dir),
        cutoff=str(fc_cutoff),
        dry_run=dry_run,
    )
    if forecast_dir.is_dir():
        for f in sorted(forecast_dir.glob("forecast-*.json")):
            if not f.is_file():
                continue
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                # Try to read a date field from the file
                file_date_str = data.get("date") or data.get("generated_at", "")
                if file_date_str:
                    file_date = datetime.fromisoformat(
                        file_date_str.replace("Z", "+00:00")
                    ).date()
                else:
                    # Fall back to file modification time
                    file_date = datetime.fromtimestamp(f.stat().st_mtime).date()
            except (json.JSONDecodeError, ValueError, OSError):
                # Fall back to file modification time
                try:
                    file_date = datetime.fromtimestamp(f.stat().st_mtime).date()
                except OSError:
                    continue
            if file_date < fc_cutoff:
                removed["forecast_files"].append(str(f))
                if not dry_run:
                    f.unlink()
                    log.info("deep_cleanup.removed_forecast", path=str(f))

    # --- Summary ---
    log.info(
        "deep_cleanup.summary",
        date_dirs=len(removed["date_dirs"]),
        trend_files=len(removed["trend_files"]),
        forecast_files=len(removed["forecast_files"]),
        dry_run=dry_run,
    )

    return removed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean up old entries from Foundry history.json"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_ARCHIVE_DAYS,
        help=f"Remove entries older than N days (default: {DEFAULT_ARCHIVE_DAYS})",
    )
    parser.add_argument(
        "--history-path",
        type=str,
        default=DEFAULT_HISTORY_PATH,
        help=f"Path to history.json (default: {DEFAULT_HISTORY_PATH})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without modifying the file",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Also prune old workspace date dirs, trend-history, and forecast files",
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=str(DEFAULT_WORKSPACE),
        help=f"Foundry workspace root (default: {DEFAULT_WORKSPACE})",
    )
    args = parser.parse_args()

    history_path = args.history_path

    # Gracefully handle missing or corrupt history.json
    if not os.path.exists(history_path):
        print(f"⚠️  History file not found: {history_path}")
        print("   Creating fresh history.json")
        fresh = {
            "schema_version": 1,
            "builds": [],
            "rejections": [],
            "dedup_window_days": 30,
        }
        Path(history_path).parent.mkdir(parents=True, exist_ok=True)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(fresh, f, indent=2)
        print("   Fresh history.json created. Nothing to clean up.")
        if args.deep:
            _run_deep_cleanup(args)
        return

    try:
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
        if not isinstance(history, dict) or "builds" not in history:
            raise ValueError("Invalid structure")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️  Corrupt history.json: {e}")
        print("   Backing up and creating fresh history.json")
        backup_path = (
            f"{history_path}.corrupt.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        os.rename(history_path, backup_path)
        print(f"   Backup: {backup_path}")
        fresh = {
            "schema_version": 1,
            "builds": [],
            "rejections": [],
            "dedup_window_days": 30,
        }
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(fresh, f, indent=2)
        print("   Fresh history.json created. Nothing to clean up.")
        if args.deep:
            _run_deep_cleanup(args)
        return

    # Show current state
    builds_count = len(history.get("builds", []))
    rejections_count = len(history.get("rejections", []))
    print(f"📋 History: {builds_count} builds, {rejections_count} rejections")
    print(f"🗓️  Cleaning entries older than {args.days} days")

    if args.dry_run:
        # Simulate without writing
        cutoff = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
        old_builds = [
            b for b in history.get("builds", []) if b.get("date", "") < cutoff
        ]
        old_rejections = [
            r for r in history.get("rejections", []) if r.get("date", "") < cutoff
        ]
        print("\n🔍 DRY RUN — would remove:")
        print(f"   {len(old_builds)} builds:")
        for b in old_builds:
            print(f"     - {b.get('date')} {b.get('project_name', 'unknown')}")
        print(f"   {len(old_rejections)} rejections:")
        for r in old_rejections:
            print(f"     - {r.get('date')} {r.get('title', 'unknown')[:50]}")
        if args.deep:
            _run_deep_cleanup(args)
        return

    stats = cleanup_history(history_path, archive_days=args.days)

    print("✅ Cleanup complete:")
    print(f"   Builds removed: {stats['builds_removed']}")
    print(f"   Rejections removed: {stats['rejections_removed']}")

    # Show remaining
    with open(history_path, "r", encoding="utf-8") as f:
        updated = json.load(f)
    print(
        f"   Remaining: {len(updated.get('builds', []))} builds, {len(updated.get('rejections', []))} rejections"
    )

    # Deep cleanup (workspace dirs, trend-history, forecasts)
    if args.deep:
        _run_deep_cleanup(args)


def _run_deep_cleanup(args: argparse.Namespace) -> None:
    """Run the deep cleanup pass on workspace artifacts.

    Args:
        args: Parsed CLI arguments (must include workspace and dry_run).
    """
    workspace = Path(args.workspace)
    print(f"\nDeep cleanup: workspace={workspace}")
    results = deep_cleanup(workspace=workspace, dry_run=args.dry_run)

    label = "DRY RUN -- would remove" if args.dry_run else "Removed"

    if results["date_dirs"]:
        print(f"\n  {label} {len(results['date_dirs'])} workspace date directories:")
        for d in results["date_dirs"]:
            print(f"    - {d}")
    else:
        print("\n  No old workspace date directories to remove.")

    if results["trend_files"]:
        print(f"  {label} {len(results['trend_files'])} trend-history files:")
        for f in results["trend_files"]:
            print(f"    - {f}")
    else:
        print("  No old trend-history files to remove.")

    if results["forecast_files"]:
        print(f"  {label} {len(results['forecast_files'])} forecast files:")
        for f in results["forecast_files"]:
            print(f"    - {f}")
    else:
        print("  No old forecast files to remove.")


if __name__ == "__main__":
    main()
