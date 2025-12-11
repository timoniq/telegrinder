from __future__ import annotations

import dataclasses
import typing

from kungfu.library.monad.result import Error as Err
from kungfu.library.monad.result import Ok

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.router.abc import ABCRouter
from telegrinder.bot.dispatch.view.box import ViewBox
from telegrinder.modules import logger
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
        self.name = ":".join((get_frame_module_name(), self.__class__.__name__, hex(id(self))))

    def __repr__(self) -> str:
        return f"<{self.name}>"

    def __hash__(self) -> int:
        return hash(self.name)

    def __bool__(self) -> bool:
        return any(self.views.values()) or bool(self.raw) or bool(self.error)

    async def route_view(self, view: View, api: API, update: Update, context: Context) -> bool:
        # Check if the view is applicable to the update

        await logger.adebug(
            "Checking view `{!r}` from router `{!r}` for update (id={}, type={!r})...",
            view,
            self,
            update.update_id,
            update.update_type,
        )

        match await view.check(api, update, context):
            case Ok():
                await logger.adebug(
                    "View `{!r}` from router `{!r}` for update (id={}, type={!r}) is okay, processing...",
                    view,
                    self,
                    update.update_id,
                    update.update_type,
                )
                result = await view.process(api, update, context)
                await logger.ainfo(
                    "Update(id={}, type={!r}) processed with view `{!r}` from router `{!r}`. {}",
                    update.update_id,
                    update.update_type,
                    view,
                    self,
                    result.error if not result else result.value,
                )
                return bool(result)
            case Err(error):
                await logger.adebug(
                    "Checking view `{!r}` from router `{!r}` for update (id={}, type={!r}) failed: {}",
                    view,
                    self,
                    update.update_id,
                    update.update_type,
                    error,
                )

        return False

    async def route(self, api: API, update: Update, context: Context) -> bool:
        try:
            # Filtering non-empty views
            for view in filter(None, self.views.values()):
                # Route the non-empty view
                if await self.route_view(view, api, update, context):
                    return True

            return False
        except Exception as exception:
            context.exceptions_update[self] = exception  # type: ignore
            raise


__all__ = ("Router",)
