from pydantic import Field
from pydantic_settings import BaseSettings

from .constants import ENV_FILE_PATH

from .components.database import DatabaseConfig
from .components.cors import CORSConfig


class ApplicationConfig(BaseSettings):
    """
    Main application configuration with environment variables support.

    Attributes:
        debug: Run in debug mode (default: False)
        title: Application title (default: "Shorter API")
        description: API functionality description
                    (default: "An API for creating and interacting with short URLs")
        redoc_url: Path for ReDoc documentation (default: "/redoc")
        docs_url: Path for Swagger docs (default: "/")
        database: Database connection configuration
        cors: CORS configuration

    All fields can be overridden via environment variables using:
    - CONFIG__ prefix
    - __ as nested delimiter (e.g. CONFIG__DATABASE__HOST)
    - .env file or OS environment variables
    """

    debug: bool = Field(default=False)
    title: str = Field(default="Shorter API")
    description: str = Field(default="An API for creating and interacting with short URLs")
    redoc_url: str = Field(default="/redoc")
    docs_url: str = Field(default="/")

    database: DatabaseConfig = DatabaseConfig()
    cors: CORSConfig = CORSConfig()

    class Config:
        """
        Environment variables configuration
        """

        env_file = ENV_FILE_PATH
        env_file_encoding = "utf-8"
        case_sensitive = False
        env_nested_delimiter = "__"
        env_prefix = "CONFIG__"


config: ApplicationConfig = ApplicationConfig()

__all__ = ["config"]
