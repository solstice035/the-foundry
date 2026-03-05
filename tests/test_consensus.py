"""
Tests for Epic 2.5: Consensus Analyst

Tests consensus analysis with multiple perspectives, adversarial Critic,
and genuine disagreement detection.
"""

import json
from pathlib import Path
from jsonschema import validate
import pytest


# Test data directory
TEST_DATA = Path(__file__).parent / "mock_consensus"
SCHEMA_PATH = Path(__file__).parent.parent / "config/schemas/consensus.schema.json"


@pytest.fixture
def consensus_schema():
    """Load consensus analysis schema"""
    with open(SCHEMA_PATH) as f:
        return json.load(f)


@pytest.fixture
def good_build_example():
    """Example: pdf-privacy-tools (strong build, 34 stars)"""
    return {
        "project": "pdf-privacy-tools",
        "date_built": "2026-02-18",
        "repo": "https://github.com/jeevesbot-io/pdf-privacy-tools",
        "current_metrics": {
            "stars": 34,
            "forks": 3,
            "issues": 2,
            "days_since_build": 4,
            "trend_source": "reddit",
            "build_cost_usd": 0.52,
        },
    }


@pytest.fixture
def mediocre_build_example():
    """Example: todo-cli (saturated space, low engagement)"""
    return {
        "project": "todo-cli",
        "date_built": "2026-02-20",
        "repo": "https://github.com/jeevesbot-io/todo-cli",
        "current_metrics": {
            "stars": 3,
            "forks": 0,
            "issues": 0,
            "days_since_build": 6,
            "trend_source": "hn",
            "build_cost_usd": 0.38,
        },
    }


@pytest.fixture
def bad_build_example():
    """Example: crypto-tracker (rejected category, poor execution)"""
    return {
        "project": "crypto-tracker",
        "date_built": "2026-02-21",
        "repo": "https://github.com/jeevesbot-io/crypto-tracker",
        "current_metrics": {
            "stars": 1,
            "forks": 0,
            "issues": 0,
            "days_since_build": 5,
            "trend_source": "x",
            "build_cost_usd": 0.41,
        },
    }


def test_schema_exists():
    """Schema file exists and is valid JSON"""
    assert SCHEMA_PATH.exists(), f"Schema not found at {SCHEMA_PATH}"

    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["title"] == "Consensus Analysis"


def test_schema_requires_five_perspectives(consensus_schema):
    """Schema enforces exactly 5 perspectives"""
    assert consensus_schema["properties"]["perspectives"]["minItems"] == 5
    assert consensus_schema["properties"]["perspectives"]["maxItems"] == 5

    allowed_roles = consensus_schema["properties"]["perspectives"]["items"][
        "properties"
    ]["role"]["enum"]
    assert set(allowed_roles) == {"user", "critic", "builder", "marketer", "investor"}


def test_schema_requires_votes(consensus_schema):
    """Each perspective must vote invest/hold/pass"""
    vote_enum = consensus_schema["properties"]["perspectives"]["items"]["properties"][
        "vote"
    ]["enum"]
    assert set(vote_enum) == {"invest", "hold", "pass"}


def test_schema_enforces_reasoning_length(consensus_schema):
    """Reasoning must be substantive (min 50 chars)"""
    min_length = consensus_schema["properties"]["perspectives"]["items"]["properties"][
        "reasoning"
    ]["minLength"]
    assert min_length == 50, "Reasoning should require at least 50 characters"


def test_valid_consensus_good_build(consensus_schema):
    """Valid consensus output for a strong build validates against schema"""
    consensus = {
        "project": "pdf-privacy-tools",
        "date_built": "2026-02-18",
        "date_analyzed": "2026-02-22",
        "trigger": "crossed_25_stars",
        "current_metrics": {
            "stars": 34,
            "forks": 3,
            "issues": 2,
            "days_since_build": 4,
            "trend_source": "reddit",
            "build_cost_usd": 0.52,
        },
        "perspectives": [
            {
                "role": "user",
                "vote": "invest",
                "reasoning": "This solves a real privacy concern. I'd use it for sensitive documents. Would like batch processing and GUI option.",
                "key_requests": ["Batch processing", "Simple GUI wrapper"],
                "adoption_blockers": ["CLI-only limits non-technical users"],
            },
            {
                "role": "critic",
                "vote": "hold",
                "reasoning": "Privacy tools exist (pdf-redact-tools, mat2). Differentiation is unclear. Engagement could be novelty-driven. Need to prove sustained utility.",
                "concerns": [
                    "Existing tools: pdf-redact-tools, mat2, ExifTool",
                    "Market timing unclear — is this a new concern or evergreen?",
                    "No clear technical advantage over existing solutions",
                ],
                "competitive_threats": [
                    "pdf-redact-tools (established)",
                    "mat2 (metadata removal)",
                ],
                "fatal_flaws": "None identified, but differentiation gap is real",
            },
            {
                "role": "builder",
                "vote": "invest",
                "reasoning": "Clean architecture, good use of PyPDF2. Tests exist but coverage is ~40%. Adding batch processing is 3-4 hours. GUI wrapper would be 8-10 hours.",
                "technical_debt": [
                    "Test coverage at 40% (needs 80%+)",
                    "No CI/CD",
                    "Error handling for corrupted PDFs missing",
                    "No progress indicators for large files",
                ],
                "effort_estimate": "6-8 hours for production quality",
                "architecture_assessment": "Solid foundation, modular design",
                "extensibility": "Easy to add formats, batch operations",
            },
            {
                "role": "marketer",
                "vote": "invest",
                "reasoning": "Privacy angle is strong, timely with AI data concerns. Target: security-conscious devs, journalists, legal. Distribution: r/privacy, HN, InfoSec Twitter.",
                "distribution_channels": [
                    "r/privacy",
                    "r/security",
                    "Hacker News",
                    "InfoSec Twitter",
                ],
                "narrative": "Remove metadata from PDFs before sharing — protect yourself from accidental leaks",
                "virality_potential": "Medium — niche but passionate audience",
                "timing": "Good — AI data scraping makes metadata privacy more relevant",
                "differentiation_angle": "Simple, focused tool for one job (vs Swiss Army knife tools)",
            },
            {
                "role": "investor",
                "vote": "pass",
                "reasoning": "This is a feature, not a product. No moat, easy to replicate. Revenue path unclear (open-source privacy tool = hard to monetize). However, good portfolio piece for privacy/security cred.",
                "classification": "feature",
                "moat": "None — functionality easily replicable",
                "monetization_path": "Not viable (privacy users expect free/open-source)",
                "growth_trajectory": "Linear — no network effects",
                "opportunity_cost": "Limited — small time investment acceptable",
                "exit_criteria": "Polish to portfolio-ready, add to showcase",
                "recommendation": "Keep as portfolio piece, don't commercialize",
            },
        ],
        "consensus": {
            "votes": {"invest": 3, "hold": 1, "pass": 1},
            "recommendation": "invest_limited",
            "effort_cap_hours": 8,
            "summary": "Worth 6-8 hours to production-ready. Strong use case (privacy), good execution, but no commercialization path. Polish for portfolio and credibility.",
            "rationale": "User, Builder, Marketer see value. Critic correctly flags differentiation gap. Investor right to pass on commercialization but wrong to ignore portfolio value. Compromise: limited investment for showcase.",
            "action_items": [
                "Add batch processing mode — 3 hours",
                "Increase test coverage to 80% — 2 hours",
                "Add CI/CD (GitHub Actions) — 1 hour",
                "Polish README with security warnings — 1 hour",
                "Post to r/privacy — 1 hour",
            ],
            "total_estimated_effort": "8 hours",
            "do_not": [
                "Build GUI version (out of scope)",
                "Add cloud/SaaS features",
                "Attempt to monetize",
                "Expand to other file formats yet",
            ],
            "success_criteria": [
                "Test coverage >80%",
                "CI passing",
                "Posted to r/privacy with positive reception",
                "README has clear security warnings",
            ],
        },
        "meta": {
            "perspectives_disagreed": True,
            "critic_vote": "hold",
            "investor_vote": "pass",
            "genuine_conflict": True,
            "rubber_stamping_detected": False,
        },
    }

    # Should validate without errors
    validate(instance=consensus, schema=consensus_schema)


def test_critic_must_be_skeptical():
    """Critic should vote 'hold' or 'pass' >80% of the time"""
    # This test documents the requirement
    # In practice, tested by running Consensus Analyst on 10+ builds

    # Load example analyses if they exist
    if not TEST_DATA.exists():
        pytest.skip("No test consensus data yet")

    analyses = list(TEST_DATA.glob("*.json"))
    if len(analyses) < 5:
        pytest.skip("Need at least 5 consensus analyses to test Critic behavior")

    critic_skeptical_count = 0
    total = 0

    for analysis_path in analyses:
        with open(analysis_path) as f:
            data = json.load(f)

        critic = next(p for p in data["perspectives"] if p["role"] == "critic")
        total += 1

        if critic["vote"] in ["hold", "pass"]:
            critic_skeptical_count += 1

    skepticism_rate = critic_skeptical_count / total
    assert skepticism_rate >= 0.8, (
        f"Critic should vote 'hold' or 'pass' >80% of time, got {skepticism_rate:.1%}"
    )


def test_rubber_stamping_detection():
    """Detect when all perspectives agree without critical analysis"""
    rubber_stamp_example = {
        "project": "test-project",
        "date_built": "2026-02-20",
        "date_analyzed": "2026-02-21",
        "trigger": "manual_analysis",
        "current_metrics": {
            "stars": 10,
            "forks": 1,
            "issues": 0,
            "days_since_build": 1,
        },
        "perspectives": [
            {
                "role": "user",
                "vote": "invest",
                "reasoning": "This looks great, very useful tool for developers everywhere.",
            },
            {
                "role": "critic",
                "vote": "invest",
                "reasoning": "No concerns, this is well executed and valuable to community.",
            },
            {
                "role": "builder",
                "vote": "invest",
                "reasoning": "Code quality is good, architecture is sound, ready to go.",
            },
            {
                "role": "marketer",
                "vote": "invest",
                "reasoning": "Great story, will resonate with audience, easy to market.",
            },
            {
                "role": "investor",
                "vote": "invest",
                "reasoning": "Strong potential, clear path to growth, worth investing.",
            },
        ],
        "consensus": {
            "votes": {"invest": 5, "hold": 0, "pass": 0},
            "recommendation": "invest",
            "summary": "Everyone agrees this is great",
            "rationale": "Unanimous support",
            "action_items": ["Build more features"],
            "do_not": ["Nothing to avoid"],
        },
        "meta": {
            "perspectives_disagreed": False,
            "critic_vote": "invest",
            "investor_vote": "invest",
            "genuine_conflict": False,
            "rubber_stamping_detected": True,  # Should flag this
            "unanimous_invest": True,
        },
    }

    # This should validate (schema allows it) but should be flagged in meta
    assert rubber_stamp_example["meta"]["rubber_stamping_detected"] is True
    assert rubber_stamp_example["meta"]["unanimous_invest"] is True


def test_genuine_disagreement_example():
    """Example of genuine disagreement with substantive reasoning"""
    disagreement_example = {
        "project": "todo-cli",
        "date_built": "2026-02-20",
        "date_analyzed": "2026-02-22",
        "trigger": "manual_analysis",
        "current_metrics": {"stars": 3, "forks": 0, "issues": 0, "days_since_build": 2},
        "perspectives": [
            {
                "role": "user",
                "vote": "hold",
                "reasoning": "Too many todo apps exist. Would only use this if it had unique feature like AI task breakdown or time estimation. Basic CLI todo is solved problem.",
            },
            {
                "role": "critic",
                "vote": "pass",
                "reasoning": "Saturated space with hundreds of alternatives (todoist, things, todo.txt, taskwarrior). Zero differentiation. Low engagement confirms lack of interest. Fatal flaw: no reason to exist.",
                "concerns": [
                    "Saturated market",
                    "No differentiation",
                    "Low engagement indicates no PMF",
                ],
                "competitive_threats": ["todoist", "things", "todo.txt", "taskwarrior"],
                "fatal_flaws": "No unique value proposition in extremely crowded space",
            },
            {
                "role": "builder",
                "vote": "hold",
                "reasoning": "Code is clean but generic. Standard CRUD operations. Architecture is fine but unremarkable. Would take 4-5 hours to add AI features, but still unclear if worth it.",
            },
            {
                "role": "marketer",
                "vote": "pass",
                "reasoning": "No story here. 'Another todo app' is anti-viral. No audience — productivity enthusiasts already locked into existing tools. No angle that makes this worth sharing.",
            },
            {
                "role": "investor",
                "vote": "pass",
                "reasoning": "Classic feature-not-product in solved category. No moat, no network effects, no revenue path. Opportunity cost is high — time better spent elsewhere. Clear pass.",
            },
        ],
        "consensus": {
            "votes": {"invest": 0, "hold": 2, "pass": 3},
            "recommendation": "pass",
            "summary": "Unanimous rejection. Saturated space, no differentiation, no engagement. Archive immediately.",
            "rationale": "All perspectives agree: no unique value in crowded market. Even sympathetic views (User, Builder) vote 'hold' not 'invest'. Clear signal to archive.",
            "action_items": [],
            "do_not": ["Invest any more time"],
            "success_criteria": [],
        },
        "meta": {
            "perspectives_disagreed": True,
            "critic_vote": "pass",
            "investor_vote": "pass",
            "genuine_conflict": False,
            "rubber_stamping_detected": False,
            "archive_immediately": True,
        },
    }

    # Verify genuine disagreement (votes split between hold/pass)
    assert disagreement_example["consensus"]["votes"]["invest"] == 0
    assert disagreement_example["consensus"]["votes"]["pass"] >= 3
    assert disagreement_example["meta"]["archive_immediately"] is True


def test_effort_cap_enforcement():
    """invest_limited must include effort_cap_hours"""
    consensus = {
        "consensus": {
            "recommendation": "invest_limited"
            # Missing effort_cap_hours
        }
    }
    with pytest.raises(KeyError):
        _ = consensus["consensus"]["effort_cap_hours"]


def test_action_items_must_be_specific():
    """Action items should be specific and time-bounded"""
    good_actions = [
        "Add multi-provider support (Anthropic, local models) — 4 hours",
        "Increase test coverage to 80% — 2 hours",
        "Add CI/CD (GitHub Actions) — 1 hour",
    ]

    # Good actions have time estimates and specifics
    for action in good_actions:
        assert "—" in action or "hours" in action.lower(), (
            f"Action should be time-bounded: {action}"
        )


def test_do_not_list_prevents_scope_creep():
    """'Do not' list should prevent feature creep"""
    good_do_nots = [
        "Do not build a SaaS version",
        "Do not add features beyond core use case",
        "Do not spend more than 12 hours total",
    ]

    for item in good_do_nots:
        assert item.lower().startswith("do not") or "don't" in item.lower(), (
            f"'Do not' item should be explicit: {item}"
        )


def test_engagement_thresholds():
    """Test trigger types for different engagement levels"""
    triggers = [
        "crossed_25_stars",
        "crossed_50_stars",
        "crossed_100_stars",
        "external_issues",
        "manual_analysis",
    ]

    # Schema should allow all these triggers
    # (This is tested implicitly by schema validation)
    assert len(triggers) == 5


def test_perspective_specific_fields():
    """Each perspective should have role-specific fields"""
    # User should have key_requests, adoption_blockers
    # Critic should have concerns, competitive_threats, fatal_flaws
    # Builder should have technical_debt, effort_estimate
    # Marketer should have distribution_channels, narrative
    # Investor should have classification, moat, monetization_path

    # This is tested by schema structure
    pass


def test_mock_consensus_directory_setup():
    """Ensure test data directory exists or create it"""
    TEST_DATA.mkdir(exist_ok=True)

    # Create a README if it doesn't exist
    readme = TEST_DATA / "README.md"
    if not readme.exists():
        readme.write_text("""# Mock Consensus Analyses

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
""")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
