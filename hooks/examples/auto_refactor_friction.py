"""
Hook: on_refactor_pass

Fired when refactor-cleaner, janitor, dead-code removal, tech-debt, ai-slop-cleaner runs.
Records refactor friction (behavior change, test gaps, hidden deps, over-clean).
Preflight for safe cleanup.
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
    target = kwargs.get("target", "module/file set")
    scope = kwargs.get("scope", "dead-code / duplication / slop")
    session_context = kwargs.get("session_context", "")

    record_friction(
        pattern=f"Refactor pass: {scope} on {target}",
        category="Refactor/TechDebt",
        description=f"Cleanup on {target}. Ensure tests cover removed paths, no behavior regression, call-graph validated.",
        friction_impact="Medium",
        session_context=session_context,
        recommended_fix_type="refactor-cleaner + janitor + tdd-guide for regression tests + coroner for pattern propagation",
        tags=["refactor", "janitor", "dead-code", "tech-debt", "slop"]
    )

    try:
        pf = run_preflight(
            task_description=f"Refactor: {scope} - {target}",
            workspace_id=session_context or None
        )
    except Exception:
        pf = {}

    return {
        "hook": "on_refactor_pass",
        "target": target,
        "friction_recorded": True,
        "preflight": pf.get("friction_checklist_brief", ""),
        "recommendation": "refactor-cleaner + run tests + coroner after"
    }
