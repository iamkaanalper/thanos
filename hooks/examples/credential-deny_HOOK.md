# credential-deny Hook Adapter (Grok)

Core PreToolUse security guard. See on_pre_tool_use_HOOK.md for full contract + how TUI invokes it directly.

Implements secret pattern + entropy detection. Returns decision "allow" or "warn" (with reason). Never blocks the user session (fail-open on its own errors).

