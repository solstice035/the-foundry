# Instructions for Claude/AI Agents

**Project:** The Foundry 🏭  
**Purpose:** Autonomous overnight app factory  
**Owner:** Nick Solly (jeeves@jeevesbot.io)

---

## What This Project Is

The Foundry is a multi-agent system that:
1. **The Blacksmith** (foundry-blacksmith) coordinates the overnight pipeline
2. **Trend Scout** (foundry-scout) scans trending developer pain points (Reddit, HN) at midnight
3. **Spec Writer** (foundry-spec) selects one buildable trend
4. **Builder** (foundry-builder) builds an MVP overnight using aider + LLM
5. Pushes to GitHub and delivers a morning briefing at 8am

**Status:** Design complete, awaiting implementation approval  
**Timeline:** 16 weeks (3 phases, 16 epics)  
**Cost:** ~$42-57/month when fully operational

---

## If You're Working on This Project

### Before You Start

1. **Read the design docs:** All in `docs/` (symlinked to Obsidian)
   - Start with `docs/README - Status & Next Steps.md`
   - Then `docs/Implementation Plan - Epics.md` for the full breakdown
   - Agent-specific: `docs/Agent Architecture.md`

2. **Check the War Room:** http://localhost:3333
   - Filter by project: "The Foundry"
   - See which epics are in progress
   - Don't duplicate work

3. **Understand the architecture:**
   - 1 coordinator: The Blacksmith (foundry-blacksmith, Sonnet) spawns and monitors all agents
   - 3 core agents: foundry-scout (Haiku) → foundry-spec (Sonnet) → foundry-builder (Sonnet + aider)
   - 3 phases: Core Pipeline → Feedback Loop → Social Amplification
   - 16 epics total, currently all in backlog

### Project Structure

```
the-foundry/
├── docs/              Symlink to Obsidian design docs (read-only via git)
├── src/               Agent task prompts, Python utilities, orchestration code
├── scripts/           Deployment scripts, testing harnesses, admin tools
├── config/            Agent configs, cron schedules, schema definitions
├── tests/             Agent testing, validation, mock data
└── README.md          Project overview
```

### Code Guidelines

**Agent Task Prompts (src/):**
- Write task strings for `sessions_spawn` calls
- Include full context (no assumptions about what the agent knows)
- Reference design docs explicitly (e.g., "See Builder-Coding-Agent Design.md")
- Test prompts 3-5 times with same input before committing
- Document expected outputs (schema, file paths)

**Python Utilities (src/):**
- Type hints required (`from typing import ...`)
- Docstrings for all functions
- Error handling for network calls, file I/O
- No hardcoded secrets (use environment variables)
- Test coverage for critical paths

**Configuration (config/):**
- YAML for agent configs, cron schedules
- JSON for schemas (with `schema_version` field)
- Comments explaining non-obvious settings
- Validate before committing (schema checkers)

**Testing (tests/):**
- Mock external APIs (HN, Reddit, GitHub)
- Test failure modes (timeouts, rate limits, bad data)
- Integration tests for multi-agent handoffs
- Run before every commit

### What NOT to Do

❌ **Don't skip the design docs** — they exist for a reason  
❌ **Don't hardcode secrets** — use env vars or 1Password  
❌ **Don't commit runtime data** — .gitignore handles this  
❌ **Don't break the multi-agent flow** — agents are sequential, not parallel (Phase 1)  
❌ **Don't add dependencies without asking** — keep it lightweight  
❌ **Don't deploy without testing** — test locally first, dry run in isolation

### Git Workflow

**Branching:**
- `main` branch is the source of truth
- Feature branches: `epic/1.1-trend-scout-data` (per epic)
- Bug fixes: `fix/description`
- Experiments: `exp/description`

**Commits:**
- One epic = one or more focused commits
- Commit message format:
  ```
  Epic 1.1: Trend Scout data collection
  
  - Implemented HN Algolia API integration
  - Added Reddit JSON endpoint fetching (5 subreddits)
  - Per-source timeout enforcement (5 min)
  - Tests: individual source validation
  
  Acceptance criteria: 6/6 complete
  ```

**Pull Requests:**
- Not required (solo project, Nick reviews via War Room)
- If used: reference epic number, link design doc, list acceptance criteria

### Testing Strategy

**Before committing any agent code:**

1. **Unit test:** Individual functions (keyword extraction, normalization, scoring)
2. **Mock test:** Agent with mocked API responses
3. **Live test:** Agent with real APIs (rate limit aware)
4. **Integration test:** Full pipeline (Scout → Spec → Builder)
5. **Failure test:** Timeouts, bad data, source failures
6. **Consistency test:** Run 3-5 times, verify output similarity

**Acceptance criteria must be verifiable** — write tests that check them.

### When You Get Stuck

1. **Check the design docs** — likely already answered
2. **Review the independent review** (`docs/Independent review.md`) — common issues addressed
3. **Look at `docs/Response to Review.md`** — explains design decisions
4. **Ask Nick** — he's the product owner, final say on all decisions

### Voice & Tone for Agent Prompts

**The Foundry agents should:**
- Be direct and specific (no fluff)
- Include explicit schemas and output paths
- Document failure modes and recovery
- Reference design docs by name
- Use concrete examples (not abstract descriptions)

**Example of good agent prompt:**
```
You are the Trend Scout for The Foundry.

Mission: Scan HN and Reddit for trending developer pain points.

Data sources:
1. HN Algolia API: http://hn.algolia.com/api/v1/search?tags=story&numericFilters=created_at_i>{unix_24h_ago}
2. Reddit JSON: https://www.reddit.com/r/programming/hot.json?limit=25

For each source:
- Timeout: 5 minutes
- If fails: log error, continue with remaining sources
- Minimum: 1 of 2 sources must succeed

Output: ~/.openclaw/workspace/foundry/YYYY-MM-DD/trends-raw.json
Schema: See docs/Deep Dive - Trend Research.md, section "Common Trend Schema"

If you encounter rate limits, document in output and continue.
```

**Example of bad agent prompt:**
```
Scan the web for trending topics and return a JSON file with the results.
```

### Documentation Discipline

**From AGENTS.md:**
> Verify before documenting. Never assume schemas, APIs, or column names — check the source of truth first. LLMs hallucinate plausible-sounding details with total confidence. If you document something wrong, every agent downstream inherits the mistake.

**For The Foundry specifically:**
- All JSON schemas must include `schema_version` field
- All file paths must be absolute or explicitly relative
- All timeouts must be specified in seconds
- All API endpoints must be tested before documenting
- All error messages must be actionable

### Context for This Project

**Why The Foundry exists:**
- Nick wants autonomous overnight builds from trending topics
- Multi-agent pipeline ensures quality (Scout finds, Spec evaluates, Builder builds)
- Learning loops prevent duplicates and optimize over time
- Social amplification shares successful builds

**Design philosophy:**
- Agents are specialized, not generalist
- Each agent has clear inputs/outputs (file-based handoffs)
- Failures degrade gracefully (partial success > full failure)
- Everything is observable (state files, logs, metrics)
- Cost is capped (concrete timeouts, model selection)

**What success looks like:**
- First autonomous night within 2 weeks of starting Epic 1.1
- 5 consecutive nights without manual intervention (Phase 1 exit criteria)
- Zero duplicate builds after Phase 2
- Content automation reduces Nick's posting time to <15 min/day (Phase 3)

---

## Emergency Contacts

**Project Owner:** Nick Solly  
**Primary Agent:** Jeeves (main OpenClaw session)  
**War Room:** http://localhost:3333  
**Documentation:** `~/projects/the-foundry/docs/`  
**Workspace:** `~/.openclaw/workspace/foundry/` (runtime data)

---

## Quick Reference

**Design docs to read first:**
1. `README - Status & Next Steps.md` — current state
2. `Implementation Plan - Epics.md` — all 16 epics
3. `Agent Architecture.md` — agent specs
4. `Builder-Coding-Agent Design.md` — most complex component
5. `Independent review.md` — comprehensive review

**Key decisions:**
- Coordinator: The Blacksmith (foundry-blacksmith, Sonnet) - orchestrates entire pipeline
- Models: Haiku (foundry-scout), Sonnet (foundry-spec + foundry-builder)
- Sources: HN, Reddit (5 subs), X (3 searches) in Phase 1
- Builder tool: aider (not pty-based Claude Code)
- Timing: 00:00 (Blacksmith spawns) → 00:00-00:45 (Scout) → 00:45-01:30 (Spec) → 01:30-07:00 (Builder) → 08:00 (Briefing)
- Dedup: 14-day window, keyword overlap, Jaccard similarity

**Don't change these without asking Nick.**

---

**Last Updated:** 2026-02-18  
**Status:** Design complete, awaiting implementation approval
