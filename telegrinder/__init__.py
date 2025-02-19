"""Telegrinder

Modern visionary telegram bot framework.

* Type hinted
* Customizable and extensible
* Ready to use scenarios and rules
* Fast models built on [msgspec](https://github.com/jcrist/msgspec)
* Both low-level and high-level API
* Support [optional dependecies](https://github.com/timoniq/telegrinder/blob/dev/docs/guide/optional_dependencies.md)

Basic example:

```python
from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import Text

api = API(token=Token("123:token"))
bot = Telegrinder(api)
logger.set_level("INFO")


@bot.on.message(Text("/start"))
async def start(message: Message):
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
    ABCStateView,
    ABCView,
    AudioReplyHandler,
    BaseCute,
    BaseReturnManager,
    BaseStateView,
    BaseView,
    CallbackQueryCute,
    CallbackQueryReturnManager,
    CallbackQueryRule,
    CallbackQueryView,
    ChatJoinRequestCute,
    ChatJoinRequestRule,
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
    InlineQueryRule,
    MediaGroupReplyHandler,
    MessageCute,
    MessageReplyHandler,
    MessageReturnManager,
    MessageRule,
    MessageView,
    PhotoReplyHandler,
    Polling,
    PreCheckoutQueryCute,
    PreCheckoutQueryManager,
    PreCheckoutQueryView,
    RawEventView,
    ShortState,
    StateViewHasher,
    StickerReplyHandler,
    Telegrinder,
    UpdateCute,
    VideoReplyHandler,
    ViewBox,
    WaiterMachine,
    register_manager,
)
from .client import ABCClient, AiohttpClient, AiosonicClient
from .model import Model
from .modules import logger
from .tools.error_handler import ABCErrorHandler, ErrorHandler
from .tools.formatting import HTMLFormatter
from .tools.global_context import ABCGlobalContext, CtxVar, GlobalContext, ctx_var
from .tools.i18n import (
    ABCTranslator,
    ABCTranslatorMiddleware,
    I18nEnum,
    SimpleI18n,
    SimpleTranslator,
)
from .tools.input_file_directory import InputFileDirectory
from .tools.keyboard import (
    AnyMarkup,
    Button,
    InlineButton,
    InlineKeyboard,
    Keyboard,
    RowButtons,
)
from .tools.lifespan import Lifespan
from .tools.loop_wrapper import ABCLoopWrapper, DelayedTask, LoopWrapper
from .tools.magic import cache_translation, get_cached_translation, magic_bundle
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
    "ABCClient",
    "ABCDispatch",
    "ABCErrorHandler",
    "ABCGlobalContext",
    "ABCHandler",
    "ABCLoopWrapper",
    "ABCMiddleware",
    "ABCPolling",
    "ABCReturnManager",
    "ABCRule",
    "ABCScenario",
    "ABCStateStorage",
    "ABCStateStorage",
    "ABCStateView",
    "ABCTranslator",
    "ABCTranslatorMiddleware",
    "ABCView",
    "API",
    "APIError",
    "APIResponse",
    "APIServerError",
    "AiohttpClient",
    "AiosonicClient",
    "AnyMarkup",
    "AudioReplyHandler",
    "BaseCute",
    "BaseReturnManager",
    "BaseStateView",
    "BaseView",
    "Bot",
    "Button",
    "CALLBACK_QUERY_FOR_MESSAGE",
    "CALLBACK_QUERY_FROM_CHAT",
    "CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE",
    "CallbackQuery",
    "CallbackQueryCute",
    "CallbackQueryReturnManager",
    "CallbackQueryRule",
    "CallbackQueryView",
    "ChatJoinRequest",
    "ChatJoinRequestCute",
    "ChatJoinRequestRule",
    "ChatJoinRequestView",
    "ChatMemberUpdated",
    "ChatMemberUpdatedCute",
    "ChatMemberView",
    "Checkbox",
    "Choice",
    "Context",
    "CtxVar",
    "DelayedTask",
    "Dispatch",
    "DocumentReplyHandler",
    "ErrorHandler",
    "FuncHandler",
    "GlobalContext",
    "HTMLFormatter",
    "Hasher",
    "I18nEnum",
    "InlineButton",
    "InlineKeyboard",
    "InlineQuery",
    "InlineQueryCute",
    "InlineQueryReturnManager",
    "InlineQueryRule",
    "InputFileDirectory",
    "Keyboard",
    "Lifespan",
    "LoopWrapper",
    "MESSAGE_FROM_USER",
    "MESSAGE_FROM_USER_IN_CHAT",
    "MESSAGE_IN_CHAT",
    "MediaGroupReplyHandler",
    "MemoryStateStorage",
    "MemoryStateStorage",
    "Message",
    "MessageCute",
    "MessageReplyHandler",
    "MessageReplyHandler",
    "MessageReturnManager",
    "MessageRule",
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
    "SimpleI18n",
    "SimpleTranslator",
    "StateData",
    "StateData",
    "StateViewHasher",
    "StickerReplyHandler",
    "Telegrinder",
    "Token",
    "Update",
    "UpdateCute",
    "VideoReplyHandler",
    "ViewBox",
    "WaiterMachine",
    "cache_translation",
    "ctx_var",
    "get_cached_translation",
    "logger",
    "magic_bundle",
    "register_manager",
)
