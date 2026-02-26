#!/bin/bash
# Test foundry-spec consistency: run 3 times, compare decisions
# Usage: bash test-foundry-spec.sh

DATE="2026-02-18"
WORKSPACE="$HOME/.openclaw/workspace/foundry/$DATE"
PROMPT_FILE="$HOME/projects/the-foundry/src/prompts/foundry-spec-v1.md"
TRENDS_FILE="$WORKSPACE/trends-summary.json"
HISTORY_FILE="$HOME/.openclaw/workspace/foundry/history.json"

echo "=== foundry-spec Consistency Test ==="
echo "Date: $DATE"
echo "Trends: $TRENDS_FILE"
echo "History: $HISTORY_FILE"
echo ""

for i in 1 2 3; do
  OUTPUT="$WORKSPACE/spec-test-run-$i.json"
  echo "--- Run $i ---"
  echo "Output: $OUTPUT"
  echo ""
done

echo "Run the agent 3 times, save output to spec-test-run-{1,2,3}.json"
echo "Then compare decisions."
