import typing

import pytest

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.abc import ABCHandler
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.return_manager.abc import register_manager
from telegrinder.bot.dispatch.return_manager.message import MessageReturnManager
from telegrinder.bot.dispatch.view.base import BaseStateView
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.text import Text


class CustomMessageReturnManager(MessageReturnManager):
    @register_manager(int)
    @staticmethod
    async def int_manager(value: int, event: MessageCute, ctx: Context) -> None:
        assert isinstance(value, int)


class CustomMessageView(BaseStateView[MessageCute]):
    def __init__(self) -> None:
        self.middlewares: list[ABCMiddleware[MessageCute]] = []
        self.auto_rules: list[ABCRule[MessageCute]] = []
        self.handlers: list[ABCHandler[MessageCute]] = []
        self.return_manager: CustomMessageReturnManager = CustomMessageReturnManager()

    async def get_state_key(self, event: MessageCute) -> int | None:
        return event.message_id


class PreMiddleware(ABCMiddleware[MessageCute]):
    async def pre(self, event: MessageCute, ctx: Context) -> bool:
        return True


class PostMiddleware(ABCMiddleware[MessageCute]):
    async def post(self, event: MessageCute, ctx: Context, responses: list[typing.Any]) -> None:
        assert responses == [b"123data"]


@pytest.mark.asyncio()
async def test_register_middleware():
    view = CustomMessageView()

    @view.register_middleware(one=1, two=2)
    class SomeMiddleware(ABCMiddleware[MessageCute]):
        def __init__(self, one: int, two: int) -> None:
            self.one = one
            self.two = two

        async def pre(self, event: MessageCute) -> None:
            pass

    assert len(view.middlewares) == 1
    assert isinstance(view.middlewares[0], SomeMiddleware)
    assert view.middlewares[0].one == 1
    assert view.middlewares[0].two == 2


@pytest.mark.asyncio()
async def test_register_func_handler():
    view = CustomMessageView()

    @view()
    async def func_handler(event: MessageCute) -> None:
        pass

    assert len(view.handlers) == 1
    assert isinstance(view.handlers[0], FuncHandler)
    assert view.handlers[0] == func_handler
    assert view.handlers[0].function == func_handler.function


@pytest.mark.asyncio()
async def test_register_auto_rule():
    view = CustomMessageView()

    class SomeRule(ABCRule[MessageCute]):
        async def check(self, event: MessageCute) -> bool: ...

    view.auto_rules.append(SomeRule())
    assert len(view.auto_rules) == 1
    assert isinstance(view.auto_rules[0], SomeRule)


@pytest.mark.asyncio()
async def test_register_return_manager():
    view = CustomMessageView()

    @view.return_manager.register_manager(bytes)
    async def manager(value: bytes, event: MessageCute, ctx: Context) -> None: ...

    assert isinstance(view.return_manager, MessageReturnManager)
    assert manager in view.return_manager.managers


@pytest.mark.asyncio()
async def test_view_check_and_process(api_instance, message_update):
    view = CustomMessageView()

    @view()
    async def handler(message: MessageCute):
        assert isinstance(message, MessageCute) is True

    assert await view.check(message_update) is True
    assert await view.process(message_update, api_instance, Context()) is True


@pytest.mark.asyncio()
async def test_process_pre_middleware(api_instance, message_update):
    view = CustomMessageView()
    view.middlewares.append(PreMiddleware())

    @view()
    async def handler(message: MessageCute):
        return None

    assert await view.check(message_update) is True
    assert await view.process(message_update, api_instance, Context()) is True


@pytest.mark.asyncio()
async def test_process_post_middleware(api_instance, message_update):
    view = CustomMessageView()
    view.middlewares.append(PostMiddleware())

    @view()
    async def handler(message: MessageCute):
        return b"123data"

    assert await view.check(message_update) is True
    assert await view.process(message_update, api_instance, Context()) is True


@pytest.mark.asyncio()
async def test_process_with_rule(api_instance, message_update):
    view = CustomMessageView()

    @view(Text("Hello, Telegrinder! btw, laurelang - nice pure logical programming launguage ^_^"))
    async def handler(message: MessageCute):
        return None

    assert await view.check(message_update) is True
    assert await view.process(message_update, api_instance, Context()) is True


@pytest.mark.asyncio()
async def test_process_with_return_manager(api_instance, message_update):
    view = CustomMessageView()

    @view()
    async def handler(message: MessageCute):
        return 123

    assert await view.check(message_update) is True
    assert await view.process(message_update, api_instance, Context()) is True
