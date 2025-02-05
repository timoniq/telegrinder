import pytest

from telegrinder.bot.cute_types import CallbackQueryCute, MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.process import check_rule
from telegrinder.rules import IsPrivate, MessageRule, PayloadEqRule
from telegrinder.types.objects import CallbackQuery, Message

message_event_with_text = {
    "message_id": 9999,
    "from": {
        "id": 1,
        "is_bot": False,
        "first_name": "Alex",
        "last_name": "Doe",
        "username": "alex777",
        "language_code": "en",
    },
    "chat": {
        "id": 1,
        "first_name": "Alex",
        "last_name": "Doe",
        "is_bot": False,
        "username": "alex777",
        "type": "private",
    },
    "date": 1234567898,
    "text": "",
}

cb_event_with_data = {
    "id": "4382bfdwdsb323b2d9",
    "from": {
        "id": 1,
        "is_bot": False,
        "first_name": "Alex",
        "last_name": "Doe",
        "username": "alex777",
        "language_code": "en",
    },
    "message": message_event_with_text,
    "chat_instance": "23asinstance23442",
    "inline_message_id": "1234csdbsk4839",
    "data": "",
}


class Text(MessageRule):
    def __init__(self, text: str) -> None:
        self.text = text

    def check(self, message: MessageCute) -> bool:
        return message.text.unwrap_or_none() == self.text


def test_rule_callback_data_eq(api_instance):
    cb_event_with_data["data"] = "test"
    cb_update = CallbackQuery.from_dict(cb_event_with_data)
    cb_event = CallbackQueryCute.from_update(cb_update, api_instance)
    assert PayloadEqRule("test").check(cb_event.data.unwrap()) is True
    assert PayloadEqRule("test1").check(cb_event.data.unwrap()) is False


def test_rule_text(api_instance):
    message_event_with_text["text"] = "hello!!!"
    msg_update = Message.from_dict(message_event_with_text)
    msg_event = MessageCute.from_update(msg_update, api_instance)
    assert Text("hello!!!").check(msg_event) is True
    assert Text("hello!!").check(msg_event) is False


@pytest.mark.asyncio()
async def test_rule_is_private_message_source(api_instance, message_update):
    assert await check_rule(api_instance, IsPrivate(), message_update, Context())


@pytest.mark.asyncio()
async def test_rule_is_private_callback_query_source(api_instance, callback_query_update):
    assert await check_rule(api_instance, IsPrivate(), callback_query_update, Context())
