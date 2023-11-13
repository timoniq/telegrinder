from telegrinder.api import ABCAPI
from telegrinder.option import Nothing, Option, Some
from telegrinder.types import Update, UpdateType

from .base import BaseCute


class UpdateCute(BaseCute[Update], Update, kw_only=True):
    api: ABCAPI

    @property
    def update_type(self) -> Option[UpdateType]:
        for name, update in self.to_dict(
            exclude_fields={"update_id"},
        ).items():
            if update is not None:
                return Some(UpdateType(name))
        return Nothing
