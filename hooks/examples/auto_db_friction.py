"""
Hook: on_db_change

Fired for database-reviewer, postgres, mongo, schema migrations, query optimization, vault.
Records DB friction (migration risk, lock, data loss, perf regression, backup gaps).
Preflight for schema safety + migration plan.
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
    change = kwargs.get("change", "schema/index/migration")
    db = kwargs.get("db", "postgres/mongo")
    session_context = kwargs.get("session_context", "")

    record_friction(
        pattern=f"DB change: {change} on {db}",
        category="Database/Schema",
        description=f"Database modification {change}. Migration safety, zero-downtime, backup/restore test, query impact.",
        friction_impact="High",
        session_context=session_context,
        recommended_fix_type="database-reviewer + vault + migration rehearsal + rollback script",
        tags=["db", "postgres", "mongo", "schema", "migration", "index"]
    )

    try:
        pf = run_preflight(
            task_description=f"DB: {change} ({db})",
            workspace_id=session_context or None
        )
    except Exception:
        pf = {}

    return {
        "hook": "on_db_change",
        "change": change,
        "friction_recorded": True,
        "preflight": pf.get("friction_checklist_brief", ""),
        "recommendation": "database-reviewer + require migration tests before apply"
    }
