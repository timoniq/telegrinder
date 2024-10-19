import types
import typing

from telegrinder.node import CallbackDataModel, CallbackQueryNode, ComposeError, Polymorphic, impl
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup

from .data import OpenIdButton, PaginatedDataProtocol, PaginatorButton, SwitchPageButton
from .fetcher import Fetcher

GenericAlias: typing.TypeAlias = types.GenericAlias


class _PaginatorData[T: PaginatedDataProtocol, F](Polymorphic):
    __cached_paginator_nodes__: typing.ClassVar[
        dict[type[typing.Any], type["_PaginatorData[typing.Any, typing.Any]"]]
    ] = {}

    model_t: type[T]
    fetcher: type[Fetcher[T]]

    def __class_getitem__(cls, data: typing.Any | tuple[type[T], F]) -> type["_PaginatorData[T, F]"]:
        if isinstance(data, tuple) and len(data) == 2:
            model_t, fetcher = data
            origin_model_t = typing.get_origin(model_t) or model_t

            paginator_node = cls.__cached_paginator_nodes__.get(origin_model_t)
            if paginator_node is None:
                paginator_node = type(
                    "Paginator" + model_t.__name__,
                    (cls,),
                    {"model_t": model_t, "fetcher": fetcher} | cls.__dict__,
                )
                cls.__cached_paginator_nodes__[origin_model_t] = paginator_node

            return paginator_node
        return super().__class_getitem__(data)  # type: ignore

    @classmethod
    def is_paginator_data(cls, data: PaginatorButton) -> bool:
        return data.paginator == cls.model_t.__name__

    @impl
    async def compose_open_id(cls, callback_data: CallbackDataModel[OpenIdButton]) -> T:
        if not cls.is_paginator_data(callback_data):
            raise ComposeError("Paginator data does not belong to this paginator")
        return await cls.model_t.fetch(callback_data.open_id)

    @impl
    async def compose_switch_page(
        cls, event: CallbackQueryNode, callback_data: CallbackDataModel[SwitchPageButton]
    ) -> typing.NoReturn:
        if not cls.is_paginator_data(callback_data):
            raise ComposeError("Paginator data does not belong to this paginator")

        await event.edit_reply_markup(
            reply_markup=await cls.get_keyboard(page_number=callback_data.page_number),
        )
        raise ComposeError("Switch page.")

    @classmethod
    async def get_keyboard(cls, page_number: int = 1) -> InlineKeyboardMarkup:
        first_page = await cls.fetcher().get_page(page_number)
        keyboard = InlineKeyboard()

        for item in first_page.items:
            keyboard.add(InlineButton(str(item), callback_data=OpenIdButton(cls.model_t.__name__, item.id)))
            keyboard.row()

        if first_page.page_number > 1:
            keyboard.add(
                InlineButton("<", callback_data=SwitchPageButton(cls.model_t.__name__, page_number - 1))
            )

        keyboard.add(
            InlineButton(
                f"{min(first_page.max_page, page_number)}/{first_page.max_page}", callback_data="nope"
            )
        )

        if first_page.page_number < first_page.max_page:
            keyboard.add(
                InlineButton(">", callback_data=SwitchPageButton(cls.model_t.__name__, page_number + 1))
            )

        return keyboard.get_markup()


class Paginator[T: PaginatedDataProtocol, F: Fetcher](
    _PaginatorData[T, Fetcher[T]] if typing.TYPE_CHECKING else GenericAlias
):
    def __class_getitem__(
        cls, data: tuple[type[T], type[Fetcher[T]]], /
    ) -> type["_PaginatorData[T, Fetcher[T]]"]:
        model_t, fetcher = data
        return _PaginatorData[model_t, fetcher]


if typing.TYPE_CHECKING:
    type PaginatorData[T, F] = typing.Annotated[T, F]
else:
    PaginatorData = _PaginatorData


__all__ = ("Paginator", "PaginatorData")
