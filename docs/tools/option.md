# Option

Telegrinder has models built on `msgspec.Struct` that use the `Option` monad instead of the `typing.Optional` type:

```python
from telegrinder.option.msgspec_option import Option  # special protocol for msgspec models
from telegrinder.option import Some, NothingType
from telegrinder.types import User
from telegrinder.model import Model
from telegrinder import API, Token

api = API(Token.from_env())


# Option usage instead of typing.Optional:
class Admin(Model):
    name: str
    age: int
    bio: Option[str] = Nothing


async def main():
    me = (await api.get_me()).unwrap()
    print("my last name is", me.last_name.unwrap_or("Unknown"))

    match me.username:
        case Some(username):
            print("my username is", username)
        case _:
            print("oops...")
```

`Option` monad example:

```python
import typing

from telegrinder.option import Nothing, Option, Some

T = typing.TypeVar("T")


def cast_obj(obj: object, type: type[T]) -> Option[T]:
    try:
        return Some(type(obj))
    except (ValueError, TypeError):
        return Nothing


str_to_int = cast_obj("123", int).unwrap()  # 123
int_to_list = cast_obj(123, list).unwrap()  # ValueError: Nothing to unwrap.
```

`Option` methods:
* `unwrap`
* `unwrap_or`
* `unwrap_or_else`
* `unwrap_or_other`
* `map`
* `map_or`
* `map_or_else`
* `expect`
