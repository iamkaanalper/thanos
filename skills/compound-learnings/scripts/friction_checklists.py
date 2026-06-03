"""
friction_checklists.py

Faz 2 — Dinamik Friction Checklist Modülü

Ledger'dan gelen friction pattern'lerinin kategorisine göre
prompt'lara enjekte edilecek checklist metinlerini merkezi olarak tutar.

Bu dosya compound-learnings sisteminin bir parçasıdır.
"""

from typing import Dict, List

# Kategori bazlı checklist'ler
# Yeni kategori eklendiğinde sadece buraya ekleyin.
CHECKLISTS: Dict[str, str] = {
    "handoff": """
## Extra Focus: Handoff Discipline
- Her boundary'de (implement → review, PR → PR, phase → phase) yapılandırılmış handoff kullan.
- Context'i net ve eksiksiz aktar. Vague "devam et" tarzı geçiş yapma.
- Handoff template'lerini (`~/.grok/skills/handoff/SKILL.md`) takip et.
""".strip(),

    "factcheck": """
## Extra Focus: Factcheck-Guard
- Her claim için "bu oturumda okudum mu?" kontrolü yap.
- Kod hakkında yorum yapmadan önce ilgili satırları oku.
- "Sanırım", "herhalde", "bence" tarzı ifadelerden kaçın.
- Okumadan yapılan claim'ler geçmişte en çok friction yaratan kategoridir.
""".strip(),

    "null": """
## Extra Focus: Null / Undefined / Input Validation
- Public boundary'lerde (fonksiyon parametreleri, API input, user input) null/undefined kontrolü yap.
- Guard clause + erken return tercih et.
- Sadece tipe güvenme, runtime'da da doğrula.
- Geçmişte en sık "runtime'da patladı" kategorisidir.
""".strip(),

    "security": """
## Extra Focus: Security Boundary
- Auth, authorization, secret, payment, sensitive data ile ilgili her değişiklikte ekstra dikkat.
- Input sanitization ve validation her security boundary'de zorunlu.
- Hata mesajlarında sensitive bilgi sızdırma.
- Race condition ve TOCTOU risklerini kontrol et.
""".strip(),

    "error handling": """
## Extra Focus: Error Handling
- Kritik path'lerde bare except kullanma.
- Hata log'lanmadan re-raise veya dönüştürme yapma.
- Kullanıcıya anlamlı, iç bilgi sızdırmayan hata mesajı ver.
- Geçmişte en çok "debug etmek imkansız" şikayeti bu kategoriden geldi.
""".strip(),

    "long function": """
## Extra Focus: Complexity / Long Function
- 50-60 satırı geçen fonksiyonları refactor etmeyi düşün.
- Extract before continue prensibini uygula.
- Geçmişte uzun fonksiyonlar en çok "review turu" ve "bug" üreten alanlardan biriydi.
""".strip(),
}


def get_checklist_for_categories(categories: List[str]) -> str:
    """
    Verilen kategori listesine göre ilgili checklist metinlerini birleştirip döndürür.
    """
    result_parts = []
    seen = set()

    for cat in categories:
        cat_lower = cat.lower()
        for key in CHECKLISTS:
            if key in cat_lower and key not in seen:
                result_parts.append(CHECKLISTS[key])
                seen.add(key)

    if not result_parts:
        return ""

    header = "## Faz 2 — Dinamik Friction Checklist (Ledger Kategorilerine Göre)\n"
    header += "Aşağıdaki alanlar bu workspace'te geçmişte en çok friction yaratan kategorilerdir.\n"
    header += "Bu çalışmada özellikle dikkat et.\n\n"

    return header + "\n\n".join(result_parts)


def get_checklist_for_ledger_patterns(patterns: List[str]) -> str:
    """
    Ledger'dan gelen pattern string'lerine bakarak ilgili kategorileri tespit eder
    ve checklist metnini döndürür.
    """
    detected_categories = set()

    for p in patterns:
        p_lower = p.lower()
        if any(k in p_lower for k in ["handoff", "context", "boundary"]):
            detected_categories.add("handoff")
        if any(k in p_lower for k in ["factcheck", "claim", "read", "without reading"]):
            detected_categories.add("factcheck")
        if any(k in p_lower for k in ["null", "undefined", "none", "input validation"]):
            detected_categories.add("null")
        if any(k in p_lower for k in ["secret", "auth", "security", "injection", "bypass"]):
            detected_categories.add("security")
        if any(k in p_lower for k in ["error handling", "except", "swallow"]):
            detected_categories.add("error handling")
        if any(k in p_lower for k in ["long function", "too long", "complex", "god"]):
            detected_categories.add("long function")

    if not detected_categories:
        return ""

    return get_checklist_for_categories(list(detected_categories))
