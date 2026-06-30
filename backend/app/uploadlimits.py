from fastapi import HTTPException, UploadFile

from app.config import settings


async def readZipUpload(file: UploadFile) -> bytes:
    data = await file.read(settings.maxUploadBytes + 1)
    if len(data) > settings.maxUploadBytes:
        raise HTTPException(status_code=413, detail="Archive exceeds size limit")
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")
    return data
