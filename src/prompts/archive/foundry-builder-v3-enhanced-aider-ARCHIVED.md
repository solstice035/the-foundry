# Foundry Builder v3 — Enhanced Feature-Complete Builds

## Overview
Takes a `spec.json` from the Spec Writer and uses aider to build a **production-ready, feature-complete** project — not just an MVP.

## Key Differences from v2
- **More comprehensive prompts** — detailed implementation guidance for all features
- **Production quality focus** — proper error handling, edge cases, polish
- **Complete feature set** — implement ALL must-have features fully, not just skeletons
- **Better UX** — responsive design, loading states, error messages, accessibility
- **Testing included** — basic test coverage where appropriate

## Prerequisites
- `aider` installed and accessible via PATH
- API key available (OpenRouter recommended via `OPENROUTER_API_KEY`)
- `gh` CLI authenticated for GitHub operations
- `git` configured with user.name and user.email

## Workflow

### 1. Setup
```bash
mkdir -p ~/projects/foundry/<DATE>-<PROJECT_NAME>
cd ~/projects/foundry/<DATE>-<PROJECT_NAME>
git init
git branch -m main
git config user.name "The Foundry"
git config user.email "foundry@jeevesbot.io"
```

### 2. Prepare Enhanced Build Prompt

Extract from `spec.json` and **enhance with production requirements**:

```
You are building a production-ready implementation of <PROJECT_NAME>.

CRITICAL: This should be FEATURE-COMPLETE and PRODUCTION-READY, not an MVP.
Implement all features fully with proper error handling, edge cases, and polish.

## Project Overview
<description from spec>

## Tech Stack
<stack from spec>

## Core Features (IMPLEMENT ALL FULLY)

For each must-have feature from spec:
1. <Feature Name>
   - Full implementation details
   - Edge cases to handle
   - Error states
   - User feedback (loading, success, errors)
   - Accessibility considerations

## Quality Requirements

**Error Handling:**
- Validate all user inputs
- Graceful error messages (user-friendly, not technical)
- Handle network failures, timeouts, invalid data
- Loading states for async operations

**User Experience:**
- Responsive design (mobile + desktop)
- Keyboard navigation support
- Clear visual feedback for all actions
- Empty states, loading states, error states
- Smooth transitions/animations where appropriate

**Code Quality:**
- TypeScript strict mode (if applicable)
- Proper type definitions
- Clean, readable code with comments for complex logic
- Modular structure (separate concerns)
- No console.log statements in production code

**Testing:**
- Include basic tests for core functionality
- Test error cases, edge cases
- Integration tests if appropriate

**Documentation:**
- Comprehensive README with:
  - Clear project description
  - Feature list with screenshots/GIFs if visual
  - Installation instructions
  - Usage examples
  - Architecture overview (if complex)
  - Known limitations
  - Future improvements

## Nice-to-Have Features
<from spec — implement if time permits>

## Out of Scope
<from spec — explicitly DO NOT implement these>

## Success Criteria
<from spec>

## File Structure
Create a clean, logical file structure:
- Separate components/modules
- Shared utilities in dedicated folder
- Tests alongside code
- Clear naming conventions

## Deployment Readiness
- Include .env.example if needed
- Proper .gitignore
- Build/deploy scripts
- Production optimizations (minification, code splitting if applicable)

BUILD THIS TO A STANDARD YOU'D BE PROUD TO SHOW IN A PORTFOLIO.
Make it genuinely useful and well-crafted, not just functional.
```

### 3. Spawn Aider with Extended Timeout

Since we're building feature-complete apps, allow more time:

```bash
OPENROUTER_API_KEY=<key> aider \
  --yes \
  --model openrouter/anthropic/claude-sonnet-4-5 \
  --message "<enhanced build prompt>" \
  2>&1 | tee build.log
```

**Timeout:** 8 hours (28800 seconds) — enhanced builds take longer
**Background after:** 2 minutes

### 4-9. Same as v2

(Post-build cleanup, testing, GitHub push, output files, history update, failure handling)

## Expected Outcomes

**v2 (MVP) builds:**
- Duration: 7-20 minutes
- Features: Basic implementation, proof of concept
- Quality: "Works on my machine"
- Cost: $0.40-$0.80

**v3 (Enhanced) builds:**
- Duration: 30-90 minutes
- Features: Full implementation with polish
- Quality: Production-ready, portfolio-worthy
- Cost: $2.00-$5.00

The tradeoff: Higher cost and time, but significantly better output quality.

---

**Status:** v3 — Enhanced feature-complete builds for tonight's experimental run
**Created:** 2026-02-28
