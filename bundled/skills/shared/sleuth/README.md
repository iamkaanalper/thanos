# Sleuth Router Module

Bu modül, Sleuth ajanının veya Sleuth persona katmanının ne zaman önerileceğini belirleyen basit ama etkili bir routing sistemi sağlar.

## Ne İşe Yarar?

Sleuth davranışı iki şekilde aktif edilebilir:
- Dedicated `sleuth` ajanı olarak
- `general-purpose` üzerine `sleuth` persona katmanı olarak

Bu modül, verilen bir göreve göre hangisinin daha uygun olduğunu skorlayarak önerir.

## Dosya Yapısı

- `router.py` — Ana `get_sleuth_recommendation()` fonksiyonu
- `triggers.py` — Tetikleyici kelimeler ve ağırlıkları
- `prompts.py` — Hazır Sleuth disiplin prompt blokları
- `normalize.py` — Türkçe karakter normalizasyonu (_normalize_text) — Post-MVE Item 1
- `__init__.py` — Kolay import için

## Temel Kullanım

```python
from bundled.skills.shared.sleuth.router import get_sleuth_recommendation

rec = get_sleuth_recommendation(
    description="Bu state corruption bug'ını kök nedenini bulmam lazım",
    context="Intermittent ve race condition şüphesi var"
)

print(rec["recommended_mode"])        # "dedicated_agent" | "persona_layer" | "none"
```

## Türkçe / i18n Desteği (Post-MVE Item 1)

Router, Türkçe karakterleri otomatik normalize eder (`normalize.py`).

Bu sayede "kök neden", "bug'ını", "şüphesi" gibi girdiler bile güçlü skor üretir (Senaryo A live test'te görülen 0 skor sorunu çözüldü).

Regression test: `router_test.py` (normalize + Senaryo A tarzı Türkçe input).
print(rec["confidence"])              # "high" | "medium" | "low"
print(rec["suggested_subagent_type"])
print(rec["suggested_persona"])
print(rec["prompt_addition"])         # Persona katmanı öneriliyorsa kullanılabilir
```

## Önerilen Kullanım Yerleri

- Ana orchestrator veya intent classification katmanında
- `pr-babysit` gibi karmaşık teşhis içeren workflow'larda
- Gelecekteki "fix", "debug" veya "investigate" wrapper skill'lerinde
- Herhangi bir yerde "derin kök neden araştırması" gerektiğinde karar desteği olarak

## Geliştirme Notu

Bu modül kasıtlı olarak küçük, bağımsız ve kolay genişletilebilir tutulmuştur. 
Gerektiğinde daha gelişmiş bir intent router sistemine entegre edilebilir.