"""
Hook: on_analyzer_start

Fired right before the compound analyzer runs.

Can be used to:
- Inject recent high-impact friction as extra context to the analyzer
- Adjust min_patterns based on current system state
- Log or record that analysis was triggered by a specific run
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
    min_patterns = kwargs.get("min_patterns", 2)

    try:
        recent_patterns = get_high_impact_patterns(min_impact="Medium")
    except Exception:
        recent_patterns = []

    return {
        "status": "success",
        "recent_high_impact_patterns": len(recent_patterns),
        "recommended_extra_context": recent_patterns[:5],
        "hook": "auto_analyzer_preflight",
        "note": "Analyzer should receive these patterns as additional input for better clustering",
    }
