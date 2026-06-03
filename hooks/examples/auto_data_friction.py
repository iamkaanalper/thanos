"""
Hook: on_data_analysis

Fired for data-analyst, data-pipeline-expert, neuron, ETL, analytics, feature engineering.
Records data friction (skew, leakage, drift, privacy, pipeline fragility).
Preflight for data quality + lineage.
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
    scope = kwargs.get("scope", "data scope")
    pipeline = kwargs.get("pipeline", "etl/feature/pipeline")
    session_context = kwargs.get("session_context", "")

    record_friction(
        pattern=f"Data analysis/pipeline: {scope} ({pipeline})",
        category="Data/Pipeline",
        description=f"Data work on {scope}. Data quality, leakage prevention, drift detection, privacy, reproducibility.",
        friction_impact="Medium",
        session_context=session_context,
        recommended_fix_type="data-analyst + neuron + schema validation + experiment tracking",
        tags=["data", "pipeline", "etl", "analytics", "feature", "ml"]
    )

    try:
        pf = run_preflight(
            task_description=f"Data: {scope} - {pipeline}",
            workspace_id=session_context or None
        )
    except Exception:
        pf = {}

    return {
        "hook": "on_data_analysis",
        "scope": scope,
        "friction_recorded": True,
        "preflight": pf.get("friction_checklist_brief", ""),
        "recommendation": "data-analyst + add on_compound for pipeline pattern capture"
    }
