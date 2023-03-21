import asyncio
import dataclasses
import typing
from telegrinder.bot.rules import ABCRule


DefaultWaiterHandler = typing.Callable[[typing.Any], typing.Coroutine]
T = typing.TypeVar("T")
E = typing.TypeVar("E")


@dataclasses.dataclass
class Waiter:
    rules: typing.Iterable[ABCRule]
    event: asyncio.Event
    default: typing.Optional[typing.Union[DefaultWaiterHandler, str]] = None


async def wait(waiter: Waiter) -> typing.Tuple[typing.Any, dict]:
    await waiter.event.wait()
    event, ctx = getattr(waiter.event, "e")
    return event, ctx


class WithWaiter(typing.Generic[T, E]):
    short_waiters: typing.Dict[T, Waiter]
    auto_rules: typing.List[ABCRule]

    async def wait_for_answer(
        self,
        key: T,
        *rules: ABCRule,
        default: typing.Optional[typing.Union[DefaultWaiterHandler, str]] = None
    ) -> typing.Tuple[E, dict]:
        event = asyncio.Event()
        waiter = Waiter([*self.auto_rules, *rules], event, default)
        self.short_waiters[key] = waiter
        return await wait(waiter)
