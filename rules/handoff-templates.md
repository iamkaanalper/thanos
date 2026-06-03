# Handoff Templates - Agent Arası İletişim Standartları (Grok Port)

Agent'lar arası mesajlarda bu şablonları kullan (handoff skill + make_devqa_handoff_context + orchestrators).

**Grok adaptation note:** .claude counterpart'ından (readonly) uyarlandı. Grok'ta handoff'lar structured (JSON-ish veya markdown) + ledger state + friction context içerir. Skill (bundled/skills/handoff/SKILL.md) executable şablonlar sağlar; bu rule dokümantasyon + enforcement. Tüm handoff'lar Production Contract'a (ledger + preflight + friction + compound) bağlanır. Hiç .claude/ touch.

## 1. Standard Handoff (İş Teslimi)

```
DURUM: <tamamlanan iş özeti>
DOSYALAR: <değişen dosyalar + satır aralıkları>
BAĞIMLILIKLAR: <önkoşullar, ledger state snapshot>
TESLİM: <ne bekleniyor, kabul kriterleri (test, review, handoff kalitesi)>
KALİTE: <test/review durumu, linter skoru, friction notları>
SONRAKİ: <bir sonraki adım + hangi agent>
```

## 2. QA Verdict: PASS

```
--topic review-result --subject "QA PASS: <task>"
--body "KARAR: PASS
KANIT: <test sonuçları, screenshot, metrik, linter 100, ledger clean>
KRİTERLER: [x] Kod kalitesi [x] Build [x] Testler [x] Security [x] Ledger/handoff
SONRAKİ: <bir sonraki adım veya commit>"
```

## 3. QA Verdict: FAIL

```
--topic review-result --priority high
--subject "QA FAIL: <task> (deneme N/3)"
--body "KARAR: FAIL
SORUN 1: [severity] <açıklama>
  BEKLENEN: <ne olmalı>
  GERÇEK: <ne oluyor>
  FIX: <ne yapılmalı>
  DOSYA: <hangi dosya:satır>
SORUN 2: ...
RETRY: Sadece listelenen sorunları düzelt, yeni özellik EKLEME. Production Contract'a sadık kal."
```

## 4. Escalation (3 Denemeden Sonra)

```
--topic escalation --priority critical
--subject "ESCALATION: <task> 3/3 başarısız"
--body "TASK: <açıklama>
GEÇMİŞ:
  Deneme 1: <ne oldu, neden fail>
  Deneme 2: <ne oldu, neden fail>
  Deneme 3: <ne oldu, neden fail>
KÖK NEDEN: <neden sürekli başarısız>
ÖNERİ: [reassign|decompose|revise|defer|accept with limitation]
ETKİ: <neyi blokluyor>
LEDGER: <current attempts + evidence chain>"
```

## 5. Bug Report

```
--topic bug-report --priority <severity>
--subject "BUG: <kısa açıklama>"
--body "NE OLUYOR: <hata açıklaması>
BEKLENEN: <doğru davranış>
TEKRAR: <nasıl reproduce edilir (adım adım)>
DOSYA: <ilgili dosyalar>
TAHMİN: <olası root cause (factcheck ile verify)>
FRICTION: <eşlik eden friction pattern>"
```

## 6. Security Finding

```
--topic security-finding --priority critical
--subject "SECURITY: <açık tipi> - <konum>"
--body "TİP: <XSS|SQLi|SSRF|Auth Bypass|Hardcoded secret|...>
KONUM: <dosya:satır>
ETKİ: <ne olabilir>
EXPLOIT: <nasıl istismar edilir>
FIX: <çözüm önerisi + Production Contract adımları>
ACİLİYET: <hemen|sprint|sonraki>
EVIDENCE: <factcheck-guard read_file sonuçları>"
```

## 7. Status Update

```
--topic status --subject "Durum: <agent> - <özet>"
--body "TAMAMLANAN: <liste>
DEVAM EDEN: <liste>
BLOCKER: <varsa + ledger state>
SONRAKİ: <plan + hangi agent/handoff>"
```

## Kurallar (Grok'ta Zorunlu)

- TÜRKÇE yaz (teknik terimler hariç).
- Body 500 karakter max (comms / handoff limiti) — kısa ve actionable tut.
- Priority doğru seç: critical sadece gerçek acil durumlar (production down, data loss, security).
- Her handoff'ta kabul kriterleri belirt (test, review, ledger clean, handoff kalitesi).
- QA FAIL'de spesifik fix talimatı ver, genel yorum YAZMA. "Sadece listelenen sorunları düzelt".
- Production Contract: Her handoff ledger state, preflight sonucu, friction notu, compound önerisi içerir.
- Factcheck: Handoff'ta "X exists/does Y" iddiası varsa, read_file + two-pass kanıtı ekle.
- Hooks: Handoff sonrası run_hook (on_handoff veya equivalent) ile compound/friction tetikle.
- Escalation: 3x FAIL sonrası ledger escalate + handoff #4 ile ilgili agent'lara veya user'a.

## Grok Entegrasyonu

- Skill: bundled/skills/handoff/SKILL.md (executable templates + make_devqa_handoff_context).
- Orchestrators: implement/SKILL.md, execute-plan/SKILL.md, swarm/orchestrator.py — mandatory handoff + ledger.
- Task Lifecycle: record_attempt + escalate otomatik handoff üretir.
- Friction/Compound: Her handoff sonrası friction capture + compound için pattern extraction.
- Spawn: spawn_helper build_spawn_context içinde handoff_ctx otomatik eklenir.

Bu rule + skill, Thanos (Grok port of the original Claude Code AI software team system) structured communication disiplinini Grok'un executable orchestrator'larına ve ledger'ına taşır. Handoff'lar sadece mesaj değil, kalite ve self-improvement sinyali üretir.