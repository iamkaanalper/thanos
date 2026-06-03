---
name: friction-curator
description: Manages the friction ledger (compound-friction.jsonl). Curates high-impact patterns, suggests new Pre-Flight items, deduplicates, and helps close the self-improvement loop. Works closely with hooks and compound-learnings.
when-to-use: When maintaining the health of the self-improvement flywheel, or as part of compound-learnings / end-of-run processes.
---

# Friction Curator Skill â€” Grok Edition

This skill is responsible for the long-term health of the Friction Ledger system.

## Core Responsibilities

1. **Curation**
   - Review recently recorded friction (especially via auto hooks).
   - Identify high-frequency or high-impact patterns that should become permanent Pre-Flight checklist items or new rules.

2. **Deduplication & Quality**
   - Prevent low-value or duplicate noise from polluting the ledger.
   - Promote truly valuable patterns (with evidence) into higher-confidence artifacts.

3. **Integration with Hooks & Compound Learnings**
   - Designed to be called by `on_friction_recorded` and `on_draft_generated` style hooks.
   - Feeds directly into compound-learnings drafts.

4. **Pre-Flight Contribution**
   - Its main output should be suggestions that the preflight skill (or on_implement_start hook) can inject into future runs.

## Recommended Flow (Modern)

```python
# After a run produces friction (via hook or bridge)
from bundled.skills.shared.friction import get_high_impact_patterns

patterns = get_high_impact_patterns()
# Then call this skill (or its logic) to curate them into actionable Pre-Flight updates
```

## Current Status

Production Contract stub. The actual ledger management is still mostly done through the friction.py helpers. This skill provides the **governance and curation layer** on top, which is the missing piece for the flywheel to mature.

---

Together with the preflight skill and the hook system, this completes a strong closed loop for continuous improvement.

## Real Implementation (Sýrayla #2 ile Production-Ready)

Gerçek kod: undled/skills/shared/friction_curator.py

- un_friction_curation() — büyük run / hook sonunda çaðrýlýr
- curate_high_impact_patterns() — tekrar eden High/Medium pattern'leri bulur
- get_preflight_suggestions_from_curator() — preflight için hazýr markdown blok üretir

Hook entegrasyonu (on_friction_recorded) ve preflight ile derin wiring tamamlandý (Sýrayla #2).

## Current Status (Sýrayla #2 Tamam)

Artýk thin stub deðil. Gerçek curation + Pre-Flight öneri üretimi + hook tetikleme production-ready seviyede. Flywheel'in 'öðrenilen friction › kalýcý kural' kýsmý kapandý.

Together with preflight + hook system, the core self-improvement loop is now fully wired and executable.
