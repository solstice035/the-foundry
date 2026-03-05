# Scaffolding Status

**Last Updated:** 2026-03-05
**Status:** ✅ Phase 1 & 2 complete, Phase 3 Epic 3.1a in progress

---

## What's In Place

### 📄 Documentation

| File | Purpose | Status |
|------|---------|--------|
| README.md | Project overview | ✅ |
| CLAUDE.md | AI agent instructions | ✅ |
| AGENTS.md | Sub-agent instructions | ✅ |
| STATUS.md | Current status | ✅ |
| MASTER-STATUS.md | Master progress tracker | ✅ |
| VALIDATION.md | Phase 1 validation | ✅ |
| docs/ | Design docs symlink (23 files) | ✅ |

### ⚙️ Configuration

| File/Directory | Purpose | Status |
|----------------|---------|--------|
| .env.example | Environment variable template | ✅ |
| .gitignore | Comprehensive ignore patterns | ✅ |
| conftest.py | pytest path fix (sys.path) | ✅ |
| config/schemas/ | JSON schemas for all outputs (12 schemas) | ✅ |

### 🐍 Python Setup

| File | Purpose | Status |
|------|---------|--------|
| requirements.txt | Python dependencies | ✅ |
| src/__init__.py | Package init | ✅ |
| src/utils.py | Common utilities (keyword extraction, scoring, JSON I/O) | ✅ |
| src/dedup.py | Deduplication engine (Jaccard similarity, 14-day window) | ✅ |
| src/process_trends.py | Core trend processing logic | ✅ |
| src/utils_engagement.py | Engagement tracking utilities | ✅ |

**Scripts (src/scripts/):**
| File | Purpose | Status |
|------|---------|--------|
| check_engagement.py | Daily GitHub engagement + consensus auto-trigger | ✅ |
| cleanup_history.py | History cleanup with --deep (workspace/trends/forecasts) | ✅ |
| aggregate_metrics.py | Weekly metrics aggregation from metrics.jsonl | ✅ |
| multi_run_spawner.py | Multi-run pipeline spawner | ✅ |

**Agent Prompts (src/prompts/):** 14 versioned markdown files covering all pipeline agents.

### 🧪 Testing

| File | Purpose | Status |
|------|---------|--------|
| tests/test_utils.py | Utils test suite | ✅ |
| tests/test_dedup.py | Deduplication logic tests | ✅ |
| tests/test_lifecycle.py | Trend lifecycle tracking | ✅ |
| tests/test_engagement.py | Engagement scoring tests | ✅ |
| tests/test_metrics.py | Metrics calculation tests | ✅ |
| tests/test_consensus.py | Consensus analyst tests | ✅ |
| tests/test_content_drafter.py | Content drafter tests | ✅ |
| tests/test_content_queue.py | Content queue schema validation (25 tests) | ✅ |
| tests/README.md | Test strategy docs | ✅ |

**Test coverage:** 114 tests passing across 8 test files.

### 🔧 Scripts

| File | Purpose | Executable | Status |
|------|---------|-----------|--------|
| scripts/init_workspace.sh | Workspace initialization | ✅ | ✅ |

**What it does:**
- Creates `~/.openclaw/workspace/foundry/` structure
- Initializes `history.json` (empty, schema v1)
- Initializes `metrics.jsonl` (empty)
- Creates `~/projects/foundry/` (builds directory)
- Color output, error handling

### 📂 Directory Structure

```
the-foundry/
├── .git/
├── .gitignore
├── .env.example
├── conftest.py                 # pytest path fix
├── README.md
├── CLAUDE.md
├── AGENTS.md
├── STATUS.md
├── MASTER-STATUS.md
├── VALIDATION.md
├── config/
│   └── schemas/                # 12 JSON schemas
├── src/
│   ├── __init__.py
│   ├── utils.py
│   ├── dedup.py
│   ├── process_trends.py
│   ├── utils_engagement.py
│   ├── prompts/                # 14 agent prompt files
│   └── scripts/                # 4 operational scripts
├── scripts/
│   └── init_workspace.sh
├── tests/                      # 8 test files, 114 tests
├── social/                     # Phase 3 voice guide, patterns, manual posts
│   └── manual-posts/           # 5 drafts from real builds
├── docs/                       # Symlink to Obsidian (23 files)
└── requirements.txt
```

---

## What's Been Added Since Scaffolding

### Phase 1 (2026-02-18)

- Agent task prompts (Scout v1-v3, Spec v1, Builder v1-v3, Blacksmith v1)
- Core processing (process_trends.py, dedup.py)
- Workspace initialization and cron setup

### Phase 2 (2026-03-05)

- Spec Writer v2 (forecast integration)
- Blacksmith v2 (engagement in briefing)
- Trend Researcher Mode A (lifecycle) + Mode B (forecasting)
- Consensus Analyst v1 (auto-triggered)
- Scripts: cleanup_history.py (--deep), aggregate_metrics.py, check_engagement.py (consensus trigger)
- Schemas: forecast.schema.json, metrics-aggregated.schema.json
- Tests: 7 test files, 89 tests total
- conftest.py for pytest imports

---

### Phase 3 Epic 3.1a (2026-03-05)

- Voice guide v1.1 (grounded in real build data from 12 pipeline runs)
- Patterns v1.1 (baseline observations from build metrics)
- content-history.schema.json (voice learning history)
- voice-patterns.schema.json (learned voice patterns)
- voice-patterns.json seed file (workspace: ~/.openclaw/workspace/foundry/social/)
- content-queue.json initialized with 5 drafts (workspace)
- 5 manual post drafts in social/manual-posts/ (deptox, terminal-phone, process thread, tool-lint, failure)
- test_content_queue.py (25 schema validation tests)
- Tests: 8 test files, 114 tests total

---

## Summary

Phase 1 and Phase 2 are fully delivered. Phase 3 Epic 3.1a (Voice Guide & Manual Posting — artifacts) is complete. Epic 3.1b (Nick manually posts for 2-3 weeks to calibrate voice) is next.

---

**Last Updated:** 2026-03-05
**Status:** Phase 3 Epic 3.1a complete, 3.1b pending (manual posting)
