# EduEval Backend — Developer Setup

1. Create and activate a Python virtual environment (Windows Powershell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app (from the `backend` folder):

```powershell
uvicorn app:app --reload --port 8000
```

### 📑 Research Metrics & Benchmarking
To generate quantitative data for conference papers (CER, WER, Pearson Correlation):
```powershell
python generate_metrics.py
```
This benchmarks the live system performance on your current hardware.

## 📌 Notes
- The project requires packages listed in `requirements.txt` (FastAPI, SQLAlchemy, transformers, paddleocr, torch, OpenCV, etc.).
- If you only want to run basic API endpoints without heavy ML features, you can comment out or guard imports in `services/` that require large packages.
