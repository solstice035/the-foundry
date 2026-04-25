# deptox — Phantom npm Package Scanner

**Content Type:** build_announcement
**Priority:** 1
**Estimated Engagement:** high
**Source Build:** 2026-03-04
**Best Posting Time:** Tuesday 9-10am EST (dev Twitter peak)
**Prerequisite:** Post after Foundry process thread (Post 1) for context

---

## X/Twitter

**Format:** thread

**Tweet 1:**
AI coding assistants hallucinate npm package names. Those phantom packages end up in your lockfile — and anyone can register them as malware. Built a scanner that catches this. Now taking it to v2.

**Tweet 2:**
deptox parses package-lock, pnpm-lock, and yarn.lock. Checks every dependency against the npm registry. Risk scores 0-100 across 6 signals — existence, downloads, freshness, maintainer count, name patterns, typosquat distance. 22 tests, 3,664 LOC TypeScript.

**Tweet 3:**
Built overnight by an autonomous pipeline for $0.55 in 8 minutes. Scored 81/100 against 18 other overnight builds — strongest v1, best market timing (axios compromise, litellm, supply chain attacks every week now). Going v2: PyPI support, advisory database, GitHub Action. `npx deptox` to try it. https://github.com/jeevesbot-io/deptox

**Visual suggestion:** Terminal screenshot showing deptox scanning a lockfile with colour-coded risk scores. Attach to Tweet 1.

---

## Reddit

**Subreddit:** r/SideProject

**Title:** deptox — CLI scanner that finds phantom npm packages hallucinated by AI coding assistants

**Body:**
AI coding assistants make up npm package names. Not often, but often enough. Those phantom packages end up in lockfiles and nobody notices — until someone registers the name and you've got a supply chain attack.

Built deptox to catch this. It parses your lockfile (package-lock.json, pnpm-lock.yaml, yarn.lock), checks every dependency against the npm registry, and flags anything that doesn't exist or looks suspicious.

**What it does:**

- Multi-lockfile parser (npm, pnpm, yarn)
- Registry checker with concurrency + progress bar
- Risk scoring engine (0-100) across 6 signals
- Levenshtein-based typosquat detection with alternative suggestions
- Colour-coded terminal report
- JSON output + exit code 1 for CI gating

**Stats:**

- 3,664 LOC TypeScript (strict mode)
- 22 tests via vitest
- Built in 8 minutes 44 seconds by an autonomous overnight pipeline
- Cost: $0.55

**Going v2:**

Scored this against 18 other overnight builds using 7 weighted criteria. deptox won at 81/100 — strongest technical foundation, best market timing (supply chain attacks are weekly news now), and the AI hallucination angle is novel. v2 adds PyPI support, OSV advisory database integration, GitHub Action, and configurable scoring.

**Known issues:**

- npm downloads API returns 0 for scoped packages, which causes false positives
- Typosquat detection gets noisy on short package names
- Yarn v1 format only (v2/v3 coming in v2)

Repo: https://github.com/jeevesbot-io/deptox

---

## Notes

- Updated from original draft: new repo URL (renamed from foundry-20260304-deptox to deptox), v2 framing, current supply chain context.
- The "going v2" angle is new — positions this as an active project, not a one-off build.
- The axios/litellm references make it timely without being clickbait.
- `npx deptox` call-to-action is critical — instant try-ability drives stars.
- Post after the Foundry process thread so readers have context about the autonomous pipeline.
