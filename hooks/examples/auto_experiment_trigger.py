"""
Hook Handler: auto_experiment_trigger

Triggers experiment-loop on perf sensitive or compound signals.
"""

from typing import Any, Dict

try:
    from grok.skills.experiment_loop import run_experiment  # stub
except Exception:
    def run_experiment(*a, **k): pass

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        trigger: "perf_bottleneck" or "compound_suggestion"
        metric: str
        target: str
        session_context: str
    """
    trigger = kwargs.get("trigger", "")
    metric = kwargs.get("metric", "")
    target = kwargs.get("target", "")
    session_context = kwargs.get("session_context", "")

    if not trigger or not metric:
        return {"status": "skipped"}

    try:
        # Would call the experiment loop skill
        run_experiment(
            metric=metric,
            target=target,
            context=session_context,
            trigger=trigger
        )
        return {
            "status": "success",
            "hook": "auto_experiment_trigger",
            "trigger": trigger,
            "metric": metric,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "hook": "auto_experiment_trigger",
        }
