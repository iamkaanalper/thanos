"""
Task Lifecycle Ledger — Grok-native minimal state machine for multi-round Dev-QA loops.

Addresses the root cause discovered in Post-MVE Item 2:
- The 3-retry + cumulative feedback + escalation logic lived only in prompt text (handoff templates).
- No executable, versioned, queryable state → races across subagents/hooks.

This module provides a lightweight, JSONL-backed ledger that can be used by:
- The handoff skill
- implement / review / sleuth orchestrators
- Any long-running swarm or /swarm-lite flow

Design constraints (strict):
- Zero external dependencies (stdlib only)
- Works with worktree isolation
- Simple atomic-ish transitions (best-effort on Windows, strong on Unix with rename)
- Human + agent readable (the JSONL is the source of truth + audit log)
- Easy to adopt incrementally (the text handoff templates remain the primary UX)

Usage example (inside an orchestrator):
    from .task_lifecycle import TaskLifecycleLedger

    ledger = TaskLifecycleLedger(session_id="...")
    state = ledger.start_or_resume(task_id="fix-qa-race-42", objective="...")

    # On each QA round
    ledger.record_attempt(state.task_id, feedback="...", issues=["..."])
    if state.attempt >= 3:
        ledger.escalate(...)

The handoff templates (SKILL.md) should reference the ledger state when doing bounded loops.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

__all__ = [
    "TaskState",
    "TaskLifecycleLedger",
    "make_devqa_handoff_context",
    "DEFAULT_LEDGER_DIR",
]

DEFAULT_LEDGER_DIR = Path.home() / ".grok" / "task-ledgers"


@dataclass
class TaskState:
    task_id: str
    objective: str
    attempt: int = 0
    max_attempts: int = 3
    status: str = "in_progress"  # in_progress | escalated | completed | deferred
    accumulated_feedback: List[Dict[str, Any]] = field(default_factory=list)
    correlation_id: Optional[str] = None
    version: int = 1
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TaskState":
        return cls(**d)


class TaskLifecycleLedger:
    """
    Minimal ledger for tracking Dev-QA / multi-agent task rounds with real state.

    Backed by a single JSONL file per ledger (append-only for auditability).
    Latest state for a task_id is the last record with that id.
    """

    def __init__(
        self,
        ledger_path: Optional[Path] = None,
        session_id: Optional[str] = None,
        lock_timeout: float = 5.0,
    ):
        if ledger_path is None:
            ledger_dir = DEFAULT_LEDGER_DIR
            ledger_dir.mkdir(parents=True, exist_ok=True)
            session = session_id or "default"
            ledger_path = ledger_dir / f"{session}.jsonl"
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock_path = self.ledger_path.with_suffix(".lock")
        self.lock_timeout = lock_timeout

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _read_all(self) -> List[Dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        records: List[Dict[str, Any]] = []
        with self.ledger_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return records

    def _write_record(self, record: Dict[str, Any]) -> None:
        """Append-only write with simple advisory lock."""
        self._acquire_lock()
        try:
            with self.ledger_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        finally:
            self._release_lock()

    def _acquire_lock(self) -> None:
        start = time.time()
        while time.time() - start < self.lock_timeout:
            try:
                # Simple exclusive creation
                fd = os.open(self._lock_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                os.close(fd)
                return
            except FileExistsError:
                time.sleep(0.05)
        raise TimeoutError(f"Could not acquire ledger lock for {self.ledger_path}")

    def _release_lock(self) -> None:
        try:
            self._lock_path.unlink(missing_ok=True)
        except Exception:
            pass

    # --- Public API ---

    def start_or_resume(self, task_id: str, objective: str, max_attempts: int = 3) -> TaskState:
        """Idempotent: returns existing state or creates a new one at attempt 0."""
        existing = self.get_state(task_id)
        if existing:
            return existing

        state = TaskState(
            task_id=task_id,
            objective=objective,
            attempt=0,
            max_attempts=max_attempts,
            created_at=self._now(),
            updated_at=self._now(),
        )
        self._write_record(state.to_dict())
        return state

    def get_state(self, task_id: str) -> Optional[TaskState]:
        records = self._read_all()
        for rec in reversed(records):
            if rec.get("task_id") == task_id:
                return TaskState.from_dict(rec)
        return None

    def record_attempt(
        self,
        task_id: str,
        feedback: str,
        issues: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TaskState:
        """
        Records the result of one QA/implementation round.
        Increments attempt and appends to accumulated_feedback.
        """
        state = self.get_state(task_id)
        if not state:
            raise ValueError(f"No task with id {task_id}. Call start_or_resume first.")

        state.attempt += 1
        state.accumulated_feedback.append(
            {
                "attempt": state.attempt,
                "timestamp": self._now(),
                "feedback": feedback,
                "issues": issues or [],
                "metadata": metadata or {},
            }
        )
        state.updated_at = self._now()
        state.version += 1

        if state.attempt >= state.max_attempts and state.status == "in_progress":
            state.status = "escalated"

        self._write_record(state.to_dict())
        return state

    def escalate(self, task_id: str, reason: str, recommendation: str) -> TaskState:
        """Explicit escalation (even before max_attempts if needed)."""
        state = self.get_state(task_id)
        if not state:
            raise ValueError(f"No task with id {task_id}")

        state.status = "escalated"
        state.accumulated_feedback.append(
            {
                "attempt": state.attempt,
                "timestamp": self._now(),
                "type": "escalation",
                "reason": reason,
                "recommendation": recommendation,
            }
        )
        state.updated_at = self._now()
        state.version += 1
        self._write_record(state.to_dict())
        return state

    def complete(self, task_id: str, summary: str) -> TaskState:
        state = self.get_state(task_id)
        if not state:
            raise ValueError(f"No task with id {task_id}")

        state.status = "completed"
        state.accumulated_feedback.append(
            {"attempt": state.attempt, "timestamp": self._now(), "type": "completion", "summary": summary}
        )
        state.updated_at = self._now()
        state.version += 1
        self._write_record(state.to_dict())
        return state

    def get_full_history(self, task_id: str) -> List[Dict[str, Any]]:
        """Returns the complete append-only history for a task (great for prompts)."""
        records = self._read_all()
        return [r for r in records if r.get("task_id") == task_id]


# Convenience helper for orchestrators that already use spawn_subagent + handoff templates
def make_devqa_handoff_context(ledger: TaskLifecycleLedger, task_id: str) -> Dict[str, Any]:
    """
    Produces a small dict you can inject into a subagent prompt when doing bounded Dev-QA.
    This makes the "deneme N/3 + birikimli feedback" actually driven by real state.
    """
    state = ledger.get_state(task_id)
    if not state:
        return {}

    return {
        "task_lifecycle": {
            "task_id": state.task_id,
            "current_attempt": state.attempt,
            "max_attempts": state.max_attempts,
            "status": state.status,
            "accumulated_feedback": state.accumulated_feedback,
            "version": state.version,
        },
        "instruction": "Use the task_lifecycle data above as the single source of truth for attempt count and previous feedback. Do not invent rounds.",
    }