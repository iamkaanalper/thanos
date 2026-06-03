"""
Minimal pilot example: Using Task Lifecycle Ledger with handoff templates
for a bounded Dev-QA loop.

This is the first concrete pilot usage of the ledger (Post-MVE Item 2 fix).

Run it to see how real attempt tracking + automatic escalation works.
"""

from pathlib import Path
import sys

# Add parent to path for this example
sys.path.insert(0, str(Path(__file__).parent.parent))

from task_lifecycle import TaskLifecycleLedger, make_devqa_handoff_context


def simulate_bounded_devqa_loop(task_id: str, objective: str, max_rounds: int = 3):
    """
    Simulates a real bounded Dev-QA loop using the ledger.
    In a real orchestrator this would call spawn_subagent with the injected context.
    """
    ledger = TaskLifecycleLedger(session_id="pilot-example")
    state = ledger.start_or_resume(task_id, objective, max_attempts=max_rounds)

    print(f"Starting bounded Dev-QA for: {objective}")
    print(f"Max rounds: {max_rounds}\n")

    for round_num in range(1, max_rounds + 1):
        print(f"=== Round {round_num} ===")

        # 1. Get real state to inject into prompts
        context = make_devqa_handoff_context(ledger, task_id)
        print(f"Injected context for prompt:\n{context}\n")

        # In real life: spawn implementer with the context injected
        # Then spawn reviewer...

        # 2. Simulate reviewer result
        if round_num < 3:
            feedback = f"Round {round_num} issues found. Fix them."
            issues = [f"issue-{round_num}"]
            print(f"Reviewer feedback: {feedback}\n")
            state = ledger.record_attempt(task_id, feedback=feedback, issues=issues)
        else:
            # Last round succeeds
            feedback = "All issues resolved."
            print(f"Reviewer feedback: {feedback}\n")
            state = ledger.record_attempt(task_id, feedback=feedback, issues=[])
            state = ledger.complete(task_id, summary="Task completed successfully after bounded reviews.")

        print(f"Current state: attempt={state.attempt}, status={state.status}\n")

        if state.status in ("completed", "escalated"):
            break

    print("=== Final History ===")
    history = ledger.get_full_history(task_id)
    for entry in history:
        print(entry)

    return history


if __name__ == "__main__":
    simulate_bounded_devqa_loop(
        task_id="pilot-handoff-ledger-001",
        objective="Add bounded Dev-QA loop support using the new ledger",
        max_rounds=3,
    )
