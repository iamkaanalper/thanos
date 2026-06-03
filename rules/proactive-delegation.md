# Proactive Agent Delegation (Grok Port)

Main context'i temiz tut, agent'lara delege et.

**Grok Adaptation:** Use spawn_subagent (with explore type for research, worktree isolation for parallel impl, etc.). Leverage our bundled agents and skills. Main context only does coordination, user intent, workflow choice, and summarization.

## Pattern Tespiti

| Pattern              | Sinyal                  | Aksiyon                          |
|----------------------|-------------------------|----------------------------------|
| Birden fazla iş      | "X ve Y", "ayrica"      | Paralel agent'lar öner (spawn_subagent multiple) |
| Araştırma lazım      | "nasıl", "ne", "bul"    | scout/explore veya oracle spawn et |
| Implementasyon       | "ekle", "implement et"  | /implement veya /execute-plan workflow'una yönlendir |
| Bug/sorun            | "fix", "bozuk", "çalışmıyor" | /fix workflow'una (sleuth → spark/kraken) |
| Keşfet               | "anla", "incele"        | scout / explore cagir            |

## Agent Seçimi (Grok)

| Görev                    | Kullan                          | Kullanma (düşük doğruluk riski) |
|--------------------------|---------------------------------|---------------------------------|
| Codebase keşfetme        | scout / explore                 | General (token verimsiz)       |
| Dış araştırma            | oracle                          | General                        |
| Pattern bulma            | scout                           | General                        |
| Dokümantasyon            | technical-writer / doc-updater (portlu) | General                  |

Opus veya yüksek doğruluk lazım ise, direkt araçlar (list_dir + read_file + grep) + tldr equivalents kullan.

## Main Context = Sadece Koordinasyon

**Agent'lara ver:**
- 3+ dosya okuma/analiz
- Dış araştırma
- Implementasyon (multi-file)
- Test yazma/calıstırma
- Debug (karmaşık)
- Review (code-reviewer, security-reviewer, vb.)

**Main'de tut:**
- Kullanıcı niyetini anlama
- Uygun workflow / agent seçimi (assignment-matrix'e göre)
- Agent sonuçlarını özetle
- Kullanıcıya sun
- Karar noktalarında (collaborative-decisions)

## Workflow Zincirleme (Grok)

| Biten          | Öner                              |
|----------------|-----------------------------------|
| /explore       | "/implement" veya "/build"        |
| /plan          | "/execute-plan" veya premortem    |
| /fix           | "/commit" veya verifier           |
| Araştırma      | implement / swarm                 |

## Delegasyon ZORUNLU Durumlar

Bu durumlarda MUTLAKA agent spawn et (spawn_subagent), main context'te YAPMA:

| Durum                        | Agent / Workflow                  | Neden                              |
|------------------------------|-----------------------------------|------------------------------------|
| 5+ dosya okuma/analiz        | scout / explore                   | Main context kirlenmesin           |
| Bug investigation            | sleuth (sonra spark/kraken)       | İzole debug context                |
| 3+ dosya edit                | kraken veya spark (worktree)      | Paralel çalışma + isolation        |
| Test yazma/calıstırma        | tdd-guide + arbiter / test-enforcement | Test context ayrı             |
| Security audit               | security-reviewer                 | Uzman göz                          |
| Build hatası                 | build-error-resolver              | Hızlı fix                          |
| Code review                  | code-reviewer                     | Objektif review                    |
| Dependency analiz            | migrator                          | CVE + impact analiz                |
| Tech debt tarama             | janitor                           | Codebase health                    |
| E2E / QA strategy            | e2e-runner / qa-engineer          | Uzman test disiplini               |
| External research (deep)     | oracle / harvest / pathfinder     | Dış bilgi                          |

## Main Context Limitleri

Main context SADECE bunları yapsın:
- Kullanıcı niyetini anla
- Uygun workflow/agent seç (agent-assignment-matrix + proactive rules)
- Agent sonuçlarını özetle
- Kullanıcıya sun + karar al

Main context BUNLARI YAPMASIN:
- 3'ten fazla dosya okuma (scout/explore'a ver)
- Uzun debug session'ları (sleuth'a ver)
- Multi-file edit (kraken/spark'a ver, worktree isolation ile)
- Test yazma/calıstırma (tdd-guide + arbiter/test-enforcement'a ver)
- Detaylı code review (code-reviewer'a ver)
- Derin external research (oracle/harvest/pathfinder'a ver)

## Aşırı Delege Etme

Delege etme: tek basit soru, 1-2 dosya okuma, kullanıcı direkt cevap istiyorsa, hız önemliyse (ama yukarıdaki ZORUNLU tablo her zaman öncelikli).

**ÖNEMLİ:** "Delegasyon ZORUNLU Durumlar" tablosu her zaman önceliklidir. Hız istense bile security, dependency CVE, 5+ dosya analizi, veya karmaşık bug durumlarında MUTLAKA delege et.

Grok avantajı: spawn_subagent parallel + worktree isolation ile gerçek paralel delegation mümkün. Ana context temiz kalır, context window tasarrufu + daha iyi odak.

Bu kural claim-verification, research-confidence (90% kuralı), ve Production Contract (preflight + ledger + handoff) ile birlikte uygulanır.

(Original from Claude/Thanos (Grok port of the original Claude Code AI software team system) proactive-delegation; ported with Grok spawn_subagent, worktree, explore type, bundled agents, and emphasis on main context only coordination.)
