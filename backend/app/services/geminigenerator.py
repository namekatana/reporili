import google.generativeai as genai

from app.config import settings
from app.schemas.analysis import GeneratedDocuments, RepoAnalysis
from app.services.patternmatcher import buildAnalysisSummary


class GeminiGeneratorError(Exception):
    pass


def generateDocuments(analysis: RepoAnalysis) -> GeneratedDocuments:
    if not settings.geminiApiKey:
        raise GeminiGeneratorError("GEMINI_API_KEY is not configured")

    genai.configure(api_key=settings.geminiApiKey)
    model = genai.GenerativeModel(settings.geminiModel)
    summary = buildAnalysisSummary(analysis)
    prompt = _buildPrompt(analysis.projectName, summary, analysis)

    try:
        response = model.generate_content(prompt)
        text = response.text
    except Exception as exc:
        raise GeminiGeneratorError(f"Gemini API error: {exc}") from exc

    return _parseResponse(text)


def _buildPrompt(projectName: str, summary: str, analysis: RepoAnalysis) -> str:
    hasPayments = any(p.category == "payments" for p in analysis.patterns)
    paymentNote = (
        "Include a dedicated Payment and Billing section covering subscriptions, refunds, and third-party payment processors."
        if hasPayments
        else ""
    )

    return f"""You are a legal document drafter for software products. Generate project-specific legal documents based ONLY on the code analysis below. Do not use generic boilerplate — tailor every section to what the code actually does.

Project name: {projectName}

Code analysis:
{summary}

{paymentNote}

Output format — use exactly these markdown headers:

## Privacy Policy
(full document)

## Terms of Service
(full document)

## Disclaimer
(short disclaimer that documents are AI-generated drafts, not legal advice)

Rules:
- Write in clear English
- Reference specific technologies found (auth, payments, analytics, etc.)
- If a data practice was NOT detected, do not claim it exists
- Use markdown formatting
- Be thorough but concise (each main document 800-1500 words)
"""


def _parseResponse(text: str) -> GeneratedDocuments:
    sections = {
        "privacyPolicy": _extractSection(text, "Privacy Policy"),
        "termsOfService": _extractSection(text, "Terms of Service"),
        "disclaimer": _extractSection(text, "Disclaimer"),
    }

    if not sections["privacyPolicy"] and not sections["termsOfService"]:
        sections["privacyPolicy"] = text.strip()

    return GeneratedDocuments(**sections)


def _extractSection(text: str, title: str) -> str:
    marker = f"## {title}"
    start = text.find(marker)
    if start == -1:
        return ""

    start += len(marker)
    nextHeader = text.find("\n## ", start)
    body = text[start:nextHeader] if nextHeader != -1 else text[start:]
    return body.strip()
