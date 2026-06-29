from app.constants.patterns import PATTERNS, STACK_MARKERS
from app.schemas.analysis import DetectedPattern, RepoAnalysis
from app.services.repoparser import ParsedFile, ParsedRepo


def buildAnalysis(parsed: ParsedRepo, source: str) -> RepoAnalysis:
    patterns = _detectPatterns(parsed.files)
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


def _detectPatterns(files: list[ParsedFile]) -> list[DetectedPattern]:
    results: list[DetectedPattern] = []

    for category, keywords in PATTERNS.items():
        foundKeywords: set[str] = set()
        foundFiles: set[str] = set()

        for file in files:
            lowerContent = file.content.lower()
            lowerPath = file.path.lower()
            for keyword in keywords:
                keyLower = keyword.lower()
                if keyLower in lowerContent or keyLower in lowerPath:
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


def _detectStack(files: list[ParsedFile]) -> list[str]:
    pathSet = {f.path.lower() for f in files}
    pathNames = {f.path.rsplit("/", 1)[-1].lower() for f in files}
    allNames = pathSet | pathNames
    combinedContent = "\n".join(f.content[:2000] for f in files[:50]).lower()

    detected: list[str] = []
    for stackName, markers in STACK_MARKERS.items():
        for marker in markers:
            markerLower = marker.lower()
            if markerLower in allNames or markerLower in combinedContent:
                detected.append(stackName)
                break

    return detected


def buildAnalysisSummary(analysis: RepoAnalysis) -> str:
    lines = [
        f"Project: {analysis.projectName}",
        f"Source: {analysis.source}",
        f"Files analyzed: {analysis.fileCount}",
        f"Stack: {', '.join(analysis.stack) if analysis.stack else 'unknown'}",
        "",
        "Detected data practices:",
    ]

    if not analysis.patterns:
        lines.append("- No specific patterns detected from code scan")
    else:
        for pattern in analysis.patterns:
            lines.append(f"- {pattern.category}: {', '.join(pattern.keywords)}")
            sampleFiles = ", ".join(pattern.files[:5])
            if sampleFiles:
                lines.append(f"  Files: {sampleFiles}")

    lines.extend(["", "Sample files:", *analysis.sampledFiles[:15]])
    return "\n".join(lines)
