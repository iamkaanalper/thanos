"""
Hook: on_infra_change

Fired when devops-expert, terraform, k8s, docker, ci/cd work happens.
Records infra-specific friction (drift, secret leak, cost, rollback risk).
Triggers preflight for IaC safety.
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
    change = kwargs.get("change", "infra change")
    tool = kwargs.get("tool", "terraform/k8s/docker")
    session_context = kwargs.get("session_context", "")

    record_friction(
        pattern=f"Infra change: {change} via {tool}",
        category="Infra/DevOps",
        description=f"Infrastructure modification. Ensure drift detection, secret hygiene, cost guard, rollback plan.",
        friction_impact="High",
        session_context=session_context,
        recommended_fix_type="devops-expert review + terraform plan + canary + observability",
        tags=["infra", "devops", "terraform", "k8s", "docker", "ci"]
    )

    try:
        pf = run_preflight(
            task_description=f"Infra: {change} ({tool})",
            workspace_id=session_context or None
        )
    except Exception:
        pf = {}

    return {
        "hook": "on_infra_change",
        "change": change,
        "friction_recorded": True,
        "preflight": pf.get("friction_checklist_brief", ""),
        "recommendation": "Call devops-expert + add on_phase_end for infra validation"
    }
