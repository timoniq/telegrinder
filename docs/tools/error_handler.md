# Error Handler

Error Handler is used to handle exceptions.
```python
from telegrinder.tools.error_handler import ErrorHandler
```

Abstact interface:
```python
from telegrinder.tools.error_handler import ABCErrorHandler
```

The catcher is a dataclass that contains:
* `function` - Catcher function
* `exceptions` - List of exceptions
* `logging` - Logging the result of the catcher at the level `DEBUG`
* `ignore_exceptions` - Ignoring all exceptions
* `raise_exception` - Raise an exception if it occurs during the catcher's execution

```python
from telegrinder.tools.error_handler import Catcher
```

Decorator to register the catcher function has paramaters:
* `exceptions` - The exceptions to be caught;
* `logging` - Logging the result of the catcher at the level `DEBUG`;
* `ignore_errors` - Ignoring errors that may occur;
* `raise_exception` - Raising an exception if it occurs during the catcher's execution.

```python
from telegrinder.tools.error_handler import ErrorHandler

error_handler = ErrorHandler()


@error_handler(NameError, ValueError("Wrong value!"), logging=True, ignore_errors=True, raise_exception=False)
async def some_catcher(exception: NameError | ValueError) -> None:
    print("Oops...")
```

The catcher function *_always accepts the error object as its first parameter_*, which has no specific name, and can also accept two optional arguments:

* `api` - API instance;
* `event` - Incoming event.

Additionally some parameters from the context and the catcher function can return a value for `ReturnManager`.

`.run()` method:

* `handler` - The handler that needs to be processed;
* `event` - Incoming event;
* `api` - API instance;
* `ctx` - Context instance.

```python
from telegrinder.tools.error_handler import ErrorHandler

error_handler = ErrorHandler()


async def some_handler(message: Message, value: int):
    if value == 123:
        raise ValueError("Wrong value!")


@error_handler(NameError, ValueError("Wrong value!"), logging=True, ignore_errors=True, raise_exception=False)
async def some_catcher(exception: NameError | ValueError) -> None:
    print(exception)


asyncio.run(error_handler.run(some_handler, Message(...), API(...), Context(value=123))))
```
