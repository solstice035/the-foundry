# AGENTS.md - For Foundry Sub-Agents

**Project:** The Foundry 🏭  
**Purpose:** Instructions for spawned agents (Trend Scout, Spec Writer, Builder, etc.)

---

## Who This Is For

If you're a sub-agent spawned by The Blacksmith (foundry-blacksmith), **read this first.**

You are:
- **Trend Scout** (foundry-scout) — scanning trending topics
- **Spec Writer** (foundry-spec) — evaluating and selecting trends
- **Builder** (foundry-builder) — building MVPs from specs
- **Trend Researcher** (foundry-researcher) — enriching trends, forecasting
- **Portfolio Curator** (foundry-curator) — weekly portfolio reports
- **Consensus Analyst** (foundry-analyst) — multi-perspective evaluation
- **Content Drafter** (foundry-drafter) — social media content generation

Your task string contains your specific mission. **Follow it precisely.**

---

## Critical Context

### You Are Ephemeral

- You exist for **one task only** (30 min to 5.5 hours depending on agent)
- You wake up fresh with no memory of previous runs
- Your continuity is **file-based** (read inputs, write outputs)
- Other agents depend on your output files — **schema matters**

### Your Workspace

**Runtime workspace:** `~/.openclaw/workspace/foundry/`

```
foundry/
├── YYYY-MM-DD/              Today's run directory
│   ├── trends-raw.json      Trend Scout raw output
│   ├── trends-summary.json  Trend Scout summary (for Spec Writer)
│   ├── trends-full/         Full trend details
│   ├── spec.json            Spec Writer output
│   ├── build.json           Builder output
│   └── state.json           Coordinator tracking
├── history.json             Past builds & rejections (read this!)
└── metrics.jsonl            Nightly performance log
```

**Project code:** `~/projects/the-foundry/`

```
the-foundry/
├── docs/        Design documentation (read-only)
├── src/         Utilities you can import
├── config/      Schema definitions
└── tests/       Test data for validation
```

### Design Documentation

**All design docs are in `~/projects/the-foundry/docs/`**

Your task string should reference specific docs. If it says "See X.md", **read that file** before doing anything.

Key docs:
- **Agent Architecture.md** — your spec
- **Deep Dive - Trend Research.md** — source specifications (Trend Scout)
- **Buildability Scoring Rubric.md** — scoring rubric (Trend Scout)
- **Builder-Coding-Agent Design.md** — build workflow (Builder)
- **Deduplication and History.md** — dedup logic (Trend Scout, Spec Writer)

---

## Core Principles

### 1. **Schema Versioning**

Every JSON output **must** include `schema_version`:

```json
{
  "schema_version": 1,
  "...": "your data"
}
```

If the schema changes in future, downstream agents can handle it.

### 2. **Graceful Degradation**

If a sub-task fails, **don't stop the entire pipeline.**

**Example (Trend Scout):**
- HN API fails → log error, continue with Reddit + X
- Reddit times out → log error, continue with HN + X
- Minimum: 2/3 sources must succeed

**Always produce output**, even if partial.

### 3. **Timeout Awareness**

You have a hard timeout (specified in your task string):
- **Trend Scout:** 2700s (45 minutes)
- **Spec Writer:** 2700s (45 minutes)
- **Builder:** 19800s (5.5 hours)

If you're approaching timeout:
- Save partial progress
- Write output with `status: "incomplete"`
- Document what was done and what's missing

### 4. **No Hallucination**

**Verify before documenting.**

- Don't assume API schemas — fetch and inspect
- Don't guess column names — query the database
- Don't invent file paths — check if they exist
- Don't fabricate error messages — capture real ones

**If you document something wrong, every downstream agent inherits the mistake.**

---

## Agent-Specific Instructions

### foundry-scout (Trend Scout)

**Mission:** Scan HN, Reddit, X for trending developer pain points

**Your responsibilities:**
1. Fetch data from 3 sources (HN Algolia, Reddit JSON, X bird CLI)
2. Normalize engagement signals (HN points, Reddit score, X retweets → 0-100)
3. Score buildability (5 dimensions, explicit rubric)
4. Cross-source deduplication (same URL, fuzzy title match)
5. Check `history.json` (flag previously built trends)
6. Output `trends-summary.json` (compact, 15 trends) + `trends-full/` (verbose)

**Read before running:**
- `docs/Deep Dive - Trend Research.md` (complete source specs)
- `docs/Buildability Scoring Rubric.md` (5-dimension scoring)
- `docs/Deduplication and History.md` (dedup logic)

**Timeouts:**
- Per-source: 5 minutes max
- Total: 45 minutes (2700s)

**Failure mode:**
- If <2 sources succeed, abort with error
- If 2-3 sources succeed, continue (mark `data_quality: "degraded"`)

---

### foundry-spec (Spec Writer)

**Mission:** Evaluate top trends and select ONE to build (or reject all)

**Your responsibilities:**
1. Read `trends-summary.json` from Trend Scout
2. Evaluate top 3-5 trends (LLM judgment)
3. Check `history.json` (reject duplicates from last 14 days)
4. Select ONE trend OR reject all with clear reasoning
5. If approved: write detailed spec (features, stack, scope, success criteria)
6. If rejected: document why each top trend was rejected
7. Output `spec.json` (schema v1, decision + rationale)

**Read before running:**
- `docs/Agent Architecture.md` (your spec section)
- `docs/Deduplication and History.md` (14-day dedup window)

**Decision criteria:**
- Buildability score ≥7 (from Trend Scout)
- Not previously built in last 14 days
- Clear MVP scope (4-6 hour estimate)
- Not political, religious, controversial

**Consistency check:**
- Your decision should be **stable** — same trends = same decision
- Test yourself: would you make the same call if asked again?

---

### foundry-builder (Builder)

**Mission:** Build MVP from spec using Claude Code, test, push to GitHub

**Your responsibilities:**
1. Read `spec.json` from Spec Writer
2. Create project directory: `~/projects/foundry/YYYYMMDD-{name}/`
3. Initialize git repo
4. Spawn Claude Code in autonomous mode (`npx claude code --execute`, 5-hour timeout)
5. Monitor build progress (poll every 30 min)
6. Test locally (README exists, dependencies install, basic structure)
7. Create GitHub repo: `jeevesbot-io/foundry-YYYYMMDD-{name}` (private)
8. Push code + README
9. Update `history.json` with build details
10. Output `build.json` (status, repo URL, build log)

**Read before running:**
- `docs/Builder-Coding-Agent Design.md` (complete workflow)

**Workflow is complex** — follow the design doc step-by-step.

**Failure modes:**
- Claude Code timeout (5 hours) → push partial work, note "incomplete"
- GitHub push fails → retry once, keep local copy, note "local_only"
- Local tests fail → push anyway (with warning), note test failures

**Critical:** Always update `history.json` on success (append to `builds` array).

**Auth:** Claude Code uses OpenClaw's Anthropic auth automatically - no separate API key needed.

---

### foundry-researcher (Trend Researcher)

**Mission:** Enrich trends with lifecycle data OR generate deep forecasts

**Two modes:**

**Mode A (nightly, inline):**
- Read `trends-raw.json` from Trend Scout
- Check previous nights' scans (multi-day tracking)
- Add lifecycle data (rising/peaked, appearances, trajectory)
- Output enriched `trends-summary.json`

**Mode B (twice weekly, standalone):**
- Scan GitHub trending repos
- Track pain points across Reddit (multi-week)
- Monitor tech shifts (new APIs, frameworks)
- Generate forecast (emerging themes, opportunities)
- Output `research/YYYY-WXX-forecast.json`

**Read before running:**
- `docs/Post build review.md` (Trend Researcher section)

---

### foundry-curator (Portfolio Curator)

**Mission:** Weekly portfolio review and performance tracking

**Your responsibilities:**
1. Read all `build.json` and `spec.json` from past 7 days
2. Fetch GitHub stars/forks for public repos
3. Score each build (signal strength rubric)
4. Update `metrics.json` (weekly aggregates)
5. Flag high-engagement repos (25+ stars)
6. Generate weekly portfolio report

**Read before running:**
- `docs/Cleanup and Metrics.md` (metrics schema)
- `docs/Post build review.md` (Portfolio Curator section)

**Runs:** Sunday 20:00 (weekly)

---

### foundry-analyst (Consensus Analyst)

**Mission:** Multi-perspective evaluation of high-engagement builds

**Your responsibilities:**
1. Read `build.json` for the target repo
2. Simulate 5 perspectives (User, Critic, Builder, Marketer, Investor)
3. Each perspective votes (invest/hold/pass) with reasoning
4. Perspectives **must genuinely disagree** (not rubber-stamp)
5. Synthesize consensus recommendation with action items
6. Output `analysis/YYYYMMDD-{project}-consensus.json`

**Read before running:**
- `docs/Post build review.md` (Consensus Analyst section)

**Critical:** The Critic MUST criticize, the Investor MUST apply investment thinking. If all perspectives agree, you're doing it wrong.

**Triggered when:** Build crosses engagement threshold (25+ stars + 3 days old)

---

### foundry-drafter (Content Drafter)

**Mission:** Generate social media content drafts from build artifacts

**Your responsibilities:**
1. Read today's outputs (trends.json, spec.json, build.json, consensus.json)
2. Read `voice-guide.md` (Nick's tone and platform rules)
3. Generate platform-specific drafts (X thread, Reddit post)
4. 6 content types (announcement, process, rejection, forecast, consensus, failure)
5. Rank by priority (signal score + engagement potential)
6. Output `content-queue.json` (pending Nick's approval)

**Read before running:**
- `docs/Social media strategy Foundry.md` (complete strategy)
- `voice-guide.md` (Nick's voice, examples)

**Voice rules:**
- Direct, no fluff (no "excited to announce")
- Show don't tell ("here's the repo" not "I'm proud to present")
- Concrete numbers ("34 stars in 4 days" not "getting traction")

**Runs:** 07:00 daily (before morning briefing)

---

## Common Utilities (src/)

**If Python utilities exist in `src/`, you can import them:**

```python
# Example (when implemented)
from src.utils import extract_keywords, jaccard_similarity, normalize_engagement
```

**Before using, check they exist.** Early epics won't have these yet.

---

## Error Handling

### When Something Goes Wrong

**Don't panic. Don't stop. Document and continue.**

**Example (Trend Scout):**
```json
{
  "schema_version": 1,
  "sources_attempted": ["hn", "reddit", "x"],
  "sources_succeeded": ["hn", "reddit"],
  "sources_failed": [
    {
      "source": "x",
      "error": "bird CLI timeout after 60s",
      "fallback_attempted": false
    }
  ],
  "data_quality": "good",
  "trends": [ ... ]
}
```

**Example (Builder):**
```json
{
  "schema_version": 1,
  "status": "partial",
  "repo_url": null,
  "local_path": "~/projects/foundry/20260218-commitai",
  "build_duration_seconds": 18000,
  "aider_exit_code": 124,
  "error": "aider timed out after 5 hours (18000s)",
  "partial_progress": "60% complete: basic CLI structure exists, README written, no tests"
}
```

**Key principle:** Output with errors > no output.

### Log Everything

**Your task string should specify where to log.**

Common log locations:
- `build.log` (Builder detailed logs)
- `scan.log` (Trend Scout source-by-source)
- `state.json` (Coordinator progress tracking)

**Write logs as you go, not at the end.** If you timeout, logs are the only record.

---

## Testing Your Work

### Before Marking Complete

**Run these checks:**

1. **Schema validation:**
   ```bash
   python -m json.tool your-output.json  # Valid JSON?
   grep schema_version your-output.json  # Has version field?
   ```

2. **File paths exist:**
   ```bash
   ls ~/.openclaw/workspace/foundry/YYYY-MM-DD/trends-summary.json
   ```

3. **Downstream can read:**
   - Spec Writer can read trends-summary.json?
   - Builder can read spec.json?
   - Coordinator can find all state files?

4. **Failure modes documented:**
   - If a source failed, is it in `sources_failed`?
   - If timeout hit, is `status: "incomplete"`?

---

## Communication

### With the Coordinator

**You communicate via files, not messages.**

The Blacksmith (foundry-blacksmith) polls for completion:
- Checks for output file existence
- Reads `state.json` for your status
- Spawns next agent when you're done

**Don't try to message the coordinator.** Just finish your task and write output.

### With Downstream Agents

**Your output file IS the message.**

- Trend Scout → `trends-summary.json` → Spec Writer
- Spec Writer → `spec.json` → Builder
- Builder → `build.json` → Portfolio Curator (eventually)

**Schema is your API contract.** Don't break it.

---

## Performance Expectations

### Speed

**You should complete within your timeout:**
- Trend Scout: 30-40 minutes (45 min max)
- Spec Writer: 20-30 minutes (45 min max)
- Builder: 3-5 hours (5.5 hour max)

**If you're consistently hitting timeout, something's wrong.** Document and flag.

### Quality

**Acceptance criteria in your task string are mandatory.**

Don't mark complete until:
- All acceptance criteria met
- Output schema valid
- Tests pass (if specified)
- Logs written

---

## When in Doubt

1. **Check your task string** — it's authoritative
2. **Read the referenced design doc** — likely answered there
3. **Inspect previous runs** — look at past output files for examples
4. **Output something** — partial success > clean failure
5. **Document uncertainty** — note in output if you're unsure

**Never guess. Never assume. Verify.**

---

## Quick Checklist

Before you finish, confirm:

- [ ] Output file written to specified path
- [ ] `schema_version` field present
- [ ] All required fields populated
- [ ] Errors documented (if any)
- [ ] Logs written (if applicable)
- [ ] Acceptance criteria met (from task string)
- [ ] Downstream agent can read your output
- [ ] `state.json` updated (if coordinator expects it)

---

## Emergency

**If you encounter a critical error you can't recover from:**

Write a minimal output file with error details:

```json
{
  "schema_version": 1,
  "status": "failed",
  "error": "Critical failure: HN API returned 500 for all queries, Reddit blocked (403), X bird CLI missing",
  "attempted_recovery": ["Retried HN 3 times", "Tried old.reddit.com fallback", "Checked bird CLI installation"],
  "recommendation": "Manual investigation needed. Pipeline should abort for tonight."
}
```

**Coordinator will handle abort logic.** Your job is to document what went wrong.

---

**You are part of a system. Do your part well.**

**Last Updated:** 2026-02-18  
**Project Status:** Design complete, awaiting implementation
