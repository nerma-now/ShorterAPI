from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    async def generate_code(self, *args, **kwargs) -> str:
        raise NotImplementedError()

__all__ = ["BaseService"]