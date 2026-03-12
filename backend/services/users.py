from sqlalchemy.orm import Session
from models import User
import bcrypt
import hashlib


def _prehash_password(password: str) -> bytes:
    """
    bcrypt supports max 72 bytes.
    Truncate the password to 72 bytes before encoding.
    Then SHA256 first (fixed length), then bcrypt.
    """
    # Truncate to 72 bytes to respect bcrypt's limitation
    password_bytes = password.encode("utf-8")[:72]
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    return sha256_hash.encode("utf-8")


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str):
    safe_pw = _prehash_password(password)
    hashed = bcrypt.hashpw(safe_pw, bcrypt.gensalt())
    user = User(username=username, password=hashed.decode("utf-8"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(password: str, hashed_password: str):
    safe_pw = _prehash_password(password)
    return bcrypt.checkpw(safe_pw, hashed_password.encode("utf-8"))
