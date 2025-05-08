import dataclasses
import typing

from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.tools.error_handler.abc import ABCErrorHandler
from telegrinder.tools.error_handler.error import CatcherError
from telegrinder.tools.magic.function import bundle

type FuncCatcher[Exc: BaseException] = typing.Callable[
    typing.Concatenate[Exc, ...],
    typing.Awaitable[typing.Any],
]


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
        exception: BaseException,
        event: Event,
        api: API,
        ctx: Context,
    ) -> Result[typing.Any, BaseException]:
        return await self.run(api, event, ctx, exception)

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
    ) -> Result[typing.Any, BaseException]:
        if self.match_exception(exception):
            logger.debug(
                "Error handler caught an exception {!r}, running catcher {!r}...".format(
                    exception,
                    self.func.__qualname__,
                )
            )
            return Ok(await bundle(self.func, {"event": event, "api": api, **ctx})(exception))

        logger.debug("Failed to match exception {!r}.", exception.__class__.__name__)
        return Error(exception)


class ErrorHandler[Event](ABCErrorHandler[Event]):
    def __init__(self, catcher: Catcher[Event] | None = None, /) -> None:
        self.catcher = catcher

    def __repr__(self) -> str:
        return (
            "<{}: exceptions=[{}], catcher={!r}>".format(
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

    async def suppress(
        self,
        exception: BaseException,
        event: Event,
        api: API,
        ctx: Context,
    ) -> Result[typing.Any, BaseException]:
        assert self.catcher is not None

        try:
            return await self.catcher(exception, event, api, ctx)
        except BaseException as exc:
            return Error(
                CatcherError(
                    exc,
                    "{!r} was occurred during the running catcher {!r}.".format(
                        exc,
                        self.catcher.func.__name__,
                    ),
                )
            )

    async def run(
        self,
        exception: BaseException,
        event: Event,
        api: API,
        ctx: Context,
    ) -> typing.Any:
        if not self.catcher:
            raise exception from None

        match await self.suppress(exception, event, api, ctx):
            case Ok(value):
                if self.catcher.logging:
                    logger.debug(
                        "Catcher {!r} returned: {!r}",
                        self.catcher.func.__name__,
                        value,
                    )
                return value
            case Error(exc):
                if isinstance(exc, CatcherError):
                    return self._process_catcher_error(exc).unwrap()
                if self.catcher.ignore_errors:
                    return None
                raise exc from None


__all__ = ("Catcher", "ErrorHandler")
