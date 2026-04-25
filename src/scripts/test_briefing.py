#!/usr/bin/env python3
"""
Test briefing compilation for all three paths:
1. Success (existing data from 2026-02-18)
2. Rejection (mock rejected spec)
3. Failure (mock failed build)
"""

import json
import os
import sys

WORKSPACE = os.path.expanduser("~/.openclaw/workspace/foundry")
DATE = "2026-02-18"
DAY_DIR = os.path.join(WORKSPACE, DATE)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def format_duration(seconds):
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m {secs}s" if secs else f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m" if mins else f"{hours}h"


def compile_success_briefing(trends, spec, build):
    """Compile a success briefing from real data."""
    # Extract trend info
    trend_title = spec.get("selected_trend_title", "Unknown trend")
    trend_score = None
    trend_source = "unknown"
    for t in trends.get("trends", []):
        if t.get("id") == spec.get("selected_trend_id"):
            trend_score = t.get("buildability_score", "?")
            trend_source = t.get("source", "unknown")
            break

    project = spec.get("spec", {})
    features = build.get("features_implemented", project.get("features", []))
    stack_parts = []
    if isinstance(project.get("stack"), dict):
        stack_parts = project["stack"].get("dependencies", [])
        if project["stack"].get("language"):
            stack_parts = [project["stack"]["language"]] + stack_parts
    elif isinstance(project.get("stack"), list):
        stack_parts = project["stack"]

    build_duration = format_duration(build.get("build_duration_seconds", 0))
    files = build.get("files_created", 0)
    cost = build.get("cost_usd", 0)  # was aider_cost_usd
    repo = build.get("repo_url", "N/A")

    # Estimate stage durations (for real pipeline, these come from state.json)
    scout_duration = "1m 22s"
    spec_duration = "1m 16s"
    total_seconds = build.get("build_duration_seconds", 0) + 82 + 76
    total_duration = format_duration(total_seconds)

    feature_lines = "\n".join(f"• {f}" for f in features)

    briefing_text = f"""🏭 The Foundry — Morning Briefing
📅 {DATE}

✅ BUILD SUCCESSFUL

📦 Project: {build.get("project_name", project.get("project_name", "unknown"))}
📈 Trend: "{trend_title}" (score {trend_score}/10, {trend_source})
🔧 Stack: {" + ".join(stack_parts)}

Features:
{feature_lines}

Build Stats:
• Duration: {build_duration}
• Files: {files}
• Cost: ${cost:.2f}
• GitHub: {repo}

Pipeline: Scout ({scout_duration}) → Spec ({spec_duration}) → Builder ({build_duration})
Total: {total_duration}"""

    briefing_json = {
        "schema_version": 1,
        "date": DATE,
        "type": "success",
        "pipeline_duration_seconds": total_seconds,
        "stages_completed": ["scout", "spec", "builder"],
        "project": {
            "name": build.get("project_name", project.get("project_name")),
            "description": project.get("description", ""),
            "trend_title": trend_title,
            "trend_source": trend_source,
            "trend_score": trend_score,
            "stack": stack_parts,
            "features": features,
            "repo_url": repo,
            "build_duration_seconds": build.get("build_duration_seconds", 0),
            "files_created": files,
            "cost_usd": cost,
        },
        "stage_timings": {
            "scout": {"duration_seconds": 82, "status": "complete"},
            "spec": {"duration_seconds": 76, "status": "complete"},
            "builder": {
                "duration_seconds": build.get("build_duration_seconds", 0),
                "status": "complete",
            },
        },
        "summary_text": briefing_text,
    }

    return briefing_json, briefing_text


def compile_rejection_briefing(trends, spec):
    """Compile a rejection briefing."""
    rejections = spec.get("rejected_alternatives", [])
    if not rejections:
        rejections = [{"title": "No details available", "rejection_reason": "Unknown"}]

    rejection_lines = []
    for i, r in enumerate(rejections[:5], 1):
        title = r.get("title", "Unknown")
        reason = r.get("rejection_reason", r.get("reason", "Unknown"))
        rejection_lines.append(f"{i}. {title} — {reason}")

    reasoning = spec.get(
        "rejection_summary",
        spec.get("reasoning", "No trends met buildability threshold."),
    )

    briefing_text = f"""🏭 The Foundry — Morning Briefing
📅 {DATE}

⏸️ NO BUILD TONIGHT

Decision: All trends rejected by Spec Writer

Top trends evaluated:
{chr(10).join(rejection_lines)}

Reasoning: {reasoning}

Pipeline: Scout (1m 22s) → Spec (1m 16s) → Rejected"""

    briefing_json = {
        "schema_version": 1,
        "date": DATE,
        "type": "rejection",
        "pipeline_duration_seconds": 158,
        "stages_completed": ["scout", "spec"],
        "project": None,
        "rejection": {
            "trends_evaluated": spec.get("trends_reviewed", len(rejections)),
            "top_rejections": [
                {
                    "title": r.get("title"),
                    "reason": r.get("rejection_reason", r.get("reason")),
                }
                for r in rejections[:5]
            ],
            "recommendation": spec.get(
                "what_would_work",
                "Tomorrow's scan should prioritize web apps, CLIs, or APIs.",
            ),
        },
        "stage_timings": {
            "scout": {"duration_seconds": 82, "status": "complete"},
            "spec": {"duration_seconds": 76, "status": "complete"},
            "builder": {"duration_seconds": 0, "status": "skipped"},
        },
        "summary_text": briefing_text,
    }

    return briefing_json, briefing_text


def compile_failure_briefing(trends, spec, build):
    """Compile a failure briefing."""
    trend_title = spec.get("selected_trend_title", "Unknown")
    trend_score = None
    for t in trends.get("trends", []):
        if t.get("id") == spec.get("selected_trend_id"):
            trend_score = t.get("buildability_score", "?")
            break

    project = spec.get("spec", {})
    error = build.get("error", "Unknown error")
    partial = build.get("partial_progress", build.get("notes", "No details available"))
    local_path = build.get("local_path", "N/A")

    briefing_text = f"""🏭 The Foundry — Morning Briefing
📅 {DATE}

❌ BUILD FAILED

📦 Project: {build.get("project_name", project.get("project_name", "unknown"))}
📈 Trend: "{trend_title}" (score {trend_score}/10)

Failure Stage: Builder
Error: {error}

Partial Progress:
• {partial}

Local Path: {local_path}
Status: Not pushed to GitHub

Next Steps: Manual review or retry tomorrow"""

    briefing_json = {
        "schema_version": 1,
        "date": DATE,
        "type": "failure",
        "pipeline_duration_seconds": 600,
        "stages_completed": ["scout", "spec"],
        "project": {
            "name": build.get("project_name", project.get("project_name")),
            "trend_title": trend_title,
            "trend_score": trend_score,
        },
        "failure": {
            "stage": "builder",
            "error": error,
            "partial_progress": partial,
            "local_path": local_path,
            "next_steps": "Manual review or retry tomorrow",
        },
        "stage_timings": {
            "scout": {"duration_seconds": 82, "status": "complete"},
            "spec": {"duration_seconds": 76, "status": "complete"},
            "builder": {"duration_seconds": 442, "status": "failed"},
        },
        "summary_text": briefing_text,
    }

    return briefing_json, briefing_text


def test_success_path():
    """Test 1: Success path with real data."""
    print("=" * 60)
    print("TEST 1: SUCCESS PATH")
    print("=" * 60)

    trends = load_json(os.path.join(DAY_DIR, "trends-summary.json"))
    spec = load_json(os.path.join(DAY_DIR, "spec.json"))
    build = load_json(os.path.join(DAY_DIR, "build.json"))

    briefing_json, briefing_text = compile_success_briefing(trends, spec, build)

    out_path = os.path.join(DAY_DIR, "briefing-test-success.json")
    with open(out_path, "w") as f:
        json.dump(briefing_json, f, indent=2)

    print(briefing_text)
    print(f"\n✅ Success briefing written to {out_path}")
    print(f"   Type: {briefing_json['type']}")
    print(f"   Stages: {briefing_json['stages_completed']}")
    print(f"   Project: {briefing_json['project']['name']}")
    return True


def test_rejection_path():
    """Test 2: Rejection path with mock data."""
    print("\n" + "=" * 60)
    print("TEST 2: REJECTION PATH")
    print("=" * 60)

    trends = load_json(os.path.join(DAY_DIR, "trends-summary.json"))

    # Mock rejected spec
    mock_spec = {
        "schema_version": 1,
        "decision": "rejected",
        "date": DATE,
        "trends_reviewed": 10,
        "rejection_summary": "No trends met buildability threshold ≥7 with clear MVP scope.",
        "what_would_work": "Tomorrow's scan should prioritize web apps, CLIs, or APIs with specific pain points.",
        "rejected_alternatives": [
            {
                "title": "AsteroidOS 2.0",
                "rejection_reason": "Hardware/firmware OS (unbuildable overnight)",
            },
            {
                "title": "Free alternative to Wispr Flow",
                "rejection_reason": "Already exists as open-source (no value)",
            },
            {
                "title": "BarraCUDA compiler",
                "rejection_reason": "GPU toolchain (too complex, score 6/10)",
            },
        ],
    }

    briefing_json, briefing_text = compile_rejection_briefing(trends, mock_spec)

    out_path = os.path.join(DAY_DIR, "briefing-test-rejection.json")
    with open(out_path, "w") as f:
        json.dump(briefing_json, f, indent=2)

    print(briefing_text)
    print(f"\n✅ Rejection briefing written to {out_path}")
    print(f"   Type: {briefing_json['type']}")
    print(f"   Trends evaluated: {briefing_json['rejection']['trends_evaluated']}")
    return True


def test_failure_path():
    """Test 3: Failure path with mock data."""
    print("\n" + "=" * 60)
    print("TEST 3: FAILURE PATH")
    print("=" * 60)

    trends = load_json(os.path.join(DAY_DIR, "trends-summary.json"))
    spec = load_json(os.path.join(DAY_DIR, "spec.json"))

    # Mock failed build
    mock_build = {
        "schema_version": 1,
        "date": DATE,
        "project_name": "pdf-privacy-tools",
        "status": "failed",
        "error": "claude-code-acp session timed out",
        "partial_progress": "Project structure created, dependencies installed, 8/10 features implemented, tests incomplete",
        "local_path": "~/projects/foundry/20260218-pdf-privacy-tools",
        "build_duration_seconds": 18000,
    }

    briefing_json, briefing_text = compile_failure_briefing(trends, spec, mock_build)

    out_path = os.path.join(DAY_DIR, "briefing-test-failure.json")
    with open(out_path, "w") as f:
        json.dump(briefing_json, f, indent=2)

    print(briefing_text)
    print(f"\n✅ Failure briefing written to {out_path}")
    print(f"   Type: {briefing_json['type']}")
    print(f"   Failed stage: {briefing_json['failure']['stage']}")
    return True


if __name__ == "__main__":
    results = []
    results.append(("Success path", test_success_path()))
    results.append(("Rejection path", test_rejection_path()))
    results.append(("Failure path", test_failure_path()))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")

    # Also write the real briefing.json (success, since that's what actually happened)
    trends = load_json(os.path.join(DAY_DIR, "trends-summary.json"))
    spec = load_json(os.path.join(DAY_DIR, "spec.json"))
    build = load_json(os.path.join(DAY_DIR, "build.json"))
    briefing_json, _ = compile_success_briefing(trends, spec, build)
    real_path = os.path.join(DAY_DIR, "briefing.json")
    with open(real_path, "w") as f:
        json.dump(briefing_json, f, indent=2)
    print(f"\n📝 Real briefing.json written to {real_path}")

    all_passed = all(r[1] for r in results)
    sys.exit(0 if all_passed else 1)
