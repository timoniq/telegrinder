import typing

from telegrinder.api import ABCAPI, API
from telegrinder.model import Model

UpdateT = typing.TypeVar("UpdateT", bound=Model)


@typing.dataclass_transform()
class BaseCute(typing.Generic[UpdateT]):
    api: ABCAPI

    @classmethod
    def from_update(cls, update: UpdateT, bound_api: ABCAPI) -> typing.Self:
        return cls(**update.to_dict(), api=bound_api)

    @property
    def ctx_api(self) -> API:
        assert isinstance(self.api, API)
        return self.api

    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ):
        exclude_fields = exclude_fields or set()
        return super().to_dict(exclude_fields={"api"} | exclude_fields)  # type: ignore
