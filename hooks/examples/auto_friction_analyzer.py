"""
Hook: on_friction_recorded

Every time friction is recorded (via helper or bridge), this hook can:
- Analyze if this is a new high-frequency pattern
- Suggest creating a new Pre-Flight checklist item or rule
- Feed directly into compound-learnings drafts

MVP version: Simple frequency hint.
"""

from typing import Any, Dict

def handle(**kwargs) -> Dict[str, Any]:
    pattern = kwargs.get("pattern", "")
    category = kwargs.get("category", "")

    suggestions = []

    if "error" in category.lower() or "handling" in pattern.lower():
        suggestions.append("Add to Pre-Flight: 'Error handling & rollback checklist'")

    if "hook" in pattern.lower() or "state" in pattern.lower():
        suggestions.append("Consider new hook for this class of friction")

    return {
        "status": "success",
        "pattern_analyzed": pattern[:80],
        "auto_suggestions": suggestions,
        "hook": "auto_friction_analyzer",
    }
