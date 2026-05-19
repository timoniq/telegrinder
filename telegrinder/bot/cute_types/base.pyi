import dataclasses
import typing

from msgspex import Model

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.tools.magic.shortcut import shortcut
from telegrinder.types.objects import Update

def compose_method_params[Cute: BaseCute](
    params: dict[str, typing.Any],
    update: Cute,
    *,
    default_params: set[str | tuple[str, str]] | None = ...,
    validators: dict[str, typing.Callable[[Cute], bool]] | None = ...,
    hooks: dict[str, typing.Callable[[typing.Any], tuple[str, typing.Any]]] | None = ...,
) -> dict[str, typing.Any]: ...

class BaseShortcuts[Cute: BaseCute[typing.Any] = typing.Any]:
    cute: typing.Final[Cute]

class BaseCute[T: Model = typing.Any](Model, kw_only=True):
    ctx_api: dataclasses.InitVar[API]

    api: typing.ClassVar[API]
    """Alias for `bound_api`."""

    bound_api: typing.ClassVar[API]
    """`API` bound to the cute model."""

    bound_update: typing.ClassVar[Update]
    """`Update` object if this cute type is an update."""

    @classmethod
    def __compose__(cls, update: Update, context: Context) -> typing.Self: ...
    @classmethod
    def from_update(cls, update: T, bound_api: API) -> typing.Self: ...
    @classmethod
    def from_data[**P, R](cls: typing.Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R: ...
    @classmethod
    def from_mapping(cls, data: typing.Mapping[str, typing.Any], bound_api: API) -> typing.Self: ...
    @classmethod
    def from_dict(cls, data: dict[str, typing.Any], bound_api: API) -> typing.Self: ...
    @classmethod
    def from_raw(cls, raw: str | bytes, bound_api: API) -> typing.Self: ...
    def bind(self, update: Update, api: API) -> typing.Self: ...
    def bind_api(self, api: API, /) -> typing.Self: ...
    def bind_update(self, update: Update, /) -> typing.Self: ...
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
