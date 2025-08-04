import dataclasses
import enum
import typing

from telegrinder import (
    API,
    CallbackQuery,
    Message,
    Telegrinder,
    Token,
)
from telegrinder.node import ChatId
from telegrinder.rules import PayloadModelRule, Text
from telegrinder.tools import MsgPackSerializer
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard

api = API(token=Token.from_env())
bot = Telegrinder(api)


@enum.unique
class MenuAction(enum.Enum):
    show_fact = enum.auto()
    show_store = enum.auto()


@enum.unique
class StoreAction(enum.Enum):
    buy_coffee = enum.auto()
    buy_tea = enum.auto()
    back_to_menu = enum.auto()


@dataclasses.dataclass(slots=True, frozen=True)
class MenuCallback:
    __key__ = "menu"
    __serializer__ = MsgPackSerializer[typing.Self]

    action: MenuAction


@dataclasses.dataclass(slots=True, frozen=True)
class StoreCallback:
    __key__ = "store"
    __serializer__ = MsgPackSerializer[typing.Self]

    action: StoreAction
    item: str = ""
    price: int = 0


class MainMenuKeyboard(InlineKeyboard):
    show_fact = InlineButton(
        "🎯 Show Random Fact",
        callback_data=MenuCallback(action=MenuAction.show_fact),
        new_row=True,
    )
    show_store = InlineButton(
        "🛒 Open Store",
        callback_data=MenuCallback(action=MenuAction.show_store),
    )


class StoreKeyboard(InlineKeyboard):
    buy_coffee = InlineButton(
        "☕ Coffee - $3",
        callback_data=StoreCallback(action=StoreAction.buy_coffee, item="Coffee", price=3),
        new_row=True,
    )
    buy_tea = InlineButton(
        "🍵 Tea - $2",
        callback_data=StoreCallback(action=StoreAction.buy_tea, item="Tea", price=2),
        new_row=True,
    )
    back_to_menu = InlineButton(
        "⬅️ Back to Menu",
        callback_data=StoreCallback(action=StoreAction.back_to_menu),
    )


@bot.on.message(Text("/start"))
async def start(message: Message) -> None:
    await message.answer(
        text="hi there. pick an option below:",
        reply_markup=MainMenuKeyboard.get_markup(),
    )


@bot.on.callback_query(StoreKeyboard.back_to_menu)
async def back_menu(cb: CallbackQuery, chat_id: ChatId) -> None:
    await cb.api.send_message(
        chat_id=chat_id,
        text="hi there. pick an option below:",
        reply_markup=MainMenuKeyboard.get_markup(),
    )
    await cb.answer()


@bot.on.callback_query(MainMenuKeyboard.show_fact)
async def interest_fact(cb: CallbackQuery) -> None:
    await cb.answer("brace yourself: he comes again", show_alert=True)


@bot.on.callback_query(MainMenuKeyboard.show_store)
async def store(cb: CallbackQuery) -> None:
    await cb.edit_text("what do u want?", reply_markup=StoreKeyboard.get_markup())
    await cb.answer()


@bot.on.callback_query(PayloadModelRule(StoreCallback, alias="my_model"))
async def view_store(cb: CallbackQuery, chat_id: ChatId, my_model: StoreCallback) -> None:
    await cb.api.send_message(chat_id=chat_id, text=f"your choice - {my_model.item}; price - {my_model.price}")
    await cb.answer()


bot.run_forever(skip_updates=True)
