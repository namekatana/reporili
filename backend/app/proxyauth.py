from fastapi import Header, HTTPException

from app.config import settings


def requireProxyAuth(
    xReporiliProxy: str | None = Header(default=None, alias="X-Reporili-Proxy"),
) -> None:
    secret = settings.proxySecret
    if not secret:
        return
    if xReporiliProxy != secret:
        raise HTTPException(status_code=403, detail="Forbidden")
