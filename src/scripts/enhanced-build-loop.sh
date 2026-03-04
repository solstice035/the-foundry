#!/bin/bash
# Enhanced multi-run loop for The Foundry
# Runs the pipeline 3 times tonight with enhanced Builder v3

set -euo pipefail

WORKSPACE_BASE="$HOME/.openclaw/workspace/foundry"
LOG_FILE="$WORKSPACE_BASE/enhanced-runs-$(date +%Y-%m-%d).log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

run_pipeline() {
  local run_number="$1"
  log "=== Starting Enhanced Run #$run_number ==="
  
  # Spawn the Blacksmith via OpenClaw
  # Note: This assumes Jeeves is running and can spawn sub-agents
  openclaw send jeeves "Spawn foundry-blacksmith now. Use enhanced Builder v3 (foundry-builder-v3-enhanced.md). Mission: Run full pipeline (Scout → Researcher → Spec → Builder) with production-ready build quality."
  
  log "Blacksmith spawned for run #$run_number. Monitoring completion..."
  
  # Wait for completion (check every 30 minutes for up to 8 hours)
  local max_wait_minutes=480  # 8 hours
  local check_interval=30
  local waited=0
  
  while [ $waited -lt $max_wait_minutes ]; do
    sleep $((check_interval * 60))
    waited=$((waited + check_interval))
    
    # Check if briefing.json exists (indicates completion)
    local today=$(date +%Y-%m-%d)
    if [ -f "$WORKSPACE_BASE/$today/briefing.json" ]; then
      log "Run #$run_number completed! (waited ${waited}m)"
      return 0
    fi
    
    log "Run #$run_number still in progress (waited ${waited}m/${max_wait_minutes}m)..."
  done
  
  log "WARNING: Run #$run_number timed out after ${max_wait_minutes}m"
  return 1
}

main() {
  log "Enhanced Foundry Multi-Run Loop started"
  log "Target: 3 full pipeline runs with enhanced Builder v3"
  log "Expected duration: 8-10 hours total"
  
  # Run 1: Immediate
  run_pipeline 1
  
  # Wait 1 hour between runs to space them out
  log "Run 1 complete. Waiting 1 hour before Run 2..."
  sleep 3600
  
  # Run 2
  run_pipeline 2
  
  # Wait 1 hour
  log "Run 2 complete. Waiting 1 hour before Run 3..."
  sleep 3600
  
  # Run 3
  run_pipeline 3
  
  log "=== All 3 enhanced runs complete ==="
  log "Check briefing messages in Telegram for results"
}

main "$@"
