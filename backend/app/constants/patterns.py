PATTERNS: dict[str, list[str]] = {
    "auth": ["jwt", "oauth", "bcrypt", "passport", "fastapi-users", "nextauth"],
    "payments": ["stripe", "paypal", "paddle", "lemon-squeezy", "checkout.session"],
    "analytics": ["google-analytics", "mixpanel", "amplitude", "gtag(", "segment.com"],
    "email": ["smtp", "sendgrid", "mailgun", "nodemailer", "fastapi-mail"],
    "storage": ["boto3", "s3://", "@aws-sdk/client-s3", "firebase", "supabase", "cloudinary"],
    "cookies": ["document.cookie", "set-cookie", "localstorage", "sessionstorage"],
    "geo": ["geolocation", "geoip", "maxmind", "navigator.geolocation"],
}

SKIP_DIRS: set[str] = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    "target",
    "vendor",
    ".idea",
    ".vscode",
}

SKIP_SCAN_SUFFIXES: tuple[str, ...] = (
    "patterns.py",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "geminigenerator.py",
)

SKIP_SCAN_PARTS: tuple[str, ...] = (
    "/constants/",
    "\\constants\\",
    "/scripts/",
    "\\scripts\\",
)

TEXT_EXTENSIONS: set[str] = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".cs",
    ".swift",
    ".vue",
    ".svelte",
    ".astro",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".xml",
    ".env",
    ".sql",
    ".graphql",
    ".prisma",
}

STACK_MARKERS: dict[str, list[str]] = {
    "Python": ["requirements.txt", "pyproject.toml", "Pipfile"],
    "Node.js": ["package.json"],
    "Go": ["go.mod"],
    "Rust": ["Cargo.toml"],
    "Ruby": ["Gemfile"],
    "PHP": ["composer.json"],
    "Java": ["pom.xml", "build.gradle"],
    "Docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
    "Astro": ["astro.config.mjs", "astro.config.ts"],
    "Next.js": ["next.config.js", "next.config.mjs", "next.config.ts"],
    "Svelte": ["svelte.config.js", "svelte.config.ts"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "Rails": ["config/application.rb"],
}
