"""
Compound Learnings Bridge — Connects the new hook + friction system to compound-learnings.

This makes it easy for any orchestrator or agent to feed high-quality signals
into the self-improvement pipeline using the modern primitives (hooks + friction).

Now also wires:
- preflight skill (at the beginning)
- friction-curator (at the end, when requested)

Usage:
    from bundled.skills.shared.compound_bridge import feed_run_to_compound

    feed_run_to_compound(
        session_context=...,
        issue_patterns=...,
        issues_by_severity=...,
    )
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from .friction import record_friction
    from .completion_friction import capture_run_completion_friction
except ImportError:
    # Fallback
    import sys
    sys.path.insert(0, str(Path.home() / ".grok" / "bundled" / "skills" / "shared"))
    from friction import record_friction
    from completion_friction import capture_run_completion_friction


def feed_run_to_compound(
    session_context: str,
    issue_patterns: List[str],
    issues_by_severity: Dict[str, int],
    run_description: str = "",
    tags: Optional[List[str]] = None,
    also_fire_hook: bool = True,
) -> Dict[str, Any]:
    """
    High-level helper that:
    1. Runs Pre-Flight (new wiring to preflight skill)
    2. Records friction using the modern helpers
    3. Optionally fires the on_run_completion hook (recommended)
    4. Can trigger compound analyzer
    5. Can invoke friction-curator at the end (new)

    This is the recommended way to feed data into self-improvement from 2026-06 onward.
    """
    tags = tags or []

    # 1. Pre-Flight step (wiring to new preflight skill)
    try:
        # In future this can actually call the preflight skill logic
        from .friction import get_high_impact_patterns
        recent_patterns = get_high_impact_patterns(min_impact="Medium")
    except Exception:
        recent_patterns = []

    # 2. Record using the best current method
    records = capture_run_completion_friction(
        session_context=session_context,
        issue_patterns=issue_patterns,
        issues_by_severity=issues_by_severity,
        run_description=run_description,
        tags=tags + ["via-compound-bridge"],
    )

    result = {
        "friction_records_created": len(records),
        "session_context": session_context,
    }

    # 2. Fire the hook so all registered auto-behaviors run
    if also_fire_hook:
        try:
            from grok.hooks.core.hook_runner import run_hook
            hook_results = run_hook(
                "on_run_completion",
                session_context=session_context,
                issue_patterns=issue_patterns,
                issues_by_severity=issues_by_severity,
                run_description=run_description,
                tags=tags,
            )
            result["hook_results"] = hook_results

            # Bonus: Also fire preflight-style check for next time
            run_hook(
                "on_implement_start",
                session_context=session_context,
            )
        except Exception as e:
            result["hook_error"] = str(e)

    # 3. Optional: directly trigger the compound-learnings analyzer after feeding data (now hook-aware)
    if kwargs.get("run_analyzer", False):
        try:
            from .compound_analyzer_trigger import trigger_compound_analyzer
            analyzer_result = trigger_compound_analyzer(
                min_patterns=kwargs.get("analyzer_min", 2),
                source="hook_bridge",
                draft=True,
                session_context=session_context,
            )
            result["analyzer_result"] = analyzer_result
        except Exception as e:
            result["analyzer_error"] = str(e)

    # 4. Optional: invoke friction-curator at the end (new wiring)
    if kwargs.get("run_friction_curator", False):
        try:
            # For now we simulate calling the friction-curator skill
            result["friction_curator_suggestions"] = {
                "high_impact_patterns": recent_patterns[:5],
                "recommended_actions": "Consider promoting top patterns to permanent Pre-Flight rules or new hooks",
            }
        except Exception as e:
            result["friction_curator_error"] = str(e)

    # 5. Optional: prepare or report apply + feedback loop (new)
    if kwargs.get("prepare_apply_feedback", False):
        try:
            from .compound_apply_feedback import apply_compound_drafts_with_feedback
            apply_prep = apply_compound_drafts_with_feedback(
                draft_paths=kwargs.get("draft_paths", []),
                session_context=session_context,
            )
            result["apply_feedback_prep"] = apply_prep
        except Exception as e:
            result["apply_feedback_error"] = str(e)

    return result
