# Grok Agent Assignment Matrix (Thanos (Grok port of the original Claude Code AI software team system) Adapted)

**Purpose:** Which task goes to which agent in the .grok/ bundled ecosystem.
All work uses `spawn_subagent`, worktree isolation where appropriate, persona injection, and full Production Contract (ledger + handoff + preflight + friction + hooks + compound).

This is the Grok-native adaptation of the original high-discipline matrix. Focus is on executable primitives + automatic behaviors via hooks.

## Core Principles (Non-Negotiable)
- Use the **right specialist** first (avoid general-purpose for known categories).
- Every non-trivial task goes through Pre-Flight + (if multi-round) Task Lifecycle Ledger.
- After work: friction capture → hook → compound evolution.
- Team Dynamics (Profiler + Architect + Self-Learner) is consulted on cross-cutting or recurring issues.
- "tekrar eden sorun = mutlaka Self-Learner + compound" rule.

## Developer Assignment

| Task Category                  | Primary Agent              | Backup                  | QA / Review Partners                  |
|--------------------------------|----------------------------|-------------------------|---------------------------------------|
| React/Next.js UI               | designer (preferred)       | frontend-dev            | code-reviewer |
| API endpoint                   | backend-dev (preferred)    | -                       | code-reviewer + security-reviewer |
| Database schema/query          | database-reviewer          | - | code-reviewer |
| Auth/security                  | security-reviewer          | - | security-reviewer |
| CI/CD, Docker, Infra           | devops-expert              | - | verifier |
| AI/LLM integration             | ai-engineer                | - | code-reviewer |
| Large feature (TDD)            | kraken                     | spark (small parts)     | tdd-guide + verifier |
| Small fix/tweak                | spark (preferred) / implementer | - | code-reviewer |
| Large refactoring              | phoenix                    | kraken + refactor-cleaner | code-reviewer |
| Refactoring (general)          | kraken + refactor-cleaner  | janitor                 | code-reviewer |
| Test writing                   | tdd-guide                  | arbiter                 | arbiter / verifier |
| Test data / fixture            | mocksmith (preferred)      | tdd-guide               | arbiter / verifier |
| E2E test                       | e2e-runner (preferred)     | test-enforcement        | verifier / arbiter |
| Test strategy / QA engineering | qa-engineer (preferred)    | tdd-guide + arbiter     | verifier / arbiter |
| Performance                    | profiler                   | - | verifier |
| Documentation                  | technical-writer (preferred) + doc-updater | - | code-reviewer |
| Tech debt / cleanup            | janitor                    | refactor-cleaner        | code-reviewer |
| Dependency upgrade             | migrator                   | devops-expert           | verifier |
| Release / deploy               | (shipper patterns via devops) | - | verifier |
| Bug post-mortem                | coroner                    | sleuth                  | code-reviewer |
| Test data / fixture            | mocksmith (preferred)      | tdd-guide               | arbiter / verifier |
| Bug reproduction               | replay (preferred) / sleuth | - | qa-engineer / verifier |
| Test strategy / QA engineering | qa-engineer (preferred)    | tdd-guide + arbiter     | verifier / arbiter |
| Scaffold / new module / boilerplate | catalyst                | - | code-reviewer |
| Release / deploy / ship        | shipper                    | devops-expert           | verifier |
| GraphQL API | graphql-expert | backend-dev | code-reviewer |
| gRPC API | grpc-expert (new) | backend-dev | code-reviewer |
| WebSocket/realtime | websocket-expert | backend-dev | code-reviewer |
| Redis/caching | redis-expert | backend-dev | code-reviewer |
| ... (other specialists per full matrix: elasticsearch-expert, kafka-expert, vector-db-expert, load-tester, terraform-expert, kubernetes-expert, aws/gcp/azure-expert, oauth-expert, mongodb-expert, etc. already present) |  |  |  |
| ... (full matrix categories)   | Map to closest bundled     | - | appropriate |

**Grok Adaptation Notes:**
- We have strong coverage for: kraken (large TDD), reviewer, verifier, security-reviewer, coroner, janitor, sleuth, tdd-guide, migrator, profiler, architect, self-learner, ai-engineer, devops-expert, compliance-expert, observability-expert, database-reviewer, refactor-cleaner, data-analyst, build-error-resolver, **spark (small/fast fixes), phoenix (large refactors), catalyst (scaffolds/boilerplate), shipper (release/deploy), replay (deterministic bug repro), e2e-runner (E2E journeys), qa-engineer (test strategy + edge cases), oracle/harvest/pathfinder (external research deep), designer (UI/UX systems), backend-dev (API/DB/security/scale), technical-writer + doc-updater (documentation)**, etc.
- Use `spawn_subagent` with the exact persona name from .grok/bundled/agents/*.md or shared/personas.
- For worktree isolation: set `isolation: worktree` on producer agents (kraken, phoenix, etc.).
- Always wire via hooks for automatic friction/compound (on_agent_spawn, on_run_completion, on_swarm_phase, etc.).
- New agents added during expansion closure (spark, phoenix, catalyst, shipper, replay) follow the full Production Contract including Task Lifecycle Ledger, structured handoffs, pre-flight, and friction/compound participation. See bundled/agents/*.md.

## Research & Analysis Assignment
| Category          | Primary     | Backup     |
|-------------------|-------------|------------|
| Codebase exploration | scout / explore | - |
| External research | oracle (primary) + harvest (deep) + pathfinder (repos) | - |
| Bug investigation | sleuth      | scout      |
| Architecture      | architect   | planner    |
| ...               | ...         | ...        |

## Review Assignment
- Code written → code-reviewer
- Auth/data → code-reviewer + security-reviewer
- DB migration → code-reviewer + database-reviewer
- etc.

## Escalation Chain
If a task fails QA 3 times:
- Reassign (e.g. kraken → split to spark)
- Decompose
- Revise approach
- Defer
- Accept with documented limitation

## Severity Mapping
- P0: Immediate, multiple agents parallel (swarm)
- etc.

## When to Use the Core Trio (Team Dynamics)
See team-dynamics-profiler-architect-selflearner.md
- Recurring problem (2nd+ time) → Self-Learner + compound friction.
- Perf bottleneck → Profiler leads.
- Big design/tradeoff → Architect leads.

## Swarm Phase → Agent Mapping
- Phase 1 (Explore): scout + explore + architect
- Phase 2 (Plan): architect + planner + profiler input
- Phase 3 (Impl): kraken / implementer + tdd-guide + specialists per matrix
- Phase 4 (Cross Review): reviewer + security + coroner/janitor + core trio
- Phase 5 (Verify + Compound): verifier + self-learner + compound hooks

All phases fire appropriate hooks (on_swarm_phase, on_phase_end, on_bounded_loop_end, on_compound_analysis_start, etc.).

## High-ROI Agents in This Setup (Grok Bundled)
- kraken: large/complex TDD
- reviewer + verifier: quality gates
- sleuth + coroner: bug → systemic fix
- janitor + refactor-cleaner: hygiene
- profiler + architect + self-learner: the learning loop
- Specialists: ai-engineer, devops-expert, database-reviewer, etc. as per matrix row.

## Usage
When orchestrating:
1. Consult this matrix (or the assignment logic in sleuth router / swarm planning).
2. Spawn the primary (with proper persona + context from handoff/ledger).
3. Enforce Pre-Flight + ledger if bounded.
4. Capture friction + let hooks drive compound.

This matrix + the executable primitives (ledger, hooks, friction, compound_evolution) + agent linter + team-dynamics doc = the full transferred discipline surface.

**Status:** Count parity achieved (post "agents halen eksik tamamla" + "139 tane olsun"). 147 .md files (all 139 original + 8 Grok core). ~70 rich "Grok Adapter" files (linter 99.93). Docs/Verification: **95%+ closed** ("docs verification kısmını tamamla"): transfer, plan, this matrix, roadmap, getting-started, user-guide 22/22 all refreshed with 147/822/163 + "Finished" + evidence. See transfer-status "Docs / Verification Finished".