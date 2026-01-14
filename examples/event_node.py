import typing

from telegrinder import API, Telegrinder, Token
from telegrinder.modules import setup_logger
from telegrinder.node import EventNode
from telegrinder.rules import IsUpdateType, Text
from telegrinder.types import UpdateType
from telegrinder.types.objects import Message

setup_logger()

bot = Telegrinder(API(Token.from_env()))


@bot.on.raw(Text(["hello", "hi"], ignore_case=True))
async def handle_raw_message(raw_msg: EventNode[Message]) -> None:
    await bot.api.send_message(chat_id=raw_msg.chat_id, text="Hello, World!")


@bot.on.raw(IsUpdateType(UpdateType.CALLBACK_QUERY))
async def handle_raw_cb(event: EventNode[dict[str, typing.Any]]) -> None:
    await bot.api.answer_callback_query(callback_query_id=event["id"])


bot.run_forever(skip_updates=True)
