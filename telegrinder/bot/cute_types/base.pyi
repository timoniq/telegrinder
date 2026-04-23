import typing

from msgspex.model import Model

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.tools.magic.shortcut import shortcut
from telegrinder.types.objects import Update

def compose_method_params[Cute: BaseCute](
    params: dict[str, typing.Any],
    update: Cute,
    *,
    default_params: set[str | tuple[str, str]] | None = None,
    validators: dict[str, typing.Callable[[Cute], bool]] | None = None,
) -> dict[str, typing.Any]: ...

class BaseShortcuts[Cute: BaseCute[typing.Any] = typing.Any]:
    cute: typing.Final[Cute]

class BaseCute[T: Model = typing.Any](Model):
    api: typing.ClassVar[typing.Final[API]]
    """Alias for `bound_api`."""

    bound_api: typing.ClassVar[typing.Final[API]]
    """`API` bound to the cute model."""

    bound_update: typing.ClassVar[typing.Final[Update]]
    """`Update` object bound to the cute model."""

    @classmethod
    def __compose__(cls, update: Update, context: Context) -> typing.Self: ...
    @classmethod
    def from_update(cls, update: T, bound_api: API) -> typing.Self: ...
    def bind(self, update: Update, api: API) -> typing.Self: ...
    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]: ...
    def to_full_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, typing.Any]: ...

__all__ = ("BaseCute", "BaseShortcuts", "compose_method_params", "shortcut")
