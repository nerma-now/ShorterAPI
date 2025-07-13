from typing import Any, Optional, Sequence

from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from infrastructure.database.models import Base

from .abc import AbstractRepository, T


class BaseRepository(AbstractRepository[T]):
    model = Base

    async def get_all(
            self, session: AsyncSession, limit: Optional[int] = None
    ) -> Sequence[T]:
        """
        Retrieve all instances of the model with optional limit.

        Args:
            session: Async database session
            limit: Maximum number of records to return

        Returns:
            Sequence of model instances
        """

        result: Result = await session.execute(Select(self.model).limit(limit))

        return result.scalars().all()

    async def get(
            self, session: AsyncSession, target: InstrumentedAttribute[Any], value: Any
    ) -> Optional[T]:
        """
        Get a single instance by matching a specific attribute value.

        Args:
            session: Async database session
            target: Model attribute to filter by
            value: Value to match against the target attribute

        Returns:
            The matching model instance or None if not found
        """

        result: Result = await session.execute(
            Select(self.model).where(target == value)
        )

        return result.scalar_one_or_none()

    async def add(self, session: AsyncSession, target: T) -> T:
        """
        Add a new model instance to the database.

        Args:
            session: Async database session
            target: Model instance to add

        Returns:
            The added model instance
        """

        session.add(target)

        await session.commit()

        return target

    async def update(self, session: AsyncSession, instance: T, **update_data: Any) -> T:
        """
        Update an existing model instance with new data.

        Args:
            session: Async database session
            instance: Model instance to update
            **update_data: Field-value pairs to update

        Returns:
            The updated model instance
        """

        for key, value in update_data.items():
            setattr(instance, key, value)

        session.add(instance)

        await session.commit()
        await session.refresh(instance)

        return instance

    async def delete(self, session: AsyncSession, target: T) -> T:
        """
        Delete a model instance from the database.

        Args:
            session: Async database session
            target: Model instance to delete

        Returns:
            The deleted model instance (before deletion)
        """

        await session.delete(target)

        await session.commit()

        return target


__all__ = ["BaseRepository"]
