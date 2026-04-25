# Social Media Patterns - What Works & What Doesn't

**Version:** 1.1
**Last Updated:** 2026-03-05  
**Purpose:** Document learned patterns from manual posting to inform Content Drafter automation  
**Status:** Living document (updated weekly during testing, monthly after automation)

---

## Overview

This document captures patterns discovered through manual posting and engagement tracking. These patterns will:

1. **Inform Content Drafter's generation logic** (what to emphasize, what to avoid)
2. **Update voice-guide.md** (refine tone based on what resonates)
3. **Guide platform prioritization** (where to focus effort)
4. **Improve approval rates** (Nick approves drafts that match proven patterns)

**Patterns are evidence-based, not assumptions.** Each pattern should reference specific posts or data from `engagement-tracking.md`.

---

## Pattern Categories

1. **Content Patterns** - What topics/angles/formats work
2. **Voice Patterns** - Specific language/tone choices that resonate
3. **Timing Patterns** - When to post for maximum engagement
4. **Platform Patterns** - Platform-specific learnings
5. **Visual Patterns** - When/how visuals improve performance
6. **Engagement Patterns** - What drives comments/shares vs passive likes

---

## 🎯 Content Patterns

### What Works

_This section will be populated during manual testing phase based on engagement data_

**Baseline Observations (from 12 pipeline runs, pre-posting):**

These aren't validated engagement patterns yet — they're quantitative observations from the build pipeline that can inform content strategy. They'll be validated once actual posts go live.

| Metric | Value | Content Angle |
|--------|-------|---------------|
| Build success rate | 91.7% (11/12) | Reliability narrative |
| Average build cost | $0.41 (range $0.00-$0.58) | "Less than a coffee" |
| Average pipeline duration | ~13 min | "While you make coffee" |
| Consecutive successes | 10 (since 02-26) | Streak narrative |
| Category breakdown | 8 CLI, 1 web, 1 API, 2 dev-tools | Terminal-native audience |
| Source breakdown | 8 Reddit, 2 HN, 2 X | Reddit as primary signal |
| Top engagement builds | ai-code-guard (244.0), deptox (120.9), reddit-keyword-monitor (85.0) | Security tools resonate |

**Observations worth testing as content:**
1. Security-themed tools (ai-code-guard, deptox, vibe-check, ai-deploy-guard) consistently score highest engagement — security angle may resonate with dev audience
2. CLI category dominates — "terminal-native" positioning aligns with audience
3. Build costs are concrete and shareable ($0.34-$0.57 per build)
4. The 10-night streak itself is a story ("10 consecutive overnight builds, zero failures")
5. Reddit is overwhelmingly the best signal source — worth mentioning in process threads

**Initial Hypotheses (to be validated):**

1. **Rejection posts > Build announcements**
   - Hypothesis: Showing what you chose NOT to do is more engaging than showing what you did
   - Reasoning: Counterintuitive, shows judgment, invites disagreement
   - Test: Compare engagement rates between rejection posts and build announcements
   - Status: ⏳ Untested

2. **Process > Product**
   - Hypothesis: "How the pipeline works" threads get more engagement than "what it built" threads
   - Reasoning: The meta-story (building the thing that builds things) is more novel
   - Test: Compare process threads vs build announcement threads
   - Status: ⏳ Untested

3. **Concrete numbers increase credibility**
   - Hypothesis: Posts with specific metrics (time, cost, stars) perform better than vague descriptions
   - Reasoning: Specificity signals authenticity
   - Test: A/B test announcements with/without numbers
   - Status: ⏳ Untested

4. **Failure posts get higher-quality engagement**
   - Hypothesis: Posts about failures get fewer likes but better comments
   - Reasoning: Vulnerability invites genuine discussion vs performative praise
   - Test: Compare comment quality (questions, insights) between failure and success posts
   - Status: ⏳ Untested

5. **Early trend forecasts position as thought leader**
   - Hypothesis: Identifying emerging pain points before they peak builds credibility
   - Reasoning: "I spotted this before it was trending" > "here's what's trending now"
   - Test: Track whether forecast posts lead to follower growth
   - Status: ⏳ Untested

6. **Multi-perspective analysis is uncommon format**
   - Hypothesis: Consensus posts stand out because the format is unusual
   - Reasoning: Novelty drives engagement, showing internal debate is interesting
   - Test: Compare consensus posts to standard analysis
   - Status: ⏳ Untested

---

**Validated Patterns:**

_Will populate here after manual testing with format:_

```markdown
**Pattern: [Name]**
- Evidence: Post #X, #Y (links to engagement-tracking.md)
- Data: [Specific metrics]
- Reasoning: [Why this works]
- Application: [How Content Drafter should use this]
- Confidence: High/Medium/Low
```

---

### What Doesn't Work

_This section will be populated during manual testing phase based on underperforming posts_

**Initial Anti-Patterns (to be validated):**

1. **Generic enthusiasm kills credibility**
   - Hypothesis: Posts with "excited to share!" perform worse
   - Reasoning: Sounds corporate, not authentic
   - Test: Track any posts that slip into this language
   - Status: ⏳ Untested

2. **Multiple posts per day cannibalize reach**
   - Hypothesis: Posting twice in one day reduces both posts' performance
   - Reasoning: Algorithm penalizes frequency, audience gets fatigued
   - Test: Compare engagement when spacing posts 24h+ apart
   - Status: ⏳ Untested

3. **Hashtags on X reduce reach**
   - Hypothesis: Hashtags make posts look spammy
   - Reasoning: Dev Twitter culture avoids hashtags
   - Test: Track any posts that use hashtags
   - Status: ⏳ Untested

4. **Too-long threads lose readers**
   - Hypothesis: Threads over 8 tweets have high drop-off
   - Reasoning: Attention span limits
   - Test: Track completion rate (replies on last tweet vs first)
   - Status: ⏳ Untested

5. **Posting without visuals hurts reach on X**
   - Hypothesis: Text-only posts get 30-50% fewer impressions
   - Reasoning: X's algorithm favors media
   - Test: Compare impressions with/without visuals
   - Status: ⏳ Untested (but widely reported)

6. **Cross-posting identical content fails**
   - Hypothesis: Same content on X and Reddit performs worse than platform-specific versions
   - Reasoning: Different platform cultures
   - Test: Compare engagement when tailoring vs reusing content
   - Status: ⏳ Untested

---

**Validated Anti-Patterns:**

_Will populate here after manual testing with format:_

```markdown
**Anti-Pattern: [Name]**
- Evidence: Post #X, #Y (links to engagement-tracking.md)
- Data: [Specific metrics showing poor performance]
- Reasoning: [Why this doesn't work]
- Avoidance: [How Content Drafter should avoid this]
- Confidence: High/Medium/Low
```

---

## 🗣️ Voice Patterns

### Language That Resonates

_This section captures specific word choices, phrase structures, and tone elements that perform well_

**Initial Voice Preferences (from voice-guide.md):**

- "Built this" > "Launched this" > "Shipped this"
- "My AI pipeline" > "My build pipeline" > "My autonomous system"
- Em dash (—) > semicolon
- Short first tweet (<180 chars)
- No exclamation marks
- No "excited" or "thrilled"
- Direct statements > questions
- Specific > vague ("3h 12m" > "quickly")

**To Validate:**

- Does understatement actually work better than enthusiasm?
- Do technical details increase or decrease engagement?
- Does dry humor land, or does it confuse?

---

**Validated Voice Wins:**

_Will populate here with examples of language choices that performed well_

```markdown
**Example: [Description]**
- Post: #X
- What was said: [Quote]
- Why it worked: [Analysis]
- Pattern to reinforce: [Guideline for Content Drafter]
```

---

### Language That Falls Flat

_This section captures word choices or phrases that didn't resonate_

**To Avoid (from voice-guide.md):**

- "Excited to announce"
- "Thrilled to share"
- "Great question!"
- "Let me explain why this matters"
- Excessive emoji use
- Corporate speak

**To Validate:**

- Are there other phrases that kill engagement?
- Do certain technical jargon terms alienate vs engage?

---

**Validated Voice Failures:**

_Will populate here with examples of language that underperformed_

```markdown
**Example: [Description]**
- Post: #X
- What was said: [Quote]
- Why it failed: [Analysis]
- Pattern to avoid: [Guideline for Content Drafter]
```

---

## ⏰ Timing Patterns

### Best Posting Times

**Platform-specific hypotheses:**

| Platform | Best Times (GMT) | Reasoning |
|----------|------------------|-----------|
| X | 09:00-11:00, 15:00-17:00 | Dev morning scroll, afternoon break |
| Reddit | 14:00-16:00 | US morning (where most devs are) |
| LinkedIn | 08:00-10:00 Tue-Thu | Professional browsing time |
| HN | 14:00-16:00 | US morning, competitive |

**To Validate:**

- Track actual performance by time slot
- Compare weekday vs weekend
- Identify platform-specific peaks

---

**Validated Timing Patterns:**

_Will populate with data from engagement-tracking.md_

```markdown
**Pattern: [Platform] performs best at [Time]**
- Evidence: Posts #X, #Y, #Z
- Data: Avg impressions at this time vs other times
- Confidence: High/Medium/Low
```

---

### Timing Anti-Patterns

**Hypotheses to validate:**

- Posting late night (23:00+) kills reach
- Posting midday (12:00-14:00 GMT) is dead zone
- Posting Friday evening gets lost in weekend noise
- Reddit posts at UK daytime (when US is asleep) underperform

---

**Validated Timing Failures:**

_Will populate with examples of bad timing choices_

```markdown
**Anti-Pattern: [Description]**
- Evidence: Post #X
- Time posted: [Time]
- Performance: [Metrics vs baseline]
- Lesson: [What to avoid]
```

---

## 📱 Platform Patterns

### X/Twitter Learnings

**Platform characteristics:**
- Fast-moving feed, short attention span
- Algorithm favors media (images, GIFs, videos)
- Threads allow depth but need strong hook
- Developer community is dense here
- Dry humor and directness work well

**Hypotheses:**

1. First tweet determines thread performance (hook is everything)
2. Links in first tweet kill reach (algorithm penalizes outbound links)
3. Quote tweets of your own content look desperate
4. Replying to your own thread within 10 min boosts it
5. Visual content in tweet 2 (not 1) maintains credibility while getting algo boost

**To Track:**

- Engagement rate by thread length
- Impressions with vs without media
- Performance of single tweets vs threads
- Reply timing impact

---

**Validated X Patterns:**

_Will populate during testing_

---

### Reddit Learnings

**Platform characteristics:**
- Slower-moving than X, longer shelf life
- Community-specific cultures
- Hates self-promotion unless value-added
- Loves process and technical depth
- OP engagement in first 2h is critical

**Hypotheses:**

1. Posts with "How I built this" section perform better
2. Responding to all comments in first 2h boosts ranking
3. r/SideProject is more forgiving than r/programming
4. Posts on weekends get buried
5. Title clarity matters more than cleverness

**To Track:**

- Upvote ratio by subreddit
- Performance with/without "How I built" section
- Engagement correlation with OP reply speed
- Shelf life (upvotes over 7 days vs 24h)

---

**Validated Reddit Patterns:**

_Will populate during testing_

---

### LinkedIn Learnings

**Platform characteristics:**
- Professional network, less technical than X/Reddit
- Monthly summaries work better than frequent posts
- Longer form acceptable
- Different audience (founders, PMs, recruiters vs devs)

**Hypotheses:**

1. Portfolio summaries outperform individual build posts
2. Tuesday-Thursday mornings best
3. Hashtags work here (unlike X)
4. Personal reflection angle works well

**To Track:**

- View count by content type
- Engagement rate vs X/Reddit
- Follower demographics (if visible)

---

**Validated LinkedIn Patterns:**

_Will populate during testing_

---

### Hacker News Learnings

**Platform characteristics:**
- Brutally honest feedback
- Extremely high quality bar
- "Show HN" format is sacred
- Front page is competitive
- Community punishes over-posting

**Hypotheses:**

1. Only post builds with signal score 15+
2. Working demo is non-negotiable
3. Being in comments immediately after posting helps
4. Timing is critical (weekday mornings US time)
5. The pipeline story will do better than individual tools

**To Track:**

- Point threshold for front page
- Comment sentiment
- Best time to post

---

**Validated HN Patterns:**

_Will populate during testing (likely very limited data in Epic 3.1)_

---

## 🖼️ Visual Patterns

### When Visuals Help

**Hypotheses:**

1. **Terminal GIFs for CLI tools:** Demonstrate functionality better than text
2. **Architecture diagrams for process threads:** Make abstract concepts concrete
3. **Before/after comparisons:** Show transformation/improvement
4. **Stat screenshots:** Make numbers more shareable

**To Validate:**

- Compare engagement with vs without visuals
- Track which visual types get saved/shared most
- Identify posts where visual was critical vs nice-to-have

---

**Validated Visual Wins:**

_Will populate with examples_

```markdown
**Pattern: [Visual type] increases [metric] by [amount]**
- Evidence: Posts #X vs #Y
- Visual type: [Terminal GIF / Screenshot / Diagram / etc]
- Performance delta: [Specific improvement]
- Application: [When Content Drafter should suggest this visual]
```

---

### When Visuals Don't Help (or Hurt)

**Hypotheses:**

1. **Rejection posts:** Text-only maintains seriousness
2. **Trend forecasts:** Visual would distract from thought leadership
3. **Generic screenshots:** Add nothing if they don't show key feature
4. **AI-generated images:** Look cheap, hurt credibility

**To Validate:**

- Track posts where visual didn't improve engagement
- Identify when text-only outperforms media

---

**Validated Visual Failures:**

_Will populate with examples_

```markdown
**Anti-Pattern: [Visual type] in [context] doesn't help**
- Evidence: Post #X
- Visual type: [Description]
- Performance: [Same or worse than text-only baseline]
- Lesson: [When to avoid visuals]
```

---

## 💬 Engagement Patterns

### What Drives Comments

**Hypotheses:**

1. **Asking genuine questions:** (not engagement bait "What do you think?")
2. **Acknowledging limitations:** Invites suggestions
3. **Controversial opinions:** Polite disagreement drives discussion
4. **Technical details:** Depth attracts technical discussion
5. **Failure posts:** Vulnerability invites sharing similar experiences

**To Validate:**

- Track comment count by post type
- Analyze comment quality (technical questions vs praise)
- Identify posts that sparked genuine discussion

---

**Validated Comment Drivers:**

_Will populate with examples_

---

### What Drives Shares

**Hypotheses:**

1. **Counterintuitive takes:** "I rejected everything" is shareable
2. **Novel formats:** Consensus analysis stands out
3. **Useful tools:** If it solves a real problem, people share it
4. **Process threads:** "Here's how I did X" is share-worthy
5. **Concrete numbers:** Specific data gets shared

**To Validate:**

- Track retweet/share count by content type
- Identify what makes content feel "share-worthy"

---

**Validated Share Drivers:**

_Will populate with examples_

---

### What Drives Passive Engagement (Likes/Saves)

**Hypotheses:**

1. **Build announcements:** People like to support, but don't always comment
2. **Relatable pain points:** "I feel that" liking
3. **Quick wins:** Saves for later ("I'll check this out")
4. **Clever one-liners:** Appreciation without needing to reply

**To Validate:**

- Track like:comment ratio by content type
- Identify what gets saved (bookmark feature on X)

---

**Validated Passive Engagement Patterns:**

_Will populate with examples_

---

## 🔄 Iteration & Refinement

### How This Document Evolves

**Weekly during testing:**
1. Review engagement-tracking.md
2. Identify patterns (min 2 examples to establish pattern)
3. Move hypotheses to "Validated" sections with evidence
4. Add new hypotheses based on observations
5. Update voice-guide.md with learned patterns

**Monthly after automation:**
1. Review content-history.json (from automated drafts)
2. Track what Nick approves vs edits vs rejects
3. Refine patterns based on approval rates
4. Update Content Drafter prompts to reinforce successful patterns

---

### Confidence Levels

**High Confidence:**
- Pattern observed in 5+ posts
- Consistent across different builds/contexts
- Statistically significant difference (>50% improvement)
- Aligns with platform best practices

**Medium Confidence:**
- Pattern observed in 3-4 posts
- Some variation in results
- Moderate improvement (20-50%)
- Plausible but needs more data

**Low Confidence:**
- Pattern observed in 1-2 posts
- Could be coincidence
- Small improvement (<20%)
- Needs validation

Only **High Confidence** patterns should inform Content Drafter's core logic.  
**Medium Confidence** patterns can be tested in drafts.  
**Low Confidence** patterns are tracked but not acted on.

---

### Pattern Invalidation

If a pattern is tested and fails:

1. Document the failure in the appropriate "What Doesn't Work" section
2. Remove it from "What Works" if it was there
3. Add it to Content Drafter's avoidance list
4. Note the evidence for future reference

**Example:**

```markdown
**Invalidated Pattern: Terminal GIFs always increase engagement**
- Original hypothesis: Visual content boosts reach
- Test: Posts #12, #15, #18 with terminal GIFs
- Result: No significant improvement vs text-only (3% increase, within margin)
- New understanding: GIFs help only when they demonstrate complex interaction
- Updated guideline: Use GIFs only for multi-step workflows, not simple commands
```

---

## 📊 Success Metrics for Patterns

A pattern is "successful" if it:

1. **Increases approval rate:** Nick approves content using this pattern at >70%
2. **Improves engagement:** Posts using this pattern beat baseline by >30%
3. **Applies broadly:** Works across multiple builds/contexts
4. **Guides automation:** Content Drafter can apply it reliably

---

## 🎯 Current Focus Areas

**During Epic 3.1 (Manual Testing):**

- [ ] Validate top 3 content hypotheses
- [ ] Establish baseline engagement rates per platform
- [ ] Identify at least one high-confidence pattern per category
- [ ] Test all 6 content types at least once
- [ ] Document at least 3 clear anti-patterns to avoid

**For Epic 3.2 (Content Drafter Automation):**

- [ ] High-confidence patterns integrated into Content Drafter prompts
- [ ] Anti-patterns added to Content Drafter's avoidance list
- [ ] Voice-guide.md updated with validated language patterns
- [ ] Platform-specific rules refined based on data

---

## Quick Reference: Pattern Summary

_This section will be populated as patterns are validated. It serves as a quick lookup for Content Drafter._

### Top 5 Pre-Validation Observations (Content Angles)

1. Security tools get highest engagement scores (244.0, 120.9, 82.3)
2. Build cost <$0.60 is concrete, shareable, and counterintuitive
3. CLI-heavy output matches dev Twitter audience preferences
4. 10-night success streak has narrative power
5. Reddit as signal source creates a meta-loop worth discussing

### Top 5 Validated "Avoid This" Patterns

1. _To be determined after manual posting_
2. _To be determined_
3. _To be determined_
4. _To be determined_
5. _To be determined_

---

## Update Log

**v1.1 (2026-03-05):**
- Added baseline observations from 12 pipeline runs
- Seeded quantitative data for content strategy
- Updated Quick Reference with pre-validation observations

**v1.0 (2026-02-26):**
- Initial patterns document created
- Hypotheses defined for testing
- Pattern categories established
- Validation framework created

**Future updates:**
- Weekly during Epic 3.1 testing phase
- Monthly after Content Drafter automation
- Major revisions when significant new patterns emerge

---

**Status:** Active (Testing Phase)  
**Owner:** Nick (during testing), Content Drafter (during automation)  
**Integration:** Feeds into voice-guide.md and Content Drafter prompts  
**Review Frequency:** Weekly during testing, monthly during automation
