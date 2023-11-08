from telegrinder.api import ABCAPI
from telegrinder.types import Update, UpdateType

from .base import BaseCute


class UpdateCute(BaseCute, Update, kw_only=True):
    api: ABCAPI

    @property
    def update_type(self) -> UpdateType:  # type: ignore
        for name, update in self.to_dict(
            exclude_fields={"update_id"},
        ).items():
            if update is not None:
                return UpdateType(name)
