"""Tests for content-queue.schema.json validation.

Validates that the content queue schema correctly accepts valid drafts
and rejects malformed entries.
"""

import json
from pathlib import Path

import jsonschema
import pytest

SCHEMA_PATH = (
    Path(__file__).parent.parent / "config" / "schemas" / "content-queue.schema.json"
)


@pytest.fixture
def schema():
    """Load the content queue schema."""
    with open(SCHEMA_PATH) as f:
        return json.load(f)


@pytest.fixture
def minimal_valid_queue():
    """Minimal valid content queue with empty pending array."""
    return {
        "schema_version": 1,
        "last_updated": "2026-03-05T08:00:00Z",
        "pending": [],
    }


@pytest.fixture
def valid_draft():
    """A valid draft entry with X platform."""
    return {
        "id": "draft-20260305-001",
        "created": "2026-03-05T08:00:00Z",
        "content_type": "build_announcement",
        "priority": 1,
        "status": "pending_review",
        "platforms": {
            "x": {
                "format": "single",
                "tweets": [
                    "Just shipped pdf-privacy-tools overnight. Strip metadata from PDFs in one command."
                ],
                "estimated_engagement": "high",
                "best_posting_time": "09:00-10:00 GMT (dev morning scroll)",
            }
        },
    }


@pytest.fixture
def valid_reddit_draft():
    """A valid Reddit platform draft."""
    return {
        "subreddit": "r/SideProject",
        "title": "I built a tool that strips metadata from PDFs",
        "body": "Built this overnight with AI agents. Here's how it works...",
        "estimated_engagement": "medium-high",
        "best_posting_time": "14:00-15:00 GMT",
    }


# --- Schema Loading ---


def test_schema_loads_as_valid_json():
    """Schema file exists and loads as valid JSON."""
    assert SCHEMA_PATH.exists(), f"Schema not found at {SCHEMA_PATH}"
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)
    assert isinstance(schema, dict)


def test_schema_has_required_top_level_properties(schema):
    """Schema defines required top-level properties."""
    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["title"] == "Content Queue Schema"
    assert "schema_version" in schema["properties"]
    assert "last_updated" in schema["properties"]
    assert "pending" in schema["properties"]
    assert schema["required"] == ["schema_version", "last_updated", "pending"]


# --- Valid Entry Tests ---


def test_minimal_valid_queue(schema, minimal_valid_queue):
    """Minimal valid content queue with empty pending array passes validation."""
    jsonschema.validate(instance=minimal_valid_queue, schema=schema)


def test_valid_draft_x_only(schema, minimal_valid_queue, valid_draft):
    """Valid draft with X platform only passes validation."""
    queue = {**minimal_valid_queue, "pending": [valid_draft]}
    jsonschema.validate(instance=queue, schema=schema)


def test_valid_draft_x_and_reddit(
    schema, minimal_valid_queue, valid_draft, valid_reddit_draft
):
    """Valid draft with X + Reddit platforms passes validation."""
    draft = {
        **valid_draft,
        "platforms": {
            **valid_draft["platforms"],
            "reddit": valid_reddit_draft,
        },
    }
    queue = {**minimal_valid_queue, "pending": [draft]}
    jsonschema.validate(instance=queue, schema=schema)


def test_valid_draft_all_fields(
    schema, minimal_valid_queue, valid_draft, valid_reddit_draft
):
    """Valid draft with all fields populated passes validation."""
    draft = {
        **valid_draft,
        "source_build": "2026-03-04",
        "estimated_engagement": "high",
        "notes": "Strong privacy angle, timely with AI data concerns.",
        "platforms": {
            "x": {
                "format": "thread",
                "tweets": [
                    "Just shipped pdf-privacy-tools overnight.",
                    "Strip metadata from PDFs in one command. No cloud, no uploads.",
                ],
                "estimated_engagement": "high",
                "best_posting_time": "09:00-10:00 GMT (dev morning scroll)",
                "visual": {
                    "type": "terminal_gif",
                    "path": "assets/pdf-demo.gif",
                    "alt_text": "Terminal showing pdf-privacy-tools stripping metadata",
                    "placement": 1,
                },
            },
            "reddit": valid_reddit_draft,
            "linkedin": {
                "body": "Built a privacy tool overnight with AI agents.",
                "estimated_engagement": "medium",
                "best_posting_time": "08:00-09:00 GMT",
            },
            "hackernews": {
                "title": "Show HN: pdf-privacy-tools",
                "url": "https://github.com/jeevesbot-io/pdf-privacy-tools",
                "estimated_engagement": "medium-high",
                "requires_approval": True,
            },
        },
    }
    queue = {
        **minimal_valid_queue,
        "pending": [draft],
        "approved": [],
        "rejected": [],
        "posted": [],
    }
    jsonschema.validate(instance=queue, schema=schema)


# --- Invalid Entry Tests (parametrized) ---


@pytest.mark.parametrize(
    "description, mutation",
    [
        (
            "missing_schema_version",
            lambda q: {k: v for k, v in q.items() if k != "schema_version"},
        ),
        (
            "missing_last_updated",
            lambda q: {k: v for k, v in q.items() if k != "last_updated"},
        ),
        (
            "missing_pending",
            lambda q: {k: v for k, v in q.items() if k != "pending"},
        ),
        (
            "invalid_schema_version",
            lambda q: {**q, "schema_version": 2},
        ),
        (
            "invalid_content_type",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-20260305-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "blog_post",
                        "priority": 1,
                        "status": "pending_review",
                        "platforms": {
                            "x": {
                                "format": "single",
                                "tweets": ["Test tweet"],
                                "estimated_engagement": "high",
                                "best_posting_time": "09:00 GMT",
                            }
                        },
                    }
                ],
            },
        ),
        (
            "invalid_priority_zero",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-20260305-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "build_announcement",
                        "priority": 0,
                        "status": "pending_review",
                        "platforms": {
                            "x": {
                                "format": "single",
                                "tweets": ["Test tweet"],
                                "estimated_engagement": "high",
                                "best_posting_time": "09:00 GMT",
                            }
                        },
                    }
                ],
            },
        ),
        (
            "invalid_priority_four",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-20260305-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "build_announcement",
                        "priority": 4,
                        "status": "pending_review",
                        "platforms": {
                            "x": {
                                "format": "single",
                                "tweets": ["Test tweet"],
                                "estimated_engagement": "high",
                                "best_posting_time": "09:00 GMT",
                            }
                        },
                    }
                ],
            },
        ),
        (
            "invalid_estimated_engagement",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-20260305-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "build_announcement",
                        "priority": 1,
                        "estimated_engagement": "very-high",
                        "status": "pending_review",
                        "platforms": {
                            "x": {
                                "format": "single",
                                "tweets": ["Test tweet"],
                                "estimated_engagement": "high",
                                "best_posting_time": "09:00 GMT",
                            }
                        },
                    }
                ],
            },
        ),
        (
            "invalid_draft_id_pattern",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-abc-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "build_announcement",
                        "priority": 1,
                        "status": "pending_review",
                        "platforms": {
                            "x": {
                                "format": "single",
                                "tweets": ["Test tweet"],
                                "estimated_engagement": "high",
                                "best_posting_time": "09:00 GMT",
                            }
                        },
                    }
                ],
            },
        ),
        (
            "invalid_status",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-20260305-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "build_announcement",
                        "priority": 1,
                        "status": "draft",
                        "platforms": {
                            "x": {
                                "format": "single",
                                "tweets": ["Test tweet"],
                                "estimated_engagement": "high",
                                "best_posting_time": "09:00 GMT",
                            }
                        },
                    }
                ],
            },
        ),
        (
            "tweet_exceeding_280_chars",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-20260305-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "build_announcement",
                        "priority": 1,
                        "status": "pending_review",
                        "platforms": {
                            "x": {
                                "format": "single",
                                "tweets": ["x" * 281],
                                "estimated_engagement": "high",
                                "best_posting_time": "09:00 GMT",
                            }
                        },
                    }
                ],
            },
        ),
        (
            "empty_platforms_object",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-20260305-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "build_announcement",
                        "priority": 1,
                        "status": "pending_review",
                        "platforms": {},
                    }
                ],
            },
        ),
        (
            "invalid_subreddit_pattern",
            lambda q: {
                **q,
                "pending": [
                    {
                        "id": "draft-20260305-001",
                        "created": "2026-03-05T08:00:00Z",
                        "content_type": "build_announcement",
                        "priority": 1,
                        "status": "pending_review",
                        "platforms": {
                            "reddit": {
                                "subreddit": "SideProject",
                                "title": "Test post",
                                "body": "Test body",
                                "estimated_engagement": "medium",
                                "best_posting_time": "14:00 GMT",
                            }
                        },
                    }
                ],
            },
        ),
    ],
    ids=[
        "missing_schema_version",
        "missing_last_updated",
        "missing_pending",
        "invalid_schema_version",
        "invalid_content_type",
        "invalid_priority_zero",
        "invalid_priority_four",
        "invalid_estimated_engagement",
        "invalid_draft_id_pattern",
        "invalid_status",
        "tweet_exceeding_280_chars",
        "empty_platforms_object",
        "invalid_subreddit_pattern",
    ],
)
def test_invalid_entries(schema, minimal_valid_queue, description, mutation):
    """Invalid entries are rejected by schema validation."""
    invalid_queue = mutation(minimal_valid_queue)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_queue, schema=schema)


# --- Tweet Length Validation ---


def test_tweet_exactly_280_chars(schema, minimal_valid_queue):
    """A 280-character tweet passes validation."""
    draft = {
        "id": "draft-20260305-001",
        "created": "2026-03-05T08:00:00Z",
        "content_type": "build_announcement",
        "priority": 1,
        "status": "pending_review",
        "platforms": {
            "x": {
                "format": "single",
                "tweets": ["x" * 280],
                "estimated_engagement": "high",
                "best_posting_time": "09:00 GMT",
            }
        },
    }
    queue = {**minimal_valid_queue, "pending": [draft]}
    jsonschema.validate(instance=queue, schema=schema)


def test_tweet_281_chars_fails(schema, minimal_valid_queue):
    """A 281-character tweet fails validation."""
    draft = {
        "id": "draft-20260305-001",
        "created": "2026-03-05T08:00:00Z",
        "content_type": "build_announcement",
        "priority": 1,
        "status": "pending_review",
        "platforms": {
            "x": {
                "format": "single",
                "tweets": ["x" * 281],
                "estimated_engagement": "high",
                "best_posting_time": "09:00 GMT",
            }
        },
    }
    queue = {**minimal_valid_queue, "pending": [draft]}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=queue, schema=schema)


def test_empty_tweets_array_fails(schema, minimal_valid_queue):
    """Empty tweets array fails validation (minItems: 1)."""
    draft = {
        "id": "draft-20260305-001",
        "created": "2026-03-05T08:00:00Z",
        "content_type": "build_announcement",
        "priority": 1,
        "status": "pending_review",
        "platforms": {
            "x": {
                "format": "single",
                "tweets": [],
                "estimated_engagement": "high",
                "best_posting_time": "09:00 GMT",
            }
        },
    }
    queue = {**minimal_valid_queue, "pending": [draft]}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=queue, schema=schema)


# --- Platform-Specific Tests ---


def test_x_draft_missing_tweets(schema, minimal_valid_queue):
    """X draft missing required 'tweets' field fails validation."""
    draft = {
        "id": "draft-20260305-001",
        "created": "2026-03-05T08:00:00Z",
        "content_type": "build_announcement",
        "priority": 1,
        "status": "pending_review",
        "platforms": {
            "x": {
                "format": "single",
                "estimated_engagement": "high",
                "best_posting_time": "09:00 GMT",
            }
        },
    }
    queue = {**minimal_valid_queue, "pending": [draft]}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=queue, schema=schema)


def test_reddit_draft_missing_subreddit(schema, minimal_valid_queue):
    """Reddit draft missing required 'subreddit' field fails validation."""
    draft = {
        "id": "draft-20260305-001",
        "created": "2026-03-05T08:00:00Z",
        "content_type": "build_announcement",
        "priority": 1,
        "status": "pending_review",
        "platforms": {
            "reddit": {
                "title": "Test post",
                "body": "Test body",
                "estimated_engagement": "medium",
                "best_posting_time": "14:00 GMT",
            }
        },
    }
    queue = {**minimal_valid_queue, "pending": [draft]}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=queue, schema=schema)


def test_reddit_draft_missing_title(schema, minimal_valid_queue):
    """Reddit draft missing required 'title' field fails validation."""
    draft = {
        "id": "draft-20260305-001",
        "created": "2026-03-05T08:00:00Z",
        "content_type": "build_announcement",
        "priority": 1,
        "status": "pending_review",
        "platforms": {
            "reddit": {
                "subreddit": "r/SideProject",
                "body": "Test body",
                "estimated_engagement": "medium",
                "best_posting_time": "14:00 GMT",
            }
        },
    }
    queue = {**minimal_valid_queue, "pending": [draft]}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=queue, schema=schema)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
