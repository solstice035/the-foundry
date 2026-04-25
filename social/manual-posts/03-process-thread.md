# Process Thread — 18 Overnight Builds in 6 Weeks

**Content Type:** process_thread
**Priority:** 1
**Estimated Engagement:** high
**Source Build:** multiple
**Best Posting Time:** Friday 10am-12pm EST (reflection content performs well end-of-week)

---

## X/Twitter

**Format:** thread

**Tweet 1:**
I built an autonomous AI pipeline that builds an MVP every night while I sleep. 40 pipeline runs over 6 weeks. 18 working repos. Here's what actually happened.

**Tweet 2:**
The pipeline scans Reddit, HN, and X for developer pain points at midnight. Picks one, writes a spec, scaffolds the project, writes code, runs tests, pushes to GitHub. Average pipeline: 15 minutes. Average cost: $0.33.

**Tweet 3:**
18 out of 20 build attempts succeeded. 90.5% success rate. The 2 failures — builder sessions that produced empty repos. 9 more nights the pipeline scanned everything and rejected all trends. That's 29 quiet nights out of 40. Most nights, nothing is worth building.

**Tweet 4:**
What it built: a phantom npm package scanner, an E2E encrypted terminal walkie-talkie, an AI code security auditor, a TUI app generator, a double-entry accounting CLI, an MCP token proxy, a video trimmer, a semantic knowledge base, and 10 more developer tools.

**Tweet 5:**
The pipeline got more reliable as it ran — early builds had rougher edges, later ones landed cleaner. Not because I tuned it overnight. I was asleep. The spec writer learned what "buildable in under 10 minutes" actually means.

**Tweet 6:**
Cost breakdown: ~$6 total across all 40 runs. Recent builds cost $0.00 (Claude Code via ACP). The most expensive build was $0.58. The cheapest was $0.13. The rejected nights cost nothing — no spec, no build, no charge.

**Tweet 7:**
Best build: deptox — 3,664 lines of TypeScript, 22 tests, npm lockfile scanner for AI-hallucinated phantom dependencies. Built in 8 minutes 44 seconds. Going v2 now. Worst build: net-scope — empty repo, builder failed before writing a line.

**Tweet 8:**
Not sharing this to flex. Sharing it because the cost of trying ideas just collapsed. $0.33 and 15 minutes to go from "devs are complaining about X" to a working repo with tests. The failure mode is a quiet night — not a wasted sprint. https://github.com/jeevesbot-io

**Visual suggestion:** Table image showing all 18 builds with dates, names, build times, and costs. Attach to Tweet 1 or Tweet 4.

---

## Notes

- This is the highest-value post. Meta content about the system itself drives more engagement than any single build.
- Updated from original 12-build draft to reflect 18 builds, 40 pipeline runs, 6 weeks of data.
- The 8-tweet thread is long but each tweet stands on its own if someone drops off.
- Tweet 3 (failures + rejections) is strategically placed early — it builds trust before the success stats.
- Tweet 7 introduces deptox naturally as "the best build, going v2" — sets up Act 2.
- Tweet 8 reframes the whole thing around cost-of-experimentation, not AI hype.
- The org link at the end lets people browse all repos without being directed to one.
- Risk: "autonomous AI pipeline" could trigger eye-rolls. The specific numbers ($0.33, 15 minutes, 90.5%) counter that.
