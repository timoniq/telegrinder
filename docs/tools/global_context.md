# Global Context

To store globally throughout the project variables in Telegrinder there is a class called GlobalContext.

`GlobalContext(ctx_name: str | None = None, /, **vars: Any | CtxVar[Any])`

```python
from telegrinder.tools.global_context import GlobalContext
```

For contexts, you can assign names by passing a string with the desired context name to the `GlobalContext` class constructor. For contexts, you can assign names by passing the first string with the desired context name to the GlobalContext class constructor. By implication, the `None` value means that the context is nameless.

```python
from telegrinder.tools.global_context import GlobalContext

gc1 = GlobalContext()  # without name
gc2 = GlobalContext("my_ctx")  # with name 'my_ctx'
```

When you initialize a GlobalContext class transcript, we can transfer variables there via keyword args:

```python
from telegrinder.tools.global_context import GlobalContext

gc = GlobalContext(name="Alex", url="https://google.com")
```

The context variable can be both changeable and unaltered. To make it unalterable, use dataclass CtxVar:

`CtxVar(value: T, *, const: bool = False)`

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

gc = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
```

You can set, get, delete a context variable value using the magic methods of class `__setattr__`, `__getattr__`, `__delattr__`:

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

gc = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
gc.URL  # 'https://google.com'
gc.name = "Max"
del gc.name  # ok if the variable is not const
```

If you want to get a context variable directly use the .get() method:

`GlobalContext.get(name: str, value_type: type[T] = Any) -> Result[GlobalCtxVar[T], str]`

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

gc = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
URL = gc.get("URL", str).unwrap()  #: <GlobalCtxVar(URL=ConstCtxVar(value='https://google.com'))>
```

Use the .clear() method to clear the context:

`GlobalContext.clear(*, include_consts: bool = False) -> None`

```python
from telegrinder.tools.global_context import GlobalContext, CtxVar

gc = GlobalContext(name="Alex", URL=CtxVar("https://google.com", const=True))
gc.clear()  # clear the conex leaving only const variables
gc.clear(include_consts=True)  # clear full context (get a warning from logger)
```

We can also remove our named context using the .delete_ctx() method

`GlobalContext.delete_ctx() -> Result[None, str]`

```python
from telegrinder.tools.global_context import GlobalContext

gc = GlobalContext("my_ctx")
gc.delete_ctx()
```

There is a .rename() method to change the name of a context variable

`GlobalContext.rename(old_name: str, new_name: str) -> Result[None, str]`

```python
from telegrinder.tools.global_context import GlobalContext

gc = GlobalContext(name="Alex")
gc.rename("name", "first_name").unwrap()
gc.first_name  # 'Alex'
gc.name  # is not defined in global context
```

It is possible to specify the necessary types of context variables for the `GlobalContext`:

```python
import typing

from telegrinder.tools.global_context import GlobalContext, ctx_var

class MyGlobalContext(GlobalContext):
    __ctx_name__ = "my_ctx"

    name: str
    URL: typing.Final[str] = ctx_var("https://google.com", const=True)

gc = MyGlobalContext(name="Alex")
# gc: <'MyGlobalContext@my_ctx' -> (<GlobalCtxVar(name=<CtxVar(value='Alex')>)>, <GlobalCtxVar(URL=<ConstCtxVar(value='https://google.com')>)>)> 
```

Where: `__ctx_name__ = "my_ctx"` is specified not to pass the name to the constructor if we need for named context; `ctx_var()` function that returns the dataclass CtxVar but under the value type we passed.

Signature: `ctx_var(value: T, *, const: bool = False) -> T`

`__iter__`, `__contains__`, `__eq__`, `__bool__` magic methods:

```python
import typing

from telegrinder.tools.global_context import GlobalContext, GlobalCtxVar

gc1 = GlobalContext(items=[1, 2, 3], state=False)
gc2 = GlobalContext()
gc_ctx_vars: list[GlobalCtxVar[typing.Any]] = list(gc)
assert "items" in gc1 and "name" not in gc1
assert gc1 == gc2  # ok because same context name
assert gc1  # ok because context is not empty
```

Telegrinder has a basic typed global context class whose name is `TelegrinderCtx`:

```python
from telegrinder.tools import TelegrinderCtx
```

This class uses the `Telegrinder` itself. The name of the `'telegrinder'` context.