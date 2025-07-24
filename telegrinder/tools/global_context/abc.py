from __future__ import annotations

import dataclasses
import typing
from abc import ABC, abstractmethod

NOVALUE: typing.Final[object] = object()


@dataclasses.dataclass(frozen=True)
class CtxVar[T = typing.Any]:
    value: T
    factory: typing.Any = dataclasses.field(default=NOVALUE, kw_only=True)
    const: bool = dataclasses.field(default=False, kw_only=True)


@dataclasses.dataclass(repr=False, frozen=True)
class GlobalCtxVar[T = typing.Any](CtxVar[T]):
    name: str
    value: T
    factory: typing.Any = dataclasses.field(default=NOVALUE, kw_only=True)
    const: bool = dataclasses.field(default=False, kw_only=True)

    def __repr__(self) -> str:
        return "<{}({}={})>".format(
            self.__class__.__name__,
            self.name,
            repr(CtxVar(self.value, const=self.const, factory=self.factory)),
        )

    @classmethod
    def from_var(
        cls,
        name: str,
        ctx_value: T | CtxVariable[T],
        const: bool = False,
    ) -> typing.Self:
        var = CtxVar(ctx_value, const=const) if not isinstance(ctx_value, CtxVar | GlobalCtxVar) else ctx_value
        if var.value is NOVALUE and var.factory is not NOVALUE:
            var = dataclasses.replace(var, value=var.factory())
        return cls(**dict(var.__dict__) | dict(name=name))


class ABCGlobalContext[T = typing.Any](ABC):
    @abstractmethod
    def __getattr__(self, __name: str) -> typing.Any:
        pass

    @abstractmethod
    def __setattr__(self, __name: str, __value: T | CtxVariable[T]) -> None:
        pass

    @abstractmethod
    def __delattr__(self, __name: str) -> None:
        pass


type CtxVariable[T = typing.Any] = CtxVar[T] | GlobalCtxVar[T]


__all__ = (
    "ABCGlobalContext",
    "CtxVar",
    "CtxVariable",
    "GlobalCtxVar",
)
