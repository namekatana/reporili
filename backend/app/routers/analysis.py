from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.proxyauth import requireProxyAuth
from app.schemas.analysis import GenerateResponse, GithubAnalyzeRequest
from app.services.analysisservice import analyzeAndGenerateGithub, analyzeAndGenerateZip
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
