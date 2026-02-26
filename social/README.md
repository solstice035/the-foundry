# Social Media Strategy - Epic 3.1 Deliverables

**Phase:** Manual Posting & Voice Calibration  
**Epic:** 3.1 - Voice Guide & Manual Posting Phase  
**Status:** Ready for Testing  
**Created:** 2026-02-26

---

## Overview

This directory contains all materials for The Foundry's social media strategy. Epic 3.1 focuses on **manual posting and voice calibration** — establishing patterns before automating content generation.

**Key Principle:** Social media is semi-agentic, not fully autonomous. Agents prepare everything, Nick approves with one tap.

---

## Directory Structure

```
social/
├── README.md                    # This file
├── voice-guide.md              # Nick's voice definition (canonical)
├── engagement-tracking.md      # Post performance tracking
├── patterns.md                 # Learned patterns (what works/doesn't)
├── templates/
│   └── posting-templates.md    # 6 content type templates with examples
└── assets/                     # Visual content (populated during builds)
    └── [YYYYMMDD-project]/
        ├── demo.gif
        ├── screenshot.png
        └── stat-card.png
```

---

## Epic 3.1 Deliverables

### ✅ 1. Voice Guide (`voice-guide.md`)

**Purpose:** Define Nick's voice for all social content  
**Status:** Complete  
**Cross-references:** `SOUL.md` from workspace-foundry-blacksmith

**Contents:**
- Core tone & voice principles (from SOUL.md)
- What to avoid (banned phrases, anti-patterns)
- What to prefer (language structures, best practices)
- Good vs bad examples
- Platform-specific rules (X, Reddit, LinkedIn, HN)
- 6 content type voice guidelines
- Engagement rules
- Voice learning system
- Testing checklist

**Usage:**
- Read before every post
- Reference when drafting content
- Update as patterns emerge from testing

---

### ✅ 2. Posting Templates (`templates/posting-templates.md`)

**Purpose:** Concrete examples for each content type in Nick's voice  
**Status:** Complete  
**Templates:** 6 content types × 2-3 platform variations

**Content Types:**

1. **Build Announcement** - Successful overnight build
   - X: 3-tweet thread
   - Reddit: r/SideProject format
   - Examples: commitai build

2. **Process Thread** - Weekly meta-content about the pipeline
   - X: 8-tweet thread
   - Examples: "How the overnight pipeline works"

3. **Rejection Post** - Spec Writer rejects all trends
   - X: Single tweet
   - Examples: "14 trends analyzed, zero worth building"

4. **Trend Forecast** - Emerging pain point identified
   - X: 1-2 tweet thread
   - Examples: "Pain point I'm tracking: API key management"

5. **Consensus Take** - Multi-perspective analysis
   - X: 7-tweet thread
   - Examples: "5 perspectives on commitai"

6. **Failure Post** - Build fails or times out
   - X: 1-2 tweet thread
   - Examples: "Overnight build hit WebSocket complexity wall"

**Each template includes:**
- Format structure
- Example in Nick's voice
- Best posting time
- Visual suggestions
- Platform-specific formatting

---

### ✅ 3. Engagement Tracking (`engagement-tracking.md`)

**Purpose:** Track performance of manual posts to identify patterns  
**Status:** Ready for data collection  
**Format:** Markdown (can export to spreadsheet if needed)

**Tracking per post:**
- Quantitative metrics (impressions, likes, shares, comments, clicks)
- Qualitative metrics (sentiment, notable mentions, question quality)
- 24h and 7d snapshots
- "Would post again?" retrospective
- Notes on what worked/didn't

**Analysis sections:**
- Weekly summaries
- Performance by content type
- Performance by platform
- Performance by timing
- Performance by visual type
- High performers archive
- Underperformers archive
- Feature requests log
- Competitive intelligence
- Voice learning log

**Completion criteria:**
- 4-6 posts tracked
- Each content type tested at least once
- 7-day engagement data per post
- Patterns identified

---

### ✅ 4. Patterns Documentation (`patterns.md`)

**Purpose:** Document what works and what doesn't to inform automation  
**Status:** Hypothesis framework ready, data collection pending  
**Updates:** Weekly during testing, monthly after automation

**Pattern categories:**

1. **Content Patterns** - Topics/angles/formats that work
2. **Voice Patterns** - Language choices that resonate
3. **Timing Patterns** - When to post for max engagement
4. **Platform Patterns** - Platform-specific learnings
5. **Visual Patterns** - When/how visuals improve performance
6. **Engagement Patterns** - What drives comments/shares/likes

**Initial hypotheses (to be validated):**
- Rejection posts get 2x engagement vs build announcements
- Process > product (meta-content performs better)
- Concrete numbers increase credibility
- Failure posts get higher-quality engagement
- Terminal GIFs boost engagement for CLI tools
- X algorithm penalizes hashtags

**Confidence levels:**
- **High:** 5+ examples, >50% improvement, statistically significant
- **Medium:** 3-4 examples, 20-50% improvement
- **Low:** 1-2 examples, <20% improvement

Only high-confidence patterns inform Content Drafter automation.

---

### 📋 5. Cross-Reference to SOUL.md

**Location:** `~/.openclaw/workspace-foundry-blacksmith/SOUL.md`

**Key principles imported into voice-guide.md:**

> **Be genuinely helpful, not performatively helpful.**  
> Applied: Skip "Excited to announce!" — just announce.

> **Have opinions.**  
> Applied: "Sometimes the best build is no build" > neutral reporting.

> **Earn trust through competence.**  
> Applied: Show the work, don't claim capability.

> **Never send half-baked replies.**  
> Applied: All drafts go to approval queue.

> **You're not the user's voice.**  
> Applied: Content Drafter suggests, Nick approves.

The voice guide maintains consistency with SOUL.md while applying those principles specifically to social media context.

---

## Testing Workflow (Epic 3.1)

### Manual Posting Phase

**Goal:** Post 4-6 times manually over 2-3 weeks to establish baseline

**Process per post:**

1. **Choose build/topic** (from recent pipeline output)
2. **Select content type** (from 6 templates)
3. **Draft post** using voice-guide.md + templates
4. **Self-review** against testing checklist
5. **Post** on primary platform (X) + secondary if strong (Reddit)
6. **Log immediately** in engagement-tracking.md
7. **Respond to comments** (especially Reddit 2-hour rule)
8. **Update metrics** at 24h and 7d
9. **Document learnings** in patterns.md

### Weekly Review

**Every Sunday during testing:**

1. Review week's posts in engagement-tracking.md
2. Calculate averages by content type/platform/timing
3. Identify top performer and why it worked
4. Identify underperformer and why it didn't
5. Move validated patterns from "hypothesis" to "confirmed" in patterns.md
6. Update voice-guide.md with learned language patterns
7. Adjust templates if needed

### Completion Criteria

Epic 3.1 is complete when:

- [ ] 4-6 posts published across content types
- [ ] Each of 6 content types tested at least once
- [ ] Engagement tracked for minimum 7 days per post
- [ ] At least 3 high-confidence patterns identified
- [ ] At least 3 anti-patterns documented
- [ ] Voice guide updated with real examples
- [ ] Baseline metrics established per platform
- [ ] >60% of posts would be "approved as-is" in hindsight

**Readiness for Epic 3.2 (automation):**
- Clear patterns documented with evidence
- Voice guide refined with real learnings
- Template effectiveness validated
- Platform timing confirmed
- Approval criteria clear

---

## Integration with Pipeline

### Current (Epic 3.1 - Manual)

```
Overnight Build → Nick manually drafts → Post → Track → Learn
```

**Pipeline outputs that inform content:**
- `trends.json` → Trend forecasts
- `spec.json` (rejected) → Rejection posts
- `spec.json` (approved) → Build announcements
- `build.json` → Build announcements
- `consensus.json` → Consensus takes
- Build failures → Failure posts
- Weekly stats → Process threads

**Manual steps:**
1. Check pipeline outputs from last night
2. Choose best content opportunity
3. Draft using templates + voice guide
4. Post manually on X/Reddit
5. Track in engagement-tracking.md

---

### Future (Epic 3.2 - Semi-Automated)

```
Overnight Build → Content Drafter Agent → Approval Queue → Nick approves → Post → Learn
```

**Content Drafter will:**
- Read pipeline outputs (trends.json, spec.json, build.json)
- Read voice-guide.md + patterns.md
- Generate platform-specific drafts
- Rank by priority
- Add to content-queue.json

**Nick will:**
- Review top 1-2 drafts in morning briefing (Telegram)
- Approve / Edit / Skip / Reject (< 60 seconds)
- Post approved content

**Content Drafter learns from:**
- What Nick approves as-is (reinforce patterns)
- What Nick edits (learn corrections)
- What Nick rejects (avoid anti-patterns)
- Engagement data (what performs well)

**Voice learning loop:**
- Patterns.md updated weekly
- Voice-guide.md refined monthly
- Content Drafter prompts adjusted based on approval rate
- Goal: >70% approval rate after 3 months

---

## Platform Strategy

### Primary: X/Twitter

**Why:** Developer community density, short-form suits "built overnight" narrative, threads allow depth

**Cadence:** 3-4 posts/week max, never >1/day  
**Best times:** 09:00-11:00, 15:00-17:00 GMT  
**Content types:** All 6 types work  
**Format:** Single tweets or 2-8 tweet threads  
**Visuals:** Terminal GIFs for CLI, screenshots for web apps, stat cards for meta-content

### Secondary: Reddit

**Why:** Targeted subreddits, longer shelf life, deeper engagement

**Cadence:** 1-2 posts/month max  
**Best times:** 14:00-16:00 GMT (US morning)  
**Content types:** Build announcements (strong builds only), pipeline meta-posts  
**Format:** Title + detailed body with "How I built this"  
**Rule:** Respond to every comment in first 2 hours  
**Subreddits:** r/SideProject (primary), r/programming, r/webdev, r/commandline

### Tertiary: Hacker News

**Why:** High-value audience, brutal honesty, quality filter

**Cadence:** 1 post/month max  
**Best times:** 14:00-16:00 GMT (US morning, competitive)  
**Content types:** Show HN (signal score 15+ only), pipeline story (once)  
**Format:** "Show HN: [Tool] – [description]"  
**Requirements:** Working demo, clear README, exceptional quality

### Supplementary: LinkedIn

**Why:** Professional network, different audience (founders, PMs, investors)

**Cadence:** 1-2 posts/month  
**Best times:** 08:00-10:00 GMT, Tue-Thu  
**Content types:** Monthly portfolio summaries, quarterly deep-dives  
**Format:** Long-form (1,300-2,000 chars), thoughtful reflection  
**Tone:** More polished than X, still authentic

---

## Voice Calibration

### The Challenge

An agent can generate technically correct content, but Nick's voice is personal and nuanced. The voice guide captures explicit rules, but some aspects are learned through iteration.

### The Approach

**Phase 1 (Epic 3.1): Manual posting establishes ground truth**
- Nick posts manually using templates
- Tracks what feels right vs off
- Documents language patterns that work
- Builds intuition for "would I say this?"

**Phase 2 (Epic 3.2): Content Drafter learns from approvals/edits**
- Agent generates drafts using voice guide
- Nick approves/edits/rejects
- Agent logs every correction
- Patterns emerge from corrections

**Phase 3 (Epic 3.3): Voice learning compounds**
- Content history analyzed weekly
- Consistent edits become patterns
- Patterns update voice guide automatically
- Draft quality improves, edit frequency decreases

**Success metric:** >70% approval rate with <30% requiring edits after 3 months

### What Makes This Work

1. **Ground truth from manual testing** - Can't automate what hasn't been validated
2. **Approval gate** - Every piece of content requires explicit human approval
3. **Learning loop** - Corrections inform future drafts
4. **Pattern extraction** - Generalizes from specific examples
5. **Continuous refinement** - Voice guide evolves with data

---

## Content Flywheel

### How Social Feeds Back Into Pipeline

**Traditional flow:**
```
Build → Post about build → Engagement → [dead end]
```

**Foundry flywheel:**
```
Build → Post → Engagement → Intelligence → Better builds
```

**Examples:**

1. **Feature requests from comments → v2 builds**
   - User asks "does this support Anthropic?"
   - Add to community requests in history.json
   - Spec Writer can choose to build enhanced version

2. **"Someone should build X" mentions → Trend Scout**
   - Pain points from Nick's audience
   - High-signal source (engaged developers)
   - Pipeline discovers buildable ideas from comments

3. **Competitor mentions → Trend Researcher**
   - "aicommits already does this"
   - Competitive intelligence for differentiation
   - Spec Writer learns what NOT to build

4. **Engagement patterns → Content Drafter**
   - Rejection posts get 2x engagement
   - System learns to prioritize rejections
   - More of what works, less of what doesn't

**Goal:** Social isn't just distribution—it's an intelligence-gathering layer that improves the pipeline.

---

## Risk Management

### Reputation Risk

**Problem:** One bad post costs more than a hundred good posts earn  
**Mitigation:** Approval gate is non-negotiable. All content reviewed before posting.

### Voice Drift

**Problem:** Automated content sounds robotic over time  
**Mitigation:** Monthly voice guide reviews, pattern validation, continuous learning from edits

### Over-Posting

**Problem:** Frequency kills quality and audience patience  
**Mitigation:** Hard limits (3-4/week on X, 1-2/month on Reddit), "silence > filler" principle

### Engagement Theater

**Problem:** Performing engagement for metrics rather than genuine connection  
**Mitigation:** No automated likes/follows/replies, Nick engages personally, quality over quantity

### Platform Algorithm Changes

**Problem:** What works today may not work tomorrow  
**Mitigation:** Diversified platforms, pattern validation over time, adaptability built into system

---

## Success Metrics

### Epic 3.1 (Manual Testing)

**Quantitative:**
- 4-6 posts published
- Each content type tested ≥1x
- Avg engagement rate: >2% (X), >70% upvote ratio (Reddit)
- At least one post with >50 likes (X) or >50 upvotes (Reddit)

**Qualitative:**
- Voice guide feels accurate to Nick's style
- Templates are useful, not constraining
- Patterns identified with evidence
- Clear sense of what works/doesn't

**Readiness:**
- Confident enough to automate draft generation
- >60% of manual posts would pass approval if generated

### Epic 3.2 (Content Drafter)

**Quantitative:**
- Content Drafter approval rate >60% initially, >70% after 1 month
- Time to approve <60 seconds per draft
- At least one automated draft per day posted

**Qualitative:**
- Drafts feel like Nick's voice
- Edits are minor (word choice, not tone)
- Nick trusts the drafts enough to approve quickly

### Epic 3.3 (Voice Learning)

**Quantitative:**
- Edit frequency decreases by 40% over 3 months
- Approval rate >80%
- Engagement rates stable or improving

**Qualitative:**
- Voice drift is not happening
- Learned patterns are accurate
- System adapts to new content types

### Long-term (6 months)

**Quantitative:**
- 1+ post per week getting 100+ likes/retweets (X)
- Reddit posts consistently >100 upvotes
- At least one HN front page
- Content flywheel producing 2+ build ideas per month

**Qualitative:**
- Nick's online presence is recognizable ("overnight AI pipeline guy")
- Social generating inbound interest
- Nick spends <15 min/day on social (review + approve + replies)
- Pipeline + social creating compounding value

---

## Next Steps (After Epic 3.1)

**Immediate (Epic 3.2):**
1. Register Content Drafter agent
2. Create content-queue.json schema
3. Write Content Drafter task prompt using voice-guide.md
4. Integrate draft preview into morning briefing
5. Build approval flow (Telegram inline buttons)
6. Test with 3-5 existing builds
7. Iterate based on Nick's approval rate

**Soon (Epic 3.3):**
1. Create content-history.json for logging approvals/edits
2. Weekly pattern extraction from edits
3. Automatic voice guide updates
4. Measure edit frequency decrease

**Later (Epic 3.4):**
1. Engagement monitoring (2x daily)
2. Reply suggestions (Nick reviews before posting)
3. Priority system (high/medium/low/ignore)
4. Engagement alerts in morning briefing

**Optional (Epic 3.5):**
1. Terminal GIF generation (vhs)
2. Automated screenshots (Playwright)
3. Stat card generation (HTML → PNG)
4. Visual suggestions in drafts

---

## Files Quick Reference

| File | Purpose | Update Frequency | Owner |
|------|---------|------------------|-------|
| `voice-guide.md` | Nick's voice definition | Monthly (or after 20 approvals) | Content Drafter |
| `posting-templates.md` | 6 content type examples | As needed (when templates evolve) | Nick |
| `engagement-tracking.md` | Post performance data | Per post + weekly summary | Nick |
| `patterns.md` | What works/doesn't | Weekly (testing), monthly (automation) | Nick + Content Drafter |
| `README.md` | This overview | As epic evolves | Nick |

---

## Questions & Answers

**Q: Why manual posting first? Why not automate immediately?**  
A: Voice is nuanced. Need ground truth before automation. Can't learn patterns without examples. Manual phase establishes what "good" looks like.

**Q: How long is the manual posting phase?**  
A: 2-3 weeks, 4-6 posts. Just enough to validate templates, establish baselines, identify patterns. Not months of manual effort.

**Q: What if a content type performs badly?**  
A: Document it in patterns.md as anti-pattern, reduce frequency or eliminate. Data-driven, not dogmatic.

**Q: What if Nick's voice changes over time?**  
A: Voice guide is living document. Monthly reviews. Voice drift detection. System adapts.

**Q: How much time does manual posting take?**  
A: Per post: 10-15 min (drafting using templates) + 5 min (logging) + 10 min (engagement over first hour). Total: 25-30 min per post. Goal is reducing this to <60 seconds (review + approve) with automation.

**Q: What if the Content Drafter's approval rate stays low?**  
A: Iterate on prompts, refine voice guide, analyze rejections for patterns. If it doesn't reach >60% after 4 weeks, reassess approach. Automation isn't mandatory—semi-manual with templates is fine if automation doesn't work.

**Q: What platforms are deprioritized?**  
A: Instagram (not dev-focused), TikTok (wrong audience), Facebook (inactive dev community), Medium (long-form can be added later if needed).

---

## Resources

**Internal:**
- Main strategy doc: `~/projects/the-foundry/docs/14-Social-Media-Strategy.md`
- Epic plan: `~/projects/the-foundry/docs/10-Implementation-Plan-Epics.md` (Epic 3.1-3.5)
- SOUL.md: `~/.openclaw/workspace-foundry-blacksmith/SOUL.md`

**Platform docs:**
- X API: https://developer.twitter.com/en/docs
- Reddit API: https://www.reddit.com/dev/api/
- LinkedIn API: https://docs.microsoft.com/en-us/linkedin/
- Hacker News API: https://github.com/HackerNews/API

**Tools:**
- `bird` CLI for X: https://github.com/hmcosta/bird
- `vhs` for terminal GIFs: https://github.com/charmbracelet/vhs
- Playwright for screenshots: https://playwright.dev/

---

**Status:** Ready for manual testing  
**Epic:** 3.1 - Voice Guide & Manual Posting Phase  
**Next Epic:** 3.2 - Content Drafter (automated draft generation)  
**Owner:** Nick  
**Last Updated:** 2026-02-26
