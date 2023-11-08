import typing

from telegrinder.api import ABCAPI, API
from telegrinder.model import Model, dataclass_to_dict

Update = Model


@typing.dataclass_transform(kw_only_default=True)
class BaseCute:
    api: ABCAPI

    @property
    def ctx_api(self) -> API:
        return self.api  # type: ignore

    @classmethod
    def from_update(cls, update: Update, bound_api: ABCAPI) -> typing.Self:
        return cls(**update.to_dict(), api=bound_api)  # type: ignore

    def to_dict(
        self,
        *,
        exclude_fields: set[str] | None = None,
    ):
        return dataclass_to_dict(
            self,  # type: ignore
            exclude_fields={"api", *(exclude_fields or ())},
        )
