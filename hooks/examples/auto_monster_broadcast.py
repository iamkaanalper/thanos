"""
Hook Handler: auto_monster_broadcast

Cross-training: one agent's mistake trains the whole team.
Analog to monster error broadcast, skill tracker.
Feeds friction to compound and other agents via hooks.
"""

from typing import Any, Dict

try:
    from bundled.skills.shared.friction import record_friction
    from bundled.skills.shared.compound_bridge import feed_run_to_compound
except Exception:
    def record_friction(*a, **k): pass
    def feed_run_to_compound(*a, **k): pass

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        agent: str (the one that errored)
        error_type: str
        lesson: str
        session_context: str
        severity: str
    """
    agent = kwargs.get("agent", "unknown")
    error_type = kwargs.get("error_type", "generic")
    lesson = kwargs.get("lesson", "")
    session_context = kwargs.get("session_context", "")
    severity = kwargs.get("severity", "medium")

    try:
        record_friction(
            pattern=f"monster broadcast: {agent} failed with {error_type}",
            category="Cross-Training",
            description=lesson,
            friction_impact="High" if severity == "critical" else "Medium",
            session_context=session_context,
            recommended_fix_type="Update all similar agents + compound evolution",
            tags=["monster", "cross-train", "auto-hook", agent]
        )

        feed_run_to_compound(
            session_context=session_context,
            issue_patterns=[f"agent-error:{agent}:{error_type}"],
            issues_by_severity={severity: 1},
            run_analyzer=True,
            tags=["monster", "auto"]
        )

        # === Full monster persistence (error-ledger + skill-matrix update) ===
        from datetime import datetime, timezone
        from pathlib import Path
        import json

        monster_DIR = Path.home() / ".grok" / "monster"
        LEDGER = monster_DIR / "error-ledger.jsonl"
        MATRIX = monster_DIR / "skill-matrix.json"

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent,
            "error_type": error_type,
            "lesson": lesson,
            "severity": severity,
            "session_context": session_context[:200] if session_context else "",
        }
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # Update skill-matrix (simple increment)
        mat = {}
        if MATRIX.exists():
            try:
                mat = json.loads(MATRIX.read_text(encoding="utf-8"))
            except Exception:
                mat = {"agents": {}}
        if "agents" not in mat:
            mat["agents"] = {}
        ad = mat["agents"].setdefault(agent, {"success_rate": 80, "error_count": 0, "lessons_learned": 0, "avg_evolution_score": 80, "last_error": None, "tags": ["auto"]})
        ad["error_count"] = ad.get("error_count", 0) + 1
        ad["last_error"] = entry["timestamp"]
        ad["lessons_learned"] = ad.get("lessons_learned", 0) + 1
        # simple decay on success_rate
        ad["success_rate"] = max(50, ad.get("success_rate", 80) - 2)
        ad["avg_evolution_score"] = max(50, ad.get("avg_evolution_score", 80) - 1)
        mat["updated"] = entry["timestamp"]
        MATRIX.parent.mkdir(parents=True, exist_ok=True)
        MATRIX.write_text(json.dumps(mat, indent=2, ensure_ascii=False), encoding="utf-8")

        return {
            "status": "success",
            "hook": "auto_monster_broadcast",
            "agent": agent,
            "broadcast": True,
            "ledger_written": True,
            "matrix_updated": True,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "hook": "auto_monster_broadcast",
        }
