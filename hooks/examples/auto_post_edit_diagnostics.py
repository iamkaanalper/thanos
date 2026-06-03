# auto_post_edit_diagnostics.py

import json
import sys
from pathlib import Path

try:

    from .shared.hook_health import reportHealth

except ImportError:

    # Fallback for direct script execution (e.g. hook system running py file standalone)

    sys.path.insert(0, str(Path(__file__).resolve().parent))

    from shared.hook_health import reportHealth



def handle(data):

    reportHealth('post-edit-diagnostics', 'adapter')

    return {"status": "delegated"}


if __name__ == '__main__':
    # Full power for post_tool_use: read payload, call handle (which does the report and logic)
    try:
        data = {}
        if not sys.stdin.isatty():
            raw = sys.stdin.read().strip()
            if raw:
                try:
                    data = json.loads(raw)
                except Exception:
                    data = {}
        handle(data)
        sys.exit(0)
    except Exception:
        sys.exit(0)
