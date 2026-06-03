# THANOS - Your AI software team. Built on Grok

**https://github.com/iamkaanalper/thanos**

**Star & contribute:** https://github.com/iamkaanalper/thanos — original credit on social media by the author.

## Community

We follow a [Code of Conduct](CODE_OF_CONDUCT.md) adapted from the original vibecosystem project. Please read it before contributing.

> Bu repo, Grok TUI kullanıcıları için ücretsiz dağıtılan portable snapshot'tır.  
> Geliştirme .grok/ kurulumunda devam eder; burası yayın için temizlenmiş halidir.

> "Ben bu projeyi insanlarla paylaşmak için yaptım. GitHub'da ücretsiz dağıtacağım.  
> İnsanlık paylaşmak ve gelişmektir. Bilim böyle gelişecektir."

Bu felsefeyle, yüksek kaldıraçlı disiplinleri (Bounded Dev-QA Loop, Production Contract, Structured Handoff, Pre-Flight, Friction/Compound self-improvement flywheel, Palace layered memory, monster cross-training, claim-verification two-pass, tam güç pre/post hooks) Grok TUI kullanıcılarına ücretsiz olarak sunuyoruz. Herkes üzerine ekleyebilir, geliştirebilir.

## Neden Thanos?

Orijinal sistem (vibecosystem by @vibeeval) Claude Code için muhteşem bir AI yazılım ekibi disiplini getiriyordu:
- 139+ agent + assignment matrix
- 295+ skill + meta/patterns
- 73 hook + 587 handler
- Canavar (şimdi monster) cross-training
- Palace + layered recall
- Compound flywheel
- Bounded Dev-QA (max 3 retry + escalation)
- Production Contract + handoff templates
- Claim-verification (two-pass factcheck)

**Thanos** bunu Grok 4.3+ için uyarladı:
- 147 agent (106%+ count parity, 100% Production Contract + linter 99.93 avg)
- 311 skill dizini, 609+ .md (100% activation)
- 22 kural (yüksek değerli olanların tam portu)
- 161+ hook dosyası (pre/post tam güç, 64+ bulk guard ile TUI direct spawn'da handle(data) + side-effect çalışır)
- Monster (tam rename + purge, 0 remnant)
- Palace + layered-recall + pre-compact WIP
- spawn_with_discipline + spawn_helper (ledger/handoff/friction/contract otomatik)
- Grok'a özgü iyileştirmeler: worktree isolation, tldr-cli entegrasyonu, enter_plan_mode, MCP araçları ile hibrit

**Genel günlük kullanılabilirlik: ~97%+** (orijinalin üstünde count + Grok robustness + hook tam güç ile).

**Eksik parça kaldı mı?** Hayır.  
Detaylı kontroller (claim-verification two-pass + factcheck-guard, agent_linter batch 99.93, hook batch simülasyon 0 failure, remnant sweep 0 aktif "vibecosystem"/"canavar" in .grok sources, full power no-disable) tamamlandı. Tüm agent ve skill "devreye" (Contract/SKILL.md + handle).

Tam envanter ve kanıt: [transfer-status-2026-06-02-end-of-day.md](docs/transfer-status-2026-06-02-end-of-day.md) ve [guncel-durum-tablo.md](guncel-durum-tablo.md)

## Hızlı Başlangıç (Grok TUI)

1. Bu snapshot'ı alın (GitHub repo'dan clone veya zip).
2. Taşınabilir kısımları `~/.grok/` altına kopyalayın (aşağıdaki "Kurulum" bölümüne bakın).
3. Grok'u başlatın.
4. `/swarm <görev>` veya `/implement [--effort N] <görev>` yazın.

Ledger, handoff, preflight, friction capture, compound, palace recall, monster broadcast otomatik çalışır. "Bitti" demeden önce verifier düşünün.

## Kurulum (Diğer Grok Kullanıcıları İçin)

**Önemli:** Bu, sizin kişisel `~/.grok/` dizininizin içindeki port edilmiş yapıdır. GitHub'da paylaşırken **sadece taşınabilir (portable) kısımları** yayınlayın. Kişisel dosyaları (sessions/, auth.json, logs/, downloads/, active_sessions*, tip_cursor.json vb.) **asla** paylaşmayın.

Taşınabilir yapı (önerilen):

```
~/.grok/
├── rules/                  # 22 kural (thanos-welcome, monster, claim-verification, qa-loop, phantom, hooks, safety, coding-style, incremental-writing, memory-system, pre-compact, auto-skill-activation, tldr-cli, proactive-delegation, commit-trailers, collaborative-decisions, performance, agents, handoff-templates, hizir-identity, cross-project-learning, research-confidence)
├── bundled/
│   ├── agents/             # 147 .md (tam 139 rol + Grok adapter'lar + 8 core; her birinde verbatim Production Contract)
│   ├── skills/             # 61 (implement, execute-plan, review, swarm, preflight, friction-curator, compound-learnings, handoff, task_lifecycle, spawn_helper, agent_linter, friction, vb. + shared/)
│   └── personas/roles/...
├── hooks/
│   ├── core/hook_runner.py
│   ├── examples/           # 100+ auto_*.py (full __main__ + handle(data) + reportHealth; pre/post tam güç)
│   └── README.md
├── monster/                # monster.py CLI + error-ledger.jsonl + skill-matrix.json
├── palace/                 # default.jsonl + index (skeleton)
├── projects/               # default/ (MEMORY.md + wip-state.jsonl skeleton)
├── skills/                 # Kullanıcı/taşınabilir skill'ler (core high-leverage + adapters)
├── docs/                   # THANOS-README.md, transfer-status, agent-assignment-matrix, thanos-grok-*, user-guide (thanos ilgili)
└── guncel-durum-tablo.md
```

**Kopyalama önerisi (Windows PowerShell örneği):**

```powershell
# Sadece portable kısımları kopyala (kendi .grok'unuza)
$src = "C:\path\to\thanos-port\.grok"
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

Sonra Grok TUI'yi yeniden başlat. Hook'lar (python adapter'lar) TUI tarafından direkt spawn edildiğinde tam logic çalışır (stdin JSON oku → handle(data) → side-effect + reportHealth + silent exit 0).

**Tam güç notu:** Orijinal `.claude/settings.local.json` + `dist/*.mjs` (Claude kullanıcıları için) aynen bırakıldı ve unicode patch'lerle encoding sorunu çözüldü. Hiçbir hook devre dışı bırakılmadı. Hem Claude hem Grok tarafı tam güçte paralel çalışabilir.

## Komutlar

| Komut / Skill              | Ne yapar |
|----------------------------|----------|
| `/hizir`                   | Kullanım kılavuzu (rules + docs) |
| `/swarm <task>`            | 5-phase tam ekip aktivasyonu (Kesif → Geliştirme → Review → Düzeltme → Final) + ledger + handoff + friction/compound + phase gate |
| `/implement [--effort N]`  | TDD + multi-reviewer + verifier + bounded Dev-QA döngüsü |
| `/fix <bug>`               | sleuth → spark/kraken → coroner → verifier |
| `/review`                  | code-reviewer + security-reviewer + verifier |
| `/commit`                  | verifier gate + conventional commit + trailers |
| `/learn <kural>`           | Friction/compound ile hızlı öğrenim kaydet |
| preflight skill            | Mandatory Pre-Flight (exploration, friction review, handoff kalitesi, ledger state) |
| compound-learnings         | Self-improvement flywheel (observe → draft → review → promote) |

## Tam Güç Hook Sistemi

- Grok TUI her tool öncesi/sonra (read_file, run_terminal_command, search_replace, edit vb.) python adapter'ları subprocess olarak çağırır.
- Adapter'lar: `if __name__ == "__main__": payload = json.load(sys.stdin) ... handle(data) ... print compact decision or silent ... sys.exit(0)`
- 64+ adapter bulk ile güncellendi. Batch audit: 0 failure.
- Credential deny, monster broadcast, friction capture, compound trigger, palace save/recall, tamagotchi, session compressor, preflight, post-edit diagnostics vb. **tam side-effect** ile çalışır.
- Hiçbir kayıt devre dışı bırakılmadı.

## Production Contract (Zorunlu)

Her agent ve orchestrator skill (non-trivial iş için):

1. Ledger'a kaydet (task_lifecycle.py + record_attempt / escalate)
2. Structured handoff yayınla (handoff skill + make_devqa_handoff_context)
3. Non-trivial ise preflight çalıştır
4. Friction'ı compound-friction.jsonl'e kaydet
5. Compound flywheel'e katıl (self-improvement)
6. Claim-verification two-pass uygula (Pass 1: hypothesize ?INFERRED; Pass 2: read actual file → ✓VERIFIED)

Tüm 147 agent'ta verbatim blok var. Tüm 311 skill dir'inde SKILL.md + Contract + hooks + claim-verif + delegation.

## Katkıda Bulunun

Bu proje "insanlık paylaşmak ve gelişmektir" ruhuyla ücretsiz dağıtılıyor.

- Yeni Grok adapter agent/skill ekleyin (agent_linter'ı çalıştırın, Production Contract + sections ekleyin, claim-verif two-pass yapın).
- Friction yakalayın, compound'a besleyin (kurallar/persona/skill evolution).
- monster CLI ile ekip performansını izleyin.
- Palace + layered-recall ile kendi projelerinizde continuity sağlayın.
- Orijinal repoya da katkı yapın: https://github.com/vibeeval/vibecosystem

Pull request'ler, issue'lar, fork'lar hoş geldiniz. Bilim böyle ilerler.

## Lisans & Attribution

- Orijinal: https://github.com/vibeeval/vibecosystem (by @vibeeval) — lütfen orijinal krediyi koruyun.
- Thanos (Grok port): Bu yapı Grok TUI için uyarlanmış distinct implementasyondur. Aynı felsefe ve disiplinleri taşır.
- Kullanım: Ücretsiz, paylaşın, geliştirin. Ticari kullanımda orijinal + bu port attribution önerilir.

## İletişim & Kaynaklar

- Orijinal proje: https://github.com/vibeeval/vibecosystem
- Thanos transfer detayları: .grok/docs/transfer-status-2026-06-02-end-of-day.md (tüm "bitir" kanıtları, % tabloları, hook fix root cause + fix'ler)
- Kurallar: .grok/rules/ (thanos-welcome.md, monster.md, claim-verification.md, qa-loop.md ...)
- Hoş geldin: .grok/rules/thanos-welcome.md

**Teşekkürler @vibeeval** — bu disiplini yaratıp paylaşarak bilime ve insanlığa büyük katkı sağladınız. Thanos ile Grok kullanıcıları da aynı kalitede çalışabilecek.

İnsanlık paylaşmak ve gelişmektir. Bilim böyle gelişecektir.

---

*Bu README, detaylı kontroller tamamlandıktan sonra (claim-verif, linter, hook batch 0 fail, remnant 0, full power) paylaşım için hazırlandı. 2026-06.*