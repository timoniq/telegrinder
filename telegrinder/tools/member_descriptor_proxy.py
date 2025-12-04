from __future__ import annotations

import dataclasses
import operator
import types
import typing

type Operation = GetAttribute | GetItem | MethodCall


def evaluate_operations(
    obj: typing.Any,
    member_name: str,
    operations: list[Operation],
    /,
) -> typing.Any:
    obj = getattr(obj, member_name)

    for operation in operations:
        match operation:
            case GetAttribute(attribute_name=attribute_name):
                obj = getattr(obj, attribute_name)
            case GetItem():
                obj = operation[obj]
            case MethodCall():
                obj = operation(obj)

    return obj


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class MethodCall:
    caller: operator.methodcaller

    def __call__(self, obj: typing.Any, /) -> typing.Any:
        return self.caller(obj)


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class GetAttribute:
    attribute_name: str


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class GetItem:
    itemgetter: operator.itemgetter[typing.Any]

    def __getitem__(self, obj: typing.Any, /) -> typing.Any:
        return self.itemgetter(obj)


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

        self._operations.append(GetAttribute(attribute_name=__name))
        return self

    def __getitem__(self, __item: typing.Any) -> typing.Any:
        self._operations.append(GetItem(itemgetter=operator.itemgetter(__item)))
        return self

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        if not self._operations or not isinstance(operation := self._operations.pop(-1), GetAttribute):
            raise SyntaxError("No operations to call.")

        self._operations.append(MethodCall(caller=operator.methodcaller(operation.attribute_name, *args, **kwargs)))
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
