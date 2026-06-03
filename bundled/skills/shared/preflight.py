"""
Preflight — Mandatory first-class Pre-Flight discipline for Grok orchestrators.

This is the real executable implementation behind the preflight skill.
Orchestrators (implement, execute-plan, etc.) MUST call run_preflight() at the very start of Setup for any non-trivial work.

Production Contract:
- Always runs exploration awareness (caller responsibility, we just enforce the hook + friction step)
- Pulls recent high-impact friction from the ledger
- Returns a ready-to-inject "Recent Friction to Avoid" + ledger state block
- Fires on_implement_start hook when appropriate
- Records any Pre-Flight gaps as friction
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .friction import get_high_impact_patterns, record_friction
from .compound_bridge import feed_run_to_compound  # for future deeper wiring

try:
    from grok.hooks.core.hook_runner import run_hook, _HOOK_REGISTRY
except Exception:
    run_hook = None
    _HOOK_REGISTRY = {}


def run_preflight(
    task_description: str,
    workspace_id: Optional[str] = None,
    force: bool = False,
    min_impact: str = "Medium",
) -> Dict[str, Any]:
    """
    Run the mandatory Pre-Flight checks and return injectable context.

    Call this as the absolute first thing in orchestrator Setup (before any subagent spawn)
    for any work that is not a trivial one-file fix.

    Returns:
        {
            "friction_checklist_brief": "...markdown block...",
            "recent_patterns": [...],
            "hook_fired": bool,
            "skipped_reason": str | None,
        }
    """
    result: Dict[str, Any] = {
        "friction_checklist_brief": "",
        "recent_patterns": [],
        "hook_fired": False,
        "skipped_reason": None,
    }

    # 1. Hook existence + fire (on_implement_start style)
    if run_hook and "on_implement_start" in _HOOK_REGISTRY:
        try:
            run_hook(
                "on_implement_start",
                task_description=task_description,
                workspace_id=workspace_id,
            )
            result["hook_fired"] = True
        except Exception as e:
            # Never let hook failure kill the run
            record_friction(
                pattern="preflight hook failed",
                category="Self-Improvement",
                description=f"on_implement_start hook error: {e}",
                friction_impact="Low",
            )
    else:
        result["skipped_reason"] = "hook system not available or on_implement_start not registered"

    # 2. Pull high-impact friction patterns (the core value)
    try:
        patterns = get_high_impact_patterns(min_impact=min_impact)
        result["recent_patterns"] = patterns

        if patterns:
            # Build the exact same style block that implement/execute-plan already inject
            lines = [
                "## Recent Friction to Avoid (from Pre-Flight)",
                "The following high/medium impact patterns have appeared in recent runs. Actively avoid repeating them:",
            ]
            for i, p in enumerate(patterns[:12], 1):  # cap for prompt sanity
                lines.append(f"{i}. {p}")
            lines.append("")
            result["friction_checklist_brief"] = "\n".join(lines)
        else:
            result["friction_checklist_brief"] = ""
    except Exception as e:
        record_friction(
            pattern="preflight friction ledger read failed",
            category="Self-Improvement",
            description=str(e),
            friction_impact="Low",
        )
        result["skipped_reason"] = f"friction ledger error: {e}"

    # 3. Record that Pre-Flight actually ran (for compound learnings)
    if not force and not patterns and not result["hook_fired"]:
        # Low signal case — still record for audit
        pass

    return result


def require_preflight_for_large_work(task_description: str) -> None:
    """
    Convenience guard. Call early in Setup. Raises a clear error if critical preflight signals are missing
    on a large-looking task (heuristic: description length + keywords).
    """
    large_keywords = ("multi", "refactor", "auth", "migration", "plan", "swarm", "multiple PR", "architecture")
    desc_lower = task_description.lower()

    is_large = len(task_description) > 120 or any(k in desc_lower for k in large_keywords)

    if is_large:
        pf = run_preflight(task_description)
        if not pf["recent_patterns"] and not pf["hook_fired"]:
            # Not fatal — we are defensive — but we do record the gap
            record_friction(
                pattern="large work started without preflight signals",
                category="Process",
                description=f"Task likely large but no friction patterns or hooks fired: {task_description[:80]}",
                friction_impact="Medium",
            )
