# TLDR CLI - Token-Efficient Code Analysis (Grok Port)

You have efficient code analysis tools available for token-efficient codebase understanding. In this Grok environment, leverage built-in capabilities and skills for structure, flow, impact, etc.

**Grok Note:** We have `tldr` references in some contexts, but primarily use:
- Native tools: list_dir, read_file, grep (with ripgrep power)
- Skills: tldr-code, tldr-overview, tldr-deep, tldr-router, tldr-stats (from available skills)
- For full parity with original: the philosophy is the same — use structured, low-token analysis before raw file reads.

## Core Commands / Equivalent Capabilities (Grok)

**Core analysis**
- list_dir / tldr tree equivalent: See file tree and summary.
- tldr structure / tldr-code: Code structure, codemaps (use tldr-code skill or tldr structure if CLI available).
- grep + search-router: Search files (prefer search-router or grep tool over raw for structured results).
- read_file: Full file info (but use tldr extract / tldr context first for LLM-ready summaries).
- tldr context equivalents: Use tldr context skill or "tldr context <entry>" style via skills for relevant code.

**Flow analysis**
- tldr cfg / dfg / slice / calls: Control/data flow, program slice, cross-file calls. Use tldr-deep or dedicated flow tools if present; otherwise trace manually with read + grep after high-level tldr.

**Codebase analysis**
- tldr impact: Who calls this? (reverse call graph) — use dependency-graph or manual impact analysis via grep + read.
- tldr dead: Find unreachable/dead code — use dead-code skill or janitor/refactor-cleaner patterns.
- tldr arch: Detect architectural layers — use tldr-overview or architect agent.

**Import analysis**
- tldr imports / importers: Parse and reverse imports — use grep for "import|from .* import" or dedicated import tools.

**Quality & testing**
- tldr diagnostics: Type check + lint (pyright/ruff etc.) — run via terminal (pyright, ruff, tsc --noEmit) or qlty-check skill.
- tldr change-impact: Find tests affected by changes — use test-enforcement or manual call graph + test file search.

## When to Use (Grok Adaptation)

- **Before reading files**: Use list_dir + tldr-overview / tldr structure equivalent (or tldr-code skill) to see what exists. Never start with raw read on unknown code.
- **Finding code**: Use grep / search-router / tldr search equivalent instead of blind reads.
- **Understanding functions**: Use high-level structure first, then targeted read + flow tracing (cfg/dfg style via manual or tools).
- **Debugging**: Use tldr slice equivalent (find what affects a line) via grep + read focused on data/control.
- **Context for tasks**: Use tldr context style (LLM-ready summary) via skills before spawning agents.
- **Impact analysis**: Before refactoring, analyze who calls / imports the target (tldr impact equivalent).
- **Dead code**: Use janitor + dead-code skill or tldr dead style before cleanup.
- **Architecture**: Use tldr arch / tldr-overview + architect agent.
- **Import tracking**: Grep or dedicated for imports/importers.
- **Before tests**: Use diagnostics (type/lint) + test-enforcement.
- **Selective testing**: Use change-impact thinking (what tests cover the changed code).

## Languages

Supports analysis for Python, TypeScript/JS, Go, Rust (and others via general tools).

## Example Workflow (Grok Style)

```bash
# 1. See project structure
list_dir src/   # or tldr tree equivalent

# 2. Find relevant code
grep "process_data" src/   # or search-router / tldr search style

# 3. Get context for a function
# Use tldr context equivalent or read focused after structure

# 4. Understand control flow
# Targeted read + trace calls (tldr cfg style via tools or manual)

# 5. Before refactoring - check impact
# Analyze callers/importers (tldr impact style)

# 6. Find dead code to clean up
# dead-code skill or janitor + tldr dead style
```

## Codebase Analysis Commands (Grok Equivalents)

Use the philosophy: token-efficient, structured, layered analysis (AST-ish via tools, call graph via grep/impact, CFG/DFG via tracing) before full reads.

For full original TLDR CLI parity, ensure tldr is on PATH in the environment when needed; otherwise fall back to our skills (tldr-code, tldr-overview, etc.) and native tools.

**Grok-specific note:** This rule enforces the "stop at 90% research confidence" (see research-confidence.md) + claim-verification (two-pass read, not grep-only). Always combine with preflight for non-trivial analysis.

(Original from Claude/Thanos (Grok port of the original Claude Code AI software team system) TLDR CLI; ported with emphasis on Grok's tool + skill set (tldr-code skill, grep, list_dir, read_file, impact via analysis, diagnostics via terminal/qlty, etc.) while preserving the token-efficiency and "use before raw reading" discipline.)
