import abc
import dataclasses
import typing

from fntypes import Error, Nothing, Ok, Option, Some
from fntypes.result import Result

from telegrinder.modules import logger
from telegrinder.tools.adapter.errors import AdapterError
from telegrinder.tools.aio import maybe_awaitable

type AdaptResult[To] = Result[To, AdapterError] | typing.Awaitable[Result[To, AdapterError]]


if typing.TYPE_CHECKING:
    from telegrinder.api.api import API
    from telegrinder.bot.dispatch.context import Context
    from telegrinder.model import Model


class ABCAdapter[From: "Model", To](abc.ABC):
    ADAPTED_VALUE_KEY: str | None = None

    @abc.abstractmethod
    def adapt(self, api: "API", update: From, context: "Context") -> AdaptResult[To]:
        pass


@dataclasses.dataclass(slots=True)
class Event[To]:
    obj: To


async def run_adapter[T, U: "Model"](
    adapter: "ABCAdapter[U, T]",
    api: "API",
    update: U,
    context: "Context",
) -> Option[T]:
    adapt_result = await maybe_awaitable(adapter.adapt(api, update, context))
    match adapt_result:
        case Ok(value):
            return Some(value)
        case Error(err):
            logger.debug("Adapter {!r} failed with error message: {!r}", adapter, str(err))
            return Nothing()


__all__ = ("ABCAdapter", "AdaptResult", "Event", "run_adapter")
