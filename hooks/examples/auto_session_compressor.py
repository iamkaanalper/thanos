"""
Hook Handler: auto_session_compressor

Pre-compact state preservation and compression.
Analog to pre-compact-continuity and session-compressor.
Uses our notepad or palace for WIP.
"""

from typing import Any, Dict

try:
    from grok.skills.memory_palace import store_memory
except Exception:
    def store_memory(*a, **k): pass

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        trigger: "pre_compact" or "session_end"
        active_task: str
        modified_files: list
        decisions: list
        session_context: str
    """
    trigger = kwargs.get("trigger", "pre_compact")
    active_task = kwargs.get("active_task", "")
    modified = kwargs.get("modified_files", [])
    decisions = kwargs.get("decisions", [])
    session_context = kwargs.get("session_context", "")

    try:
        content = f"Pre-compact snapshot: task={active_task}, files={len(modified)}, decisions={len(decisions)}"
        store_memory(
            wing=session_context or "default",
            room="session-state",
            content=content,
            tags=["pre-compact", "compressor", "auto-hook"],
            type="state"
        )
        return {
            "status": "success",
            "hook": "auto_session_compressor",
            "trigger": trigger,
            "saved": True,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "hook": "auto_session_compressor",
        }
