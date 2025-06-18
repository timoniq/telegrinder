# Functional bits

As you probably noticed earlier in telegrinder we use some freaky constructions like `.unwrap()`, `.map()` and others. If you previously have had experience with some functional languages this concepts might be easy to grasp for you, but even if not, this article will explain why it is so useful.

In python libraries mostly raise exceptions in case something goes wrong. We think this approach is bad. Why? Its hard to tell which exceptions the function call might raise. The exception might appear somewhere deep inside dependency modules and what you get is something unexpected. As programmers, we try to avoid unexpected behaviour, thats why we try to implement good type hinting into telegrinder. With exceptions - that becomes very hard.

The solution is instead of raising an exception we say that function may RETURN two possible states of result. An error if something is not right, or a value if everything went right.

We use `fntypes` to provide a functional backend for telegrinder. Lets look into some simple examples.

Lets write a function using fntypes backend so we can understand the concept on the deep level.

```python
from fntypes import Result, Ok, Error

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Error("Cannot divide by zero")
    return Ok(a / b)
```

Thats a function which allows us to safely divide `a` by `b`. Since we cannot divide by zero, in case we get it as a divisor we return `Error`. If everything is great, we get `Ok` with an actual result of the division.

Fntypes provides many built-in utilities to work with its instances.

One of them, which you have probably seen already is `.unwrap()`.

Its actually a way to turn control flow into the one we are used to. If we get an error inside, the exception will be raised, if value, we will simply turn our result into one value.

```python
divide(6, 3).unwrap() == 2
divide(3, 0).unwrap()  # Exception UnwrapError("Cannot divide by zero")
```

[Advanced documentation with all methods](https://github.com/timoniq/fntypes/blob/main/docs/result.md#application)

---

Now we can quickly build chains and control what to do with our errors.

```python
result = (
    divide(6, 2)  # We divide and get the result
    .map(int)     # If the result is successful, we cast int onto it. int(3.0) == 3
    .then(lambda x: divide(x, 3))  # If the result is successful, we get new result after doing our second division
    .map_or(0)    # This will replace error state with successful state of a default value (0)
)
```

We strictly control what we get from this chain and avoid losing control over it with some exception. The result of this chain is going to be `Result[float, str]`.

We can process it like this:

```python
match result:
    case Ok(value):
        print("Value is", value)
    case Err(err):
        print("Something is wrong:", err)
```

or we can transform error into custom exception with `expect`

```python
result.expect(ZeroDivisionError())  # 1
```

I know, this looks abstract at this point but playing around with these types will help you nicely to build good stuff using telegrinder. The first practical usage is going to happen in the very next article since we are going to work with API methods and they may result in these exact two states: an error and a value.

[>> Next: API](4_api.md)
