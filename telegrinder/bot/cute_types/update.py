import typing

from telegrinder.api import ABCAPI, API
from telegrinder.types import Update


class UpdateCute(Update):
    api: ABCAPI

    @property
    def ctx_api(self) -> API:
        return self.api  # type: ignore

    @classmethod
    def from_update(cls, update: Update, bound_api: ABCAPI) -> typing.Self:
        return cls(**update.to_dict(), api=bound_api)

    def to_dict(self) -> dict[str, typing.Any]:
        return super().to_dict(exclude_fields={"api"})
