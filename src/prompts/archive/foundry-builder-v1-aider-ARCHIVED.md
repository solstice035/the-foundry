# Foundry Builder v1 — Aider Integration Workflow

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

### 8. Output
Create `build.json` with:
- Status (success/partial/failed/local_only)
- Repo URL
- Build duration
- Test results
- File count, LOC
- Aider cost

Update `history.json` with build record.

## Failure Handling
| Scenario | Status | Action |
|----------|--------|--------|
| Aider completes, tests pass | `success` | Push to GitHub |
| Aider completes, build fails | `success_with_warnings` | Push anyway |
| Aider times out (≥60% done) | `partial` | Push what exists |
| Aider times out (<60% done) | `failed` | Don't push |
| Aider crashes | `failed` | Log error, don't push |
| GitHub creation fails | `local_only` | Keep code locally |

## Lessons Learned (v1)
1. Aider creates files from markdown code blocks in README — clean up before commit
2. TypeScript strict mode may cause `Uint8Array` type errors with `Blob` — easy fix
3. OpenRouter API key works well for aider when Anthropic key isn't directly available
4. Single-message mode (`--message`) is fast and reliable for batch builds
5. Build completes in ~7 minutes for a mid-complexity web app (not 4-5 hours as estimated)
6. Cost: ~$0.47 per build with Claude Sonnet 4.5 via OpenRouter
