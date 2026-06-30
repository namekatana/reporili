from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    geminiApiKey: str = Field(default="", validation_alias="GEMINI_API_KEY")
    geminiModel: str = Field(default="gemini-2.5-flash", validation_alias="GEMINI_MODEL")
    githubToken: str | None = Field(default=None, validation_alias="GITHUB_TOKEN")
    maxFileBytes: int = Field(default=500_000, validation_alias="MAX_FILE_BYTES")
    maxTotalBytes: int = Field(default=5_000_000, validation_alias="MAX_TOTAL_BYTES")
    maxUploadBytes: int = Field(default=52_428_800, validation_alias="MAX_UPLOAD_BYTES")
    proxySecret: str = Field(default="", validation_alias="PROXY_SECRET")
    allowedOrigins: list[str] = Field(
        default=[
            "https://reporili.tech",
            "https://www.reporili.tech",
            "http://localhost:4321",
            "http://127.0.0.1:4321",
        ],
        validation_alias="ALLOWED_ORIGINS",
    )

    @field_validator("allowedOrigins", mode="before")
    @classmethod
    def parseAllowedOrigins(cls, value: object) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value  # type: ignore[return-value]


settings = Settings()
