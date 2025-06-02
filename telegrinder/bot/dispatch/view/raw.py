from telegrinder.bot.dispatch.view.abc import ABCEventRawView
from telegrinder.bot.dispatch.view.base import BaseView


class RawEventView(ABCEventRawView, BaseView):
    pass


__all__ = ("RawEventView",)
