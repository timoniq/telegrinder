import types
import typing

from telegrinder.api import API
from telegrinder.node import CallbackDataModel, CallbackQueryNode, ComposeError, Polymorphic, impl

from .data import OpenId, PaginatedData, SwitchPage
from .paginator import Paginator

GenericAlias: typing.TypeAlias = types.GenericAlias


class _PaginatorItem[T: PaginatedData, F](Polymorphic):
    model_t: type[T]
    paginator: type[Paginator[T]]

    def __class_getitem__(cls, data: tuple[type[T], type[Paginator[T]]]) -> type["_PaginatorItem[T, F]"]:
        model_t, paginator = data
        cls.model_t = model_t
        cls.paginator = paginator
        return cls

    @impl
    async def compose_open_id(
        cls,
        api: API,
        callback_data: CallbackDataModel[OpenId],
    ) -> T:
        if not cls.paginator.validate_action(callback_data):
            raise ComposeError("Paginator action does not belong to this paginator")
        return await cls.paginator.from_action(api, callback_data).get_detail(callback_data.open_id)

    @impl
    async def compose_switch_page(
        cls,
        event: CallbackQueryNode,
        api: API,
        callback_data: CallbackDataModel[SwitchPage],
    ) -> typing.NoReturn:
        if not cls.paginator.validate_action(callback_data):
            raise ComposeError("Paginator action does not belong to this paginator")

        await event.edit_reply_markup(
            reply_markup=(
                await cls.paginator.from_action(api, callback_data).get_keyboard(
                    page=callback_data.page_number
                )
            ),
        )
        raise ComposeError("Switch page.")


if typing.TYPE_CHECKING:
    type PaginatorItem[T, F] = typing.Annotated[T, F]
else:
    PaginatorItem = _PaginatorItem


__all__ = ("PaginatorItem",)
