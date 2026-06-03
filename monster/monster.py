#!/usr/bin/env python3
"""
monster CLI — Grok-native Agent Cross-Training (the original Claude Code AI software team system (by @vibeeval) / Claude Code port, now part of Thanos on Grok)

One agent's mistake trains the whole team via error-ledger + skill-matrix + friction/compound.

Usage:
  python .grok/monster/monster.py report
  python .grok/monster/monster.py agent kraken
  python .grok/monster/monster.py errors --days 7
  python .grok/monster/monster.py weak --limit 5
  python .grok/monster/monster.py leaderboard --top 10

Integrates with:
- .grok/monster/error-ledger.jsonl
- .grok/monster/skill-matrix.json
- .grok/compound-friction.jsonl
- .grok/hook-health.jsonl
- compound-learnings + friction-curator + self-learner + auto_monster_broadcast hook

Run via: python .grok/monster/monster.py <cmd> ...
Or add to PATH: alias monster='python ~/.grok/monster/monster.py'
"""

from __future__ import annotations
import argparse
import json
import sys
from collections import defaultdict, Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

HOME = Path.home()
GROK = HOME / ".grok"
LEDGER = GROK / "monster" / "error-ledger.jsonl"
MATRIX = GROK / "monster" / "skill-matrix.json"
FRICTION = GROK / "compound-friction.jsonl"
HOOK_HEALTH = GROK / "hook-health.jsonl"

def _load_jsonl(path: Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    if limit:
        lines = lines[-limit:]
    out = []
    for line in lines:
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out

def _load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default or {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default or {}

def _save_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def cmd_report(args):
    """Genel durum raporu."""
    matrix = _load_json(MATRIX, {"agents": {}})
    ledger = _load_jsonl(LEDGER, limit=100)
    friction = _load_jsonl(FRICTION, limit=50)
    health = _load_jsonl(HOOK_HEALTH, limit=20)

    agents = matrix.get("agents", {})
    total_agents = len(agents)
    avg_success = sum(a.get("success_rate", 0) for a in agents.values()) / max(1, total_agents)
    total_errors = len(ledger)
    recent_errors = [e for e in ledger if "2026-06" in e.get("timestamp", "")]  # recent

    # Weak agents
    weak = sorted(
        [(name, a.get("success_rate", 0), a.get("error_count", 0)) for name, a in agents.items()],
        key=lambda x: (x[1], -x[2])
    )[:5]

    print("=== monster Cross-Training Report ===")
    print(f"Agents tracked: {total_agents}")
    print(f"Avg success rate: {avg_success:.1f}%")
    print(f"Total errors in ledger: {total_errors}")
    print(f"Recent errors (sample): {len(recent_errors)}")
    print("\nTop weak agents (lowest success + errors):")
    for name, rate, errs in weak:
        print(f"  - {name}: success={rate}% errors={errs}")

    print("\nRecent friction signals (cross-train related):")
    ct = [f for f in friction if "monster" in str(f.get("tags", "")).lower() or "cross" in str(f.get("category", "")).lower()]
    for f in ct[-3:]:
        print(f"  - {f.get('pattern', f.get('description', ''))[:80]}")

    print("\nHook health (recent broadcasts):")
    monster_hooks = [h for h in health if "monster" in str(h).lower()]
    print(f"  Recent monster broadcasts: {len(monster_hooks)}")

    print("\n(Full data in .grok/monster/ + compound-friction.jsonl)")

def cmd_agent(args):
    """Agent detay raporu."""
    name = args.agent
    matrix = _load_json(MATRIX, {"agents": {}})
    ledger = _load_jsonl(LEDGER)

    agent_data = matrix.get("agents", {}).get(name, {})
    if not agent_data:
        print(f"No data for agent '{name}'. Seeded agents or errors not yet recorded.")
        return

    print(f"=== monster: {name} ===")
    print(f"Success rate: {agent_data.get('success_rate')}%")
    print(f"Error count: {agent_data.get('error_count')}")
    print(f"Lessons learned: {agent_data.get('lessons_learned')}")
    print(f"Avg evolution score: {agent_data.get('avg_evolution_score')}")
    print(f"Tags: {agent_data.get('tags', [])}")
    print(f"Last error: {agent_data.get('last_error')}")

    agent_errors = [e for e in ledger if e.get("agent") == name]
    print(f"\nErrors for this agent ({len(agent_errors)}):")
    for e in agent_errors[-5:]:
        print(f"  - {e.get('timestamp')}: {e.get('error_type')} | {e.get('lesson', '')[:60]}")

    print("\n(Use compound-learnings or friction-curator for deeper patterns)")

def cmd_errors(args):
    """Son N gün hataları."""
    days = args.days
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    ledger = _load_jsonl(LEDGER)

    recent = [e for e in ledger if e.get("timestamp", "") >= cutoff]
    print(f"=== monster Errors (last {days} days) ===")
    print(f"Total: {len(recent)}")
    by_agent = Counter(e.get("agent", "unknown") for e in recent)
    print("By agent:")
    for ag, cnt in by_agent.most_common(10):
        print(f"  {ag}: {cnt}")

    print("\nRecent entries:")
    for e in recent[-10:]:
        print(f"  {e.get('timestamp')[:19]} | {e.get('agent')} | {e.get('error_type')} | {e.get('lesson', '')[:50]}")

def cmd_weak(args):
    """En zayıf agent'lar."""
    limit = args.limit
    matrix = _load_json(MATRIX, {"agents": {}})
    agents = matrix.get("agents", {})

    scored = []
    for name, d in agents.items():
        score = d.get("success_rate", 0) - (d.get("error_count", 0) * 2)  # penalize errors
        scored.append((name, score, d.get("success_rate"), d.get("error_count"), d.get("lessons_learned")))

    scored.sort(key=lambda x: x[1])
    print(f"=== monster Weak Agents (lowest score, top {limit}) ===")
    for name, sc, rate, errs, less in scored[:limit]:
        print(f"  {name}: score={sc:.0f} success={rate}% errors={errs} lessons={less}")

def cmd_leaderboard(args):
    """Başarı sıralaması."""
    top = args.top
    matrix = _load_json(MATRIX, {"agents": {}})
    agents = matrix.get("agents", {})

    scored = [(name, d.get("avg_evolution_score", 0), d.get("success_rate", 0)) for name, d in agents.items()]
    scored.sort(key=lambda x: -x[1])

    print(f"=== monster Leaderboard (top {top} by evolution score) ===")
    for i, (name, evo, succ) in enumerate(scored[:top], 1):
        print(f"  {i}. {name}: evolution={evo} success={succ}%")

def main():
    p = argparse.ArgumentParser(description="monster - Agent Cross-Training CLI (Grok)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("report", help="Genel durum").set_defaults(func=cmd_report)

    pa = sub.add_parser("agent", help="Agent detay")
    pa.add_argument("agent", help="Agent adı (örn: kraken)")
    pa.set_defaults(func=cmd_agent)

    pe = sub.add_parser("errors", help="Son N gün hataları")
    pe.add_argument("--days", type=int, default=7)
    pe.set_defaults(func=cmd_errors)

    pw = sub.add_parser("weak", help="En zayıf agent'lar")
    pw.add_argument("--limit", type=int, default=5)
    pw.set_defaults(func=cmd_weak)

    pl = sub.add_parser("leaderboard", help="Başarı sıralaması")
    pl.add_argument("--top", type=int, default=10)
    pl.set_defaults(func=cmd_leaderboard)

    args = p.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()