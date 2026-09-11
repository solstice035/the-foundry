# The Foundry 🏭

**An autonomous overnight build factory.** While I sleep, a pipeline of Claude agents picks a developer pain point off Hacker News and Reddit, writes a spec for it, builds an MVP, pushes it to GitHub and sends me a briefing at 08:00.

> [!NOTE]
> **This repo was built by agents too.** Every commit here is by Jeeves, my OpenClaw agent. I commissioned the system, approved each phase and reviewed what it shipped. The factory's own output is listed [below](#what-it-shipped).

## The pipeline

```
HN + Reddit ─► Trend Scout ─► Spec Writer ─► Builder ───────────► new GitHub repo
                (Haiku)        (Sonnet)       (Sonnet + aider)     + briefing at 08:00
```

An orchestrator agent, the Blacksmith, runs each night on a cron.

| Stage | Model | Job | Hand-off contract |
|:--|:--|:--|:--|
| Trend Scout | Claude Haiku | Pulls ~100 posts, normalises engagement, scores buildability, dedupes across sources, flags anything already built | `trends-summary.schema.json` |
| Spec Writer | Claude Sonnet | Picks one trend or rejects them all, then writes the MVP spec | `spec.schema.json` |
| Builder | Claude Sonnet via aider | Builds the MVP and pushes it to a new repo | `build.schema.json` |
| Blacksmith | — | Runs the night end to end and writes the morning briefing | `history.schema.json` |

## Why it's built this way

- **One model per stage, priced to the job.** Haiku does the high-volume reading. Sonnet is kept for the two steps that need judgement: choosing what to build, and building it. The first end-to-end build cost **$0.47**.
- **Schemas between agents.** Each stage writes JSON against a schema in [`config/schemas/`](config/schemas), so every hand-off has a defined shape.
- **Prompts are versioned.** [`src/prompts/`](src/prompts) holds the scout (`v1` → `v2`), spec writer, builder and orchestrator prompts.
- **An explicit buildability rubric.** Five dimensions scored 0–2: API availability, scope clarity, time confidence, differentiation, output type. Politics and crypto are rejected automatically.
- **Degrade, don't stop.** A failed source lowers the night's data-quality flag instead of ending the run.
- **Gated rollout.** Every epic had acceptance criteria, and a separate agent reviewed all of Phase 1 before the cron was switched on.

## Phase 1, as delivered (18 Feb 2026)

| Epic | Acceptance criteria |
|:--|:--|
| 1.1 Trend Scout: data collection | 10/11 |
| 1.2 Trend Scout: normalisation and scoring | 8/8 |
| 1.3 Spec Writer: trend selection | 6/6 |
| 1.4 Builder: aider integration | 10/10 |
| 1.5 Coordination and morning briefing | 7/7 |

The test scan pulled 114 posts (HN 70, Reddit 44), deduplicated them to 95 and scored a top 15. The first autonomous build, [`pdf-privacy-tools`](https://github.com/solstice035/pdf-privacy-tools), took 7 min 20 s and cost $0.47. The full end-to-end run took 9 min 58 s. The timeline is in [`STATUS.md`](STATUS.md) and the review in [`VALIDATION.md`](VALIDATION.md).

The one missed criterion in 1.1 was an X/Twitter source. It needed browser-cookie auth, so it was deferred, never ran, and has since been removed.

The plan runs to 16 epics across three phases, and `main` documents Phase 1. The [`feature/foundry-dashboard`](https://github.com/solstice035/the-foundry/tree/feature/foundry-dashboard) branch carries what came next:

- **Phase 2, six feedback-loop epics:** history-based dedup, build metrics, trend lifecycle tracking, forecasting, a consensus analyst and GitHub engagement monitoring
- **A Vue dashboard** over the pipeline's data
- **Early Phase 3:** a voice guide and a content drafter that prepares build announcements for me to approve before anything is posted

In late April the aider builder prompts were archived and a Claude Code builder prompt (`foundry-builder-v4-claude-code.md`) was added on the same branch. Every build listed below predates that change.

## What it shipped

19 repos between 18 February and 4 April 2026, built by the pipeline under its own `The Foundry` git identity. Eight are public:

| Built | Repo | What it does |
|:--|:--|:--|
| 18 Feb | [`pdf-privacy-tools`](https://github.com/solstice035/pdf-privacy-tools) | Privacy-first browser PDF toolkit — the first build |
| 21 Feb | [`ctx-handoff`](https://github.com/solstice035/ctx-handoff) | Captures git repo context into handoff documents for AI coding assistants |
| 26 Feb | [`mcp-slim`](https://github.com/solstice035/mcp-slim) | CLI proxy that cuts MCP token usage |
| 2 Mar | [`tool-lint`](https://github.com/solstice035/tool-lint) | Linter for MCP, OpenAI and Anthropic tool definitions |
| 4 Mar | [`deptox`](https://github.com/solstice035/deptox) | Finds AI-hallucinated phantom npm packages in lockfiles |
| 5 Mar | [`vibe-check`](https://github.com/solstice035/vibe-check) | Security scanner for AI-generated projects |
| 6 Mar | [`gh-prompt-shield`](https://github.com/solstice035/gh-prompt-shield) | Scans GitHub issues and PRs for prompt injection aimed at AI coding tools |
| 13 Mar | [`agent-safe`](https://github.com/solstice035/agent-safe) | Credential proxy for AI coding agents |

The other eleven are still private: map-poster-studio, ai-deploy-guard, smart-rename, ai-code-guard, terminal-phone, reddit-keyword-monitor, tui-forge, clipsnip, beankeeper, semantic-vault and image-forge.

## Repo layout

```
config/schemas/   JSON schemas for every agent hand-off
src/prompts/      versioned agent prompts
src/              trend processing and shared utilities
scripts/          workspace setup
tests/            unit tests for the utilities
```

The Foundry runs as agents inside OpenClaw and isn't packaged to run standalone. [`SCAFFOLDING.md`](SCAFFOLDING.md) lists the setup. The design docs live in a private knowledge base and aren't included.
