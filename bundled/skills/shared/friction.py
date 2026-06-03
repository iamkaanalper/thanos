"""
Friction Ledger Helper — Grok-native ergonomic writer for the compound learnings flywheel.

Makes it trivial for orchestrators and agents to record high-signal friction
without raw JSON appends or copy-paste hacks.

Location: .grok/bundled/skills/shared/friction.py
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

__all__ = [
    "record_friction",
    "get_high_impact_patterns",
    "DEFAULT_FRICTION_PATH",
]

DEFAULT_FRICTION_PATH = Path.home() / ".grok" / "compound-friction.jsonl"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def record_friction(
    pattern: str,
    category: str,
    description: str,
    friction_impact: str = "Medium",  # "High" | "Medium" | "Low"
    session_context: Optional[str] = None,
    evidence: str = "",
    recommended_fix_type: str = "",
    confidence: str = "medium",  # "high" | "medium" | "low"
    tags: Optional[List[str]] = None,
    ledger_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Append a structured friction record to the compound learnings ledger.

    This is the recommended way for Grok orchestrators and agents to feed
    the self-improvement flywheel.

    Returns the record that was written (for logging / handoff purposes).
    """
    path = Path(ledger_path) if ledger_path else DEFAULT_FRICTION_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    record: Dict[str, Any] = {
        "timestamp": _now_iso(),
        "type": "FRICTION",
        "pattern": pattern,
        "category": category,
        "description": description,
        "friction_impact": friction_impact,
        "confidence": confidence,
        "tags": tags or [],
    }

    if session_context:
        record["session_context"] = session_context
    if evidence:
        record["evidence"] = evidence
    if recommended_fix_type:
        record["recommended_fix_type"] = recommended_fix_type

    # Append atomically enough for our use case (single writer per session is common)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def get_high_impact_patterns(
    ledger_path: Optional[Path] = None,
    min_impact: str = "Medium",
) -> List[str]:
    """
    Read the friction ledger and return high/medium impact patterns.
    Used by orchestrators (implement, review, execute-plan) to build dynamic checklists.
    """
    path = Path(ledger_path) if ledger_path else DEFAULT_FRICTION_PATH
    if not path.exists():
        return []

    patterns: List[str] = []
    impact_levels = {"High", "Medium"} if min_impact == "Medium" else {"High"}

    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if rec.get("friction_impact") in impact_levels:
                        pat = rec.get("pattern") or rec.get("description")
                        if pat:
                            patterns.append(pat)
                except json.JSONDecodeError:
                    continue
    except Exception:
        return []

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for p in patterns:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


# Convenience for one-liners inside orchestrators
def record_friction_simple(pattern: str, category: str, impact: str = "Medium") -> None:
    """Ultra-simple version for quick calls from agents."""
    record_friction(
        pattern=pattern,
        category=category,
        description=pattern,
        friction_impact=impact,
    )
