from abc import ABC, abstractmethod


class ABCTemplating(ABC):
    @abstractmethod
    async def render(self, template_name: str) -> str:
        pass
