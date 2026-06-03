"""
Regression tests for Sleuth Router i18n normalization.

This protects the critical fix from Post-MVE Item 1 (Senaryo A live test failure
where pure Turkish input produced score=0 before _normalize_text was added).

Note: Full end-to-end recommendation tests require running inside the package
context (e.g. pytest with proper PYTHONPATH or as part of larger test suite)
because router.py uses relative imports.

Run: python .grok/bundled/skills/shared/sleuth/router_test.py
"""

import sys
from pathlib import Path

# Make the pure normalization importable for direct test run (no relative import problems)
pkg_dir = Path(__file__).parent
sys.path.insert(0, str(pkg_dir))

from normalize import normalize_text as _normalize_text


def test_normalize_text_turkish_chars():
    """Basic sanity for the normalization function added in Item 1."""
    text = "Bu state corruption bug'ını kök nedenini bulmam lazım"
    normalized = _normalize_text(text)
    assert "ı" not in normalized
    assert "ğ" not in normalized
    assert "ç" not in normalized
    assert "state corruption" in normalized.lower()
    assert "kok neden" in normalized.lower()  # ı → i, ğ → g


def test_senaryo_a_style_turkish_normalization():
    """
    Regression case based on the exact problematic Turkish input from Senaryo A.
    The normalization must turn Turkish chars into ASCII equivalents so that
    the existing triggers (kök neden, root cause, race condition, etc.) can match.
    """
    problematic_input = "Bu state corruption bug'ını kök nedenini bulmam lazım"
    normalized = _normalize_text(problematic_input)

    # Critical assertions for the original failure mode
    assert "kok neden" in normalized
    assert "state corruption" in normalized
    assert "bug" in normalized

    # Also test uppercase Turkish chars
    upper = _normalize_text("KÖK NEDENİ BUL")
    assert "kok neden" in upper


if __name__ == "__main__":
    test_normalize_text_turkish_chars()
    test_senaryo_a_style_turkish_normalization()
    print("All router i18n normalization regression tests PASSED.")