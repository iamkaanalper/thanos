"""
Hook: on_swarm_start / on_swarm_phase / on_phase_end

Fired by SwarmOrchestrator at phase boundaries and key internal points.
- Records phase friction (slow phases, escalation clusters)
- Auto-triggers curation + compound at end of phase 5
- Injects cross-phase context (global friction summary)
- Closes bounded loops with ledger-aware signals
"""

from typing import Any, Dict

try:
    from bundled.skills.shared.friction import record_friction
    from bundled.skills.shared.friction_curator import run_friction_curation
except Exception:
    def record_friction(*a, **k): pass
    def run_friction_curation(*a, **k): return {}


def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        event: "start" | "phase_end" | "bounded_loop" | "escalation"
        phase: int (1-5)
        swarm_id: str
        track_id: str (optional)
        status: str
        details: dict (optional)
        session_context: str
    """
    event = kwargs.get("event", "phase")
    phase = kwargs.get("phase", 0)
    swarm_id = kwargs.get("swarm_id", "unknown-swarm")
    track_id = kwargs.get("track_id")
    status = kwargs.get("status", "")
    session_context = kwargs.get("session_context", swarm_id)
    details = kwargs.get("details", {})

    result = {
        "hook": "auto_swarm_phase",
        "event": event,
        "phase": phase,
        "swarm_id": swarm_id,
    }

    # Always record a low-friction breadcrumb for traceability
    try:
        record_friction(
            pattern=f"Swarm {event} (phase {phase})",
            category="Swarm/Orchestration",
            description=f"Swarm {swarm_id} {event} phase={phase} track={track_id} status={status}",
            friction_impact="Low",
            session_context=session_context,
            recommended_fix_type="Review phase report + per-track ledgers",
            tags=["swarm", "phase", event, f"phase-{phase}"]
        )
    except Exception:
        pass

    # High-signal cases
    if event == "escalation" or status == "escalated":
        record_friction(
            pattern=f"Swarm track escalated in phase {phase}",
            category="Swarm Escalation",
            description=f"Track {track_id} exhausted attempts. Details: {details}",
            friction_impact="High",
            session_context=session_context,
            recommended_fix_type="Reassign/decompose/revise per escalation options in ledger",
            tags=["swarm", "escalation", "qa-loop"]
        )

    if event == "bounded_loop" and phase == 3:
        # Already handled by auto_loop_ledger_sync in many cases, but reinforce
        record_friction(
            pattern="Swarm phase-3 bounded loop round recorded",
            category="Iteration Cost",
            description=f"Implementation round for {track_id}",
            friction_impact="Medium",
            session_context=session_context,
            tags=["swarm", "bounded-loop", "phase-3"]
        )

    # Phase 5 special: auto-curate + suggest compound
    if phase == 5 and event in ("phase_end", "completion"):
        try:
            curation = run_friction_curation(also_fire_hook=True)
            result["curation"] = curation
            # The compound hook will be fired by phase5 code or caller
        except Exception as e:
            result["curation_error"] = str(e)

    result["status"] = "success"
    return result
