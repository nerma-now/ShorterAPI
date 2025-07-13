from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from typing import Optional

from infrastructure.database.mixins import (
    IdPkMixin,
    CreatedAtMixin,
    LastUpdatedAtMixin,
)

from .base import Base


class Short(Base, CreatedAtMixin, LastUpdatedAtMixin, IdPkMixin):
    """
    Database model representing a shortened URL entry.

    Attributes:
        is_activated: Whether the short URL is active (default: True)
        code: Unique 6-character short code
        url: Original long URL
        expires_at: Optional expiration datetime
    """

    __tablename__ = "shorts"

    is_activated: Mapped[bool] = mapped_column(
        Boolean,
        server_default=expression.true(),
        nullable=False
    )
    code: Mapped[str] = mapped_column(
        String(6),
        unique=True,
        nullable=False
    )
    url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    expires_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


__all__ = ["Short"]
