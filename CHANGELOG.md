# Changelog

All notable changes to the Thanos (Grok AI software team) portable snapshot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06

### Added
- **First stable public release** of the portable Thanos snapshot for Grok TUI users.
- Full adaptation of the original vibecosystem (by @vibeeval) high-leverage disciplines into Grok-native form (distinct brand "THANOS - Your AI software team. Built on Grok").
- **147 agents** (106%+ count parity over original 139): every agent includes verbatim **Production Contract** (6 mandatory items: ledger, handoff, preflight, friction, compound, claim-verification two-pass), agent_linter hygiene (99.93 avg), Swarm roles, and self-improvement participation.
- **822+ skills entries** across 311+ skill directories (core orchestrators + Grok Adapters + user skills) — 100% activation with SKILL.md, Production Contract references, hooks, and delegation notes.
- **22 rules** (full port of the highest-value ones + Grok-specific adaptations: thanos-welcome, claim-verification, qa-loop, monster, hooks, phantom-mindset, coding-style, safety-and-quality, incremental-writing, memory-system, pre-compact-state, etc.).
- **163+ hook files** with **full power** (pre + post ToolUse): 64+ bulk updated with guarded `__main__`, stdin JSON payload parsing, `handle(data)`, `reportHealth`, silent side-effects + compact decision JSON, always `sys.exit(0)`. No hooks disabled. Direct TUI spawn protocol fully supported (both .grok Python adapters and original .claude dist mjs with ASCII patches for Windows).
- **monster** cross-training system (renamed from canavar, 0 remnant in active sources): `monster.py` CLI, error-ledger.jsonl, skill-matrix.json (87+ agents, 5-dim scoring), auto_monster_broadcast hook.
- **Palace + layered-recall**: hierarchical memory (Wings > Rooms > Drawers), 4-scope / 3-depth progressive recall (10-50x token savings), pre-compact wip-state, default project skeleton.
- **Bounded Dev-QA Loop** (assign → implement → @code-reviewer + @verifier → PASS / FAIL<3 retry or escalate: reassign/decompose/revise/defer/accept) with TaskLifecycleLedger + handoff skill.
- **spawn_with_discipline + spawn_helper**: automatic injection of ledger_state, handoff_ctx, friction_hint, production_contract_reminder on every agent spawn.
- **Compound self-improvement flywheel**: friction-curator, compound-learnings, auto skill evolution.
- **claim-verification two-pass + factcheck-guard**: Pass 1 hypothesize (?INFERRED from grep), Pass 2 read actual file (✓VERIFIED). Enforced on all public claims and agent/skill work.
- Clean portable export structure (rules/, bundled/agents+skills+personas, hooks/core+examples full power, monster/, palace/, projects/, skills/, docs/) ready to robocopy into `~/.grok/`.
- Bilingual public documentation: English first (complete), then full Türkçe section after separator. No mixed-language paragraphs.
- Adapted community files for the repo:
  - CODE_OF_CONDUCT.md
  - CONTRIBUTING.md
  - SECURITY.md
- User philosophy preserved verbatim: "Ben bu projeyi insanlarla paylaşmak için yaptım. GitHub'da ücretsiz dağıtacağım. İnsanlık paylaşmak ve gelişmektir. Bilim böyle gelişecektir."
- Extensive verification artifacts (claim-verif passes, linter runs, hook exit-0 simulations, remnant sweeps = 0, absolute-path hygiene, Production Contract audits) documented in `docs/transfer-status-2026-06-02-end-of-day.md`, `docs/PUBLIC-RELEASE-CHECKLIST.md`, and `guncel-durum-tablo.md`.
- Grok-native enhancements: worktree isolation, tldr-cli integration (95% token savings), enter_plan_mode, MCP tool hybrid usage, phantom mindset, incremental writing.

### Changed
- Branding finalized to "THANOS - Your AI software team. Built on Grok" (removed any "Grok native port of" phrasing from headers per maintainer request; historical credit to original preserved in docs, social media attribution left to author).
- All internal paths and references updated to .grok/ (readonly reads of .claude/ only for reference during port).
- Numbers in docs/welcome updated to final verified counts (147/822/163).

### Fixed
- All hook direct-execution issues (BOM, missing __main__, wrong sys.path, unicode in dist mjs) resolved without disabling any hooks.
- Remnant purge: 0 active occurrences of "vibecosystem"/"canavar" in portable source (only archival/credit mentions remain).
- Multiple linter, claim-verification, and full-power hook batch audits passed with evidence.

### Notes
- This is the initial v1.0.0 public distribution. The development source lives in the maintainer's `~/.grok/` tree; this `thanos/` folder is the clean, personal-data-free portable snapshot published to GitHub for free use by the community.
- Future releases will follow semver. Minor/patch updates will be made available via the same portable export process.
- Original project: https://github.com/vibeeval/vibecosystem (credit on social media by the author as requested).

[1.0.0]: https://github.com/iamkaanalper/thanos/releases/tag/v1.0.0

---

## [Unreleased]

### Planned
- Ongoing agent/skill additions via Grok Adapters and community contributions.
- Further compound-driven self-improvements.
- Additional docs, examples, and Turkish/English parity maintenance.