import typing

from telegrinder.bot.dispatch.view.base import EventModelView
from telegrinder.bot.rules.media import IsMediaGroup
from telegrinder.types.objects import Message

if typing.TYPE_CHECKING:
    from nodnod.agent.base import Agent

    from telegrinder.bot.dispatch.return_manager.abc import ABCReturnManager


class MediaGroupView(EventModelView[Message]):
    def __init__(
        self,
        *,
        return_manager: ABCReturnManager | None = None,
        agent_cls: type[Agent] | None = None,
    ) -> None:
        super().__init__(model=Message, return_manager=return_manager, agent_cls=agent_cls)

        self.filter = IsMediaGroup()


__all__ = ("MediaGroupView",)
