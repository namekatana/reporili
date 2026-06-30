import re

from app.constants.patterns import PATTERNS, SKIP_SCAN_PARTS, SKIP_SCAN_SUFFIXES, STACK_MARKERS
from app.schemas.analysis import DetectedPattern, RepoAnalysis
from app.services.repoparser import ParsedFile, ParsedRepo


def buildAnalysis(parsed: ParsedRepo, source: str) -> RepoAnalysis:
    scannable = _scannableFiles(parsed.files)
    patterns = _detectPatterns(scannable)
    stack = _detectStack(parsed.files)
    sampledFiles = [f.path for f in parsed.files[:30]]

    return RepoAnalysis(
        projectName=parsed.projectName,
        source=source,
        stack=stack,
        patterns=patterns,
        fileCount=len(parsed.files),
        sampledFiles=sampledFiles,
    )


def _scannableFiles(files: list[ParsedFile]) -> list[ParsedFile]:
    result: list[ParsedFile] = []
    for file in files:
        lowerPath = file.path.lower()
        if lowerPath.endswith(SKIP_SCAN_SUFFIXES):
            continue
        if lowerPath.endswith(".md"):
            continue
        if any(part in lowerPath for part in SKIP_SCAN_PARTS):
            continue
        result.append(file)
    return result


def _detectPatterns(files: list[ParsedFile]) -> list[DetectedPattern]:
    results: list[DetectedPattern] = []

    for category, keywords in PATTERNS.items():
        foundKeywords: set[str] = set()
        foundFiles: set[str] = set()

        for file in files:
            lowerPath = file.path.lower()
            lowerContent = file.content.lower()
            for keyword in keywords:
                keyLower = keyword.lower()
                if _keywordMatches(keyLower, lowerContent, lowerPath, file.path):
                    foundKeywords.add(keyword)
                    foundFiles.add(file.path)

        if foundKeywords:
            results.append(
                DetectedPattern(
                    category=category,
                    keywords=sorted(foundKeywords),
                    files=sorted(foundFiles)[:15],
                )
            )

    return results


def _keywordMatches(keyword: str, content: str, path: str, originalPath: str) -> bool:
    if path.endswith("package.json"):
        return _matchesPackageJson(keyword, content)

    if keyword in path:
        return True

    if "(" in keyword or "://" in keyword or "@" in keyword:
        return keyword in content

    pattern = re.compile(rf"(?<![a-z0-9_./@-]){re.escape(keyword)}(?![a-z0-9_./@-])")
    if not pattern.search(content):
        return False

    if _isUiCopyFile(originalPath):
        return _hasCodeContext(keyword, content)

    return True


def _isUiCopyFile(path: str) -> bool:
    lower = path.lower()
    return lower.endswith(".svelte") or lower.endswith(".astro") or lower.endswith(".tsx") or lower.endswith(".jsx")


def _hasCodeContext(keyword: str, content: str) -> bool:
    contextPatterns = [
        rf"\bimport\b[^\n]*{re.escape(keyword)}",
        rf"\bfrom\b[^\n]*{re.escape(keyword)}",
        rf"require\s*\([^\n]*{re.escape(keyword)}",
        rf"{re.escape(keyword)}\s*[:=]",
        rf"process\.env\.[A-Z0-9_]*{re.escape(keyword.upper())}",
        rf"os\.getenv\s*\([^\n]*{re.escape(keyword)}",
    ]
    lower = content.lower()
    return any(re.search(pattern, lower) for pattern in contextPatterns)


def _matchesPackageJson(keyword: str, content: str) -> bool:
    lower = content.lower()
    depsMarker = '"dependencies"'
    if depsMarker not in lower and '"devdependencies"' not in lower:
        return False
    pattern = re.compile(rf'"{re.escape(keyword)}"\s*:')
    return pattern.search(lower) is not None


def _detectStack(files: list[ParsedFile]) -> list[str]:
    basenames = {f.path.rsplit("/", 1)[-1].lower() for f in files}
    extensionCounts: dict[str, int] = {}
    for file in files:
        lowerPath = file.path.lower()
        dotIndex = lowerPath.rfind(".")
        if dotIndex == -1:
            continue
        ext = lowerPath[dotIndex:]
        extensionCounts[ext] = extensionCounts.get(ext, 0) + 1

    detected: list[str] = []

    for stackName, markers in STACK_MARKERS.items():
        if _stackMarkerHit(markers, basenames, files):
            detected.append(stackName)

    languageStack = _detectFromExtensions(extensionCounts)
    for item in languageStack:
        if item not in detected:
            detected.append(item)

    return detected


def _stackMarkerHit(markers: list[str], basenames: set[str], files: list[ParsedFile]) -> bool:
    fileMarkers = {
        "requirements.txt",
        "pyproject.toml",
        "pipfile",
        "package.json",
        "go.mod",
        "cargo.toml",
        "gemfile",
        "composer.json",
        "pom.xml",
        "build.gradle",
        "dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        "astro.config.mjs",
        "astro.config.ts",
        "next.config.js",
        "next.config.mjs",
        "next.config.ts",
        "svelte.config.js",
        "svelte.config.ts",
        "config/application.rb",
    }

    for marker in markers:
        markerLower = marker.lower()
        if markerLower in fileMarkers:
            if markerLower == "dockerfile":
                if "dockerfile" in basenames:
                    return True
                continue
            if markerLower in basenames:
                return True
            if any(f.path.lower().endswith(f"/{markerLower}") for f in files):
                return True
            continue

        if markerLower in {"fastapi", "django"}:
            pattern = re.compile(rf"\b{re.escape(markerLower)}\b")
            for file in files:
                if not file.path.lower().endswith((".py", ".txt", ".toml")):
                    continue
                if file.path.lower().endswith(SKIP_SCAN_SUFFIXES):
                    continue
                if pattern.search(file.content.lower()):
                    return True

    return False


def _detectFromExtensions(extensionCounts: dict[str, int]) -> list[str]:
    mapping = {
        ".py": "Python",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".svelte": "Svelte",
        ".astro": "Astro",
        ".go": "Go",
        ".rs": "Rust",
        ".rb": "Ruby",
        ".php": "PHP",
        ".java": "Java",
        ".css": "CSS",
    }

    ranked = sorted(
        ((ext, count) for ext, count in extensionCounts.items() if ext in mapping),
        key=lambda item: item[1],
        reverse=True,
    )

    result: list[str] = []
    for ext, count in ranked:
        if count == 0:
            continue
        label = mapping[ext]
        if label not in result:
            result.append(label)
    return result


def buildAnalysisSummary(analysis: RepoAnalysis) -> str:
    lines = [
        f"Project: {analysis.projectName}",
        f"Source: {analysis.source}",
        f"Files analyzed: {analysis.fileCount}",
        f"Stack: {', '.join(analysis.stack) if analysis.stack else 'unknown'}",
        "",
        "Detected data practices (from code scan):",
    ]

    if not analysis.patterns:
        lines.append("- None of the tracked categories matched (auth, payments, analytics, email, storage, cookies, geo)")
    else:
        for pattern in analysis.patterns:
            lines.append(f"- {pattern.category}: {', '.join(pattern.keywords)}")
            sampleFiles = ", ".join(pattern.files[:5])
            if sampleFiles:
                lines.append(f"  Files: {sampleFiles}")

    lines.extend(["", "Operational context for the legal drafter:"])
    lines.extend(_buildOperationalContext(analysis))

    lines.extend(["", "Sample file paths (internal only, do not quote in legal docs):", *analysis.sampledFiles[:15]])
    return "\n".join(lines)


def _buildOperationalContext(analysis: RepoAnalysis) -> list[str]:
    stack = set(analysis.stack)
    patternCategories = {p.category for p in analysis.patterns}
    context: list[str] = []

    if "FastAPI" in stack or "Python" in stack:
        context.append("- Web API backend processes user requests")
    if any(item in stack for item in ("Astro", "Svelte", "Node.js", "TypeScript")):
        context.append("- Browser-based web frontend")

    sampled = " ".join(analysis.sampledFiles).lower()
    if "github" in sampled:
        context.append("- Accepts public GitHub repository URLs and downloads repo archives via GitHub API")
        context.append("- Users do not sign in to GitHub through this app; only public repo URLs or ZIP uploads")
    if "gemini" in sampled or "generativeai" in sampled:
        context.append("- Sends derived code analysis text to Google Gemini API to generate documents")
    if "docker" in stack or "dockerfile" in sampled:
        context.append("- Deployed as containerized web service (standard HTTP server logs may apply)")

    if "auth" not in patternCategories:
        context.append("- No user accounts, login, or authentication flow detected")
    if "payments" not in patternCategories:
        context.append("- No payment processing detected")
    if "storage" not in patternCategories:
        context.append("- No cloud storage SDK or user database detected in scan")
    if "analytics" not in patternCategories:
        context.append("- No analytics or tracking SDK detected")

    context.append("- Typical user input: ZIP upload or GitHub URL of source code")
    context.append("- Processing appears in-memory for analysis and generation, not described as long-term user data storage")

    return context
