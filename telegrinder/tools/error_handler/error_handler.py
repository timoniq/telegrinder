import dataclasses
import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api import ABCAPI
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.tools.magic import magic_bundle

from .abc import ABCErrorHandler, EventT, Handler
from .error import CatcherError

F = typing.TypeVar("F", bound="FuncCatcher")
ExceptionT = typing.TypeVar("ExceptionT", bound=BaseException, contravariant=True)
FuncCatcher = typing.Callable[typing.Concatenate[ExceptionT, ...], typing.Awaitable[typing.Any]]


@dataclasses.dataclass(frozen=True, repr=False, slots=True)
class Catcher(typing.Generic[EventT]):
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
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
        ctx: Context,
    ) -> Result[typing.Any, BaseException]:
        try:
            return Ok(await handler(event, **magic_bundle(handler, ctx)))  # type: ignore
        except BaseException as exc:
            return await self.process_exception(api, event, ctx, exc, handler.__name__)

    async def process_exception(
        self,
        api: ABCAPI,
        event: EventT,
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
            return Ok(
                await self.func(
                    exception,
                    **magic_bundle(self.func, {"event": event, "api": api} | ctx),  # type: ignore
                )
            )
        logger.debug("Failed to match exception {!r}.", exception.__class__.__name__)
        return Error(exception)

    def match_exception(self, exception: BaseException) -> bool:
        for exc in self.exceptions:
            if isinstance(exc, type) and type(exception) is exc:
                return True
            if isinstance(exc, object) and type(exception) is type(exc):
                return True if not exc.args else exc.args == exception.args
        return False


class ErrorHandler(ABCErrorHandler[EventT]):
    def __init__(self, catcher: Catcher[EventT] | None = None, /) -> None:
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

        :param logging: Logging the result of the catcher at the level 'DEBUG'.
        :param raise_exception: Raise an exception if the catcher hasn't started.
        :param ignore_errors: Ignore errors that may occur.
        """

        def decorator(func: F) -> F:
            if not self.catcher:
                self.catcher = Catcher(
                    func,
                    exceptions=list(exceptions),
                    logging=logging,
                    raise_exception=raise_exception,
                    ignore_errors=ignore_errors,
                )
            return func

        return decorator

    async def process(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
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

    def process_catcher_error(self, error: CatcherError) -> Result[None, BaseException]:
        assert self.catcher is not None

        if self.catcher.raise_exception:
            raise error.exc from None
        if self.catcher.logging:
            logger.error(error.message)
        if not self.catcher.ignore_errors:
            return Error(error.exc)

        return Ok(None)

    async def run(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
        ctx: Context,
    ) -> Result[typing.Any, BaseException]:
        if not self.catcher:
            return Ok(await handler(event, **magic_bundle(handler, ctx)))  # type: ignore

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
                    return self.process_catcher_error(exc)
                if self.catcher.ignore_errors:
                    return Ok(None)
                return err
