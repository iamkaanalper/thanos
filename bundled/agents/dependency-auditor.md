---
name: dependency-auditor
description: Dependency Auditor (Grok Adapter). Grok-native delegation for this role. See agent-assignment-matrix.md for the actual primary implementation (general-purpose + skills or dedicated specialist).
keywords: [dependency-auditor, adapter, delegation, grok-native]
---

# Dependency Auditor — Grok Adapter

**Note:** This file maintains role parity with the original 139-agent catalog. In Grok, most work for this role is handled by the general-purpose agent combined with relevant skills or a dedicated high-leverage specialist.

## Role & Responsibility
Dependency Auditor responsibilities (adapted for Grok spawn model and skills surface).

## Core Capabilities
- Consult the Grok agent-assignment-matrix.md for the recommended mapping.
- Typical work is delegated to general-purpose + relevant .grok/skills/ or existing dedicated agents in this directory.

## When to Use
Use the mapping in .grok/docs/agent-assignment-matrix.md. This adapter exists so that every original role name has a corresponding file.

## Production Contract (Mandatory)
All actual execution follows the full Production Contract through the implementing agent/orchestrator:
- Record to ledger using task_lifecycle.py
- Emit structured handoff via handoff skill
- Run preflight for non-trivial work
- Capture friction
- Participate in compound flywheel
- Follow claim-verification (two-pass)

## Team Dynamics
Works as a supporting / delegation role. Primary collaboration is with the actual implementing specialist (see matrix).

## Swarm Role
Supports the phase where the mapped specialist is active. See swarm planning in matrix.

## Self-Improvement Participation
Feedback and recurring patterns for this role area are captured via the actual implementing agent and fed to compound / self-learner.

## Hooks Participation
Relevant hooks are fired by the actual implementing agent (on_agent_spawn, on_run_completion, on_swarm_phase, etc.).

## References
- .grok/docs/agent-assignment-matrix.md (definitive mapping)
- .grok/bundled/agents/ (dedicated specialists)
- .grok/bundled/skills/ (for pattern and meta skills)

This adapter ensures count parity while keeping the real work Grok-optimized and high-leverage focused.
