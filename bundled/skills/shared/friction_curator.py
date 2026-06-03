"""
Friction Curator — Governance & long-term health of the compound-friction.jsonl ledger.

Real executable implementation for the friction-curator skill.

Responsibilities (Production Contract):
- Curate high-frequency / high-impact patterns into actionable Pre-Flight suggestions
- Deduplicate noise
- Promote valuable patterns toward rules / new checklist items
- Designed to be called by on_friction_recorded and end-of-run hooks
- Feeds directly into preflight skill and compound-learnings drafts
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .friction import DEFAULT_FRICTION_PATH, record_friction

try:
    from grok.hooks.core.hook_runner import run_hook, _HOOK_REGISTRY
except Exception:
    run_hook = None
    _HOOK_REGISTRY = {}


def curate_high_impact_patterns(
    ledger_path: Optional[Path] = None,
    min_occurrences: int = 3,
    top_n: int = 15,
) -> List[Dict[str, Any]]:
    """
    Scan the friction ledger and return the highest-signal patterns that should become
    permanent Pre-Flight checklist items or new rules.

    Returns list of {pattern, count, categories, suggested_action, ...}
    """
    path = Path(ledger_path) if ledger_path else DEFAULT_FRICTION_PATH
    if not path.exists():
        return []

    pattern_stats: Dict[str, Dict[str, Any]] = {}

    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if rec.get("type") != "FRICTION":
                        continue

                    pat = rec.get("pattern") or rec.get("description")
                    if not pat:
                        continue

                    if pat not in pattern_stats:
                        pattern_stats[pat] = {
                            "pattern": pat,
                            "count": 0,
                            "categories": set(),
                            "impacts": Counter(),
                            "last_seen": None,
                        }

                    stats = pattern_stats[pat]
                    stats["count"] += 1
                    if rec.get("category"):
                        stats["categories"].add(rec["category"])
                    stats["impacts"][rec.get("friction_impact", "Low")] += 1
                    stats["last_seen"] = rec.get("timestamp")
                except Exception:
                    continue
    except Exception:
        return []

    # Filter + rank
    curated = []
    for pat, stats in pattern_stats.items():
        if stats["count"] < min_occurrences:
            continue
        high_medium = stats["impacts"].get("High", 0) + stats["impacts"].get("Medium", 0)
        if high_medium == 0:
            continue

        suggested = "Add to Pre-Flight checklist and agent persona constraints"
        if "Security" in stats["categories"]:
            suggested = "Mandatory security-reviewer reviewer + input validation rule"
        elif "Testing" in stats["categories"]:
            suggested = "Enforce test coverage in TDD skill + verifier"

        curated.append({
            "pattern": pat,
            "count": stats["count"],
            "categories": sorted(stats["categories"]),
            "high_medium_count": high_medium,
            "suggested_action": suggested,
            "last_seen": stats["last_seen"],
        })

    # Sort by (high+medium count desc, total count desc)
    curated.sort(key=lambda x: (-x["high_medium_count"], -x["count"]))
    return curated[:top_n]


def run_friction_curation(
    also_fire_hook: bool = True,
    min_occurrences: int = 3,
) -> Dict[str, Any]:
    """
    Full curation pass. Intended to be called at end of large runs or via on_friction_recorded hook.

    Returns summary + list of new Pre-Flight candidates.
    Also records a FRICTION record if it discovers new high-value patterns that should be promoted.
    """
    candidates = curate_high_impact_patterns(min_occurrences=min_occurrences)

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "candidates_found": len(candidates),
        "candidates": candidates,
        "hook_fired": False,
    }

    if candidates:
        # Record one aggregate friction for the self-improvement flywheel
        record_friction(
            pattern="friction curator found repeatable high-impact patterns",
            category="Self-Improvement",
            description=f"{len(candidates)} patterns seen >= {min_occurrences} times with High/Medium impact — promote to permanent checks",
            friction_impact="High",
            recommended_fix_type="preflight + rule update",
        )

    if also_fire_hook and run_hook and "on_friction_recorded" in _HOOK_REGISTRY:
        try:
            run_hook("on_friction_recorded", curation_summary=summary)
            summary["hook_fired"] = True
        except Exception:
            pass

    return summary


def get_preflight_suggestions_from_curator() -> str:
    """
    Convenience: returns a ready-to-inject markdown block of the top curated suggestions.
    Used by preflight.py and orchestrators that want the curator view instead of raw recent patterns.
    """
    candidates = curate_high_impact_patterns(min_occurrences=2, top_n=8)
    if not candidates:
        return ""

    lines = [
        "## Curated Friction Patterns (from friction-curator)",
        "These patterns have repeated across runs. Strongly consider turning them into permanent Pre-Flight / persona rules.",
    ]
    for i, c in enumerate(candidates, 1):
        lines.append(f"{i}. **{c['pattern']}** (seen {c['count']}×, {c['high_medium_count']} high/medium) → {c['suggested_action']}")

    lines.append("")
    return "\n".join(lines)
