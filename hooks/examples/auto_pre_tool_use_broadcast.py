# auto_pre_tool_use_broadcast.py
import sys
import json
from pathlib import Path

try:
    from .shared.hook_health import reportHealth
except ImportError:
    # Fallback for direct script execution (e.g. hook system running py file standalone)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from shared.hook_health import reportHealth

def handle(data):
    reportHealth('pre-tool-use-broadcast', 'adapter')
    return {"status": "delegated"}


# Direct execution support for TUI PreToolUse broadcast (same contract).
# Always emit safe allow decision. Broadcast adapters must not block or pollute stdout.
if __name__ == "__main__":
    try:
        data = {}
        if not sys.stdin.isatty():
            raw = sys.stdin.read().strip()
            if raw:
                try:
                    data = json.loads(raw)
                except Exception:
                    data = {}
        # Execute the handle to run full logic (reportHealth etc) for full power
        handle(data)
        # Silent for broadcast/adapter pre hooks
        sys.exit(0)
    except Exception:
        sys.exit(0)

