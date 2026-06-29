from app.schemas.analysis import GenerateResponse, RepoAnalysis
from app.services.geminigenerator import generateDocuments
from app.services.githubclient import fetchRepoZipball
from app.services.patternmatcher import buildAnalysis
from app.services.repoparser import parseGithubUrl, parseZipArchive


async def analyzeZipUpload(data: bytes, filename: str | None = None) -> RepoAnalysis:
    projectName = filename.removesuffix(".zip") if filename else "project"
    parsed = parseZipArchive(data, projectName)
    return buildAnalysis(parsed, source="zip")


async def analyzeGithubRepo(githubUrl: str) -> RepoAnalysis:
    owner, repo, branch = parseGithubUrl(githubUrl)
    data = await fetchRepoZipball(owner, repo, branch)
    parsed = parseZipArchive(data, projectName=repo)
    return buildAnalysis(parsed, source=githubUrl)


async def analyzeAndGenerateZip(data: bytes, filename: str | None = None) -> GenerateResponse:
    analysis = await analyzeZipUpload(data, filename)
    documents = generateDocuments(analysis)
    return GenerateResponse(analysis=analysis, documents=documents)


async def analyzeAndGenerateGithub(githubUrl: str) -> GenerateResponse:
    analysis = await analyzeGithubRepo(githubUrl)
    documents = generateDocuments(analysis)
    return GenerateResponse(analysis=analysis, documents=documents)
