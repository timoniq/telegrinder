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


### Method `add_task`

The `add_task` method is used to schedule a task in the `LoopWrapper`. If the `LoopWrapper` is not yet running, the task is simply added to an internal list of tasks and will be scheduled when the loop starts. If the `LoopWrapper` is already running, the task is immediately created and added to the list of active tasks.

In summary:

- If the loop is not running, tasks are queued.
- If the loop is running, tasks are immediately scheduled.

This allows you to prepare tasks before starting the loop or add new tasks on the fly while the loop is active.


### Method `create_task`

This method is an asynchronous and it does the same as `add_task`, but with an important difference when a task limit is set using the `limit()` method:

- If a limit is defined, `create_task` will asynchronously wait for permission to create the task.
- It uses the internal `semaphore's` acquire() method to determine whether a new task can be started immediately or if it needs to wait for another task to complete and release the semaphore.

This behavior ensures that the task limit is respected:

- If the limit has been reached, `create_task` waits for an available slot.
- If a slot is available, it proceeds to create and schedule the task.

For this reason, when the `LoopWrapper` is running and you want to schedule new tasks dynamically with a task limit in place, it is recommended to use `create_task`. This ensures that your code properly waits for available slots and respects the concurrency limit.


### Limitation of the number of tasks

If you need to limit the number of tasks created in the event loop, there is a method-builder `limit` that sets the limit on the number of created tasks.

```python
import asyncio

from telegrinder.tools import LoopWrapper

loop_wrapper = LoopWrapper().limit(10)


async def task(identifier: int):
    print(f"Task #{identifier}")
    await asyncio.sleep(1)


for identifier in range(15):
    loop_wrapper.add_task(task(identifier + 1))


loop_wrapper.run()
```

In this example, we use the `LoopWrapper` to limit the number of concurrent tasks. Internally, loop wrapper uses an `asyncio.Semaphore` to ensure that no more than 10 tasks are running at the same time. When one of the running tasks completes (after sleeping for 1 second in this example), the semaphore is released, allowing the next task to start.

This behavior resembles a `"traffic light"` system:

- The first 10 tasks are immediately started and "sleep" for 1 second.
- The remaining tasks wait for the semaphore to be released ("the green light") before they can start.
- As each task completes, it signals the semaphore, allowing new tasks to start in a controlled and safe manner.


### Creating startup and shutdown tasks

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

### Using with `asyncio`

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
