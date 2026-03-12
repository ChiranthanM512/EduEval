from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schema import UserCreate, Login
from services.users import create_user, get_user, verify_password
from utils import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.username):
        raise HTTPException(status_code=409, detail="User already exists")
    created = create_user(db, user.username, user.password)
    return {"message": "User registered", "id": created.id}


@router.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    db_user = get_user(db, user.username)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
