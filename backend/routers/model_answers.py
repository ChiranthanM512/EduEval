from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ModelAnswer
from schema import ModelAnswerCreate, ModelAnswerOut, ModelAnswerUpdate

router = APIRouter(prefix="/model-answers", tags=["Model Answers"])


# ✅ GET all Model Answers
@router.get("/", response_model=list[ModelAnswerOut])
def get_model_answers(db: Session = Depends(get_db)):
    answers = db.query(ModelAnswer).all()
    return answers


# ✅ CREATE Model Answer
@router.post("/", response_model=ModelAnswerOut)
def create_model_answer(data: ModelAnswerCreate, db: Session = Depends(get_db)):
    new_answer = ModelAnswer(
        question_title=data.question_title,
        model_text=data.model_text
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


# ✅ DELETE Model Answer
@router.delete("/{answer_id}")
def delete_model_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(ModelAnswer).filter(ModelAnswer.id == answer_id).first()

    if not answer:
        raise HTTPException(status_code=404, detail="Model answer not found")

    db.delete(answer)
    db.commit()
    return {"message": "Model answer deleted successfully"}


# ✅ UPDATE Model Answer
@router.put("/{answer_id}", response_model=ModelAnswerOut)
def update_model_answer(answer_id: int, data: ModelAnswerUpdate, db: Session = Depends(get_db)):
    answer = db.query(ModelAnswer).filter(ModelAnswer.id == answer_id).first()

    if not answer:
        raise HTTPException(status_code=404, detail="Model answer not found")

    answer.question_title = data.question_title
    answer.model_text = data.model_text

    db.commit()
    db.refresh(answer)

    return answer
