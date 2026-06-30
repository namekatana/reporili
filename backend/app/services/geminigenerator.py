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
    detectedCategories = [p.category for p in analysis.patterns]
    sectionNotes: list[str] = []

    if "payments" in detectedCategories:
        sectionNotes.append("- Include Payment and Billing terms (subscriptions, refunds, third-party processors).")
    else:
        sectionNotes.append("- Do NOT include payment, billing, or subscription sections.")

    if "auth" in detectedCategories:
        sectionNotes.append("- Include account registration, authentication, and credential handling sections.")
    else:
        sectionNotes.append("- Do NOT include user accounts or login sections unless required for a detected auth system.")

    if "analytics" in detectedCategories:
        sectionNotes.append("- Include analytics and tracking disclosure with named providers from the analysis.")
    else:
        sectionNotes.append("- Do NOT include analytics or marketing cookies sections unless detected.")

    sectionRules = "\n".join(sectionNotes)

    return f"""You draft public-facing legal documents for a software product. Write for end users, not developers.

Project name: {projectName}

Internal analysis (for your reasoning only):
{summary}

Output format — use exactly these markdown headers:

## Privacy Policy
## Terms of Service
## Disclaimer

Style and content rules:
- Write clear English suitable for a product website
- Describe what the service actually does and what data flows occur
- Use product and vendor names (GitHub API, Google Gemini), never source file names or module paths
- Never mention "code analysis", "patterns detected", "scan", or how these documents were generated inside Privacy Policy or Terms
- Never write sections titled "Information We Do Not Collect" or explain missing features
- If a practice was not detected, omit that topic entirely instead of denying it repeatedly
- Include only sections that apply: auth, payments, analytics, email, cookies, geo — skip absent categories
- Describe real flows from the analysis: ZIP/GitHub input, third-party API calls, AI processing, HTTP hosting
- Do not claim users must connect a GitHub account unless OAuth/login was detected
- Do not claim zero IP collection if the product is a web service; standard server logs may record IP addresses and request metadata
- Do not claim data is never stored if code is sent to third-party AI; disclose that code excerpts/summaries are transmitted to Google Gemini
- Use placeholders where facts are unknown: [Company Name], [Contact Email], [Jurisdiction]
- Keep Disclaimer short (2-4 sentences): AI-generated draft, not legal advice, consult a lawyer

Section rules:
{sectionRules}

Length: Privacy Policy and Terms of Service each 600-1200 words. No filler, no repetition.
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
