import inspect
import types
import typing

import msgspex

from telegrinder.tools.member_descriptor_proxy import MemberDescriptorProxy


class Model(msgspex.Model):
    def __init_subclass__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        super().__init_subclass__(*args, **kwargs)

        for member_name, descriptor in dict(
            inspect._getmembers(  # type: ignore
                cls,
                lambda v: isinstance(v, types.MemberDescriptorType | property),
                lambda obj, key: obj.__dict__.get(key),
            ),
        ).items():
            setattr(cls, member_name, MemberDescriptorProxy(descriptor, cls))

        return None


__all__ = ("Model",)
