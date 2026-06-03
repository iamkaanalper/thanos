"""
Completion Friction Capture — Grok-native helper for the end of big runs.

When a long-running orchestrator (implement, execute-plan, swarm-lite, etc.) finishes,
this makes it trivial to turn the patterns discovered during the run into high-quality
friction records that will improve future runs.

This closes the self-improvement loop ergonomically.

Usage example (at the very end of a run, before final report):

```python
from bundled.skills.shared.completion_friction import capture_run_completion_friction

capture_run_completion_friction(
    session_context="implement run for feature X",
    issue_patterns=issue_patterns,                    # from orchestrator state
    issues_by_severity=total_issues_by_severity,      # from orchestrator state
    run_description=description,
    tags=["implement", "feature-x"],
)
```
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .friction import record_friction

__all__ = ["capture_run_completion_friction"]


def capture_run_completion_friction(
    session_context: str,
    issue_patterns: List[str],
    issues_by_severity: Dict[str, int],
    run_description: str = "",
    tags: Optional[List[str]] = None,
    min_issues_for_record: int = 3,
) -> List[Dict[str, Any]]:
    """
    At the end of a significant run, automatically turn discovered patterns into friction records.

    This should be called in the final stage of implement, execute-plan, or custom swarm-lite flows,
    right before or during the memory flush / compound capture step.

    Returns the list of friction records that were created.
    """
    created: List[Dict[str, Any]] = []
    total_issues = sum(issues_by_severity.values())

    if total_issues < min_issues_for_record and not issue_patterns:
        return created

    base_tags = tags or []
    base_tags = list(set(base_tags + ["run-completion", "self-improvement"]))

    # Record the overall pattern count as one high-level friction item
    if total_issues >= min_issues_for_record:
        rec = record_friction(
            pattern=f"Run produced {total_issues} issues across {len(issue_patterns)} distinct patterns",
            category="Run Quality & Iteration Cost",
            description=f"Run '{run_description or session_context}' required significant review-fix iterations. "
                        f"Issues by severity: {issues_by_severity}",
            friction_impact="Medium" if total_issues < 10 else "High",
            session_context=session_context,
            recommended_fix_type="Improve Pre-Flight, add more specific handoff templates, or strengthen verifier checks for this category of work",
            confidence="high",
            tags=base_tags + ["iteration-cost"],
        )
        created.append(rec)

    # Record each distinct pattern as its own friction item (these become future checklist material)
    for pattern in issue_patterns:
        rec = record_friction(
            pattern=pattern,
            category="Recurring Code/Process Issue",
            description=f"Pattern appeared during run: {session_context}",
            friction_impact="Medium",
            session_context=session_context,
            recommended_fix_type="Consider adding this pattern to future Pre-Flight checklists or verifier rules",
            confidence="medium",
            tags=base_tags + ["pattern-from-run"],
        )
        created.append(rec)

    return created
