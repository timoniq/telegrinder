# Optional Dependecies

## A table of the default and optional dependecies

| Default      | Optional                                                                                           |
| ------------ | ---------------------------------------------------------------------------------------------------|
| [asyncio](https://docs.python.org/3/library/asyncio.html)      | [uvloop](#uvloop)                                |
| [logging](https://docs.python.org/3/library/logging.html)      | [loguru](#loguru)                                |

### [uvloop](https://github.com/MagicStack/uvloop)
Telegrinder uses the `asyncio` event loop and when you install `uvloop`, `uvloop.EventLoopPolicy()` will be automatically set:
```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```


### [loguru](https://github.com/Delgan/loguru)
If this dependency is installed it is used instead of the default `logging` std module.

Telegrinder supports env variable to set a logging level: `LOGGER_LEVEL`, the default is `DEBUG`.

There is a function to set a logging level for both `logging` or `loguru`:
```python
from telegrinder.modules import logger

logger.set_level("INFO")
```
