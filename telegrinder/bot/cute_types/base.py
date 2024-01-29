import typing

from telegrinder.api import ABCAPI, API
from telegrinder.model import Model

UpdateT = typing.TypeVar("UpdateT", bound=Model)

if typing.TYPE_CHECKING:

    class BaseCute(Model, typing.Generic[UpdateT]):
        api: ABCAPI

        @classmethod
        def from_update(cls, update: UpdateT, bound_api: ABCAPI) -> typing.Self:
            ...

        @property
        def ctx_api(self) -> API:
            ...

        def to_dict(
            self,
            *,
            exclude_fields: set[str] | None = None,
        ) -> dict[str, typing.Any]:
            ...

else:

    class BaseCute(typing.Generic[UpdateT]):
        api: ABCAPI

        @classmethod
        def from_update(cls, update, bound_api):
            return cls(**update.to_dict(), api=bound_api)

        @property
        def ctx_api(self):
            assert isinstance(self.api, API)
            return self.api

        def to_dict(self, *, exclude_fields=None):
            exclude_fields = exclude_fields or set()
            return super().to_dict(exclude_fields={"api"} | exclude_fields)


__all__ = ("BaseCute",)
