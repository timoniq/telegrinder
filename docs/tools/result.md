# Result

Telegrinder is built upon the concept of result monad. This means that instead of raising an exception returning result is preferred. In this way it is easier to created typed code and avoid try-except constructs.

```python
from telegrinder import Result, Ok, Error

def function(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Error("Cannot divide by zero")
    return Ok(a / b)

def main():
    a = get_a()
    b = get_b()

    match function(a, b):
        case Ok(c):
            print("I did it!", c)
        case Error(msg):
            print("Oops, error:", msg)
```

In telegrinder framework this is used to work with api requests.

```python
from telegrinder import API
from telegrinder.types import User

api = API()

def repr_user(user: User) -> str:
    ...

async def main():
    my_name = (await api.get_me()).map(repr_user).unwrap_or("unknown")
    print("My name is", my_name)
```
