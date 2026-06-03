"""
Hook Handler: auto_palace_recall (or palace-recall)

Injects relevant memories from memory-palace + layered-recall at session start / on_agent_spawn.
Uses progressive (L1-L3) to keep context small.
"""

from typing import Any, Dict
import json
from pathlib import Path

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        wing: project
        query: current task/domain for L3 room
        max_tokens: budget for recall (default ~2000)
    Returns context snippet for injection.
    """
    wing = kwargs.get("wing", "default")
    query = kwargs.get("query", "") or kwargs.get("session_context", "")
    max_tokens = kwargs.get("max_tokens", 2000)

    PALACE = Path.home() / ".grok" / "palace"
    PROJECTS = Path.home() / ".grok" / "projects"

    context = []
    tokens = 0

    # L1: Identity from palace or projects/default
    id_mem = PROJECTS / "default" / "MEMORY.md"
    if id_mem.exists():
        l1 = id_mem.read_text()[:300]
        context.append(f"[L1 Identity]\n{l1}")
        tokens += 300

    # L2: Project facts
    proj_mem = PROJECTS / wing / "MEMORY.md"
    if proj_mem.exists():
        l2 = proj_mem.read_text()[:500]
        context.append(f"[L2 Project Facts for {wing}]\n{l2}")
        tokens += 500

    # L3: Room recall from palace jsonl if query
    if query and tokens < max_tokens:
        wing_file = PALACE / f"{wing}.jsonl"
        if wing_file.exists():
            for line in wing_file.read_text().splitlines():
                if tokens > max_tokens:
                    break
                try:
                    d = json.loads(line)
                    if query.lower() in d.get("content", "").lower() or any(query.lower() in t.lower() for t in d.get("tags", [])):
                        preview = d.get("content", "")[:100]
                        context.append(f"[L3 Room:{d.get('room')} id:{d.get('id')}] {preview}...")
                        tokens += 120
                except:
                    pass

    recall_ctx = "\n\n".join(context) if context else "No prior palace memories for this query."
    return {
        "status": "success",
        "hook": "auto_palace_recall",
        "wing": wing,
        "recall_context": recall_ctx[:max_tokens],
        "tokens_used": min(tokens, max_tokens),
    }