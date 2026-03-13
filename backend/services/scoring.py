import os
import sys
from sentence_transformers import SentenceTransformer, util

# Multilingual SBERT model
print("Loading SBERT Scoring model...")
embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Similarity below this means answer is fundamentally unrelated or too noisy
NOT_RELATED_THRESHOLD = 0.30


def semantic_score(student_text: str, model_text: str) -> dict:
    student_text = (student_text or "").strip()
    model_text = (model_text or "").strip()

    if not student_text or not model_text:
        return {"score": 0.0, "similarity": 0.0, "length_ratio": 0.0}

    # 1. Base SBERT Score (Semantic Similarity)
    emb1 = embedder.encode(student_text, convert_to_tensor=True)
    emb2 = embedder.encode(model_text, convert_to_tensor=True)

    similarity_tensor = util.cos_sim(emb1, emb2)
    sim = float(similarity_tensor.item())
    sim = max(0.0, min(sim, 1.0))

    if sim < NOT_RELATED_THRESHOLD:
        return {"score": 0.0, "similarity": round(sim, 4), "length_ratio": 0.0}

    # 2. Map similarity to a score.
    # We map NOT_RELATED_THRESHOLD (0.30) -> 0 and 1.0 -> 100.
    # Using a square-root curve (0.5 power) to reward partial knowledge fairly.
    normalized = (sim - NOT_RELATED_THRESHOLD) / (1.0 - NOT_RELATED_THRESHOLD)
    boosted_score = 100.0 * (normalized ** 0.5)

    # 3. Length Adjustment (very mild penalty for short answers)
    length_ratio = float(len(student_text) / max(len(model_text), 1))
    length_ratio = min(length_ratio, 1.0)
    
    final_score = boosted_score * (0.95 + 0.05 * length_ratio)

    return {
        "score": round(float(max(0.0, min(final_score, 100.0))), 2),
        "similarity": round(sim, 4),
        "length_ratio": round(length_ratio, 4)
    }
