from typing import Dict

from pydantic import Field, SecretStr, BaseModel

from sqlalchemy import URL


class DatabaseConfig(BaseModel):
    """
    Database connection settings and SQLAlchemy configuration.

    Attributes:
        driver: Database driver (e.g., 'postgresql+asyncpg')
        database: Database name
        user: Database username
        password: Database password (secured)
        host: Database server host
        host_alembic: Database host for migrations
        port: Database server port
        echo: Log SQL queries (debug)
        echo_pool: Log connection pool activity
        pool_size: Connection pool size
        max_overflow: Additional allowed connections
        naming_convention: SQLAlchemy constraint naming rules
    """


    driver: str = Field(default="postgresql+asyncpg")
    database: str = Field(default="database")
    user: str = Field(default="user")
    password: SecretStr = Field(default=SecretStr("password"))
    host: str = Field(default="postgres")
    host_alembic: str = Field(default="postgres")
    port: int = Field(default=5432)

    echo: bool = Field(default=False)
    echo_pool: bool = Field(default=False)
    pool_size: int = Field(default=5)
    max_overflow: int = Field(default=10)

    naming_convention: Dict[str, str] = Field(
        default={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        }
    )

    def build_url(
            self,
            host: str
    ) -> str:
        """
        Generate SQLAlchemy connection URL for given host.

        Args:
            host: Target database hostname

        Returns:
            Complete connection string (includes password)
        """

        url: str = URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password.get_secret_value(),
            host=host,
            port=self.port,
            database=self.database
        ).render_as_string(
            hide_password=False
        )

        return url


__all__ = ["DatabaseConfig"]
