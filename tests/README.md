# Epic 2.3: Trend Lifecycle Tracking - Tests

## Overview

This test suite validates the lifecycle tracking logic implemented in Epic 2.3. It simulates multi-night trend data to verify that rising, peaked, stable, and new trends are correctly detected and scored.

## Test Data

**Mock trend files:** `tests/mock_trends/`
- `2026-02-23.json` - Night 1 (4 trends)
- `2026-02-24.json` - Night 2 (5 trends, some repeating)
- `2026-02-25.json` - Night 3 (5 trends, different engagement)
- `2026-02-26.json` - Night 4 (5 trends, final state)

### Example Trend Trajectories

1. **PDF Privacy Tools** (Rising)
   - 2026-02-23: 45 points (reddit)
   - 2026-02-24: 67 points (reddit + hn)
   - 2026-02-25: 102 points (reddit + hn + x)
   - 2026-02-26: 95 points (reddit + hn)
   - **Status:** Rising (upward trajectory, momentum 2.0)

2. **Docker CLI** (Peaked)
   - 2026-02-23: 120 points
   - 2026-02-24: 95 points
   - 2026-02-25: 78 points
   - 2026-02-26: 62 points
   - **Status:** Peaked (downward trajectory, momentum 0.52)

3. **RSS Reader** (Stable)
   - 2026-02-23: 67 points
   - 2026-02-24: 72 points
   - 2026-02-25: 65 points
   - **Status:** Stable (flat trajectory, momentum 1.0)

4. **GitHub Actions Alternative** (Explosive Growth)
   - 2026-02-24: 140 points
   - 2026-02-25: 185 points
   - 2026-02-26: 245 points
   - **Status:** Rising (explosive growth, momentum 1.75)

## Running Tests

```bash
cd ~/projects/the-foundry
python3 tests/test_lifecycle.py
```

All 8 tests should pass:
- ✅ New trend detection
- ✅ Rising trend detection
- ✅ Peaked trend detection
- ✅ Stable trend detection
- ✅ Explosive growth momentum
- ✅ Fuzzy title matching
- ✅ Momentum score bounds
- ✅ Rising vs Peaked scoring comparison

## Test Coverage

### Core Logic Tested

1. **Trend Matching**
   - URL-based exact matching
   - Fuzzy title matching (Jaccard similarity ≥60%)
   - Keyword extraction and normalization

2. **Lifecycle Detection**
   - New trends (first appearance)
   - Rising trends (increasing engagement)
   - Peaked trends (declining engagement)
   - Stable trends (flat engagement)

3. **Momentum Calculation**
   - Rising trends: 1.0 to 2.0 multiplier
   - Peaked trends: 0.2 to 1.0 multiplier
   - Bounds enforcement (min 0.2, max 2.0)

4. **Scoring Impact**
   - Rising trends score higher than peaked trends
   - Momentum multiplier applied to base buildability score
   - Final score = base_score × momentum_score

## Implementation Classes

### `TrendMatcher`
- `normalize_title(title)` - Extract keywords from title
- `jaccard_similarity(set1, set2)` - Calculate similarity between keyword sets
- `match_trend(trend, history)` - Find historical matches for a trend

### `LifecycleCalculator`
- `calculate_trajectory(scores)` - Determine upward/downward/flat trajectory
- `calculate_status(appearances, trajectory)` - Determine new/rising/peaked/stable
- `calculate_momentum(status, scores)` - Calculate momentum multiplier (0.2-2.0)

### `enrich_trend_with_lifecycle(trend, history)`
Main function that orchestrates the enrichment process:
1. Match trend against history
2. Build engagement timeline
3. Calculate lifecycle metrics
4. Return enriched trend with `lifecycle` object

## Expected Output Format

```json
{
  "id": "trend-20260226-042",
  "title": "...",
  "engagement_score": 102,
  "lifecycle": {
    "status": "rising",
    "trajectory": "upward",
    "first_seen": "2026-02-23",
    "appearances": 3,
    "engagement_history": [
      {"date": "2026-02-23", "score": 45},
      {"date": "2026-02-24", "score": 67},
      {"date": "2026-02-26", "score": 102}
    ],
    "days_active": 4,
    "momentum_score": 2.0
  }
}
```

## Integration with Foundry Pipeline

This test logic mirrors what the **Trend Researcher (Mode A)** agent will implement:

1. Trend Scout outputs `trends-raw.json`
2. Trend Researcher reads raw trends + trend history
3. Enriches each trend with lifecycle data
4. Outputs `trends-summary.json` (schema v2)
5. Spec Writer uses lifecycle status to prioritize trends

**Key benefit:** Rising trends get boosted, peaked trends get penalized, helping Spec Writer select fresher opportunities.

## Notes

- Mock data simulates realistic engagement patterns
- Tests verify both happy path and edge cases
- All scoring logic is deterministic (same input → same output)
- Fuzzy matching handles typos and slight title variations
