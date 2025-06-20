import typing
from collections import deque

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import FuncHandler, Function
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.process import process_inner
from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager
from telegrinder.bot.dispatch.view.abc import ABCView
from telegrinder.bot.rules.abc import ABCRule, Always
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import Update

type Func[**P, T] = typing.Callable[P, typing.Coroutine[typing.Any, typing.Any, T]]


class BaseView(ABCView):
    def __init__(self, update_type: UpdateType | None = None) -> None:
        self.handlers: deque[ABCHandler] = deque()
        self.middlewares: deque[ABCMiddleware] = deque()
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

    @classmethod
    def to_handler[T: Function](cls, *rules: ABCRule, final: bool = True) -> typing.Callable[[T], FuncHandler[T]]:
        def wrapper(func: T, /) -> FuncHandler[T]:
            return FuncHandler(
                function=func,
                rules=list(rules),
                final=final,
            )

        return wrapper

    def __call__[T: Function](self, *rules: ABCRule, final: bool = True) -> typing.Callable[[T], T]:
        def wrapper(func: T, /) -> T:
            self.handlers.append(
                FuncHandler(
                    function=func,
                    rules=[self.auto_rules, *rules],
                    final=final,
                ),
            )
            return func

        return wrapper

    @typing.overload
    def register_middleware[T: ABCMiddleware](self, middleware_cls: type[T], /) -> type[T]: ...

    @typing.overload
    def register_middleware(self, middleware: ABCMiddleware, /) -> None: ...

    def register_middleware(
        self,
        middleware: type[ABCMiddleware] | ABCMiddleware,
    ) -> typing.Callable[..., typing.Any] | None:
        self.middlewares.append(middleware() if isinstance(middleware, type) else middleware)
        return middleware if isinstance(middleware, type) else None

    async def check(self, event: Update) -> bool:
        if self.update_type is not None and event.update_type != self.update_type:
            return False
        return bool(self.handlers or self.middlewares)

    async def process(self, event: Update, api: API, context: Context) -> bool:
        return await process_inner(
            api,
            event,
            context,
            self,
        )

    def load(self, external: typing.Self, /) -> None:
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)


__all__ = ("BaseView",)
