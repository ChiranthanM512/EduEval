from config import MAX_FILE_MB, ALLOWED_EXTENSIONS
from utils import get_extension


def validate_upload(filename: str, file_size_bytes: int):
    ext = get_extension(filename)

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type: {ext}")

    size_mb = file_size_bytes / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        raise ValueError(f"File too large: {size_mb:.2f}MB (max {MAX_FILE_MB}MB)")
