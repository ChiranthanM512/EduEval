from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from PIL import Image
import io

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_TYPES = {"application/pdf", "image/png", "image/jpeg"}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_file(file: UploadFile):
    ext = Path(file.filename).suffix.lower()

    # 1) extension validation
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}"
        )

    # 2) content-type validation
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type: {file.content_type}"
        )

    return ext


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = validate_file(file)

    # read file bytes
    data = await file.read()

    # 3) file size check
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max allowed is {MAX_FILE_SIZE / (1024*1024)} MB"
        )

    # 4) real PDF check
    if ext == ".pdf" and not data.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Not a valid PDF file.")

    # 5) real image check
    if ext in [".jpg", ".jpeg", ".png"]:
        try:
            Image.open(io.BytesIO(data)).verify()
        except:
            raise HTTPException(status_code=400, detail="Not a valid image file.")

    # 6) safe unique filename
    safe_name = f"{uuid.uuid4().hex}{ext}"
    save_path = UPLOAD_DIR / safe_name

    # save file
    with open(save_path, "wb") as f:
        f.write(data)

    return {"filename": safe_name, "path": str(save_path)}
