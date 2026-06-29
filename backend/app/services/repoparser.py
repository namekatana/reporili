import io
import re
import zipfile
from dataclasses import dataclass

from app.config import settings


@dataclass
class ParsedFile:
    path: str
    content: str


@dataclass
class ParsedRepo:
    projectName: str
    files: list[ParsedFile]


def parseZipArchive(data: bytes, projectName: str = "project") -> ParsedRepo:
    files: list[ParsedFile] = []
    totalBytes = 0

    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        rootPrefix = _detectRootPrefix(names)

        for name in names:
            if name.endswith("/"):
                continue
            relativePath = name[len(rootPrefix) :] if rootPrefix and name.startswith(rootPrefix) else name
            if _shouldSkip(relativePath):
                continue
            if not _isTextFile(relativePath):
                continue

            try:
                raw = archive.read(name)
            except (KeyError, RuntimeError):
                continue

            if len(raw) > settings.maxFileBytes:
                continue
            if totalBytes + len(raw) > settings.maxTotalBytes:
                break

            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    content = raw.decode("latin-1")
                except UnicodeDecodeError:
                    continue

            totalBytes += len(raw)
            files.append(ParsedFile(path=relativePath.replace("\\", "/"), content=content))

    if not projectName or projectName == "project":
        projectName = _inferProjectName(names)

    return ParsedRepo(projectName=projectName, files=files)


def _detectRootPrefix(names: list[str]) -> str:
    if not names:
        return ""
    first = names[0]
    if "/" in first:
        return first.split("/")[0] + "/"
    return ""


def _inferProjectName(names: list[str]) -> str:
    for name in names:
        if "/" in name:
            return name.split("/")[0]
    return "project"


def _shouldSkip(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    for part in parts:
        if part in _skipDirs():
            return True
    lower = path.lower()
    if lower.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".zip", ".tar", ".gz", ".pdf", ".exe", ".dll", ".so", ".dylib")):
        return True
    return False


def _skipDirs() -> set[str]:
    from app.constants.patterns import SKIP_DIRS

    return SKIP_DIRS


def _isTextFile(path: str) -> bool:
    from app.constants.patterns import TEXT_EXTENSIONS

    lower = path.lower()
    for ext in TEXT_EXTENSIONS:
        if lower.endswith(ext):
            return True
    basename = lower.rsplit("/", 1)[-1]
    return basename in ("dockerfile", "makefile", "gemfile", "rakefile", "procfile")


def parseGithubUrl(url: str) -> tuple[str, str, str | None]:
    cleaned = url.strip().rstrip("/")
    patterns = [
        r"^https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?(?:/tree/(?P<branch>[^/]+))?$",
        r"^github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?(?:/tree/(?P<branch>[^/]+))?$",
        r"^(?P<owner>[^/]+)/(?P<repo>[^/]+)$",
    ]
    for pattern in patterns:
        match = re.match(pattern, cleaned, re.IGNORECASE)
        if match:
            owner = match.group("owner")
            repo = match.group("repo").removesuffix(".git")
            branch = match.groupdict().get("branch")
            return owner, repo, branch
    raise ValueError(f"Invalid GitHub URL: {url}")
