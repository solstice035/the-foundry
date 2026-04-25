# The Foundry 🏭

**Autonomous overnight app factory**

*"You sleep. We build."*

---

## What This Is

The Foundry is an autonomous multi-agent system that:
1. Scans trending developer pain points on X, Reddit, and Hacker News
2. Selects one buildable trend per night
3. Builds an MVP while you sleep (using Claude Code via ACP — free)
4. Pushes to GitHub and delivers a morning briefing

**Cost:** ~$40-55/month  
**Timeline:** 16 weeks to full implementation (4 months)  
**Output:** 1 build per night, 30+ apps per month

---

## Architecture

**Multi-agent pipeline:**
```
Trend Scout (Haiku) → Spec Writer (Sonnet) → Builder (Claude Code via ACP)
                ↓
        Morning Briefing (08:00)
```

**Three phases:**
- **Phase 1 (Weeks 1-4):** Core build pipeline (5 epics)
- **Phase 2 (Weeks 5-10):** Feedback loops (6 epics)
- **Phase 3 (Weeks 11-16):** Social amplification (5 epics)

**Total: 16 epics, 82-105 hours**

---

## Project Structure

```
the-foundry/
├── docs/           → Symlink to Obsidian design docs
├── src/            → Agent task prompts, utilities
├── scripts/        → Deployment, testing, utilities
├── config/         → Agent configs, cron schedules
├── tests/          → Agent testing, validation
└── README.md       → This file
```

---

## Documentation

**All design docs are in `docs/` (symlinked to Obsidian):**
- `README - Status & Next Steps.md` — Current status, approval flow
- `Implementation Plan - Epics.md` — 16 epics broken down
- `Agent Architecture.md` — All agent specifications
- `Builder-Coding-Agent Design.md` — Builder workflow detail
- `Deep Dive - Trend Research.md` — Source specifications
- `Independent review.md` — Comprehensive review with feedback

**23 total docs covering all phases.**

---

## Status

**Design:** ✅ Complete  
**Epics:** ✅ 16 in War Room (Mission Control)  
**Git Repo:** ✅ Initialized (no remote)  
**Implementation:** ⏸️ Awaiting approval

---

## Next Steps

1. **Approval:** Nick approves Phase 1 (or full project)
2. **Epic 1.1:** Trend Scout - Data Collection
3. **First autonomous night:** 1-2 weeks from start

---

## War Room

**View epics:** http://localhost:3333  
**Project filter:** "The Foundry"  
**Phases:** 3 (16 epics total)

---

## License

Private project. No public release planned.

---

**Created:** 2026-02-18  
**Last Updated:** 2026-02-18
