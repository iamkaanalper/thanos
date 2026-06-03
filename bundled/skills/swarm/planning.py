"""
Swarm Planning Helper

Swarm'ın Phase 2'sini (Planning & Track Design) desteklemek için kullanılır.
Architect ajanını çağırarak track'leri daha bilinçli şekilde parçalamayı,
bağımlılıkları analiz etmeyi ve basit bir plan raporu üretmeyi sağlar.

Bu dosya, swarm orchestrator'ının planlama kalitesini artırmak için tasarlanmıştır.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

try:
    from tools import spawn_subagent, get_command_or_subagent_output
except ImportError:
    spawn_subagent = None
    get_command_or_subagent_output = None


@dataclass
class TrackPlan:
    id: str
    title: str
    objective: str
    dependencies: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    estimated_complexity: str = "medium"  # low, medium, high
    performance_sensitive: bool = False   # Profiler'ın erken dahil edilmesi gereken track'ler için
    architectural_impact: bool = False    # Architect'in daha fazla dikkat etmesi gereken track'ler için
    suggested_specialists: List[str] = field(default_factory=list)  # e.g. ["profiler", "security-reviewer"]


@dataclass
class SwarmPlan:
    swarm_id: str
    overall_objective: str
    tracks: List[TrackPlan] = field(default_factory=list)
    global_risks: List[str] = field(default_factory=list)
    recommended_order: List[str] = field(default_factory=list)
    notes: str = ""


def generate_swarm_plan(
    swarm_id: str,
    objective: str,
    exploration_summary: str = "",
    architect_prompt_override: Optional[str] = None
) -> SwarmPlan:
    """
    Swarm için daha gelişmiş plan üretir.

    - Architect ajanını çağırır (mümkünse)
    - Track'ler arası bağımlılık ve risk analizi yapar
    - Önerilen execution sırasını belirler
    """
    plan = SwarmPlan(
        swarm_id=swarm_id,
        overall_objective=objective
    )

    if spawn_subagent:
        prompt = architect_prompt_override or f"""
You are the Architect for Swarm {swarm_id}.

Overall Objective: {objective}

Keşif özeti (varsa):
{exploration_summary or "Henüz detaylı keşif yapılmadı."}

Görevin:
1. Bu işi 2-5 arası mantıklı, mümkün olduğunca bağımsız track'lere böl.
2. Her track için şu bilgileri ver:
   - id (track-1, track-2 ...)
   - title
   - objective (1-2 cümle)
   - dependencies (başka track ID'leri)
   - risks (en kritik 2-3 risk)
   - estimated_complexity (low / medium / high)
3. Track'ler için önerilen execution sırasını belirt (recommended_order).
4. Genel sistemik riskleri ve önemli notları yaz.

Çıktıyı yapılandırılmış ve net ver.
"""
        try:
            task = spawn_subagent(
                subagent_type="general-purpose",
                description=f"[architect] Swarm {swarm_id} Phase 2 Planning",
                prompt=prompt
            )
            # Gerçek ortamda burada sonucu parse ederdik.
            plan.notes = "Architect çağrıldı. Gerçek ortamda sonucu parse et ve planı doldur."
        except Exception as e:
            plan.notes = f"Architect çağrısı başarısız: {e}"

    # Fallback (Architect çağrılamazsa) - daha zengin
    if not plan.tracks:
        plan.tracks = _simple_track_decomposition(objective)
        plan.recommended_order = [t.id for t in plan.tracks]
        plan.global_risks = ["Architect çağrısı yapılamadı, basit decomposition kullanıldı"]
        if "fallback" not in (plan.notes or "").lower():
            plan.notes = (plan.notes or "") + " | Basit ama zenginleştirilmiş fallback decomposition kullanıldı."

    # Basit dependency ve order iyileştirmesi
    if not plan.recommended_order:
        plan.recommended_order = [t.id for t in plan.tracks]

    # Otomatik flag'leri fallback'te de uygula (performance_sensitive için)
    for t in plan.tracks:
        if any(kw in t.objective.lower() for kw in ["performance", "slow", "latency", "cpu", "memory"]):
            t.performance_sensitive = True
        if any(kw in t.objective.lower() for kw in ["architecture", "boundary", "service", "model", "tradeoff"]):
            t.architectural_impact = True

    return plan


def _simple_track_decomposition(objective: str) -> List[TrackPlan]:
    """Daha zengin basit track ayrıştırması. Gerçek implementasyonda Architect ajanına bırakılır."""
    return [
        TrackPlan(
            id="track-1",
            title="Core Implementation",
            objective=f"Main logic and core changes for: {objective}",
            estimated_complexity="high",
            performance_sensitive=True,
            architectural_impact=True,
            suggested_specialists=["kraken", "profiler"]
        ),
        TrackPlan(
            id="track-2",
            title="Integration, Tests & Edge Cases",
            objective="Cross-track integration, tests and critical edge cases",
            dependencies=["track-1"],
            estimated_complexity="medium",
            performance_sensitive=True,
            suggested_specialists=["reviewer", "tdd-guide"]
        ),
        TrackPlan(
            id="track-3",
            title="Security, Observability, Docs & Hygiene",
            objective="Security review, logging/metrics, documentation and code hygiene",
            dependencies=["track-1", "track-2"],
            estimated_complexity="low",
            suggested_specialists=["security-reviewer", "janitor"]
        )
    ]


def build_dependency_graph(tracks: List[TrackPlan]) -> str:
    """Basit metin tabanlı dependency graph üretir."""
    lines = ["## Dependency Graph (text)"]
    for t in tracks:
        deps = ", ".join(t.dependencies) if t.dependencies else "none"
        lines.append(f"- {t.id} depends on: {deps}")
    return "\n".join(lines)


def generate_plan_report(swarm_plan: SwarmPlan) -> str:
    """Swarm planından güzel bir markdown raporu üretir."""
    lines = []
    lines.append(f"# Swarm Plan - {swarm_plan.swarm_id}")
    lines.append(f"\n**Objective:** {swarm_plan.overall_objective}\n")

    lines.append("## Tracks")
    for track in swarm_plan.tracks:
        lines.append(f"\n### {track.id}: {track.title}")
        lines.append(f"- **Objective**: {track.objective}")
        lines.append(f"- **Dependencies**: {', '.join(track.dependencies) if track.dependencies else 'None'}")
        lines.append(f"- **Complexity**: {track.estimated_complexity}")
        if track.performance_sensitive:
            lines.append(f"- **Performance Sensitive**: Yes (Profiler önerilir)")
        if track.architectural_impact:
            lines.append(f"- **Architectural Impact**: Yes (Architect önerilir)")
        if track.risks:
            lines.append(f"- **Risks**: {', '.join(track.risks)}")

    if swarm_plan.recommended_order:
        lines.append("\n## Recommended Order")
        lines.append(" → ".join(swarm_plan.recommended_order))

    if swarm_plan.global_risks:
        lines.append("\n## Global Risks")
        for r in swarm_plan.global_risks:
            lines.append(f"- {r}")

    if swarm_plan.notes:
        lines.append(f"\n## Notes\n{swarm_plan.notes}")

    return "\n".join(lines)
