import typing

from msgspec.structs import Struct


class Model(Struct, omit_defaults=True):
    pass


class Schema(Model):
    version: str
    release_date: str
    changelog: str
    methods: list["MethodSchema"]
    types: list["TypeSchema"]


class MethodSchema(Model):
    name: str
    href: str
    returns: typing.Optional[list[str]] = None
    description: typing.Optional[list[str]] = None
    fields: typing.Optional[list["Field"]] = None


class TypeSchema(Model):
    name: str
    href: str
    description: typing.Optional[list[str]] = None
    fields: typing.Optional[list["Field"]] = None


class Field(Model):
    name: str
    types: list[str]
    required: bool = False
    description: typing.Optional[str] = None
