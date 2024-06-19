import typing

from fntypes.co import Nothing, Some

from telegrinder.api import ABCAPI
from telegrinder.msgspec_utils import Option
from telegrinder.types import Model, Update

from .base import BaseCute

ModelT = typing.TypeVar("ModelT", bound=Model)


class UpdateCute(BaseCute[Update], Update, kw_only=True):
    api: ABCAPI

    @property
    def incoming_update(self) -> Model:
        return getattr(self, self.update_type.value).unwrap()

    def get_event(self, event_model: type[ModelT]) -> Option[ModelT]:
        if isinstance(self.incoming_update, event_model):
            return Some(self.incoming_update)
        return Nothing()


__all__ = ("UpdateCute",)
