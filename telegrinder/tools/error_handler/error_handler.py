import dataclasses
import typing

from telegrinder.api import ABCAPI
from telegrinder.modules import logger
from telegrinder.result import Error, Ok, Result
from telegrinder.tools.magic import magic_bundle

from .abc import ABCErrorHandler, EventT, Handler

F = typing.TypeVar("F", bound="FuncCatcher")
ExceptionT = typing.TypeVar("ExceptionT", bound=BaseException, contravariant=True)
FuncCatcher = typing.Callable[
    typing.Concatenate[ExceptionT, ...], typing.Awaitable[typing.Any]
]


@dataclasses.dataclass(frozen=True)
class Catcher(typing.Generic[EventT]):
    func: FuncCatcher
    _: dataclasses.KW_ONLY
    exceptions: list[type[BaseException] | BaseException] = dataclasses.field(default_factory=lambda: [])
    logging: bool = dataclasses.field(default=False)
    raise_exception: bool = dataclasses.field(default=False)
    ignore_errors: bool = dataclasses.field(default=False)

    def match_exception(self, exception: BaseException) -> bool:
        for exc in self.exceptions:
            if isinstance(exc, type) and type(exception) == exc:
                return True
            if isinstance(exc, object) and type(exception) == type(exc):
                return True if not exc.args else exc.args == exception.args
        return False        

    async def __call__(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
        ctx: dict,
    ) -> Result[typing.Any, typing.Any]:
        try:
            result = Ok(await handler(event, **magic_bundle(handler, ctx)))
        except BaseException as exc:
            logger.debug(
                "Exception {!r} occurred while running handler {!r}. Matching  "
                "exceptions it with exception that can be caught by the catcher {!r}...",
                exc.__class__.__name__,
                handler.__name__,
                self.func.__name__,
            )
            if self.match_exception(exc):
                logger.debug(
                    "Catcher {!r} caught an exception in handler {!r}, "
                    "running catcher...".format(
                        self.func.__name__,
                        handler.__name__,
                    )
                )
                params: dict = {"event": event, "api": api} | ctx
                result = Ok(await self.func(exc, **magic_bundle(self.func, params)))
            else:
                logger.debug("Failed to match exception {!r}!", exc.__class__.__name__)
                result = Error(exc)
        
        logger.debug(
            "Catcher {!r} {} with result: {!r}",
            self.func.__name__,
            "completed" if result else "failed",
            result,
        )
        return result
    

class ErrorHandler(ABCErrorHandler[EventT]):
    def __init__(self, __catcher: Catcher[EventT] | None = None):
        self.catcher = __catcher
    
    def __repr__(self) -> str:
        return f"<ErrorHandler: {self.catcher!r}>"
    
    def catch(
        self,
        *exceptions: type[BaseException] | BaseException,
        logging: bool = False,
        raise_exception: bool = False,
        ignore_errors: bool = False,
    ):
        """Catch an exception while the handler is running.
        :param logging: Error logging in stderr.
        :param raise_exception: Raise an exception if the catcher hasn't started.
        :param ignore_errors: Ignore errors that may occur in the catcher.
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

    async def run(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
        ctx: dict,
    ) -> Result[typing.Any, typing.Any]:
        if not self.catcher:
            return Ok(await handler(event, **magic_bundle(handler, ctx)))
        
        try:
            result = await self.catcher(handler, event, api, ctx)
        except BaseException as e:
            error_msg = "Exception {} was occurred during the running catcher {!r}.".format(
                repr(e.__class__.__name__)
                if not e.args
                else f"{e.__class__.__name__!r}: {str(e)!r}",
                self.catcher.func.__name__,
            )
            if not self.catcher.ignore_errors:
                return Error(error_msg)
            if self.catcher.logging:
                logger.error(error_msg)
            result = Ok(None)

        if self.catcher.raise_exception and not result:
            return result
        if self.catcher.logging and not result:
            logger.error(
                "Catcher {!r} failed with error: {!r}",
                self.catcher.func.__name__,
                result.error,
            )
            return Ok(None)
        return Ok(result.unwrap_or(None))
