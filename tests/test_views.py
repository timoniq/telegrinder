import pytest

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.func import FuncHandler
from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware
from telegrinder.bot.dispatch.return_manager.abc import register_manager
from telegrinder.bot.dispatch.return_manager.message import MessageReturnManager
from telegrinder.bot.dispatch.view.base import View
from telegrinder.bot.rules.abc import ABCRule, AndRule
from telegrinder.bot.rules.text import Text


class CustomMessageReturnManager(MessageReturnManager):
    @register_manager(int)
    @staticmethod
    async def int_manager(value: int) -> None:
        assert isinstance(value, int)


class CustomMessageView(View):
    def __init__(self) -> None:
        super().__init__(return_manager=CustomMessageReturnManager())


class PreMiddleware(ABCMiddleware):
    def pre(self, event: MessageCute, ctx: Context) -> bool:
        return True


class PostMiddleware(ABCMiddleware):
    def post(self, ctx: Context) -> None:
        assert ctx.responses == [b"123data"]


@pytest.mark.asyncio()
async def test_register_middleware():
    view = CustomMessageView()

    @view.register_middleware
    class SomeMiddleware(ABCMiddleware):
        async def pre(self, event: MessageCute) -> None:
            pass

    assert len(view.middlewares) == 1
    assert isinstance(view.middlewares.user_middlewares[0], SomeMiddleware)


@pytest.mark.asyncio()
async def test_register_func_handler():
    view = CustomMessageView()

    @view()
    async def func_handler(event: MessageCute) -> None:
        pass

    assert len(view.handlers) == 1
    assert isinstance(view.handlers[0], FuncHandler)
    assert view.handlers[0].function == func_handler


@pytest.mark.asyncio()
async def test_register_auto_rules():
    view = CustomMessageView()

    class Rule(ABCRule):
        async def check(self, event: MessageCute) -> bool: ...

    view.auto_rules = Rule() & Rule()
    assert isinstance(view.auto_rules, AndRule)


@pytest.mark.asyncio()
async def test_register_return_manager():
    view = CustomMessageView()

    assert isinstance(view.return_manager, CustomMessageReturnManager)

    @view.return_manager.register_manager(bytes)
    async def manager(value: bytes, event: MessageCute, ctx: Context) -> None: ...

    assert isinstance(view.return_manager, MessageReturnManager)
    assert manager in view.return_manager.managers


@pytest.mark.asyncio()
async def test_view_check_and_process(api_instance, message_update, message_context):
    view = CustomMessageView()

    @view()
    async def handler(message: MessageCute):
        assert isinstance(message, MessageCute) is True

    assert bool(await view.check(api_instance, message_update, message_context)) is True
    assert bool(await view.process(api_instance, message_update, message_context.copy())) is True


@pytest.mark.asyncio()
async def test_process_pre_middleware(api_instance, message_update, message_context):
    view = CustomMessageView()
    view.middlewares.put(PreMiddleware())

    @view()
    async def handler(message: MessageCute):
        return None

    assert bool(await view.check(api_instance, message_update, message_context)) is True
    assert bool(await view.process(api_instance, message_update, message_context.copy())) is True


@pytest.mark.asyncio()
async def test_process_post_middleware(api_instance, message_update, message_context):
    view = CustomMessageView()
    view.middlewares.put(PostMiddleware())

    @view()
    async def handler(message: MessageCute):
        return b"123data"

    assert bool(await view.check(api_instance, message_update, message_context)) is True
    assert bool(await view.process(api_instance, message_update, message_context.copy())) is True


@pytest.mark.asyncio()
async def test_process_with_rule(api_instance, message_update, message_context):
    view = CustomMessageView()

    @view(Text("Hello, Telegrinder! btw, laurelang - nice pure logical programming launguage ^_^"))
    async def handler(message: MessageCute):
        return None

    assert bool(await view.check(api_instance, message_update, message_context)) is True
    assert bool(await view.process(api_instance, message_update, message_context.copy())) is True


@pytest.mark.asyncio()
async def test_process_with_return_manager(api_instance, message_update, message_context):
    view = CustomMessageView()

    @view()
    async def handler(message: MessageCute):
        return 123

    assert bool(await view.check(api_instance, message_update, message_context)) is True
    assert bool(await view.process(api_instance, message_update, message_context.copy())) is True
