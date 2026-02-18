# The Foundry - Social Media Posts

**Campaign:** Phase 1 Launch Announcement  
**Date:** 2026-02-18  
**Hook:** Built an autonomous overnight app factory in one day  
**Proof:** First build already live on GitHub

---

## X/Twitter - Thread Format

### Tweet 1 (Main)
Built an autonomous overnight app factory today. You sleep → it scans trending dev pain points → picks one → builds an MVP → pushes to GitHub.

First test run: 10 minutes, $0.47, working app.

Tonight at midnight it runs for real. 🏭

### Tweet 2
The pipeline:
• Trend Scout (Haiku) scans HN + Reddit
• Spec Writer (Sonnet) picks the best one
• Builder (Opus + aider) codes it
• Morning briefing with repo link

All autonomous. No human in the loop.

### Tweet 3
First build: pdf-privacy-tools

Browser-based PDF toolkit (merge/split/extract). Privacy-first, zero server uploads. TypeScript + Vite + pdf-lib.

7m 20s build time. 13 files. Working demo.

GitHub: https://github.com/jeevesbot-io/foundry-20260218-pdf-privacy-tools

### Tweet 4
Built on @AnthropicAI Claude via @OpenClawAI

Stack:
• Haiku for trend scanning ($)
• Sonnet for evaluation
• Opus 4 for orchestration
• aider for code generation

Cost per build: ~$0.50
Timeline: midnight → morning briefing

### Tweet 5
Design → production in 24 hours:
• 5 epics shipped
• 16 design docs
• End-to-end tested
• Cron enabled
• First autonomous run: tonight

Open question: what happens when you give an AI agent 8 hours unsupervised with trending pain points?

We'll find out in the morning. 🏭

---

## Threads - Single Post Format

Built an autonomous overnight app factory today. The entire pipeline runs while you sleep:

🔍 Midnight: Scans HN + Reddit for trending dev pain points  
📋 Evaluates buildability (5 dimensions, explicit scoring)  
🛠️ Picks ONE trend and spawns aider to build it  
📦 Creates GitHub repo, pushes code  
📨 Morning briefing with results

First test run: 10 minutes, $0.47, working app.

The build: pdf-privacy-tools — browser-based PDF toolkit (merge, split, extract text). Privacy-first, client-side only. TypeScript + Vite + pdf-lib. 7m 20s from spec to GitHub.

Stack: Claude via OpenClaw (Haiku for scanning, Sonnet for evaluation, Opus for orchestration), aider for code generation.

Tonight at midnight it runs for real. No human intervention. Just wake up to either a new autonomous build or a clear explanation of why nothing shipped.

Design → production in 24 hours. 5 epics. 16 design docs. End-to-end tested. Cron enabled.

GitHub (first build): https://github.com/jeevesbot-io/foundry-20260218-pdf-privacy-tools

Open question: what happens when you give an AI agent 8 hours unsupervised with trending pain points? We'll find out tomorrow morning. 🏭

---

## LinkedIn - Professional Format

### Title
We Built an Autonomous Overnight App Factory in 24 Hours

### Body
Today we shipped The Foundry — an autonomous pipeline that scans trending developer pain points, evaluates buildability, and builds working MVPs overnight while you sleep.

**The Pipeline:**

• **Trend Scout (Haiku):** Scans Hacker News and Reddit for trending pain points. Normalizes engagement signals, scores buildability across 5 dimensions (API availability, scope clarity, time confidence, differentiation, output type).

• **Spec Writer (Sonnet):** Evaluates top trends with LLM judgment. Selects ONE buildable trend or rejects all with clear reasoning. Checks against 14-day history to avoid duplicates.

• **Builder (Opus + aider):** Takes the spec, spawns aider in batch mode, builds the MVP, tests locally, creates a private GitHub repo, and pushes the code.

• **Morning Briefing:** Compiles results and delivers via Telegram. Either a new autonomous build with repo link, or a detailed rejection report.

**First Test Build:**

We tested the full pipeline today with real data from HN and Reddit. Result: pdf-privacy-tools — a privacy-first, browser-based PDF toolkit (merge, split, extract text, page thumbnails, dark mode).

- Build time: 7 minutes 20 seconds
- Cost: $0.47
- Files: 13
- Stack: TypeScript + Vite + pdf-lib + pdfjs-dist
- Status: SUCCESS (all tests passing)
- GitHub: https://github.com/jeevesbot-io/foundry-20260218-pdf-privacy-tools

**Design → Production Timeline:**

• 00:00 - Started design discussions
• 18:00 - All 5 epics shipped (Trend Scout, Normalization, Spec Writer, Builder, Coordination)
• 19:00 - End-to-end pipeline tested
• 20:00 - Independent validation complete
• 20:30 - Cron job enabled

24 hours from concept to autonomous operation.

**The Question:**

What happens when you give an AI agent 8 hours unsupervised with trending pain points from developer communities?

Tonight at midnight (GMT), The Foundry runs for real. No human in the loop. Just autonomous trend scanning, evaluation, building, and delivery.

We'll share results in the morning briefing.

Built on Claude (Anthropic) via OpenClaw. Orchestrated with Opus 4, evaluated with Sonnet, scanned with Haiku. Code generation via aider.

**Tech Stack:**
- OpenClaw (agent orchestration)
- Claude Opus 4 (coordination)
- Claude Sonnet 4.5 (evaluation)
- Claude Haiku 4 (scanning)
- aider (code generation)
- GitHub CLI (deployment)

**Cost Model:**
~$0.50 per build. ~$15/month for nightly operation.

We're documenting everything. All design docs, validation reports, and build logs are in the repo. The first autonomous build will be public (if the trend selected is appropriate).

The future isn't AGI. It's narrow, autonomous agents doing one thing extremely well while you sleep.

#AI #Automation #OpenSource #Development #Claude #Anthropic

---

## Reddit - r/SideProject Format

### Title
[Show SP] I built an autonomous overnight app factory that scans trending pain points and builds MVPs while I sleep

### Body
**What it is:**

The Foundry - an autonomous pipeline that runs at midnight, scans Hacker News and Reddit for trending developer pain points, picks the most buildable one, and spawns an AI coding agent to build an MVP overnight.

You wake up to either a new GitHub repo with a working app, or a detailed briefing on why nothing shipped.

**First test run (today):**

- Scanned 114 trends from HN + Reddit
- Normalized engagement, scored buildability (5 dimensions)
- Selected: "privacy-first PDF tool" (browser-based, no servers)
- Built: pdf-privacy-tools (TypeScript + Vite + pdf-lib)
- Features: PDF merge, split, text extraction, page thumbnails, dark mode
- Build time: 7m 20s
- Cost: $0.47
- Status: SUCCESS (all tests passing, pushed to GitHub)

**The pipeline:**

1. **Trend Scout** (Claude Haiku) - Scans HN Algolia API + Reddit JSON endpoints for hot posts. Extracts titles, URLs, engagement metrics. Normalizes HN points and Reddit scores to 0-100 scale. Scores buildability: API availability, scope clarity, time confidence, differentiation, output type (each 0-2, total 0-10). Deduplicates across sources. Outputs top 15 trends.

2. **Spec Writer** (Claude Sonnet) - Evaluates top 3-5 trends with LLM judgment. Checks against 14-day history to avoid duplicates. Selects ONE trend with buildability ≥7 and clear MVP scope, OR rejects all with reasoning. Outputs detailed spec: features, stack, scope, success criteria.

3. **Builder** (Claude Opus + aider) - Spawns aider in batch mode with full spec. Monitors build progress (5-hour timeout). Tests locally (README, dependencies, build). Creates private GitHub repo. Pushes code. Updates history.json for deduplication.

4. **Morning Briefing** - Compiles results (success/rejection/failure). Delivers via Telegram with repo link or rejection reasoning.

**Tech stack:**

- OpenClaw (agent orchestration framework)
- Claude Opus 4 (coordination)
- Claude Sonnet 4.5 (evaluation)
- Claude Haiku 4 (scanning - cost optimized)
- aider (AI pair programming CLI)
- GitHub CLI (deployment)

**Timeline:**

Design → production in 24 hours:
- 5 epics shipped (Trend Scout, Normalization, Spec Writer, Builder, Coordination)
- 16 design documents
- End-to-end tested with real data
- Independent validation complete
- Cron job enabled

**Tonight at midnight:**

First autonomous run. No human intervention. Just wake up tomorrow to see what it built (or why it didn't build anything).

**Cost:**

~$0.50 per build. ~$15/month for nightly operation. Way cheaper than paying for trending app ideas.

**Source:**

- First build: https://github.com/jeevesbot-io/foundry-20260218-pdf-privacy-tools
- Design docs: ~/projects/the-foundry/ (local, might open-source later)
- Built on: OpenClaw + Claude (Anthropic)

**Open questions:**

1. Will it consistently pick buildable trends?
2. How often will aider actually produce working code?
3. What's the success rate over 30 nights?
4. What happens when it picks something genuinely novel?

We're about to find out. First autonomous run in 3 hours.

**Why I built this:**

Wanted to test: can you fully automate the "idea → MVP" pipeline with current AI tools? Turns out: yes, but you need explicit buildability scoring, deduplication, and graceful failure modes.

The interesting part isn't whether it works (it does). It's what happens when you run it for 30 nights straight. Does it find patterns? Build actually useful tools? Or just churn out variations of the same CRUD apps?

Tomorrow morning we'll have the first data point.

---

## Reddit - r/programming Format (More Technical)

### Title
[Show r/programming] Autonomous overnight build pipeline: trending pain points → buildability scoring → aider → GitHub

### Body
Built an autonomous agent pipeline that scans Hacker News and Reddit for trending developer pain points, scores buildability with explicit rubrics, and spawns aider to build working MVPs overnight.

**Architecture:**

Multi-agent pipeline coordinated by OpenClaw (agent orchestration framework):

```
00:00 Trend Scout (Haiku 4)
  ├─ HN Algolia API (3 queries: top, Show HN, Ask HN)
  ├─ Reddit JSON (5 subs: programming, webdev, SideProject, selfhosted, commandline)
  └─ X/Twitter (bird CLI - auth deferred)
  
00:45 Normalization & Scoring
  ├─ Engagement: HN points/5, Reddit score/10 → 0-100 scale
  ├─ Cross-source amplification: 1.3x-2.0x
  ├─ Buildability: 5 dimensions, each 0-2
  │   ├─ API availability (0=none, 1=unofficial, 2=official)
  │   ├─ Scope clarity (0=vague, 1=clear, 2=very specific)
  │   ├─ Time confidence (0=uncertain, 1=probably 4-6h, 2=definitely)
  │   ├─ Differentiation (0=saturated, 1=unique, 2=novel)
  │   └─ Output type (0=hard to show, 1=can demo, 2=immediately visible)
  ├─ Auto-filters: political/crypto keywords → reject
  └─ Deduplication: URL exact + title fuzzy (>70%)

01:30 Spec Writer (Sonnet 4.5)
  ├─ Evaluate top 3-5 trends (LLM judgment)
  ├─ Check history.json (14-day dedup window)
  ├─ Select ONE with buildability ≥7 OR reject all
  └─ Output: spec.json (features, stack, scope, success criteria)

07:00 Builder (Opus 4 + aider)
  ├─ Spawn aider: --yes --model sonnet-4-5 --message "<spec>"
  ├─ Monitor: 5-hour timeout, poll every 30min
  ├─ Test: README, npm install, npm build, dist/ exists
  ├─ GitHub: gh repo create (private), git push
  └─ Update history.json with keywords for dedup

08:00 Morning Briefing
  └─ Compile: success (repo link) / rejection (reasoning) / failure (logs)
```

**First test run results:**

Input: 114 raw trends (HN: 70, Reddit: 44, X: 0)  
After dedup: 95 trends  
After filters: 94 trends (1 political rejected)  
Top 15 scored and ranked  

Selected: "privacy-first PDF tool" (buildability: 9/10)

Builder output:
- Project: pdf-privacy-tools
- Stack: TypeScript + Vite + pdf-lib + pdfjs-dist
- Features: merge, split, extract text, thumbnails, dark mode, responsive
- Build time: 7m 20s
- Cost: $0.47 (aider LLM usage)
- Files: 13
- Tests: all passing
- GitHub: https://github.com/jeevesbot-io/foundry-20260218-pdf-privacy-tools

**Interesting technical decisions:**

1. **Two-tier schema:** trends-summary.json (compact, 15 trends for Spec Writer) + trends-full/ (verbose, 94 files for debugging). Saves tokens.

2. **Graceful degradation:** If 1 source fails (e.g., X auth), continue with 2/3. Mark data_quality: "good". Don't block pipeline.

3. **Schema versioning:** All outputs include `schema_version: 1` for forward compatibility.

4. **aider in batch mode:** `--yes` flag runs non-interactively. Spawn via exec tool, poll for completion, capture exit code.

5. **Buildability scoring:** LLM-based but with explicit rubric. Not "rate this 1-10" but "score each dimension with clear criteria".

6. **Deduplication:** Keyword extraction (simple bag-of-words) + Jaccard similarity >50% + 14-day window. Prevents building the same thing twice.

**Performance:**

- End-to-end: 9m 58s (budget: 8 hours - 48x faster)
- Cost: $0.47/build (budget: $2 - 76% under)
- Speed: Haiku for scanning (cheap), Sonnet for evaluation (balanced), Opus for orchestration (expensive but reliable)

**Cron schedule:**

Daily at 00:00 GMT. 8-hour timeout. Isolated session. Delivers to Telegram on completion.

**First autonomous run:**

Tonight at midnight. No human in the loop. Full pipeline unsupervised.

**Why this is interesting:**

Not "can AI build apps" (we know it can). The question is: **can you automate the entire idea → MVP pipeline with current tools?**

Answer: yes, but you need:
- Explicit buildability rubrics (not vibes)
- Deduplication (or you build todo apps forever)
- Graceful failure modes (sources go down, aider times out)
- Two-phase eval (cheap scan + expensive judgment)
- Cost awareness (Haiku for volume, Opus for decisions)

**Open-source?**

Maybe. Currently local. Deciding whether to publish design docs + prompts. The code isn't novel (just orchestration), but the **architecture** might be useful.

Built on OpenClaw (agent framework) + Claude (Anthropic) + aider.

**Next 30 days:**

Run it every night. Track:
- Success rate (builds that actually work)
- Build diversity (are we just making CRUD apps?)
- Cost per build
- Dedup effectiveness (are we avoiding duplicates?)
- Human intervention needed (ideally zero)

Will report back in a month.

---

## Hacker News - Show HN Format

### Title
Show HN: The Foundry – Autonomous overnight builds from trending HN/Reddit pain points

### Body
I built an autonomous pipeline that scans HN and Reddit for trending developer pain points, scores buildability, and spawns an AI coding agent to build MVPs overnight.

First test run today: 10 minutes, $0.47, working app (pdf-privacy-tools: browser-based PDF toolkit). GitHub: https://github.com/jeevesbot-io/foundry-20260218-pdf-privacy-tools

Pipeline: Trend Scout (scans HN Algolia + Reddit JSON) → Spec Writer (picks one trend with buildability ≥7) → Builder (spawns aider to code it) → Morning Briefing (repo link or rejection reasoning).

Tech: Claude (Haiku for scanning, Sonnet for evaluation, Opus for orchestration) via OpenClaw, aider for code generation.

Cost: ~$0.50/build. Timeline: midnight → morning. First autonomous run: tonight.

Design → production in 24 hours (5 epics, 16 design docs, end-to-end tested).

The interesting question isn't "can AI build apps" (it can), it's "what happens when you give it 8 hours unsupervised with trending pain points every night for 30 days?"

Tomorrow we'll have the first data point.

---

## Meta - All Platforms Summary

**Core message:** Built an autonomous overnight app factory in 24 hours. First test run: 10 minutes, $0.47, working app. Tonight it runs for real.

**Proof points:**
- End-to-end tested with real data
- First build on GitHub (pdf-privacy-tools)
- Concrete numbers (7m 20s, $0.47, 13 files)
- Cron enabled, runs tonight

**Hook variations:**
- X: "You sleep → it builds"
- Threads: "Autonomous overnight app factory"
- LinkedIn: "Design → production in 24 hours"
- Reddit: "Wake up to a new GitHub repo"
- HN: "What happens when you give AI 8 hours unsupervised?"

**Platform-specific:**
- X: Thread format, punchy, no jargon
- Threads: Single post, visual, engaging
- LinkedIn: Professional, business impact, tech stack
- Reddit: Technical details, architecture, open questions
- HN: Minimal hype, focus on interesting problem, link to repo

**Call to action:**
- Tomorrow morning we'll share results
- First autonomous build will be public (if appropriate)
- Documenting everything for 30-day experiment

**Hashtags (LinkedIn only):**
#AI #Automation #OpenSource #Development #Claude #Anthropic

**Links:**
- First build: https://github.com/jeevesbot-io/foundry-20260218-pdf-privacy-tools
- OpenClaw: @OpenClawAI (X/Threads)
- Anthropic: @AnthropicAI (X), @anthropic-ai (Threads)

---

**Posting strategy:**

1. **Tonight (after midnight, before results):**
   - X: Thread announcing first autonomous run
   - Threads: Single post with same message
   
2. **Tomorrow morning (after first briefing):**
   - X: Thread with results (success or failure, full transparency)
   - LinkedIn: Full post-mortem
   - Reddit: r/SideProject post (if build is good)
   - HN: Show HN (if build is genuinely interesting)
   - Threads: Results update

3. **After 5 nights (Phase 1 exit):**
   - LinkedIn: "5 consecutive autonomous builds" update
   - Medium/blog: Full technical writeup
   - Reddit: r/programming (technical deep dive)

4. **After 30 nights:**
   - Full retrospective across all platforms
   - Data analysis: success rate, cost, build diversity
   - Lessons learned
   - Open-source decision

---

**Tone guide:**

- **Show, don't tell:** "7m 20s, $0.47, 13 files" > "incredibly fast and cheap"
- **No hype:** "First test run: SUCCESS" > "Revolutionary breakthrough"
- **Concrete:** "pdf-privacy-tools on GitHub" > "amazing app"
- **Humble:** "We'll find out tomorrow" > "This will change everything"
- **Transparent:** Share failures as openly as successes

**Nick's voice (from SOUL.md):**

- Relaxed, not stuffy
- Dry wit, British sensibility
- Commit to a take (no hedging)
- Concise (if it fits in one sentence, one sentence)
- Swear sparingly but authentically ("bloody brilliant" not "amazing")

**Example opening (Nick's voice):**

"Built an autonomous overnight app factory today. Sounds mental. Works though.

Scans HN + Reddit at midnight, picks a trending pain point, spawns aider to build it, pushes to GitHub. You wake up to either a new repo or a clear explanation of why it didn't ship.

First test: 10 minutes, 50 cents, working app.

Tonight it runs for real. No human in the loop. Just autonomous trend → code → GitHub.

What could possibly go wrong. 🏭"
