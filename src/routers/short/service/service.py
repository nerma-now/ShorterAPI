import string
import random

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.crud import ShortRepository
from infrastructure.database.models import Short

from .base import BaseService


class Service(BaseService):
    async def generate_code(self, session: AsyncSession, max_length: int = 6) -> str:
        alphabet: str = string.ascii_letters + string.digits

        code: str = str()

        while True:
            code = code.join(random.choice(alphabet) for _ in range(max_length))

            exist: Optional[Short] = await ShortRepository().get(
                session=session,
                target=Short.code,
                value=code
            )

            if not exist:
                return code


__all__ = ["Service"]
