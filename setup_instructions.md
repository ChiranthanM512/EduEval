# 📌 EduEval – Setup Instructions

## 1️⃣ Project Overview

EduEval is an AI-powered evaluation system that:

- Accepts user input (PDF/Text/Image)
- Processes responses using NLP/ML models
- Compares with model answers
- Generates evaluation results
- Stores results in a database
- Provides Explainable AI insights
- Displays results in the frontend

---

## 🖥️ System Requirements

- Python 3.9 or above
- Node.js 18 or above
- pip
- Git
- (Optional) CUDA-enabled GPU for faster inference

---

## 📂 Step 1: Clone the Repository

```bash
git clone <your-repository-link>
cd project-root
```

---

# 🐍 Backend Setup

Navigate to backend folder:

```bash
cd backend
```

## Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt fails, install manually:

```bash
pip install fastapi uvicorn torch transformers pdf2image pillow scikit-learn pandas numpy sqlalchemy
```

---

## 🤖 Step 4: Model Setup

The system uses Transformer-based NLP models for evaluation and explainability.

Example model loading:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "microsoft/Phi-3-mini-4k-instruct"
```

⚠️ Internet connection is required during first run to download models.

If using GPU:

```python
device_map="auto"
torch_dtype="auto"
```

To check GPU availability:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 🗄️ Step 5: Database Setup

This project uses **SQLite** database.

Database file:
```
backend/edueval.db
```

The database will be created automatically on first run if not present.

If migrations are required:

```bash
python db_migrate_add_explainable_ai.py
```

---

## 🚀 Step 6: Run Backend Server

From inside the `backend` folder:

```bash
uvicorn app:app --reload
```

Backend will run at:

```
http://127.0.0.1:8000
```

API docs available at:

```
http://127.0.0.1:8000/docs
```

---

# 🌐 Frontend Setup

Open a new terminal.

Navigate to frontend folder:

```bash
cd frontend
```

## Install Dependencies

```bash
npm install
```

## Run Frontend

```bash
npm start
```

Frontend will run at:

```
http://localhost:3000
```

---

# 🔄 System Workflow

1. User uploads answer (PDF/Text)
2. Backend processes input
3. Model compares with model answers
4. Explainable AI generates justification
5. Result is stored in SQLite database
6. Frontend displays marks + explanation

---

# 📁 Project Structure

```
project-root/
│
├── backend/
│   ├── __pycache__/
│   ├── database/
│   ├── model_answers/
│   ├── routers/
│   ├── services/
│   ├── uploads/
│   ├── venv/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── db_migrate_add_explainable_ai.py
│   ├── edueval.db
│   ├── models.py
│   ├── schema.py
│   ├── utils.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── README.md
│
├── architecture.png
├── demo_video_link.txt
└── .gitignore
```

---

# 🛠️ Common Issues & Fixes

### 1️⃣ Uvicorn Not Found
```
pip install uvicorn
```

### 2️⃣ Torch CUDA Error
- Ensure correct CUDA version installed
- Or run on CPU (default)

### 3️⃣ pdf2image Error
Install Poppler:

Windows:
- Download Poppler and add to PATH

Mac:
```
brew install poppler
```

---

# ✅ Setup Complete

1. Start backend
2. Start frontend
3. Open browser at http://localhost:3000
4. Upload answer and test evaluation system

---

# 🎯 Notes

- Make sure backend is running before starting frontend.
- Ensure correct Python version.
- First model download may take a few minutes.