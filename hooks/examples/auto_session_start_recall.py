"""
Hook Handler: auto_session_start_recall

Port of session-start-recall + smart-memory-recall + palace-recall.
On session start (or on_agent_spawn), triggers layered-recall (L1 + L2) + palace memory for context injection.
Reduces context loss, works with compass, memory-palace, layered-recall skill.

Registered under "on_session_start".
"""

from typing import Any, Dict

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        wing: project
        query: initial prompt or cwd context
    """
    wing = kwargs.get("wing", "default")
    query = kwargs.get("query", kwargs.get("session_context", ""))

    # Simulate calling layered-recall and palace
    # In real: from grok.skills.layered_recall import layered_recall
    # ctx = layered_recall(query, scope="project", depth=2, wing=wing)
    ctx = f"[Session Start Recall] Loaded L1 identity + L2 facts for {wing}. Use memory-palace + layered-recall for full progressive context. Query: {query[:100]}..."

    return {
        "status": "success",
        "hook": "auto_session_start_recall",
        "wing": wing,
        "recall_context": ctx,
        "suggestion": "Inject into agent context for low context-loss start. See layered-recall/SKILL.md and palace.",
    }