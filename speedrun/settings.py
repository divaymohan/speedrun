import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_host: str = "speedrun-db"
    db_port: int = 5432
    db_user: str = "speedrun"
    db_pass: str = "speedrun"
    db_base: str = "speedrun"
    db_echo: bool = False

    rbmq_host: str = "speedrun-rabbitmq"
    rbmq_port: str = "5672"
    rbmq_user_name: str = "speedrun"
    rbmq_password: str = "speedrun"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SPEEDRUN_",
        env_file_encoding="utf-8",
    )


settings = Settings()
