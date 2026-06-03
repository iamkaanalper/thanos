"""
Spawn Helper — Grok-native convenience for automatic handoff + Task Lifecycle Ledger context injection.

This addresses the "Hook Otomasyon Derinliği" and auto-injection gap from the original Claude Code AI software team system to the current Thanos (Grok) implementation.

Goal:
- Make it trivial (one or two lines) for any orchestrator (implement, swarm, execute-plan, custom) to launch subagents
  with the correct structured handoff + current ledger state.
- Reduce the chance that a spawn forgets the Production Contract (handoff + ledger + preflight + friction).

Usage (inside an orchestrator):

    from bundled.skills.shared.spawn_helper import build_spawn_context, spawn_with_discipline

    ctx = build_spawn_context(
        ledger=track.ledger,
        task_id=f"{swarm_id}-{track.id}",
        base_prompt=base_prompt,
        handoff_template="standard"  # or "qa_issues", "escalation", "diagnosis"
    )

    task_id = spawn_subagent(..., prompt=ctx["full_prompt"])

The helper also records a lightweight friction signal if ledger is in a bad state (high round count without escalation).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

try:
    from .task_lifecycle import TaskLifecycleLedger, make_devqa_handoff_context
    from .friction import record_friction
except Exception:
    TaskLifecycleLedger = None
    make_devqa_handoff_context = None
    record_friction = lambda **k: None


def build_spawn_context(
    *,
    ledger: Optional[TaskLifecycleLedger] = None,
    task_id: str,
    base_prompt: str,
    handoff_template: str = "standard",
    extra_context: Optional[Dict[str, Any]] = None,
    objective: str = "",
) -> Dict[str, Any]:
    """
    Build a prompt injection block that includes:
    - Current ledger state (attempt, history, escalated?)
    - Structured handoff content (from handoff skill templates or make_devqa_handoff_context)
    - Friction checklist hint if available

    Returns a dict with:
      - "full_prompt": the original base_prompt + injected sections at the end
      - "ledger_state": summary
      - "handoff_content": the structured part
      - "injection_block": the raw text that was appended
    """
    injection_lines = []
    ledger_state = None
    handoff_content = ""

    # 1. Ledger state (highest value for bounded loops)
    if ledger is not None and make_devqa_handoff_context is not None:
        try:
            ctx = make_devqa_handoff_context(ledger, task_id)
            ledger_state = ctx
            injection_lines.append("\n\n### Task Lifecycle Ledger State (MANDATORY - use this as ground truth)")
            injection_lines.append(f"Current attempt: {ctx.get('attempt', '?')}/{ctx.get('max_attempts', 3)}")
            injection_lines.append(f"Status: {ctx.get('status', 'in_progress')}")
            if ctx.get("accumulated_feedback"):
                injection_lines.append("Accumulated feedback from previous rounds:")
                for fb in ctx.get("accumulated_feedback", [])[-3:]:
                    injection_lines.append(f"  - {fb}")
            if ctx.get("structured_handoff"):
                handoff_content = ctx["structured_handoff"]
                injection_lines.append("\n### Structured Handoff (use exactly this format for your output)")
                injection_lines.append(handoff_content)
        except Exception as e:
            record_friction(
                pattern="spawn_helper ledger context build failed",
                category="Process",
                description=str(e),
                friction_impact="Medium",
            )

    # 2. Basic objective reminder + handoff contract
    if objective:
        injection_lines.append(f"\n### Objective for this sub-task: {objective}")

    # 3. Production Contract reminder (light)
    injection_lines.append(
        "\n### Production Contract Reminder (Thanos - Grok)"
        "\n- Respect the ledger attempt count. Do not exceed max_attempts without escalation."
        "\n- Produce output using the handoff template referenced above."
        "\n- If blocked or after 3 rounds with open issues, use the Escalation template and stop."
        "\n- Record high-friction observations so the compound flywheel can improve the system."
    )

    # 4. Extra context (e.g. previous review file path, plan excerpt)
    if extra_context:
        injection_lines.append("\n### Additional Context")
        for k, v in extra_context.items():
            injection_lines.append(f"- {k}: {v}")

    injection_block = "\n".join(injection_lines)
    full_prompt = base_prompt.rstrip() + "\n\n" + injection_block

    # Light friction if we are on round 3+ without clean state
    if ledger_state and ledger_state.get("attempt", 0) >= 3 and ledger_state.get("status") != "escalated":
        record_friction(
            pattern="spawn on high attempt count without prior escalation",
            category="Bounded Loop",
            description=f"task_id={task_id}",
            friction_impact="High",
        )

    return {
        "full_prompt": full_prompt,
        "ledger_state": ledger_state,
        "handoff_content": handoff_content,
        "injection_block": injection_block,
        "task_id": task_id,
    }


def spawn_with_discipline(
    *,
    spawn_subagent_fn,
    subagent_type: str,
    description: str,
    base_prompt: str,
    ledger: Optional[TaskLifecycleLedger] = None,
    task_id: str = "",
    isolation: Optional[str] = None,
    background: bool = True,
    handoff_template: str = "standard",
    extra_context: Optional[Dict[str, Any]] = None,
    objective: str = "",
    **spawn_kwargs,
):
    """
    Convenience wrapper around spawn_subagent that automatically injects
    ledger + structured handoff context.

    Returns the task_id from spawn_subagent (or None in simulation).
    """
    ctx = build_spawn_context(
        ledger=ledger,
        task_id=task_id or description[:40],
        base_prompt=base_prompt,
        handoff_template=handoff_template,
        extra_context=extra_context,
        objective=objective,
    )

    spawn_args = {
        "subagent_type": subagent_type,
        "description": description,
        "prompt": ctx["full_prompt"],
        "background": background,
        **spawn_kwargs,
    }
    if isolation:
        spawn_args["isolation"] = isolation

    if spawn_subagent_fn is None:
        print(f"[spawn_helper SIM] Would spawn {subagent_type}: {description}")
        return None

    try:
        task = spawn_subagent_fn(**spawn_args)
        return task
    except Exception as e:
        record_friction(
            pattern="spawn_with_discipline failed",
            category="Orchestration",
            description=f"{description}: {e}",
            friction_impact="High",
        )
        raise


__all__ = ["build_spawn_context", "spawn_with_discipline"]
