import dataclasses
import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import is_node
from telegrinder.tools.error_handler.abc import ABCErrorHandler, Handler
from telegrinder.tools.error_handler.error import CatcherError
from telegrinder.tools.magic import get_annotations, magic_bundle

type FuncCatcher[Exc: BaseException] = typing.Callable[
    typing.Concatenate[Exc, ...], typing.Awaitable[typing.Any]
]


async def run_handler(
    handler: Handler,
    event: typing.Any,
    ctx: dict[str, typing.Any],
) -> typing.Any:
    annotations = tuple(get_annotations(handler).values())
    start_idx = 0 if is_node(None if not annotations else annotations[0]) else 1
    context = magic_bundle(handler, ctx, start_idx=start_idx)
    return await (handler(event, **context) if start_idx == 1 else handler(**context))


@dataclasses.dataclass(frozen=True, repr=False, slots=True)
class Catcher[Event]:
    func: FuncCatcher[BaseException]
    exceptions: list[type[BaseException] | BaseException] = dataclasses.field(
        default_factory=lambda: [],
        kw_only=True,
    )
    logging: bool = dataclasses.field(default=False, kw_only=True)
    raise_exception: bool = dataclasses.field(default=False, kw_only=True)
    ignore_errors: bool = dataclasses.field(default=False, kw_only=True)

    def __repr__(self) -> str:
        return "<Catcher: function={!r}, logging={}, raise_exception={}, ignore_errors={}>".format(
            self.func.__name__,
            self.logging,
            self.raise_exception,
            self.ignore_errors,
        )

    async def __call__(
        self,
        handler: Handler,
        event: Event,
        api: API,
        ctx: Context,
    ) -> Result[typing.Any, BaseException]:
        try:
            return Ok(await run_handler(handler, event, ctx))
        except BaseException as exc:
            return await self.run(api, event, ctx, exc, handler.__name__)

    def match_exception(self, exception: BaseException) -> bool:
        for exc in self.exceptions:
            if isinstance(exc, type) and type(exception) is exc:
                return True
            if isinstance(exc, object) and type(exception) is type(exc):
                return True if not exc.args else exc.args == exception.args

        return False

    async def run(
        self,
        api: API,
        event: Event,
        ctx: Context,
        exception: BaseException,
        handler_name: str,
    ) -> Result[typing.Any, BaseException]:
        if self.match_exception(exception):
            logger.debug(
                "Error handler caught an exception {!r} in handler {!r}, running catcher {!r}...".format(
                    exception, handler_name, self.func.__name__
                )
            )
            return Ok(await run_handler(self.func, event, {"event": event, "api": api} | ctx))

        logger.debug("Failed to match exception {!r}.", exception.__class__.__name__)
        return Error(exception)


class ErrorHandler[Event](ABCErrorHandler[Event]):
    def __init__(self, catcher: Catcher[Event] | None = None, /) -> None:
        self.catcher = catcher

    def __repr__(self) -> str:
        return (
            "<{}: exceptions_handled=[{}], catcher={!r}>".format(
                self.__class__.__name__,
                ", ".join(e.__name__ if isinstance(e, type) else repr(e) for e in self.catcher.exceptions),
                self.catcher,
            )
            if self.catcher is not None
            else "<{}()>".format(self.__class__.__name__)
        )

    def __call__(
        self,
        *exceptions: type[BaseException] | BaseException,
        logging: bool = False,
        raise_exception: bool = False,
        ignore_errors: bool = False,
    ):
        """Register the catcher.

        :param logging: Logging the result of the catcher at the level `DEBUG`.
        :param raise_exception: Raise an exception if the catcher has not started.
        :param ignore_errors: Ignore errors that may occur.
        """

        def decorator[Func: FuncCatcher](catcher: Func, /) -> Func:
            if not self.catcher:
                self.catcher = Catcher(
                    catcher,
                    exceptions=list(exceptions),
                    logging=logging,
                    raise_exception=raise_exception,
                    ignore_errors=ignore_errors,
                )
            return catcher

        return decorator

    def _process_catcher_error(self, error: CatcherError) -> Result[None, BaseException]:
        assert self.catcher is not None

        if self.catcher.raise_exception:
            raise error.exc from None
        if self.catcher.logging:
            logger.error(error.message)
        if not self.catcher.ignore_errors:
            return Error(error.exc)

        return Ok(None)

    async def process(
        self,
        handler: Handler,
        event: Event,
        api: API,
        ctx: Context,
    ) -> Result[typing.Any, BaseException]:
        assert self.catcher is not None
        logger.debug("Processing the error handler for handler {!r}...", handler.__name__)

        try:
            return await self.catcher(handler, event, api, ctx)
        except BaseException as exc:
            return Error(
                CatcherError(
                    exc,
                    "Exception {} was occurred during the running catcher {!r}.".format(
                        repr(exc), self.catcher.func.__name__
                    ),
                )
            )

    async def run(
        self,
        handler: Handler,
        event: Event,
        api: API,
        ctx: Context,
    ) -> Result[typing.Any, BaseException]:
        if not self.catcher:
            return Ok(await run_handler(handler, event, ctx))

        match await self.process(handler, event, api, ctx):
            case Ok(value) as ok:
                if self.catcher.logging:
                    logger.debug(
                        "Catcher {!r} returned: {!r}",
                        self.catcher.func.__name__,
                        value,
                    )
                return ok
            case Error(exc) as err:
                if isinstance(exc, CatcherError):
                    return self._process_catcher_error(exc)
                if self.catcher.ignore_errors:
                    return Ok(None)
                return err


__all__ = ("Catcher", "ErrorHandler")
