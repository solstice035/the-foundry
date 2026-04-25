# Show HN: deptox

**Content Type:** build_announcement
**Priority:** 1
**Estimated Engagement:** high
**Best Posting Time:** Tuesday-Thursday 10am-12pm EST
**Prerequisite:** README complete, `npx deptox` working, tests passing, published to npm

---

## Hacker News

**Format:** Show HN

**Title:** Show HN: deptox – CLI scanner for phantom npm packages hallucinated by AI coding tools

**Body:**

AI coding assistants occasionally hallucinate npm package names that don't exist. Those phantom packages end up in your lockfile. The risk: anyone can register that name on npm and you've got a supply chain attack vector that no existing tool catches.

deptox scans your lockfile (package-lock.json, pnpm-lock.yaml, yarn.lock), checks every dependency against the npm registry, and flags packages that:

- Don't exist on the registry (phantom packages)
- Have suspiciously low download counts (<100/week)
- Were published very recently by new maintainers
- Have generated-looking names (consonant runs, no vowels)
- Are within Levenshtein distance 2 of a popular package (typosquats)

Each package gets a risk score (0-100) with reasons. Exit code 1 if anything scores above the threshold, so you can gate CI.

    npx deptox

3,664 LOC TypeScript (strict mode), 22 tests. Built overnight by an autonomous pipeline that scans Reddit/HN for developer pain points and builds an MVP while I sleep — this one scored highest across 18 builds and is now going v2.

v2 roadmap: PyPI support, OSV advisory database integration, GitHub Action, configurable scoring weights.

https://github.com/jeevesbot-io/deptox

---

## Notes

- HN Show HN format: title must start with "Show HN:". Keep the description factual and technical.
- The "built overnight by an autonomous pipeline" line is HN catnip — it's the kind of meta-engineering HN readers love. But it's one line, not the focus.
- Lead with the problem (AI hallucinated packages → supply chain risk), not the solution.
- The `npx deptox` one-liner is critical — HN readers will try it immediately.
- "No existing tool catches" is a strong claim — back it up in comments if challenged. npm audit only checks known CVEs. Snyk is general-purpose. Socket.dev is SaaS.
- v2 roadmap shows this isn't abandonware.
- Do NOT post until: README is complete, npx works, tests pass, npm published.
- Be ready to respond to comments for the first 3-4 hours. HN rewards fast, technical responses.
