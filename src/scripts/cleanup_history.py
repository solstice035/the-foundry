#!/usr/bin/env python3
"""
History cleanup script for The Foundry nightly pipeline.

Removes entries from history.json older than the configured archive window.
Designed to be called at pipeline start (by the Blacksmith) or via cron.

Usage:
    python3 src/scripts/cleanup_history.py [--days 7] [--history-path PATH]

Default: removes entries older than 7 days from the standard history.json path.
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dedup import cleanup_history


DEFAULT_HISTORY_PATH = os.path.expanduser(
    '~/.openclaw/workspace/foundry/history.json'
)
DEFAULT_ARCHIVE_DAYS = 7


def main():
    parser = argparse.ArgumentParser(
        description='Clean up old entries from Foundry history.json'
    )
    parser.add_argument(
        '--days', type=int, default=DEFAULT_ARCHIVE_DAYS,
        help=f'Remove entries older than N days (default: {DEFAULT_ARCHIVE_DAYS})'
    )
    parser.add_argument(
        '--history-path', type=str, default=DEFAULT_HISTORY_PATH,
        help=f'Path to history.json (default: {DEFAULT_HISTORY_PATH})'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be removed without modifying the file'
    )
    args = parser.parse_args()

    history_path = args.history_path

    # Gracefully handle missing or corrupt history.json
    if not os.path.exists(history_path):
        print(f"⚠️  History file not found: {history_path}")
        print("   Creating fresh history.json")
        fresh = {
            'schema_version': 1,
            'builds': [],
            'rejections': [],
            'dedup_window_days': 30
        }
        Path(history_path).parent.mkdir(parents=True, exist_ok=True)
        with open(history_path, 'w') as f:
            json.dump(fresh, f, indent=2)
        print("   ✅ Fresh history.json created. Nothing to clean up.")
        return

    try:
        with open(history_path, 'r') as f:
            history = json.load(f)
        if not isinstance(history, dict) or 'builds' not in history:
            raise ValueError("Invalid structure")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️  Corrupt history.json: {e}")
        print("   Backing up and creating fresh history.json")
        backup_path = f"{history_path}.corrupt.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        os.rename(history_path, backup_path)
        print(f"   Backup: {backup_path}")
        fresh = {
            'schema_version': 1,
            'builds': [],
            'rejections': [],
            'dedup_window_days': 30
        }
        with open(history_path, 'w') as f:
            json.dump(fresh, f, indent=2)
        print("   ✅ Fresh history.json created. Nothing to clean up.")
        return

    # Show current state
    builds_count = len(history.get('builds', []))
    rejections_count = len(history.get('rejections', []))
    print(f"📋 History: {builds_count} builds, {rejections_count} rejections")
    print(f"🗓️  Cleaning entries older than {args.days} days")

    if args.dry_run:
        # Simulate without writing
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
        old_builds = [b for b in history.get('builds', []) if b.get('date', '') < cutoff]
        old_rejections = [r for r in history.get('rejections', []) if r.get('date', '') < cutoff]
        print(f"\n🔍 DRY RUN — would remove:")
        print(f"   {len(old_builds)} builds:")
        for b in old_builds:
            print(f"     - {b.get('date')} {b.get('project_name', 'unknown')}")
        print(f"   {len(old_rejections)} rejections:")
        for r in old_rejections:
            print(f"     - {r.get('date')} {r.get('title', 'unknown')[:50]}")
        return

    stats = cleanup_history(history_path, archive_days=args.days)

    print(f"✅ Cleanup complete:")
    print(f"   Builds removed: {stats['builds_removed']}")
    print(f"   Rejections removed: {stats['rejections_removed']}")

    # Show remaining
    with open(history_path, 'r') as f:
        updated = json.load(f)
    print(f"   Remaining: {len(updated.get('builds', []))} builds, {len(updated.get('rejections', []))} rejections")


if __name__ == '__main__':
    main()
