#!/usr/bin/env python3
"""
Multi-run spawner for The Foundry enhanced builds.
Spawns additional Blacksmith runs at intervals through the night.
"""

import time
import subprocess
import sys
from datetime import datetime, timedelta

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def spawn_blacksmith(run_number):
    """Spawn a Blacksmith run via openclaw CLI"""
    log(f"Spawning enhanced run #{run_number}...")
    
    task = f"""You are foundry-blacksmith, The Blacksmith. Run the full Foundry pipeline (Run #{run_number}) with ENHANCED PRODUCTION-READY builds.

Read and execute: ~/projects/the-foundry/src/prompts/foundry-blacksmith-v2.md

CRITICAL MODIFICATION for tonight:
- When you reach Stage 4 (Builder), use the ENHANCED Builder prompt at ~/projects/the-foundry/src/prompts/foundry-builder-v3-enhanced.md instead of v2
- This means: spawn foundry-builder with instructions to read foundry-builder-v3-enhanced.md
- The enhanced version builds feature-complete, production-ready projects (not MVPs)
- Expect longer build times (30-90 min instead of 7-20 min)
- Expect higher costs ($2-5 instead of $0.40-$0.80)
- Quality bar: portfolio-worthy, genuinely useful apps

Pipeline: Scout → Researcher → Spec → Builder (ENHANCED) → Briefing

Run the full pipeline and deliver the briefing to Nick via Telegram when complete."""
    
    try:
        # Use openclaw send to spawn via Jeeves
        cmd = [
            'openclaw', 'send', 'jeeves',
            f'Spawn foundry-blacksmith (run #{run_number}): {task}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            log(f"✓ Run #{run_number} spawned successfully")
            return True
        else:
            log(f"✗ Run #{run_number} spawn failed: {result.stderr}")
            return False
            
    except Exception as e:
        log(f"✗ Run #{run_number} spawn error: {e}")
        return False

def main():
    log("Enhanced Foundry Multi-Run Spawner started")
    log("Will spawn 2 additional runs at 2-hour intervals")
    
    # Wait 2 hours, then spawn run 2
    wait_seconds = 2 * 60 * 60
    next_run_time = datetime.now() + timedelta(seconds=wait_seconds)
    
    log(f"Next run (#2) scheduled for {next_run_time.strftime('%H:%M:%S')}")
    time.sleep(wait_seconds)
    spawn_blacksmith(2)
    
    # Wait another 2 hours, then spawn run 3
    next_run_time = datetime.now() + timedelta(seconds=wait_seconds)
    log(f"Next run (#3) scheduled for {next_run_time.strftime('%H:%M:%S')}")
    time.sleep(wait_seconds)
    spawn_blacksmith(3)
    
    log("All scheduled runs spawned. Multi-run spawner complete.")

if __name__ == '__main__':
    main()
