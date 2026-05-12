from unittest.mock import AsyncMock

import msgspec
import pytest
from kungfu.library import Ok, Sum
from msgspex import decoder

from telegrinder.api.api import API, Token
from telegrinder.bot.cute_types.message import DEFAULT_ANSWER, DEFAULT_EDIT, MessageCute
from telegrinder.tools.bound_cute import BoundCute
from telegrinder.types.objects import Message

from .test_utils import MockedHttpClient


def make_message() -> Message:
    return decoder.decode(msgspec.json.encode(make_message_payload()), type=Message)


def make_message_payload() -> dict:
    return {
        "message_id": 1,
        "date": 1_713_971_200,
        "chat": {
            "id": 1,
            "type": "private",
            "first_name": "Cute",
        },
        "text": "hello",
    }


def make_raw(value) -> msgspec.Raw:
    return msgspec.Raw(msgspec.json.encode(value))


def make_message_cute(api: API) -> MessageCute:
    return MessageCute.from_update(make_message(), bound_api=api)


def make_api() -> API:
    return API(Token("123:ABCdef"), http=MockedHttpClient())


@pytest.mark.asyncio()
async def test_execute_method_answer_is_lazy(mocker):
    api = make_api()
    message_cute = make_message_cute(api)
    source_message = make_message()
    spy = mocker.spy(MessageCute, "bind_api")
    spy.reset_mock()
    api.request_raw = AsyncMock(return_value=Ok(make_raw(make_message_payload())))
    api.send_message = AsyncMock()

    result = await DEFAULT_ANSWER(message_cute, "send_message", {}, BoundCute[MessageCute])

    api.request_raw.assert_awaited_once()
    request_raw_call = api.request_raw.await_args
    assert request_raw_call is not None
    assert request_raw_call.args[0] == "sendMessage"
    api.send_message.assert_not_awaited()
    assert spy.call_count == 0
    assert result.unwrap().message_id == source_message.message_id
    assert spy.call_count == 1


@pytest.mark.asyncio()
async def test_shortcut_uses_return_type_for_cute_result(mocker):
    api = make_api()
    message_cute = make_message_cute(api)
    source_message = make_message()
    spy = mocker.spy(MessageCute, "bind_api")
    spy.reset_mock()
    api.request_raw = AsyncMock(return_value=Ok(make_raw(make_message_payload())))
    api.send_message = AsyncMock()

    result = await message_cute.answer("hello")

    api.request_raw.assert_awaited_once()
    request_raw_call = api.request_raw.await_args
    assert request_raw_call is not None
    assert request_raw_call.args[0] == "sendMessage"
    api.send_message.assert_not_awaited()
    assert spy.call_count == 0
    assert result.unwrap().message_id == source_message.message_id
    assert spy.call_count == 1


@pytest.mark.asyncio()
async def test_execute_method_answer_uses_api_method_when_result_is_not_cute():
    api = make_api()
    message_cute = make_message_cute(api)
    api.request_raw = AsyncMock()
    api.send_message_draft = AsyncMock(return_value=Ok(True))

    result = await DEFAULT_ANSWER(message_cute, "send_message_draft", {}, bool)

    assert result.unwrap() is True
    api.send_message_draft.assert_awaited_once()
    api.request_raw.assert_not_awaited()


@pytest.mark.asyncio()
async def test_execute_method_answer_list_result_is_lazy(mocker):
    api = make_api()
    message_cute = make_message_cute(api)
    spy = mocker.spy(MessageCute, "bind_api")
    spy.reset_mock()
    api.request_raw = AsyncMock(return_value=Ok(make_raw([make_message_payload()])))

    result = await DEFAULT_ANSWER(message_cute, "send_media_group", {}, list[BoundCute[MessageCute]])

    api.request_raw.assert_awaited_once()
    request_raw_call = api.request_raw.await_args
    assert request_raw_call is not None
    assert request_raw_call.args[0] == "sendMediaGroup"
    assert spy.call_count == 0
    assert result.unwrap()[0].message_id == make_message().message_id
    assert spy.call_count == 1


@pytest.mark.asyncio()
async def test_execute_method_edit_is_lazy(mocker):
    api = make_api()
    message_cute = make_message_cute(api)
    source_message = make_message()
    spy = mocker.spy(MessageCute, "bind_api")
    spy.reset_mock()
    api.request_raw = AsyncMock(return_value=Ok(make_raw(make_message_payload())))
    api.edit_message_text = AsyncMock()

    result = await DEFAULT_EDIT(message_cute, "edit_message_text", {}, Sum[BoundCute[MessageCute], bool])

    api.request_raw.assert_awaited_once()
    request_raw_call = api.request_raw.await_args
    assert request_raw_call is not None
    assert request_raw_call.args[0] == "editMessageText"
    api.edit_message_text.assert_not_awaited()
    assert spy.call_count == 0
    assert result.unwrap().v.message_id == source_message.message_id
    assert spy.call_count == 1


@pytest.mark.asyncio()
async def test_message_forward_is_lazy(mocker):
    api = make_api()
    message_cute = make_message_cute(api)
    source_message = make_message()
    spy = mocker.spy(MessageCute, "bind_api")
    spy.reset_mock()
    api.request_raw = AsyncMock(return_value=Ok(make_raw(make_message_payload())))
    api.forward_message = AsyncMock()

    result = await message_cute.forward(chat_id=2)

    api.request_raw.assert_awaited_once()
    request_raw_call = api.request_raw.await_args
    assert request_raw_call is not None
    assert request_raw_call.args[0] == "forwardMessage"
    api.forward_message.assert_not_awaited()
    assert spy.call_count == 0
    assert result.unwrap().message_id == source_message.message_id
    assert spy.call_count == 1
