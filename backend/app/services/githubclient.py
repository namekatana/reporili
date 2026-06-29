import httpx

from app.config import settings


async def fetchRepoZipball(owner: str, repo: str, branch: str | None = None) -> bytes:
    ref = branch or "HEAD"
    url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{ref}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Reporili/1.0",
    }
    if settings.githubToken:
        headers["Authorization"] = f"Bearer {settings.githubToken}"

    async with httpx.AsyncClient(follow_redirects=True, timeout=120.0) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404 and branch is None:
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/zipball/main",
                headers=headers,
            )
        response.raise_for_status()
        return response.content
