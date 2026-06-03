# Hooks System (Grok Port)

## Hook Tipleri
- **PreToolUse**: Tool calistirilmadan once (validasyon, parametre degisiklik)
- **PostToolUse**: Tool calistiktan sonra (format, kontrol)
- **Stop**: Session bitince (son dogrulama)

## Mevcut Hook'lar (Grok Python Implementation)
### Core
- on_run_completion → friction
- on_friction_detected → tagger
- on_verifier_run → friction
- on_bounded_loop_end → ledger sync
- on_agent_spawn → context injector (ledger + friction + team)
- on_friction_recorded → analyzer
- on_implement_start → preflight
- on_analyzer_start / on_draft_generated / on_compound_analysis_start / on_draft_applied / on_self_improvement_cycle → compound flywheel
- Specialist: on_ai_feature, on_infra_change, on_compliance_check, on_observability_setup, on_db_change, on_refactor_pass, on_data_analysis
- Swarm: on_swarm_start, on_swarm_phase, on_phase_end
- Linter: on_agent_lint
- Madde-3: on_palace_auto_save, on_tamagotchi_update, on_skill_compound, on_model_route, on_session_compress, on_monster_broadcast, on_experiment_trigger

## Hook Auto-Execute
Our runner (hook_runner.py) calls handlers safely, records health to ~/.grok/hook-health.jsonl. Existence guard via has_hook().

## Kurallar
- Auto-accept: guvenli, tanimli planlar icin
- Exploratory is icin disable et (use preflight)
- Use register_hook for dynamic.

**Grok Note**: Python focused for our orchestrators/skills. ~40+ events registered (core flywheel + specialists + swarm + palace/memory/layered-recall + new for hooks bitir: credential-deny, tldr-enforcer, pre-compact-continuity, session-start-recall, intent-classifier). 

Core runner supports run_hook, register_hook, has_hook, health to hook-health.jsonl, auto-discovery notes. 

High-value ported/enhanced: on_agent_spawn (with palace recall), on_pre_compact, on_session_start, on_pre_tool_use (credential guard), on_tldr_enforce, full monster/palace/tamagotchi/compound integration, session compressor, preflight checks.

See .grok/hooks/core/hook_runner.py (enhanced), examples/auto_*.py (25+), .grok/skills/layered-recall + memory-palace for recall hooks, pre-compact-state rule.

Original in ~/.claude/rules/hooks.md (TS with 73 hooks + dist/ 60+). We prioritized adaptive high-leverage for Grok (flywheel, memory efficiency, security guards, token savings) over 1:1 volume. Full auto-activation + more guards in future via register_hook.

Hooks now "bitir": wired into spawn_helper, preflight, swarm, compound, palace, on_spawn for low context loss + self-improvement.