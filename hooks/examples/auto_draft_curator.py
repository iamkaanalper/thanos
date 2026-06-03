"""
Hook: on_draft_generated

Fired after the compound analyzer successfully produces draft artifacts.

Responsibilities:
- Auto-curate / promote high-confidence drafts
- Record the event as friction or working solution
- Suggest next actions (e.g. "run --apply on these drafts")
"""

from typing import Any, Dict, List

try:
    from bundled.skills.shared.friction import record_friction
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / ".grok" / "bundled" / "skills" / "shared"))
    from friction import record_friction


def handle(**kwargs) -> Dict[str, Any]:
    draft_paths: List[str] = kwargs.get("draft_paths", [])
    session_context = kwargs.get("session_context", "")

    if not draft_paths:
        return {"status": "skipped", "reason": "no drafts"}

    # Record this as a positive self-improvement event
    record_friction(
        pattern=f"Compound analyzer produced {len(draft_paths)} new drafts",
        category="Self-Improvement Output",
        description=f"Drafts generated for session: {session_context}",
        friction_impact="Low",  # This is a good thing
        session_context=session_context,
        recommended_fix_type="Review and selectively apply the generated drafts using the --apply command",
        tags=["compound-learnings", "draft-generated", "auto-hook"],
    )

    return {
        "status": "success",
        "drafts_recorded": len(draft_paths),
        "suggestion": "Run: python3 ~/.grok/skills/compound-learnings/scripts/analyze.py --apply",
        "hook": "auto_draft_curator",
    }
