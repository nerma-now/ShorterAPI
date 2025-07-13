from abc import ABC, abstractmethod

from typing import Any


class BaseRepository(ABC):
    """
    Abstract base class for database repository implementations.

    Provides core interface and common functionality for database connectors.

    Args:
        url: Database connection URL
    """

    def __init__(
            self,
            url: str,
            *args: Any,
            **kwargs: Any
    ) -> None:
        self._url: str = url

    @property
    def url(self) -> str:
        """
        Get the database connection URL

        Returns:
            Database connection URL
        """

        return self._url

    @abstractmethod
    async def dispose(self, *args, **kwargs) -> None:
        """
        Release all database resources and connections.

        Must be implemented by concrete subclasses.
        """

        raise NotImplementedError()

    @abstractmethod
    async def session(self, *args, **kwargs) -> Any:
        """
        Get a new database session context manager.

        Returns:
            A context manager yielding a database session

        Must be implemented by concrete subclasses.
        """

        raise NotImplementedError()


__all__ = ["BaseRepository"]
