"""
consolidation.py
Smart pattern consolidation for compound-learnings (Grok).

Goal: Turn noisy, repetitive review issues into clean, generalizable patterns
so we can make high-leverage recommendations (rules, persona updates, small skills).
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

try:
    from semantic import enhance_clustering_with_semantics, is_semantic_available
except ImportError:
    enhance_clustering_with_semantics = None
    is_semantic_available = lambda: False


@dataclass
class ConsolidatedPattern:
    description: str
    category: str
    count: int
    examples: list[str]          # original descriptions that were merged
    keywords: set[str]


# ------------------------------------------------------------------
# Normalization
# ------------------------------------------------------------------

_NORMALIZATION_RULES = [
    # === Core Reliability ===
    (r"\b(null|undefined|None)\b", "null/undefined"),
    (r"missing (null|undefined) (check|guard|validation)", "missing null/undefined check"),
    (r"no (null|undefined) (check|guard)", "missing null/undefined check"),
    (r"lack of (null|undefined) (check|guard)", "missing null/undefined check"),

    # === Input Validation ===
    (r"(input|user input|param|parameter|argument).*(validat|saniti|sanitize)", "input validation missing or insufficient"),
    (r"missing (input )?validation", "input validation missing or insufficient"),
    (r"no (input )?validation", "input validation missing or insufficient"),

    # === Error Handling ===
    (r"(poor|weak|missing|inadequate).*(error handling|exception handling)", "insufficient error handling"),
    (r"swallow(ed)? (exception|error)", "insufficient error handling"),
    (r"bare except", "insufficient error handling"),

    # === Complexity ===
    (r"(function|method|class).*(too long|too big|too complex|exceeds.*line)", "function or method too long / complex"),
    (r"long function", "function or method too long / complex"),
    (r"god function|god class", "function or method too long / complex"),

    # === Security ===
    (r"(hardcoded|hard-coded).*(secret|key|token|password|credential)", "hardcoded secret/credential"),
    (r"secret.*(in code|hardcoded)", "hardcoded secret/credential"),

    # === Grok-specific high-frequency patterns ===
    (r"(handoff|hand-off).*(missing|weak|not used|not followed)", "handoff discipline not followed"),
    (r"persona.*(not injected|missing|not used)", "persona not properly injected"),
    (r"(worktree|work-tree).*(issue|problem|isolation)", "worktree isolation problem"),
    (r"spawn_subagent.*(without|missing).*(handoff|context)", "subagent launched without proper handoff/context"),
    (r"factcheck|fact-check|claim.*(without reading|without verification)", "factcheck-guard violation (claim without reading code)"),
    (r"memory.*(not used|ignored|bypassed)", "memory system not leveraged"),
    (r"(review|implementer).*(loop|round).*too many", "review-fix loop taking too many rounds"),
]

_SYNONYM_GROUPS = {
    "null/undefined check": {"null check", "undefined guard", "none check", "missing null"},
    "input validation": {"input sanitization", "validate input", "user input validation"},
    "error handling": {"exception handling", "error propagation", "proper error handling"},
    "long function": {"function too long", "method too large", "god function", "decompose function"},
}


def _normalize_text(text: str) -> str:
    """Aggressive but safe normalization for review pattern text."""
    t = text.lower().strip()
    t = re.sub(r"[^\w\s/]", " ", t)          # remove most punctuation
    t = re.sub(r"\s+", " ", t)

    for pattern, replacement in _NORMALIZATION_RULES:
        t = re.sub(pattern, replacement, t, flags=re.IGNORECASE)

    return t.strip()


def _extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords for clustering."""
    words = re.findall(r"\b[a-z]{3,}\b", text.lower())
    stop = {"the", "and", "for", "with", "this", "that", "from", "into", "have", "been"}
    return {w for w in words if w not in stop}


# ------------------------------------------------------------------
# Clustering / Merging
# ------------------------------------------------------------------

def _are_similar(a: str, b: str, keywords_a: set[str], keywords_b: set[str]) -> bool:
    """Heuristic similarity for review patterns (strengthened)."""
    norm_a = _normalize_text(a)
    norm_b = _normalize_text(b)

    if norm_a == norm_b:
        return True

    # High keyword overlap (Jaccard)
    overlap = len(keywords_a & keywords_b)
    union = len(keywords_a | keywords_b)
    if union > 0 and overlap / union >= 0.5:
        return True

    # Strong substring containment
    if norm_a in norm_b or norm_b in norm_a:
        return True

    # Grok-specific high-signal phrase matching
    high_signal_phrases = [
        "null/undefined", "input validation", "error handling",
        "handoff", "persona", "worktree", "factcheck", "memory"
    ]
    for phrase in high_signal_phrases:
        if phrase in norm_a and phrase in norm_b:
            return True

    return False


def detect_meta_patterns(consolidated: list[ConsolidatedPattern]) -> list[dict[str, Any]]:
    """
    Detect when multiple patterns in the same category suggest a higher-leverage artifact.
    This is one of the highest-ROI parts of compound learning.
    """
    meta_suggestions = []
    by_category: dict[str, list[ConsolidatedPattern]] = defaultdict(list)

    for p in consolidated:
        by_category[p.category].append(p)

    for category, patterns in by_category.items():
        if len(patterns) >= 3:
            total_occurrences = sum(p.count for p in patterns)
            if total_occurrences >= 8:
                meta_suggestions.append({
                    "type": "meta_pattern",
                    "category": category,
                    "pattern_count": len(patterns),
                    "total_occurrences": total_occurrences,
                    "patterns": [p.description for p in patterns[:5]],
                    "recommendation": (
                        f"Instead of addressing these {len(patterns)} separate patterns individually, "
                        f"consider creating **one strong, high-leverage artifact** that covers this entire category "
                        f"(e.g. a dedicated rule, a small skill, or a significant persona tightening)."
                    ),
                    "suggested_artifact": _suggest_meta_artifact(category, patterns)
                })

    return meta_suggestions


def _suggest_meta_artifact(category: str, patterns: list[ConsolidatedPattern]) -> str:
    cat = category.lower()

    if "error" in cat or "reliability" in cat or "exception" in cat:
        return (
            "High-leverage action: Create a new small skill `defensive-error-handling` or add a strong mandatory constraint "
            "to the implementer persona requiring full error context logging before any re-throw or conversion."
        )
    if "security" in cat or "secret" in cat or "credential" in cat:
        return (
            "High-leverage action: Add zero-tolerance 'Hardcoded Secrets' rule + require security-auditor review on any run "
            "touching auth, config, or external services. Consider a small helper for secret validation at startup."
        )
    if "test" in cat or "coverage" in cat or "edge" in cat:
        return (
            "Recommended: Create 'Testing Excellence' guidance document + increase weight of Tests specialist in reviewer "
            "selection for complex changes. Consider adding coverage-related checks in the implementer persona."
        )
    if "complex" in cat or "long function" in cat or "decomposition" in cat:
        return (
            "Strong recommendation: Add a hard guideline in the implementer persona — functions over 60 lines must be "
            "justified in the Implementation Summary. Update reviewer to flag excessive complexity even when correct."
        )
    if "input" in cat or "validation" in cat or "null" in cat:
        return (
            "High impact move: Create a focused 'Input Safety' rule + add it as a non-negotiable pre-condition in the "
            "implementer persona. This single rule will eliminate a large class of runtime and security issues."
        )
    if "handoff" in cat or "persona" in cat or "factcheck" in cat:
        return (
            "System-level improvement: Strengthen orchestrator pre-flight checks to require proper handoffs and persona "
            "injection. Consider adding automatic warnings when these disciplines are bypassed."
        )

    return (
        f"Create one focused, high-signal artifact for the '{category}' category (either a new rule in ~/.grok/rules/ "
        f"or a significant tightening of the relevant persona). This will be more effective than addressing the patterns individually."
    )


def consolidate_issues(issues: list[dict[str, Any]]) -> list[ConsolidatedPattern]:
    """
    Main entry point.

    Takes raw issues from memory.py snapshot and returns consolidated patterns
    with merged counts and original examples.
    """
    if not issues:
        return []

    # First pass: normalize everything
    normalized: list[tuple[str, dict]] = []
    for issue in issues:
        original_desc = issue.get("description", "")
        category = issue.get("category", "General")
        count = issue.get("count", 1)

        norm = _normalize_text(original_desc)
        keywords = _extract_keywords(norm)

        normalized.append((norm, {
            "original": original_desc,
            "category": category,
            "count": count,
            "keywords": keywords
        }))

    # Clustering (with optional semantic boost)
    clusters: list[list[dict]] = []
    used = [False] * len(normalized)

    normalized_texts = [item[0] for item in normalized]
    semantic_sim_matrix = None

    if is_semantic_available():
        try:
            from semantic import get_semantic_similarity
            semantic_sim_matrix = get_semantic_similarity(normalized_texts)
        except Exception:
            semantic_sim_matrix = None

    for i in range(len(normalized)):
        if used[i]:
            continue

        current_cluster = [normalized[i][1]]
        used[i] = True
        norm_i, data_i = normalized[i]

        for j in range(i + 1, len(normalized)):
            if used[j]:
                continue

            norm_j, data_j = normalized[j]
            similar = False

            # 1. Try semantic similarity first (highest quality)
            if semantic_sim_matrix is not None:
                try:
                    sim_score = float(semantic_sim_matrix[i, j])
                    if sim_score >= 0.67:
                        similar = True
                except Exception:
                    pass

            # 2. Fallback to strong heuristic
            if not similar:
                similar = _are_similar(norm_i, norm_j, data_i["keywords"], data_j["keywords"])

            if similar:
                current_cluster.append(data_j)
                used[j] = True

        clusters.append(current_cluster)

    # Build final consolidated patterns
    result: list[ConsolidatedPattern] = []
    for cluster in clusters:
        total_count = sum(item["count"] for item in cluster)
        category = cluster[0]["category"]  # take first category (they are usually consistent)

        # Choose the most representative description (usually the shortest clean one)
        descriptions = [item["original"] for item in cluster]
        best_desc = min(descriptions, key=lambda d: (len(d), d))

        all_keywords = set()
        for item in cluster:
            all_keywords.update(item["keywords"])

        result.append(ConsolidatedPattern(
            description=best_desc,
            category=category,
            count=total_count,
            examples=descriptions,
            keywords=all_keywords
        ))

    # Sort by count descending
    result.sort(key=lambda p: p.count, reverse=True)
    return result