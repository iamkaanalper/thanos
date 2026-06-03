"""
Sleuth Activation Router

Bu modül, verilen bir görev açıklamasına göre Sleuth ajanının 
veya Sleuth persona katmanının önerilip önerilmeyeceğini belirler.

Kullanım örneği:
    from bundled.skills.shared.sleuth.router import get_sleuth_recommendation

    rec = get_sleuth_recommendation(
        description="Bu state corruption bug'ını kök nedenini bulmam lazım",
        context="Intermittent ve race condition şüphesi var"
    )

    if rec["recommended_mode"] == "dedicated_agent":
        # spawn_subagent(subagent_type="sleuth", ...)
        pass
    elif rec["recommended_mode"] == "persona_layer":
        # spawn_subagent(..., persona="sleuth", prompt=rec["prompt_addition"])
        pass
"""

from typing import Literal, TypedDict
from .triggers import STRONG_TRIGGERS, MEDIUM_TRIGGERS, BOOSTERS
from .prompts import get_sleuth_persona_reminder
from .normalize import normalize_text as _normalize_text


class SleuthRecommendation(TypedDict):
    recommended_mode: Literal["dedicated_agent", "persona_layer", "none"]
    confidence: Literal["high", "medium", "low"]
    score: float
    reasons: list[str]
    suggested_subagent_type: str | None
    suggested_persona: str | None
    prompt_addition: str | None


def get_sleuth_recommendation(
    description: str,
    context: str = "",
    current_subagent_type: str | None = None
) -> SleuthRecommendation:
    """
    Kullanıcı girdisine göre Sleuth aktivasyonu önerir.

    Returns:
        SleuthRecommendation: Öneri detayları
    """
    text = _normalize_text(description + " " + context)
    score = 0.0
    reasons: list[str] = []

    # Strong triggers
    for keyword, weight in STRONG_TRIGGERS.items():
        if keyword in text:
            score += weight
            reasons.append(f"Strong: {keyword}")

    # Medium triggers
    for keyword, weight in MEDIUM_TRIGGERS.items():
        if keyword in text:
            score += weight
            reasons.append(f"Medium: {keyword}")

    # Boosters
    for keyword, weight in BOOSTERS.items():
        if keyword in text:
            score += weight
            reasons.append(f"Booster: {keyword}")

    final_score = min(score, 10.0)

    if final_score >= 5.5:
        mode: Literal["dedicated_agent", "persona_layer", "none"] = "dedicated_agent"
        confidence: Literal["high", "medium", "low"] = "high" if final_score >= 7.5 else "medium"
        subagent_type = "sleuth"
        persona = None
        prompt_addition = None

    elif final_score >= 3.0:
        mode = "persona_layer"
        confidence = "medium"
        subagent_type = current_subagent_type or "general-purpose"
        persona = "sleuth"
        prompt_addition = get_sleuth_persona_reminder()

    else:
        mode = "none"
        confidence = "low"
        subagent_type = None
        persona = None
        prompt_addition = None

    return {
        "recommended_mode": mode,
        "confidence": confidence,
        "score": round(final_score, 1),
        "reasons": reasons,
        "suggested_subagent_type": subagent_type,
        "suggested_persona": persona,
        "prompt_addition": prompt_addition,
    }