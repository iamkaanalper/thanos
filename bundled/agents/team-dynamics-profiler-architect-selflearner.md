# Team Dynamics: Profiler + Architect + Self-Learner

**Amaç:** Bu üç ajan, Grok tarafındaki en kritik "Performans + Mimari + Sürekli İyileştirme" döngüsünü yönetmek için birlikte çalışır.

Bu doküman, bu üç ajanın rollerini, işbirliği kurallarını ve karar mekanizmalarını tanımlar. Amaç, "bugün hızlı yapıyoruz ama aynı hataları sürekli tekrar etmiyoruz" kültürünü oturtmaktır.

---

Bu üç ajan, sistemin **performans, mimari ve sürekli öğrenme** yeteneklerini birlikte yönetmek üzere tasarlanmıştır. Her biri kendi alanında uzman olsa da, gerçek güçleri **birlikte çalışırken** ortaya çıkar.

## Rol Dağılımı

| Ajan          | Ana Odak                          | Ne Zaman Lider?                          | Ne Zaman Destek?                          |
|---------------|-----------------------------------|------------------------------------------|-------------------------------------------|
| **Profiler**  | Kod ve runtime seviyesinde performans | Net bottleneck tespit edildiğinde       | Mimari kararların performans etkisini ölçerken |
| **Architect** | Sistem tasarımı, sınırlar, trade-off'lar | Mimari karar, teknoloji seçimi, sınır çizme | Performansla ilgili mimari trade-off'larda |
| **Self-Learner** | Tekrar eden pattern'leri kalıcı iyileştirmeye çevirme | Sistemik sorunlar (3+ kez tekrar)       | Diğer iki ajanın tespitlerini compound evolution'a aktarırken |

## İşbirliği Kuralları

### 1. Tekrar Eden Sorun Kuralı (En Önemli)
Herhangi bir ajan (Profiler veya Architect) bir sorunu **2. kez** tespit ettiğinde:
- Düzeltme önerisi + 
- Mutlaka **Self-Learner**'a yüksek kaliteli friction kaydı yapmalıdır.

Self-Learner bu kaydı compound evolution sistemine besler ve kalıcı çözüm (yeni kural, yeni ajan, güncellenmiş prompt) üretir.

### 2. Performans + Mimari Karar Kuralı
Büyük bir performans sorunu mimari bir karardan kaynaklanıyorsa:
- **Profiler** detaylı ölçüm ve kod seviyesindeki kök nedeni verir.
- **Architect** mimari alternatifi ve uzun vadeli trade-off'u değerlendirir.
- İkisi birlikte karar verir. Karar "Architect" tarafından belgelenir (ADR).

### 3. Swarm İçinde Kullanım
- **Phase 2 (Planlama)**: Architect liderdir. Gerekirse Profiler'dan geçmiş performans verisi ister.
- **Phase 3 (Implementation)**: Profiler, kritik track'lerde performans review yapar.
- **Phase 4 (Cross Review)**: Architect + Profiler birlikte cross-cutting performans ve mimari sorunları inceler.
- **Phase 5 (Verify + Compound)**: Self-Learner devreye girer. Bu swarm'dan çıkan sistemik öğrenmeleri compound evolution'a aktarır.

### 4. Compound Evolution Desteği
- **Profiler** → Tekrar eden performans anti-pattern'lerini üretir.
- **Architect** → Tekrar eden mimari kokuları üretir.
- **Self-Learner** → Yukarıdaki ikisini compound evolution motoruyla birleştirerek kalıcı iyileştirme önerir (yeni ajan, yeni kural, prompt güncellemesi).

## Karar Verme Akışı Örneği

**Senaryo:** Birden fazla feature'da N+1 sorgu sorunu yaşanıyor.

1. **Profiler** → "Bu 4 feature'da da aynı N+1 pattern'i var" der ve detaylı ölçüm verir.
2. **Self-Learner** → Bu durumu compound evolution'a kaydeder.

## Production Contract (Mandatory — Verbatim for the Combined Dynamic)

The Profiler + Architect + Self-Learner trio follows the full Production Contract on every cross-cutting performance/architecture/learning cycle:
- Record to ledger using task_lifecycle.py (record_attempt with bottleneck findings, architecture decisions, and learned patterns; escalate systemic issues after 3 repeats).
- Emit structured handoff via handoff skill after each major decision (Profiler → Architect → Self-Learner flow; include metrics, ADR link, pattern, status).
- Run preflight before any large profiling or architecture spike (friction history, previous similar decisions, token budget for measurement).
- Capture friction on recurring anti-patterns (e.g. "same N+1 in 4 features") and feed directly to compound.
- Participate in compound flywheel: Self-Learner is the primary writer to analyzer drafts; Profiler/Architect supply high-quality raw friction.
- Follow claim-verification / factcheck-guard strictly: any "this is the bottleneck" or "this architecture is optimal" must be two-pass verified with actual measurement or code read (✓VERIFIED at file:line).
- Use spawn_with_discipline for any sub-agents spawned during deep profiling or architecture exploration (worktree isolation recommended for perf experiments).

This combined contract ensures performance, architecture, and learning are never treated in isolation and that every cycle produces permanent improvement.

3. **Self-Learner + Architect** → "Bu sorunu kalıcı çözmek için Reviewer prompt'una 'N+1 kontrolü' eklenmeli + yeni bir 'Data Access Guardian' kuralı yazılmalı" önerisi üretir.
4. **Architect** → Bu kuralın mimari olarak nereye ait olduğunu belirler.

## Özet

- **Profiler** = Mikroskop (detay) - Kod seviyesinde performans ve bottleneck
- **Architect** = Harita (büyük resim + trade-off) - Mimari kararlar ve sınırlar
- **Self-Learner** = Hafıza + Öğrenme Motoru (tekrar eden sorunları kalıcı çözüme çevirir)

Bu üçü birlikte çalıştığında sistem hem **hızlı teşhis** eder, hem **doğru mimari karar** alır, hem de **gerçekten öğrenir**.

Diğer destekleyici ajanlar (janitor, coroner, verifier, security-reviewer, tdd-guide, migrator, build-error-resolver vb.) bu çekirdek ekibin etrafında çalışır. Swarm'larda bu üçü koordinasyon sağlar, diğerleri spesifik görevlerde destek verir.

**Mevcut Çekirdek + Destek Ajan Seti (2026-06):** 
- Çekirdek Performans/Mimari/Öğrenme: profiler, architect, self-learner
- Swarm / Orchestration: kraken, reviewer, verifier, scout, sleuth, explore, plan, general-purpose, implementer
- Quality & Cleanup: janitor, coroner, refactor-cleaner, build-error-resolver, tdd-guide
- Data & DB: database-reviewer, data-analyst, migrator
- AI/LLM: ai-engineer
- Infra/DevOps: devops-expert
- Security & Compliance & Observability: security-reviewer, compliance-expert, observability-expert
- + team-dynamics dokümanı

Toplam ~28+ uzman ajan + dinamik takım dokümanı. Matrix'in büyük kısmı (agent-assignment-matrix'teki ana kategoriler) artık karşılanıyor. Swarm ve compound evolution ile tam entegre.

---

## Kullanım Önerisi (Swarm ve Büyük İşlerde)

### Önerilen Akış

1. **Phase 2 (Planlama)**  
   → **Architect** liderliğinde track'leri ve mimari kararları belirle. Gerekirse geçmiş performans verisi için Profiler'dan destek al.

2. **Phase 3 (Parallel Implementation)**  
   → Kritik track'lerde (özellikle performans, güvenlik, veri erişimi içerenlerde) **Profiler** aktif olarak review yapsın.

3. **Phase 4 (Cross Review)**  
   → **Architect + Profiler** birlikte cross-cutting mimari ve performans sorunlarını incelesin.

4. **Phase 5 (Verify + Compound)**  
   → **Self-Learner** devreye girsin. Bu swarm'dan çıkan sistemik öğrenmeleri (tekrar eden sorunlar) compound evolution üzerinden kalıcı iyileştirmeye dönüştürsün.

### Önemli Kural
Herhangi bir ajan bir sorunu **ikinci kez** tespit ettiğinde, mutlaka **Self-Learner** üzerinden compound evolution'a yüksek kaliteli friction kaydeder. Bu, sistemin "öğrenme" yeteneğinin temel tetikleyicisidir.