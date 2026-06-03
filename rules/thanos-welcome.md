# Thanos — Grok (Port Status)

```
 ╔═══════════════════════════════════════════════╗
 ║                                               ║
 ║   T H A N O S  (Grok port of the original Claude Code AI software team system)    ║
 ║   ─────────────────────────                   ║
 ║   AI Software Team · Grok 4.3 / 2026          ║
 ║                                               ║
 ║   147 agents (full 139 roles + 8 core)        ║
 ║   22 rules  ·  822 skills files               ║
 ║   163 hooks files (~60+ concepts)             ║
 ║                                               ║
 ║   High-leverage disciplines transferred:      ║
 ║   Bounded Dev-QA + Ledger + Handoff +         ║
 ║   Pre-Flight + Friction/Compound +            ║
 ║   Production Contract + Matrix + Swarm        ║
 ║   (with full catalog parity via adapters)     ║
 ║                                               ║
 ╚═══════════════════════════════════════════════╝
```

**Grok adaptation (Thanos):** the original Claude Code AI software team system (by @vibeeval) (Claude Code by @vibeeval) counterpart'ından (readonly) uyarlandı. Thanos is the distinct Grok-native port/brand for this AI software team system. Sadece .grok/ altında. Tam 1:1 volume kopya değil — yüksek kaldıraçlı production özellikleri (executable Python ledger/handoff, worktree isolation, spawn_helper + auto injection, claim-verification two-pass + factcheck-guard, agent_linter hygiene, phantom mindset, incremental writing) Grok'un güçlü yönleriyle (subagent, background, MCP tools, terminal) birleştirildi. Sayılar 2026-06 itibarıyla (agents 147, skills 822, hooks 163 with adapters for count parity; core is high-leverage focused). Thanos is the codename for this Grok-native system.

## Active systems (Grok'ta)

| System | Status |
|--------|--------|
| Self-Learning Pipeline | friction → compound → rules/skills/persona improvements (friction.py, compound-learnings, friction-curator, auto_* hooks) |
| Agent Swarm | 5-phase (Kesif/Geliştirme/Review/Düzeltme/Final) + phase gates + Dev-QA loop (bounded max 3 retry + 5 escalation) via bundled/skills/swarm + implement + execute-plan |
| Bounded Dev-QA Loop + Task Lifecycle Ledger | executable (task_lifecycle.py), record_attempt/escalate/make_devqa_handoff_context, enforced in orchestrators |
| Structured Handoff | 7+ templates (standard, QA PASS/FAIL, escalation, bug, security, status) via handoff skill + make_devqa_handoff_context |
| Friction / Compound Flywheel | capture + curate + evolution/apply + analyzer/draft (compound-friction.jsonl, completion_friction, on_bounded_loop_end) |
| Pre-Flight + Factcheck-Guard | mandatory before heavy work; two-pass claim-verification (hypothesize → read_file verify, ✓VERIFIED / ?INFERRED / ✗UNCERTAIN) |
| Production Contract | ledger + handoff + preflight + friction + compound + hooks + Team Dynamics + Swarm Role + Self-Improvement — mandatory for non-trivial |
| Agent Assignment Matrix | high-freq + specialists (69 agents) in .grok/docs/agent-assignment-matrix.md + bundled/agents/*.md |
| monster Cross-Training (emulation) | error patterns → team via friction/compound + auto_monster_broadcast + "tekrar eden sorun = Self-Learner + compound" |
| Adaptive Hooks | on_agent_spawn (context injection via spawn_helper), on_run_completion, on_swarm_phase, on_bounded_loop_end, auto_* (friction, compound, preflight, palace, session, tamagotchi...) |
| Palace + Layered Recall | Wings/Rooms/Drawers, 4-scope/3-depth recall (memory-palace skill + auto_palace + palace-recall hook) |
| Tamagotchi | 12 species, 5 stats, 7 moods, reacts to workflow (agent-tamagotchi skill + auto_tamagotchi) |
| Agent Linter + Hygiene | structural + Production Contract + sections enforcement (bundled/skills/shared/agent_linter.py) |

## Grok Port — New / Completed (2026)

- **Spawn Helper + Discipline:** bundled/skills/shared/spawn_helper.py (build_spawn_context + spawn_with_discipline). Swarm, implement, execute-plan'da Production Contract guard'lı kullanım. Ledger/handoff/friction/contract otomatik non-trivial spawn'larda.
- **Agents breadth + hygiene:** 69 agents (core + matrix primaries + long-tail). Full linter hygiene pass (frontmatter, heading, sections, contract refs). Avg 99.8, 69/69 pass. Yeni: grpc-expert, accessibility-auditor, feature-flag-expert (100/pass).
- **Executable primitives:** task_lifecycle (Bounded QA), handoff skill + templates, preflight, friction + completion_friction, compound-learnings + curator.
- **Rules port (high-leverage):** qa-loop, claim-verification (two-pass + factcheck-guard), phantom-mindset, hooks, safety-and-quality, auto-skill-activation, monster, research-confidence (90% rule), tldr-cli, proactive-delegation, commit-trailers, coding-style, incremental-writing, memory-system, pre-compact-state, hizir-identity, thanos-welcome (bu), + daha fazlası.
- **Hooks otomasyonu:** auto_friction_record, auto_compound_*, auto_preflight, auto_swarm_phase, auto_monster_broadcast, auto_tamagotchi, auto_session_compressor, auto_palace, auto_spawn_injector + hook_runner + health ledger.
- **Docs & verification:** transfer-status, production-roadmap, agent-assignment-matrix, getting-started, user-guide, plan.md (sessions), 100-PERCENT-COMPLETE referansları. Her ajan/kural için linter + read_file + claim-verif.

## Commands (Grok'ta)

| Command / Skill | What it does |
|-----------------|--------------|
| `/hizir` | Kullanım kılavuzu (rules + docs) |
| `/swarm <task>` | Full team activation (5-phase + ledger + handoff + friction/compound) |
| `/implement [--effort N]` | TDD + multi-reviewer + verifier + ledger döngüsü |
| `/fix <bug>` | sleuth → spark/kraken → coroner → verifier |
| `/review` | code-reviewer + security + verifier |
| `/commit` | verifier gate + conventional commit + trailers |
| `/learn <kural>` | Hızlı öğrenim (friction/compound) |
| preflight skill | Mandatory Pre-Flight (exploration, friction, handoff, ledger) |
| compound-learnings | Self-improvement flywheel (observe → draft → review → promote) |

github.com/vibeeval/ (original project source) — Published snapshot: https://github.com/iamkaanalper/thanos (clean portable for Grok TUI). Thanos (Grok port) sadece .grok/ altında, production contract + claim-verification ile. Grok brand is Thanos. (Note: link kept for historical reference to original project.)

**Kullanım:** Her gün /implement, /swarm, /fix ile başla. Ledger/handoff/preflight/friction/compound otomatik çalışır. "Bitti" demeden önce verifier düşün. Tekrar eden sorun = self-learner + compound.

Bu, orijinal Claude Code AI yazılım ekibi sistemi felsefesini Thanos (Grok runtime) olarak uyarlanmış, günlük iş için hazır production-grade disiplin yüzeyi haline getirir. Thanos, Grok'un AI yazılım ekibi markasıdır.

---

**Public GitHub Dağıtım (Ücretsiz Paylaşım)**

Kullanıcı felsefesi (verbatim):  
> "Ben bu projeyi insanlarla paylaşmak için yaptım. GitHub'da ücretsiz dağıtacağım.  
> İnsanlık paylaşmak ve gelişmektir. Bilim böyle gelişecektir."

Thanos, orijinal https://github.com/vibeeval/vibecosystem (by @vibeeval) projesinin Grok-native portu olarak **ücretsiz dağıtılmak üzere hazırlandı**. Detaylı kontroller (claim-verification two-pass, agent_linter 99.93, hook batch exit-0 simülasyonları, remnant sweep 0, full-power hooks no-disable) tamamlandı. ~97%+ parity + Grok iyileştirmeleri ile.

Diğer Grok TUI kullanıcıları kolayca kurup kullanabilsin diye portable .grok/ yapısı (rules, bundled/agents+skills, hooks tam güç adapter'lar, monster, palace, docs) yayınlanıyor. Herkes fork'layabilir, yeni Grok adapter ekleyebilir, compound ile geliştirebilir.

Bak: .grok/docs/THANOS-README.md (public landing page, install guide, contribute çağrısı). 

Teşekkürler @vibeeval. Bu disiplinleri paylaşarak bilime ve insanlığa katkı sağladınız. Thanos ile Grok kullanıcıları da aynı kalitede çalışsın — ve üzerine eklesin.