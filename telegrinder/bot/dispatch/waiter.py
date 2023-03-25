import asyncio
import dataclasses
import typing

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.abc import ABCRule


DefaultWaiterHandler = typing.Callable[[typing.Any], typing.Coroutine]
T = typing.TypeVar("T")
E = typing.TypeVar("E")


@dataclasses.dataclass
class Waiter:
    rules: typing.Iterable["ABCRule"]
    event: asyncio.Event
    default: DefaultWaiterHandler | str | None = None


async def wait(waiter: Waiter) -> tuple[typing.Any, dict]:
    await waiter.event.wait()
    event, ctx = getattr(waiter.event, "e")
    return event, ctx


class WithWaiter(typing.Generic[T, E]):
    short_waiters: dict[T, Waiter]
    auto_rules: list["ABCRule"]

    async def wait_for_answer(
        self,
        key: T,
        *rules: "ABCRule",
        default: DefaultWaiterHandler | str | None = None
    ) -> tuple[E, dict]:
        event = asyncio.Event()
        waiter = Waiter([*self.auto_rules, *rules], event, default)
        self.short_waiters[key] = waiter
        return await wait(waiter)
