"""
Hook: on_friction_detected - Auto Tagger

When friction is recorded (manually or via completion helper), this hook can
automatically add tags, deduplicate, or boost impact based on rules.

For now: simple auto-tagging based on keywords.
"""

from typing import Any, Dict, List

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        pattern: str
        category: str
        description: str
        current_tags: list (optional)
    """
    pattern = kwargs.get("pattern", "").lower()
    category = kwargs.get("category", "")
    description = kwargs.get("description", "").lower()
    current_tags: List[str] = kwargs.get("current_tags", [])

    auto_tags = set(current_tags)

    # Simple keyword-based auto tagging (can be made much smarter later)
    if any(word in pattern + description for word in ["race", "atomic", "concurrent", "hook", "state"]):
        auto_tags.add("concurrency-risk")

    if any(word in pattern + description for word in ["error", "exception", "handling", "rollback"]):
        auto_tags.add("error-handling")

    if "security" in category.lower() or any(word in pattern + description for word in ["auth", "secret", "injection"]):
        auto_tags.add("security")

    if "verifier" in (kwargs.get("tags") or []):
        auto_tags.add("final-gate")

    return {
        "status": "success",
        "added_tags": list(auto_tags - set(current_tags)),
        "final_tags": list(auto_tags),
        "hook": "auto_friction_tagger",
    }
