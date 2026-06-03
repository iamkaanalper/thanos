# on_pre_tool_use Hook Adapter (Grok)

**Primary implementation:** `auto_credential_deny.py` (registered in hook_runner for "on_pre_tool_use").

**Direct execution contract (TUI/CLI PreToolUse enforcement):**
- Invoked by the Grok TUI as `python <path-to-script.py>` (subprocess) before tool calls.
- Payload: JSON on stdin (typical keys: tool_name, tool_input/args, context).
- Output: **exactly one compact JSON line** to stdout: `{"decision":"allow"|"warn"|"deny", "reason":"...", "hook":"..."}`
- Must `sys.exit(0)` always on normal path (fail-open with allow JSON on internal errors).
- No extra text, no banners, no "RESULT:", no tracebacks on stdout. Use stderr or health file for diagnostics.
- Health: optional, via shared/hook_health (file append only).

**Internal path:** `hook_runner.run_hook("on_pre_tool_use", tool_name=..., args=...)` calls `handle(**kwargs)` and expects the same decision dict.

**See:** auto_credential_deny.py (full handle + guarded __main__), auto_on_pre_tool_use.py, auto_pre_tool_use_broadcast.py (observer variants that also comply).

**Test:** `echo '{"tool_name":"bash","tool_input":{"command":"..."}}' | python auto_credential_deny.py` must emit exactly the decision JSON and exit 0.

