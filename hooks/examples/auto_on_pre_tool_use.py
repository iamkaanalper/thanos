# auto_on_pre_tool_use.py
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
    reportHealth('on_pre_tool_use', 'adapter')
    return {"status": "delegated"}


# Direct execution support for TUI PreToolUse (same contract as credential_deny).
# Always emit a safe decision JSON + exit 0. This is a no-op/delegated observer.
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
        # Execute the handle to run full adapter logic (e.g. reportHealth inside handle for full power)
        handle(data)
        # Silent for non-decision pre hooks (side effect / broadcast / adapter)
        sys.exit(0)
    except Exception:
        sys.exit(0)

