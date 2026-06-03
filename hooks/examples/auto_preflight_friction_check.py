"""
Hook: on_implement_start

At the very beginning of a big implement/execute-plan run, this hook can:
- Pull recent high-impact friction patterns
- Inject them as a dynamic Pre-Flight briefing (exactly like the old friction_checklist_brief)

This is how the flywheel actually closes the loop in practice.
"""

from typing import Any, Dict

try:
    from bundled.skills.shared.friction import get_high_impact_patterns
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / ".grok" / "bundled" / "skills" / "shared"))
    from friction import get_high_impact_patterns


def handle(**kwargs) -> Dict[str, Any]:
    session_context = kwargs.get("session_context", "")

    try:
        patterns = get_high_impact_patterns(min_impact="Medium")
    except Exception:
        patterns = []

    return {
        "status": "success",
        "high_impact_patterns_found": len(patterns),
        "recommended_preflight_injection": patterns[:8],  # top 8
        "hook": "auto_preflight_friction_check",
        "note": "Orchestrator should inject these into the first implementer prompt as 'Recent Friction to Avoid'",
    }
