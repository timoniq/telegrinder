from fntypes.co import Nothing, Some

from telegrinder.api import ABCAPI
from telegrinder.msgspec_utils import Option
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
        return Nothing()


__all__ = ("UpdateCute",)
