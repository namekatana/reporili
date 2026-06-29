from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.analysis import AnalyzeResponse, GenerateResponse, GithubAnalyzeRequest
from app.services.analysisservice import (
    analyzeAndGenerateGithub,
    analyzeAndGenerateZip,
    analyzeGithubRepo,
    analyzeZipUpload,
)
from app.services.geminigenerator import GeminiGeneratorError

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze/zip", response_model=AnalyzeResponse)
async def analyzeZip(file: UploadFile = File(...)) -> AnalyzeResponse:
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Upload a .zip archive")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        analysis = await analyzeZipUpload(data, file.filename)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to parse ZIP: {exc}") from exc

    return AnalyzeResponse(analysis=analysis)


@router.post("/analyze/github", response_model=AnalyzeResponse)
async def analyzeGithub(body: GithubAnalyzeRequest) -> AnalyzeResponse:
    try:
        analysis = await analyzeGithubRepo(body.githubUrl)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch repository: {exc}") from exc

    return AnalyzeResponse(analysis=analysis)


@router.post("/generate/zip", response_model=GenerateResponse)
async def generateFromZip(file: UploadFile = File(...)) -> GenerateResponse:
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Upload a .zip archive")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        return await analyzeAndGenerateZip(data, file.filename)
    except GeminiGeneratorError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to process ZIP: {exc}") from exc


@router.post("/generate/github", response_model=GenerateResponse)
async def generateFromGithub(body: GithubAnalyzeRequest) -> GenerateResponse:
    try:
        return await analyzeAndGenerateGithub(body.githubUrl)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except GeminiGeneratorError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to process repository: {exc}") from exc
