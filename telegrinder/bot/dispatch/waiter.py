import asyncio
import dataclasses
import typing
from telegrinder.bot.rules import ABCRule


DefaultWaiterHandler = typing.Callable[[typing.Any], typing.Coroutine]


@dataclasses.dataclass
class Waiter:
    rules: typing.Iterable[ABCRule]
    event: asyncio.Event
    default: typing.Optional[typing.Union[DefaultWaiterHandler, str]] = None


async def wait(waiter: Waiter) -> typing.Tuple[typing.Any, dict]:
    await waiter.event.wait()
    event, ctx = getattr(waiter.event, "e")
    return event, ctx
