# Global Context

The global context stores values for the entire program that can be set by name. The base global context inherits from the `dict` class, so it works like a `dict` object.
```python
from telegrinder.tools.global_context import GlobalContext
```

Abstact interface:
```python
from telegrinder.tools.global_context import ABCGlobalContext
```

The global context can be named:
```python
from telegrinder.tools.global_context import GlobalContext

ctx = GlobalContext()  # unnamed
assert ctx != GlobalContext("context")
```

Context variables can be set in `__init__()` by kwargs:
```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(name="Alex", url=CtxVar("https://google.com", const=True))
```

Get the value of a context variable with the provided type:
```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(arseny="cool programmer")
ctx.arseny  # 'cool programmer' (unknown type)
ctx["arseny"]  # 'cool programmer' (unknown type)
ctx.get_value("arseny", str).unwrap()  # 'cool programmer' (type 'str')
ctx.lul  # NameError: Name 'lul' is not defined in '<Unnamed global context at 0x7f8d07eb1f80>'.
ctx.get_value("wupi woop").unwrap()  # UnwrapError: Name 'wupi woop' is not defined in '<Unnamed global context at 0x7f8d07eb1f80>'.
```

Set the value of a context variable:
```python
from telegrinder.tools.global_context import GlobalContext

ctx = GlobalContext()
ctx.kitten = Kitten()  # cool!
ctx["items"] = ["Oopa", "Loopa", "Woopa"]  # very nice!
```

Delete a context variable:
```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(first="woop", second=CtxVar("wop", const=True))
del ctx.woop  # cool!
del ctx["wop"]  # cannot delete const context variable!
```

Get a context variable with the provided type:
```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
URL = ctx.get("URL", int)  # AssertionError: "Context variable value type of 'str' does not correspond to the expected type 'int'."
URL = ctx.get("URL", str).unwrap()  # <GlobalCtxVar(URL=ConstCtxVar(value='https://google.com'))>
```

Clear the global context:
```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
ctx.clear()  # exclude constants
ctx.clear(include_consts=True)
```

Delete the global context:
```python
from telegrinder.tools.global_context import GlobalContext

ctx = GlobalContext("context")
ctx.delete_ctx().unwrap()  # ok!

ctx = GlobalContext()
ctx.delete_ctx().unwrap()  # error: cannot delete unnamed context!
```

Renaming a context variable:
```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

ctx = GlobalContext(georgy="cool", telegrinder=CtxVar("cool", const=True))
ctx.rename("georgy", "arseny").unwrap()
ctx.arseny  # 'cool'
ctx.georgy  # is not defined
ctx.rename("telegrinder", "other framework").unwrap()  # error: cannot rename const context variable!
```

The global context can be type-hinted:
```python
import typing

from telegrinder.tools.global_context import GlobalContext, ctx_var


class MyGlobalContext(GlobalContext):
    __ctx_name__ = "context"

    supplier: str
    COOKIES: typing.Final[set[str]] = ctx_var(default={"chocolate", "chip", "cracker"}, const=True, init=False)

ctx = MyGlobalContext(supplier="Brooklyn Born Chocolate")  # <MyGlobalContext@context contains variables: <GlobalCtxVar(supplier=<CtxVar(value='Brooklyn Born Chocolate')>)>, <GlobalCtxVar(COOKIES=<ConstCtxVar(value={'chocolate', 'chip', 'cracker'})>)>>
```

The GlobalContext has a magic methods `__iter__`, `__contains__`, `__eq__`, `__bool__`:
```python
from telegrinder.tools.global_context import GlobalContext

global_ctx = GlobalContext(db_session=DatabaseSession(...), waiter_machine=WaiterMachine())
ctx_vars = list(ctx1)
assert "db_session" in global_ctx and "http_client" not in global_ctx  # ok
assert global_ctx  # ok, is not empty
other_ctx = GlobalContext()
assert global_ctx == other_ctx  # ok, same
```

A built-in type-hinted global context:
```python
from telegrinder.tools.global_context import TelegrinderContext
```
