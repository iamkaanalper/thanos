"""
Hook Handler: auto_self_improvement_feedback

Fired after drafts are applied (manually or automatically).

Job:
- Record the outcome of applying drafts as Working Solution or Friction
- Close the self-improvement loop with evidence
- Suggest follow-up actions (new rules, new hooks, new agents, etc.)
"""

from typing import Any, Dict

try:
    from bundled.skills.shared.friction import record_friction
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / ".grok" / "bundled" / "skills" / "shared"))
    from friction import record_friction


def handle(**kwargs) -> Dict[str, Any]:
    draft_paths = kwargs.get("draft_paths", [])
    applied_successfully = kwargs.get("applied_successfully", True)
    session_context = kwargs.get("session_context", "")
    notes = kwargs.get("notes", "")

    if applied_successfully:
        record_friction(
            pattern="Drafts from compound analysis were successfully applied",
            category="Self-Improvement Success",
            description=f"Applied {len(draft_paths)} drafts in context: {session_context}. Notes: {notes}",
            friction_impact="Low",
            session_context=session_context,
            recommended_fix_type="Continue monitoring for new patterns created by these changes",
            tags=["self-improvement", "draft-applied", "positive"],
        )
    else:
        record_friction(
            pattern="Draft application from compound analysis had issues",
            category="Self-Improvement Friction",
            description=f"Problems applying drafts in {session_context}. Notes: {notes}",
            friction_impact="Medium",
            session_context=session_context,
            recommended_fix_type="Improve draft quality or add safer apply mechanisms",
            tags=["self-improvement", "draft-applied", "friction"],
        )

    return {
        "status": "success",
        "feedback_recorded": True,
        "hook": "auto_self_improvement_feedback",
    }
