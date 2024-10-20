import abc
import typing

from telegrinder.api import API
from telegrinder.model import Model
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup

from .data import OpenId, Page, PageAction, PaginatedData, SwitchPage

NONE_CALLBACK_DATA = str(None)


class Paginator[T: PaginatedData](Model):
    api: API

    @classmethod
    def from_action(cls, api: API, action: PageAction) -> typing.Self:
        return cls(api=api, **action.filters)

    @classmethod
    def validate_action(cls, action: PageAction) -> bool:
        return action.pg_key == cls.get_pg_key()

    @classmethod
    def get_pg_key(cls) -> str:
        return cls.__name__

    @abc.abstractmethod
    async def get_page(self, page_number: int) -> Page[T]: ...

    @abc.abstractmethod
    async def get_detail(self, id) -> T: ...

    async def get_keyboard(self, page: int = 1) -> InlineKeyboardMarkup:
        first_page = await self.get_page(page)
        keyboard = InlineKeyboard()
        filters = {}

        for item in first_page.items:
            keyboard.add(InlineButton(str(item), callback_data=OpenId(self.get_pg_key(), item.id, filters)))
            keyboard.row()

        if first_page.page_number > 1:
            keyboard.add(InlineButton("<", callback_data=SwitchPage(self.get_pg_key(), page - 1, filters)))

        keyboard.add(
            InlineButton(
                f"{min(first_page.max_page, page)}/{first_page.max_page}",
                callback_data=NONE_CALLBACK_DATA,
            )
        )

        if first_page.page_number < first_page.max_page:
            keyboard.add(InlineButton(">", callback_data=SwitchPage(self.get_pg_key(), page + 1, filters)))

        return keyboard.get_markup()


__all__ = ("Paginator",)
