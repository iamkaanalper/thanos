"""
Hook: on_agent_lint

Fired by agent-linter or after new agent/skill creation.
Records quality friction for low-score agents (missing sections, no team-dynamics, no compound participation).
Used to auto-improve the agent surface.
"""

from typing import Any, Dict

try:
    from bundled.skills.shared.friction import record_friction
except Exception:
    def record_friction(*a, **k): pass


def handle(**kwargs) -> Dict[str, Any]:
    agent_name = kwargs.get("agent_name", "unknown")
    score = kwargs.get("quality_score", 0)
    issues = kwargs.get("issues", [])
    session_context = kwargs.get("session_context", "")

    if score >= 80:
        return {"status": "skipped", "reason": "high quality agent"}

    record_friction(
        pattern=f"Agent lint low score: {agent_name} ({score})",
        category="Agent Quality",
        description=f"Linter found {len(issues)} issues on {agent_name}. Missing team-dynamics/compound/ledger refs likely.",
        friction_impact="Medium",
        session_context=session_context,
        recommended_fix_type="Update agent frontmatter + add Self-Improvement Participation + ledger/handoff sections",
        tags=["agent-linter", "quality", agent_name]
    )

    return {
        "hook": "on_agent_lint",
        "agent": agent_name,
        "score": score,
        "friction_recorded": True,
        "suggestion": "Re-run agent-linter after fixes; promote high-value patterns to shared/"
    }
