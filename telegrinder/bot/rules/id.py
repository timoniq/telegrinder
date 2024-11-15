import typing

from telegrinder.types.objects import Update

from .abc import ABCRule


type Resolver[Identifier] = typing.Callable[[Update], tuple[typing.Any, Identifier] | None]


class IdRule[Identifier](ABCRule):
    def __init__(
        self, 
        tracked_identifiers: set[tuple[typing.Any, Identifier]] | None = None, 
        resolvers: list[Resolver[Identifier]] | None = None,
    ):
        self.tracked_identifiers = tracked_identifiers or set()
        self.resolvers: list[Resolver] = resolvers or []

    def __call__(
        self, 
        resolvers: list[Resolver[Identifier]],
    ):
        return self.__class__(
            self.tracked_identifiers.copy(), 
            self.resolvers + resolvers,
        )

    def get_identifier(self, event: Update) -> tuple[typing.Any, Identifier] | None:
        for resolver in self.resolvers:
            if identifier := resolver(event):
                return identifier
        return None
    
    async def check(self, event: Update) -> bool:
        ident = self.get_identifier(event)
        return ident in self.tracked_identifiers


__all__ = ("IdRule",)
