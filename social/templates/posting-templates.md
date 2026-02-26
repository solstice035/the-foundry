# Social Media Posting Templates

**Version:** 1.0  
**Last Updated:** 2026-02-26  
**For:** Manual posting phase (Epic 3.1)  
**Reference:** See `voice-guide.md` for tone guidelines

---

## Purpose

These templates provide concrete examples for manual posting during the initial testing phase. Use these as starting points, adapt to specific builds, and track what works.

Each template includes:
- **Platform variations** (X, Reddit, LinkedIn where applicable)
- **Example in Nick's voice** (following `voice-guide.md`)
- **Timing guidance**
- **Visual suggestions**

---

## Template 1: Build Announcement

**When to use:** Successful overnight build, signal score 8+  
**Platforms:** X (primary), Reddit (if strong), LinkedIn (monthly summary)  
**Frequency:** 1-2x per week maximum

### X/Twitter Version (Thread Format)

**Tweet 1: Hook**
```
Saw devs complaining about [PROBLEM] on [PLATFORM] yesterday.

So my overnight build pipeline picked it up, speced it, and built [SOLUTION] while I slept.
```

**Tweet 2: What it does**
```
→ [KEY FEATURE 1]
→ [KEY FEATURE 2]
→ [KEY FEATURE 3]

[ONE-LINE DESCRIPTION OF VALUE]
```

**Tweet 3: Link + numbers**
```
Repo: [GITHUB_URL]

Built in [TIME]. ~$[COST] in API costs.

[OPTIONAL: One-line insight about the build process]
```

**Example (commitai):**

```
Tweet 1:
Saw devs complaining about writing commit messages yesterday.

So my overnight build pipeline picked it up, wrote a spec, and built a CLI tool while I slept.

Tweet 2:
→ Analyzes your git diff
→ Generates a commit message via LLM
→ Approve, edit, or regenerate

Simple problem, simple tool.

Tweet 3:
Repo: github.com/jeevesbot-io/autonomous-builds-20260218-commitai

Built in 3h 12m. ~$0.47 in API costs.

The overnight pipeline is getting reliable.
```

**Visual:** Terminal GIF showing the tool in action (tweet 2)

**Best posting time:** 09:00-10:00 GMT (dev morning scroll)

---

### Reddit Version (r/SideProject format)

**Title Format:**
```
I built [TOOL_NAME] — [ONE-LINE DESCRIPTION] [built overnight with an AI pipeline]
```

**Post Structure:**

```markdown
**The problem:** [2-3 sentences explaining the pain point and where you saw it]

**What it does:** 
- [Feature 1]
- [Feature 2]  
- [Feature 3]

[One paragraph on how it works]

**How it was built:**
This was built overnight by my autonomous build pipeline. The system scans trending developer pain points from HN, Reddit, and X, writes a spec, and spawns a coding agent to build it. [Link to pipeline docs if available]

**Stack:** [Tech stack]

**Demo:** [Screenshot or GIF if available]

**Repo:** [GitHub link]

Happy to answer questions about the tool or the pipeline that built it.
```

**Example (commitai):**

```markdown
Title: I built commitai — AI-powered git commit messages from your diff (built overnight with an AI pipeline)

Body:
**The problem:** Writing good commit messages is tedious. I saw developers on Twitter yesterday complaining about staring at `git commit` prompts, trying to summarize changes they made hours ago.

**What it does:**
- Analyzes your git diff
- Generates a conventional commit message via LLM
- Lets you approve, edit, or regenerate
- Configurable prompt templates

You run `commitai`, it reads your staged changes, suggests a message, and you either use it or tweak it.

**How it was built:**
This was built overnight by my autonomous build pipeline. The system scans trending developer pain points from HN, Reddit, and X, writes a spec, and spawns a coding agent (aider) to build it while I sleep. This was one of the first tools it built that actually works well enough to use daily.

**Stack:** Node.js, TypeScript, OpenAI API

**Demo:** [Screenshot of terminal output]

**Repo:** github.com/jeevesbot-io/autonomous-builds-20260218-commitai

Happy to answer questions about the tool or the pipeline that built it.
```

**Visual:** Terminal screenshot or GIF

**Best posting time:** 14:00-16:00 GMT (US morning)

**Engagement:** Respond to every comment in first 2 hours

---

## Template 2: Process Thread

**When to use:** Weekly meta-content about the pipeline itself  
**Platforms:** X only (thread format)  
**Frequency:** Once per week (Thursday or Friday)

### X/Twitter Thread Structure

**Tweet 1: Hook**
```
I built a system that watches dev Twitter overnight and builds apps from trending pain points.

[Current stats: X builds, Y public, Z stars]
```

**Tweet 2: How it works - Scanning**
```
At midnight, a Trend Scout agent scans X, Reddit, HN, and ProductHunt for developer pain points.

[Specific example of what it found this week]
```

**Tweet 3: How it works - Decision**
```
A Spec Writer agent picks ONE trend (or rejects them all) and writes a full build spec.

This week: [what was approved/rejected and why]
```

**Tweet 4: How it works - Build**
```
A Builder agent spawns a coding agent (aider) and builds the MVP.

[Time taken, cost, outcome]
```

**Tweet 5: This week's result**
```
This week it built [PROJECT_NAME]: [one-line description]

→ [Key feature 1]
→ [Key feature 2]

[Link]
```

**Tweet 6: The numbers**
```
Pipeline stats:
• [X] builds so far
• [Y] public repos
• [Z] total stars
• ~$[COST]/night
• [SUCCESS_RATE]% completion rate
```

**Tweet 7: What I learned**
```
[One genuine insight or surprise from this week's build/rejection]

[Example: "Turns out most trending pain points are already solved—the pipeline rejected 8/10 this week."]
```

**Tweet 8: CTA**
```
The pipeline is fully documented and the code is public.

What should it build next?

[Link to docs or repo]
```

**Visual:** Architecture diagram (tweet 2) or stats screenshot (tweet 6)

**Best posting time:** Thursday or Friday 15:00-17:00 GMT

**Voice note:** This is the hero content. The "how I built the thing that builds things" story is more interesting than any individual tool.

---

## Template 3: Rejection Post

**When to use:** Spec Writer rejects all trends from a night's scan  
**Platforms:** X only (single tweet)  
**Frequency:** 1-2x per month (sparingly—only when rejection reasoning is interesting)

### X/Twitter Single Tweet

**Format:**
```
My AI build pipeline analyzed [N] trending topics last night and decided none of them were worth building.

Top reject: [TOPIC] ([concise reason])

[One-line insight about saying no]
```

**Example 1:**
```
My AI build pipeline analyzed 14 trending topics last night and decided none of them were worth building.

Top reject: crypto portfolio tracker (saturated, no differentiator)

Sometimes the best build is no build.
```

**Example 2:**
```
My overnight pipeline rejected everything last night.

8 trends scanned, zero approved.

Mostly "AI wrapper over X" ideas that already exist with better UX. The bar is higher than Twitter makes it seem.
```

**Example 3:**
```
Pipeline said "pass" on all 12 trends last night.

Best candidate was a Markdown editor. Then we found 47 existing ones, 6 of which are excellent.

Copying homework doesn't count as building.
```

**Visual:** None (text-only for maximum credibility)

**Best posting time:** Tuesday or Wednesday 16:00-18:00 GMT

**Why this works:** Counterintuitive. Shows judgment, not just output. People engage with "here's what I chose NOT to do" more than "here's what I did."

---

## Template 4: Trend Forecast

**When to use:** Emerging pain point identified, not yet built  
**Platforms:** X only (1-2 tweets)  
**Frequency:** Mid-week filler when no build to announce

### X/Twitter Format

**Single Tweet Version:**
```
Pain point I'm tracking: [PROBLEM]

[N] mentions on [PLATFORM] this week (up from [M] last week). [Why current solutions don't work]

[Prediction or intent]
```

**Two-Tweet Thread Version:**
```
Tweet 1:
Pain point I'm tracking: [PROBLEM]

[Evidence: mentions, discussions, where you're seeing it]

Tweet 2:
[Why current solutions fall short]

[What a good solution would look like / might build this next]
```

**Example 1 (Single):**
```
Pain point I'm tracking: managing API keys across multiple AI providers.

23 Reddit mentions this week, up from 8. dotenv doesn't cut it when you're juggling OpenAI, Anthropic, Mistral, and local models.

Someone's going to build a proper solution. Might be my pipeline.
```

**Example 2 (Thread):**
```
Tweet 1:
Seeing more devs struggle with local-first sync lately.

CRDTs are too complex, Firebase is overkill for simple use cases, and rolling your own is tedious.

Tweet 2:
What's missing: a dead-simple drop-in sync layer for SQLite. No backend required, no CRDT PhD needed.

The gap between "just use PostgreSQL" and "here's 400 pages on CRDTs" is real.
```

**Example 3 (Single):**
```
Trend I'm watching: CLI tools with built-in TUIs for better UX.

Developers want the scriptability of CLIs but the discoverability of GUIs. Charm's Bubble Tea is getting traction for a reason.

My pipeline might pick this up soon.
```

**Visual:** None

**Best posting time:** Wednesday 15:00-17:00 GMT

**Voice note:** Thought leadership without the fluff. This positions Nick as having a pulse on what's emerging, not just reacting to what's already trending.

---

## Template 5: Consensus Take

**When to use:** Multi-perspective analysis complete (Consensus Analyst triggered)  
**Platforms:** X only (thread format)  
**Frequency:** Rare (only when builds hit engagement thresholds)

### X/Twitter Thread Structure

**Tweet 1: Setup**
```
Ran my 5-perspective analysis on [PROJECT_NAME] ([ENGAGEMENT_METRIC]).

[Brief what-it-does]
```

**Tweet 2-6: Perspectives (one per tweet)**
```
🧑‍💻 User: "[User perspective quote]"

🔍 Critic: "[Critical perspective quote]"

🛠️ Builder: "[Technical assessment quote]"

📢 Marketer: "[Marketing perspective quote]"

💰 Investor: "[Business perspective quote]"
```

**Tweet 7: Verdict**
```
Verdict: [Decision: invest/polish for portfolio/abandon]

[One-line reasoning or action item]
```

**Example (commitai - 34 stars in 4 days):**

```
Tweet 1:
Ran my 5-perspective analysis on commitai (34 stars in 4 days).

CLI tool that generates git commit messages from your diff using LLM.

Tweet 2:
🧑‍💻 User: "I'd use it if it supported Anthropic, not just OpenAI. Also needs conventional commit format options."

Tweet 3:
🔍 Critic: "aicommits already has 7K stars. Differentiation is thin. This is late to market."

Tweet 4:
🛠️ Builder: "8-12 hours to production quality. No tests yet. Prompt templates are hardcoded."

Tweet 5:
📢 Marketer: "The creation story is the hook, not the tool. 'Built overnight by AI' is more interesting than the commit messages."

Tweet 6:
💰 Investor: "Feature, not product. TAM is too small. But great portfolio piece for 'here's what my pipeline can do.'"

Tweet 7:
Verdict: Polish for portfolio, don't chase it as a product.

Add tests, support Anthropic, make prompts configurable. Ship v1.1 then move on.
```

**Visual:** None (text-only focuses on the analysis)

**Best posting time:** Friday 14:00-16:00 GMT (weekend reading)

**Voice note:** Unusual format = high engagement. Shows the multi-faceted thinking process, not just the conclusion. The disagreement between perspectives is the interesting part.

---

## Template 6: Failure Post

**When to use:** Build fails or times out  
**Platforms:** X only (single tweet or 2-tweet thread)  
**Frequency:** Sparingly (only when failure teaches something interesting)

### X/Twitter Single Tweet

**Format:**
```
Overnight build attempted [WHAT_WAS_TRIED].

[WHERE_IT_FAILED].

Lesson: [WHAT_YOU_LEARNED]

[Optional: One-line about why cheap experiments allow for public failures]
```

**Example 1:**
```
Overnight build attempted a real-time collaborative whiteboard.

Hit the WebSocket complexity wall at 60% complete after 5 hours.

Lesson: should have scoped to single-user first.

Not every night produces a win. That's the point of automation—cheap experiments.
```

**Example 2:**
```
Pipeline timed out trying to build a Chrome extension for tab management.

Got stuck on manifest v3 permission issues that are genuinely hard to debug programmatically.

Turns out some things still need human judgment.
```

**Example 3:**
```
Build failed: PDF annotation tool.

Canvas rendering worked, but file save/load turned into a mess of encoding edge cases.

Partial code pushed. Might be salvageable, might not. Either way, $0.80 well spent.
```

### X/Twitter Two-Tweet Thread (for complex failures)

**Tweet 1: What was attempted**
```
Overnight build: [DESCRIPTION]

[Why it seemed like a good idea]
```

**Tweet 2: Where it failed + lesson**
```
[Specific failure point and technical reason]

Lesson: [What you learned]

[Optional: What you'd do differently]
```

**Example:**
```
Tweet 1:
Overnight build: local-first notes app with E2E encryption.

Saw it trending on Reddit, seemed straightforward. Encryption, sync, Markdown. Basic stuff.

Tweet 2:
Crypto worked fine. Sync logic exploded when handling merge conflicts on concurrent edits.

Lesson: "local-first" is harder than it looks. Operational transforms aren't trivial.

Should've started with single-device, added sync later.
```

**Visual:** None (or optional: screenshot of error log if it's genuinely interesting)

**Best posting time:** Tuesday 10:00-12:00 GMT

**Voice note:** Vulnerability builds credibility. The willingness to publicly say "this didn't work" makes the successes more believable. Cheap experiments allow for public failures—lean into that.

---

## Platform-Specific Formatting Reference

### X/Twitter

- **Character limit:** 280 per tweet (but aim for <240 for natural breaks)
- **Thread length:** 2-3 tweets for announcements, 4-8 for process threads
- **Links:** Always in the last tweet of a thread
- **Hashtags:** Avoid (unless ironic)
- **Emojis:** Not in first tweet; sparingly elsewhere
- **@mentions:** Only when directly relevant, not for clout

### Reddit

- **Title length:** 60-100 characters ideal
- **Title format:** Descriptive, not clickbait
- **Body structure:** Problem → Solution → Details → Link
- **Formatting:** Use bold, bullets, headers (Markdown)
- **Self-promotion:** Must provide value, not just link dump
- **Engagement:** Respond to all comments in first 2 hours

### LinkedIn

- **Post length:** 1,300-2,000 characters works well
- **Formatting:** Short paragraphs, line breaks for readability
- **Tone:** Slightly more polished than X, but still authentic
- **Hashtags:** 3-5 relevant ones acceptable (unlike X)
- **Links:** Can be in body, not just at end

---

## Timing Guidelines

### Best Posting Times (GMT)

**X/Twitter:**
- **Morning (09:00-11:00):** Build announcements, quick updates
- **Midday (12:00-14:00):** Avoid (low engagement)
- **Afternoon (15:00-17:00):** Process threads, trend forecasts
- **Evening (18:00-20:00):** Consensus posts, failure posts

**Reddit:**
- **US Morning (14:00-16:00 GMT):** Best for r/programming, r/webdev
- **US Evening (00:00-02:00 GMT):** Alternative window
- Avoid: UK daytime (03:00-13:00 GMT)

**LinkedIn:**
- **Weekday mornings (08:00-10:00 GMT):** Professional browsing time
- **Tuesday-Thursday:** Higher engagement than Mon/Fri

### Content Spacing

- **Never post more than once per day** on X
- **Never post more than twice per week** on Reddit
- **Rest days are fine** — silence is better than filler

---

## Visual Content Suggestions

### For Each Template

**Build Announcement:**
- Terminal GIF showing the tool in action (preferred)
- Screenshot of key feature
- Architecture diagram (for complex tools)

**Process Thread:**
- Pipeline architecture diagram
- Stats screenshot (builds/stars/costs)
- Before/after comparison

**Rejection Post:**
- None (text-only for maximum credibility)

**Trend Forecast:**
- None (thought leadership is text-based)

**Consensus Take:**
- None (focus on the analysis)

**Failure Post:**
- Optional: Error log screenshot (only if genuinely interesting)
- Optional: "What I learned" diagram

### Visual Generation Notes

- CLI tools: Use `vhs` or `asciinema` for terminal recordings
- Web apps: Playwright screenshots during build
- Stats: Simple HTML → PNG renders, not AI-generated graphics
- Consistent branding: Dark background, monospace font

---

## Engagement Tracking (Per Template)

For each post, track:

| Metric | Target (X) | Target (Reddit) |
|--------|-----------|----------------|
| Impressions | 5,000+ | N/A |
| Likes | 30+ | 50+ upvotes |
| Retweets/Shares | 5+ | N/A |
| Comments/Replies | 3+ | 5+ |
| Click-through to repo | 50+ | 20+ |

**High performers** (2x+ these targets) should be analyzed:
- What made it work?
- Which template?
- What angle?
- What time?

Document in `patterns.md`.

---

## Template Usage Checklist

Before posting, ask:

- [ ] Does this follow the voice guide?
- [ ] Is it direct, or is there fluff?
- [ ] Are there concrete numbers/specifics?
- [ ] Would I stop scrolling to read this?
- [ ] Is the timing appropriate?
- [ ] Is the platform right for this content?
- [ ] Do I have a visual if needed?
- [ ] Can I respond to comments for 2 hours? (Reddit)

If any answer is "no," revise or delay.

---

## Update Log

**v1.0 (2026-02-26):**
- Initial templates created
- 6 content types with X/Reddit/LinkedIn variations
- Examples in Nick's voice
- Timing and visual guidance
- Engagement tracking baseline

**Future updates will include:**
- Real-world examples from manual posting
- Engagement data per template
- Refined timing based on actual performance
- New templates based on what works

---

**Status:** Active  
**Usage:** Manual posting phase (Epic 3.1)  
**Next Phase:** Content Drafter will use these as reference for automated draft generation
