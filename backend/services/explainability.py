import re
import requests
from spellchecker import SpellChecker
from rapidfuzz import process, fuzz

OLLAMA_MODEL = "llama3.2:1b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# English spell checker — offline, no server needed
_en_spell = SpellChecker()

# Stopwords we never want to replace
_STOPWORDS = {
    "the", "a", "an", "in", "is", "it", "of", "on", "at", "to", "and",
    "or", "but", "for", "with", "are", "was", "were", "be", "been",
    "have", "has", "had", "that", "this", "these", "those", "by",
    "from", "as", "into", "through", "each", "some", "all", "not",
    "where", "when", "which", "who", "how", "what", "its", "their"
}


def _extract_model_vocabulary(model_text: str) -> list:
    """Extract meaningful words from model answer.
    Works for BOTH English (Latin) and Hindi (Devanagari) text."""
    # English words (length >= 4)
    english_words = re.findall(r'\b[a-zA-Z]{4,}\b', model_text)
    # Devanagari words (length >= 2 Devanagari chars — words are shorter in Hindi)
    hindi_words = re.findall(r'[\u0900-\u097F]{2,}', model_text)

    seen = set()
    vocab = []
    for w in english_words + hindi_words:
        lc = w.lower()
        if lc not in seen and lc not in _STOPWORDS:
            seen.add(lc)
            vocab.append(lc)
    return vocab


def _is_devanagari(text: str) -> bool:
    """Returns True if text contains primarily Devanagari characters."""
    deva = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    return deva > len(text) * 0.3


def _vocabulary_guided_correction(ocr_text: str, model_text: str) -> str:
    """
    Fixes whole-word OCR substitutions using character-level fuzzy matching
    against the model answer vocabulary.
    Works for BOTH English and Hindi (Devanagari) text.
    """
    if not model_text or not ocr_text:
        return ocr_text

    model_vocab = _extract_model_vocabulary(model_text)
    if not model_vocab:
        return ocr_text

    # Separate English and Hindi vocabularies for targeted matching
    en_vocab = [w for w in model_vocab if all(c.isascii() for c in w)]
    hi_vocab = [w for w in model_vocab if _is_devanagari(w)]

    words = ocr_text.split()
    corrected = []

    for word in words:
        # Preserve punctuation attached to word
        stripped = word.strip(".,;:!?()।")
        suffix = word[len(stripped):]

        if not stripped:
            corrected.append(word)
            continue

        lower = stripped.lower()
        is_hindi_word = _is_devanagari(stripped)

        if is_hindi_word:
            # Hindi word: match against Hindi model vocabulary
            if not hi_vocab or stripped in hi_vocab:
                corrected.append(word)
                continue
            result = process.extractOne(
                stripped, hi_vocab,
                scorer=fuzz.ratio,
                score_cutoff=65  # slightly higher for Hindi — words are shorter
            )
        else:
            # English word
            if (not stripped.isalpha() or len(stripped) < 4
                    or lower in _STOPWORDS or lower in en_vocab):
                corrected.append(word)
                continue
            result = process.extractOne(
                lower, en_vocab,
                scorer=fuzz.ratio,
                score_cutoff=60
            )

        if result:
            replacement = result[0]
            # For English: preserve capitalisation
            if not is_hindi_word and stripped[0].isupper():
                replacement = replacement.capitalize()
            corrected.append(replacement + suffix)
        else:
            corrected.append(word)

    return " ".join(corrected)


def _correct_minor_typos(text: str, model_text: str = "") -> str:
    """
    Fast word-by-word spell correction using pyspellchecker.
    Only fixes words NOT in English dictionary (e.g., 'relibale' → 'reliable').
    Uses model vocabulary as domain-specific override.
    """
    if not text:
        return text

    # Expand spell checker with model answer words as correct domain vocabulary
    if model_text:
        domain_words = re.findall(r'\b[a-zA-Z]{4,}\b', model_text)
        _en_spell.word_frequency.load_words(domain_words)

    words = text.split()
    misspelled = _en_spell.unknown(words)
    corrected = []

    for word in words:
        lower = word.lower()
        if (word.isdigit()
                or len(word) <= 2
                or word[0].isupper()
                or lower in _STOPWORDS
                or lower not in misspelled):
            corrected.append(word)
        else:
            suggestion = _en_spell.correction(lower)
            corrected.append(suggestion if suggestion else word)

    return " ".join(corrected)


def refine_ocr_text(ocr_text: str, lang_hint: str = "english", model_text: str = "") -> str:
    """
    OCR text refinement using free open-source tools:

    English:
      Pass 1: pyspellchecker  → obvious letter-substitution typos
      Pass 2: rapidfuzz vocab → whole-word substitutions using model vocabulary

    Hindi/other:
      Pass 1: rapidfuzz Devanagari vocab → fixes OCR word errors against model vocabulary
      Pass 2: Ollama (optional)          → deeper cleanup if server is running
    """
    if not ocr_text or len(ocr_text.strip()) < 3:
        return ocr_text

    if lang_hint != "english":
        # Pass 1: vocabulary-guided correction using model answer words (works for Hindi too)
        text = _vocabulary_guided_correction(ocr_text, model_text)
        # Pass 2: Ollama (optional — falls back if refused or offline)
        text = _correct_via_ollama(text, model_text=model_text, lang_hint=lang_hint)
        return text

    # English Pass 1: minor typo correction
    text = _correct_minor_typos(ocr_text, model_text=model_text)

    # English Pass 2: vocabulary-guided whole-word correction
    text = _vocabulary_guided_correction(text, model_text)

    return text


# Phrases that indicate Ollama refused instead of correcting
_OLLAMA_REFUSAL_PHRASES = (
    "i can't", "i cannot", "i'm unable", "i am unable",
    "i don't", "i do not", "i'm not able", "i won't",
    "i will not", "sorry", "i apologize", "as an ai",
    "i'm an ai", "i am an ai"
)


def _correct_via_ollama(ocr_text: str, model_text: str = "", lang_hint: str = "english") -> str:
    """Ollama refinement — only used for non-English. Falls back silently on refusal or error."""
    if not ocr_text or len(ocr_text.strip()) < 3:
        return ocr_text

    if lang_hint == "english":
        topic = f"TOPIC CONTEXT:\n{model_text[:200]}\n\n" if model_text else ""
        prompt = (
            f"Task: Fix OCR errors in the following student answer text.\n"
            f"{topic}"
            f"Rules: Only fix obvious OCR mistakes. Do not add or remove content. "
            f"Output the corrected text only.\n\n"
            f"Input: {ocr_text}\n\nOutput:"
        )
    else:
        prompt = (
            f"Fix OCR errors in this Hindi text. Correct broken characters only. "
            f"Do not translate. Output the corrected Hindi text only.\n\n"
            f"Input: {ocr_text}\n\nOutput:"
        )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30
        )
        if response.status_code == 200:
            cleaned = response.json().get("response", "").strip().strip('"\'')

            # Detect and discard LLM refusal messages
            cleaned_lower = cleaned.lower()
            if any(cleaned_lower.startswith(phrase) for phrase in _OLLAMA_REFUSAL_PHRASES):
                return ocr_text  # Return original — Ollama refused

            # Only accept if plausible length
            if cleaned and len(cleaned) < len(ocr_text) * 2.5:
                return cleaned
    except Exception:
        pass  # Ollama not running — silently fall back

    return ocr_text


def explain_answer(student_text: str, model_text: str) -> dict:
    """Generate structured explanation using local Ollama."""
    prompt = f"""Compare the student answer with the model answer and explain the evaluation.

MODEL ANSWER:
{model_text}

STUDENT ANSWER:
{student_text}

Explain:
1. What the student answered correctly
2. What important points are missing
3. Suggestions to improve the answer

Provide the response in clear Markdown."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120
        )
        if response.status_code == 200:
            return {"explanation": response.json().get("response", "No response generated.")}
        return {"explanation": f"Ollama error ({response.status_code}): {response.text}"}
    except Exception as e:
        return {"explanation": f"Explainability failed: Ollama server not running.\nError: {e}"}