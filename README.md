# 🎓 EduEval: AI-Powered Exam Evaluation System

**EduEval** (formerly EduEvalve) is a free, open-source, and **local-first** AI evaluation platform. It automates the grading of handwritten answer sheets using a hybrid OCR pipeline, semantic similarity scoring, and AI-generated feedback—all running entirely on your local hardware for 100% privacy and zero API costs.

---

## 🏗️ System Architecture

EduEval follows a modular **5-Stage Evaluation Pipeline** to ensure accuracy even with imperfect handwriting.

```mermaid
graph TD
    User([Handwritten Answer Sheet]) --> UI[React Frontend]
    UI --> API[FastAPI Backend]
    
    subgraph "Evaluation Intelligence (Local)"
        API --> S1[Stage 1: Image Preprocessing]
        S1 --> S2[Stage 2: Hybrid OCR Extraction]
        S2 --> S3[Stage 3: Vocabulary-Guided Correction]
        S3 --> S4[Stage 4: Semantic Scoring]
        S4 --> S5[Stage 5: Local AI Feedback]
    end
    
    API <--> DB[(SQLite Database)]
    S5 --> UI
```

### 🧠 The Intelligence Layer

1.  **Hybrid OCR**: Combines **TrOCR** (English handwriting) and **EasyOCR** (Indic languages & layout) for superior text extraction.
2.  **Vocabulary-Guided Correction**: Replaces garbled OCR text with likely correct terms from the *Model Answer* using **RapidFuzz** (Levenshtein distance).
3.  **Semantic Scoring**: Uses **SBERT** (`sentence-transformers`) to grade answers based on meaning and context, rather than just exact word matches.
4.  **Local AI Feedback**: Integrates **Ollama (Llama 3.2)** and **T5-Small** to generate detailed performance explanations and identify missing keywords.

---

## 🛠️ Technology Stack

-   **Frontend**: React, Vite, Framer Motion (for animations).
-   **Backend**: FastAPI, SQLAlchemy (SQLite).
-   **AI Infrastructure**: 
    -   OCR: `microsoft/trocr-base-handwritten`, `EasyOCR`.
    -   NLP: `sentence-transformers` (paraphrase-multilingual-MiniLM-L12-v2).
    -   LLM: `Ollama` (Llama 3.2).
-   **Libraries**: OpenCV, RapidFuzz, PySpellChecker, PyMuPDF.

---

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.9+
- Node.js 18+
- [Ollama](https://ollama.com/) (Required for AI feedback)
- **Poppler** (Required for PDF processing)

### 1. External Dependencies Setup

#### 🤖 Ollama (Local LLM)
1. **Install**: Download and install from [ollama.com](https://ollama.com/).
2. **Start Service**: Ensure the Ollama application is running in your system tray.
3. **Pull Model**: Open your terminal and run:
   ```bash
   ollama pull llama3.2
   ```

#### 📄 Poppler (PDF Support)
1. **Windows**: 
   - Download the latest binary from [Github (OSGeo)](https://github.com/oschwartz10612/poppler-windows/releases/).
   - Extract the folder (e.g., to `C:\poppler`).
   - Add the `bin/` directory to your system **Environment Variables (PATH)**.
2. **Mac**: `brew install poppler`
3. **Linux**: `sudo apt install poppler-utils`

---

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 4. Model Preparation
On first run, the system will download TrOCR and SBERT models (requires internet). Ensure Ollama is running (`ollama run llama3.2`) to enable the evaluation feedback.

---

## 📂 Project Structure

```text
EduEval/
├── backend/            # FastAPI Server & AI Services
│   ├── routers/        # API Endpoints (Auth, Eval, Results)
│   ├── services/       # OCR, Scoring, and Feedback Logic
│   └── models.py       # DB Schema (SQLAlchemy)
├── frontend/           # React Application
│   └── src/components/ # UI Modules (Upload, Results, Navbar)
├── architecture.png    # High-level design diagram
└── setup_instructions.md # Detailed installation guide
```

---

## ⚖️ License
This project is open-source and free for educational use. 
