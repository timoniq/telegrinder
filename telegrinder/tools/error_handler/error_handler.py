import dataclasses
import typing
from functools import cached_property

from fntypes.result import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.modules import logger
from telegrinder.node.base import IsNode, get_nodes
from telegrinder.node.composer import compose_nodes
from telegrinder.tools.error_handler.abc import ABCErrorHandler
from telegrinder.tools.error_handler.error import CatcherError
from telegrinder.tools.fullname import fullname
from telegrinder.tools.magic.function import bundle
from telegrinder.types.objects import Update

type FunctionCatcher = typing.Callable[..., typing.Awaitable[typing.Any]]


@dataclasses.dataclass(frozen=True, repr=False)
class Catcher:
    func: FunctionCatcher
    exceptions: list[type[BaseException] | BaseException] = dataclasses.field(
        default_factory=lambda: [],
        kw_only=True,
    )
    logging: bool = dataclasses.field(default=False, kw_only=True)
    raise_exception: bool = dataclasses.field(default=False, kw_only=True)
    ignore_errors: bool = dataclasses.field(default=False, kw_only=True)

    def __repr__(self) -> str:
        return "<{}: function={!r}, logging={}, raise_exception={}, ignore_errors={}>".format(
            type(self).__name__,
            fullname(self.func),
            self.logging,
            self.raise_exception,
            self.ignore_errors,
        )

    async def __call__(
        self,
        exception: BaseException,
        event: Update,
        api: API,
        ctx: Context,
    ) -> Result[typing.Any, BaseException]:
        return await self.run(api, event, ctx, exception)

    @cached_property
    def required_nodes(self) -> dict[str, IsNode]:
        return get_nodes(self.func)

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
        event: Update,
        context: Context,
        exception: BaseException,
    ) -> Result[typing.Any, BaseException]:
        if self.match_exception(exception):
            logger.debug(
                "Error handler caught an exception {!r}, running catcher {!r}...".format(
                    exception,
                    fullname(self.func),
                )
            )

            node_col = None
            data = {Update: event, API: api}

            if self.required_nodes:
                match await compose_nodes(self.required_nodes, context, data=data):
                    case Ok(value):
                        node_col = value
                    case Error(compose_error):
                        logger.debug(
                            "Cannot compose nodes for catcher `{}`, error: {!r}",
                            fullname(self),
                            compose_error.message,
                        )
                        return Error(exception)

            try:
                data_bundle = bundle(self.func, {**data, Context: context.copy()})
                return Ok(
                    await bundle(
                        self.func,
                        {"exception": exception} | context | ({} if node_col is None else node_col.values),
                        start_idx=0,
                    )(*data_bundle.args, **data_bundle.kwargs)
                )
            finally:
                if node_col is not None:
                    await node_col.close_all()

        logger.debug("Failed to match exception {!r}.", type(exception).__name__)
        return Error(exception)


class ErrorHandler(ABCErrorHandler):
    def __init__(self, catcher: Catcher | None = None, /) -> None:
        self.catcher = catcher

    def __repr__(self) -> str:
        return (
            "<{}: exceptions=[{}], catcher={!r}>".format(
                type(self).__name__,
                ", ".join(fullname(e) for e in self.catcher.exceptions),
                self.catcher,
            )
            if self.catcher is not None
            else "<{}()>".format(type(self).__name__)
        )

    def __call__[Func: FunctionCatcher](
        self,
        *exceptions: type[BaseException] | BaseException,
        logging: bool = False,
        raise_exception: bool = False,
        ignore_errors: bool = False,
    ) -> typing.Callable[[Func], Func]:
        """Register the catcher.

        :param logging: Logging the result of the catcher at the level `DEBUG`.
        :param raise_exception: Raise an exception if the catcher has not started.
        :param ignore_errors: Ignore errors that may occur.
        """

        def decorator(catcher: Func, /) -> Func:
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

    def _process_catcher_error(self, error: CatcherError, /) -> Result[None, BaseException]:
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
        event: Update,
        api: API,
        context: Context,
    ) -> Result[typing.Any, BaseException]:
        assert self.catcher is not None

        try:
            return await self.catcher(exception, event, api, context)
        except BaseException as exc:
            return Error(
                CatcherError(
                    exc,
                    "{!r} was occurred during the running catcher {!r}.".format(
                        exc,
                        fullname(self.catcher.func),
                    ),
                )
            )

    async def run(
        self,
        exception: BaseException,
        event: Update,
        api: API,
        context: Context,
    ) -> typing.Any:
        if not self.catcher:
            raise exception from None

        match await self.suppress(exception, event, api, context):
            case Ok(value):
                if self.catcher.logging:
                    logger.debug(
                        "Catcher {!r} returned: {!r}",
                        fullname(self.catcher.func),
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
