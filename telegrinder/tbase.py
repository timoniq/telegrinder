import pydantic
import typing


def convert(d: typing.Any) -> typing.Any:
    if isinstance(d, BaseModel):
        return d.get_dict()
    elif isinstance(d, dict):
        return {k: convert(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        li = [convert(el) for el in d]
        return li
    return d


class BaseModel(pydantic.BaseModel):
    def get_dict(self) -> dict:
        d = self.dict()
        return {k: convert(v) for k, v in d.items() if v is not None}


__all__ = ("convert", "BaseModel")
