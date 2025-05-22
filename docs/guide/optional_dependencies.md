# Optional Dependecies

## A table of the default and optional dependecies

| Default      | Optional                                                                                           |
| ------------ | ---------------------------------------------------------------------------------------------------|
| [asyncio](https://docs.python.org/3/library/asyncio.html)      | [uvloop](#uvloop)                                |
| [logging](https://docs.python.org/3/library/logging.html)      | [loguru](#loguru)                                |
| [base64](https://docs.python.org/3/library/base64.html)        | [brotli](#brotli)                                |
| *None*                                                         | [socks](#aiohttp-socks)                          |


Installing all optional dependecies:
```console
pip install "telegrinder[all]"
```

### [uvloop](https://github.com/MagicStack/uvloop)
```console
pip install "telegrinder[uvloop]"
```

Telegrinder uses the `asyncio` event loop and when you install `uvloop`, `uvloop.EventLoopPolicy` will be automatically set:
```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```

### [loguru](https://github.com/Delgan/loguru)
```console
pip install "telegrinder[loguru]"
```

If this dependency is installed it is used instead of the default `logging` std module.

Telegrinder supports env variable to set a logging level: `LOGGER_LEVEL`, the default is `DEBUG`.

There is a function to set a logging level for both `logging` or `loguru`:
```python
from telegrinder.modules import logger

logger.set_level("INFO")
```

### [brotli](https://github.com/google/brotli)
Brotli is required for `telegrinder.tools.callback_data_serilization.MsgPackSerializer`, which provides a much more compact encode data.
```console
pip install "telegrinder[brotli]"
```

### [aiohttp-socks](https://github.com/romis2012/aiohttp-socks)
```console
pip install "telegrinder[socks]"
```

The `aiohttp-socks` dependency provides a proxy connector for `telegrinder.client.aiohttp.AiohttpClient`.

```python
from telegrinder.api.api import API
from telegrinder.client.aiohttp import AiohttpClient

SOCKS5_DSN = "socks5://user:password@127.0.0.1:1080"

client = API(token=..., http=AiohttpClient(proxy=SOCKS5_DSN))
```
