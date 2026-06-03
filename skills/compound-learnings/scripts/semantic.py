"""
semantic.py
Semantic similarity utilities for compound-learnings.

Provides high-quality clustering using embeddings when available,
with intelligent fallbacks.

Priority:
1. sentence-transformers (best quality, if installed)
2. scikit-learn TF-IDF + cosine (good quality, often available)
3. Current heuristic (always available fallback)
"""

from __future__ import annotations

import warnings
from typing import Any, Callable, List, Optional

# Try to import heavy dependencies gracefully
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    _SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    _SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine
    import numpy as np
    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False


# Singleton model cache
_model: Optional[Any] = None


def _get_embedding_model() -> Optional[Any]:
    """Load sentence-transformers model lazily (only once)."""
    global _model
    if _model is not None:
        return _model

    if not _SENTENCE_TRANSFORMERS_AVAILABLE:
        return None

    try:
        # Small, fast, high-quality model good for technical text
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        return _model
    except Exception as e:
        warnings.warn(f"Failed to load sentence-transformers model: {e}")
        return None


def get_semantic_similarity(texts: List[str]) -> Optional[Any]:
    """
    Returns a similarity matrix using the best available method.

    Returns:
        numpy array of shape (n, n) with cosine similarities, or None if no good method available.
    """
    if len(texts) < 2:
        return None

    # 1. Best: Sentence embeddings
    model = _get_embedding_model()
    if model is not None:
        try:
            embeddings = model.encode(texts, show_progress_bar=False)
            sim_matrix = cosine_similarity(embeddings)
            return sim_matrix
        except Exception:
            pass  # fall through to next method

    # 2. Good fallback: TF-IDF + cosine
    if _SKLEARN_AVAILABLE:
        try:
            vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                max_features=5000
            )
            tfidf = vectorizer.fit_transform(texts)
            sim_matrix = sklearn_cosine(tfidf)
            return sim_matrix
        except Exception:
            pass

    # 3. No good semantic method available
    return None


def semantic_are_similar(
    text_a: str,
    text_b: str,
    threshold: float = 0.72
) -> bool:
    """
    Returns True if two texts are semantically similar above the threshold.
    Uses the best available embedding method.
    """
    sim_matrix = get_semantic_similarity([text_a, text_b])
    if sim_matrix is None:
        return False

    return float(sim_matrix[0, 1]) >= threshold


def enhance_clustering_with_semantics(
    patterns: List[str],
    current_similarity_func: Callable[[str, str], bool],
    semantic_threshold: float = 0.68
) -> Callable[[str, str], bool]:
    """
    Returns an enhanced similarity function that first tries semantic similarity,
    then falls back to the provided heuristic.

    This is the recommended way to integrate semantic clustering.
    """
    def enhanced_similarity(a: str, b: str) -> bool:
        # First try semantic (if available)
        if _SENTENCE_TRANSFORMERS_AVAILABLE or _SKLEARN_AVAILABLE:
            if semantic_are_similar(a, b, threshold=semantic_threshold):
                return True

        # Fallback to original heuristic
        return current_similarity_func(a, b)

    return enhanced_similarity


def is_semantic_available() -> bool:
    """Quick check if any semantic method is usable."""
    return _SENTENCE_TRANSFORMERS_AVAILABLE or _SKLEARN_AVAILABLE