"""
Hook Handler: auto_skill_compounder

For skill-evolution and compound learnings.
Observes skill usage and triggers compounding / evolution scoring.
"""

from typing import Any, Dict

try:
    from grok.skills.skill_evolution import score_skill_execution
    from bundled.skills.shared.compound_bridge import feed_run_to_compound
except Exception:
    def score_skill_execution(*a, **k): pass
    def feed_run_to_compound(*a, **k): pass

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        skill_name: str
        execution_result: dict with scores or outcome
        session_context: str
        agent: str
    """
    skill_name = kwargs.get("skill_name", "unknown")
    execution_result = kwargs.get("execution_result", {})
    session_context = kwargs.get("session_context", "")

    try:
        # Score it
        score_skill_execution(
            skill_name=skill_name,
            result=execution_result,
            context=session_context
        )

        # Feed to compound if high signal
        if execution_result.get("score", 0) > 70 or "friction" in str(execution_result).lower():
            feed_run_to_compound(
                session_context=session_context,
                issue_patterns=[f"skill:{skill_name}"],
                issues_by_severity={"medium": 1},
                run_analyzer=True,
                tags=["skill-compound", "auto-hook"]
            )

        return {
            "status": "success",
            "hook": "auto_skill_compounder",
            "skill": skill_name,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "hook": "auto_skill_compounder",
        }
