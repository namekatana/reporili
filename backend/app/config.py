from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    geminiApiKey: str = Field(default="", validation_alias="GEMINI_API_KEY")
    geminiModel: str = Field(default="gemini-2.5-flash", validation_alias="GEMINI_MODEL")
    githubToken: str | None = Field(default=None, validation_alias="GITHUB_TOKEN")
    maxFileBytes: int = Field(default=500_000, validation_alias="MAX_FILE_BYTES")
    maxTotalBytes: int = Field(default=5_000_000, validation_alias="MAX_TOTAL_BYTES")


settings = Settings()
