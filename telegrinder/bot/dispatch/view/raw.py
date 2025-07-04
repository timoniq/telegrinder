from telegrinder.bot.dispatch.view.abc import ABCEventRawView
from telegrinder.bot.dispatch.view.base import BaseView


class RawEventView(ABCEventRawView, BaseView):
    def __init__(self) -> None:
        super().__init__()


__all__ = ("RawEventView",)
