# Foundry Builder v2 — Aider Integration Workflow

## Overview
The Builder stage takes a `spec.json` from the Spec Writer and uses aider (AI pair programmer) to autonomously generate a complete project.

## Prerequisites
- `aider` installed and accessible via PATH
- API key available (OpenRouter recommended via `OPENROUTER_API_KEY`)
- `gh` CLI authenticated for GitHub operations
- `git` configured with user.name and user.email

## Workflow

### 1. Setup
```bash
mkdir -p ~/projects/foundry/<DATE>-<PROJECT_NAME>
cd ~/projects/foundry/<DATE>-<PROJECT_NAME>
git init
git branch -m main
git config user.name "The Foundry"
git config user.email "foundry@jeevesbot.io"
```

### 2. Prepare Build Prompt
Extract from `spec.json`:
- Project name, description
- Tech stack
- Must-have features (detailed implementation guidance)
- Nice-to-have features
- Out of scope items
- Success criteria
- File structure expectations

Format as a comprehensive single message for aider's `--message` flag.

### 3. Spawn Aider
```bash
OPENROUTER_API_KEY=<key> aider \
  --yes \
  --model openrouter/anthropic/claude-sonnet-4-5 \
  --message "<build prompt>" \
  2>&1 | tee build.log
```

**Key flags:**
- `--yes`: Auto-accept all changes (batch mode)
- `--model`: Use Claude Sonnet 4.5 via OpenRouter
- Pipe to `tee build.log` for logging

**Timeout:** 5 hours (18000 seconds)
**Background after:** 2 minutes (check progress periodically)

### 4. Post-Build Cleanup
Aider may create spurious files from code blocks in README/docs:
- Files named like shell commands (`npm install`, `cd project-name`)
- Files named like directory tree lines (`└── README.md`)
- Remove these before committing

### 5. Local Testing
```bash
test -f README.md        # README exists
test -f package.json     # Package config exists
npm install              # Dependencies install
npm run build            # Project builds
test -d dist             # Build output exists
```

### 6. Fix Common Issues
- **TypeScript `Uint8Array` / `BlobPart` error:** Cast with `as BlobPart`
- **pdfjs-dist worker path:** May need CDN URL or vite plugin
- **Missing .gitignore:** Create with node_modules/, dist/, .aider*

### 7. GitHub Push
```bash
gh repo create <org>/foundry-<date>-<project> \
  --private \
  --description "<description>" \
  --source=. \
  --remote=origin \
  --push
```

### 8. Output Files

#### 8.1 Create `build.json`
```json
{
  "schema_version": 1,
  "date": "YYYY-MM-DD",
  "project_name": "project-name",
  "status": "success|partial|failed|local_only",
  "repo_url": "https://github.com/org/repo",
  "build_duration_seconds": 420,
  "test_results": {
    "readme_exists": true,
    "dependencies_installed": true,
    "build_succeeded": true
  },
  "file_count": 12,
  "lines_of_code": 850,
  "aider_cost_usd": 0.47
}
```

#### 8.2 Update History ✨ NEW in v2

After a **successful build** (status: `success` or `partial`), append to `~/.openclaw/workspace/foundry/history.json`:

```bash
cd ~/projects/the-foundry
python3 << 'EOF'
import json
import sys
from datetime import datetime
from src.dedup import add_build_to_history

# Read spec.json to get the original trend title
spec_path = '~/.openclaw/workspace/foundry/YYYY-MM-DD/spec.json'
with open(spec_path) as f:
    spec = json.load(f)

# Read build.json for repo URL and status
build_path = '~/.openclaw/workspace/foundry/YYYY-MM-DD/build.json'
with open(build_path) as f:
    build = json.load(f)

# Only append to history if build succeeded
if build['status'] not in ['success', 'partial']:
    print(f"Build status: {build['status']} - NOT adding to history")
    sys.exit(0)

# Extract source from trend (if available)
# This should be in the original trends-summary.json
source = 'unknown'
trend_id = spec.get('selected_trend_id')
if trend_id:
    trends_path = '~/.openclaw/workspace/foundry/YYYY-MM-DD/trends-summary.json'
    try:
        with open(trends_path) as f:
            trends_data = json.load(f)
            matching_trend = next((t for t in trends_data['trends'] if t['id'] == trend_id), None)
            if matching_trend:
                source = matching_trend.get('source', 'unknown')
    except FileNotFoundError:
        pass

# Build history entry
history_entry = {
    'date': build['date'],
    'project_name': build['project_name'],
    'title': spec.get('selected_trend_title', ''),
    'repo_url': build.get('repo_url', ''),
    'status': build['status'],
    'source': source
}

# Add to history (keywords will be auto-extracted)
history_path = '~/.openclaw/workspace/foundry/history.json'
add_build_to_history(history_path, history_entry)

print(f"✓ Added {build['project_name']} to history.json")
EOF
```

**Why update history?**
- Prevents duplicate builds in future scans
- Tracks what we've built over time
- Enables metrics and portfolio analysis

**What about rejections?**
- Spec Writer rejections are NOT added to history (they're in spec.json with decision: "rejected")
- Only successful/partial builds are added
- This keeps history.json focused on what we've actually built

### 9. Failure Handling
| Scenario | Status | Action | Add to History? |
|----------|--------|--------|-----------------|
| Aider completes, tests pass | `success` | Push to GitHub | ✅ Yes |
| Aider completes, build fails | `success_with_warnings` | Push anyway | ✅ Yes |
| Aider times out (≥60% done) | `partial` | Push what exists | ✅ Yes |
| Aider times out (<60% done) | `failed` | Don't push | ❌ No |
| Aider crashes | `failed` | Log error, don't push | ❌ No |
| GitHub creation fails | `local_only` | Keep code locally | ✅ Yes (if code is good) |

**Rule:** Add to history if we have working code, even if GitHub push failed or build warnings exist.

## Lessons Learned (v1)
1. Aider creates files from markdown code blocks in README — clean up before commit
2. TypeScript strict mode may cause `Uint8Array` type errors with `Blob` — easy fix
3. OpenRouter API key works well for aider when Anthropic key isn't directly available
4. Single-message mode (`--message`) is fast and reliable for batch builds
5. Build completes in ~7 minutes for a mid-complexity web app (not 4-5 hours as estimated)
6. Cost: ~$0.47 per build with Claude Sonnet 4.5 via OpenRouter

---

**Status:** v2 — Implements Epic 2.1 (append to history.json)
**Last Updated:** 2026-02-26
