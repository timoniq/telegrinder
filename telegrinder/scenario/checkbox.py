import dataclasses
import enum
import secrets
import typing

from telegrinder.scenario.abc import ABCScenario
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard
from telegrinder.tools.waiter_machine.hasher.callback import CALLBACK_QUERY_FOR_MESSAGE

if typing.TYPE_CHECKING:
    from _typeshed import SupportsRAdd

    from telegrinder.api.api import API
    from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
    from telegrinder.bot.dispatch.view.base import View
    from telegrinder.tools.waiter_machine.hasher.hasher import Hasher
    from telegrinder.tools.waiter_machine.machine import WaiterMachine
    from telegrinder.types.enums import KeyboardButtonStyle
    from telegrinder.types.objects import InlineKeyboardMarkup

type MessageId = int
type CallbackQueryView = View


class ChoiceAction(enum.StrEnum):
    READY = "ready"
    CANCEL = "cancel"


@dataclasses.dataclass(slots=True)
class Option[Key: typing.Hashable]:
    key: Key
    is_picked: bool
    default_text: str
    picked_text: str
    code: str
    icon_id: str | int | None = None
    style: KeyboardButtonStyle | None = None

    def __eq__(self, other: typing.Self, /) -> bool:
        return self.code == other.code

    def __bool__(self) -> bool:
        return self.is_picked

    def __add__(self, other: typing.Self, /) -> int:
        return self.is_picked + other.is_picked

    def __radd__(self, other: SupportsRAdd[bool, int], /) -> int:
        return self.is_picked + other


class _Checkbox[T](ABCScenario):
    options: list[Option[typing.Hashable]]

    def __init__(
        self,
        chat_id: int,
        message: str,
        *,
        parse_mode: str | None = None,
        max_in_row: int = 3,
        callback_answer: str | None = None,
        callback_answer_as_alert: bool | None = None,
        ready_text: str = "Ready",
        ready_icon_id: str | int | None = None,
        ready_style: KeyboardButtonStyle | None = None,
        cancel_text: str | None = None,
        cancel_icon_id: str | int | None = None,
        cancel_style: KeyboardButtonStyle | None = None,
        waiter_machine: WaiterMachine | None = None,
    ) -> None:
        self.options = []
        self.random_code = secrets.token_hex(8)
        self.chat_id = chat_id
        self.message = message
        self.callback_answer = callback_answer
        self.callback_answer_as_alert = (
            None if callback_answer_as_alert is True and not callback_answer else callback_answer_as_alert
        )
        self.waiter_machine = waiter_machine
        self.max_in_row = max_in_row
        self.parse_mode = parse_mode
        self.ready = ready_text
        self.ready_icon_id = ready_icon_id
        self.ready_style = ready_style
        self.cancel_text = cancel_text
        self.cancel_icon_id = cancel_icon_id
        self.cancel_style = cancel_style

    def __repr__(self) -> str:
        return (
            "<{}@{!r} choices={!r} max_in_row={} waiter_machine={!r} ready_text={!r} "
            "cancel_text={!r} chat_id={} message={!r}>"
        ).format(
            type(self).__name__,
            self.random_code,
            self.options,
            self.max_in_row,
            self.waiter_machine,
            self.ready,
            self.cancel_text,
            self.chat_id,
            self.message,
        )

    def get_markup(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboard()

        for option in self.options:
            kb.add(
                InlineButton(
                    text=option.default_text if not option.is_picked else option.picked_text,
                    callback_data=f"{self.random_code}/{option.code}",
                    icon_id=option.icon_id,
                    style=option.style,
                ),
            )

            if len(kb.keyboard[-1]) == self.max_in_row:
                kb.row()

        kb.row()
        kb.add(
            InlineButton(
                text=self.ready,
                callback_data=f"{self.random_code}/{ChoiceAction.READY}",
                icon_id=self.ready_icon_id,
                style=self.ready_style,
            ),
        )

        if self.cancel_text is not None:
            kb.row()
            kb.add(
                InlineButton(
                    text=self.cancel_text,
                    callback_data=f"{self.random_code}/{ChoiceAction.CANCEL}",
                    icon_id=self.cancel_icon_id,
                    style=self.cancel_style,
                ),
            )

        return kb.get_markup()

    def validate_code(self, data: str, /) -> str | typing.Literal[False]:
        code = data.removeprefix(f"{self.random_code}/")

        match code:
            case ChoiceAction.READY:
                return False
            case ChoiceAction.CANCEL:
                self.options = []
                return False

        return False if data == code else code

    def add_option[Key: typing.Hashable](
        self,
        key: Key,
        default_text: str,
        picked_text: str,
        *,
        is_picked: bool = False,
        icon_id: str | int | None = None,
        style: KeyboardButtonStyle | None = None,
    ) -> Checkbox[Key]:
        option = Option(
            key,
            is_picked,
            default_text,
            picked_text,
            code=secrets.token_hex(8),
            icon_id=icon_id,
            style=style,
        )
        self.options.append(option)  # type: ignore
        return self  # type: ignore

    async def handle(self, cb: CallbackQueryCute) -> bool:
        code = self.validate_code(cb.data.unwrap())

        if not code:
            return False

        changed = False

        for option in self.options:
            if option.code == code:
                # Toggle option
                option.is_picked = not option.is_picked
                changed = True
                break

        if changed:
            await cb.edit_text(
                text=self.message,
                parse_mode=self.parse_mode,
                reply_markup=self.get_markup(),
            )

        return True

    async def wait(
        self,
        api: API,
        hasher: Hasher[CallbackQueryCute, MessageId] = CALLBACK_QUERY_FOR_MESSAGE,
        *,
        view: CallbackQueryView | None = None,
        waiter_machine: WaiterMachine | None = None,
    ) -> tuple[dict[typing.Hashable, bool], MessageId]:
        waiter_machine = self.waiter_machine if waiter_machine is None else waiter_machine

        if not self.options or waiter_machine is None:
            raise AssertionError

        message = (
            await api.send_message(
                chat_id=self.chat_id,
                text=self.message,
                parse_mode=self.parse_mode,
                reply_markup=self.get_markup(),
            )
        ).unwrap()
        should_continue = True

        while should_continue:
            callback, _ = await waiter_machine.wait(
                hasher,
                view=view,
                data=message.message_id,
            )
            should_continue = await self.handle(callback)
            await callback.answer(text=self.callback_answer, show_alert=self.callback_answer_as_alert)

        return ({option.key: option.is_picked for option in self.options}, message.message_id)


if typing.TYPE_CHECKING:

    class Checkbox[Key: typing.Hashable](_Checkbox):
        options: list[Option[Key]]

        @typing.overload
        async def wait(self, api: API, /) -> tuple[dict[Key, bool], MessageId]: ...

        @typing.overload
        async def wait(
            self, api: API, hasher: Hasher[CallbackQueryCute, MessageId]
        ) -> tuple[dict[Key, bool], MessageId]: ...

        @typing.overload
        async def wait(
            self,
            api: API,
            *,
            view: CallbackQueryView | None,
        ) -> tuple[dict[Key, bool], MessageId]: ...

        @typing.overload
        async def wait(
            self,
            api: API,
            *,
            waiter_machine: WaiterMachine | None,
        ) -> tuple[dict[Key, bool], MessageId]: ...

        @typing.overload
        async def wait(
            self,
            api: API,
            *,
            view: CallbackQueryView | None,
            waiter_machine: WaiterMachine | None,
        ) -> tuple[dict[Key, bool], MessageId]: ...

        @typing.overload
        async def wait(
            self,
            api: API,
            hasher: Hasher[CallbackQueryCute, MessageId],
            *,
            view: CallbackQueryView | None,
        ) -> tuple[dict[Key, bool], MessageId]: ...

        @typing.overload
        async def wait(
            self,
            api: API,
            hasher: Hasher[CallbackQueryCute, MessageId],
            *,
            waiter_machine: WaiterMachine | None,
        ) -> tuple[dict[Key, bool], MessageId]: ...

        @typing.overload
        async def wait(
            self,
            api: API,
            hasher: Hasher[CallbackQueryCute, MessageId],
            *,
            view: CallbackQueryView | None,
            waiter_machine: WaiterMachine | None,
        ) -> tuple[dict[Key, bool], MessageId]: ...

        async def wait(
            self,
            api: API,
            hasher: Hasher[CallbackQueryCute, MessageId] = CALLBACK_QUERY_FOR_MESSAGE,
            *,
            view: CallbackQueryView | None = None,
            waiter_machine: WaiterMachine | None = None,
        ) -> tuple[dict[Key, bool], MessageId]: ...

else:
    Checkbox = _Checkbox


__all__ = ("Checkbox", "Option")
