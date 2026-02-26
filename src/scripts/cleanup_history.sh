#!/bin/bash
#
# cleanup_history.sh - Weekly cleanup of old history entries
#
# Removes builds and rejections older than 30 days from history.json.
# The active deduplication window is 14 days, but we keep 30 days of history
# for metrics and portfolio analysis.
#
# Usage: ./cleanup_history.sh
#
# Intended to run via cron: Saturday 03:00 GMT
# Example cron entry:
#   0 3 * * 6 cd ~/projects/the-foundry && ./src/scripts/cleanup_history.sh >> /tmp/foundry-cleanup.log 2>&1
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HISTORY_PATH="$HOME/.openclaw/workspace/foundry/history.json"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting history cleanup..."

# Check if history.json exists
if [ ! -f "$HISTORY_PATH" ]; then
    echo "  ✗ history.json not found at $HISTORY_PATH"
    exit 0
fi

# Run cleanup via Python
cd "$PROJECT_ROOT"
python3 << EOF
import json
import sys
from src.dedup import cleanup_history

history_path = '$HISTORY_PATH'

try:
    stats = cleanup_history(history_path, archive_days=30)
    print(f"  ✓ Removed {stats['builds_removed']} old builds")
    print(f"  ✓ Removed {stats['rejections_removed']} old rejections")
    
    # Log summary
    with open(history_path) as f:
        history = json.load(f)
    print(f"  Current history: {len(history.get('builds', []))} builds, {len(history.get('rejections', []))} rejections")
    
except Exception as e:
    print(f"  ✗ Cleanup failed: {e}", file=sys.stderr)
    sys.exit(1)
EOF

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] History cleanup complete"
