import typing

from telegrinder.api import ABCAPI, API
from telegrinder.model import Model

UpdateT = typing.TypeVar("UpdateT", bound=Model, contravariant=True)


class CuteType(typing.Generic[UpdateT], typing.Protocol):
    api: ABCAPI

    @property
    def ctx_api(self) -> API:
        ...

    @classmethod
    def from_update(cls, update: UpdateT, bound_api: ABCAPI) -> typing.Self:
        ...

    def to_dict(self) -> dict[str, typing.Any]:
        ...
