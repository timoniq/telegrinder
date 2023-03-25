from telegrinder.types import Update
from telegrinder.api import API, ABCAPI


class UpdateCute(Update):
    api: ABCAPI

    @property
    def ctx_api(self) -> API:
        return self.api  # type: ignore

    def to_dict(self) -> dict:
        dct = super().to_dict()
        dct.pop("api")
        return dct

    @classmethod
    def from_update(cls, update: Update, bound_api: API):
        return cls(**update.to_dict(), api=bound_api)
