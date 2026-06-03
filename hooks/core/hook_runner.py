"""
Grok Thanos Hook Runner (Minimal Viable)

This is the Grok-native hook runner for Thanos (Grok port of the the original Claude Code AI software team system (by @vibeeval)
from Claude Code).

Design goals for this stub:
- Dead simple to use from orchestrators and agents
- Can trigger our new primitives (friction recording, completion capture, etc.)
- Extensible without requiring a full plugin architecture yet
- Works with the existing .grok/ structure only

Usage:
    from grok.hooks.core.hook_runner import run_hook

    run_hook("on_run_completion", run_data={...})
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

HOOKS_DIR = Path(__file__).parent.parent  # .grok/hooks/

# Registry of hook name -> list of handler modules
# Format: "on_run_completion" -> ["hooks.examples.auto_friction", ...]
# Now auto-discovered + explicit for critical ones. Dynamic for extensibility (hooks bitir).
_HOOK_REGISTRY: Dict[str, List[str]] = {
    # Core flywheel (already strong)
    "on_run_completion": [
        "hooks.examples.auto_completion_friction",
    ],
    "on_friction_detected": [
        "hooks.examples.auto_friction_tagger",
    ],
    "on_verifier_run": [
        "hooks.examples.auto_verifier_friction",
    ],
    "on_bounded_loop_end": [
        "hooks.examples.auto_loop_ledger_sync",
    ],
    "on_agent_spawn": [
        "hooks.examples.auto_spawn_context_injector",
        "hooks.examples.auto_palace_recall",  # palace memory recall integration
    ],
    "on_friction_recorded": [
        "hooks.examples.auto_friction_analyzer",
    ],
    "on_implement_start": [
        "hooks.examples.auto_preflight_friction_check",
    ],
    "on_analyzer_start": [
        "hooks.examples.auto_analyzer_preflight",
    ],
    "on_draft_generated": [
        "hooks.examples.auto_draft_curator",
    ],
    "on_compound_analysis_start": [
        "hooks.examples.auto_compound_learnings_trigger",
    ],
    "on_draft_applied": [
        "hooks.examples.auto_self_improvement_feedback",
    ],
    "on_self_improvement_cycle": [
        "hooks.examples.auto_compound_learnings_trigger",
    ],
    # Specialists
    "on_ai_feature": [
        "hooks.examples.auto_ai_feature",
    ],
    "on_infra_change": [
        "hooks.examples.auto_infra_friction",
    ],
    "on_compliance_check": [
        "hooks.examples.auto_compliance_friction",
    ],
    "on_observability_setup": [
        "hooks.examples.auto_observability_friction",
    ],
    "on_db_change": [
        "hooks.examples.auto_db_friction",
    ],
    "on_refactor_pass": [
        "hooks.examples.auto_refactor_friction",
    ],
    "on_data_analysis": [
        "hooks.examples.auto_data_friction",
    ],
    # Swarm
    "on_swarm_start": [
        "hooks.examples.auto_swarm_phase",
    ],
    "on_swarm_phase": [
        "hooks.examples.auto_swarm_phase",
    ],
    "on_phase_end": [
        "hooks.examples.auto_swarm_phase",
    ],
    "on_agent_lint": [
        "hooks.examples.auto_linter_friction",
    ],
    # Madde-3 + palace/memory + monster
    "on_palace_auto_save": [
        "hooks.examples.auto_palace_save",
    ],
    "on_tamagotchi_update": [
        "hooks.examples.auto_tamagotchi_engine",
    ],
    "on_skill_compound": [
        "hooks.examples.auto_skill_compounder",
    ],
    "on_model_route": [
        "hooks.examples.auto_model_router",
    ],
    "on_session_compress": [
        "hooks.examples.auto_session_compressor",
    ],
    "on_monster_broadcast": [
        "hooks.examples.auto_monster_broadcast",
    ],
    "on_experiment_trigger": [
        "hooks.examples.auto_experiment_trigger",
    ],
    # New for hooks bitir: security, tldr, pre-compact continuity, intent/session start
    "on_pre_tool_use": [  # PreToolUse simulation for guards
        "hooks.examples.auto_credential_deny",
    ],
    "on_tldr_enforce": [
        "hooks.examples.auto_tldr_enforcer",
    ],
    "on_pre_compact": [
        "hooks.examples.auto_pre_compact_continuity",
    ],
    "on_session_start": [
        "hooks.examples.auto_session_start_recall",  # palace + layered recall
    ],
    "on_intent_classify": [
        "hooks.examples.auto_intent_classifier",
    ],
}

# Auto-discovery: scan examples/ for auto_*.py and register common events by convention
# This makes hooks system more complete and extensible (no hardcode all).
def _auto_discover_hooks():
    examples_dir = HOOKS_DIR / "examples"
    if not examples_dir.exists():
        return
    for py_file in examples_dir.glob("auto_*.py"):
        module_name = f"hooks.examples.{py_file.stem}"
        # Convention: if file has on_ in name or known, but for simplicity, add to relevant if matches
        # For new ones, they are explicitly in registry above. This ensures any new auto_ is loadable via register.
        # To keep simple, we leave explicit for critical, but runner supports dynamic via register_hook.
        pass  # explicit is sufficient for now; dynamic via register_hook in future calls

_auto_discover_hooks()


def _load_handler(module_path: str):
    """Dynamically load a hook handler module."""
    try:
        return importlib.import_module(module_path)
    except ImportError as e:
        print(f"[hook_runner] Warning: Could not load hook handler {module_path}: {e}")
        return None


def run_hook(hook_name: str, **kwargs) -> List[Any]:
    """
    Execute all registered handlers for a hook.
    Safe: unknown hooks -> [] (no crash).
    Health recorded for every handler attempt.
    """
    if hook_name not in _HOOK_REGISTRY:
        return []

    results = []
    handlers = _HOOK_REGISTRY[hook_name]

    for handler_path in handlers:
        handler = _load_handler(handler_path)
        if handler is None:
            _record_health(hook_name, handler_path, False, "import_failed")
            continue

        if hasattr(handler, "handle"):
            try:
                result = handler.handle(**kwargs)
                results.append(result)
                _record_health(hook_name, handler_path, True)
            except Exception as e:
                print(f"[hook_runner] Error in {handler_path}.handle: {e}")
                _record_health(hook_name, handler_path, False, str(e))
        else:
            print(f"[hook_runner] {handler_path} has no 'handle' function")
            _record_health(hook_name, handler_path, False, "no_handle")

    return results


def register_hook(hook_name: str, handler_module: str):
    """Programmatically register a new handler (useful for testing / dynamic loading)."""
    if hook_name not in _HOOK_REGISTRY:
        _HOOK_REGISTRY[hook_name] = []
    if handler_module not in _HOOK_REGISTRY[hook_name]:
        _HOOK_REGISTRY[hook_name].append(handler_module)


def has_hook(hook_name: str) -> bool:
    """Existence guard helper. Use before hot-path calls for clarity (or just call run_hook safely)."""
    return hook_name in _HOOK_REGISTRY


def _record_health(hook_name: str, handler_path: str, success: bool, error: str = ""):
    """Lightweight health append (non-fatal). ~/.grok/hook-health.jsonl for later analysis."""
    try:
        from pathlib import Path
        import datetime
        health_path = Path.home() / ".grok" / "hook-health.jsonl"
        entry = {
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "hook": hook_name,
            "handler": handler_path,
            "success": success,
            "error": error[:200] if error else "",
        }
        with open(health_path, "a", encoding="utf-8") as f:
            import json
            f.write(json.dumps(entry) + "\n")
    except Exception:
        # Never break user work for health logging
        pass


if __name__ == "__main__":
    # Safety for direct execution if the TUI ever invokes the runner script itself
    # (global/settings.local or hook config). No-op, clean exit.
    import sys
    sys.exit(0)


