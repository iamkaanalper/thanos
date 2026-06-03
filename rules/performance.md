# Performance & Model Selection (Grok Port)

## Model Kuralları (Grok)

- Agent spawn'larken `model` parametresini **OMIT ET** (parent'tan inherit eder — spawn_subagent çağrılarında model belirtme).
- Haiku KULLANMA. Hiçbir agent'ta haiku kullanma (düşük doğruluk riski).
- Opus: karmaşık mimari kararlar, araştırma, analiz, planlama (enter_plan_mode + architect/planner).
- Sonnet (veya eşdeğer güçlü model): ana geliştirme, orchestration, implement, review, swarm execution.
- Grok context: subagent'lar parent model'i inherit eder; background=true için uzun işlerde dikkat et.

## Context Window

Son %20'ye girme (kompres uyarısı):
- Büyük refactoring, multi-file feature, karmaşık debug, uzun swarm.
- Bu tarz işleri agent'lara delege et (spawn_subagent + worktree isolation ile paralel).
- Pre-compact: palace + session-compression + layered-recall kullan (ACDE format, 10-30x reduction).
- compass / palace recall ile context recovery.

## Ultrathink + Plan Mode (Grok)

Karmaşık işlerde:
1. Plan Mode aç (enter_plan_mode) — ambiguity yüksekse veya high-impact kararlar.
2. Split role sub-agent'lar kullan (e.g. architect + planner + profiler; reviewer + security-reviewer).
3. Birden fazla tur kritik yap (pre-flight + ledger + handoff).
4. exit_plan_mode ile kullanıcı onayı al (collaborative-decisions kuralı + AskUserQuestion).

## Build Hatası

1. **build-error-resolver** agent çağır (veya go-build-resolver Python/Go için).
2. Hata mesajlarını analiz et (tldr diagnostics, run_terminal_command ile build log).
3. Parçalı düzelt, her fix sonrası verify et (verifier + linter + test).
4. Friction capture et → compound için öğrenim (tekrar eden build hataları = self-learner + rule update).

## Grok Özel Notlar

- spawn_helper.build_spawn_context + spawn_with_discipline kullanırken model inheritance otomatik.
- Uzun context için: tldr-cli (structure, calls, impact, dead code), memory-palace recall, session-compression hook.
- Cost/performance: token-budget skill, cost-tracker analog.
- Agent'lar için: worktree isolation producer'larda (kraken, phoenix, implementer vb.) gerçek paralel + isolation.
- Pre-Flight zorunlu: context window riski olan işlerde exploration + friction review yap.
- Claim-verification: büyük işlerde factcheck-guard kullan, grep-only claim'lerden kaçın (80% false claim riski).

Bu kural, Thanos (Grok port of the original Claude Code AI software team system) performans disiplinini Grok'un subagent, plan-mode, tldr, palace ve executable orchestrator'larına uyarlar. Asla context window'u zorlama — delege et ve disiplinli ilerle.