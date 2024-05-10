# Global Context

The `GlobalContext` class was created to store context globally.

`GlobalContext(ctx_name: str | None = None, /, **variables: Any | CtxVar[Any])`

```python
from telegrinder.tools.global_context import GlobalContext
```

Context can be named:

```python
from telegrinder.tools.global_context import GlobalContext

ctx = GlobalContext()  # without name
ctx_with_name = GlobalContext("context")  # with name 'context'
```

Context variables can be set in `.__init__()` using keyword arguments:

`CtxVar(value: T, *, const: bool = False)`

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(name="Alex", url=CtxVar("https://google.com", const=True))
```

Get a context variable value using the magic methods `__getattr__`, `__getitem__` or method `.get_value()`:

`.get_value(var_name: str, value_type: type[T] = Any) -> Result[T, str]`

This method can check the value of a context variable for the type you passed.

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(arseny="cool programmer")
ctx.arseny  # 'cool programmer' (but an unknown type)
ctx["arseny"]  # 'cool programmer'
ctx.get_value("arseny", str).unwrap()  # 'cool programmer' (type 'str')
ctx.lul  # raises an exception 'NameError'
ctx.get_value("wupi woop").unwrap()  # UnwrapError: Name 'wupi woop' is not defined in global context.
```

Set the value of a context variable or create new context variable using the magic methods `__setattr__`, `__setitem__`:

```python
from telegrinder.tools.global_context import GlobalContext

ctx = GlobalContext()
ctx.kitten = Kitten(...)  # cool!
ctx["items"] = ["Oopa", "Loopa", "Woopa"]  # very nice!
```

Delete a context variable using the magic methods `__delattr__`, `__delitem__`:

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(first="woop", second=CtxVar("wop", const=True))
del ctx.woop  # cool!
del ctx["wop"]  # you can't delete const context variable!
```

Get a context variable use the method `.get()`:

`.get(var_name: str, var_value_type: type[T] = Any) -> Result[GlobalCtxVar[T], str]`


```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
URL = ctx.get("URL", int)  # AssertionError: "Context variable value type of 'str' does not correspond to the expected type 'int'."
URL = ctx.get("URL", str).unwrap()  # <GlobalCtxVar(URL=ConstCtxVar(value='https://google.com'))>
```

`.clear()` method to clear the context:

`.clear(*, include_consts: bool = False) -> None`

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
ctx.clear()  # clears the context (except constants)
ctx.clear(include_consts=True)  # clears the context
```

Delete context using the `.delete_ctx()` method:

`.delete_ctx() -> Result[None, str]`

```python
from telegrinder.tools.global_context import GlobalContext

ctx = GlobalContext("context")
ctx.delete_ctx().unwrap()  # ok!

ctx = GlobalContext()
ctx.delete_ctx().unwrap()  # error! you cant delete ctx without name!
```

Renaming a context variable using the `.rename()` method:

`.rename(old_var_name: str, new_var_name: str) -> Result[None, str]`

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(georgy="cool", telegrinder=CtxVar("cool", const=True))
ctx.rename("georgy", "arseny").unwrap()
ctx.arseny  # 'cool'
ctx.georgy  # is not defined in global context
ctx.rename("telegrinder", "other framework").unwrap()  # error! you cant rename const context varible!
```

The global context can be type-hinted:

```python
import typing

from telegrinder.tools.global_context import GlobalContext, ctx_var

class MyGlobalContext(GlobalContext):
    __ctx_name__ = "my_ctx"

    supplier: str
    COOKIES: typing.Final[set[str]] = CtxVar({"chocolate", "chip", "cracker"}, const=True)
    # NOTE: type hints typing.Final, typing.ClassVar mark the fields as a constant, so such fields will not be present in the __init__ signature.

ctx = MyGlobalContext(supplier="Brooklyn Born Chocolate")  # <'MyGlobalContext@my_ctx' -> (<GlobalCtxVar(supplier=<CtxVar(value='Brooklyn Born Chocolate')>)>, <GlobalCtxVar(COOKIES=<ConstCtxVar(value={'chocolate', 'chip', 'cracker'})>)>)> 
```

Function `ctx_var(value: T, *, const: bool = False) -> T` is the same as dataclass `CtxVar` but it returns this dataclass as type T.


`__iter__`, `__contains__`, `__eq__`, `__bool__` magic methods:

```python
from telegrinder.tools.global_context import GlobalContext

global_ctx = GlobalContext(db_session=DatabaseSession(...), waiter_machine=WaiterMachine())
ctx_vars = list(ctx1)
assert "db_session" in global_ctx and "http_client" not in global_ctx  # ok
assert global_ctx  # ok, because context is not empty
other_ctx = GlobalContext()
assert global_ctx == other_ctx  # ok, because same context name
```

Telegrinder has a basic type-hinted global context `TelegrinderCtx` __(context name `telegrinder`)__:

```python
from telegrinder.tools.global_context import TelegrinderCtx
```