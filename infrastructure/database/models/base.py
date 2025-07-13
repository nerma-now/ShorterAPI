from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.config import config


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy declarative models.

    Note:
        Uses naming conventions from application configuration.
    """

    __abstract__ = True

    metadata = MetaData(naming_convention=config.database.naming_convention)


__all__ = ["Base"]
