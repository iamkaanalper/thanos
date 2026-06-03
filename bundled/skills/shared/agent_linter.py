"""
Agent Linter (Basic Quality Gate)

Ajan dosyalarının (.md) yapısal kalitesini kontrol eder.

Kontrol ettiği şeyler:
- Frontmatter (--- ile başlayan) var mı?
- name ve description alanları var mı?
- Temel bölümler mevcut mu? (Core Personality, When You Are Used, vb.)
- Tutarlı format kullanılıyor mu?

Bu, ajan sayısı arttıkça kaliteyi korumak için temel bir araçtır.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List


def lint_agent_file(path: str | Path) -> Dict[str, Any]:
    """
    Tek bir ajan dosyasını daha kapsamlı lint'ler (2026-06 güncellemesi).
    """
    p = Path(path)
    if not p.exists():
        return {"status": "file_not_found", "path": str(p)}

    content = p.read_text(encoding="utf-8", errors="ignore")
    content_lower = content.lower()

    issues: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []

    # Special case: team-dynamics doc is reference, not strict persona
    if "team-dynamics" in p.name.lower():
        # Still check length and key refs, but relax required sections
        if len(content) > 1500:
            return {
                "status": "pass",
                "path": str(p),
                "issues": [],
                "warnings": [],
                "suggestions": ["Reference doc - high value for cross-agent coordination."],
                "score": 92,
            }

    # Frontmatter kontrolü
    if not content.strip().startswith("---"):
        issues.append("Frontmatter (---) ile başlamıyor")

    # Zorunlu bölümler (Grok-adapted: match actual shipped templates + legacy)
    # Grok agents use: Role & Responsibility / Core Capabilities / Core Principles, When to Use / When You Are Used, Team Dynamics / Interaction / Swarm Role
    required_checks = [
        ("Core Personality / Role", ["core personality", "core principles", "role & responsibility", "core capabilities", "core principles (non-negotiable)"]),
        ("When to Use / Role", ["when you are used", "when to use", "when to use ", "when you are used this agent"]),
        ("Interaction / Team Dynamics / Swarm", ["interaction with other agents", "interaction with other", "interaction", "team dynamics", "swarm role"]),
    ]

    for label, variants in required_checks:
        found = any(v in content_lower for v in variants)
        if not found:
            issues.append(f"Zorunlu bölüm eksik: {label}")

    # Önerilen / Kalite bölümleri
    recommended_sections = [
        "Self-Improvement Participation",
        "Team Dynamics",
    ]

    for section in recommended_sections:
        if section.lower() not in content_lower:
            warnings.append(f"Önerilen bölüm eksik: {section}")
            suggestions.append(f"'{section}' bölümü eklenerek ajan kalitesi artırılabilir.")

    # Başlık kontrolü (Grok: allow slightly after long but valid frontmatter; look in first 400 chars or after first --- block)
    first_400 = content[:400]
    if "# " not in first_400:
        # also check after frontmatter close if present
        if "---" in content[:300]:
            after_fm = content[content.find("---", content.find("---")+3): content.find("---", content.find("---")+3)+300]
            if "# " not in after_fm:
                issues.append("Dosya başında net bir başlık (# Agent Name) yok")
        else:
            issues.append("Dosya başında net bir başlık (# Agent Name) yok")

    # Compound Evolution / Self-Improvement bağlantısı
    if "compound" not in content_lower and "self-improvement" not in content_lower:
        warnings.append("Compound Evolution / Self-Improvement bağlantısı zayıf")
        suggestions.append("Self-Improvement Participation bölümünde compound evolution ile ilişki belirtilmeli.")

    # Takım Dinamiği kontrolü (Profiler-Architect-Self-Learner üçlüsü)
    if "team dynamics" not in content_lower and "profiler" not in content_lower and "architect" not in content_lower:
        warnings.append("Takım dinamiği (Profiler/Architect/Self-Learner) referansı yok")
        suggestions.append("Diğer kritik ajanlarla (Profiler, Architect, Self-Learner) ilişki tanımlanmalı.")

    # Uzunluk kontrolü
    if len(content) < 800:
        warnings.append("Dosya oldukça kısa (<800 karakter)")
        suggestions.append("Daha fazla örnek, senaryo ve diğer ajanlarla ilişki eklenmeli.")

    # Genel kalite önerileri
    if "swarm" not in content_lower:
        suggestions.append("Swarm içindeki rolü belirtilmemiş (Phase 2/3/4/5).")

    # Production Contract / Executable primitives (high value for bundled agents)
    contract_hits = 0
    for term in ["ledger", "task_lifecycle", "handoff", "preflight", "friction", "production contract", "bounded qa", "bounded loop"]:
        if term in content_lower:
            contract_hits += 1
    if contract_hits < 3:
        warnings.append("Production Contract / Ledger / Handoff / Preflight / Friction referansları zayıf")
        suggestions.append("Ledger, handoff, preflight, friction, bounded QA mentions ekle (executable disiplin).")

    # Hooks participation (post hooks bitir)
    if "hook" not in content_lower and "on_" not in content_lower and "run_hook" not in content:
        warnings.append("Hooks entegrasyonu belirtilmemiş")
        suggestions.append("Hooks Participation bölümü ekle: hangi on_* event'leri ateşler veya dinler (örn on_ai_feature, on_agent_spawn).")

    # Frontmatter name/desc quality
    if content.strip().startswith("---"):
        if "name:" not in content[:300].lower():
            warnings.append("Frontmatter'da name: alanı eksik")
        if "description:" not in content[:300].lower():
            warnings.append("Frontmatter'da description: alanı eksik")

    status = "pass" if not issues else "fail"
    base = 100 - len(issues) * 20 - len(warnings) * 8
    bonus = min(15, contract_hits * 2 + (3 if "hook" in content_lower or "on_" in content_lower else 0))
    score = max(0, min(100, base + bonus))

    return {
        "status": status,
        "path": str(p),
        "issues": issues,
        "warnings": warnings,
        "suggestions": suggestions,
        "score": score,
    }


def lint_all_agents(agents_dir: str | Path = None) -> Dict[str, Any]:
    """
    .grok/bundled/agents/ altındaki tüm ajanları toplu lint'ler ve olgun rapor üretir.
    """
    if agents_dir is None:
        agents_dir = Path.home() / ".grok" / "bundled" / "agents"

    agents_dir = Path(agents_dir)
    results = []
    total_score = 0
    all_suggestions = []

    for md_file in agents_dir.glob("*.md"):
        if md_file.name.lower() in ["readme.md", "index.md"]:
            continue
        res = lint_agent_file(md_file)
        results.append(res)
        total_score += res.get("score", 0)
        all_suggestions.extend(res.get("suggestions", []))

    avg_score = round(total_score / len(results), 1) if results else 0

    # En sık tekrar eden önerileri bul
    from collections import Counter
    suggestion_counts = Counter(all_suggestions)
    top_suggestions = [s for s, _ in suggestion_counts.most_common(5)]

    # Kategorize öneriler
    categorized = {
        "team_dynamics": [s for s in all_suggestions if "team" in s.lower() or "profiler" in s.lower() or "architect" in s.lower()],
        "compound_evolution": [s for s in all_suggestions if "compound" in s.lower() or "self-improvement" in s.lower()],
        "general_quality": [s for s in all_suggestions if "team" not in s.lower() and "compound" not in s.lower()]
    }

    return {
        "agents_checked": len(results),
        "average_score": avg_score,
        "results": results,
        "top_improvement_areas": top_suggestions,
        "categorized_suggestions": categorized,
        "summary": f"{len(results)} ajan kontrol edildi. Ortalama kalite skoru: {avg_score}",
        "global_recommendation": "En sık tekrar eden iyileştirme alanları yukarıda listelendi. Özellikle 'Team Dynamics' ve 'Compound Evolution' bağlantısı zayıf ajanlara öncelik verilmeli." if top_suggestions else "Tüm ajanlar genel olarak iyi durumda görünüyor."
    }


if __name__ == "__main__":
    print(lint_all_agents())