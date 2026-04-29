import typing

from telegrinder.scenario.checkbox import CallbackQueryView, Checkbox, MessageId
from telegrinder.tools.waiter_machine.hasher.callback import CALLBACK_QUERY_FOR_MESSAGE

if typing.TYPE_CHECKING:
    from telegrinder.api.api import API
    from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
    from telegrinder.tools.waiter_machine.hasher.hasher import Hasher
    from telegrinder.tools.waiter_machine.machine import WaiterMachine


class Choice[Key: typing.Hashable](Checkbox[Key]):
    async def handle(self, cb: CallbackQueryCute) -> bool:
        code = self.validate_code(cb.data.unwrap())

        if not code:
            return False

        changed = False

        for option in self.options:
            if option.code == code:
                changed = True if changed else not option.is_picked
                option.is_picked = True
            else:
                changed = True if changed else option.is_picked
                option.is_picked = False

        if changed:
            await cb.edit_text(
                text=self.message,
                parse_mode=self.parse_mode,
                reply_markup=self.get_markup(),
            )

        return True

    @typing.overload
    async def wait(self, api: API, /) -> tuple[Key, MessageId]: ...

    @typing.overload
    async def wait(self, api: API, hasher: Hasher[CallbackQueryCute, MessageId]) -> tuple[Key, MessageId]: ...

    @typing.overload
    async def wait(
        self,
        api: API,
        *,
        view: CallbackQueryView | None,
    ) -> tuple[Key, MessageId]: ...

    @typing.overload
    async def wait(
        self,
        api: API,
        *,
        waiter_machine: WaiterMachine | None,
    ) -> tuple[Key, MessageId]: ...

    @typing.overload
    async def wait(
        self,
        api: API,
        *,
        view: CallbackQueryView | None,
        waiter_machine: WaiterMachine | None,
    ) -> tuple[Key, MessageId]: ...

    @typing.overload
    async def wait(
        self,
        api: API,
        hasher: Hasher[CallbackQueryCute, MessageId],
        *,
        view: CallbackQueryView | None,
    ) -> tuple[Key, MessageId]: ...

    @typing.overload
    async def wait(
        self,
        api: API,
        hasher: Hasher[CallbackQueryCute, MessageId],
        *,
        waiter_machine: WaiterMachine | None,
    ) -> tuple[Key, MessageId]: ...

    @typing.overload
    async def wait(
        self,
        api: API,
        hasher: Hasher[CallbackQueryCute, MessageId],
        *,
        view: CallbackQueryView | None,
        waiter_machine: WaiterMachine | None,
    ) -> tuple[Key, MessageId]: ...

    async def wait(
        self,
        api: API,
        hasher: Hasher[CallbackQueryCute, MessageId] = CALLBACK_QUERY_FOR_MESSAGE,
        *,
        view: CallbackQueryView | None = None,
        waiter_machine: WaiterMachine | None = None,
    ) -> tuple[Key, MessageId]:
        if sum(self.options) != 1:
            raise ValueError("Exactly one option must be picked.")

        options, message_id = await super().wait(api, hasher, view=view, waiter_machine=waiter_machine)
        picked_key = next((key for key, value in options.items() if value is True), None)

        if picked_key is None:
            raise ValueError("Unable to get a key from the picked option.")

        return (picked_key, message_id)


__all__ = ("Choice",)
