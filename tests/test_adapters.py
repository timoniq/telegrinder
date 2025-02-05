import pytest
from fntypes.co import Ok

from telegrinder.bot.cute_types import CallbackQueryCute, MessageCute, UpdateCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.node.composer import NodeSession
from telegrinder.node.text import Text
from telegrinder.tools.adapter import Event, EventAdapter, NodeAdapter, RawUpdateAdapter
from telegrinder.types.enums import UpdateType


@pytest.mark.asyncio()
async def test_event_adapter_with_event_message_cute(api_instance, message_update):
    adapter = EventAdapter(UpdateType.MESSAGE, MessageCute)
    context = Context(raw_update=message_update)

    result = adapter.adapt(api_instance, message_update, context)

    assert isinstance(result, Ok)
    assert isinstance(result.value, MessageCute)
    assert adapter.ADAPTED_VALUE_KEY in context
    assert isinstance(context[adapter.ADAPTED_VALUE_KEY], MessageCute)
    assert context[adapter.ADAPTED_VALUE_KEY] is result.value


@pytest.mark.asyncio()
async def test_event_adapter_with_event_callback_query_cute(api_instance, callback_query_update):
    adapter = EventAdapter(UpdateType.CALLBACK_QUERY, CallbackQueryCute)
    context = Context(raw_update=callback_query_update)

    result = adapter.adapt(api_instance, callback_query_update, context)

    assert isinstance(result, Ok)
    assert isinstance(result.value, CallbackQueryCute)
    assert adapter.ADAPTED_VALUE_KEY in context
    assert isinstance(context[adapter.ADAPTED_VALUE_KEY], CallbackQueryCute)
    assert context[adapter.ADAPTED_VALUE_KEY] is result.value


@pytest.mark.asyncio()
async def test_raw_update_adapter_with_message_update(api_instance, message_update):
    adapter = RawUpdateAdapter()
    context = Context(raw_update=message_update)

    result = adapter.adapt(api_instance, message_update, context)

    assert isinstance(result, Ok)
    assert isinstance(result.value, UpdateCute)
    assert isinstance(result.value.incoming_update, MessageCute)
    assert adapter.ADAPTED_VALUE_KEY in context
    assert isinstance(context[adapter.ADAPTED_VALUE_KEY], UpdateCute)
    assert context[adapter.ADAPTED_VALUE_KEY] is result.value


@pytest.mark.asyncio()
async def test_raw_update_adapter_with_callback_query_update(api_instance, callback_query_update):
    adapter = RawUpdateAdapter()
    context = Context(raw_update=callback_query_update)

    result = adapter.adapt(api_instance, callback_query_update, context)

    assert isinstance(result, Ok)
    assert isinstance(result.value, UpdateCute)
    assert isinstance(result.value.incoming_update, CallbackQueryCute)
    assert adapter.ADAPTED_VALUE_KEY in context
    assert isinstance(context[adapter.ADAPTED_VALUE_KEY], UpdateCute)
    assert context[adapter.ADAPTED_VALUE_KEY] is result.value


@pytest.mark.asyncio()
async def test_node_adapter(api_instance, message_update):
    adapter = NodeAdapter(Text)  # type: ignore
    context = Context(raw_update=message_update)

    result = await adapter.adapt(api_instance, message_update, context)

    assert isinstance(result, Ok)
    assert isinstance(result.value, Event)
    assert isinstance(result.value.obj[0], NodeSession)
    assert (
        result.value.obj[0].value.__class__ is str
        and result.value.obj[0].value
        == "Hello, Telegrinder! btw, laurelang - nice pure logical programming launguage ^_^"
    )
