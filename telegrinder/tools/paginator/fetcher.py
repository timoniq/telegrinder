import abc

from .data import Page


class Fetcher[T](abc.ABC):
    @abc.abstractmethod
    async def get_page(self, n: int) -> Page[T]: ...


__all__ = ("Fetcher",)
