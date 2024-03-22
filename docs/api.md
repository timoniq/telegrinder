# API

API instance is used to make telegram bot api requests.

It is derived from ABCAPI which guarantees implementation of `request` and `request_raw` methods.

`telegrinder.API` instance is fully typed and implements all the methods provided by telegram bot api.

Initialization:

```python
from telegrinder import API, Token
api = API(Token("token"))
```

## Using typed methods

All methods are in snake case and return a result of model or APIError.

More about results [here](tools/result.md).

```python
user = (await api.get_me()).unwrap()
user.first_name
```

## `.request`

Makes a request with `request_raw`, returns result with parsed data (list, dict or boolean) or APIError.

```python
result = await api.request("getMe", {})
result.unwrap()["first_name"]
```

## `.request_raw`

Makes a request to telegram instance serving at `.request_url`.

Returns result with `msgspec.Raw` data or `APIError`.

```python
result = await api.request_raw("getMe", {})
json.loads(result.unwrap())["first_name"]
```

## APIError

`telegrinder.APIError` contains `code` and `error`

```python
from telegrinder import Result, APIError, Error
result: Result[bool, APIError] = get_result()

match result:
    case Error(err):
        print(err.code, err.error)
```
