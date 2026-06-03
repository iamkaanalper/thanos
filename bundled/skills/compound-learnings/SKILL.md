---
name: compound-learnings
description: Self-improvement orchestrator. Transforms session artifacts (friction, review findings, run patterns) into permanent capabilities (new rules, skills, agents, or hook behaviors). Follows full Production Contract discipline.
when-to-use: At the end of significant runs, or when explicitly asked to improve the system based on recent work.
---

# Compound Learnings Skill — Grok Edition (Production Contract Version)

This is the Grok-native realization of the compound-learnings flywheel.

It now sits on top of the modern primitives we built:
- Task Lifecycle Ledger
- Structured Handoffs
- Friction system + completion capture
- Real hook system

## Core Contract (Non-Negotiable)

1. **Pre-Flight**
   - Must pull recent high-impact friction (via get_high_impact_patterns or compound_bridge).
   - Must consider the current Task Lifecycle state if the run is part of a bounded loop.

2. **Input Quality**
   - Prefer data coming through hooks or compound_bridge over raw conversation.
   - Every pattern should have evidence (session_context, run description, severity counts, etc.).

3. **Output Discipline**
   - New artifacts must be high-confidence and narrowly scoped.
   - Must produce clear "apply" instructions (especially for new rules or small skills).
   - Must record what was proposed in the friction ledger.

4. **Hook Awareness**
   - This skill should be callable from hooks (especially on_run_completion and on_friction_recorded).
   - When invoked via hook, it should be lighter and more focused (auto-draft mode).

## Current Implementation Status

This is a focused Production Contract stub. The actual heavy lifting (pattern clustering, draft generation, promotion logic) still lives primarily in the original compound-learnings skill.

However, the **integration surface** is now much better:
- `compound_bridge.py` + `compound_analyzer_trigger.py` provide clean on-ramps.
- Hooks can now drive this skill.
- All new work (verifier, friction, ledger) is designed to feed it cleanly.
- `compound_evolution.py` ile draft değerlendirme + promote/repair/archive karar döngüsü eklendi (Gap-3).

## Recommended Invocation (2026-06+)

```python
from bundled.skills.shared.compound_bridge import feed_run_to_compound

result = feed_run_to_compound(
    session_context=...,
    issue_patterns=...,
    issues_by_severity=...,
    run_analyzer=True,
    analyzer_min=2,
)
```

The `compound_analyzer_trigger.py` now includes:
- Automatic `on_analyzer_start` and `on_draft_generated` hook firing
- Post-success friction recording for successful analyses
- Better draft path extraction

This makes the internal analyzer flow significantly more observable and integrated with the rest of the self-improvement system.

---

The foundation is now solid. Future work can focus on making the analyzer itself smarter and more automatic.