"""
Compound Evolution Engine (Skill Curator)

Bu modül, compound-learnings flywheel'in en kritik eksik parçasını tamamlar:

- Draft'ları otomatik değerlendirme (5 boyutlu skorlama)
- Promote / Repair / Archive kararları
- Yüksek kaliteli draft'ların kalıcı kural / ajan / skill haline getirilmesi
- Düşük kaliteli olanların temizlenmesi

Bu, sistemin zamanla gerçekten "öğrenip" kendi disiplinini güçlendirmesini sağlar.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from .friction import record_friction
except Exception:
    def record_friction(*args, **kwargs): pass


@dataclass
class DraftEvaluation:
    draft_path: str
    scores: Dict[str, float]  # 5 boyut
    overall_score: float
    decision: str  # "promote", "repair", "archive", "review"
    reasons: List[str] = field(default_factory=list)
    suggested_actions: List[str] = field(default_factory=list)
    promoted_category: str = ""      # new_agent, new_rule, hook_behavior, skill_update, persona_update
    confidence: str = "medium"       # high, medium, low
    suggested_target_file: str = ""  # Örnek: "bundled/agents/xxx.md" veya "docs/rules/yyy.md"
    priority: str = "medium"         # high, medium, low
    estimated_effort: str = "medium" # high, medium, low
    evaluated_at: str = ""


def evaluate_draft(draft_path: str, draft_content: str = "", context: str = "") -> DraftEvaluation:
    """
    Bir compound draft'ını 5 boyut üzerinden daha derin değerlendirir.

    Geliştirilmiş versiyon:
    - Context'i gerçekten kullanır
    - Promote kararında "nereye promote edileceği"ni de önerir
    - Repair için daha somut öneriler üretir
    """
    scores = {
        "impact": 5.0,
        "clarity": 5.0,
        "generality": 5.0,
        "evidence": 5.0,
        "safety": 8.0,
    }

    reasons = []
    actions = []
    promoted_category = ""

    content_lower = (draft_content or "").lower()
    context_lower = (context or "").lower()

    # === Impact ===
    if any(k in content_lower for k in ["friction", "pattern", "recurring", "tekrar eden"]):
        scores["impact"] += 2.5
        reasons.append("Yüksek frekanslı / tekrar eden pattern içeriyor")
    if any(k in content_lower for k in ["architectural", "sistem", "tüm", "genel"]):
        scores["impact"] += 1.5

    # === Clarity ===
    if len(draft_content) > 1200:
        scores["clarity"] -= 2.0
        reasons.append("Fazla uzun, netlik riski yüksek")
        actions.append("Daha kısa, madde madde ve actionable hale getir")
    if any(k in content_lower for k in ["nasıl yapılır", "adım", "step", "şu şekilde"]):
        scores["clarity"] += 2.0

    # === Generality ===
    if any(k in content_lower for k in ["her zaman", "genelde", "çoğu durumda", "tüm projelerde"]):
        scores["generality"] += 2.0
    if "bu projeye özel" in content_lower or "sadece burada" in content_lower:
        scores["generality"] -= 1.5

    # === Evidence ===
    if any(k in content_lower for k in ["örnek", "example", "görüldü", "yaşandı", "senaryo"]):
        scores["evidence"] += 2.5
    if "kanıt" in content_lower or "gözlem" in content_lower:
        scores["evidence"] += 1.0

    # === Safety ===
    if any(k in content_lower for k in ["risk", "breaking", "tehlikeli", "dikkat", "yan etki"]):
        scores["safety"] -= 2.5
        reasons.append("Risk / yan etki potansiyeli belirtilmiş")
    if "zorunlu" in content_lower or "her zaman uygulanmalı" in content_lower:
        scores["safety"] -= 1.0  # Zorunlu kurallar daha dikkatli incelenmeli

    # Context'ten ek sinyal
    if "swarm" in context_lower and "phase" in content_lower:
        scores["generality"] += 1.0
    if "implement" in context_lower or "execute-plan" in context_lower:
        scores["impact"] += 1.0

    # Genel skor
    overall = sum(scores.values()) / len(scores)
    overall = round(overall, 2)

    # === Geliştirilmiş Karar Mekanizması ===
    decision = "review"
    promoted_category = ""
    confidence = "medium"
    suggested_target_file = ""

    if overall >= 8.2 and scores["impact"] >= 7.5 and scores["safety"] >= 6.5:
        decision = "promote"
        confidence = "high" if overall >= 8.8 else "medium"

        # Priority ve Effort belirleme
        if overall >= 8.8 and scores["impact"] >= 8.0:
            priority = "high"
            estimated_effort = "low" if "kural" in content_lower or "rule" in content_lower else "medium"
        else:
            priority = "medium"
            estimated_effort = "medium"

        # Promote kategorisi + hedef dosya önerisi
        if "ajan" in content_lower or "agent" in content_lower or "persona" in content_lower:
            promoted_category = "new_agent"
            suggested_target_file = ".grok/bundled/agents/<yeni-ajan-ismi>.md"
            actions.append(f"Yeni bir bundled agent olarak promote edilmeli → {suggested_target_file}")
        elif "kural" in content_lower or "rule" in content_lower or "her zaman" in content_lower:
            promoted_category = "new_rule"
            suggested_target_file = "docs/rules/<kural-ismi>.md veya ilgili CLAUDE.md bölümü"
            actions.append(f"Kalıcı kural olarak promote edilmeli → {suggested_target_file}")
        elif "hook" in content_lower or "otomatik" in content_lower:
            promoted_category = "hook_behavior"
            suggested_target_file = ".grok/hooks/examples/ veya hook_runner registry"
            actions.append(f"Hook davranışı olarak promote edilmeli → {suggested_target_file}")
        else:
            promoted_category = "skill_update"
            suggested_target_file = "İlgili skill'in SKILL.md veya Production Contract bölümü"
            actions.append(f"Skill güncellemesi olarak promote edilmeli → {suggested_target_file}")

    elif overall < 5.5 or scores["safety"] < 5.0:
        decision = "archive"
        confidence = "high" if scores["safety"] < 4.5 else "medium"
        priority = "low"
        estimated_effort = "low"
        actions.append("Düşük kaliteli veya yüksek riskli → arşivlenmeli")
    elif overall >= 6.2:
        decision = "repair"
        confidence = "medium"
        priority = "medium"
        estimated_effort = "medium"
        actions.append("İyileştirme önerileriyle tekrar değerlendirilmeli")
        if scores["clarity"] < 6.0:
            actions.append("Daha net ve uygulanabilir adımlar eklenmeli")
        if scores["evidence"] < 6.0:
            actions.append("Gerçek örnek veya gözlem eklenmeli")

    return DraftEvaluation(
        draft_path=draft_path,
        scores=scores,
        overall_score=overall,
        decision=decision,
        reasons=reasons,
        suggested_actions=actions,
        promoted_category=promoted_category,
        confidence=confidence,
        suggested_target_file=suggested_target_file,
        priority=priority,
        estimated_effort=estimated_effort,
        evaluated_at=datetime.now(timezone.utc).isoformat()
    )


def curate_drafts(draft_paths: List[str], min_promote_score: float = 8.0) -> Dict[str, List[DraftEvaluation]]:
    """
    Geliştirilmiş versiyon:
    - Promote kararlarında kategoriyi de dikkate alır
    - Daha temiz ve kararlı gruplandırma yapar
    """
    results = {
        "promote": [],
        "repair": [],
        "archive": [],
        "review": []
    }

    for path in draft_paths:
        try:
            content = Path(path).read_text(encoding="utf-8", errors="ignore")
            evaluation = evaluate_draft(path, content)

            if evaluation.decision == "promote" and evaluation.overall_score >= min_promote_score:
                results["promote"].append(evaluation)
            else:
                results[evaluation.decision].append(evaluation)

        except Exception as e:
            record_friction(
                pattern="compound draft evaluation failed",
                category="Self-Improvement",
                description=f"{path}: {e}",
                friction_impact="Low"
            )

    return results


def record_promotion_decision(evaluation: DraftEvaluation, promoted_to: str = ""):
    """Promote kararını friction olarak kaydeder (kalıcı öğrenme için)."""
    record_friction(
        pattern=f"Compound draft promoted: {Path(evaluation.draft_path).name}",
        category="Compound Evolution",
        description=f"Score: {evaluation.overall_score} | Decision: {evaluation.decision} | Promoted to: {promoted_to}",
        friction_impact="High" if evaluation.overall_score >= 8.5 else "Medium",
        recommended_fix_type="Track this pattern as permanent rule/skill",
        tags=["compound-evolution", "promotion"]
    )


def run_evolution_cycle(draft_paths: List[str]) -> Dict[str, Any]:
    """
    Derinleştirilmiş evolution döngüsü.

    Artık şunları da yapar:
    - Promote edilen draft'ların önerilen kategorilerini özetler
    - Daha kaliteli friction kaydı üretir
    """
    curated = curate_drafts(draft_paths)

    promote_categories = {}
    for ev in curated["promote"]:
        cat = ev.promoted_category or "unknown"
        promote_categories[cat] = promote_categories.get(cat, 0) + 1

    summary = {
        "total": len(draft_paths),
        "promote": len(curated["promote"]),
        "repair": len(curated["repair"]),
        "archive": len(curated["archive"]),
        "review": len(curated["review"]),
        "promote_by_category": promote_categories,
        "evaluations": curated
    }

    # Promote edilenleri daha kaliteli friction olarak kaydet
    for ev in curated["promote"]:
        record_promotion_decision(ev, promoted_to=ev.suggested_target_file or "suggested_by_evolution_engine")

    return summary


def generate_promotion_guidance(evaluation: DraftEvaluation) -> str:
    """
    Bir DraftEvaluation sonucuna bakarak, o draft'ı gerçekten sisteme katmak için
    somut adımlar öneren rehber metin üretir.
    """
    if evaluation.decision != "promote":
        return "Bu draft promote için uygun değil. Önce repair veya archive kararını gözden geçir."

    guidance = f"""
## Promotion Guidance for: {Path(evaluation.draft_path).name}

**Karar:** PROMOTE (Güven: {evaluation.confidence}, Öncelik: {evaluation.priority}, Tahmini Çaba: {evaluation.estimated_effort})

**Önerilen Kategori:** {evaluation.promoted_category}
**Hedef Dosya Önerisi:** {evaluation.suggested_target_file or "Henüz belirlenmedi"}

**Gerekçe:**
{chr(10).join('- ' + r for r in evaluation.reasons)}

**Önerilen Adımlar:**
1. İlgili dosyayı aç (veya oluştur): {evaluation.suggested_target_file or '[hedef dosya]'}
2. Bu draft'taki ana kuralı net ve kısa bir şekilde yaz.
3. "Rejected Alternatives" veya "Notlar" bölümü ekle.
4. İlgili ajanların (varsa) prompt'larına veya Production Contract'ına referans ekle.
5. Bu değişikliği compound-friction.jsonl'e "PROMOTED" olarak kaydet.

**Dikkat Edilecekler:**
{chr(10).join('- ' + a for a in evaluation.suggested_actions)}

---
Bu rehberi takip ederek draft'ı sistematik şekilde sisteme katabilirsin.
"""
    return guidance.strip()


def suggest_full_promotion_package(evaluation: DraftEvaluation) -> Dict[str, Any]:
    """
    Bir draft değerlendirmesine bakarak, promote edilmesi durumunda
    yapılması gereken tüm somut işleri tek bir pakette önerir.
    (İleri taşınmış, olgun versiyon)
    """
    if evaluation.decision != "promote":
        return {
            "status": "not_ready_for_promotion",
            "decision": evaluation.decision,
            "message": "Bu draft promote için uygun değil."
        }

    package = {
        "draft": Path(evaluation.draft_path).name,
        "overall_score": evaluation.overall_score,
        "priority": evaluation.priority,
        "estimated_effort": evaluation.estimated_effort,
        "promoted_category": evaluation.promoted_category,
        "suggested_target_file": evaluation.suggested_target_file,
        "confidence": evaluation.confidence,
        "actions": [],
        "friction_to_record": f"Compound draft promoted as {evaluation.promoted_category}: {Path(evaluation.draft_path).name}",
        "related_agents": [],
        "draft_skeleton": "",
        "next_steps": [],
    }

    # Kategoriye göre somut aksiyonlar + iskelet
    if evaluation.promoted_category == "new_agent":
        package["actions"].append("Yeni agent dosyası oluştur (.grok/bundled/agents/)")
        package["actions"].append("İlgili persona dosyasını güncelle (gerekirse)")
        package["related_agents"] = ["Self-Learner", "Architect"]
        package["draft_skeleton"] = _get_agent_skeleton(evaluation)
        package["next_steps"].append("Oluşturulan ajanı team-dynamics-profiler-architect-selflearner.md dosyasına ekle")

    elif evaluation.promoted_category == "new_rule":
        package["actions"].append("Kuralı docs/rules/ veya ilgili CLAUDE.md bölümüne ekle")
        package["actions"].append("İlgili ajanların prompt'larına referans ekle")
        package["related_agents"] = ["Reviewer", "Kraken", "Architect"]
        package["draft_skeleton"] = _get_rule_skeleton(evaluation)
        package["next_steps"].append("Yeni kuralı agent linter'ın recommended sections'ına ekle")

    elif evaluation.promoted_category == "hook_behavior":
        package["actions"].append("Hook'u .grok/hooks/ altına ekle veya mevcut hook'u güçlendir")
        package["actions"].append("hook_runner.py registry'sine ekle")
        package["related_agents"] = ["Self-Learner"]
        package["draft_skeleton"] = _get_hook_skeleton(evaluation)
        package["next_steps"].append("Hook'u compound_analyzer_trigger.py veya completion_friction ile entegre et")

    else:
        package["actions"].append("İlgili skill'in SKILL.md veya Production Contract bölümünü güncelle")
        package["related_agents"] = ["Self-Learner", "Architect"]
        package["draft_skeleton"] = _get_skill_update_skeleton(evaluation)
        package["next_steps"].append("Skill güncellemesini swarm planning ve agent linter ile senkronize et")

    # Genel adımlar
    package["actions"].append("Bu değişikliği compound-friction.jsonl'e 'PROMOTED' olarak kaydet (yüksek impact)")
    package["actions"].append("Gerekirse ilgili test veya örnek senaryo ekle")
    package["actions"].append("Promotion'ı compound-learnings/SKILL.md 'de örnek olarak dokümante et")

    return package


def _get_agent_skeleton(evaluation: DraftEvaluation) -> str:
    return f"""# {Path(evaluation.draft_path).stem.replace('-', ' ').title()} Agent

**Role:** [Buraya kısa rol tanımı yaz]

## Core Personality
[Bu ajanın kişilik özellikleri]

## When You Are Used
[Ne zaman çağrılmalı?]

## Key Responsibilities
- ...

## Interaction With Other Agents
- **Self-Learner**: ...
- **Architect**: ...
- **Profiler**: ...

## Self-Improvement Participation
[Compound Evolution ile nasıl beslenir?]
"""

def _get_rule_skeleton(evaluation: DraftEvaluation) -> str:
    return f"""## {Path(evaluation.draft_path).stem.replace('-', ' ').title()}

**Kural:** [Net ve kısa kural ifadesi]

**Neden?**
{evaluation.reasons[0] if evaluation.reasons else "..."}

**Ne Zaman Uygulanmalı?**
...

**İlgili Ajanlar:**
- ...
"""

def _get_hook_skeleton(evaluation: DraftEvaluation) -> str:
    return """# Hook Davranışı Önerisi

**Hook Adı:** on_...
**Tetikleyici:** ...
**Ne Yapmalı:** ...
**Örnek Kod:** ...
"""

def _get_skill_update_skeleton(evaluation: DraftEvaluation) -> str:
    return """## Skill Güncelleme Önerisi

**Etkilenecek Skill:** ...
**Eklenecek Bölüm / Kural:** ...
**Gerekçe:** ...
"""
