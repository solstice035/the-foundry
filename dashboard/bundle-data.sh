#!/bin/bash
# Bundle all Foundry workspace data into a single JSON file for the dashboard
set -e

WORKSPACE="$HOME/.openclaw/workspace/foundry"
BUILDS_DIR="$HOME/projects/foundry"
OUTPUT="$(dirname "$0")/public/dashboard-data.json"

# Helper: read a JSON file or return null
read_json() {
  if [ -f "$1" ]; then
    cat "$1"
  else
    echo "null"
  fi
}

# Helper: read JSON file, extract top N entries by score from .trends array
read_trends_top() {
  local file="$1"
  local n="${2:-15}"
  if [ -f "$file" ]; then
    jq -c "[.trends // [] | sort_by(-.final_score // -.buildability_score // 0)][:${n}]" "$file" 2>/dev/null || echo "[]"
  else
    echo "[]"
  fi
}

# Helper: read trends metadata (counts, lifecycle summary) without the full array
read_trends_meta() {
  local file="$1"
  if [ -f "$file" ]; then
    jq -c '{
      total_trends: (.trends // [] | length),
      sources_scanned: (.sources_scanned // null),
      scan_duration_seconds: (.scan_duration_seconds // null),
      lifecycle_summary: (
        [(.trends // [])[].lifecycle_status // "unknown"] | group_by(.) |
        map({(.[0]): length}) | add // {}
      )
    }' "$file" 2>/dev/null || echo "null"
  else
    echo "null"
  fi
}

echo "Bundling Foundry dashboard data..."

# 1. Metrics
METRICS=$(cat "$WORKSPACE/metrics.jsonl" 2>/dev/null | jq -s '.' || echo "[]")

# 2. History
HISTORY=$(read_json "$WORKSPACE/history.json")

# 3. Per-night data
NIGHTS="{}"
for dir in "$WORKSPACE"/2026-*/; do
  [ -d "$dir" ] || continue
  DATE=$(basename "$dir")

  STATE=$(read_json "$dir/state.json")
  SPEC=$(read_json "$dir/spec.json")
  BUILD=$(read_json "$dir/build.json")
  BRIEFING=$(read_json "$dir/briefing.json")
  ENGAGEMENT=$(read_json "$dir/engagement.json")
  TRENDS_META=$(read_trends_meta "$dir/trends-summary.json")
  TRENDS_TOP=$(read_trends_top "$dir/trends-summary.json" 15)

  NIGHT=$(jq -n \
    --argjson state "$STATE" \
    --argjson spec "$SPEC" \
    --argjson build "$BUILD" \
    --argjson briefing "$BRIEFING" \
    --argjson engagement "$ENGAGEMENT" \
    --argjson trends_meta "$TRENDS_META" \
    --argjson trends_top "$TRENDS_TOP" \
    '{state: $state, spec: $spec, build: $build, briefing: $briefing, engagement: $engagement, trends_meta: $trends_meta, trends_top: $trends_top}')

  NIGHTS=$(echo "$NIGHTS" | jq --arg date "$DATE" --argjson night "$NIGHT" '. + {($date): $night}')
done

# 4. Social data
CONTENT_QUEUE=$(read_json "$WORKSPACE/social/content-queue.json")
VOICE_PATTERNS=$(read_json "$WORKSPACE/social/voice-patterns.json")

# 5. Weekly reports
WEEKLY_REPORTS="[]"
for report in "$WORKSPACE"/reports/metrics-aggregated-*.json; do
  [ -f "$report" ] || continue
  WEEKLY_REPORTS=$(echo "$WEEKLY_REPORTS" | jq --argjson r "$(cat "$report")" '. + [$r]')
done

# 6. Build repo names
BUILD_REPOS=$(ls -1 "$BUILDS_DIR" 2>/dev/null | jq -R -s 'split("\n") | map(select(length > 0))' || echo "[]")

# Assemble final bundle
jq -n \
  --arg generated_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson metrics "$METRICS" \
  --argjson history "$HISTORY" \
  --argjson nights "$NIGHTS" \
  --argjson content_queue "$CONTENT_QUEUE" \
  --argjson voice_patterns "$VOICE_PATTERNS" \
  --argjson weekly_reports "$WEEKLY_REPORTS" \
  --argjson build_repos "$BUILD_REPOS" \
  '{
    generated_at: $generated_at,
    metrics: $metrics,
    history: $history,
    nights: $nights,
    social: {
      content_queue: $content_queue,
      voice_patterns: $voice_patterns
    },
    weekly_reports: $weekly_reports,
    build_repos: $build_repos
  }' > "$OUTPUT"

echo "Dashboard data bundled to $OUTPUT"
echo "  Nights: $(echo "$NIGHTS" | jq 'keys | length')"
echo "  Metrics: $(echo "$METRICS" | jq 'length')"
echo "  Build repos: $(echo "$BUILD_REPOS" | jq 'length')"
echo "  Social drafts: $(echo "$CONTENT_QUEUE" | jq '.pending // [] | length')"
