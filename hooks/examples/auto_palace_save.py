"""
Hook Handler: auto_palace_save

Analog to Claude's palace-auto-save hook.
Integrates with the memory-palace + layered-recall skills.
Fired on key events to auto-capture decisions into .grok/palace/ JSONL + .grok/projects/<wing>/ for pre-compact/WIP.
"""

from typing import Any, Dict
import json
from datetime import datetime, timezone
from pathlib import Path

PALACE_DIR = Path.home() / ".grok" / "palace"
PROJECTS_DIR = Path.home() / ".grok" / "projects"

def _append_to_palace(wing: str, room: str, content: str, tags: list, agent: str, event: str):
    PALACE_DIR.mkdir(parents=True, exist_ok=True)
    wing_file = PALACE_DIR / f"{wing}.jsonl"
    entry = {
        "id": f"d-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "wing": wing,
        "room": room,
        "content": content,
        "tags": tags + ["auto-hook", "palace-save"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "type": event
    }
    with wing_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    # Update index
    idx_file = PALACE_DIR / "index.json"
    idx = {}
    if idx_file.exists():
        idx = json.loads(idx_file.read_text(encoding="utf-8"))
    if "wings" not in idx:
        idx["wings"] = {}
    if wing not in idx["wings"]:
        idx["wings"][wing] = {"rooms": [], "last_updated": ""}
    if room not in idx["wings"][wing]["rooms"]:
        idx["wings"][wing]["rooms"].append(room)
    idx["wings"][wing]["last_updated"] = entry["timestamp"]
    idx_file.write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8")
    return entry["id"]

def _save_wip_to_project(wing: str, content: str):
    """For pre-compact: save WIP state to .grok/projects/<wing>/wip-state.jsonl"""
    proj = PROJECTS_DIR / wing
    proj.mkdir(parents=True, exist_ok=True)
    wip = proj / "wip-state.jsonl"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": "pre-compact-wip",
        "content": content[:2000],  # summary
        "agent": "auto_palace_save"
    }
    with wip.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        event: str like "decision", "error", "pattern", "pre-compact"
        wing: project name (default from context)
        room: domain e.g. auth, infra
        content: the decision or learning
        tags: list
        session_context: str
        agent: str
    """
    event = kwargs.get("event", "decision")
    wing = kwargs.get("wing") or kwargs.get("session_context", "default").replace("/", "-")[:50]
    room = kwargs.get("room", "general")
    content = kwargs.get("content", "")
    tags = kwargs.get("tags", [event])
    agent = kwargs.get("agent", "unknown")

    if not content:
        return {"status": "skipped", "reason": "no content"}

    try:
        entry_id = _append_to_palace(wing, room, content, tags, agent, event)
        if event == "pre-compact" or "wip" in str(tags).lower():
            _save_wip_to_project(wing, content)
        return {
            "status": "success",
            "hook": "auto_palace_save",
            "wing": wing,
            "room": room,
            "entry_id": entry_id,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "hook": "auto_palace_save",
        }
