# Content Drafter Test Data

This directory contains mock data for testing the content-drafter agent.

## Structure

```
content_drafter/
├── README.md (this file)
├── build_success_high_signal.json    # Strong build (signal ≥12)
├── build_success_medium_signal.json  # Mediocre build (signal 7-9)
├── spec_rejection.json               # Rejected spec with reasoning
├── build_failure.json                # Failed build with lessons
├── forecast.json                     # Trend forecast data
└── consensus.json                    # Consensus analysis data
```

## Usage

```bash
# Run all tests
python tests/test_content_drafter.py

# Run specific test
python tests/test_content_drafter.py --test build_announcement

# Validate schema only
python tests/test_content_drafter.py --validate-only
```

## Test Scenarios

### 1. Strong Build (High Signal ≥12)
- Should generate: X thread + Reddit post
- Priority: 1 (post today)
- Engagement: Medium-High or High

### 2. Mediocre Build (Signal 7-9)
- Should generate: X thread only (skip Reddit)
- Priority: 2 (this week)
- Engagement: Medium

### 3. Rejected Spec (Interesting Reasoning)
- Should generate: Rejection post (X single tweet)
- Must have counterintuitive angle
- Educational value

### 4. Failed Build (Good Lessons)
- Should generate: Failure post (X single tweet)
- Clear takeaway/lesson
- Vulnerability as strength

### 5. Trend Forecast
- Should generate: Single tweet or short thread
- Specific data (mentions, sources)
- Predictive angle

### 6. Consensus Analysis
- Should generate: X thread with perspective breakdown
- Genuine disagreement between perspectives
- Interesting conclusion

## Voice Testing

Each test validates:
- ✅ No corporate speak
- ✅ No engagement bait
- ✅ Concrete numbers over vague claims
- ✅ Platform-specific formatting
- ✅ Matches voice-guide.md tone

## Expected Approval Rate

Target: **>60% approval** from Nick (minimal edits needed)

## Mock Data

Mock data files will be added as we test with real builds. Initial testing uses inline mock data in test_content_drafter.py.
