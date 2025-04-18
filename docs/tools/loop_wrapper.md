# Loop Wrapper

This handy tool to create tasks before and after running the event loop, as well run on startup and shutdown tasks of the event loop. Loop Wrapper processes all tasks within the event loop, logs exceptions if any in task and handles the `KeyboardInterrupt` exception, ensuring the `SAFE` cancellation of all pending tasks.

```python
from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper()


async def main():
    await open_db_connection()
    await close_db_connection()


loop_wrapper.add_task(main())
loop_wrapper.run()
```

It is worth mentioning that LoopWrapper is a singleton. However, it is possible to pass the `loop` or `loop_factory` parameters to the `.bind_loop` method, which provide the event loop to be used. For reference, the built-in global context (`TelegrinderContext`) instantiate of the LoopWrapper at runtime.

```python
import asyncio

from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper.bind_loop(loop_factory=asyncio.new_event_loop)
```

> [!NOTE]
> If `loop` or `loop_factory` is not specified, `asyncio.get_event_loop` will be used by default.

The `LoopWrapper` has several properties:

* `lifespan` – Lifespan instance for creating startup and shutdown tasks.
* `event_loop` – Event loop instance.
* `running` – State of LW; True if the Loop Wrapper is running, otherwise False.


Creating startup and shutdown tasks
```python
from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper()


@loop_wrapper.lifespan.on_startup
async def start():
    await open_db_connection()


@loop_wrapper.lifespan.on_shutdown
async def shut():
    await close_db_connection()


async def main():
    print("sleep")
    await asyncio.sleep(10)
    print("wakeup")


loop_wrapper.add_task(main())
loop_wrapper.run()
```

Using with `asyncio`
```python
import asyncio
from contextlib import suppress

from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper()


async def task() -> None:
    print("sleep task1")
    await asyncio.sleep(10)
    print("wakeup task1")


async def main() -> None:
    print("sleep main function")
    await asyncio.sleep(15)
    print("wakeup main function")


loop_wrapper.add_task(task())


# You need to pass a LoopWrapper instance to the loop_factory parameter.
# A LoopWrapper instance has `__call__` method that returns an event loop object.
with suppress(KeyboardInterrupt):
    # suppress KeyboardInterrupt, because in this case the LoopWrapper will be running in task and will
    # not be responsible for control flow. As a result, asyncio.run will raise KeyboardInterrupt exception.
    asyncio.run(main=main(), loop_factory=loop_wrapper, debug=False)
```

> [!IMPORTANT]
> Loop Wrapper must always be running, as `Telegrinder` works directly with it. If another library creates a new event loop, Loop Wrapper will not be able to run on its own. So, to integrate it properly it is possible to pass an instance of `LoopWrapper` wherever a `loop_factory` is accepted or manually create an event loop, pass and set it using `asyncio.set_event_loop`. This ensures that `asyncio` works smoothly across different libraries without conflicts.

Loop Wrapper can create delayed tasks:
* `timer` — a one-shot timer that is set a preset time, after the time has elapsed calls the function.
* `interval` — a periodic timer, each time the interval timer expires it is calls the function and reloaded with the repetition interval.

```python
from datetime import timedelta

from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper()


@loop_wrapper.lifespan.on_startup
async def begin_cook_ravioli():
    print("nice, let's begin cooking the ravioli! they will be ready in 9 minutes.")


@loop_wrapper.timer(timedelta(minutes=9))
async def done_cook_ravioli():
    print("oki, ravioli ready! bon appetit ^_^")


@loop_wrapper.interval(seconds=30)
async def logging():
    data = await fetch_data()
    if data is not None:
        message = await create_log_message(data)
        await send_message_log(message)


loop_wrapper.run(close_loop=False)
```

> [!TIP]
> If you want to cancel a delayed task, the function decorated with the `timer()` or `interval()` has `.cancel()` method. This method returns True if the task was successfully canceled; otherwise, it returns False.

> [!NOTE]
> A canceled delayed task cannot be resumed.
