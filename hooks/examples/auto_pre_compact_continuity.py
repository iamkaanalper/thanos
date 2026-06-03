"""
Hook Handler: auto_pre_compact_continuity

Port of pre-compact-continuity.
On session compress warning or pre-compact, dump state to palace + .grok/projects/<wing>/wip-state.jsonl (structured WIP).
Integrates with pre-compact-state rule, memory-palace, layered-recall, auto_session_compressor.

Called from on_pre_compact or session compressor.
"""

from typing import Any, Dict
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECTS = Path.home() / ".grok" / "projects"
PALACE = Path.home() / ".grok" / "palace"

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        wing: project name
        active_task: str
        status: str
        completed: list
        remaining: list
        modified_files: list
        decision_context: str
        context_needed: str
    """
    wing = kwargs.get("wing", "default")
    state = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "active_task": kwargs.get("active_task", "unknown"),
        "status": kwargs.get("status", "in_progress"),
        "completed": kwargs.get("completed", []),
        "remaining": kwargs.get("remaining", []),
        "modified_files": kwargs.get("modified_files", []),
        "decision_context": kwargs.get("decision_context", ""),
        "context_needed": kwargs.get("context_needed", ""),
        "hook": "auto_pre_compact_continuity",
    }

    # Save to project wip
    proj_dir = PROJECTS / wing
    proj_dir.mkdir(parents=True, exist_ok=True)
    wip_file = proj_dir / "wip-state.jsonl"
    with wip_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(state, ensure_ascii=False) + "\n")

    # Also append to palace for global
    palace_file = PALACE / f"{wing}.jsonl"
    PALACE.mkdir(parents=True, exist_ok=True)
    palace_entry = {
        "id": f"wip-{state['timestamp']}",
        "wing": wing,
        "room": "pre-compact",
        "content": json.dumps(state),
        "tags": ["pre-compact", "continuity", "wip"],
        "timestamp": state["timestamp"],
        "type": "state",
    }
    with palace_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(palace_entry, ensure_ascii=False) + "\n")

    return {
        "status": "success",
        "hook": "auto_pre_compact_continuity",
        "wing": wing,
        "saved_to": str(wip_file),
    }