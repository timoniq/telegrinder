import dataclasses
import enum

from telegrinder import (
    API,
    CallbackQuery,
    Message,
    Telegrinder,
    Token,
)
from telegrinder.modules import logger
from telegrinder.node import ChatId
from telegrinder.rules import PayloadModelRule, Text
from telegrinder.tools import MsgPackSerializer
from telegrinder.tools.keyboard.buttons.static_buttons import StaticInlineButton
from telegrinder.tools.keyboard.static_keyboard import StaticInlineKeyboard

logger.set_level("DEBUG")
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
    action: MenuAction


@dataclasses.dataclass(slots=True, frozen=True)
class StoreCallback:
    __key__ = "store"
    action: StoreAction
    item: str = ""
    price: int = 0


class MainMenuKeyboard(StaticInlineKeyboard):
    serializer = MsgPackSerializer(MenuCallback)

    show_fact = StaticInlineButton(
        "🎯 Show Random Fact",
        callback_data=MenuCallback(action=MenuAction.show_fact),
        callback_data_serializer=serializer,
        row=True,
    )
    show_store = StaticInlineButton(
        "🛒 Open Store",
        callback_data=MenuCallback(action=MenuAction.show_store),
        callback_data_serializer=serializer,
    )


class StoreKeyboard(StaticInlineKeyboard):
    serializer = MsgPackSerializer(StoreCallback)

    buy_coffee = StaticInlineButton(
        "☕ Coffee - $3",
        callback_data=StoreCallback(action=StoreAction.buy_coffee, item="Coffee", price=3),
        callback_data_serializer=serializer,
        row=True,
    )
    buy_tea = StaticInlineButton(
        "🍵 Tea - $2",
        callback_data=StoreCallback(action=StoreAction.buy_tea, item="Tea", price=2),
        callback_data_serializer=serializer,
        row=True,
    )
    back_to_menu = StaticInlineButton(
        "⬅️ Back to Menu",
        callback_data=StoreCallback(action=StoreAction.back_to_menu),
        callback_data_serializer=serializer,
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
    await cb.answer(f"brace yourself: he comes again", show_alert=True)


@bot.on.callback_query(MainMenuKeyboard.show_store)
async def store(cb: CallbackQuery) -> None:
    await cb.edit_text("what do u want?", reply_markup=StoreKeyboard.get_markup())
    await cb.answer()


@bot.on.callback_query(PayloadModelRule(StoreCallback, alias="my_model", serializer=MsgPackSerializer))
async def view_store(cb: CallbackQuery, chat_id: ChatId, my_model: StoreCallback) -> None:
    await cb.api.send_message(chat_id=chat_id, text=f"your choice - {my_model.item}; price - {my_model.price}")
    await cb.answer()


bot.run_forever(skip_updates=True)
