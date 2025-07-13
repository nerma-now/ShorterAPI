from abc import ABC, abstractmethod

from typing import Type, TypeVar, Generic

from sqlalchemy.orm import DeclarativeBase

T: TypeVar = TypeVar("T", bound=DeclarativeBase)


class AbstractRepository(ABC, Generic[T]):
    """
    Abstract base class for repository pattern implementation.

    Provides standard CRUD interface for SQLAlchemy models.
    Subclasses must specify the model class attribute.

    Type Parameters:
        T: SQLAlchemy model type this repository handles
    """

    model: Type[T]

    def __init_subclass__(cls, **kwargs):
        """
        Validate that subclasses define a model attribute
        """

        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "model") or cls.model is None:
            raise TypeError(f'{cls.__name__} must define "model" class attribute')

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        """
        Retrieve all instances of the model
        """

        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        """
        Get a single model instance by criteria
        """

        raise NotImplementedError()

    @abstractmethod
    async def add(self, *args, **kwargs):
        """
        Add a new model instance to storage
        """

        raise NotImplementedError()

    @abstractmethod
    async def update(self, *args, **kwargs):
        """
        Update an existing model instance
        """

        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *args, **kwargs):
        """
        Delete a model instance from storage
        """

        raise NotImplementedError()


__all__ = ["AbstractRepository", "T"]
