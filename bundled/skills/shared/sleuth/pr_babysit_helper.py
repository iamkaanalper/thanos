"""
Sleuth + pr-babysit Entegrasyon Helper (Prototip)

Bu modül, pr-babysit'in karmaşık teşhis durumlarında Sleuth disiplinini
hafif ve güvenli şekilde enjekte etmesine yardımcı olur.

Kullanım amacı: Seviye 1 entegrasyon (düşük riskli, prompt enjeksiyonu)

Örnek kullanım:
    from bundled.skills.shared.sleuth.pr_babysit_helper import should_inject_sleuth_reminder

    if should_inject_sleuth_reminder(pr_status, diagnosis_round, error_type):
        prompt += get_sleuth_reminder_block()
"""

from typing import Literal

from .prompts import get_sleuth_persona_reminder


def should_inject_sleuth_reminder(
    pr_status: str,
    diagnosis_round: int,
    error_type: str | None = None,
    is_complex: bool = False
) -> bool:
    """
    pr-babysit'in bir teşhis adımında Sleuth disiplinini enjekte edip etmemeye karar verir.

    Args:
        pr_status: PR'ın mevcut durumu (örn: "ci_failed", "review_comments")
        diagnosis_round: Kaçıncı teşhis turu olduğu (1, 2, 3...)
        error_type: Hata tipi (örn: "flaky", "race_condition", "state_corruption")
        is_complex: Teşhisin karmaşık olduğu manuel olarak biliniyorsa True

    Returns:
        bool: Sleuth reminder enjekte edilmeli mi?
    """
    # Erken turlarda çok agresif olmayalım
    if diagnosis_round < 2:
        return False

    # Yüksek öncelikli durumlar
    high_priority_statuses = {"ci_failed", "review_comments", "conflicts"}

    if pr_status in high_priority_statuses:
        # 2. turdan itibaren veya karmaşık hata varsa enjekte et
        if diagnosis_round >= 2 or is_complex:
            return True

    # Belirli hata tipleri (derin teşhis gerektirenler)
    deep_diagnosis_types = {
        "flaky", "intermittent", "race_condition", "state_corruption",
        "concurrency", "timing", "nondeterministic"
    }

    if error_type and error_type.lower() in deep_diagnosis_types:
        return True

    # Manuel olarak karmaşık işaretlenmişse
    if is_complex and diagnosis_round >= 2:
        return True

    return False


def get_sleuth_reminder_block(context: str = "") -> str:
    """
    pr-babysit subagent'larına enjekte edilebilecek Sleuth disiplin bloğunu döndürür.
    """
    base = get_sleuth_persona_reminder()

    if context:
        base += f"\n\nBağlam: {context}\n"

    return base


def get_sleuth_injection_decision(
    pr_status: str,
    diagnosis_round: int,
    error_type: str | None = None,
    is_complex: bool = False
) -> dict:
    """
    Daha zengin bilgi döndüren versiyon (loglama ve karar takibi için kullanışlı).
    """
    should_inject = should_inject_sleuth_reminder(
        pr_status, diagnosis_round, error_type, is_complex
    )

    return {
        "should_inject": should_inject,
        "reason": _generate_reason(pr_status, diagnosis_round, error_type, is_complex),
        "reminder_block": get_sleuth_reminder_block() if should_inject else None,
        "injection_level": "light" if should_inject else "none"
    }


def _generate_reason(
    pr_status: str,
    diagnosis_round: int,
    error_type: str | None,
    is_complex: bool
) -> str:
    reasons = []
    if diagnosis_round >= 2:
        reasons.append(f"{diagnosis_round}. teşhis turu")
    if pr_status in {"ci_failed", "review_comments"}:
        reasons.append(f"karmaşık {pr_status} durumu")
    if error_type:
        reasons.append(f"hata tipi: {error_type}")
    if is_complex:
        reasons.append("manuel olarak karmaşık işaretlendi")

    return " | ".join(reasons) if reasons else "koşullar karşılanmadı"