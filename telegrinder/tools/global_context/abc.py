from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod

import typing_extensions as typing

T = typing.TypeVar("T", default=typing.Any)


@dataclasses.dataclass(repr=False, frozen=True)
class CtxVar(typing.Generic[T]):
    value: T
    const: bool = dataclasses.field(default=False, kw_only=True)

    def __repr__(self) -> str:
        return "<{}(value={!r})>".format(
            ("Const" if self.const else "") + CtxVar.__name__,
            self.value,
        )


@dataclasses.dataclass(repr=False, frozen=True)
class GlobalCtxVar(CtxVar[T], typing.Generic[T]):
    name: str
    value: T
    const: bool = dataclasses.field(default=False, kw_only=True)

    def __repr__(self) -> str:
        return "<{}({}={})>".format(
            self.__class__.__name__,
            self.name,
            repr(CtxVar(self.value, const=self.const)),
        )

    @classmethod
    def from_var(
        cls,
        name: str,
        ctx_value: T | CtxVariable[T],
        const: bool = False,
    ) -> typing.Self:
        var = CtxVar(ctx_value, const=const) if not isinstance(ctx_value, CtxVar | GlobalCtxVar) else ctx_value
        return cls(**dict(var.__dict__) | dict(name=name))


class ABCGlobalContext(ABC, typing.Generic[T]):
    @abstractmethod
    def __getattr__(self, __name: str) -> typing.Any:
        pass

    @abstractmethod
    def __setattr__(self, __name: str, __value: T | CtxVariable[T]) -> None:
        pass

    @abstractmethod
    def __delattr__(self, __name: str) -> None:
        pass


CtxVariable = CtxVar[T] | GlobalCtxVar[T]


__all__ = (
    "ABCGlobalContext",
    "CtxVar",
    "CtxVariable",
    "GlobalCtxVar",
)
