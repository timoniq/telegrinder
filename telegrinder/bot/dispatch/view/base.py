import typing

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import Func, FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.bot.dispatch.view.abc import ABCView
from telegrinder.bot.rules.abc import ABCRule, Always
from telegrinder.node.composer import CONTEXT_STORE_NODES_KEY, NodeScope
from telegrinder.tools.error_handler.error_handler import ABCErrorHandler, ErrorHandler
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update


class BaseView(ABCView):
    def __init__(self, update_type: UpdateType | None = None) -> None:
        self.handlers: list[ABCHandler] = []
        self.middlewares: list[ABCMiddleware] = []
        self.return_manager: ABCReturnManager | None = None
        self.update_type = update_type
        self._auto_rules: ABCRule = Always()

    def __repr__(self) -> str:
        return "<{}>".format(type(self).__name__)

    @property
    def auto_rules(self) -> ABCRule:
        return self._auto_rules

    @auto_rules.setter
    def auto_rules(self, value: ABCRule | list[ABCRule], /) -> None:
        """Example usage:

        ```python
        view.auto_rules = Rule1() & Rule2() | Rule3() & Rule4()
        view.auto_rules # <OrRule>

        view.auto_rules = [Rule1(), Rule2()]
        view.auto_rules # <AndRule>
        ```
        """
        if isinstance(value, list):
            for rule in value:
                self._auto_rules = self._auto_rules & rule
        else:
            self._auto_rules = value

    @typing.overload
    @classmethod
    def to_handler[**P, R](
        cls,
        *rules: ABCRule,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[Func[P, R], ErrorHandler],
    ]: ...

    @typing.overload
    @classmethod
    def to_handler[**P, ErrorHandlerT: ABCErrorHandler, R](
        cls,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        final: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Func[P, R], ErrorHandlerT]]: ...

    @typing.overload
    @classmethod
    def to_handler[**P, Dataclass, ErrorHandlerT: ABCErrorHandler, R](
        cls,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        final: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Func[P, R], ErrorHandlerT]]: ...

    @classmethod
    def to_handler(
        cls,
        *rules: ABCRule,
        error_handler: ABCErrorHandler | None = None,
        final: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func):
            return FuncHandler(
                func,
                list(rules),
                final=final,
                error_handler=error_handler or ErrorHandler(),
            )

        return wrapper

    @typing.overload
    def __call__[**P, R](
        self,
        *rules: ABCRule,
        final: bool = True,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[Func[P, R], ErrorHandler],
    ]: ...

    @typing.overload
    def __call__[**P, ErrorHandlerT: ABCErrorHandler, R](
        self,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        final: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Func[P, R], ErrorHandlerT]]: ...

    def __call__[**P, R](
        self,
        *rules: ABCRule,
        error_handler: ABCErrorHandler | None = None,
        final: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func: typing.Callable[..., typing.Any]):
            func_handler = FuncHandler(
                handler=func,
                rules=[self.auto_rules, *rules],
                final=final,
                error_handler=error_handler or ErrorHandler(),
            )
            self.handlers.append(func_handler)
            return func_handler

        return wrapper

    def register_middleware[Middleware: ABCMiddleware](self, *args: typing.Any, **kwargs: typing.Any):
        def wrapper(cls: type[Middleware]) -> type[Middleware]:
            self.middlewares.append(cls(*args, **kwargs))
            return cls

        return wrapper

    async def check(self, event: Update) -> bool:
        if self.update_type is not None and event.update_type != self.update_type:
            return False
        return bool(self.handlers or self.middlewares)

    async def process(self, event: Update, api: API, context: Context) -> bool:
        try:
            return await process_inner(
                api,
                event,
                context,
                self,
            )
        finally:
            for session in context.get(CONTEXT_STORE_NODES_KEY, {}).values():
                await session.close(scopes=(NodeScope.PER_EVENT,))

    def load(self, external: typing.Self, /) -> None:
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)


__all__ = ("BaseView",)
