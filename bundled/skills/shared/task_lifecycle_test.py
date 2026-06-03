"""
Basic tests for the TaskLifecycleLedger (TDD first pass).

Run with: python -m pytest .grok/bundled/skills/shared/task_lifecycle_test.py -q
or simply: python .grok/bundled/skills/shared/task_lifecycle_test.py
"""

import tempfile
import unittest
from pathlib import Path

from task_lifecycle import TaskLifecycleLedger


class TestTaskLifecycleLedger(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger_path = Path(self.tmp.name) / "test-ledger.jsonl"
        self.ledger = TaskLifecycleLedger(ledger_path=self.ledger_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_start_and_get_state(self):
        state = self.ledger.start_or_resume("task-1", "Fix the qa-loop race")
        self.assertEqual(state.task_id, "task-1")
        self.assertEqual(state.attempt, 0)
        self.assertEqual(state.status, "in_progress")

        loaded = self.ledger.get_state("task-1")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.objective, "Fix the qa-loop race")

    def test_record_attempts_and_escalation(self):
        self.ledger.start_or_resume("task-2", "Implement bounded retry with state", max_attempts=3)

        s1 = self.ledger.record_attempt("task-2", feedback="First round had type error", issues=["type error in ledger.py"])
        self.assertEqual(s1.attempt, 1)
        self.assertEqual(len(s1.accumulated_feedback), 1)
        self.assertEqual(s1.status, "in_progress")

        s2 = self.ledger.record_attempt("task-2", feedback="Second round still has race on concurrent writes")
        self.assertEqual(s2.attempt, 2)

        s3 = self.ledger.record_attempt("task-2", feedback="Third attempt also failed to acquire lock properly")
        self.assertEqual(s3.attempt, 3)
        self.assertEqual(s3.status, "escalated")  # auto-escalated because >= max_attempts

    def test_explicit_escalation(self):
        self.ledger.start_or_resume("task-3", "Something hard", max_attempts=5)
        self.ledger.record_attempt("task-3", feedback="First try")
        escalated = self.ledger.escalate("task-3", reason="Architecture needs revision", recommendation="decompose")
        self.assertEqual(escalated.status, "escalated")
        self.assertTrue(any(f.get("type") == "escalation" for f in escalated.accumulated_feedback))

    def test_history_is_append_only(self):
        self.ledger.start_or_resume("task-4", "Audit trail test")
        self.ledger.record_attempt("task-4", feedback="round 1")
        self.ledger.record_attempt("task-4", feedback="round 2")

        history = self.ledger.get_full_history("task-4")
        self.assertEqual(len(history), 3)  # start + 2 attempts
        self.assertEqual(history[-1]["attempt"], 2)

    def test_make_devqa_handoff_context(self):
        self.ledger.start_or_resume("task-5", "Test context helper")
        self.ledger.record_attempt("task-5", feedback="minor issue found", issues=["naming"])

        from task_lifecycle import make_devqa_handoff_context
        ctx = make_devqa_handoff_context(self.ledger, "task-5")
        self.assertIn("task_lifecycle", ctx)
        self.assertEqual(ctx["task_lifecycle"]["current_attempt"], 1)
        self.assertIn("Use the task_lifecycle data above", ctx["instruction"])


if __name__ == "__main__":
    unittest.main(verbosity=2)