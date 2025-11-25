from pathlib import Path

from pydantic import computed_field, HttpUrl, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the JobORM instance

    Everything is overridable by env var"""

    model_config = SettingsConfigDict(env_prefix="joborm_")

    SENTRY_DSN: HttpUrl | None = None

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: SecretStr
    GOOGLE_CLIENT_REDIRECT_URI: str = ""
    GOOGLE_CLIENT_HTTP: bool = False

    POOL_PRE_PING: bool = True
    POSTGRES_ECHO: bool = False

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str = "joborm"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def POSTGRES_URI(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD.get_secret_value(),
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )


# Root of repo directory
env_file = Path(__file__).resolve().parent.parent.parent.parent / ".env"
if not env_file.exists():
    # In directory of this file
    env_file = Path(__file__).resolve().parent / ".env"
settings = Settings(_env_file=env_file)
