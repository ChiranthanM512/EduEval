from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils import get_db
from schema import EvaluateRequest, EvaluateResponse
from models import ModelAnswer, Result

from services.hybrid_ocr import hybrid_ocr
from services.scoring import semantic_score
from services.feedback import gen_feedback, missing_keywords, matched_keywords
from services.text_cleaner import clean_text
from services.explainability import explain_answer, refine_ocr_text

import json
import os


router = APIRouter(prefix="/eval", tags=["Evaluation"])


@router.post("/", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest, db: Session = Depends(get_db)):

    # 1️⃣ Load model answer
    model_ans = db.query(ModelAnswer).filter(
        ModelAnswer.id == req.model_answer_id
    ).first()

    if not model_ans:
        raise HTTPException(status_code=404, detail="Model answer not found")

    # 2️⃣ OCR — language is auto-detected from model answer text
    extracted_text = hybrid_ocr.extract_text(req.file_path, hint_text=model_ans.model_text)

    engine = "HybridOCR"
    lang = "auto"

    # Clean raw OCR output (preserves non-English Unicode)
    extracted_text = clean_text(extracted_text)

    # Refine OCR text using local Ollama with model-answer context
    lang_hint = hybrid_ocr.detect_dominant_language(model_ans.model_text)
    refined_text = refine_ocr_text(extracted_text, lang_hint=lang_hint, model_text=model_ans.model_text)
    if refined_text:
        extracted_text = refined_text

    if not extracted_text or len(extracted_text.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="OCR failed: no readable text found"
        )

    # 3️⃣ Semantic score (pure SBERT)
    scoring_result = semantic_score(extracted_text, model_ans.model_text)
    score = scoring_result["score"]

    # 4️⃣ Feedback
    fb = gen_feedback(score)

    # 5️⃣ Keywords
    missing = missing_keywords(extracted_text, model_ans.model_text)
    matched = matched_keywords(extracted_text, model_ans.model_text)

    # 6️⃣ Explainable AI (using local Ollama)
    if score > 0:
        explainable_ai = explain_answer(extracted_text, model_ans.model_text)
    else:
        explainable_ai = {
            "explanation": "### Evaluation Result: Zero Marks\n\nThe submitted answer is not related to the expected model answer or topic. No marks have been assigned."
        }

    # Merge similarity and length ratio for frontend display
    explainable_ai["similarity"] = scoring_result["similarity"]
    explainable_ai["length_ratio"] = scoring_result["length_ratio"]

    # 7️⃣ Save result
    row = Result(
        file_path=req.file_path,
        extracted_text=extracted_text,
        ocr_engine=engine,
        language=lang,
        score=score,
        feedback=fb,
        missing_keywords=",".join(missing) if missing else None,
        matched_keywords=",".join(matched) if matched else None,
        explainable_output=json.dumps(explainable_ai),
        model_answer_id=model_ans.id
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    # 8️⃣ Delete uploaded files
    if os.path.exists(req.file_path):
        os.remove(req.file_path)

    clean_path = req.file_path.replace(".", "_clean.")
    if os.path.exists(clean_path):
        os.remove(clean_path)

    # 9️⃣ Return response
    return {
        "text": extracted_text,
        "score": score,
        "feedback": fb,
        "language": lang,
        "ocr_engine": engine,
        "missing_keywords": missing,
        "matched_keywords": matched,
        "explainable_ai": explainable_ai
    }