from unittest.mock import AsyncMock

import msgspec
import pytest
from kungfu.library import Ok, Sum
from msgspex import decoder

from telegrinder.api.api import API, Token
from telegrinder.bot.cute_types.message import MessageCute, execute_method_answer, execute_method_edit
from telegrinder.types.objects import Message

from .test_utils import MockedHttpClient


def make_message() -> Message:
    return decoder.decode(
        msgspec.json.encode(
            {
                "message_id": 1,
                "date": 1_713_971_200,
                "chat": {
                    "id": 1,
                    "type": "private",
                    "first_name": "Cute",
                },
                "text": "hello",
            }
        ),
        type=Message,
    )


def make_message_cute(api: API) -> MessageCute:
    return MessageCute.from_update(make_message(), bound_api=api)


def make_api() -> API:
    return API(Token("123:ABCdef"), http=MockedHttpClient())


@pytest.mark.asyncio()
async def test_execute_method_answer_is_lazy(mocker):
    api = make_api()
    message_cute = make_message_cute(api)
    source_message = make_message()
    spy = mocker.spy(MessageCute, "from_update")
    spy.reset_mock()
    api.send_message = AsyncMock(return_value=Ok(source_message))

    result = await execute_method_answer(message_cute, "send_message", {})

    assert spy.call_count == 0
    assert result.unwrap().message_id == source_message.message_id
    assert spy.call_count == 1


@pytest.mark.asyncio()
async def test_execute_method_edit_is_lazy(mocker):
    api = make_api()
    message_cute = make_message_cute(api)
    source_message = make_message()
    spy = mocker.spy(MessageCute, "from_update")
    spy.reset_mock()
    api.edit_message_text = AsyncMock(return_value=Ok(Sum[Message, bool](source_message)))

    result = await execute_method_edit(message_cute, "edit_message_text", {})

    assert spy.call_count == 0
    assert result.unwrap().v.message_id == source_message.message_id
    assert spy.call_count == 1


@pytest.mark.asyncio()
async def test_message_forward_is_lazy(mocker):
    api = make_api()
    message_cute = make_message_cute(api)
    source_message = make_message()
    spy = mocker.spy(MessageCute, "from_update")
    spy.reset_mock()
    api.forward_message = AsyncMock(return_value=Ok(source_message))

    result = await message_cute.forward(chat_id=2)

    assert spy.call_count == 0
    assert result.unwrap().message_id == source_message.message_id
    assert spy.call_count == 1
