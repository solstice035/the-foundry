# deptox Technical Deep-Dive — Reddit

**Content Type:** build_announcement
**Priority:** 1
**Estimated Engagement:** medium-high
**Best Posting Time:** Tuesday 2-4pm GMT (US morning)
**Prerequisite:** Post after Show HN (or same day)

---

## Reddit

**Subreddit:** r/programming or r/node (choose based on which has more supply chain discussion that week)

**Title:** How AI coding assistants create a new supply chain attack vector — and the scanner I built to catch it

**Body:**

## The problem

AI coding assistants hallucinate package names. When Copilot or Claude suggests `import { foo } from 'nonexistent-package'`, that package name ends up in your code, your lockfile, and your CI pipeline. Most of the time it fails at install and you fix it.

But here's the attack vector nobody's really talking about: if the hallucinated package name is plausible enough, someone can register it on npm. Your next `npm install` pulls down malware. It's dependency confusion meets AI hallucination.

npm audit won't catch it — it only checks known CVEs in the advisory database. Snyk won't catch it — it's general-purpose vulnerability scanning. The phantom package isn't vulnerable. It's not even real. It's a name your AI made up that someone weaponised.

## What deptox does

deptox scans your lockfile and checks every dependency against 6 risk signals:

1. **Existence** — Does this package actually exist on npm? (+100 risk if not)
2. **Downloads** — Does it have real usage? (<10/week = +40 risk)
3. **Freshness** — Was it published in the last 30 days by a new maintainer? (+30 risk)
4. **Maintainer history** — Single maintainer with no other packages? (+10-15 risk)
5. **Name patterns** — Does the name look generated? Consonant runs, no vowels? (+15 risk)
6. **Typosquat distance** — Is it within Levenshtein distance 2 of a popular package? (+20 risk)

Scores compound. A non-existent package that also looks like a typosquat of `express` scores 120+. A real package with 50k weekly downloads scores 0.

Risk levels: Critical (80+), High (60+), Medium (30+), Low (<30).

## Try it

```
npx deptox
```

Scans whichever lockfile it finds in the current directory. Colour-coded terminal output. JSON mode (`--json`) for CI. Exit code 1 if anything scores above threshold (default 30, configurable with `--threshold`).

## The backstory

This was built overnight by an autonomous pipeline I run — it scans Reddit and HN for developer pain points at midnight, picks one, writes a spec, and builds an MVP while I sleep. deptox scored highest across 18 overnight builds on criteria including market timing, technical foundation, and expansion potential. It's now going v2.

## v2 roadmap

- **PyPI support** — `requirements.txt`, `Pipfile.lock`, `poetry.lock` (litellm compromise proves Python is equally vulnerable)
- **Advisory database integration** — OSV + GitHub Advisory Database for known compromised packages
- **GitHub Action** — SARIF output for GitHub Security tab integration
- **Configurable scoring** — `.deptoxrc.json` with custom weights and allowlists
- **Cargo + Go modules** — full multi-ecosystem support

## Known limitations

- npm downloads API returns 0 for scoped packages → false positives on `@scope/pkg`
- Typosquat detection gets noisy on short package names (3-4 chars)
- Yarn v1 format only (v2/v3 in v2)

3,664 LOC TypeScript, 22 tests, MIT licensed.

https://github.com/jeevesbot-io/deptox

---

## Notes

- This is the technical deep-dive — more detail than the X thread or Show HN.
- The "attack vector nobody's talking about" framing is the hook for r/programming.
- The scoring breakdown is the centrepiece — it shows engineering rigour, not just "I built a thing".
- The v2 roadmap signals this is an active project, not abandonware.
- Known limitations are listed upfront to pre-empt "but what about..." comments.
- Respond to every comment in the first 2 hours.
- If posting to r/node, adjust title: "deptox — CLI scanner that finds phantom npm packages hallucinated by AI coding assistants"
