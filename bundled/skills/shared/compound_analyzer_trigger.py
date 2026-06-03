"""
Compound Analyzer Trigger (Hook-Aware)

Makes it easy and safe to invoke the compound-learnings analyzer
from hooks or at the end of big runs.

Now deeply integrated with the hook system:
- Fires on_analyzer_start before running
- Fires on_draft_generated after successful drafts
- Allows hooks to influence or react to the analysis
"""

import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from grok.hooks.core.hook_runner import run_hook


def trigger_compound_analyzer(
    min_patterns: int = 2,
    source: str = "run",
    draft: bool = True,
    timeout: int = 60,
    session_context: str = "",
) -> Dict[str, Any]:
    """
    Run the compound-learnings analyzer with sensible defaults for our new system.

    Now fires hooks at key points for automatic behaviors.
    """
    analyzer_path = Path.home() / ".grok" / "skills" / "compound-learnings" / "scripts" / "analyze.py"

    if not analyzer_path.exists():
        return {
            "status": "analyzer_not_found",
            "path_checked": str(analyzer_path),
        }

    # Fire pre-analyzer hook (hooks can inject extra context or block)
    run_hook(
        "on_analyzer_start",
        min_patterns=min_patterns,
        source=source,
        session_context=session_context,
    )

    cmd = ["python3", str(analyzer_path)]
    if min_patterns:
        cmd.extend(["--min", str(min_patterns)])
    if source:
        cmd.extend(["--source", source])
    if draft:
        cmd.append("--draft")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        # === Compound Evolution Döngüsü (ileri taşınmış) ===
        try:
            from .compound_evolution import run_evolution_cycle, suggest_full_promotion_package

            draft_paths = []
            for line in (result.stdout or "").splitlines():
                if "→ " in line and (".md" in line or "/skills-drafts/" in line):
                    candidate = line.split("→ ", 1)[-1].strip()
                    if Path(candidate).exists():
                        draft_paths.append(candidate)

            evolution_summary = None
            promotion_packages = []
            if draft_paths:
                evolution_summary = run_evolution_cycle(draft_paths)
                # Her promote adayı için promotion package önerisi üret
                for ev in evolution_summary.get("evaluations", {}).get("promote", []):
                    pkg = suggest_full_promotion_package(ev)
                    promotion_packages.append(pkg)

            # Sonucu zenginleştir
            if isinstance(result, dict):
                result["evolution"] = evolution_summary
                result["promotion_packages"] = promotion_packages
            else:
                result = {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                    "evolution": evolution_summary,
                    "promotion_packages": promotion_packages,
                }

            # Success path: fire hook for draft generation + positive friction (Production Contract)
            try:
                run_hook(
                    "on_draft_generated",
                    draft_paths=draft_paths,
                    session_context=session_context,
                    source=source,
                )
            except Exception:
                pass

            try:
                from bundled.skills.shared.friction import record_friction
                record_friction(
                    pattern=f"Compound analyzer successfully produced {len(draft_paths)} drafts",
                    category="Self-Improvement Success",
                    description=f"Analysis run for {session_context or source} generated actionable drafts.",
                    friction_impact="Low",
                    session_context=session_context,
                    recommended_fix_type="Review drafts and selectively apply using the analyzer --apply command",
                    tags=["compound-learnings", "analyzer-success", "auto"],
                )
            except Exception:
                pass

        except Exception:
            pass  # Evolution başarısız olursa ana analyzer sonucu bozulmasın

        # Prepare for on_draft_applied hook (fire via compound_apply_feedback.report_apply_result after human applies)
        # run_hook("on_draft_applied", draft_paths=draft_paths, applied_successfully=True, session_context=session_context)

        return result if 'result' in dir() else {"stdout": result.stdout if hasattr(result, 'stdout') else "", "returncode": getattr(result, 'returncode', 0)}

    except subprocess.TimeoutExpired:
        return {"status": "timeout", "timeout_seconds": timeout}
    except Exception as e:
        return {"status": "error", "error": str(e)}
