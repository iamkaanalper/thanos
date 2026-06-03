"""
Pure text normalization utilities for Sleuth router and other components.

Separated so it can be imported without triggering package relative imports
during direct test execution or lightweight usage.
"""


def normalize_text(text: str) -> str:
    """Basit Türkçe karakter normalizasyonu + lower (for routing / matching)."""
    text = text.lower()
    replacements = {
        "ı": "i", "ş": "s", "ğ": "g", "ü": "u", "ö": "o", "ç": "c",
        "İ": "i", "Ş": "s", "Ğ": "g", "Ü": "u", "Ö": "o", "Ç": "c",
    }
    for tr, en in replacements.items():
        text = text.replace(tr, en)
    return text


# Backwards-compatible alias used by router.py
_normalize_text = normalize_text