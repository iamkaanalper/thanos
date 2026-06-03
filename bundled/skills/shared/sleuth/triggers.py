"""
Sleuth tetikleyici kelimeler ve ağırlıkları.

Bu dosya, routing mantığının temelini oluşturur.
Gerektiğinde kolayca güncellenebilir.
"""

# Yüksek ağırlıklı (Strong) tetikleyiciler → Dedicated Sleuth ajanını öner
STRONG_TRIGGERS = {
    "sleuth": 5.0,
    "sleuth modunda": 5.0,
    "kök neden": 4.5,
    "kök nedeni": 4.5,
    "evidence chain": 5.0,
    "repro ile incele": 4.5,
    "bug'ı kökünden": 5.0,
    "gerçek nedeni bul": 4.5,
    "sistematik debug": 4.0,
    "sleuth disiplini": 4.5,
}

# Orta ağırlıklı (Medium) tetikleyiciler
MEDIUM_TRIGGERS = {
    "kök nedenini bul": 3.0,
    "root cause": 3.0,
    "derin araştırma": 2.5,
    "reproduction adımlarını netleştir": 3.0,
    "evidence ile": 2.5,
}

# Bağlamsal güçlendiriciler (Boosters)
BOOSTERS = {
    "intermittent": 1.5,
    "nadir repro": 1.5,
    "concurrency": 1.5,
    "race condition": 2.0,
    "state management": 1.5,
    "önceki fix'ler işe yaramadı": 2.0,
    "önceki araştırmalar yetersiz": 2.0,
    "flaky": 1.5,
    "aralıklı": 1.3,
    "düzensiz": 1.2,
    "timing": 1.2,
    "zamanlama": 1.2,
}