# Collaborative Decisions (Grok Port)

Önemli tasarım ve mimari kararlarda yapılandırılmış karar alma süreci (AskUserQuestion + one-question rule ile).

**Grok adaptation note:** .claude counterpart'ından (readonly) uyarlandı. Grok'ta karar noktalarında AskUserQuestion tool kullanılır (options ile label/description/preview). EnterPlanMode + exit_plan_mode ile plan onayı. Production Contract + preflight + ledger bağlamı korunur. Hiç .claude/ touch.

## Ne Zaman Kullan

- Birden fazla geçerli yaklaşım varsa (mimari, auth, layout, tech stack, rollout).
- Kullanıcı tercihini etkileyen kararlar (geri dönüşü zor).
- UI/UX tasarım tercihleri, API tasarım, infra seçimleri.
- Agent assignment veya orchestration stratejisi.
- Ambiguity %20+ ise (research-confidence 90% kuralı ile de ilişkilendir).

## Decision Flow (Grok'ta)

```
1. Question    → Problemi/kararı net tanımla (tek soru kuralı: MAX 1 soru per turn)
2. Options     → 2-4 seçenek sun (her biri için en az 1 artı + 1 eksi; "Recommended" belirt ama dayatma yapma)
3. Decision    → Kullanıcı seçimini al (veya güçlü tahminin varsa direkt uygula + açıkla)
4. Draft       → Seçime göre implementasyon planı / kod / doküman taslağı
5. Approval    → Plan mode'da exit_plan_mode ile kullanıcı onayı al (önemli işlerde)
6. Execute     → Production Contract (preflight + ledger + handoff + friction + compound) ile ilerle
```

## AskUserQuestion Kullanım Rehberi (Grok Tool)

İyi soru örnekleri:
- "Authentication için hangi yaklaşıma öncelik verelim?" (JWT + Refresh / Session / OAuth 2.0 + PKCE)
- "Dashboard layout için hangi stil?" (Sidebar / Top nav / Bento Grid) — her option'a explanation + preview.

Kötü: "Bunu yapalım mı?" (belirsiz), "Hangisini tercih edersiniz?" (seçeneksiz), 3+ ardışık soru (momentum kaybı).

**One-Question Rule:** Belirsiz durumlarda MAX 1 soru sor. Fazlası kullanıcıyı yorar. Güçlü tahminin varsa: sormadan ilerle + kararı kaydet (memory veya task description).

## Kurallar

- Her seçenek için en az 1 artı ve 1 eksi belirt.
- Önerileni belirt ama dayatma yapma. Max 4 seçenek.
- Karar alındıktan sonra HEMEN implement et (tekrar sorma).
- Kararı kaydet (palace + compound friction veya task description).
- Trivial kararlar için KULLANMA.
- Pre-Flight + ledger: büyük kararlar (scope-risk medium+) için ledger'a "Decision: X because Y, Rejected: Z, Confidence: ..." yaz.

## Agent'lar İçin

- **architect / planner / project-manager:** Mimari + sprint kararları.
- **designer / frontend-dev / backend-dev:** UI/UX, API, component yaklaşımı.
- **devops / infra experts:** Infra, deployment, IaC seçimleri.
- **EnterPlanMode + exit_plan_mode:** Büyük belirsiz işlerde plan onayı için kullan.

## Grok Entegrasyonu

- AskUserQuestion tool: questions + options (label, description, preview).
- EnterPlanMode: "genuine ambiguity" için (multiple reasonable architectures, high-impact).
- ExitPlanMode: plan bittikten sonra kullanıcı onayı için.
- Production Contract: karar context'ini ledger/handoff'a ekle (Constraint/Rejected/Confidence/Scope-risk/Not-tested trailer'ları commit'lerde de kullan — commit-trailers.md).
- Friction/Compound: "bu karar sonrası friction" capture et (tekrar eden kararsızlık = self-learner + compound).

Bu rule, Thanos (Grok port of the original Claude Code AI software team system)'ün collaborative decision felsefesini Grok tool'ları (AskUserQuestion, plan mode) + Production Contract ile birleştirir. Kararlar şeffaf, gerekçeli ve geri alınabilir kalır.