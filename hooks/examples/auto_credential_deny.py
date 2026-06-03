"""
Hook Handler: auto_credential_deny (PreToolUse guard simulation)

High-leverage security hook port.
Blocks or warns on potential credential exposure in tool calls, prompts, or file reads.
Grok adaptation: Python based, uses simple regex + entropy for secrets.
Integrates with preflight, security-review, on_pre_tool_use.

Usage in runner: registered under "on_pre_tool_use".
"""

from typing import Any, Dict
import re
import os
import sys
import json

# Simple patterns for common secrets (expandable)
SECRET_PATTERNS = [
    r"(?i)(api[_-]?key|secret|token|password|passwd|private[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{8,}",
    r"sk-[A-Za-z0-9]{20,}",  # OpenAI style
    r"ghp_[A-Za-z0-9]{20,}",  # GitHub
    r"AKIA[0-9A-Z]{16}",  # AWS
]

def _looks_like_secret(text: str) -> bool:
    if not text or len(text) < 8:
        return False
    for pat in SECRET_PATTERNS:
        if re.search(pat, text):
            return True
    # Entropy check for high-entropy strings (basic)
    if len(text) > 16:
        unique = len(set(text))
        if unique / len(text) > 0.7:
            return True
    return False

def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs:
        tool_name: str (e.g. read_file, run_terminal)
        args: dict or str (the input being passed)
        context: str (prompt or previous)
    Returns: {"decision": "allow" | "deny" | "warn", "reason": "..."}
    """
    tool_name = kwargs.get("tool_name", "")
    args = kwargs.get("args", "") or kwargs.get("context", "")
    if isinstance(args, dict):
        args = " ".join(str(v) for v in args.values())

    text_to_check = f"{tool_name} {args}"

    if _looks_like_secret(text_to_check):
        # Match original Claude credential-deny: output decision 'block' to prevent the tool
        return {
            "decision": "block",
            "reason": "ENGELLENDI: Potential credential/secret detected in tool input. Guvenlik kurali.",
            "hook": "auto_credential_deny",
            "tool": tool_name,
        }
    return {
        "decision": "allow",
        "hook": "auto_credential_deny",
    }


# =============================================================================
# Direct execution entrypoint for Grok TUI/CLI PreToolUse enforcement.
# The TUI spawns `python .../auto_credential_deny.py` as a subprocess for every
# tool call (read_file, run_terminal_command, etc.), feeds tool context as JSON
# on stdin, and expects:
#   - ONLY a compact decision JSON object on stdout (no extra text, no logs)
#   - sys.exit(0) on normal completion (even for "warn"/"deny")
# Any extra stdout, traceback to stdout, or non-zero exit → "failed with exit code 1"
# visible to user on every operation.
#
# Internal orchestrators use the handle(**kwargs) via hook_runner.run_hook().
# This __main__ makes the direct-subprocess contract work.
# =============================================================================

def _normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Map common PreToolUse payload shapes to what handle() expects."""
    tool_name = (
        payload.get("tool_name")
        or payload.get("tool")
        or payload.get("name")
        or ""
    )
    # tool_input / args / input are common variants
    raw_args = payload.get("tool_input") or payload.get("args") or payload.get("input") or payload.get("context") or ""
    if isinstance(raw_args, dict):
        args = raw_args
    else:
        args = {"value": str(raw_args) if raw_args else ""}
    context = payload.get("context") or payload.get("prompt") or ""
    return {"tool_name": tool_name, "args": args, "context": context}


if __name__ == "__main__":
    # This block ONLY runs on direct `python auto_credential_deny.py`
    # Never pollute stdout. All side logs to stderr or health file.
    decision = {"decision": "allow", "hook": "auto_credential_deny"}
    try:
        payload: Dict[str, Any] = {}
        # Read from stdin if the TUI piped JSON (non-tty or has data)
        if not sys.stdin.isatty():
            raw = sys.stdin.read().strip()
            if raw:
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    # Some invocations may send other formats; ignore and default allow
                    payload = {}

        normalized = _normalize_payload(payload)
        decision = handle(**normalized)

        # Guarantee required shape for TUI
        if not isinstance(decision, dict) or "decision" not in decision:
            decision = {"decision": "allow", "hook": "auto_credential_deny"}

        # Optional: record health (file only, never stdout)
        try:
            # Lazy import to keep top-level clean; use robust path for direct run
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from shared.hook_health import reportHealth  # type: ignore
            reportHealth("on_pre_tool_use:credential_deny", "direct")
        except Exception:
            pass  # health must never break the hook

        # CRITICAL: print ONLY the JSON, compact, single line, then flush
        print(json.dumps(decision, separators=(",", ":")), flush=True)
        sys.exit(0)

    except Exception as exc:
        # Fail-open: never make user's normal tool calls fail because the guard itself errored.
        # Emit a valid allow decision anyway. Details to stderr only.
        print(f"[auto_credential_deny] internal error (stderr only): {exc}", file=sys.stderr)
        fallback = {
            "decision": "allow",
            "hook": "auto_credential_deny",
            "reason": "Hook error - defaulted to allow to not block work",
        }
        print(json.dumps(fallback, separators=(",", ":")), flush=True)
        sys.exit(0)
