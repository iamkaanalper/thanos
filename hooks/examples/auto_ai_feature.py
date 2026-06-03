"""
Auto handler for on_ai_feature hook.

Fires when ai-engineer is involved in a feature (prompt, RAG, agent, LLM integration).

Records friction for AI-specific patterns (hallucination risk, cost, eval debt, PII in prompts).
Injects AI-specific preflight (evals, tracing, cost estimate).
"""

from pathlib import Path
from typing import Any, Dict

try:
    from bundled.skills.shared.friction import record_friction
    from bundled.skills.shared.preflight import run_preflight
except Exception:
    def record_friction(*a, **k): pass
    def run_preflight(*a, **k): return {}

def handle(**kwargs) -> Dict[str, Any]:
    feature = kwargs.get("feature", "unknown AI feature")
    objective = kwargs.get("objective", "")
    session_context = kwargs.get("session_context", "")

    # Record AI-specific friction
    record_friction(
        pattern=f"AI feature started: {feature}",
        category="AI/LLM",
        description=f"AI/LLM integration for {objective}. Ensure evals, cost tracking, tracing, PII redaction.",
        friction_impact="Medium",
        session_context=session_context,
        recommended_fix_type="ai-engineer review + eval harness + observability",
        tags=["ai", "llm", "prompt", "rag"]
    )

    # Preflight for AI (evals, cost, safety)
    try:
        pf = run_preflight(
            task_description=f"AI feature: {feature} - {objective}",
            workspace_id=session_context or None
        )
    except Exception:
        pf = {}

    # Suggest hook for compound
    return {
        "hook": "on_ai_feature",
        "feature": feature,
        "friction_recorded": True,
        "preflight": pf.get("friction_checklist_brief", ""),
        "recommendation": "Call ai-engineer + add on_draft_applied for prompt evolution"
    }
