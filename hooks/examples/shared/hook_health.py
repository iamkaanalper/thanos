"""
Shared hook health reporting module (Grok port).
Logs hook executions to ~/.grok/hook-health.jsonl for monitoring, monster cross-training, etc.
Matches the interface used by auto_on_* and auto_* adapters: reportHealth(hook_name, mode='adapter')
"""

from pathlib import Path
import datetime
import json

def reportHealth(hook_name: str, mode: str = "adapter") -> None:
    """Record a health entry for a hook call. Non-fatal."""
    try:
        health_path = Path.home() / ".grok" / "hook-health.jsonl"
        entry = {
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "hook": hook_name,
            "mode": mode,
            "success": True,
        }
        health_path.parent.mkdir(parents=True, exist_ok=True)
        with open(health_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        # Never break the main flow
        pass

# Optional: wrapWithHealth if needed in future, for timing etc.
def wrapWithHealth(hook_name: str, mode: str = "adapter"):
    """Decorator/context for wrapping hook logic with health report. (stub for parity)"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                reportHealth(hook_name, mode)
                return result
            except Exception as e:
                # Could log failure, but for now just report attempt
                reportHealth(hook_name, mode)
                raise
        return wrapper
    return decorator
