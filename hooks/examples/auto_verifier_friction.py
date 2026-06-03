"""
Hook: on_verifier_run

When the verifier agent finishes a final gate run, this hook can:
- Record high-value friction it discovered
- Trigger extra analysis if many issues found
- Feed directly into compound learnings

For MVP: If verifier found issues, auto-record a friction entry.
"""

from typing import Any, Dict

try:
    from bundled.skills.shared.friction import record_friction
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / ".grok" / "bundled" / "skills" / "shared"))
    from friction import record_friction


def handle(**kwargs) -> Dict[str, Any]:
    """
    Expected kwargs from verifier:
        verdict: "PASS" | "FAIL"
        critical_issues: list
        important_issues: list
        session_context: str
    """
    verdict = kwargs.get("verdict", "")
    critical = kwargs.get("critical_issues", [])
    important = kwargs.get("important_issues", [])
    session_context = kwargs.get("session_context", "verifier-run")

    if verdict == "PASS":
        return {"status": "skipped", "reason": "clean verifier run"}

    total_issues = len(critical) + len(important)

    if total_issues == 0:
        return {"status": "skipped", "reason": "no issues to record"}

    # Record a strong friction signal when verifier catches problems at the gate
    record_friction(
        pattern=f"Verifier caught {total_issues} issues at final gate ({len(critical)} critical)",
        category="Final Gate Leakage",
        description=f"Work reached verifier stage with remaining issues in {session_context}",
        friction_impact="High" if critical else "Medium",
        session_context=session_context,
        recommended_fix_type="Strengthen earlier reviewer + implementer prompts with patterns discovered by verifier",
        tags=["verifier", "final-gate", "auto-hook"],
    )

    # Balanced integration (Phase C): If security or test issues dominate, suggest the specialized skills
    suggested_skills = []
    if any("security" in (i.get("category","") or "").lower() or "auth" in str(i).lower() for i in (critical + important)):
        suggested_skills.append("security-review")
    if any("test" in str(i).lower() or "coverage" in str(i).lower() for i in (critical + important)):
        suggested_skills.append("test-enforcement")

    if suggested_skills:
        print(f"[auto_verifier_friction] Suggest running specialized skills: {suggested_skills}")

    return {
        "status": "success",
        "friction_recorded": True,
        "issues_at_gate": total_issues,
        "suggested_specialized_skills": suggested_skills,
        "hook": "auto_verifier_friction",
    }
