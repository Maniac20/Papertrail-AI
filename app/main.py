from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.core.config import get_settings
from app.api.routes.documents import router as documents_router
from app.api.routes.query import router as query_router

@asynccontextmanager
async def lifespan(app):
    get_settings().prepare_directories()
    yield

app = FastAPI(
    title="AI Research & Document Intelligence",
    version="1.1.0",
    description="Upload PDFs and ask grounded questions with page citations.",
    lifespan=lifespan,
)
app.include_router(documents_router)
app.include_router(query_router)

@app.get("/", include_in_schema=False)
async def dashboard():
    return FileResponse(Path(__file__).resolve().parent.parent / "ui" / "index.html")

@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok", "service": "document-intelligence"}
