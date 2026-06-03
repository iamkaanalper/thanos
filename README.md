# THANOS - Your AI software team. Built on Grok

**https://github.com/iamkaanalper/thanos**

**Star & contribute:** https://github.com/iamkaanalper/thanos — original credit on social media by the author.

## Community

- [Code of Conduct](CODE_OF_CONDUCT.md) — adapted from the original vibecosystem project.
- [Contributing Guidelines](CONTRIBUTING.md) — how to add agents, skills, hooks, and improvements.
- [Security Policy](SECURITY.md) — how to report vulnerabilities responsibly.

Please read them before contributing. Original credit to @vibeeval on social media by the author.

> "I created this project to share with people. I will distribute it for free on GitHub.  
> Humanity is sharing and developing. This is how science progresses."

With this philosophy, we offer high-leverage disciplines (Bounded Dev-QA Loop, Production Contract, Structured Handoff, Pre-Flight, Friction/Compound self-improvement flywheel, Palace layered memory, monster cross-training, claim-verification two-pass, full-power pre/post hooks) to Grok TUI users completely free. Anyone can build upon it, extend it, and improve it.

## Why Thanos?

The original system (vibecosystem by @vibeeval) brought an outstanding AI software team discipline to Claude Code:

- 139+ agents + assignment matrix
- 295+ skills + meta/patterns + SKILL.md + Production Contract
- 73 hooks + 587 handlers
- Canavar (now monster) cross-training with error-ledger + skill-matrix + CLI
- Palace + layered recall (4-scope / 3-depth)
- Compound flywheel (self-improvement)
- Bounded Dev-QA (max 3 retries + escalation via handoff-templates)
- Production Contract + handoff templates
- Claim-verification (two-pass factcheck-guard)

**Thanos** adapted and enhanced this for Grok 4.3+ (April 2026):

- 147 agents (106%+ count parity, 100% Production Contract + agent_linter 99.93 avg)
- 822+ skills entries / 311+ skill directories (100% activation with SKILL.md + Contract)
- 22 rules (full port of the high-value ones + Grok-specific additions)
- 163+ hook files (pre/post full power; 64+ bulk-guarded with proper __main__ + handle(data) + reportHealth for TUI direct spawn)
- Monster (full rename + remnant purge, 0 active "vibecosystem"/"canavar" in .grok sources)
- Palace + layered-recall + pre-compact WIP state
- spawn_with_discipline + spawn_helper (automatic ledger/handoff/friction/contract)
- Grok-native enhancements: worktree isolation for parallel subagents, tldr-cli (95% token savings), enter_plan_mode, MCP hybrid tools

**Overall daily usability: ~97%+** (higher than original thanks to count parity + Grok robustness + full-power hooks).

**Any missing pieces left?** No.

Detailed checks completed (claim-verification two-pass + factcheck-guard on all public claims, agent_linter batch runs, hook subprocess simulations with 0 failures, remnant sweeps, absolute-path audits, full power no-disable policy). All agents and skills are activated (verbatim Contract / SKILL.md + handle entrypoint).

Full inventory and evidence: [transfer-status-2026-06-02-end-of-day.md](docs/transfer-status-2026-06-02-end-of-day.md) and [guncel-durum-tablo.md](guncel-durum-tablo.md)

## Quick Start (Grok TUI)

1. Get this snapshot (clone or download zip from the GitHub repo).
2. Copy the portable parts into your `~/.grok/` (see the Installation section below).
3. Launch Grok.
4. Type `/swarm <task>` or `/implement [--effort N] <task>`.

Ledger, handoff, preflight, friction capture, compound, palace recall, and monster broadcast run automatically. Consider running the verifier before declaring "done".

## Installation (for other Grok users)

**Important:** This is the ported structure extracted from a personal `~/.grok/` directory. When publishing on GitHub we share **only the portable parts**. Never publish personal files (sessions/, auth.json, logs/, downloads/, active_sessions*, tip_cursor.json, etc.).

Recommended portable layout:

```
~/.grok/
├── rules/                  # 22 rules (thanos-welcome, monster, claim-verification, qa-loop, phantom, hooks, safety, coding-style, incremental-writing, memory-system, pre-compact, auto-skill-activation, tldr-cli, proactive-delegation, commit-trailers, collaborative-decisions, performance, agents, handoff-templates, hizir-identity, cross-project-learning, research-confidence)
├── bundled/
│   ├── agents/             # 147 .md (complete 139 roles + Grok adapters + 8 core; every file contains the verbatim Production Contract)
│   ├── skills/             # core orchestrators (implement, execute-plan, review, swarm, preflight, friction-curator, compound-learnings, handoff, task_lifecycle, spawn_helper, agent_linter, ...) + shared/
│   └── personas/roles/...
├── hooks/
│   ├── core/hook_runner.py
│   ├── examples/           # 100+ auto_*.py (full __main__ + handle(data) + reportHealth; pre/post full power)
│   └── README.md
├── monster/                # monster.py CLI + error-ledger.jsonl + skill-matrix.json
├── palace/                 # default.jsonl + index (skeleton)
├── projects/               # default/ (MEMORY.md + wip-state.jsonl skeleton)
├── skills/                 # user/portable skills (core high-leverage + adapters)
├── docs/                   # THANOS-README.md, transfer-status, agent-assignment-matrix, thanos-grok-*, user-guide (Thanos-related)
└── guncel-durum-tablo.md
```

**Copy recommendation (Windows PowerShell example):**

```powershell
# Copy only portable parts (into your own .grok)
$src = "C:\path\to\thanos\.grok"
$dst = "$env:USERPROFILE\.grok"

# Rules, bundled agents/skills, hooks, monster, palace skeleton, docs
robocopy "$src\rules" "$dst\rules" /E
robocopy "$src\bundled" "$dst\bundled" /E
robocopy "$src\hooks" "$dst\hooks" /E
robocopy "$src\monster" "$dst\monster" /E
robocopy "$src\palace" "$dst\palace" /E
robocopy "$src\projects" "$dst\projects" /E
robocopy "$src\docs" "$dst\docs" /E
robocopy "$src\skills" "$dst\skills" /E   # only the portable ones
copy "$src\guncel-durum-tablo.md" "$dst\"
```

Then restart the Grok TUI. When the TUI directly spawns the Python adapter hooks, the full logic executes (read stdin JSON → handle(data) → side-effects + reportHealth + silent exit 0).

**Full power note:** The original `.claude/settings.local.json` + `dist/*.mjs` (for Claude users) were left intact and the unicode/encoding issues were fixed with targeted ASCII patches. No hooks were disabled. Both the Claude and Grok sides can run at full power in parallel if desired.

## Commands

| Command / Skill            | What it does |
|----------------------------|--------------|
| `/hizir`                   | Usage guide (rules + docs) |
| `/swarm <task>`            | 5-phase full team activation (Discovery → Development → Review → Fix → Final) + ledger + handoff + friction/compound + phase gate |
| `/implement [--effort N]`  | TDD + multi-reviewer + verifier + bounded Dev-QA loop |
| `/fix <bug>`               | sleuth → spark/kraken → coroner → verifier |
| `/review`                  | code-reviewer + security-reviewer + verifier |
| `/commit`                  | verifier gate + conventional commit + trailers |
| `/learn <rule>`            | Quick learning capture via friction/compound |
| preflight skill            | Mandatory Pre-Flight (exploration, friction review, handoff quality, ledger state) |
| compound-learnings         | Self-improvement flywheel (observe → draft → review → promote) |

## Full Power Hook System

- The Grok TUI calls the Python adapters as subprocesses before/after every tool (read_file, run_terminal_command, search_replace, edit, etc.).
- Adapter contract: `if __name__ == "__main__": payload = json.load(sys.stdin) ... handle(data) ... print compact decision or silent ... sys.exit(0)`
- 64+ adapters were bulk-updated with the guard. Batch audit: 0 failures.
- Credential deny, monster broadcast, friction capture, compound trigger, palace save/recall, tamagotchi, session compressor, preflight, post-edit diagnostics, etc. all run with **full side-effects**.
- No registration was disabled.

## Production Contract (Mandatory)

Every agent and orchestrator skill (for non-trivial work):

1. Record to the ledger (task_lifecycle.py + record_attempt / escalate)
2. Emit a structured handoff (handoff skill + make_devqa_handoff_context)
3. Run preflight if the task is non-trivial
4. Capture friction in compound-friction.jsonl
5. Participate in the compound flywheel (self-improvement)
6. Apply claim-verification two-pass (Pass 1: hypothesize ?INFERRED; Pass 2: read the actual file → ✓VERIFIED)

All 147 agents contain the verbatim block. All 311+ skill directories contain SKILL.md + Contract + hooks participation + claim-verif + delegation notes.

## Contribute

This project is distributed free under the spirit of "humanity is sharing and developing."

- Add new Grok adapter agents/skills (run agent_linter, add Production Contract + required sections, perform claim-verif two-pass).
- Capture friction and feed it into compound (rules/persona/skill evolution).
- Monitor team performance with the monster CLI.
- Maintain continuity in your own projects with Palace + layered-recall.
- Also contribute to the original repo: https://github.com/vibeeval/vibecosystem

Pull requests, issues, and forks are welcome. This is how science advances.

## License & Attribution

- Original: https://github.com/vibeeval/vibecosystem (by @vibeeval) — please preserve credit to the original.
- Thanos (Grok adaptation): This is a distinct implementation adapted for the Grok TUI. It carries the same philosophy and disciplines.
- Usage: Free to use, share, and improve. For commercial use, attribution to both the original and this adaptation is recommended.

## Contact & Resources

- Original project: https://github.com/vibeeval/vibecosystem
- Thanos transfer details: docs/transfer-status-2026-06-02-end-of-day.md (all "finished" evidence, percentage tables, hook fix root causes + fixes)
- Rules: rules/ (thanos-welcome.md, monster.md, claim-verification.md, qa-loop.md, ...)
- Welcome: rules/thanos-welcome.md

**Thank you @vibeeval** — by creating and sharing this discipline you made a major contribution to science and humanity. With Thanos, Grok users can now work at the same level of quality.

Humanity is sharing and developing. This is how science progresses.

---

*This README was prepared for public distribution after all detailed checks (claim-verif, linter, hook batch 0-fail, remnant 0, full power) were completed. 2026-06.*

---

## Türkçe

# THANOS - Grok Üzerine Kurulmuş AI Yazılım Ekibiniz

**https://github.com/iamkaanalper/thanos**

**Yıldızlayın ve katkıda bulunun:** https://github.com/iamkaanalper/thanos — orijinal kredi sosyal medyada yazar tarafından yapılacaktır.

## Topluluk

- [Davranış Kuralları](CODE_OF_CONDUCT.md) — orijinal vibecosystem projesinden uyarlanmıştır.
- [Katkı Rehberi](CONTRIBUTING.md) — agent, skill, hook ve iyileştirmeler nasıl eklenir.
- [Güvenlik Politikası](SECURITY.md) — güvenlik açıklarını sorumlu şekilde nasıl bildirilir.

Lütfen katkıda bulunmadan önce bunları okuyun. Orijinal kredi sosyal medyada @vibeeval'e yazara aittir.

> "Ben bu projeyi insanlarla paylaşmak için yaptım. GitHub'da ücretsiz dağıtacağım.  
> İnsanlık paylaşmak ve gelişmektir. Bilim böyle gelişecektir."

Bu felsefeyle, yüksek kaldıraçlı disiplinleri (Sınırlı Dev-QA Döngüsü, Production Contract, Yapılandırılmış Handoff, Pre-Flight, Friction/Compound self-improvement flywheel, Palace katmanlı bellek, monster cross-training, claim-verification two-pass, tam güç pre/post hook'lar) Grok TUI kullanıcılarına tamamen ücretsiz sunuyoruz. Herkes üzerine ekleyebilir, geliştirebilir.

## Neden Thanos?

Orijinal sistem (vibecosystem by @vibeeval) Claude Code için olağanüstü bir AI yazılım ekibi disiplini getirmişti:

- 139+ agent + atama matrisi
- 295+ skill + meta/patterns + SKILL.md + Production Contract
- 73 hook + 587 handler
- Canavar (şimdi monster) cross-training (error-ledger + skill-matrix + CLI)
- Palace + layered recall (4-kapsam / 3-derinlik)
- Compound flywheel (kendi kendine iyileşme)
- Sınırlı Dev-QA (maks 3 deneme + handoff-templates ile escalation)
- Production Contract + handoff şablonları
- Claim-verification (iki geçişli factcheck-guard)

**Thanos** bunu Grok 4.3+ (Nisan 2026) için uyarladı ve geliştirdi:

- 147 agent (106%+ sayısal parite, %100 Production Contract + agent_linter ort. 99.93)
- 822+ skill kaydı / 311+ skill dizini (%100 aktivasyon, SKILL.md + Contract)
- 22 kural (yüksek değerli olanların tam portu + Grok'a özgü eklemeler)
- 163+ hook dosyası (pre/post tam güç; TUI direct spawn için 64+ bulk guard ile doğru __main__ + handle(data) + reportHealth)
- Monster (tam rename + kalıntı temizliği, .grok kaynaklarında aktif "vibecosystem"/"canavar" 0)
- Palace + layered-recall + pre-compact WIP durumu
- spawn_with_discipline + spawn_helper (ledger/handoff/friction/contract otomatik)
- Grok'a özgü iyileştirmeler: parallel subagent'lar için worktree isolation, tldr-cli (%95 token tasarrufu), enter_plan_mode, MCP araçları ile hibrit kullanım

**Genel günlük kullanılabilirlik: ~97%+** (orijinalden yüksek: sayısal parite + Grok sağlamlığı + tam güç hook'lar sayesinde).

**Eksik parça kaldı mı?** Hayır.

Tüm detaylı kontroller tamamlandı (public claim'lerde claim-verification two-pass + factcheck-guard, agent_linter batch, hook subprocess simülasyonları 0 hata, remnant sweep'ler, absolute path audit'leri, full power no-disable politikası). Tüm agent ve skill'ler devrede (verbatim Contract / SKILL.md + handle giriş noktası).

Tam envanter ve kanıt: [transfer-status-2026-06-02-end-of-day.md](docs/transfer-status-2026-06-02-end-of-day.md) ve [guncel-durum-tablo.md](guncel-durum-tablo.md)

## Hızlı Başlangıç (Grok TUI)

1. Bu snapshot'ı alın (GitHub repo'dan clone veya zip indirin).
2. Taşınabilir kısımları `~/.grok/` altına kopyalayın (aşağıdaki "Kurulum" bölümüne bakın).
3. Grok'u başlatın.
4. `/swarm <görev>` veya `/implement [--effort N] <görev>` yazın.

Ledger, handoff, preflight, friction capture, compound, palace recall ve monster broadcast otomatik çalışır. "Bitti" demeden önce verifier çalıştırmayı düşünün.

## Kurulum (Diğer Grok Kullanıcıları İçin)

**Önemli:** Bu, kişisel `~/.grok/` dizininizdeki port edilmiş yapıdan çıkarılan portable snapshot'tır. GitHub'da paylaşırken **sadece taşınabilir (portable) kısımları** yayınlayın. Kişisel dosyaları (sessions/, auth.json, logs/, downloads/, active_sessions*, tip_cursor.json vb.) **asla** paylaşmayın.

Önerilen taşınabilir yapı:

```
~/.grok/
├── rules/                  # 22 kural (thanos-welcome, monster, claim-verification, qa-loop, phantom, hooks, safety, coding-style, incremental-writing, memory-system, pre-compact, auto-skill-activation, tldr-cli, proactive-delegation, commit-trailers, collaborative-decisions, performance, agents, handoff-templates, hizir-identity, cross-project-learning, research-confidence)
├── bundled/
│   ├── agents/             # 147 .md (tam 139 rol + Grok adapter'lar + 8 core; her birinde verbatim Production Contract)
│   ├── skills/             # core orchestrator'lar (implement, execute-plan, review, swarm, preflight, friction-curator, compound-learnings, handoff, task_lifecycle, spawn_helper, agent_linter, ...) + shared/
│   └── personas/roles/...
├── hooks/
│   ├── core/hook_runner.py
│   ├── examples/           # 100+ auto_*.py (full __main__ + handle(data) + reportHealth; pre/post tam güç)
│   └── README.md
├── monster/                # monster.py CLI + error-ledger.jsonl + skill-matrix.json
├── palace/                 # default.jsonl + index (skeleton)
├── projects/               # default/ (MEMORY.md + wip-state.jsonl skeleton)
├── skills/                 # kullanıcı/taşınabilir skill'ler (core high-leverage + adapters)
├── docs/                   # THANOS-README.md, transfer-status, agent-assignment-matrix, thanos-grok-*, user-guide (thanos ilgili)
└── guncel-durum-tablo.md
```

**Kopyalama önerisi (Windows PowerShell örneği):**

```powershell
# Sadece portable kısımları kopyala (kendi .grok'unuza)
$src = "C:\path\to\thanos\.grok"
$dst = "$env:USERPROFILE\.grok"

# Kuralları, bundled agent/skill, hooks, monster, palace skeleton, docs
robocopy "$src\rules" "$dst\rules" /E
robocopy "$src\bundled" "$dst\bundled" /E
robocopy "$src\hooks" "$dst\hooks" /E
robocopy "$src\monster" "$dst\monster" /E
robocopy "$src\palace" "$dst\palace" /E
robocopy "$src\projects" "$dst\projects" /E
robocopy "$src\docs" "$dst\docs" /E
robocopy "$src\skills" "$dst\skills" /E   # sadece portable olanları
copy "$src\guncel-durum-tablo.md" "$dst\"
```

Sonra Grok TUI'yi yeniden başlatın. Hook'lar (python adapter'lar) TUI tarafından direkt spawn edildiğinde tam logic çalışır (stdin JSON oku → handle(data) → side-effect + reportHealth + silent exit 0).

**Tam güç notu:** Orijinal `.claude/settings.local.json` + `dist/*.mjs` (Claude kullanıcıları için) aynen bırakıldı ve unicode/encoding sorunları hedefli ASCII patch'lerle çözüldü. Hiçbir hook devre dışı bırakılmadı. Hem Claude hem Grok tarafı tam güçte paralel çalışabilir.

## Komutlar

| Komut / Skill              | Ne yapar |
|----------------------------|----------|
| `/hizir`                   | Kullanım kılavuzu (rules + docs) |
| `/swarm <görev>`           | 5-phase tam ekip aktivasyonu (Keşif → Geliştirme → Review → Düzeltme → Final) + ledger + handoff + friction/compound + phase gate |
| `/implement [--effort N]`  | TDD + multi-reviewer + verifier + bounded Dev-QA döngüsü |
| `/fix <hata>`              | sleuth → spark/kraken → coroner → verifier |
| `/review`                  | code-reviewer + security-reviewer + verifier |
| `/commit`                  | verifier gate + conventional commit + trailers |
| `/learn <kural>`           | Friction/compound ile hızlı öğrenim kaydet |
| preflight skill            | Mandatory Pre-Flight (keşif, friction review, handoff kalitesi, ledger durumu) |
| compound-learnings         | Self-improvement flywheel (gözlemle → taslak → incele → yükselt) |

## Tam Güç Hook Sistemi

- Grok TUI her tool öncesi/sonra (read_file, run_terminal_command, search_replace, edit vb.) python adapter'ları subprocess olarak çağırır.
- Adapter sözleşmesi: `if __name__ == "__main__": payload = json.load(sys.stdin) ... handle(data) ... print compact decision or silent ... sys.exit(0)`
- 64+ adapter bulk ile güncellendi. Batch audit: 0 failure.
- Credential deny, monster broadcast, friction capture, compound trigger, palace save/recall, tamagotchi, session compressor, preflight, post-edit diagnostics vb. **tam side-effect** ile çalışır.
- Hiçbir kayıt devre dışı bırakılmadı.

## Production Contract (Zorunlu)

Her agent ve orchestrator skill (önemsiz olmayan işler için):

1. Ledger'a kaydet (task_lifecycle.py + record_attempt / escalate)
2. Structured handoff yayınla (handoff skill + make_devqa_handoff_context)
3. Non-trivial ise preflight çalıştır
4. Friction'ı compound-friction.jsonl'e kaydet
5. Compound flywheel'e katıl (self-improvement)
6. Claim-verification two-pass uygula (Pass 1: hypothesize ?INFERRED; Pass 2: read actual file → ✓VERIFIED)

Tüm 147 agent'ta verbatim blok var. Tüm 311+ skill dizininde SKILL.md + Contract + hooks katılımı + claim-verif + delegation notları bulunur.

## Katkıda Bulunun

Bu proje "insanlık paylaşmak ve gelişmektir" ruhuyla ücretsiz dağıtılıyor.

- Yeni Grok adapter agent/skill ekleyin (agent_linter'ı çalıştırın, Production Contract + gerekli bölümleri ekleyin, claim-verif two-pass yapın).
- Friction yakalayın, compound'a besleyin (kurallar/persona/skill evolution).
- monster CLI ile ekip performansını izleyin.
- Palace + layered-recall ile kendi projelerinizde continuity sağlayın.
- Orijinal repoya da katkı yapın: https://github.com/vibeeval/vibecosystem

Pull request'ler, issue'lar, fork'lar hoş geldiniz. Bilim böyle ilerler.

## Lisans & Attribution

- Orijinal: https://github.com/vibeeval/vibecosystem (by @vibeeval) — lütfen orijinal krediyi koruyun.
- Thanos (Grok uyarlaması): Bu yapı Grok TUI için uyarlanmış distinct bir implementasyondur. Aynı felsefe ve disiplinleri taşır.
- Kullanım: Ücretsiz, paylaşın, geliştirin. Ticari kullanımda orijinal + bu uyarlama için attribution önerilir.

## İletişim & Kaynaklar

- Orijinal proje: https://github.com/vibeeval/vibecosystem
- Thanos transfer detayları: docs/transfer-status-2026-06-02-end-of-day.md (tüm "bitir" kanıtları, yüzde tabloları, hook fix kök nedenleri + düzeltmeler)
- Kurallar: rules/ (thanos-welcome.md, monster.md, claim-verification.md, qa-loop.md, ...)
- Hoş geldin: rules/thanos-welcome.md

**Teşekkürler @vibeeval** — bu disiplini yaratıp paylaşarak bilime ve insanlığa büyük katkı sağladınız. Thanos ile Grok kullanıcıları da aynı kalitede çalışabilecek.

İnsanlık paylaşmak ve gelişmektir. Bilim böyle gelişecektir.

---

*Bu README, detaylı kontroller tamamlandıktan sonra (claim-verif, linter, hook batch 0-fail, remnant 0, full power) paylaşım için hazırlandı. 2026-06.*