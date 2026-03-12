import os
import sys
from sentence_transformers import SentenceTransformer, util

# Multilingual SBERT model
print("Loading SBERT Scoring model...")
embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Similarity below this means answer is fundamentally unrelated
NOT_RELATED_THRESHOLD = 0.22


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

    # 2. Boost: map similarity to a more intuitive educational grade range.
    # SBERT cosine similarity of 0.65+ semantically means the student knows the concept.
    # We map 0.22 -> 20 and 1.0 -> 100 with a power curve that rewards higher similarity.
    # Using: score = 20 + 80 * ((sim - 0.22) / (1.0 - 0.22)) ^ 0.7
    normalized = (sim - NOT_RELATED_THRESHOLD) / (1.0 - NOT_RELATED_THRESHOLD)
    boosted_score = 20.0 + 80.0 * (normalized ** 0.7)

    # 3. Length Adjustment (mild penalty if answer is very short, no penalty if long)
    length_ratio = float(len(student_text) / max(len(model_text), 1))
    length_ratio = min(length_ratio, 1.0)
    
    final_score = boosted_score * (0.85 + 0.15 * length_ratio)

    return {
        "score": round(float(max(0.0, min(final_score, 100.0))), 2),
        "similarity": round(sim, 4),
        "length_ratio": round(length_ratio, 4)
    }
