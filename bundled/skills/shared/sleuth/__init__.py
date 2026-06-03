"""
Sleuth Activation & Routing Module

Bu modül, Sleuth ajanının veya Sleuth persona katmanının ne zaman önerileceğini
belirleyen basit ama etkili bir routing sistemi sağlar.

Kullanım:
    from bundled.skills.shared.sleuth.router import get_sleuth_recommendation

    rec = get_sleuth_recommendation(user_description)
    if rec["recommended_mode"] == "dedicated_agent":
        # spawn_subagent(subagent_type="sleuth", ...)
        ...
"""

from .router import get_sleuth_recommendation
from .prompts import get_sleuth_persona_reminder

__all__ = [
    "get_sleuth_recommendation",
    "get_sleuth_persona_reminder",
]