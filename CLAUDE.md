# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**The Foundry** is an autonomous overnight app factory -- a multi-agent pipeline that scans trending developer pain points, selects one buildable idea per night, builds an MVP while the owner sleeps, pushes to GitHub, and delivers a morning briefing at 08:00.

**Owner:** Nick Solly (jeeves@jeevesbot.io)
**Status:** Phase 1 complete (5/5 epics), Phase 2 complete (6/6 epics), Phase 3 in progress (Epic 3.1a complete)
**Cost:** ~$42-57/month when fully operational

## Tech Stack

- **Language:** Python 3.13+
- **Package management:** pip + requirements.txt (no pyproject.toml)
- **Testing:** pytest, pytest-cov, pytest-mock, pytest-timeout, responses (HTTP mocking)
- **Linting:** ruff, mypy (type checking), black (formatting)
- **Schema validation:** jsonschema
- **HTTP:** requests
- **Config:** PyYAML (YAML configs), python-dotenv (env vars)
- **CLI:** click
- **Logging:** structlog (structured logging)
- **Build tool (downstream):** aider (LLM-assisted code generation)
- **External APIs:** HN Algolia, Reddit JSON

## Architecture

Multi-agent pipeline orchestrated by The Blacksmith:

```
The Blacksmith (foundry-blacksmith, Sonnet) -- coordinator
  |
  +-- 00:00-00:45  Trend Scout (foundry-scout, Haiku) -- scans HN, Reddit
  +-- 00:45-01:30  Spec Writer (foundry-spec, Sonnet) -- evaluates & selects
  +-- 01:30-07:00  Builder (foundry-builder, Sonnet + aider) -- builds MVP
  +-- 08:00        Morning Briefing
```

Phase 2 adds feedback agents (all complete):
- **Trend Researcher** (foundry-researcher) -- Mode A: nightly lifecycle enrichment; Mode B: 2x/week deep forecasting
- **Portfolio Curator** (foundry-curator) -- weekly portfolio reports (Sunday 20:00)
- **Consensus Analyst** (foundry-analyst) -- multi-perspective evaluation (auto-triggered from engagement check)
- **Content Drafter** (foundry-drafter) -- social media content generation (Phase 3)

Agents are ephemeral (one task, no memory between runs). Continuity is file-based: each agent reads input files, writes output files, and the next agent in the pipeline picks up from there.

## Project Structure

```
the-foundry/
+-- conftest.py                # pytest path fix (adds repo root to sys.path)
+-- src/
|   +-- __init__.py
|   +-- process_trends.py      # Core trend processing logic (30K lines)
|   +-- dedup.py               # Deduplication engine (Jaccard similarity, 14-day window)
|   +-- utils.py               # Common utilities (JSON I/O, keyword extraction, scoring)
|   +-- utils_engagement.py    # Engagement tracking utilities
|   +-- prompts/               # Agent task prompts (versioned markdown files)
|   |   +-- foundry-scout-v1/v2/v3.md
|   |   +-- foundry-spec-v1/v2.md
|   |   +-- foundry-builder-v1/v2/v3-enhanced.md
|   |   +-- foundry-blacksmith-v2.md
|   |   +-- trend-researcher-mode-a-v1.md   # Nightly lifecycle enrichment
|   |   +-- trend-researcher-mode-b-v1.md   # Deep forecasting (2x/week)
|   |   +-- consensus-analyst-v1.md
|   |   +-- content-drafter-v1.md
|   |   +-- portfolio-curator-v1.md
|   +-- scripts/               # Operational scripts
|       +-- check_engagement.py    # Daily GitHub engagement check + consensus trigger
|       +-- cleanup_history.py     # History cleanup with --deep flag (workspace/trends/forecasts)
|       +-- aggregate_metrics.py   # Weekly metrics aggregation from metrics.jsonl
|       +-- multi_run_spawner.py
|       +-- test_briefing.py
+-- config/
|   +-- schemas/               # JSON schemas (all include schema_version field)
|   |   +-- build.schema.json
|   |   +-- spec.schema.json
|   |   +-- trends-summary.schema.json
|   |   +-- consensus.schema.json
|   |   +-- content-queue.schema.json
|   |   +-- content-history.schema.json
|   |   +-- voice-patterns.schema.json
|   |   +-- engagement.schema.json
|   |   +-- metrics.schema.json
|   |   +-- metrics-aggregated.schema.json
|   |   +-- history.schema.json
|   |   +-- forecast.schema.json
|   +-- cron-engagement.yml    # Cron schedule configuration
|   +-- secrets.yaml           # Secrets template (empty, use .env)
+-- tests/
|   +-- test_utils.py          # Utility function tests
|   +-- test_dedup.py          # Deduplication logic tests
|   +-- test_lifecycle.py      # Trend lifecycle tracking tests
|   +-- test_engagement.py     # Engagement scoring tests
|   +-- test_metrics.py        # Metrics calculation tests
|   +-- test_consensus.py      # Consensus analyst tests
|   +-- test_content_drafter.py # Content drafter tests
|   +-- test_content_queue.py  # Content queue schema validation (25 tests)
|   +-- mock_trends/           # Multi-night mock trend data (4 nights)
|   +-- mock_consensus/        # Mock consensus data
|   +-- test_data/             # Additional test fixtures
|   +-- README.md              # Test documentation
+-- social/                    # Social amplification (Phase 3)
|   +-- voice-guide.md         # Voice & tone guidelines
|   +-- patterns.md            # Content patterns
|   +-- engagement-tracking.md # Engagement metrics
|   +-- manual-posts/          # 5 drafts from real builds (Epic 3.1a)
|   +-- templates/             # Social post templates
|   +-- assets/                # Visual assets
+-- docs/                      # Symlink -> Obsidian design docs (23 files, read-only via git)
+-- logs/                      # Runtime logs (gitignored)
+-- scripts/
|   +-- init_workspace.sh      # Workspace initialization
+-- validate_consensus.py      # Standalone consensus validation
+-- .env.example               # Environment variable template
+-- requirements.txt           # Python dependencies
```

**Runtime workspace** (not in this repo): `~/.openclaw/workspace/foundry/`
```
foundry/
+-- YYYY-MM-DD/              # Per-night run directory
|   +-- trends-raw.json      # Scout output (raw, before lifecycle enrichment)
|   +-- trends-summary.json  # Enriched summary (for Spec Writer)
|   +-- trends-full/         # Full trend details
|   +-- spec.json            # Spec Writer output
|   +-- build.json           # Builder output
|   +-- engagement.json      # Daily engagement check results
|   +-- state.json           # Coordinator tracking
|   +-- briefing.json        # Morning briefing output
+-- history.json             # Past builds & rejections (7-day cleanup window)
+-- metrics.jsonl            # Nightly performance log
+-- trend-history/           # Multi-day trend tracking (14-day retention)
+-- forecasts/               # Deep trend forecasts (30-day retention)
|   +-- forecast-YYYY-MM-DD.json
+-- analysis/                # Consensus Analyst outputs
|   +-- YYYYMMDD-{project}-consensus.json
+-- social/                  # Social amplification runtime data
|   +-- voice-patterns.json  # Learned voice patterns (agent-writable)
|   +-- content-queue.json   # Draft queue for manual posting
|   +-- content-history.json # Voice learning history (future)
```

## Development Commands

```bash
# Install dependencies
cd ~/projects/the-foundry
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_dedup.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Run a specific test directly (some tests are executable)
python3 tests/test_lifecycle.py

# Lint
ruff check src/ tests/
ruff format --check src/ tests/

# Type check
mypy src/

# Initialize workspace
./scripts/init_workspace.sh

# Validate a consensus output
python validate_consensus.py
```

## Environment Variables

Key variables from `.env.example`:

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Claude models for aider |
| `GITHUB_TOKEN` | Builder creates repos (scope: repo, workflow) |
| `GITHUB_USERNAME` | GitHub account for repo creation |
| `OPENCLAW_GATEWAY_URL` | OpenClaw gateway (default: localhost:4445) |
| `FOUNDRY_WORKSPACE` | Runtime data path (~/.openclaw/workspace/foundry) |
| `FOUNDRY_BUILDS` | Where Builder creates projects (~/projects/foundry) |
| `LOG_LEVEL` | DEBUG, INFO, WARNING, ERROR |
| `DRY_RUN` | Skip GitHub/social posting |
| `TEST_MODE` | Use mock data instead of real APIs |

## Coding Conventions

### Python Style

- **Type hints required** on all function parameters and return values (`from typing import ...`)
- **Docstrings** on all functions (Google style: Args, Returns, Raises, Example sections)
- **Error handling** for all network calls and file I/O -- never let an agent crash silently
- **No hardcoded secrets** -- use environment variables via python-dotenv
- **Pathlib** for file paths (`from pathlib import Path`), not os.path
- **Structured logging** via structlog, not print statements
- **UTF-8 encoding** explicitly specified on all file open() calls

### Agent Task Prompts

- Write as versioned markdown files in `src/prompts/` (e.g., `foundry-scout-v3.md`)
- Include full context -- agents wake up with no memory
- Specify exact input file paths, output file paths, and JSON schemas
- Document failure modes and recovery steps
- Include explicit timeouts in seconds
- Test prompts 3-5 times with same input before committing
- Reference design docs by filename when relevant

### Configuration

- **YAML** for agent configs and cron schedules
- **JSON** for schemas -- every schema must include a `schema_version` field
- Comments explaining non-obvious settings
- Validate schemas before committing

### Testing

- Mock external APIs (HN, Reddit, GitHub) using `responses` library
- Test failure modes: timeouts, rate limits, bad data, missing sources
- Integration tests for multi-agent handoffs (Scout output -> Spec Writer input)
- All scoring logic must be deterministic (same input -> same output)
- Run before every commit

### JSON Schema Rules

- Every output schema includes `schema_version` field
- All file paths in schemas are absolute or explicitly relative
- All timeouts specified in seconds
- All API endpoints tested before documenting

## Git Workflow

- **main** branch is source of truth
- Feature branches: `epic/1.1-trend-scout-data` (per epic)
- Bug fixes: `fix/description`
- Experiments: `exp/description`
- Commit message format: reference epic number, list changes, note acceptance criteria status
- No PRs required (solo project, reviewed via War Room at http://localhost:3333)

## Key Design Decisions

- **Agents are sequential, not parallel** (Phase 1) -- Scout -> Spec -> Builder
- **File-based handoffs** between agents (JSON files in workspace)
- **Graceful degradation** -- partial success > full failure (e.g., 2/3 sources is OK)
- **Cost capping** via concrete timeouts and model selection (Haiku for Scout, Sonnet for Spec/Builder)
- **Deduplication** uses 14-day window, keyword overlap, Jaccard similarity (threshold 0.5)
- **aider** for building, not pty-based Claude Code
- **Builder tool** creates real GitHub repos via GitHub API

## Anti-Patterns

- Do NOT skip the design docs in `docs/` -- they are the source of truth for all decisions
- Do NOT hardcode secrets -- use env vars or the .env file
- Do NOT commit runtime data -- the .gitignore handles workspace artifacts
- Do NOT break the sequential agent flow -- agents depend on previous outputs
- Do NOT add dependencies without discussing -- keep the stack lightweight
- Do NOT deploy without testing -- test locally first, dry run in isolation
- Do NOT assume schemas or API column names -- verify against actual source before documenting

## External Dependencies

- **War Room:** http://localhost:3333 (Mission Control task board, filter by project "The Foundry")
- **Mission Control:** http://localhost:5173 (full dashboard)
- **OpenClaw gateway:** localhost:4445 (agent spawn/management)
- **Design docs:** `docs/` symlink to Obsidian vault at `/Users/jeeves/Obsidian/jeeves/1-Projects/The Foundry`
- **GitHub:** Repos created under `jeevesbot-io` account
- **HN Algolia API:** `http://hn.algolia.com/api/v1/search` (public, no auth)
- **Reddit JSON:** `https://www.reddit.com/r/{subreddit}/hot.json` (public, may rate-limit)

## Key Documents to Read First

1. `docs/README - Status & Next Steps.md` -- current state
2. `docs/Implementation Plan - Epics.md` -- all 16 epics
3. `docs/Agent Architecture.md` -- agent specifications
4. `docs/Builder-Coding-Agent Design.md` -- most complex component
5. `docs/Independent review.md` -- comprehensive external review
6. `MASTER-STATUS.md` -- overall progress tracker
7. `AGENTS.md` -- instructions for spawned sub-agents
