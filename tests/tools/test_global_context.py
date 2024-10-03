import typing

import pytest
from fntypes.option import Nothing

from telegrinder.tools.global_context import (
    CtxVar,
    GlobalContext,
    GlobalCtxVar,
    ctx_var,
)


def test_init_anonymous_global_ctx():
    ctx = GlobalContext(value=123)
    assert ctx
    assert "value" in ctx


def test_init_with_name_global_ctx():
    ctx = GlobalContext("context", number=1)

    assert ctx
    assert "number" in ctx
    assert ctx.ctx_name != GlobalContext(number=1).ctx_name


def test_get_value_from_global_ctx():
    ctx = GlobalContext(first_name="Alex")
    ctx.country = "Russia"

    assert ctx.first_name == "Alex"
    assert ctx.country == "Russia"
    assert ctx.get("var") == Nothing()
    assert ctx.get_value("country", str) != Nothing()

    with pytest.raises(
        AssertionError,
        match="Context variable value type of 'str' does not correspond to the expected type 'int'.",
    ):
        ctx.get_value("first_name", int)


def test_set_value_in_global_ctx():
    ctx = GlobalContext()
    ctx.counter = {}
    ctx.start_id = CtxVar(20, const=True)
    ctx.colors = GlobalCtxVar("colors", ("Red", "Green", "Blue"), const=True)

    assert "counter" in ctx
    assert "start_id" in ctx
    assert "colors" in ctx
    assert ctx.counter == {}
    assert ctx.start_id == 20
    assert ctx.colors == ("Red", "Green", "Blue")
    assert ctx.get("counter").unwrap().const is False
    assert ctx.get("start_id").unwrap().const is True
    assert ctx.get("colors").unwrap().const is True

    with pytest.raises(TypeError, match="Unable to set variable 'start_id', because it's a constant."):
        ctx.start_id = 0


def test_del_value_from_global_ctx():
    ctx = GlobalContext(ip="123.123.123.123", port=8888, flag=False)
    del ctx.ip
    del ctx.port

    assert "ip" not in ctx
    assert "port" not in ctx
    assert ctx.pop("flag", bool) != Nothing()
    assert not ctx

    ctx.URL = CtxVar("https://google.com", const=True)
    with pytest.raises(TypeError, match="Unable to delete variable 'URL', because it's a constant."):
        del ctx.URL


def test_global_ctx_with_generic():
    IntGlobalContext = GlobalContext[int]  # noqa: N806
    ctx = IntGlobalContext(one=1, two=2)

    assert isinstance(ctx.one, int)
    assert isinstance(ctx.two, int)
    assert ctx.get_value("one", int) is not Nothing
    assert ctx.get_value("two", int) is not Nothing


def test_rename_var_in_global_ctx():
    ctx = GlobalContext(name="Alex", user_id=CtxVar("123", const=True))

    assert ctx.rename("name", "first_name")
    assert "name" not in ctx
    assert "first_name" in ctx
    assert ctx.first_name == "Alex"

    assert not ctx.rename("user_id", "id")
    assert "user_id" in ctx
    assert "id" not in ctx
    assert ctx.user_id == "123"


def test_clear_global_ctx():
    ctx = GlobalContext(temp=[], state=True)
    ctx.clear()

    assert not ctx
    ctx = GlobalContext(machine=CtxVar("Machine", const=True))
    ctx.clear(include_consts=True)
    assert not ctx


def test_copy_global_ctx():
    ctx = GlobalContext(first=1, second=2, third=3)
    new_ctx = ctx.copy()
    del new_ctx.first

    assert id(ctx) != id(new_ctx)
    assert "first" in ctx
    assert "first" not in new_ctx


def test_delete_ctx_from_global_ctx():
    ctx = GlobalContext("my_context", gun="m4a1", name="John")

    assert ctx.delete_ctx()
    del ctx
    assert not GlobalContext("my_context")


def test_create_global_ctx_with_inheritance():
    class LittleContext(GlobalContext):
        __ctx_name__ = "my_little_ctx"

        flag: bool
        control_id: int
        states: typing.Final[list[bool]] = ctx_var([], frozen=True)

    ctx = LittleContext(flag=False, control_id=111, states=[True, True, False, True, False])

    assert ctx.ctx_name == "my_little_ctx"
    assert isinstance(ctx, GlobalContext)
    assert issubclass(LittleContext, GlobalContext)

    assert "flag" in ctx
    assert "control_id" in ctx
    assert "states" in ctx

    assert ctx.get_value("flag", bool)
    assert ctx.get_value("control_id", int)
    assert ctx.get_value("states", list[bool])
