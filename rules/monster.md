# monster: Agent Cross-Training (Grok Port)

- Hata yapan agent'in hatasi TUM ekibe yayilir (error-ledger + compound friction)
- Session basinda takim hatalari context'e enjekte edilir (via hooks + compound)
- Her producer agent spawn sonrasi otomatik review hatirlatmasi yapilir (Production Contract + linter)
- Agent performansi skill-matrix + friction/compound evolution ile takip edilir

**Grok Adaptation:** FULL IMPLEMENTED. .grok/monster/ dir with error-ledger.jsonl + skill-matrix.json (seeded + auto-updated). Python CLI at .grok/monster/monster.py (report / agent <name> / errors / weak / leaderboard). 

Broadcast via auto_monster_broadcast.py hook (now writes ledger + updates matrix on every error). Integrates with friction/compound/self-learner + on_agent_spawn context injection for team training.

Session start: hatalar context'e enjekte (via compound recall + hook-health). Producer spawn sonrası review hatirlatmasi (Production Contract).

CLI: python .grok/monster/monster.py report   (or add to PATH)

No node; pure Python + JSONL for Grok runtime. Cross-training now executable and persistent.

## CLI Komutlari (Current Grok Emulation)

Use compound + friction tools + hooks health:

- General status / recurring: compound-learnings analyzer or friction-curator reports (high-impact patterns)
- Agent detail / weak: agent_linter batch + friction history for specific agent
- Errors (last period): hook-health.jsonl + compound-friction.jsonl queries
- Leaderboard: manual via compound evolution scores or reputation notes in team-dynamics

Future: .grok/monster/ dir + scripts/monster-cli equivalent (report/agent/errors/weak/leaderboard) mirroring original.

## Veri Dosyalari (Current + Planned)

| Dosya | Icerik |
|-------|--------|
| `~/.grok/compound-friction.jsonl` + `hook-health.jsonl` | Current: friction events + hook success/failure (agent, tip, context) |
| `~/.grok/monster/error-ledger.jsonl` (planned Phase 2) | Tum hatalar (agent, tip, ders) |
| `~/.grok/monster/skill-matrix.json` (planned) | Agent profilleri ve basari oranlari |

See: hooks/core/auto_monster_broadcast.py (or equivalent), compound-learnings/SKILL.md, friction-curator, agent-linter for current cross-training signals.

(Original from Claude/Thanos (Grok port of the original Claude Code AI software team system); ported with Grok flywheel + hook emphasis. Full dir/CLI deferred to P2 per roadmap.)
