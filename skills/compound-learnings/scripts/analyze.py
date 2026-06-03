#!/usr/bin/env python3
"""
compound-learnings analyzer (Grok v2 - improved)

Much stronger consolidation + high-quality, ready-to-use proposals.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from consolidation import ConsolidatedPattern, consolidate_issues, detect_meta_patterns

MEMORY_HELPER = Path.home() / ".grok" / "bundled" / "skills" / "implement" / "scripts" / "memory.py"


def run_memory_snapshot() -> dict[str, Any]:
    if not MEMORY_HELPER.exists():
        print(f"ERROR: memory helper not found at {MEMORY_HELPER}", file=sys.stderr)
        sys.exit(2)

    result = subprocess.run(
        [sys.executable, str(MEMORY_HELPER), "snapshot"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        print("ERROR: Failed to read memory snapshot", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON from memory snapshot: {e}", file=sys.stderr)
        sys.exit(1)


# ------------------------------------------------------------------
# High-quality proposal generation
# ------------------------------------------------------------------

def _build_rich_draft_content(pattern: ConsolidatedPattern) -> str:
    """Generate high-quality, Grok-specific draft content."""
    desc = pattern.description.lower()

    # === High-leverage Grok-specific patterns ===
    if "handoff" in desc:
        return (
            "- Make structured handoffs (from the `handoff` skill) mandatory for all non-trivial subagent launches\n"
            "- Update `implement` and `execute-plan` to require handoff templates at phase boundaries\n"
            "- Add validation step: orchestrator should refuse to proceed without a proper handoff artifact"
        )

    if "factcheck" in desc or "claim" in desc:
        return (
            "- Add 'Factcheck-Guard' as a hard non-negotiable constraint in implementer + reviewer personas\n"
            "- 'Never make claims about code behavior without having read the actual lines in this session'\n"
            "- Consider adding a lightweight pre-edit checklist in the implementer persona"
        )

    if "persona" in desc and ("inject" in desc or "missing" in desc):
        return (
            "- Strengthen persona injection logic in `implement` and `execute-plan`\n"
            "- Make bracketed role tags (`[implementer]`, `[reviewer]`) mandatory in spawn_subagent descriptions\n"
            "- Add automatic reminder in orchestrators when launching without proper persona context"
        )

    if "worktree" in desc:
        return (
            "- Make worktree isolation rules stricter in execute-plan\n"
            "- Document and enforce the Subagent Worktree Protocol more visibly\n"
            "- Add safety checks before any branch mutation in the orchestrator"
        )

    if "memory" in desc and ("not used" in desc or "bypassed" in desc):
        return (
            "- Make past_issues_briefing usage more prominent in implementer prompts\n"
            "- Consider failing loudly (or warning strongly) when memory system is available but ignored\n"
            "- Add memory usage as a positive signal in review"
        )

    # === Classic patterns (still improved) ===
    if "null/undefined" in desc or "missing null" in desc:
        return (
            "- Add explicit 'Always validate null/undefined on public boundaries' constraint to implementer persona\n"
            "- Prefer guard clauses + early returns\n"
            "- Recommend schema validation (zod/pydantic) for complex inputs\n"
            "- Never trust types alone for required runtime values"
        )

    if "input validation" in desc:
        return (
            "- Enforce input validation at every system boundary as a hard rule\n"
            "- Prefer allow-lists over deny-lists\n"
            "- Make this a standard part of the reviewer checklist (not just security-auditor)"
        )

    if "error handling" in desc:
        return (
            "- Add 'Never silently swallow exceptions in important paths' to implementer persona\n"
            "- Require logging full context before re-throwing or converting errors\n"
            "- Consider introducing a small Result type pattern for Grok codebases"
        )

    if "long function" in desc or "too complex" in desc:
        return (
            "- Add hard guideline: functions > 60 lines require justification in the Implementation Summary\n"
            "- Update implementer persona: 'Extract before you continue'\n"
            "- Reviewer should flag long functions even if they are correct"
        )

    if "hardcoded secret" in desc or "credential" in desc:
        return (
            "- Zero tolerance policy: any new hardcoded secret is an automatic 'bug' severity finding\n"
            "- Add startup secret validation helper that Grok projects should use\n"
            "- security-auditor persona should treat this as critical by default"
        )

    # Strong generic fallback with Grok flavor
    return (
        "- Document the expected behavior explicitly in the handoff or summary\n"
        "- Add a regression test that would have caught this class of issue\n"
        "- Evaluate whether this should become a persona constraint or rule in ~/.grok/rules/"
    )


def _classify_artifact(pattern: ConsolidatedPattern) -> str:
    desc = pattern.description.lower()

    if "null/undefined" in desc or "input validation" in desc:
        return "Rule + implementer Persona Update"
    if "error handling" in desc:
        return "Rule + implementer + reviewer Persona Update"
    if "long function" in desc or "too complex" in desc:
        return "Rule (coding standards) + implementer Persona"
    if "hardcoded secret" in desc or "credential" in desc:
        return "Security Rule + security-auditor Persona + implementer Persona"
    if "test" in desc or "coverage" in desc or "edge case" in desc:
        return "Testing Guideline + reviewer Persona emphasis"
    if "handoff" in desc:
        return "Rule + handoff skill emphasis + orchestrator guidance"
    if "factcheck" in desc or "claim" in desc:
        return "Strong Rule + all personas (especially implementer + reviewer)"
    if "persona" in desc and "inject" in desc:
        return "Persona Injection Rule + implement + execute-plan skills"
    return "Rule or Focused Guidance Doc"


def generate_proposals(
    consolidated: list[ConsolidatedPattern],
    recent_runs: list[dict[str, Any]],
    min_occurrences: int = 3
) -> list[dict[str, Any]]:
    """Turn consolidated patterns into rich, actionable proposals with advanced impact scoring."""
    proposals = []

    # Precompute some signals from recent_runs for better scoring
    friction_patterns = _extract_high_friction_patterns(recent_runs)
    security_involved_patterns = _extract_security_involved_patterns(recent_runs)

    for p in consolidated:
        if p.count < min_occurrences:
            continue

        impact = _compute_advanced_impact_score(p, friction_patterns, security_involved_patterns)

        proposal = {
            "pattern": p.description,
            "category": p.category,
            "occurrences": p.count,
            "confidence": "high" if p.count >= 5 else "medium",
            "impact": impact["level"],
            "priority_score": impact["priority_score"],
            "recommended_type": _classify_artifact(p),
            "examples": p.examples[:3],
            "rationale": _build_rationale(p),
            "draft_content": _build_rich_draft_content(p),
            "suggested_files": _suggest_files(p),
            "why_now": impact.get("why_now", ""),
        }
        proposals.append(proposal)

    # Sort by priority_score (higher = more urgent)
    proposals.sort(key=lambda x: -x["priority_score"])
    return proposals


def _extract_high_friction_patterns(recent_runs: list[dict]) -> set[str]:
    """
    Patterns that appeared in runs with high review rounds (friction indicator).
    Faz 2 iyileştirmesi: 3+ round artık "yüksek friction" olarak daha ağır değerlendiriliyor.
    Ayrıca "security" specialization'ı olan run'lardaki pattern'ler de ekstra friction sinyali sayılıyor.

    Not: Review skill'i tarafından tetiklenen hafif analiz çağrılarında (Faz 2 entegrasyonu),
    review sonuçlarından gelen friction pattern'leri de bu fonksiyon tarafından değerlendirilir.
    """
    high_friction = set()
    for run in recent_runs:
        rounds = run.get("rounds", 0)
        specializations = [s.lower() for s in run.get("specializations", [])]

        is_high_friction_run = False

        # 3+ round = güçlü friction sinyali
        if rounds >= 3:
            is_high_friction_run = True

        # Security'li run'larda 2+ round bile friction sayılabilir (güvenlikte friction daha tehlikeli)
        if "security" in specializations and rounds >= 2:
            is_high_friction_run = True

        if is_high_friction_run:
            for key in run.get("key_patterns", []):
                high_friction.add(key.lower())

    return high_friction


def _extract_security_involved_patterns(recent_runs: list[dict]) -> set[str]:
    """Patterns that appeared in runs where security-auditor was active."""
    security_patterns = set()
    for run in recent_runs:
        specializations = run.get("specializations", [])
        if "security" in [s.lower() for s in specializations]:
            for key in run.get("key_patterns", []):
                security_patterns.add(key.lower())
    return security_patterns


def _compute_advanced_impact_score(
    pattern: ConsolidatedPattern,
    friction_patterns: set[str],
    security_patterns: set[str]
) -> dict[str, Any]:
    """
    Advanced impact scoring that considers multiple signals:
    - Base risk of the pattern type
    - Frequency
    - Review friction (high rounds)
    - Security involvement
    - Recency (implicit via recent_runs data)
    """
    desc = pattern.description.lower()
    count = pattern.count

    base_score = 0
    reasons = []

    # Base risk from pattern content
    high_risk_keywords = [
        "secret", "credential", "auth", "injection", "factcheck", "handoff",
        "persona", "worktree", "memory", "null/undefined", "input validation"
    ]
    medium_risk_keywords = [
        "error handling", "long function", "complex", "test", "edge case"
    ]

    if any(kw in desc for kw in high_risk_keywords):
        base_score += 40
        reasons.append("High inherent risk area")
    elif any(kw in desc for kw in medium_risk_keywords):
        base_score += 20
    else:
        base_score += 10

    # Frequency weight
    freq_bonus = min(count * 3, 25)
    base_score += freq_bonus
    if count >= 6:
        reasons.append(f"Very frequent ({count} occurrences)")

    # Friction signal (patterns that caused many review rounds) — Faz 2 güçlendirmesi
    if any(pat in desc for pat in friction_patterns):
        bonus = 30
        if args.source == "review":
            bonus = 35  # Review kaynağından gelen friction daha kritik sayılır
        base_score += bonus
        reasons.append(f"Associated with high review friction (multiple rounds) — elevated in Faz 2 [source={args.source}]")

    # Faz 2 - 1: Ledger'daki önceki friction pattern'lerle eşleşme (gelişmiş versiyon)
    try:
        from pathlib import Path
        import json
        import re

        ledger_path = Path.home() / ".grok" / "compound-friction.jsonl"
        if ledger_path.exists():
            past_records = []  # (pattern, source, priority)
            with open(ledger_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        rec = json.loads(line.strip())
                        if rec.get("impact") in ("High", "Medium"):
                            past_records.append((
                                rec.get("pattern", "").lower(),
                                rec.get("source", "unknown"),
                                rec.get("priority", 0)
                            ))
                    except:
                        continue

            current_words = set(re.findall(r'\b\w{4,}\b', desc.lower()))
            best_match = None
            best_score = 0

            for past_pattern, src, prio in past_records:
                if not past_pattern:
                    continue

                past_words = set(re.findall(r'\b\w{4,}\b', past_pattern))
                common = current_words & past_words

                match_score = 0
                if len(common) >= 3:
                    match_score = 30
                elif len(common) == 2:
                    match_score = 22
                elif past_pattern in desc:
                    match_score = 18
                elif any(len(w) >= 6 and w in desc for w in past_words):
                    match_score = 15

                if match_score > best_score:
                    best_score = match_score
                    best_match = (past_pattern, src)

            if best_match and best_score >= 15:
                bonus = best_score
                if best_match[1] == "review":
                    bonus += 5  # Review kaynaklı friction daha kritik
                base_score += bonus
                reasons.append(
                    f"Matches previous high-friction pattern from ledger "
                    f"[{best_match[1]}]: '{best_match[0][:55]}...' (Faz 2 cross-training)"
                )
    except:
        pass  # Ledger okunamıyorsa sessizce devam et

    # Security signal
    if any(pat in desc for pat in security_patterns):
        base_score += 30
        reasons.append("Appeared in security-relevant runs")

    # Final level
    if base_score >= 70:
        level = "High"
    elif base_score >= 45:
        level = "Medium"
    else:
        level = "Low"

    priority = base_score

    why_now = ""
    if level == "High":
        why_now = "This pattern is causing real pain and risk. Addressing it will have outsized positive effect on future run quality."
    elif level == "Medium":
        why_now = "Recurring enough to be worth turning into permanent capability soon."

    return {
        "level": level,
        "priority_score": priority,
        "why_now": why_now or "Moderate recurring pattern worth tracking."
    }


def _build_rationale(p: ConsolidatedPattern) -> str:
    count = p.count
    base = f"Seen {count} times across recent runs. "

    desc = p.description.lower()
    if "null" in desc:
        base += "This is the #1 source of runtime bugs that reach review. Preventing it at the implementer level has extremely high ROI."
    elif "input validation" in desc:
        base += "Directly related to security and reliability. Almost always cheaper to catch at entry point than later."
    elif "error handling" in desc:
        base += "Poor error handling creates the worst debugging experiences and silent failures in production."
    elif "long function" in desc:
        base += "Long functions are the strongest predictor of future bugs and review friction in this codebase."
    else:
        base += "Recurring pattern that keeps surviving multiple review rounds."

    return base


def _suggest_files(p: ConsolidatedPattern) -> list[str]:
    desc = p.description.lower()
    files = []

    if "null" in desc or "input validation" in desc or "error handling" in desc:
        files.append("personas/implementer.md (add constraint)")
    if "long function" in desc:
        files.append("personas/implementer.md + coding standards guidance")
    if "secret" in desc or "credential" in desc:
        files.append("personas/security-auditor.md + personas/implementer.md")
        files.append("~/.grok/rules/security.md (new or append)")

    if not files:
        files.append("~/.grok/rules/ (new focused rule) or relevant persona")

    return files


# ------------------------------------------------------------------
# Output
# ------------------------------------------------------------------

def print_proposals(proposals: list[dict[str, Any]]) -> None:
    if not proposals:
        print("No high-signal patterns found above threshold.")
        return

    print("\n" + "=" * 80)
    print("COMPOUND LEARNINGS — ADVANCED PROPOSALS (Multi-signal Impact + Meta Detection)")
    print("=" * 80 + "\n")

    for i, p in enumerate(proposals, 1):
        print(f"{i}. {p['pattern']}")
        print(f"   Occurrences : {p['occurrences']}   |  Confidence: {p['confidence']}")
        print(f"   Impact      : {p['impact']} (Priority: {p['priority_score']})")
        print(f"   Category    : {p['category']}")
        print(f"   Suggested   : {p['recommended_type']}")
        print(f"   Why this matters now: {p.get('why_now', '')}")
        print(f"   Rationale   : {p['rationale']}")
        print()
        print("   Real examples seen:")
        for ex in p.get("examples", []):
            print(f"     - {ex}")
        print()
        print("   Draft content (ready to use):")
        for line in p["draft_content"].split("\n"):
            print(f"     {line}")
        print()
        print("   Suggested files to modify:")
        for f in p["suggested_files"]:
            print(f"     • {f}")
        print("\n" + "-" * 75 + "\n")


def print_meta_patterns(meta: list[dict[str, Any]]) -> None:
    if not meta:
        return

    print("\n" + "!" * 80)
    print("META-PATTERN OPPORTUNITIES — Highest Leverage Improvements")
    print("!" * 80 + "\n")

    for m in meta:
        print(f"Category: {m['category']}")
        print(f"  Volume: {m['pattern_count']} patterns → {m['total_occurrences']} total occurrences")
        print(f"  Strategic Recommendation:")
        print(f"    {m['suggested_artifact']}")
        print()
        print("  Patterns currently being addressed individually:")
        for pat in m["patterns"]:
            print(f"    • {pat}")
        print()
        print("  Why this is powerful: Solving the cluster with one strong artifact compounds much faster")
        print("  than fixing the symptoms one by one.")
        print("\n" + "-" * 80 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Advanced compound-learnings analyzer for Grok")
    parser.add_argument("--min", type=int, default=3, help="Minimum occurrences (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--draft", action="store_true",
                        help="For High-impact proposals, generate draft files in ~/.grok/skills-drafts/compound-learnings/")
    parser.add_argument("--apply", action="store_true",
                        help="Apply previously generated High-impact drafts (with confirmation). Use after --draft.")
    parser.add_argument("--source", type=str, default="default",
                        choices=["default", "implement", "execute-plan", "review"],
                        help="Source of the analysis (affects friction threshold and rationale in Faz 2). "
                             "Use 'review' when called from review skill.")
    parser.add_argument("--ledger-summary", action="store_true",
                        help="Faz 2: Print a summary of recent high-friction patterns from the compound ledger (health check).")
    args = parser.parse_args()

    # Faz 2 - 3: Ledger health check (bağımsız çalışabilir)
    if args.ledger_summary:
        try:
            from pathlib import Path
            import json
            from collections import Counter

            ledger_path = Path.home() / ".grok" / "compound-friction.jsonl"
            if not ledger_path.exists():
                print("No compound-friction.jsonl found yet.")
                return

            patterns = []
            with open(ledger_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        rec = json.loads(line.strip())
                        if rec.get("impact") in ("High", "Medium"):
                            patterns.append(rec.get("pattern", "unknown"))
                    except:
                        continue

            if not patterns:
                print("Ledger exists but contains no High/Medium friction records yet.")
                return

            print("\n=== Compound Friction Health Check (Faz 2) ===")
            print(f"Total high/medium friction records: {len(patterns)}")
            print("\nTop recurring friction patterns:")
            for pat, count in Counter(patterns).most_common(10):
                print(f"  - ({count}x) {pat[:90]}")
            print("\nRecommendation: Run full analyzer with --min 3 --draft to generate improvement proposals.")
            return
        except Exception as e:
            print(f"Error reading ledger: {e}")
            return

    snapshot = run_memory_snapshot()
    raw_issues = snapshot.get("common_issues", [])

    consolidated = consolidate_issues(raw_issues)
    recent_runs = snapshot.get("recent_runs", [])

    proposals = generate_proposals(consolidated, recent_runs, min_occurrences=args.min)
    meta_patterns = detect_meta_patterns(consolidated)

    if args.json:
        output = {
            "proposals": proposals,
            "meta_patterns": meta_patterns
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    print_proposals(proposals)
    print_meta_patterns(meta_patterns)

    print(f"\nTotal strong proposals: {len(proposals)}")
    print(f"Meta-pattern opportunities detected: {len(meta_patterns)}")

    if args.draft:
        try:
            from generate_artifact import write_draft
        except ImportError:
            print("ERROR: generate_artifact.py not found. Cannot generate drafts.")
            return

        generated = []
        for p in proposals:
            if p.get("impact") == "High":
                try:
                    path = write_draft(p)
                    generated.append(str(path))
                except Exception as e:
                    print(f"  ! Failed to generate draft for '{p['pattern']}': {e}")

        if generated:
            print(f"\n=== Draft artifacts generated ({len(generated)}) ===")
            for path in generated:
                print(f"  → {path}")
            print("\nReview the drafts carefully before applying.")
        else:
            print("\nNo High-impact proposals were eligible for draft generation this run.")

    # Faz 2 - A: Review kaynaklı friction için ekstra not
    if any("review" in str(p.get("pattern", "")).lower() or 
           "friction" in str(p.get("rationale", "")).lower() 
           for p in proposals):
        print("\n[Faz 2] Bu analiz review kaynaklı yüksek friction pattern'leri içermektedir.")
        print("Bu pattern'ler compound öğrenme döngüsüne doğrudan beslenmiştir.")

    # Faz 2 - C: Basit Friction Ledger başlangıcı (append-only)
    # Yüksek friction pattern'leri basit bir dosyaya kaydetmeye başlar.
    # Gelecek turlarda bu, monster/cross-training için temel oluşturacak.
    if proposals:
        try:
            from pathlib import Path
            import json
            ledger_path = Path.home() / ".grok" / "compound-friction.jsonl"
            ledger_path.parent.mkdir(parents=True, exist_ok=True)

            high_friction_proposals = [p for p in proposals if p.get("impact") in ("High", "Medium")]
            if high_friction_proposals:
                with open(ledger_path, "a", encoding="utf-8") as f:
                    for p in high_friction_proposals[:5]:  # en fazla 5 tane
                        record = {
                            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
                            "pattern": p["pattern"],
                            "category": p.get("category"),
                            "impact": p.get("impact"),
                            "priority": p.get("priority_score"),
                            "source": args.source,
                            "recommended_type": p.get("recommended_type"),
                            "rationale": p.get("rationale", "")[:200]  # kısa özet
                        }
                        f.write(json.dumps(record, ensure_ascii=False) + "\n")
                print(f"\n[Faz 2 - C] {len(high_friction_proposals[:5])} high/medium friction pattern zenginleştirilmiş metadata ile ledger'a yazıldı.")
                print(f"Konum: {ledger_path}")
        except Exception as e:
            print(f"[Faz 2 - C] Friction ledger yazma hatası (görmezden gelindi): {e}")

    # Faz 2 - 1: Ledger'daki önceki yüksek friction pattern'leri mevcut önerilere enjekte et
    try:
        from pathlib import Path
        ledger_path = Path.home() / ".grok" / "compound-friction.jsonl"
        if ledger_path.exists():
            import json
            past_friction = []
            with open(ledger_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        rec = json.loads(line.strip())
                        if rec.get("impact") in ("High", "Medium"):
                            past_friction.append(rec)
                    except:
                        continue

            # Son 10 kayıttan unique pattern'leri al
            seen = set()
            unique_past = []
            for rec in reversed(past_friction[-10:]):
                if rec["pattern"] not in seen:
                    seen.add(rec["pattern"])
                    unique_past.append(rec)

            if unique_past:
                print(f"\n[Faz 2 - 1] Ledger'dan {len(unique_past)} önceki yüksek friction pattern okundu.")
                print("Bu pattern'ler gelecek analizlerde daha ağır değerlendirilecektir.")
                # Not: Gerçek enjeksiyon scoring'e entegre edilmek istenirse burası genişletilebilir.
    except Exception as e:
        print(f"[Faz 2 - 1] Ledger okuma hatası (görmezden gelindi): {e}")

    if args.apply:
        try:
            from generate_artifact import apply_draft
        except ImportError:
            print("ERROR: generate_artifact.py not found.")
            return

        drafts_dir = Path.home() / ".grok" / "skills-drafts" / "compound-learnings"
        if not drafts_dir.exists():
            print("No drafts directory found. Run with --draft first.")
            return

        # Collect recent High-impact looking drafts
        all_recent_drafts = sorted(
            [f for f in drafts_dir.iterdir() if f.is_file() and f.suffix == ".md"],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        if not all_recent_drafts:
            print("No recent drafts found. Generate some with --draft first.")
            return

        # For now, we take the most recent ones (user can curate the drafts folder)
        candidates = all_recent_drafts[:15]

        print(f"\nFound {len(candidates)} recent draft(s) in {drafts_dir}")
        print("The apply process will show a diff and ask for confirmation for each file.\n")

        applied_count = 0
        skipped = 0

        for draft in candidates:
            print(f"\n--- Reviewing: {draft.name} ---")
            success = apply_draft(draft, auto_confirm=False)
            if success:
                applied_count += 1
            else:
                skipped += 1

        print(f"\n=== Apply session complete ===")
        print(f"Successfully applied: {applied_count}")
        print(f"Skipped / cancelled:  {skipped}")


if __name__ == "__main__":
    main()