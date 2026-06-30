from pydantic import BaseModel, Field


class DetectedPattern(BaseModel):
    category: str
    keywords: list[str]
    files: list[str]


class RepoAnalysis(BaseModel):
    projectName: str
    source: str
    stack: list[str]
    patterns: list[DetectedPattern]
    fileCount: int
    sampledFiles: list[str]


class GeneratedDocuments(BaseModel):
    privacyPolicy: str
    termsOfService: str
    disclaimer: str = ""


class GenerateResponse(BaseModel):
    analysis: RepoAnalysis
    documents: GeneratedDocuments


class GithubAnalyzeRequest(BaseModel):
    githubUrl: str = Field(..., min_length=3, max_length=500, examples=["https://github.com/owner/repo"])


class AnalyzeResponse(BaseModel):
    analysis: RepoAnalysis
