"""
Hook: on_observability_setup

Fired when observability-expert, prometheus, tracing, logging, metrics, SLO work.
Records obs friction (cardinality, blind spots, alert fatigue, sampling).
Preflight for monitoring coverage.
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
    scope = kwargs.get("scope", "observability scope")
    stack = kwargs.get("stack", "prometheus/otel/grafana")
    session_context = kwargs.get("session_context", "")

    record_friction(
        pattern=f"Observability setup: {scope} ({stack})",
        category="Observability/Monitoring",
        description=f"Monitoring for {scope}. Cardinality control, coverage gaps, SLO definition, on-call paths.",
        friction_impact="Medium",
        session_context=session_context,
        recommended_fix_type="observability-expert + tracing-expert + SLO + incident response runbooks",
        tags=["observability", "prometheus", "otel", "tracing", "metrics", "slo"]
    )

    try:
        pf = run_preflight(
            task_description=f"Obs: {scope} - {stack}",
            workspace_id=session_context or None
        )
    except Exception:
        pf = {}

    return {
        "hook": "on_observability_setup",
        "scope": scope,
        "friction_recorded": True,
        "preflight": pf.get("friction_checklist_brief", ""),
        "recommendation": "observability-expert + wire on_phase_end for metric validation"
    }
