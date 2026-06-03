"""
Hook: on_agent_spawn

When any subagent is spawned (especially implementer, reviewer, verifier), 
this hook can automatically inject useful context (ledger state, recent friction patterns, etc.).

This is one of the highest-leverage behaviors from the original Claude Code AI software team system.
"""

from typing import Any, Dict

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        subagent_type: str
        description: str
        task_id: str (optional)
    """
    subagent_type = kwargs.get("subagent_type", "")
    description = kwargs.get("description", "")

    injected = []

    # If it's a long-running worker, suggest ledger context
    if any(x in subagent_type for x in ["implementer", "reviewer", "verifier", "kraken"]):
        injected.append("task_lifecycle_context")
        injected.append("recent_friction_patterns")

    return {
        "status": "success",
        "injected_context_suggestions": injected,
        "hook": "auto_spawn_context_injector",
        "note": "Orchestrator should call make_devqa_handoff_context + friction patterns here",
    }
