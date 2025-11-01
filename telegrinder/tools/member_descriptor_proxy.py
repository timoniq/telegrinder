from __future__ import annotations

import dataclasses
import operator
import types
import typing


def evaluate_operations(
    obj: typing.Any,
    member_name: str,
    operations: list[Operation],
    /,
) -> typing.Any:
    obj = getattr(obj, member_name)

    for operation in operations:
        if operation.getattribute is not None:
            obj = operator.attrgetter(operation.getattribute)(obj)
        elif operation.getitem is not None:
            obj = operator.itemgetter(operation.getitem)(obj)
        elif operation.method_call is not None:
            obj = operation.method_call(obj)

    return obj


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class MethodCall:
    method_name: str
    args: tuple[typing.Any, ...] = dataclasses.field(default_factory=tuple[typing.Any, ...])
    kwargs: dict[str, typing.Any] = dataclasses.field(default_factory=dict[str, typing.Any])

    def __call__(self, obj: typing.Any, /) -> typing.Any:
        return operator.methodcaller(self.method_name, *self.args, **self.kwargs)(obj)


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class Operation:
    getattribute: str | None = None
    getitem: typing.Any | None = None
    method_call: MethodCall | None = None


class MemberDescriptorProxy:
    _operations: list[Operation]
    _objclass: type[typing.Any]

    __slots__ = ("_descriptor", "_operations", "_member_name", "_objclass")

    def __init__(self, descriptor: types.MemberDescriptorType) -> None:
        self._descriptor = descriptor
        self._member_name = descriptor.__name__
        self._objclass = descriptor.__objclass__
        self._operations = []

    def __getattr__(self, __name: str) -> typing.Any:
        if __name in getattr(type(self), "__static_attributes__"):
            return super().__getattribute__(__name)

        self._operations.append(Operation(getattribute=__name))
        return self

    def __getitem__(self, __item: typing.Any) -> typing.Any:
        self._operations.append(Operation(getitem=__item))
        return self

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        if not self._operations or (operation := self._operations.pop(-1)).getattribute is None:
            raise SyntaxError("No operations to call.")

        self._operations.append(
            Operation(
                method_call=MethodCall(
                    method_name=operation.getattribute,
                    args=args,
                    kwargs=kwargs,
                ),
            ),
        )
        return self

    def __get__(self, instance: typing.Any, owner: typing.Type[typing.Any]) -> typing.Any:
        if instance is None:
            return self
        return self._descriptor.__get__(instance, owner)

    def __set__(self, instance: typing.Any, value: typing.Any) -> None:
        self._descriptor.__set__(instance, value)

    def __delete__(self, instance: typing.Any) -> None:
        self._descriptor.__delete__(instance)

    def __repr__(self) -> str:
        return self._descriptor.__repr__()


__all__ = ("MemberDescriptorProxy", "evaluate_operations")
