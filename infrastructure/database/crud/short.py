from infrastructure.database.models import Short

from .base import BaseRepository


class ShortRepository(BaseRepository[Short]):
    model = Short


__all__ = ["ShortRepository"]