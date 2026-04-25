# Foundry Builder v4 — Claude Code via ACP

## Overview
Takes a `spec.json` from the Architect and builds a production-ready MVP using **Claude Code via ACP** (not aider). Claude Code is free under Claude Max — zero OpenRouter cost.

## Prerequisites
- OpenClaw ACP plugin active (`agentId: "claude"`)
- `gh` CLI authenticated for GitHub operations
- `git` configured with `user.name` and `user.email`

## Workflow

### 1. Setup Project Directory
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
- Must-have features (with implementation detail)
- Nice-to-have features
- Out of scope items
- Success criteria
- Expected file structure

Build a comprehensive task prompt that covers all of the above, instructs Claude Code to:
- Implement `must_have` features fully
- Add basic tests (smoke tests at minimum)
- Write a comprehensive README
- Set up a proper `.gitignore`

### 3. Spawn Claude Code via ACP

Use `sessions_spawn` with ACP runtime:

```json
{
  "runtime": "acp",
  "agentId": "claude",
  "mode": "run",
  "cwd": "~/projects/foundry/<DATE>-<PROJECT_NAME>",
  "task": "<full build prompt>",
  "runTimeoutSeconds": 28800
}
```

**Key parameters:**
- `runtime: "acp"` — routes through OpenClaw ACP, not subagent
- `agentId: "claude"` — Claude Code harness
- `mode: "run"` — one-shot build (not persistent session)
- `cwd` — set to the project directory so Claude Code has the right context
- `runTimeoutSeconds: 28800` — 8 hours max (builds typically complete in 10–60 min)

**Cost:** FREE — Claude Code uses the Claude Max subscription, not the API.

### 4. Build Prompt Template

```
You are building an MVP for the following project. Work autonomously — create all files needed.

## Project: <NAME>

<description>

## Tech Stack
<stack>

## Must-Have Features (implement all)
<for each feature>
- <feature name>: <detailed requirements>

## Nice-to-Have (only if must-haves are complete and time permits)
<list>

## Out of Scope
<list — do NOT implement these>

## Success Criteria
<criteria from spec>

## Quality Requirements
- Working code that runs without manual fixes
- README with: what it does, install steps, usage examples, example output
- Basic tests (smoke tests minimum — does it run? does core feature work?)
- Clean .gitignore (node_modules/, dist/, .env, etc.)
- No hardcoded secrets or API keys

## File Structure
<expected structure if specified in spec>

When done, output a brief summary of what was built, any challenges, and what a v2 would include.
```

### 5. Post-Build Steps

After ACP session completes:

```bash
# Verify core deliverables exist
test -f README.md
test -f .gitignore

# Run basic smoke tests if applicable
npm install && npm test  # or equivalent for the stack

# Create private GitHub repo and push
gh repo create jeevesbot-io/foundry-<DATE>-<PROJECT_NAME> \
  --private \
  --description "<description>" \
  --source=. \
  --remote=origin \
  --push
```

### 6. Output: `build.json`

Write to `~/.openclaw/workspace/foundry/YYYY-MM-DD/build.json`:

```json
{
  "schema_version": 2,
  "date": "YYYY-MM-DD",
  "project_name": "project-name",
  "status": "success|partial|failed|local_only",
  "repo_url": "https://github.com/jeevesbot-io/foundry-YYYYMMDD-name",
  "demo_url": null,
  "build_tool": "claude-code-acp",
  "build_duration_seconds": 0,
  "test_results": {
    "readme_exists": true,
    "dependencies_installed": true,
    "build_succeeded": true
  },
  "file_count": 0,
  "lines_of_code": 0,
  "cost_usd": 0,
  "challenges": [],
  "next_steps": []
}
```

Note: `cost_usd` is always 0 — Claude Code is free under Claude Max.

### 7. Update History

Same as v2/v3 — append to `~/.openclaw/workspace/foundry/history.json` on success/partial.

### 8. Failure Handling

| Scenario | Status | Action |
|----------|--------|--------|
| Claude Code completes, tests pass | `success` | Push to GitHub, update history |
| Claude Code completes, build fails | `success_with_warnings` | Push anyway, note in build.json |
| ACP session times out (≥60% done) | `partial` | Push what exists, update history |
| ACP session times out (<60% done) | `failed` | Don't push, log error |
| ACP unavailable | `failed` | Log error, report to Blacksmith |
| GitHub push fails | `local_only` | Keep code, update history |

**Never fall back to aider.** If ACP is unavailable, report failure to the Blacksmith.

## Migration Notes

This replaces `foundry-builder-v2.md` and `foundry-builder-v3-enhanced.md`.

- **Old (aider):** `aider --yes --model openrouter/anthropic/claude-sonnet-4-5 --message "..."` — costs $0.40–$5.00/build via OpenRouter
- **New (Claude Code):** `sessions_spawn(runtime="acp", agentId="claude")` — **FREE**

The quality ceiling is higher with Claude Code — it has access to the full filesystem, can run tests, install deps, and iterate — without the per-token cost.

---

**Status:** v4 — Claude Code via ACP (replaces aider)
**Created:** 2026-03-06
