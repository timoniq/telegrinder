import typing

from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.action import ActionHandler, Behavior, Filter, When
from telegrinder.bot.dispatch.handler.func import FuncHandler

type Handler = ABCHandler | typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, typing.Any]]


def action(
    behavior: Behavior,
    *,
    when: When,
    filter: Filter | None = None,
) -> typing.Callable[[Handler], ActionHandler]:
    def decorator(handler: Handler, /) -> ActionHandler:
        handler = FuncHandler(handler, []) if not isinstance(handler, ABCHandler) else handler
        return ActionHandler(handler, behavior, when, filter)

    return decorator


__all__ = ("action",)
