import dataclasses
import typing

from kungfu.library.monad.result import Error as Err
from kungfu.library.monad.result import Ok

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.router.abc import ABCRouter
from telegrinder.bot.dispatch.view.box import ViewBox
from telegrinder.modules import log_scope, logger
from telegrinder.tools.magic.inspect import get_frame_module_name
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.view.base import ErrorView, EventView, RawEventView, View
    from telegrinder.bot.dispatch.view.media_group import MediaGroupView


@dataclasses.dataclass(kw_only=True)
class Router[
    MessageView: EventView = EventView,
    EditedMessageView: EventView = EventView,
    ChannelPostView: EventView = EventView,
    EditedChannelPostView: EventView = EventView,
    BusinessConnectionView: EventView = EventView,
    BusinessMessageView: EventView = EventView,
    EditedBusinessMessageView: EventView = EventView,
    DeletedBusinessMessagesView: EventView = EventView,
    MessageReactionView: EventView = EventView,
    MessageReactionCountView: EventView = EventView,
    InlineQueryView: EventView = EventView,
    ChosenInlineResultView: EventView = EventView,
    CallbackQueryView: EventView = EventView,
    ShippingQueryView: EventView = EventView,
    PreCheckoutQueryView: EventView = EventView,
    PurchasedPaidMediaView: EventView = EventView,
    PollView: EventView = EventView,
    PollAnswerView: EventView = EventView,
    MyChatMemberView: EventView = EventView,
    ChatMemberView: EventView = EventView,
    ChatJoinRequestView: EventView = EventView,
    ChatBoostView: EventView = EventView,
    RemovedChatBoostView: EventView = EventView,
    MediaGroup: View = MediaGroupView,
    Error: ErrorView = ErrorView,
    RawEvent: RawEventView = RawEventView,
](
    ABCRouter,
    ViewBox[
        MessageView,
        EditedMessageView,
        ChannelPostView,
        EditedChannelPostView,
        BusinessConnectionView,
        BusinessMessageView,
        EditedBusinessMessageView,
        DeletedBusinessMessagesView,
        MessageReactionView,
        MessageReactionCountView,
        InlineQueryView,
        ChosenInlineResultView,
        CallbackQueryView,
        ShippingQueryView,
        PreCheckoutQueryView,
        PurchasedPaidMediaView,
        PollView,
        PollAnswerView,
        MyChatMemberView,
        ChatMemberView,
        ChatJoinRequestView,
        ChatBoostView,
        RemovedChatBoostView,
        MediaGroup,
        Error,
        RawEvent,
    ],
):
    def __post_init__(self) -> None:
        self.module = get_frame_module_name()
        self.name = ":".join((self.module, self.__class__.__name__, hex(id(self))))

    def __repr__(self) -> str:
        return f"<{self.name}>"

    def __hash__(self) -> int:
        return hash(self.name)

    def __bool__(self) -> bool:
        return any((*self.event_views.values(), *self.views.values()))

    @staticmethod
    async def check_view(view: View, api: API, update: Update, context: Context) -> bool:
        with log_scope(repr, view):
            await logger.adebug("Checking view...")

            match await view.check(api, update, context):
                case Ok():
                    return True
                case Err(error):
                    await logger.adebug("Checking view failed: {}", error)

            return False

    async def process_view(
        self,
        view: View,
        api: API,
        update: Update,
        context: Context,
        *,
        raw_process_on_fail: bool = False,
    ) -> bool:
        with log_scope(repr, view):
            await logger.adebug("Processing...")
            result = await view.process(api, update, context)

            match result:
                case Err(error) if isinstance(error, Exception):
                    raise error from None

            await logger.ainfo("{}", result.error if not result else result.value)

            result = bool(result)
            if (
                not result
                and raw_process_on_fail is True
                and self.raw
                and await self.check_view(self.raw, api, update, context)
            ):
                return await self.process_view(self.raw, api, update, context)

            return result

    async def route(self, api: API, update: Update, context: Context) -> bool:
        with log_scope(lambda: self.module):
            try:
                for event_view in filter(None, self.event_views.values()):
                    if await self.check_view(event_view, api, update, context):
                        return await self.process_view(event_view, api, update, context, raw_process_on_fail=True)

                return False
            except Exception as exception:
                if self.event_error:
                    context.exceptions_update[self] = exception  # type: ignore

                raise


__all__ = ("Router",)
