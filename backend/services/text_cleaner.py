import re
import unicodedata


def fix_devanagari_spaces(text: str) -> str:
    """
    EasyOCR sometimes splits a single Devanagari COMBINING MARK (matra/virama)
    away from its base consonant with a stray space.
    This function only merges a character with a following COMBINING mark —
    it does NOT merge regular word boundaries.

    Devanagari combining marks (Mn / Mc / Cf categories):
      U+0900-U+0903  (nasalization, visarga)
      U+093A-U+094F  (vowel signs / matras, virama/halant)
      U+0951-U+0957  (stress marks)
      U+0962-U+0963  (vowel signs for vocalic r/l)
    """
    # Only merge when the NEXT character is a combining mark, NOT a standalone consonant/vowel
    combining_pattern = re.compile(
        r'([\u0900-\u097F])\s+([\u0900-\u0903\u093A-\u094F\u0951-\u0957\u0962-\u0963])'
    )
    for _ in range(10):
        new = combining_pattern.sub(r'\1\2', text)
        if new == text:
            break
        text = new
    return text


def clean_text(text: str, lang_hint: str = "english") -> str:
    if not text:
        return ""

    # 1) Normalize newlines to space
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # 2) Remove dot noise between words: "word . word"  (ASCII dot only)
    text = re.sub(r"(?<!\d)\.(?!\d)", " ", text)

    # 3) Remove unwanted symbols — PRESERVE:
    #    \w             → ASCII/Unicode word chars (letters, digits, underscore)
    #    \u0900-\u097F  → Full Devanagari block INCLUDING combining marks (matras)
    #    \s             → spaces
    #    common punctuation + Devanagari dandas (। ॥)
    text = re.sub(
        r"[^\w\u0900-\u097F\s,.;:!?()\u0964\u0965\-]",
        " ",
        text,
        flags=re.UNICODE
    )

    # 4) Remove repeated punctuation
    text = re.sub(r"([,.;:!?])\1+", r"\1", text)

    # 5) Fix ONLY stray combining-mark splits in Devanagari (NOT word borders)
    if any('\u0900' <= c <= '\u097F' for c in text):
        text = fix_devanagari_spaces(text)

    # 6) Final normalize
    text = re.sub(r"\s+", " ", text).strip()

    return text
