def keyword_missing_points(student_text: str, model_text: str) -> list:
    """
    Simple keyword-based missing points.
    Extracts important words from model answer and checks missing.
    """
    if not student_text or not model_text:
        return []

    model_words = set([w.lower() for w in model_text.split() if len(w) > 4])
    student_words = set([w.lower() for w in student_text.split() if len(w) > 4])

    missing = list(model_words - student_words)
    return missing[:10]
