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
    def incoming_update(self) -> Option[Model]:
        return getattr(
            self,
            self.update_type.expect("Update object has no incoming update.").value,
        )

    def get_event(self, event_model: type[ModelT]) -> Option[ModelT]:
        match self.incoming_update:
            case Some(event) if isinstance(event, event_model):
                return Some(event)
        return Nothing()


__all__ = ("UpdateCute",)
