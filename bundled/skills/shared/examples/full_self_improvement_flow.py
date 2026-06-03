"""
Full Self-Improvement Flow Example (2026-06)

Demonstrates the modern stack working together:

- Task Lifecycle Ledger (for bounded loops)
- Friction + Completion helpers
- Compound Bridge (high-level entry point)
- Hook system (automatic behaviors)

Run this file to see how a realistic implement/review/verifier flow now automatically
feeds the self-improvement system.
"""

from pathlib import Path
import sys

# Make sure we can import from shared
sys.path.insert(0, str(Path(__file__).parent.parent))

from task_lifecycle import TaskLifecycleLedger, make_devqa_handoff_context
from compound_bridge import feed_run_to_compound


def simulate_realistic_run():
    print("=== Simulating a realistic implement + review + verifier flow ===\n")

    # 1. Bounded loop with ledger (as done in real implement/execute-plan)
    ledger = TaskLifecycleLedger(session_id="example-project")
    state = ledger.start_or_resume(
        "feature-auth-v2",
        "Add proper auth with rate limiting",
        max_attempts=3
    )

    print(f"Started bounded loop for task: {state.task_id}")
    print(f"Current attempt: {state.attempt}\n")

    # Simulate 2 rounds of issues (like real review rounds)
    for round_num in range(1, 3):
        print(f"--- Round {round_num} ---")

        # Get context for subagents (as real orchestrators do)
        ctx = make_devqa_handoff_context(ledger, "feature-auth-v2")
        print(f"Injected ledger context to prompts: attempt={ctx.get('attempt')}\n")

        # Simulate reviewer finding issues
        issues = [f"missing rate limit test in round {round_num}"]
        feedback = f"Round {round_num} issues found."

        state = ledger.record_attempt("feature-auth-v2", feedback=feedback, issues=issues)
        print(f"Recorded round. New attempt count: {state.attempt}\n")

    # 2. Final verification + self-improvement (the new modern way)
    print("=== Final Verification + Automatic Self-Improvement ===\n")

    final_patterns = [
        "Missing rate limiting tests on auth endpoints",
        "No rollback path documented for auth migration",
    ]
    final_severity = {"bug": 1, "suggestion": 2, "nit": 3}

    # This one call does:
    # - Records friction properly
    # - Fires all registered hooks (auto tagger, verifier friction, etc.)
    # - Can be extended to trigger analyzer
    result = feed_run_to_compound(
        session_context="implement run: feature-auth-v2",
        issue_patterns=final_patterns,
        issues_by_severity=final_severity,
        run_description="Add proper auth with rate limiting",
        tags=["implement", "auth"],
    )

    print("Self-improvement result:")
    print(result)
    print("\n=== Flow complete. All modern primitives worked together. ===")


if __name__ == "__main__":
    simulate_realistic_run()
