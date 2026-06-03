"""
Hook: on_bounded_loop_end

Fired when a review-fix loop (in implement, execute-plan, etc.) ends a round
or reaches escalation.

Useful for:
- Syncing ledger state
- Notifying if loops are taking too many rounds
- Auto-recording "expensive iteration" friction

MVP: If attempt >= 2, record a friction signal.
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
    """
    Expected kwargs:
        task_id: str
        attempt: int
        max_attempts: int
        status: str
        session_context: str
    """
    attempt = kwargs.get("attempt", 0)
    max_attempts = kwargs.get("max_attempts", 3)
    status = kwargs.get("status", "")
    session_context = kwargs.get("session_context", "bounded-loop")

    if attempt < 2:
        return {"status": "skipped", "reason": "early round"}

    record_friction(
        pattern=f"Bounded loop reached attempt {attempt}/{max_attempts} in {session_context}",
        category="Iteration Cost",
        description=f"Loop for task {kwargs.get('task_id')} took multiple rounds",
        friction_impact="High" if attempt >= max_attempts else "Medium",
        session_context=session_context,
        recommended_fix_type="Add more specific Pre-Flight or handoff templates for this type of work",
        tags=["bounded-loop", "auto-hook", "iteration"],
    )

    return {
        "status": "success",
        "friction_recorded": True,
        "attempt": attempt,
        "hook": "auto_loop_ledger_sync",
    }
