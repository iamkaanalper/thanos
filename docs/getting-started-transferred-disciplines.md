# Getting Started with Thanos (Grok port of the original Claude Code AI software team system) Disciplines (Grok)

**Goal:** Make the most valuable patterns from Claude Code immediately usable in your daily Grok work.

All artifacts live under `.grok/` only. Nothing touches `~/.claude/`.

**Catalog parity note:** Agents (147 files for 139 roles), Skills (822 files >683), Hooks (163 files) achieved via rich Grok Adapters (delegation to core high-leverage impls) + full dedicated for high-freq. See transfer-status and agent-assignment-matrix for details. Real work uses the primitives below + matrix.

---

## The Three Primitives You Will Use Most

### 1. Structured Handoffs (`/handoff` skill or direct templates)

**File:** `.grok/skills/handoff/SKILL.md`

**When to use:**
- Every time you `spawn_subagent` for non-trivial work.
- After every review round (QA PASS or ISSUES form).
- When escalating after 3 failed attempts.

**Quick pattern:**
```markdown
## Task Handoff
**Objective:** ...
**Context:** ...
**Deliverables:** ...
**Acceptance Criteria:** ...
```

The most important templates are:
- Standard Task Handoff
- QA / Review Handoff (PASS vs ISSUES)
- Escalation (the 5 options)

### 2. Task Lifecycle Ledger (Executable Bounded QA-Loop)

**Core file:** `.grok/bundled/skills/shared/task_lifecycle.py`

**Why it exists:**
The classic "max 3 rounds + cumulative feedback + escalate" logic lived only in prompts → race conditions and lost state. This ledger makes it real, versioned, and queryable.

**Basic usage (copy-paste):**

```python
from bundled.skills.shared.task_lifecycle import TaskLifecycleLedger, make_devqa_handoff_context

ledger = TaskLifecycleLedger(session_id="my-workspace")
state = ledger.start_or_resume(task_id="my-task-42", objective="...", max_attempts=3)

# Before spawning implementer/reviewer
ctx = make_devqa_handoff_context(ledger, "my-task-42")
# Inject ctx into the prompt

# After a review round
state = ledger.record_attempt("my-task-42", feedback="...", issues=["..."])

if state.status == "escalated":
    # Present the 5 options to the user
```

**Rule of thumb:** If you were about to write "Round 2/3" or "deneme 2/3" in a handoff, use the ledger instead.

Runnable example: `.grok/bundled/skills/shared/examples/bounded_devqa_with_ledger.py`

### 3. Friction Ledger + Dynamic Checklists (Self-Improvement)

**File:** `~/.grok/compound-friction.jsonl` (append-only)

Every time you hit a painful pattern (context loss, repeated bug class, race condition, etc.), append a record. High/Medium impact entries are automatically turned into checklists that get injected into future `implement`, `review`, and `execute-plan` runs.

This is the Grok version of the compound learnings flywheel.

---

## Where the Disciplines Are Already Wired (Production Ready)

| Orchestrator | Ledger | Handoffs | Friction | Bounded 3-Round + Escalation | Pre-Flight |
|--------------|--------|----------|----------|------------------------------|------------|
| `/implement` | ✅ Strong (Production Contract) | ✅ Mandatory | ✅ Dynamic | ✅ Hard limit + escalation | ✅ |
| `/review`    | ✅ Production Contract (after cleanup) | ✅ Recommended | ✅ Dynamic | N/A (single shot or called from implement) | ✅ |
| `/execute-plan` | ✅ Production Contract added | ✅ Strong | ✅ Dynamic | ✅ Per-PR 3-round limit + escalation | ✅ |

These three are the ones you will hit daily.

---

## Core Bundled Agents (Grok-Native, Discipline-Aware)

Located in `.grok/bundled/agents/`:

- `kraken.md` — Heavy lifter for big/complex work (TDD + ledger + bounded QA)
- `reviewer.md` — General reviewer (now with full Pre-Flight + ledger awareness)
- `security-reviewer.md` — Security specialist
- `coroner.md` — Post-mortem + pattern propagation
- `janitor.md` — Tech debt & hygiene
- Others (scout, sleuth, implementer, etc.)

Use them via persona injection or as reference when building custom agents.

---

## How to Actually Use This Tomorrow

1. On any non-trivial feature or fix → run `/implement [--effort N] ...`
   - It will now use the ledger internally for review rounds.
2. When writing your own multi-agent flows → import `TaskLifecycleLedger` + `make_devqa_handoff_context` + handoff templates.
3. When you hit friction → append to `compound-friction.jsonl` (even manually at first).

---

## Current Honest Status (June 2026)

- Highest-leverage disciplines (bounded QA, handoffs, ledger, friction flywheel, Pre-Flight) → **Production usable** in the main orchestrators.
- Agent breadth → Good core set (kraken, reviewer, security-reviewer, coroner, janitor...).
- Full swarm / every specialist agent → Still partial (this was never the goal for day 1).

The parts that give the biggest daily quality and reliability improvement are already in your hands.

---

**Next time you feel context loss or review loops getting sloppy, reach for the ledger + handoff templates.** That single habit move will give you most of the value of the entire transfer.

All the heavy lifting has been done. Now it's just using it consistently.