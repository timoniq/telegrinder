"""Modern visionary telegram bot framework.

* Type hinted & [type functional](https://github.com/timoniq/telegrinder/blob/dev/docs/tutorial/en/3_functional_bits.md)
* Customizable and extensible
* Fast models built on [msgspec](https://github.com/jcrist/msgspec)
* API client powered by fast [rnet](https://github.com/0x676e67/rnet) library
* Both low-level and high-level API
* Convenient [dependency injection](https://github.com/timoniq/telegrinder/blob/dev/docs/tutorial/en/5_nodes.md) via nodes

Basic example:

```python
from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import setup_logger
from telegrinder.rules import Text

setup_logger(level="INFO")
api = API(token=Token("123:token"))
bot = Telegrinder(api)


@bot.on.message(Text("/start"))
async def start(message: Message) -> None:
    me = (await api.get_me()).unwrap()
    await message.answer(f"Hello, {message.from_user.full_name}! I'm {me.full_name}.")


bot.run_forever()
```
"""

import typing

from .api import API, APIError, APIResponse, APIServerError, Token
from .bot import (
    CALLBACK_QUERY_FOR_MESSAGE,
    CALLBACK_QUERY_FROM_CHAT,
    CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE,
    MESSAGE_FROM_USER,
    MESSAGE_FROM_USER_IN_CHAT,
    MESSAGE_IN_CHAT,
    ABCDispatch,
    ABCHandler,
    ABCMiddleware,
    ABCPolling,
    ABCReturnManager,
    ABCRouter,
    ABCRule,
    ABCScenario,
    ABCView,
    AudioReplyHandler,
    BaseCute,
    BaseReturnManager,
    BusinessConnectionCute,
    BusinessMessagesDeletedCute,
    CallbackQueryCute,
    CallbackQueryReturnManager,
    ChatBoostRemovedCute,
    ChatBoostUpdatedCute,
    ChatJoinRequestCute,
    ChatMemberUpdatedCute,
    Checkbox,
    Choice,
    ChosenInlineResultCute,
    Context,
    Dispatch,
    DocumentReplyHandler,
    ErrorView,
    EventModelView,
    EventView,
    FuncHandler,
    Hasher,
    InlineQueryCute,
    InlineQueryReturnManager,
    MediaGroupReplyHandler,
    MediaGroupView,
    MessageCute,
    MessageReactionCountUpdatedCute,
    MessageReactionUpdatedCute,
    MessageReplyHandler,
    MessageReturnManager,
    PaidMediaPurchasedCute,
    PhotoReplyHandler,
    PollAnswerCute,
    PollCute,
    Polling,
    PreCheckoutQueryCute,
    PreCheckoutQueryReturnManager,
    RawEventView,
    Router,
    ShippingQueryCute,
    ShortState,
    StickerReplyHandler,
    Telegrinder,
    UpdateCute,
    VideoReplyHandler,
    View,
    ViewBox,
    WaiterMachine,
    action,
    register_manager,
)
from .client import ABCClient, RnetClient
from .model import Model, field
from .modules import logger, setup_logger
from .tools.global_context import ABCGlobalContext, GlobalContext, TelegrinderContext
from .tools.input_file_directory import InputFileDirectory
from .tools.keyboard import (
    ABCKeyboard,
    Button,
    InlineButton,
    InlineKeyboard,
    Keyboard,
    RowButtons,
)
from .tools.lifespan import Lifespan
from .tools.loop_wrapper import DelayedTask, LoopWrapper
from .tools.parse_mode import ParseMode
from .tools.state_storage import ABCStateStorage, MemoryStateStorage, StateData

Update: typing.TypeAlias = UpdateCute
Message: typing.TypeAlias = MessageCute
PreCheckoutQuery: typing.TypeAlias = PreCheckoutQueryCute
ChatJoinRequest: typing.TypeAlias = ChatJoinRequestCute
ChatMemberUpdated: typing.TypeAlias = ChatMemberUpdatedCute
CallbackQuery: typing.TypeAlias = CallbackQueryCute
InlineQuery: typing.TypeAlias = InlineQueryCute
ChosenInlineResult: typing.TypeAlias = ChosenInlineResultCute
ShippingQuery: typing.TypeAlias = ShippingQueryCute
Poll: typing.TypeAlias = PollCute
PollAnswer: typing.TypeAlias = PollAnswerCute
PaidMediaPurchased: typing.TypeAlias = PaidMediaPurchasedCute
ChatBoostRemoved: typing.TypeAlias = ChatBoostRemovedCute
ChatBoostUpdated: typing.TypeAlias = ChatBoostUpdatedCute
BusinessConnection: typing.TypeAlias = BusinessConnectionCute
BusinessMessagesDeleted: typing.TypeAlias = BusinessMessagesDeletedCute
MessageReactionCountUpdated: typing.TypeAlias = MessageReactionCountUpdatedCute
MessageReactionUpdated: typing.TypeAlias = MessageReactionUpdatedCute
Bot: typing.TypeAlias = Telegrinder


__all__ = (
    "API",
    "CALLBACK_QUERY_FOR_MESSAGE",
    "CALLBACK_QUERY_FROM_CHAT",
    "CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE",
    "MESSAGE_FROM_USER",
    "MESSAGE_FROM_USER_IN_CHAT",
    "MESSAGE_IN_CHAT",
    "ABCClient",
    "ABCDispatch",
    "ABCGlobalContext",
    "ABCHandler",
    "ABCKeyboard",
    "ABCMiddleware",
    "ABCPolling",
    "ABCReturnManager",
    "ABCRouter",
    "ABCRule",
    "ABCScenario",
    "ABCStateStorage",
    "ABCView",
    "APIError",
    "APIResponse",
    "APIServerError",
    "AudioReplyHandler",
    "BaseCute",
    "BaseReturnManager",
    "Bot",
    "Button",
    "CallbackQuery",
    "CallbackQueryCute",
    "CallbackQueryReturnManager",
    "ChatBoostRemoved",
    "ChatBoostUpdatedCute",
    "ChatJoinRequest",
    "ChatJoinRequestCute",
    "ChatMemberUpdated",
    "ChatMemberUpdatedCute",
    "Checkbox",
    "Choice",
    "ChosenInlineResult",
    "ChosenInlineResultCute",
    "Context",
    "DelayedTask",
    "Dispatch",
    "DocumentReplyHandler",
    "ErrorView",
    "EventModelView",
    "EventView",
    "FuncHandler",
    "GlobalContext",
    "Hasher",
    "InlineButton",
    "InlineKeyboard",
    "InlineQuery",
    "InlineQueryCute",
    "InlineQueryReturnManager",
    "InputFileDirectory",
    "Keyboard",
    "Lifespan",
    "LoopWrapper",
    "MediaGroupReplyHandler",
    "MediaGroupView",
    "MemoryStateStorage",
    "Message",
    "MessageCute",
    "MessageReactionCountUpdated",
    "MessageReactionCountUpdatedCute",
    "MessageReactionUpdated",
    "MessageReactionUpdatedCute",
    "MessageReplyHandler",
    "MessageReturnManager",
    "Model",
    "PaidMediaPurchased",
    "PaidMediaPurchasedCute",
    "ParseMode",
    "PhotoReplyHandler",
    "Poll",
    "PollAnswer",
    "PollAnswerCute",
    "PollCute",
    "Polling",
    "PreCheckoutQuery",
    "PreCheckoutQueryCute",
    "PreCheckoutQueryReturnManager",
    "RawEventView",
    "RnetClient",
    "Router",
    "RowButtons",
    "ShippingQuery",
    "ShippingQueryCute",
    "ShortState",
    "StateData",
    "StickerReplyHandler",
    "Telegrinder",
    "TelegrinderContext",
    "Token",
    "Update",
    "UpdateCute",
    "VideoReplyHandler",
    "View",
    "ViewBox",
    "ViewBox",
    "WaiterMachine",
    "action",
    "field",
    "logger",
    "register_manager",
    "setup_logger",
)
