import asyncio
from pathlib import Path

from app.services.analysisservice import analyzeZipUpload

zipPath = Path(__file__).resolve().parent.parent / "test-repo.zip"
data = zipPath.read_bytes()


async def main() -> None:
    analysis = await analyzeZipUpload(data, "test-repo.zip")
    print(analysis.projectName)
    print(analysis.stack)
    print([p.category for p in analysis.patterns])


asyncio.run(main())
