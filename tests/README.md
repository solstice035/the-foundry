# Tests

Test suite for The Foundry.

## Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_utils.py

# Run specific test
pytest tests/test_utils.py::TestKeywordExtraction::test_extract_keywords_basic
```

## Test Organization

- `test_utils.py` — Tests for src/utils.py (keyword extraction, dedup, normalization)
- `test_schemas.py` — Schema validation tests (TODO)
- `test_trend_scout.py` — Trend Scout agent tests (TODO in Epic 1.1)
- `test_spec_writer.py` — Spec Writer agent tests (TODO in Epic 1.3)
- `test_builder.py` — Builder agent tests (TODO in Epic 1.4)

## Test Strategy

**6-step validation (from CLAUDE.md):**

1. **Unit test:** Individual functions
2. **Mock test:** Agents with mocked API responses
3. **Live test:** Agents with real APIs (rate limit aware)
4. **Integration test:** Full pipeline (Scout → Spec → Builder)
5. **Failure test:** Timeouts, bad data, source failures
6. **Consistency test:** Run 3-5 times, verify output similarity

## Fixtures

Mock data lives in `tests/fixtures/`:
- `trends-raw-sample.json` — Sample Trend Scout output
- `spec-approved-sample.json` — Sample approved spec
- `build-success-sample.json` — Sample successful build

## Coverage Goals

- **src/utils.py:** 90%+ (core utilities)
- **Agent task prompts:** Manual testing + consistency checks
- **Integration:** Happy path + 3 failure modes per epic
