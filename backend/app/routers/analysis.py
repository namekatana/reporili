from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.proxyauth import requireProxyAuth
from app.schemas.analysis import AnalyzeResponse, GenerateResponse, GithubAnalyzeRequest
from app.services.analysisservice import (
    analyzeAndGenerateGithub,
    analyzeAndGenerateZip,
    analyzeGithubRepo,
    analyzeZipUpload,
)
from app.services.geminigenerator import GeminiGeneratorError
from app.uploadlimits import readZipUpload

router = APIRouter(
    prefix="/api",
    tags=["analysis"],
    dependencies=[Depends(requireProxyAuth)],
)


def _requireZipName(filename: str | None) -> None:
    if not filename or not filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Upload a .zip archive")


@router.post("/analyze/zip", response_model=AnalyzeResponse)
async def analyzeZip(file: UploadFile = File(...)) -> AnalyzeResponse:
    _requireZipName(file.filename)
    data = await readZipUpload(file)

    try:
        analysis = await analyzeZipUpload(data, file.filename)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid archive") from None
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to parse ZIP archive") from None

    return AnalyzeResponse(analysis=analysis)


@router.post("/analyze/github", response_model=AnalyzeResponse)
async def analyzeGithub(body: GithubAnalyzeRequest) -> AnalyzeResponse:
    try:
        analysis = await analyzeGithubRepo(body.githubUrl)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL") from None
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to fetch repository") from None

    return AnalyzeResponse(analysis=analysis)


@router.post("/generate/zip", response_model=GenerateResponse)
async def generateFromZip(file: UploadFile = File(...)) -> GenerateResponse:
    _requireZipName(file.filename)
    data = await readZipUpload(file)

    try:
        return await analyzeAndGenerateZip(data, file.filename)
    except GeminiGeneratorError:
        raise HTTPException(status_code=503, detail="Document generation unavailable") from None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid archive") from None
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to process ZIP archive") from None


@router.post("/generate/github", response_model=GenerateResponse)
async def generateFromGithub(body: GithubAnalyzeRequest) -> GenerateResponse:
    try:
        return await analyzeAndGenerateGithub(body.githubUrl)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL") from None
    except GeminiGeneratorError:
        raise HTTPException(status_code=503, detail="Document generation unavailable") from None
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to process repository") from None
