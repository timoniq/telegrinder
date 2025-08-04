"""Modern visionary telegram bot framework.

* Type hinted & [type functional](https://github.com/timoniq/telegrinder/blob/dev/docs/tutorial/en/3_functional_bits.md)
* Customizable and extensible
* Ready to use scenarios and rules
* Fast models built on [msgspec](https://github.com/jcrist/msgspec)
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
    ABCRule,
    ABCScenario,
    ABCView,
    AudioReplyHandler,
    BaseCute,
    BaseReturnManager,
    BaseView,
    CallbackQueryCute,
    CallbackQueryReturnManager,
    CallbackQueryView,
    ChatJoinRequestCute,
    ChatJoinRequestView,
    ChatMemberUpdatedCute,
    ChatMemberView,
    Checkbox,
    Choice,
    Context,
    Dispatch,
    DocumentReplyHandler,
    FuncHandler,
    Hasher,
    InlineQueryCute,
    InlineQueryReturnManager,
    MediaGroupReplyHandler,
    MessageCute,
    MessageReplyHandler,
    MessageReturnManager,
    MessageView,
    PhotoReplyHandler,
    Polling,
    PreCheckoutQueryCute,
    PreCheckoutQueryManager,
    PreCheckoutQueryView,
    RawEventView,
    ShortState,
    StickerReplyHandler,
    Telegrinder,
    UpdateCute,
    VideoReplyHandler,
    ViewBox,
    WaiterMachine,
    action,
    register_manager,
)
from .client import ABCClient, AiohttpClient
from .model import Model, field
from .modules import logger, setup_logger
from .tools.formatting import HTMLFormatter
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
    "ABCRule",
    "ABCScenario",
    "ABCStateStorage",
    "ABCStateStorage",
    "ABCView",
    "APIError",
    "APIResponse",
    "APIServerError",
    "AiohttpClient",
    "AudioReplyHandler",
    "BaseCute",
    "BaseReturnManager",
    "BaseView",
    "Bot",
    "Button",
    "CallbackQuery",
    "CallbackQueryCute",
    "CallbackQueryReturnManager",
    "CallbackQueryView",
    "ChatJoinRequest",
    "ChatJoinRequestCute",
    "ChatJoinRequestView",
    "ChatMemberUpdated",
    "ChatMemberUpdatedCute",
    "ChatMemberView",
    "Checkbox",
    "Choice",
    "Context",
    "DelayedTask",
    "Dispatch",
    "DocumentReplyHandler",
    "FuncHandler",
    "GlobalContext",
    "HTMLFormatter",
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
    "MemoryStateStorage",
    "MemoryStateStorage",
    "Message",
    "MessageCute",
    "MessageReplyHandler",
    "MessageReplyHandler",
    "MessageReturnManager",
    "MessageView",
    "Model",
    "ParseMode",
    "PhotoReplyHandler",
    "Polling",
    "PreCheckoutQuery",
    "PreCheckoutQueryCute",
    "PreCheckoutQueryManager",
    "PreCheckoutQueryView",
    "RawEventView",
    "RowButtons",
    "ShortState",
    "StateData",
    "StateData",
    "StickerReplyHandler",
    "Telegrinder",
    "TelegrinderContext",
    "Token",
    "Update",
    "UpdateCute",
    "VideoReplyHandler",
    "ViewBox",
    "WaiterMachine",
    "action",
    "field",
    "logger",
    "register_manager",
    "setup_logger",
)
