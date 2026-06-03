"""
Example Hook: Auto Completion Friction

When a big run finishes (implement, execute-plan, etc.), this hook automatically
calls our completion_friction helper so the patterns get recorded without the
orchestrator having to remember to do it manually.

This is exactly the kind of "set and forget" behavior that made the original Claude Code AI software team system powerful.
"""

from typing import Any, Dict

# Note: import moved inside handle() for direct script execution safety.
# When TUI (global/settings.local) does `python auto_completion_friction.py` it must not
# trigger the relative import chain in bundled that assumes package context.



def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        session_context: str
        issue_patterns: list[str]
        issues_by_severity: dict
        run_description: str (optional)
        tags: list[str] (optional)
    """
    # Lazy import so that direct `python this.py` (TUI pre/post tool use from global/settings.local)
    # does not execute bundled relative imports that require package context.
    from pathlib import Path
    try:
        from bundled.skills.shared.completion_friction import capture_run_completion_friction
    except ImportError:
        import sys
        sys.path.insert(0, str(Path.home() / ".grok" / "bundled" / "skills" / "shared"))
        from completion_friction import capture_run_completion_friction

    session_context = kwargs.get("session_context", "unknown-run")
    issue_patterns = kwargs.get("issue_patterns", [])
    issues_by_severity = kwargs.get("issues_by_severity", {})

    if not issue_patterns and not issues_by_severity:
        return {"status": "skipped", "reason": "no patterns or issues to record"}

    tags = kwargs.get("tags", ["auto-hook"])
    run_description = kwargs.get("run_description", session_context)

    try:
        records = capture_run_completion_friction(
            session_context=session_context,
            issue_patterns=issue_patterns,
            issues_by_severity=issues_by_severity,
            run_description=run_description,
            tags=tags + ["auto-hook"],
        )
        return {
            "status": "success",
            "records_created": len(records),
            "hook": "auto_completion_friction",
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "hook": "auto_completion_friction",
        }


if __name__ == "__main__":
    # When TUI directly invokes this (pre/post_tool_use registration in global/settings.local),
    # just succeed. The handle() does the work when called via runner with proper context.
    import sys
    sys.exit(0)
