# Agent Orchestration (Grok Port)

## İlgili Kurallar
- `agent-assignment-matrix.md` (docs/ versiyonu + bundled/agents/*.md) → Hangi task hangi agent'a gider.
- `qa-loop.md` → Dev-QA döngüsü, retry logic, escalation (max 3, 5 seçenek).
- `handoff-templates.md` (skill + bu rule) → Agent arası mesaj şablonları.
- `collaborative-decisions.md` → Belirsiz kararlarda AskUserQuestion + plan mode.
- `performance.md` + `research-confidence.md` → Model seçimi, context, 90% kural.

## Available Agents (Grok)

Located in `.grok/bundled/agents/` (69+ total, linter 99.8 avg, full Production Contract):

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| planner | Implementation planning | Complex features, refactoring |
| architect | System design | Architectural decisions |
| tdd-guide | Test-driven development | New features, bug fixes (primary TDD) |
| code-reviewer (reviewer) | Code review | After writing code |
| security-reviewer | Security analysis | Before commits, auth/data |
| build-error-resolver | Fix build errors | When build fails |
| e2e-runner | E2E testing | Critical user flows (Playwright) |
| refactor-cleaner | Dead code cleanup | Code maintenance |
| doc-updater | Documentation | Updating docs, codemaps |
| self-learner | Hatalardan öğrenim | Her hata sonrası + compound |
| verifier | Son quality gate | "Bitti" demeden önce (build+test+lint+ledger) |
| janitor | Tech debt & code hygiene | Codebase temizlik, dead code, file size |
| migrator | Dependency upgrade & migration | CVE scan, breaking change, rollback |
| compass | Session context recovery | Nerede kaldık, decision log, thread tracking |
| shipper | Release & deploy lifecycle | Pre-deploy checklist, changelog, smoke test |
| catalyst | Scaffold & boilerplate | Pattern scan, tutarlı kod üretimi |
| coroner | Post-mortem & pattern propagation | Bug fix sonrası aynı hatayı başka yerde bul |
| mocksmith | Test data & fixture | Type'dan mock data, edge case, fixture library |
| replay | Bug reproduction & flaky test | %100 reproduce adımları, flaky test analizi |
| ... (full: kraken large TDD, spark small-fix, phoenix large-refactor, designer UI/UX, backend-dev API/DB, project-manager, oracle/harvest/pathfinder research, gcp/aws/azure-expert, go/python-reviewer, compliance-expert, technical-writer, grpc-expert, accessibility-auditor, feature-flag-expert, load-tester, vector-db-expert, kafka-expert, elasticsearch-expert, terraform-expert, kubernetes-expert, mongodb-expert, redis-expert, oauth-expert, vault, neuron, nitro, sentinel, nexus, babel, commander, profiler, data-analyst, database-reviewer, observability-expert, sleuth, explore, general-purpose, implementer, reviewer, verifier, self-learner, architect, team-dynamics-profiler-architect-selflearner.md etc.) | | |

Tüm agent'lar .grok/bundled/agents/*.md'de Production Contract (ledger, handoff, preflight, friction, compound, hooks, Team Dynamics, Swarm Role, Self-Improvement) ile tanımlı. agent_linter ile hijyen kontrolü (99.8 avg).

## Immediate Agent Usage (No user prompt needed)

1. Complex feature requests - Use **planner** + enter_plan_mode.
2. Code just written/modified - Use **reviewer** (code-reviewer) + security-reviewer if auth/data.
3. Bug fix or new feature - Use **tdd-guide** (TDD) or **spark** (small).
4. Architectural decision - Use **architect**.
5. Hata yapıldığında - Use **self-learner** + friction + compound.
6. İş tamamlandığında - Use **verifier**.
7. Tech debt/cleanup - Use **janitor** + refactor-cleaner.
8. Dependency upgrade - Use **migrator**.
9. Session başlangıcı/context - Use **compass** + palace recall.
10. Release/deploy - Use **shipper**.
11. Bug fix sonrası propagation - Use **coroner**.
12. Test data lazım - Use **mocksmith**.
13. Bug reproduce edilemiyor - Use **replay**.
14. Large TDD - **kraken** (worktree isolation).
15. External research - **oracle** (primary) + **harvest** (deep) + **pathfinder** (repos).
16. UI/UX - **designer**.
17. Backend/API - **backend-dev**.
18. E2E - **e2e-runner**.
19. QA strategy - **qa-engineer**.
20. Cloud infra - ilgili expert (gcp-expert etc.).
21. Compliance - **compliance-expert**.
22. Docs - **technical-writer** + **doc-updater**.

## Dev-QA Loop (ZORUNLU)

Her task implement edildikten sonra:
1. Developer agent (kraken/spark/phoenix/backend-dev/designer etc. matrix'e göre) implement eder.
2. @reviewer (code-reviewer) + @verifier + (auth/data için security-reviewer, DB için database-reviewer) QA yapar.
3. PASS → sonraki task | FAIL (deneme <3) → developer'a feedback (handoff-templates #3), retry (sadece listelenen sorunları düzelt, yeni özellik EKLEME).
4. 3x FAIL → escalation (reassign, decompose, revise, defer, accept with documented limitation) — handoff-templates #4.
5. STATUS → ledger + pipeline güncelle (task_lifecycle).

Detay: `qa-loop.md`. Bounded max 3 retry + executable ledger.

## Parallel Task Execution

ALWAYS use parallel Task execution for independent operations (spawn_subagent multiple, worktree isolation for producers like kraken/phoenix/implementer).

Bağımsız task'ları farklı agent'lara AYNI ANDA ver (örneğin UI + API + test data parallel).

Bağımlı task'lar için: dependency QA'den geçene kadar BEKLE, sonra ata.

## Multi-Perspective Analysis

For complex problems, use split role sub-agents (via spawn_subagent parallel):
- Factual reviewer (scout/explore + factcheck-guard)
- Senior engineer (kraken or architect)
- Security expert (security-reviewer)
- Consistency reviewer (reviewer + janitor)
- Redundancy checker (coroner or self-learner)
- Perf (profiler + nitro)

## Grok Adaptation Notes

- Agent'lar `.grok/bundled/agents/` altında (69+). Her biri tam Production Contract + matrix primary mapping + linter 99.8+.
- Spawn: `spawn_subagent` + `spawn_with_discipline` (build_spawn_context via spawn_helper) — ledger/handoff/friction/contract otomatik.
- Isolation: producer'larda `isolation: worktree` (true parallel, no shared file pollution).
- Hooks: on_agent_spawn (context injection: ledger snapshot + handoff + friction hint + contract reminder), on_run_completion (friction), on_bounded_loop_end.
- Matrix: .grok/docs/agent-assignment-matrix.md (high-freq dedicated ajanlar + escalation + severity + hizir-only).
- Self-improvement: friction → compound → rule/agent/skill evolution (self-learner + compound-learnings).
- Claim-verification: Her varlık iddiası öncesi two-pass (hypothesize ?INFERRED → read_file ✓VERIFIED). agent_linter + factcheck-guard skill.
- No .claude/ touch. Tüm iş .grok/ altında.

Bu kural, Thanos (Grok port of the original Claude Code AI software team system) agent orchestration disiplinini Grok'un executable agent sistemi + matrix + ledger + hooks + compound ile tam entegre eder. Doğru ajan + disiplin = yüksek kaliteli, self-improving iş.