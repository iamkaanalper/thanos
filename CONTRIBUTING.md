# Contributing to Thanos

Thanks for considering contributing! Here's how you can help.

## Ways to Contribute

### Add New Agents

Create a `.md` file in `bundled/agents/` with YAML frontmatter (this snapshot uses the bundled structure for Grok):

```yaml
---
name: my-agent
description: "What this agent does — one clear sentence"
---

Your agent prompt here. Be specific about the role,
what it should and shouldn't do, and output format.
```

**Fields:**
- `name` (required): kebab-case identifier
- `description` (required): role description

See existing agents in `bundled/agents/` for examples. All include the full Production Contract.

**Note:** This repository is the portable snapshot for Grok TUI users. The full development environment and source for new high-leverage agents/skills lives in the maintainer's `.grok/` setup (see THANOS-README.md for details). PRs here can improve the included snapshot, docs, export script, or add Grok-specific adapters.

### Add New Skills

Create a directory in `skills/` with a `SKILL.md`:

```yaml
---
name: my-skill
description: "When to use this skill and what it does"
---

Skill content — patterns, instructions, checklists.
```

See `skills/` for many examples (core + adapters). All follow the Production Contract.

### Improve Hooks

Python hooks live in `hooks/`. Core in `hooks/core/`, examples/adapters in `hooks/examples/`.

**Development workflow:**

Test by running the Python scripts directly or via the hook runner.

**Hook types (Grok adaptation):**
- PreToolUse — runs before a tool call (can block, inject context)
- PostToolUse — runs after a tool call (can format, validate)
- Other events via the hook system (on_agent_spawn, on_bounded_loop_end, etc.)

**Creating a new hook:**
1. Create `hooks/examples/my-hook.py` (follow existing auto_*.py patterns with handle() and __main__ guard)
2. Ensure it follows the direct TUI protocol (stdin JSON, stdout decision or silent, exit 0)
3. Update relevant docs or the export if needed

See `hooks/README.md` and examples for the Grok-native implementation (Python adapters + full power, no disable).

### Documentation & Translations

- Improve existing docs or add tutorials
- Translate README to new languages
- See docs/ for transfer status, adaptation kit, etc.

### Bug Reports & Feature Requests

Open an issue using the provided templates on GitHub. Include details about your Grok version and setup.

## Development Setup

This repo is a clean portable snapshot. To use:

1. Clone https://github.com/iamkaanalper/thanos
2. Copy the folders into your `~/.grok/` (or equivalent on Windows)
3. Restart Grok

For full development of the Thanos system (adding agents, skills, etc.):
- See the THANOS-README.md for the export process and source notes.
- The original development happens in a full `.grok/` environment with the bundled agents/skills.

## Pull Request Process

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-new-adapter`)
3. Follow the structure (Production Contract in new agents/skills, claim-verification, etc.)
4. Commit with clear messages (`feat:`, `fix:`, `docs:`, etc.)
5. Push and open a PR against `main`
6. Describe what you added and why
7. CI/lint checks if applicable

## Code Style

- **Agents**: Markdown + YAML frontmatter (in bundled/agents/)
- **Skills**: Markdown (SKILL.md) + YAML frontmatter (in skills/)
- **Hooks**: Python (Grok adaptation with handle() + __main__ for TUI direct calls)
- **Rules**: Markdown
- Follow the Production Contract for non-trivial contributions.

## Good First Issues

Look for issues labeled `good first issue`:
- Improve a skill's instructions or adapter
- Add documentation
- Enhance the export script
- Translate or improve README

## License

By contributing, you agree that your contributions will be licensed under the MIT License (same as the project).

## Credits

Thanos is the Grok-native port/adaptation of the original vibecosystem by @vibeeval. See README for full attribution. Contributions here help the Grok community while crediting the original.
