SECRET_KEY = "EDUEVAL_SUPER_SECRET"
ALGORITHM = "HS256"

UPLOAD_DIR = "uploads"
MODEL_ANSWERS_DIR = "model_answers"
DB_PATH = "edueval.db"

MAX_FILE_MB = 10
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".pdf"]

# ✅ LOCAL AI CONFIG (Ollama)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"
SUPPORTED_LANGUAGES = ["en", "hi", "te", "ta", "mr", "bn"] # Add more as needed
