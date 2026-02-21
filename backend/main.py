from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file in project root
load_dotenv()

from database import init_db
from routers import poems, about, comments, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Poetry Site API", lifespan=lifespan)

uploads_dir = os.getenv("UPLOADS_DIR", "/app/data/uploads/poems")
app.mount("/uploads", StaticFiles(directory=os.path.dirname(uploads_dir)), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(poems.router, prefix="/api/poems", tags=["poems"])
app.include_router(about.router, prefix="/api/about", tags=["about"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])

@app.get("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
