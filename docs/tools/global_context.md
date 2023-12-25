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

During global context initialization context variables can be set using keyword arguments:

`CtxVar(value: T, *, const: bool = False)`

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(name="Alex", url=CtxVar("https://google.com", const=True))
```

You can get a context variable value using the magic methods `__getattr__`, `__getitem__` or method `.get_value()`:

`.get_value(var_name: str, value_type: type[T] = Any) -> Result[T, str]`

This method can check the value of a context variable for the type you passed.

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(arseny="cool programmer")
ctx.arseny  # 'cool programmer' (but an unknown type)
ctx["arseny"]  # 'cool programmer'
ctx.get_value("arseny", str).unwrap()  # 'cool programmer' (type 'str')
ctx.lul  # raises an exception 'NameError'
ctx.get_value("lul").unwrap()  # Result.Error
```

You can set the value of a context variable or create new context variable using the magic methods `__setattr__`, `__setitem__`:

```python
from telegrinder.tools.global_context import GlobalContext

ctx = GlobalContext()
ctx.value = 1  # cool!
ctx["items"] = ["1", "2", "3"]  # very nice!
```

You can delete a context variable using the magic methods `__delattr__`, `__delitem__`:

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(first=1, second=CtxVar(2, const=True))
del ctx.value  # cool!
del ctx["second"]  # you can't delete const context variable!
```

If you want to get a context variable use the method `.get()`:

`.get(var_name: str, var_value_type: type[T] = Any) -> Result[GlobalCtxVar[T], str]`


```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
URL = ctx.get("URL", int)  # AssertionError: "Context variable value type of 'str' does not correspond to the expected type 'int'."
URL = ctx.get("URL", str).unwrap()  # <GlobalCtxVar(URL=ConstCtxVar(value='https://google.com'))>
```

Use the `.clear()` method to clear the context:

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

The global context can be typed as follows:

```python
import typing

from telegrinder.tools.global_context import GlobalContext, ctx_var

class MyGlobalContext(GlobalContext):
    __ctx_name__ = "my_ctx"

    name: str
    URL: typing.Final = ctx_var("https://google.com", const=True)
    # note: type hints typing.Final, typing.ClassVar mark the fields as a constant, so such fields will not be present in the __init__ signature.

ctx = MyGlobalContext(name="Alex") # <'MyGlobalContext@my_ctx' -> (<GlobalCtxVar(name=<CtxVar(value='Alex')>)>, <GlobalCtxVar(URL=<ConstCtxVar(value='https://google.com')>)>)> 
```

Function `ctx_var(value: T, *, const: bool = False) -> T` is the same as dataclass `CtxVar` but it returns this dataclass as type T.


`__iter__`, `__contains__`, `__eq__`, `__bool__` magic methods:

```python
from telegrinder.tools.global_context import GlobalContext

ctx1 = GlobalContext(items=[1, 2, 3], state=False)
ctx_vars = list(ctx1)
assert "items" in ctx1 and "name" not in ctx1  # ok
assert ctx1  # ok, because context is not empty
ctx2 = GlobalContext()
assert ctx1 == ctx2  # ok, because same context name
```

Telegrinder has a basic type-hinted global context `TelegrinderCtx` (context name `'telegrinder'`):

```python
from telegrinder.tools.global_context import TelegrinderCtx
```