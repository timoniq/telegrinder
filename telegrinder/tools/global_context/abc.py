import dataclasses
import typing
from abc import ABC, abstractmethod

T = typing.TypeVar("T")
CtxValue = typing.Union[typing.Any, "CtxVar[T]"]


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
class GlobalCtxVar(typing.Generic[T]):
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
    def collect(cls, name: str, ctx_value: CtxValue) -> typing.Self:
        ctx_value = ctx_value if isinstance(ctx_value, CtxVar) else CtxVar(ctx_value)
        return cls(name, **dataclasses.asdict(ctx_value))


class ABCGlobalContext(ABC):
    @abstractmethod
    def __getattr__(self, __name: str) -> typing.Any:
        pass

    @abstractmethod
    def __setattr__(self, __name: str, __value: CtxValue) -> None:
        pass

    @abstractmethod
    def __delattr__(self, __name: str) -> None:
        pass

    @abstractmethod
    def get(self, name: str, var_value_type: type[T]) -> GlobalCtxVar[T]:
        pass

    @abstractmethod
    def get_value(self, name: str, value_type: type[T]) -> T:
        pass

    @abstractmethod
    def clear(self, *, include_consts: bool) -> None:
        pass
