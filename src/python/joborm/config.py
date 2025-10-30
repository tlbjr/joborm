from pydantic import computed_field, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the JobORM instance

    Everything is overridable by env var"""

    model_config = SettingsConfigDict(env_prefix="joborm_")

    SENTRY_DSN: HttpUrl | None = None

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def POSTGRESQL_URI(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )


settings = Settings()
