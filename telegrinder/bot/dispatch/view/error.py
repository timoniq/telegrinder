from telegrinder.bot.dispatch.view.base import BaseView


class ErrorView(BaseView):
    def __init__(self) -> None:
        super().__init__()


__all__ = ("ErrorView",)
