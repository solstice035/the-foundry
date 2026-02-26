# Agent Registration for Epic 2.3

## Trend Researcher Agent

**Agent ID:** `trend-researcher`  
**Model:** `anthropic/claude-sonnet-4-5`  
**Thinking:** Medium  
**Timeout:** 900 seconds (15 minutes)  
**Purpose:** Lifecycle tracking and trend enrichment (Mode A)

### Registration Required

Add to OpenClaw agent configuration:

```toml
[agents.trend-researcher]
model = "anthropic/claude-sonnet-4-5"
thinking = "medium"
timeout = 900
description = "Trend lifecycle tracking and enrichment (Mode A)"
workspace = "~/.openclaw/workspace/foundry"
```

### Task Prompt Location

`~/projects/the-foundry/src/prompts/trend-researcher-mode-a-v1.md`

### Invocation Example

```bash
# Spawned by foundry-blacksmith at 00:45
sessions_spawn(
  task="Run Trend Researcher Mode A. Read src/prompts/trend-researcher-mode-a-v1.md...",
  agentId="trend-researcher",
  mode="run",
  runTimeoutSeconds=900
)
```

---

**NOTE:** Agent registration must be done in OpenClaw's configuration system before Epic 2.3 can be marked complete. This document serves as the specification for manual registration.
