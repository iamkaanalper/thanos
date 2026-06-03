# Auto Skill Activation (Grok Port) — ZORUNLU

BU KURAL HER SESSION'DA MÜMKÜN OLDUĞUNCA UYGULANIR. KULLANICININ HATIRLAMASINA GEREK YOK.

Grok adaptation: Partial auto-activation is already wired via:
- project-detect skill (tech stack detection)
- hooks (on_run_completion, on_friction_recorded, on_agent_spawn, auto_* handlers)
- compound-learnings + friction-curator (self-improvement)
- explicit calls in orchestrators (implement/execute-plan/swarm → verifier on done, self-learner on error, code-reviewer patterns)
- memory-palace / recall for project context
- strategist-like behavior via architect/planner when big scope

Full "every edit auto code-reviewer" is hook-dependent and evolving. We use the spirit: proactive, low-friction activation of the right specialist without user remembering names.

---

## SESSION BAŞLANGICI (Her konuşmada ilk iş)

Kullanıcı bir proje dizininde çalışıyorsa, OTOMATİK yap:

1. **Proje tespiti**: package.json, go.mod, pyproject.toml, tsconfig.json, manage.py, Cargo.toml, *.sln vb. kontrol et (project-detect skill).
2. **CLAUDE.md / AGENTS.md / .grok/ docs kontrolü**: Yoksa "Proje talimatı (CLAUDE.md veya .grok/docs) oluşturalım mı?" diye sor (hafif dokunuş).
3. **Tech stack'e göre skill'leri / agent'ları aktive et** (aşağıdaki mapping + bundled/agents).
4. **Memory recall**: project ile ilgili geçmiş öğrenimleri getir (memory-palace + recall skill + compound).
5. **@strategist / architect arka planda**: Quick analysis + risk pulse (özellikle büyük işlerde).
6. **Context brief**: "Nerede kalmıştık?" (compass analog via sessions/ + palace + git log/stash/WIP).

---

## KOD YAZILDIĞINDA / EDİT EDİLDİĞİNDE (Otomatik tetiklenir)

| Olay                        | Otomatik Aksiyon                          | Kullanıcıya Sor? |
|-----------------------------|-------------------------------------------|------------------|
| Kod yazıldı / edit edildi   | @code-reviewer (veya reviewer) çağır     | HAYIR, direkt    |
| Test yazılmadı              | "Test yazalım mı?" (tdd-guide veya test-enforcement) | EVET     |
| console.log / debug kaldı   | Uyar ve temizle                           | HAYIR            |
| Hardcoded secret görüldü    | DURDUR, uyar (security-reviewer)          | HAYIR            |
| Build fail etti             | @build-error-resolver çağır               | HAYIR            |
| Type error                  | Düzelt (build-error-resolver type mode)   | HAYIR            |
| Test data lazım             | @mocksmith çağır                          | HAYIR            |
| Dependency CVE/upgrade      | @migrator çağır                           | HAYIR            |
| Kritik dosya değişti (K8s, Terraform, GraphQL schema vb.) | İlgili expert (kubernetes-expert, terraform-expert, graphql-expert) | HAYIR |
| i18n / a11y / feature flag / config / schema değişti | İlgili specialist (i18n-expert, accessibility-auditor, feature-flag-expert, config-validator, schema-validator) | HAYIR |

---

## FEATURE / İŞ TAMAMLANDIĞINDA (Otomatik tetiklenir)

Kullanıcı "bitti", "tamam", "ok", "done", "ship it" gibi bir şey dediğinde:

1. **@verifier** çağır (build + test + lint + security + ledger/handoff checks).
2. Verifier PASS verirse: "Commit yapalım mı? (önce son bir smoke)" diye sor.
3. Verifier FAIL verirse: Sorunları listele, düzelt (veya bounded retry).

---

## HATA YAPILDIĞINDA (Otomatik tetiklenir)

Herhangi bir hata olduğunda (test fail, build fail, runtime error, agent fail):

1. **@self-learner** çağır.
2. İlgili kuralı / friction'ı kaydet (CLAUDE.md analog + .grok memory/palace + compound-friction).
3. "Bu hatadan şu kuralı öğrensek mi?" şeklinde kullanıcıya bildir (eğer yüksek sinyal).

---

## BUG FIX İSTENDİĞİNDE (Otomatik tetiklenir)

Kullanıcı "bug", "hata", "çalışmıyor", "broken", "fix" dediğinde:

**Küçük bug (tek dosya, low-risk):**
1. **@sleuth** çağır (investigate).
2. Root cause bulununca **@spark** ile düzelt.
3. **@verifier** ile kontrol et.
4. Fix sonrası **@coroner** çağır (aynı hata başka yerde var mı? pattern propagation).

**Büyük / karmaşık bug:**
1. **@sleuth** (investigate).
2. Root cause → **@kraken** (TDD fix) veya phoenix (refactor).
3. **@arbiter** / **@test-enforcement** ile test doğrula.
4. **@verifier** ile son kontrol.
5. Fix sonrası **@coroner** (post-mortem + propagation).

**Bug reproduce edilemiyorsa:**
1. **@replay** çağır (reproduce adımları + flaky analizi).
2. Reproduce edildikten sonra yukarıdaki akışa devam.

**Acil / production bug (HOTFIX):**
1. **@sleuth** (hızlı critical kontroller).
2. **@spark** minimal fix.
3. **@verifier** (sadece build + critical test).
4. Hemen commit + deploy.
5. Sonra @self-learner ile öğren + compound'a kaydet.

---

## BÜYÜK İŞ İSTENDİĞİNDE (Otomatik tetiklenir)

Kullanıcı büyük scope'lu bir iş istediğinde (yeni feature, modül, sistem, migration):

1. **Plan mode'a gir** (enter_plan_mode) eğer ambiguity yüksekse.
2. **@architect** (veya planner) ile plan çiz.
3. Plan onaylanınca **@kraken** (veya uygun implementer) ile implement et.
4. Swarm gerekiyorsa `/swarm` workflow'unu başlat (5-phase + per-track ledger + Dev-QA loop).

---

## COMMIT / RELEASE İSTENDİĞİNDE (Otomatik tetiklenir)

1. Önce **@verifier** çalıştır (build + test + lint + security + Production Contract checks).
2. PASS ise commit yap (önce user onayı).
3. FAIL ise durdur, sorunları göster.

---

## REVIEW İSTENDİĞİNDE (Otomatik tetiklenir)

1. **@code-reviewer** (genel kalite).
2. Auth/data/secret işlerinde **@security-reviewer** da ekle.
3. DB / schema işlerinde **@database-reviewer** da ekle.
4. E2E / test ağırlıklı ise **@qa-engineer** + **@e2e-runner** / **@arbiter** dahil et.

---

## TECH STACK → SKILL / AGENT MAPPING (Grok .grok/ adapted)

### Node.js / TypeScript
- coding-standards, tdd-workflow, frontend-patterns, backend-patterns
- Agents: frontend-dev, backend-dev (via patterns + implementer), graphql-expert, etc.

### Python
- python-patterns, python-testing, django-patterns + django-security + django-tdd (varsa)
- Agents: data-analyst, etc.

### Go
- golang-patterns, golang-testing
- go-build-resolver, go-reviewer (planlı)

### Java / Spring Boot
- springboot-patterns, springboot-security, springboot-tdd, jpa-patterns

### Database
- postgres-patterns, mongodb-patterns, vector-db-patterns, etc.
- database-reviewer agent (schema)

### GraphQL / Realtime / Messaging
- graphql-patterns, websocket-patterns, kafka-patterns
- graphql-expert, kafka-expert, etc.

### Infrastructure / Cloud
- terraform-patterns, kubernetes-patterns, aws-patterns, gcp-patterns, azure-patterns
- terraform-expert, kubernetes-expert, aws-expert, etc.

### Redis / Caching / Observability
- redis-patterns, caching-patterns, observability, tracing-patterns, prometheus-patterns
- redis-expert, observability-expert, etc.

### Security / Compliance
- sast-patterns, secret-patterns, gdpr-compliance, hipaa-compliance, soc2-compliance, etc.
- security-reviewer, compliance-expert

### Testing Deep
- test-strategy, test-enforcement, property-based-testing, contract-testing-patterns, mutation-testing, load-testing-patterns, e2e (via e2e-runner)
- tdd-guide, arbiter, qa-engineer, e2e-runner, verifier

### Other high-value
- experiment-loop, skill-evolution, memory-palace, agent-tamagotchi, design, pr-babysit, friction-curator, preflight, compound-learnings, handoff
- harvest-* (crawling), browser-automation, etc.

**Grok Note:** Mapping is best-effort and grows with bundled/skills + hooks. When a new high-frequency pattern appears, we add the skill/agent and update this rule via compound.

---

Auto-activation'ın amacı: Kullanıcı "şu ajanı çağır" diye hatırlamak zorunda kalmasın. Sistem proaktif olsun, kalite ve hız artsın.

Bu kural claim-verification, qa-loop, hooks, compound ve Production Contract ile birlikte uygulanır.

(Original Thanos (Grok port of the original Claude Code AI software team system) kuralından uyarlandı. Grok'ta hook'lar, executable orchestrators ve compound flywheel ile kısmen otomatik hale getirildi. Tam "her edit'te otomatik reviewer" derinliği hook kapsamına ve adoption'a bağlıdır.)
