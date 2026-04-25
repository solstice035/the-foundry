# Mock Consensus Analyses

This directory contains example consensus analysis outputs for testing.

To populate:
1. Run Consensus Analyst on 3+ builds (good, mediocre, bad)
2. Save outputs here as `{project}-consensus.json`
3. Run `pytest tests/test_consensus.py` to verify

Minimum required:
- 1 strong build (high stars, genuine utility)
- 1 mediocre build (low engagement, saturated space)
- 1 weak build (poor execution or rejected category)

Tests verify:
- Critic votes 'hold' or 'pass' >80% of time
- Perspectives genuinely disagree
- No rubber-stamping
