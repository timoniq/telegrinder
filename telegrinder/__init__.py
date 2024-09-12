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

from .api import API, APIError, APIResponse, Token
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
from .bot.rules import StateMeta
from .client import ABCClient, AiohttpClient
from .model import Model
from .modules import logger
from .tools import (
    ABCErrorHandler,
    ABCGlobalContext,
    ABCLoopWrapper,
    ABCStateStorage,
    ABCTranslator,
    ABCTranslatorMiddleware,
    AnyMarkup,
    Button,
    CtxVar,
    DelayedTask,
    ErrorHandler,
    FormatString,
    GlobalContext,
    HTMLFormatter,
    I18nEnum,
    InlineButton,
    InlineKeyboard,
    Keyboard,
    KeyboardSetBase,
    KeyboardSetYAML,
    Lifespan,
    LoopWrapper,
    MemoryStateStorage,
    ParseMode,
    RowButtons,
    SimpleI18n,
    SimpleTranslator,
    StateData,
    ctx_var,
    magic_bundle,
)

Update: typing.TypeAlias = UpdateCute
Message: typing.TypeAlias = MessageCute
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
    "AiohttpClient",
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
    "FormatString",
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
    "Keyboard",
    "KeyboardSetBase",
    "KeyboardSetYAML",
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
    "RawEventView",
    "RowButtons",
    "ShortState",
    "SimpleI18n",
    "SimpleTranslator",
    "StateData",
    "StateData",
    "StateMeta",
    "StateMeta",
    "StateViewHasher",
    "StickerReplyHandler",
    "Telegrinder",
    "Token",
    "Update",
    "UpdateCute",
    "VideoReplyHandler",
    "ViewBox",
    "WaiterMachine",
    "ctx_var",
    "logger",
    "magic_bundle",
    "register_manager",
)
