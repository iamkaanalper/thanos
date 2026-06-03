"""
Hook Handler: auto_compound_learnings_trigger

This makes the compound-learnings system itself behave as a first-class hook-driven capability.

When hooks like on_compound_analysis_start or on_self_improvement_cycle fire,
this handler can:
- Automatically run the analyzer (via compound_bridge or trigger)
- Decide whether to run in light or full mode based on context
- Feed results back into the hook system

This is a key step in making self-improvement more automatic and less manual.
"""

from typing import Any, Dict

# Imports intentionally lazy (inside handle) to allow safe direct execution by TUI
# for pre/post_tool_use without triggering relative import errors in bundled/skills.


def handle(**kwargs) -> Dict[str, Any]:
    """
    Can be triggered by:
    - on_compound_analysis_start
    - on_self_improvement_cycle
    - on_run_completion (as a follow-up action)
    """
    # Lazy imports: prevents ModuleNotFound / relative import errors when the TUI
    # directly executes this script (registered in global/settings.local for pre/post tool use).
    from pathlib import Path
    try:
        from bundled.skills.shared.compound_bridge import feed_run_to_compound
        from bundled.skills.shared.compound_analyzer_trigger import trigger_compound_analyzer
    except ImportError:
        import sys
        sys.path.insert(0, str(Path.home() / ".grok" / "bundled" / "skills" / "shared"))
        from compound_bridge import feed_run_to_compound
        from compound_analyzer_trigger import trigger_compound_analyzer

    session_context = kwargs.get("session_context", "hook-triggered-analysis")
    force_analyzer = kwargs.get("force_analyzer", True)

    result = {
        "hook": "auto_compound_learnings_trigger",
        "session_context": session_context,
    }

    try:
        if force_analyzer:
            # Use the enhanced trigger (which already fires its own hooks)
            analyzer_result = trigger_compound_analyzer(
                min_patterns=kwargs.get("min_patterns", 2),
                source="hook_trigger",
                draft=True,
                session_context=session_context,
            )
            result["analyzer_result"] = analyzer_result
        else:
            # Use the higher-level bridge (records friction + fires hooks)
            bridge_result = feed_run_to_compound(
                session_context=session_context,
                issue_patterns=kwargs.get("issue_patterns", []),
                issues_by_severity=kwargs.get("issues_by_severity", {}),
                run_analyzer=True,
                tags=["hook-triggered"],
            )
            result["bridge_result"] = bridge_result

        result["status"] = "success"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


if __name__ == "__main__":
    # Direct execution by TUI for pre/post_tool_use (logged as global/settings.local source)
    # must not fail. Real work happens on handle() call.
    import sys
    sys.exit(0)
