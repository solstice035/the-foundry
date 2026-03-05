# Deptox — Phantom npm Package Scanner

**Content Type:** build_announcement
**Priority:** 1
**Estimated Engagement:** medium-high
**Source Build:** 2026-03-04
**Best Posting Time:** Tuesday 9-10am EST (dev Twitter peak)

---

## X/Twitter

**Format:** thread

**Tweet 1:**
AI coding assistants hallucinate npm package names. Those phantom packages end up in your lockfile — and anyone can register them. Built a scanner overnight that catches this.

**Tweet 2:**
deptox parses package-lock, pnpm-lock, and yarn.lock. Checks every dependency against the npm registry. Risk scores 0-100, Levenshtein-based typosquat detection, color-coded terminal report. 22 tests, 3664 LOC TypeScript — built in 8m 44s for $0.55.

**Tweet 3:**
Exit code 1 for CI gating, JSON output for pipelines. Known gap — npm downloads API returns 0 for scoped packages so you get some false positives. Pipeline spotted the problem on Reddit, spec'd it, built it while I slept. https://github.com/jeevesbot-io/foundry-20260304-deptox

**Visual suggestion:** Terminal screenshot showing deptox scanning a lockfile with color-coded risk scores. Attach to Tweet 1.

---

## Reddit

**Subreddit:** r/SideProject

**Title:** deptox — CLI scanner that finds phantom npm packages hallucinated by AI coding assistants

**Body:**
AI coding assistants make up npm package names. Not often, but often enough. Those phantom packages end up in lockfiles and nobody notices — until someone registers the name and you've got a supply chain attack.

Built deptox to catch this. It parses your lockfile (package-lock.json, pnpm-lock.yaml, yarn.lock), checks every dependency against the npm registry, and flags anything that doesn't exist or looks like a typosquat.

**What it does:**

- Multi-lockfile parser
- Registry checker with concurrency + progress bar
- Risk scoring engine (0-100)
- Levenshtein-based alternative suggestions
- Color-coded terminal report
- JSON output + exit code 1 for CI gating

**Stats:**

- 3664 LOC TypeScript (strict mode)
- 22 tests via vitest
- Built in 8 minutes 44 seconds
- Cost: $0.55

**Known issues:**

- npm downloads API returns 0 for scoped packages, which causes false positives
- Typosquat detection gets noisy on short package names

This was built by an autonomous pipeline I run overnight — it scans Reddit and HN for developer pain points, picks one, writes a spec, and builds an MVP. This one came from a Reddit thread about AI-hallucinated dependencies.

Repo: https://github.com/jeevesbot-io/foundry-20260304-deptox

---

## Notes

- Supply chain security is a hot topic right now. The AI hallucination angle gives this a strong hook.
- The Reddit source thread could be referenced if it's still active — adds credibility.
- False positives on scoped packages should be mentioned upfront to avoid "doesn't work" comments.
- Priority 1 because the trend is fresh and the engagement score (120.9) is the second highest across all builds.
