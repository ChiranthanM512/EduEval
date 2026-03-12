import re


def extract_keywords(model_text: str):
    # simple keyword extraction (demo level)
    words = re.findall(r"[A-Za-z]{4,}", model_text.lower())
    words = list(set(words))
    words = sorted(words, key=len, reverse=True)
    return words[:10]


def matched_keywords(student_text: str, model_text: str):
    keys = extract_keywords(model_text)
    student_lower = student_text.lower()

    matched = []
    for k in keys:
        if k in student_lower:
            matched.append(k)

    return matched


def missing_keywords(student_text: str, model_text: str):
    keys = extract_keywords(model_text)
    student_lower = student_text.lower()

    missing = []
    for k in keys:
        if k not in student_lower:
            missing.append(k)

    return missing


def gen_feedback(score: float):
    if score == 0:
        return "Not related to the topic."
    if score >= 90:
        return "Excellent answer. Very close to the model answer."
    elif score >= 75:
        return "Good answer, but a few points are missing."
    elif score >= 55:
        return "Average answer. Improve explanation and include key points."
    
    elif score >= 30:
        return "Needs improvement. Many important points are missing."
    else:
        return "Poor answer or doesn't match the model answer. Consider revising the material and trying again."
   

