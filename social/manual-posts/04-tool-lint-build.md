# Tool Lint — AI Tool Description Linter

**Content Type:** build_announcement
**Priority:** 2
**Estimated Engagement:** medium-high
**Source Build:** 2026-03-02
**Best Posting Time:** Wednesday 9-11am EST

---

## X/Twitter

**Format:** thread

**Tweet 1:**
Your AI tool descriptions are probably bad. Vague names, missing parameter docs, no examples. Models perform worse when tool schemas are sloppy. Built a linter for it.

**Tweet 2:**
tool-lint scores MCP, OpenAI, and Anthropic tool schemas. Flags vague descriptions, missing fields, inconsistent naming. Outputs actionable suggestions. CI-friendly with configurable rules. 23 tests, TypeScript + Zod.

**Tweet 3:**
An AI linter for AI tools, built by an AI pipeline. The recursion writes itself. Pipeline spotted the gap on X — no standard linter exists for tool descriptions. Built in 9 minutes for $0.57. https://github.com/jeevesbot-io/tool-lint

**Visual suggestion:** Terminal screenshot showing tool-lint output with quality scores and suggestions on a sample tool schema. Attach to Tweet 1.

---

## Reddit

**Subreddit:** r/SideProject
**Title:** I built an AI linter for AI tool descriptions -- scores MCP, OpenAI, and Anthropic schemas

**Body:**
I've been noticing that AI tool descriptions (MCP servers, OpenAI function calling, Anthropic tool use) are often vague or incomplete. Models perform measurably worse when the tool schemas they're working with have sloppy descriptions, missing parameter docs, or inconsistent naming.

No standard linter existed for this, so my overnight build pipeline spotted the gap and built one: **tool-lint**.

**What it does:**
- Parses MCP, OpenAI, and Anthropic tool schema formats
- Scores description quality on multiple dimensions (clarity, completeness, consistency)
- Flags vague descriptions, missing fields, inconsistent naming conventions
- Outputs actionable improvement suggestions
- CI-friendly exit codes with configurable rule severity

**Stack:** TypeScript, Commander, Zod. 23 tests.

**The meta angle:** This is an AI linter for AI tools, built by an AI pipeline. My autonomous build system scanned X for developer pain points, identified the gap, wrote a spec, and built the whole thing in 9 minutes for $0.57 in API costs while I was asleep.

**Repo:** https://github.com/jeevesbot-io/tool-lint

**Known limitations:**
- Scoring is opinionated -- what counts as "vague" is subjective
- No auto-fix yet (just suggestions)
- Custom rule authoring is basic

Happy to answer questions about the tool or the pipeline that built it.

---

## Notes

- The meta angle — AI linting AI tools built by AI — is the real hook. Tweet 3 leans into it without overselling.
- MCP support is timely given the protocol's growth. Could attract attention from that community.
- The "your tool descriptions are probably bad" opener is direct and slightly provocative without being clickbait.
- Risk: "linter" is a crowded category and some people will ask "why not just use eslint rules." The answer is that this lints semantic quality of descriptions, not syntax — make sure that distinction is clear if replying to comments.
- Engagement score (78.0) is lower than deptox but the meta angle and MCP relevance could outperform the number.
