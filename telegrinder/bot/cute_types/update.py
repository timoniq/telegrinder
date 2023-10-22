import typing

from telegrinder.api import ABCAPI, API
from telegrinder.types import Update


class UpdateCute(Update):
    api: ABCAPI

    @property
    def ctx_api(self) -> API:
        return self.api  # type: ignore

    def to_dict(self) -> dict:
        dct = super().to_dict()
        dct.pop("api", None)
        return dct

    @classmethod
    def from_update(cls, update: Update, bound_api: API) -> typing.Self:
        return cls(**update.to_dict(), api=bound_api)
