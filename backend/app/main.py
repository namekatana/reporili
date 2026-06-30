import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import analysis

isProduction = os.getenv("ENVIRONMENT", "production") == "production"

app = FastAPI(
    title="Reporili",
    version="0.1.0",
    docs_url=None if isProduction else "/docs",
    redoc_url=None if isProduction else "/redoc",
    openapi_url=None if isProduction else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowedOrigins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

app.include_router(analysis.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
