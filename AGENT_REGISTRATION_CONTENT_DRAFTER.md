# Agent Registration for Epic 3.2

## Content Drafter Agent

**Agent ID:** `content-drafter`  
**Model:** `anthropic/claude-sonnet-4-5`  
**Thinking:** Medium  
**Timeout:** 1800 seconds (30 minutes)  
**Purpose:** Generate platform-ready social media content drafts from build pipeline outputs

### Registration Required

Add to OpenClaw agent configuration:

```toml
[agents.content-drafter]
model = "anthropic/claude-sonnet-4-5"
thinking = "medium"
timeout = 1800
description = "Generate platform-specific social media content drafts"
workspace = "~/.openclaw/workspace/foundry"
sessionTarget = "isolated"
cleanup = "delete"  # Ephemeral, output is in content-queue.json
```

### Task Prompt Location

`~/projects/the-foundry/src/prompts/content-drafter-v1.md`

### Invocation Example

```bash
# Daily at 07:00 (before morning briefing)
sessions_spawn(
  task="Run Content Drafter. Read src/prompts/content-drafter-v1.md and generate social content drafts from today's pipeline outputs.",
  agentId="content-drafter",
  mode="run",
  runTimeoutSeconds=1800
)
```

### Input Files

**Required:**
- `docs/voice-guide.md` — Canonical voice reference
- `~/.openclaw/workspace/foundry/YYYY-MM-DD/trends-summary.json`
- `~/.openclaw/workspace/foundry/YYYY-MM-DD/spec.json`
- `~/.openclaw/workspace/foundry/YYYY-MM-DD/build.json`

**Optional:**
- `~/.openclaw/workspace/foundry/YYYY-MM-DD/consensus.json`
- `~/.openclaw/workspace/foundry/forecast.json`
- `~/.openclaw/workspace/foundry/history.json`
- `~/.openclaw/workspace/foundry/social/content-history.json`
- `~/.openclaw/workspace/foundry/social/voice-patterns.json`

### Output Files

**Primary:**
- `~/.openclaw/workspace/foundry/social/content-queue.json`

**Schema:**
- `~/projects/the-foundry/config/schemas/content-queue.schema.json`

### Cron Schedule

```yaml
cron:
  jobs:
    - name: "Autonomous Builds - Content Drafting"
      schedule: { kind: cron, expr: "0 7 * * *", tz: Europe/London }
      payload: { 
        kind: systemEvent, 
        text: "Run Content Drafter. Read src/prompts/content-drafter-v1.md and generate social content drafts from today's pipeline outputs."
      }
      sessionTarget: main
      enabled: true
```

### Success Criteria

- [ ] Agent generates drafts for all 6 content types
- [ ] Drafts match voice-guide.md tone (>60% approval rate)
- [ ] Platform-specific formatting correct
- [ ] Priority ranking makes sense
- [ ] Top 1-2 drafts appear in morning briefing
- [ ] Visual suggestions included when appropriate

### Dependencies

**Epic dependencies:**
- Epic 3.1: voice-guide.md must exist (bootstrap version acceptable)
- Phase 1: Build pipeline operational (generates source artifacts)

**File dependencies:**
- `docs/voice-guide.md` (created in Epic 3.1 or bootstrapped)
- Daily pipeline outputs (trends, spec, build)
- Schema validation (content-queue.schema.json)

### Cost Estimate

**Daily run:**
- Input: ~15-20K tokens (reading pipeline outputs + voice guide)
- Output: ~10-15K tokens (2-3 drafts with platform variants)
- Model: Sonnet 4.5 at medium thinking
- Est. cost: ~$0.09/day = ~$2.70/month

**Peak days (multiple content opportunities):**
- Up to $0.15/day if generating 4-5 drafts

**Monthly estimate:** $2.70-4.50/month

### Testing Plan

See `tests/test_content_drafter.py` for test suite.

**Manual testing:**
1. Run on 3-5 existing builds from Phase 1
2. Test all 6 content types
3. Verify voice matching (Nick approval)
4. Check platform formatting
5. Validate schema compliance

**Expected results:**
- >60% approval rate from Nick (minimal edits)
- All 6 content types successfully generated
- No schema validation errors
- Estimated engagement scores reasonable

---

**NOTE:** Agent registration must be done in OpenClaw's configuration system before Epic 3.2 can be marked complete. This document serves as the specification for manual registration.
