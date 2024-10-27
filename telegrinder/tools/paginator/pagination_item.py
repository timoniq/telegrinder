import typing

from telegrinder.api.api import API
from telegrinder.node import CallbackDataModel, CallbackQueryNode, ComposeError, Polymorphic, impl
from telegrinder.node.base import FactoryNode

from .data import OpenId, PaginatedData, SwitchPage
from .paginator import Paginator


class _PaginatorItem[T: PaginatedData, F](Polymorphic, FactoryNode):
    model_t: type[T]
    paginator: type[Paginator[T]]

    def __class_getitem__(cls, data: tuple[type[T], type[Paginator[T]]]) -> type["_PaginatorItem[T, F]"]:
        model_t, paginator = data
        return cls(model_t=model_t, paginator=paginator)  # type: ignore

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
                    page=callback_data.page_number,
                )
            ),
        )
        raise ComposeError("Switch page.")


if typing.TYPE_CHECKING:
    type PaginatorItem[Data: PaginatedData, P: Paginator[typing.Any]] = typing.Annotated[Data, P]
else:
    PaginatorItem = _PaginatorItem


__all__ = ("PaginatorItem",)
