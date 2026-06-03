# auto_impact_refactor.py
try:
    from .shared.hook_health import reportHealth
except ImportError:
    # Fallback for direct script execution (e.g. hook system running py file standalone)
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from shared.hook_health import reportHealth

def handle(data):
    reportHealth('impact-refactor', 'adapter')
    return {"status": "delegated"}



if __name__ == '__main__':
    try:
        import sys
        import json
        data = {}
        if not sys.stdin.isatty():
            raw = sys.stdin.read().strip()
            if raw:
                try:
                    data = json.loads(raw)
                except Exception:
                    data = {}
        handle(data)
    except Exception:
        pass
    import sys
    sys.exit(0)
