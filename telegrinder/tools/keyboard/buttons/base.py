import dataclasses
import typing

from telegrinder.tools.fullname import fullname


class BaseButton:
    def get_data(self) -> dict[str, typing.Any]:
        assert dataclasses.is_dataclass(self), f"{fullname(self)} is not a dataclass."
        return {k: v for k, v in dataclasses.asdict(self).items() if v is not None}


@dataclasses.dataclass(kw_only=True)
class BaseStaticButton(BaseButton):
    row: bool = dataclasses.field(default=False, repr=False)


__all__ = ("BaseButton", "BaseStaticButton")
