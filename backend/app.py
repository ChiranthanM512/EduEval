from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base


from routers.auth import router as auth_router
from routers.upload import router as upload_router
from routers.evaluate import router as eval_router
from routers.results import router as results_router
from routers.model_answers import router as model_answers_router
# (upload router already imported above)

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduEvalve API")

# CORS (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(model_answers_router)
app.include_router(eval_router)
app.include_router(results_router)


@app.get("/")
def root():
    return {"message": "EduEvalve backend is running"}
