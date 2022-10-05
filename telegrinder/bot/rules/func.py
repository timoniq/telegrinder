from .abc import ABCRule, EventScheme, T
from telegrinder.types import Update
import typing


class FuncRule(ABCRule, typing.Generic[T]):
    def __init__(
        self,
        func: typing.Callable[[T, dict], bool],
        event_scheme: typing.Optional[
            typing.Union[EventScheme, typing.Tuple[str, typing.Type[T]]]
        ] = None,
    ):
        self.func = func
        if isinstance(event_scheme, tuple):
            event_scheme = EventScheme(*event_scheme)
        self.event_scheme = event_scheme

    async def check(self, event: Update, ctx: dict) -> bool:
        if self.event_scheme:
            if self.event_scheme.name not in event:
                return False
            event = self.event_scheme.dataclass(
                **getattr(event, self.event_scheme.name).to_dict()
            )
        return self.func(event, ctx)
