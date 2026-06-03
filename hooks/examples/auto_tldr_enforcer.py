"""
Hook Handler: auto_tldr_enforcer

Port of tldr-read-enforcer / tldr-context-inject.
For exploration tasks (scout, research), enforces or suggests tldr-cli / tldr-code use before raw reads/grep.
Saves context (10-50x as per layered-recall).

Registered under "on_tldr_enforce" or called from preflight / on_agent_spawn for explore agents.
"""

from typing import Any, Dict

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        agent: str (e.g. scout, oracle, explore)
        task: str (user prompt or intent)
        files_read: int (rough count of raw reads so far)
    """
    agent = kwargs.get("agent", "").lower()
    task = kwargs.get("task", "").lower()
    files_read = kwargs.get("files_read", 0)

    explore_keywords = ["explore", "research", "scout", "find", "search", "understand codebase", "tldr"]
    is_explore = any(kw in task for kw in explore_keywords) or agent in ["scout", "explore", "oracle", "harvest", "pathfinder"]

    if is_explore and files_read > 5:  # threshold
        return {
            "decision": "suggest_tldr",
            "reason": "Exploration task detected with multiple raw reads. Use tldr structure/search/impact/dead/arch before more reads for token efficiency (10-50x savings). See tldr-cli.md and layered-recall.",
            "hook": "auto_tldr_enforcer",
            "agent": agent,
        }
    return {
        "decision": "ok",
        "hook": "auto_tldr_enforcer",
    }